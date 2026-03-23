---
name: Synthetic HR Data Generation
description: Use when generating realistic fake employee compensation datasets with configurable demographic biases
type: skill
---

## When to Use
Use this skill when you need to create synthetic HR datasets for testing pay equity models, building demo dashboards, or constructing data science challenges. The generated data should have realistic distributions and tunable bias parameters.

## Key Patterns

**Reproducible Random Generator**
```python
rng = np.random.default_rng(seed=42)
```

**Multi-Dimensional Employee Attributes**
- Country: weighted sampling from list (e.g., US, UK, Japan, Germany, Brazil)
- Department: R&D, Sales, HR, Finance, Manufacturing, IT
- Education: High School, Bachelor's, Master's, PhD
- Job Level: 1-8 integer scale
- Gender: M/F with configurable ratio per level

**Compensation Formula**
```
salary = base × country_multiplier × dept_factor × (1 + edu_premium) × (1 + 0.012 × experience) × noise
```
- `base` varies by job level (e.g., level 1 = 40k, level 8 = 250k)
- `country_multiplier`: US=1.0, UK=0.85, Japan=0.75, etc.
- `dept_factor`: R&D=1.1, Sales=1.05, HR=0.9, etc.
- `edu_premium`: HS=0, BS=0.05, MS=0.12, PhD=0.20
- `noise = rng.normal(1.0, 0.05)` — 5% random variation

**Injecting Gender Bias**
- Level distribution bias: shift female probabilities toward lower levels
  ```python
  male_level_probs   = [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05]
  female_level_probs = [0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.07, 0.03]
  ```
- Direct pay penalty: multiply female salary by `(1 - gap_factor)`
- Country-specific gap: `gap ~ N(μ_country, 0.3 × μ_country)` where μ_country varies (e.g., Japan=0.12, US=0.06)

**Bonus Calculation**
```python
bonus_pct = {1: 0.05, 2: 0.08, 3: 0.10, 4: 0.15, 5: 0.20, 6: 0.25, 7: 0.30, 8: 0.40}
bonus = salary * bonus_pct[level] * rng.normal(1.0, 0.1)
```

## Checklist
- [ ] Always use seeded RNG for reproducibility
- [ ] Validate output distributions look realistic (no negative salaries, sensible ranges)
- [ ] Include both structural bias (level distribution) and direct bias (pay penalty)
- [ ] Add noise so patterns are discoverable but not trivially obvious
- [ ] Export as CSV with clear column names
- [ ] Document the true bias parameters separately for answer keys
