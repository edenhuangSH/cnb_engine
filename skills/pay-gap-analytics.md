---
name: pay-gap-analytics
description: Build gender pay gap analysis engines using Blinder-Oaxaca regression decomposition
type: skill
---

## When to Use
When building compensation equity analysis with regression-based decomposition to separate explained vs unexplained pay gaps.

## Key Patterns
- Log-linear regression: `ln(TC) = β₀ + β₁·Level + β₂·Exp + Σγ·Country + Σδ·Dept + α·IsFemale + ε`
- Gender coefficient α = unexplained gap (in log-percentage terms)
- OneHotEncoder(drop="first") for categorical features
- Fair salary = predict with IsFemale=0: `exp(β̂₀ + β̂₁L + β̂₂X + Σγ̂·C + Σδ̂·D)`
- Correction = max(0, fair - current) × budget%
- Priority ranking by percentage underpayment

## Checklist
- [ ] Use log-transformed compensation for multiplicative interpretation
- [ ] Drop first category in one-hot encoding to avoid multicollinearity
- [ ] Only recommend raises, never cuts (max with 0)
- [ ] Report both raw and unexplained gaps
- [ ] Check R² to validate model quality (>0.95 typical for pay models)
