"""
Generate synthetic employee compensation data for Takeda Pharmaceuticals.
Includes built-in gender pay bias for analysis purposes.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
NUM_EMPLOYEES = 5000

COUNTRIES = {
    "US": {"base_multiplier": 1.0, "currency": "USD", "gender_gap": 0.08},
    "JP": {"base_multiplier": 0.75, "currency": "JPY", "gender_gap": 0.12},
    "DE": {"base_multiplier": 0.90, "currency": "EUR", "gender_gap": 0.06},
    "UK": {"base_multiplier": 0.85, "currency": "GBP", "gender_gap": 0.09},
    "CH": {"base_multiplier": 1.15, "currency": "CHF", "gender_gap": 0.05},
    "BR": {"base_multiplier": 0.45, "currency": "BRL", "gender_gap": 0.10},
    "CN": {"base_multiplier": 0.50, "currency": "CNY", "gender_gap": 0.11},
    "IN": {"base_multiplier": 0.30, "currency": "INR", "gender_gap": 0.14},
    "SG": {"base_multiplier": 0.80, "currency": "SGD", "gender_gap": 0.07},
    "AU": {"base_multiplier": 0.88, "currency": "AUD", "gender_gap": 0.06},
}

DEPARTMENTS = {
    "R&D": {"weight": 0.30, "salary_factor": 1.10},
    "Commercial": {"weight": 0.25, "salary_factor": 1.05},
    "Manufacturing": {"weight": 0.20, "salary_factor": 0.95},
    "Corporate": {"weight": 0.15, "salary_factor": 1.00},
    "Medical Affairs": {"weight": 0.10, "salary_factor": 1.08},
}

EDUCATION_LEVELS = ["Bachelor's", "Master's", "PhD", "MD", "MBA"]
EDUCATION_WEIGHTS = [0.25, 0.30, 0.20, 0.10, 0.15]
EDUCATION_PREMIUM = {
    "Bachelor's": 0.0,
    "Master's": 0.08,
    "PhD": 0.18,
    "MD": 0.25,
    "MBA": 0.15,
}

# Base salary by job level (USD equivalent, level 1-10)
BASE_SALARY_BY_LEVEL = {
    1: 45000, 2: 55000, 3: 68000, 4: 82000, 5: 100000,
    6: 125000, 7: 155000, 8: 195000, 9: 250000, 10: 330000,
}

COUNTRY_DISTRIBUTION = [0.25, 0.15, 0.10, 0.08, 0.05, 0.08, 0.10, 0.07, 0.06, 0.06]


def generate_employees(n: int = NUM_EMPLOYEES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    countries = list(COUNTRIES.keys())
    departments = list(DEPARTMENTS.keys())
    dept_weights = [DEPARTMENTS[d]["weight"] for d in departments]

    records = []
    for i in range(n):
        employee_id = f"TKD-{i+1:05d}"
        gender = rng.choice(["M", "F"], p=[0.55, 0.45])
        country = rng.choice(countries, p=COUNTRY_DISTRIBUTION)
        department = rng.choice(departments, p=dept_weights)
        education = rng.choice(EDUCATION_LEVELS, p=EDUCATION_WEIGHTS)

        # Job level: slight bias — women less likely at senior levels
        if gender == "F":
            level_probs = np.array([0.12, 0.14, 0.16, 0.15, 0.14, 0.12, 0.08, 0.05, 0.03, 0.01])
        else:
            level_probs = np.array([0.08, 0.10, 0.13, 0.14, 0.15, 0.14, 0.11, 0.08, 0.05, 0.02])
        job_level = rng.choice(range(1, 11), p=level_probs)

        years_experience = max(0, int(rng.normal(loc=job_level * 2.5, scale=3)))
        years_experience = min(years_experience, 40)

        # Calculate base salary
        base = BASE_SALARY_BY_LEVEL[job_level]
        base *= COUNTRIES[country]["base_multiplier"]
        base *= DEPARTMENTS[department]["salary_factor"]
        base *= (1 + EDUCATION_PREMIUM[education])
        base *= (1 + years_experience * 0.012)  # experience premium

        # Apply gender pay gap (unexplained portion)
        if gender == "F":
            gap = COUNTRIES[country]["gender_gap"]
            # Add noise to the gap so it's not perfectly uniform
            actual_gap = rng.normal(loc=gap, scale=gap * 0.3)
            actual_gap = max(0, actual_gap)
            base *= (1 - actual_gap)

        # Add random noise
        base *= rng.normal(loc=1.0, scale=0.05)
        base_salary = round(max(base, 25000), 0)

        # Bonus: 5-30% of base depending on level
        bonus_pct = 0.05 + (job_level - 1) * 0.028
        bonus = round(base_salary * bonus_pct * rng.uniform(0.7, 1.3), 0)

        total_comp = base_salary + bonus

        records.append({
            "employee_id": employee_id,
            "gender": gender,
            "country": country,
            "department": department,
            "job_level": job_level,
            "education": education,
            "years_experience": years_experience,
            "base_salary": base_salary,
            "bonus": bonus,
            "total_compensation": total_comp,
        })

    return pd.DataFrame(records)


def save_data(df: pd.DataFrame, output_dir: str = "data") -> str:
    path = Path(output_dir) / "employee_compensation.csv"
    df.to_csv(path, index=False)
    return str(path)


if __name__ == "__main__":
    df = generate_employees()
    path = save_data(df)
    print(f"Generated {len(df)} employee records -> {path}")
    print(f"\nGender distribution:\n{df['gender'].value_counts()}")
    print(f"\nCountry distribution:\n{df['country'].value_counts()}")
    print(f"\nMean total comp by gender:\n{df.groupby('gender')['total_compensation'].mean()}")
