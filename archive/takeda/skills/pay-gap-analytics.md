---
name: Pay Gap Analytics
description: Use when building compensation equity analysis with Blinder-Oaxaca decomposition and pay correction models
type: skill
---

## When to Use
Use this skill when analyzing gender or demographic pay gaps in HR compensation data. It covers the full pipeline from regression modeling to fair-salary estimation and budget-constrained correction prioritization.

## Key Patterns

**Blinder-Oaxaca Decomposition**
- Separate the raw pay gap into "explained" (due to differences in qualifications) and "unexplained" (potential discrimination) components
- The unexplained portion is the policy-relevant metric

**Log-Linear Regression Model**
```
ln(TC) = β₀ + β₁·Level + β₂·Experience + Σγⱼ·Country + Σδₖ·Dept + α·IsFemale + ε
```
- Dependent variable is log of total compensation (base + bonus)
- `α` (the gender coefficient) represents the unexplained gap as a percentage (~exp(α) - 1)
- Use OLS via statsmodels for p-values and confidence intervals on α
- Include interaction terms (e.g., Gender×Level) if gap varies by seniority

**Fair Salary Estimation**
- For each female employee, predict salary with `IsFemale=0` while keeping all other features unchanged
- `fair_salary = exp(model.predict(X_counterfactual))`
- `gap_amount = max(0, fair_salary - current_salary)` — never reduce pay

**Budget-Constrained Correction**
- `correction = gap_amount × (budget_percentage / 100)`
- Rank employees by `raise_percentage = correction / current_salary` descending
- Prioritize largest percentage shortfalls first within budget envelope
- Report total budget needed for full correction vs. partial correction coverage

## Checklist
- [ ] Log-transform compensation before regression (normality assumption)
- [ ] Check for multicollinearity among predictors (VIF < 5)
- [ ] Validate α is statistically significant (p < 0.05)
- [ ] Never propose negative corrections (only raises)
- [ ] Report both adjusted and unadjusted gaps
- [ ] Include confidence intervals on gap estimates
- [ ] Document which controls are "explained" vs. potentially tainted by discrimination
