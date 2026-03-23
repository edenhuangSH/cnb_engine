"""
Generate synthetic employee compensation data for Amazon.
Includes built-in gender pay bias for analysis purposes.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
NUM_EMPLOYEES = 15000

COUNTRIES = {
    "US":        {"base_multiplier": 1.0,  "currency": "USD", "gender_gap": 0.09, "weight": 0.50},
    "India":     {"base_multiplier": 0.30, "currency": "INR", "gender_gap": 0.14, "weight": 0.15},
    "Germany":   {"base_multiplier": 0.90, "currency": "EUR", "gender_gap": 0.07, "weight": 0.05},
    "UK":        {"base_multiplier": 0.85, "currency": "GBP", "gender_gap": 0.08, "weight": 0.05},
    "Japan":     {"base_multiplier": 0.75, "currency": "JPY", "gender_gap": 0.13, "weight": 0.04},
    "Canada":    {"base_multiplier": 0.92, "currency": "CAD", "gender_gap": 0.06, "weight": 0.04},
    "Australia":  {"base_multiplier": 0.88, "currency": "AUD", "gender_gap": 0.06, "weight": 0.03},
    "Brazil":    {"base_multiplier": 0.40, "currency": "BRL", "gender_gap": 0.10, "weight": 0.04},
    "Singapore": {"base_multiplier": 0.82, "currency": "SGD", "gender_gap": 0.07, "weight": 0.03},
    "Mexico":    {"base_multiplier": 0.35, "currency": "MXN", "gender_gap": 0.11, "weight": 0.04},
    "France":    {"base_multiplier": 0.88, "currency": "EUR", "gender_gap": 0.07, "weight": 0.03},
}

DEPARTMENTS = {
    "AWS":                   {"weight": 0.22, "salary_factor": 1.15},
    "Retail":                {"weight": 0.18, "salary_factor": 1.00},
    "Logistics/Operations":  {"weight": 0.25, "salary_factor": 0.85},
    "Whole Foods":           {"weight": 0.08, "salary_factor": 0.80},
    "Studios/Entertainment": {"weight": 0.05, "salary_factor": 1.05},
    "Corporate":             {"weight": 0.12, "salary_factor": 1.02},
    "Devices":               {"weight": 0.10, "salary_factor": 1.08},
}

EDUCATION_LEVELS = ["High School", "Bachelor's", "Master's", "PhD", "MBA"]
EDUCATION_WEIGHTS = [0.15, 0.30, 0.28, 0.12, 0.15]
EDUCATION_PREMIUM = {
    "High School": -0.05,
    "Bachelor's": 0.0,
    "Master's": 0.08,
    "PhD": 0.18,
    "MBA": 0.15,
}

# Amazon L4-L12 levels — base salary (USD equivalent)
BASE_SALARY_BY_LEVEL = {
    4: 60000, 5: 80000, 6: 110000, 7: 140000, 8: 175000,
    9: 220000, 10: 280000, 11: 360000, 12: 500000,
}

# RSU grants by level (annual vest value, USD)
RSU_BY_LEVEL = {
    4: 10000, 5: 25000, 6: 50000, 7: 80000, 8: 130000,
    9: 200000, 10: 320000, 11: 500000, 12: 800000,
}


def generate_employees(n: int = NUM_EMPLOYEES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    countries = list(COUNTRIES.keys())
    country_weights = [COUNTRIES[c]["weight"] for c in countries]
    departments = list(DEPARTMENTS.keys())
    dept_weights = [DEPARTMENTS[d]["weight"] for d in departments]

    records = []
    for i in range(n):
        employee_id = f"AMZ-{i+1:06d}"
        gender = rng.choice(["M", "F"], p=[0.58, 0.42])
        country = rng.choice(countries, p=country_weights)
        department = rng.choice(departments, p=dept_weights)
        education = rng.choice(EDUCATION_LEVELS, p=EDUCATION_WEIGHTS)

        # Job level: women less likely at L8+
        if gender == "F":
            level_probs = np.array([0.18, 0.22, 0.24, 0.16, 0.10, 0.05, 0.03, 0.015, 0.005])
        else:
            level_probs = np.array([0.12, 0.17, 0.22, 0.18, 0.14, 0.08, 0.05, 0.03, 0.01])
        job_level = rng.choice(range(4, 13), p=level_probs)

        years_experience = max(0, int(rng.normal(loc=(job_level - 3) * 2.5, scale=3)))
        years_experience = min(years_experience, 40)

        # Base salary
        base = BASE_SALARY_BY_LEVEL[job_level]
        base *= COUNTRIES[country]["base_multiplier"]
        base *= DEPARTMENTS[department]["salary_factor"]
        base *= (1 + EDUCATION_PREMIUM[education])
        base *= (1 + years_experience * 0.012)

        # Gender pay gap
        if gender == "F":
            gap = COUNTRIES[country]["gender_gap"]
            actual_gap = rng.normal(loc=gap, scale=gap * 0.3)
            actual_gap = max(0, actual_gap)
            base *= (1 - actual_gap)

        base *= rng.normal(loc=1.0, scale=0.05)
        base_salary = round(max(base, 22000), 0)

        # Bonus: 5-25% depending on level
        bonus_pct = 0.05 + (job_level - 4) * 0.025
        bonus = round(base_salary * bonus_pct * rng.uniform(0.7, 1.3), 0)

        # RSU
        rsu_base = RSU_BY_LEVEL[job_level]
        rsu_base *= COUNTRIES[country]["base_multiplier"]
        rsu_value = round(rsu_base * rng.uniform(0.8, 1.2), 0)

        total_comp = base_salary + bonus + rsu_value

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
            "rsu_value": rsu_value,
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
    print(f"\nDept distribution:\n{df['department'].value_counts()}")
    print(f"\nMean total comp by gender:\n{df.groupby('gender')['total_compensation'].mean()}")
