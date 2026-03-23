---
name: synthetic-hr-data
description: Generate realistic synthetic employee compensation data with configurable biases
type: skill
---

## When to Use
When creating dummy HR/compensation datasets for analysis or demos.

## Key Patterns
- `np.random.default_rng(seed)` for reproducible generation
- Config dicts per country: `{base_multiplier, currency, gender_gap, weight}`
- Compensation formula: `Base × Country × Dept × (1+Edu) × (1+0.012×Exp) × noise`
- Gender bias injection: different level probability distributions + direct pay penalty
- Gap noise: `G ~ N(μ_country, 0.3·μ_country)` with max(0, gap)
- Include RSU/stock for tech companies, bonus tied to level

## Checklist
- [ ] Use seeded RNG for reproducibility
- [ ] Inject bias through BOTH level distribution AND direct pay penalty
- [ ] Add realistic noise (±5% normal)
- [ ] Ensure minimum salary floor
- [ ] Include all comp components (base + bonus + equity)
