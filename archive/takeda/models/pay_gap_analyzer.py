"""
Gender Pay Gap Analyzer using regression-based decomposition.
Identifies unexplained pay gaps and generates correction recommendations.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from dataclasses import dataclass


@dataclass
class GapAnalysisResult:
    overall_gap_pct: float
    unexplained_gap_pct: float
    gap_by_country: pd.DataFrame
    gap_by_department: pd.DataFrame
    gap_by_level: pd.DataFrame
    regression_r2: float
    coefficients: dict


@dataclass
class CorrectionPlan:
    corrections: pd.DataFrame  # per-employee adjustments
    total_cost: float
    avg_raise_pct: float
    employees_affected: int


class PayGapAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.model = None
        self.encoder = None
        self._feature_cols = ["job_level", "years_experience", "country", "department", "education"]

    def compute_raw_gap(self) -> pd.DataFrame:
        """Compute raw (unadjusted) pay gap by various dimensions."""
        results = []

        # Overall
        m_mean = self.df[self.df["gender"] == "M"]["total_compensation"].mean()
        f_mean = self.df[self.df["gender"] == "F"]["total_compensation"].mean()
        results.append({
            "dimension": "Overall",
            "category": "All",
            "male_avg": m_mean,
            "female_avg": f_mean,
            "gap_pct": (m_mean - f_mean) / m_mean * 100,
            "male_count": len(self.df[self.df["gender"] == "M"]),
            "female_count": len(self.df[self.df["gender"] == "F"]),
        })

        # By country, department, level
        for dim in ["country", "department", "job_level"]:
            for cat, group in self.df.groupby(dim):
                m = group[group["gender"] == "M"]["total_compensation"]
                f = group[group["gender"] == "F"]["total_compensation"]
                if len(m) > 5 and len(f) > 5:
                    results.append({
                        "dimension": dim,
                        "category": str(cat),
                        "male_avg": m.mean(),
                        "female_avg": f.mean(),
                        "gap_pct": (m.mean() - f.mean()) / m.mean() * 100,
                        "male_count": len(m),
                        "female_count": len(f),
                    })

        return pd.DataFrame(results)

    def fit_regression(self) -> GapAnalysisResult:
        """
        Fit regression model controlling for legitimate factors.
        The gender coefficient represents the unexplained gap.
        """
        df = self.df.copy()

        # Encode categorical variables
        cat_cols = ["country", "department", "education"]
        num_cols = ["job_level", "years_experience"]

        self.encoder = OneHotEncoder(drop="first", sparse_output=False)
        cat_encoded = self.encoder.fit_transform(df[cat_cols])
        cat_names = self.encoder.get_feature_names_out(cat_cols)

        X = np.hstack([
            df[num_cols].values,
            cat_encoded,
            (df["gender"] == "F").values.reshape(-1, 1),
        ])
        feature_names = list(num_cols) + list(cat_names) + ["is_female"]

        y = np.log(df["total_compensation"].values)  # log transformation

        self.model = LinearRegression()
        self.model.fit(X, y)

        coefficients = dict(zip(feature_names, self.model.coef_))
        r2 = self.model.score(X, y)

        # Unexplained gap = gender coefficient (in log terms -> approx percentage)
        unexplained_gap_pct = abs(coefficients["is_female"]) * 100

        # Raw overall gap
        m_mean = df[df["gender"] == "M"]["total_compensation"].mean()
        f_mean = df[df["gender"] == "F"]["total_compensation"].mean()
        overall_gap_pct = (m_mean - f_mean) / m_mean * 100

        # Gap by country
        raw_gaps = self.compute_raw_gap()
        gap_by_country = raw_gaps[raw_gaps["dimension"] == "country"].copy()
        gap_by_department = raw_gaps[raw_gaps["dimension"] == "department"].copy()
        gap_by_level = raw_gaps[raw_gaps["dimension"] == "job_level"].copy()

        return GapAnalysisResult(
            overall_gap_pct=overall_gap_pct,
            unexplained_gap_pct=unexplained_gap_pct,
            gap_by_country=gap_by_country,
            gap_by_department=gap_by_department,
            gap_by_level=gap_by_level,
            regression_r2=r2,
            coefficients=coefficients,
        )

    def generate_corrections(self, budget_pct: float = 100.0) -> CorrectionPlan:
        """
        Generate per-employee salary corrections to close the unexplained gap.
        budget_pct: percentage of full correction to apply (100 = full correction).
        """
        if self.model is None:
            self.fit_regression()

        df = self.df.copy()
        female_mask = df["gender"] == "F"
        female_df = df[female_mask].copy()

        # Predict what each female employee SHOULD earn (with gender coef = 0)
        cat_cols = ["country", "department", "education"]
        num_cols = ["job_level", "years_experience"]

        cat_encoded = self.encoder.transform(female_df[cat_cols])
        X_female = np.hstack([
            female_df[num_cols].values,
            cat_encoded,
            np.zeros((len(female_df), 1)),  # set is_female = 0
        ])

        predicted_log_fair = self.model.predict(X_female)
        fair_salary = np.exp(predicted_log_fair)

        # Calculate needed adjustment
        current_salary = female_df["total_compensation"].values
        adjustment = fair_salary - current_salary
        adjustment = np.maximum(adjustment, 0)  # only raises, no cuts
        adjustment *= (budget_pct / 100.0)

        corrections = female_df[["employee_id", "country", "department", "job_level"]].copy()
        corrections["current_compensation"] = current_salary
        corrections["fair_compensation"] = fair_salary
        corrections["recommended_raise"] = np.round(adjustment, 0)
        corrections["raise_pct"] = np.round(adjustment / current_salary * 100, 2)
        corrections = corrections[corrections["recommended_raise"] > 0].sort_values(
            "raise_pct", ascending=False
        )

        return CorrectionPlan(
            corrections=corrections,
            total_cost=corrections["recommended_raise"].sum(),
            avg_raise_pct=corrections["raise_pct"].mean() if len(corrections) > 0 else 0,
            employees_affected=len(corrections),
        )
