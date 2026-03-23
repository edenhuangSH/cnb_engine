# Compensation Analytics — Modeling Methodology

## 1. Overview

This document describes the statistical methodology used in the Takeda Compensation & Benefits Analytics Engine to detect, quantify, and remediate gender-based pay disparities across the global workforce.

The pipeline consists of three stages:

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│  Data Generation │───▶│  Gap Decomposition   │───▶│  Correction Engine  │
│  (Synthetic DB)  │    │  (Regression Model)  │    │  (Budget Simulator) │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
```

---

## 2. Data Generation

### 2.1 Population Design

We generate $N = 5{,}000$ synthetic employees distributed across 10 countries, 5 departments, and 10 job levels. The distribution parameters are calibrated to reflect a realistic pharmaceutical workforce.

### 2.2 Compensation Formula

For each employee $i$, base salary is computed as:

$$
S_i = B_{L_i} \cdot M_{C_i} \cdot F_{D_i} \cdot (1 + P_{E_i}) \cdot (1 + 0.012 \cdot X_i) \cdot \epsilon_i
$$

Where:
- $B_{L_i}$ — Base salary for job level $L$ (ranges from \$45K at level 1 to \$330K at level 10)
- $M_{C_i}$ — Country cost-of-labor multiplier (e.g., US = 1.0, CH = 1.15, IN = 0.30)
- $F_{D_i}$ — Department salary factor (e.g., R&D = 1.10, Manufacturing = 0.95)
- $P_{E_i}$ — Education premium (e.g., PhD = 18%, MBA = 15%, Bachelor's = 0%)
- $X_i$ — Years of experience (1.2% premium per year)
- $\epsilon_i \sim \mathcal{N}(1.0, 0.05)$ — Random noise

### 2.3 Embedded Gender Bias

For female employees, a country-specific pay penalty is applied:

$$
S_i^{F} = S_i \cdot (1 - G_{C_i})
$$

Where $G_{C_i} \sim \mathcal{N}(\bar{G}_C, 0.3 \cdot \bar{G}_C)$ is the gender gap factor, with country-level means $\bar{G}_C$ ranging from 5% (Switzerland) to 14% (India).

Additionally, female employees have a skewed job-level distribution, with lower probability of reaching senior levels (levels 7–10), creating a **structural gap** on top of the **direct pay gap**.

### 2.4 Total Compensation

$$
TC_i = S_i + \text{Bonus}_i
$$

Where:

$$
\text{Bonus}_i = S_i \cdot \left(0.05 + 0.028 \cdot (L_i - 1)\right) \cdot U_i, \quad U_i \sim \text{Uniform}(0.7, 1.3)
$$

---

## 3. Pay Gap Decomposition

### 3.1 Raw Gap

The unadjusted (raw) gender pay gap is:

$$
\Delta_{\text{raw}} = \frac{\bar{TC}_M - \bar{TC}_F}{\bar{TC}_M} \times 100\%
$$

This metric is computed overall and sliced by country, department, and job level.

### 3.2 Regression Model (Blinder-Oaxaca Inspired)

To separate **explained** differences (due to legitimate factors) from **unexplained** differences (potential discrimination), we fit a log-linear regression:

$$
\ln(TC_i) = \beta_0 + \beta_1 \cdot L_i + \beta_2 \cdot X_i + \sum_j \gamma_j \cdot \mathbf{1}_{C_i = j} + \sum_k \delta_k \cdot \mathbf{1}_{D_i = k} + \sum_m \phi_m \cdot \mathbf{1}_{E_i = m} + \alpha \cdot \mathbf{1}_{\text{Female}_i} + \epsilon_i
$$

Where:
- $L_i$ — Job level (numeric, 1–10)
- $X_i$ — Years of experience
- $\mathbf{1}_{C_i = j}$ — Country indicator (one-hot encoded, first dropped)
- $\mathbf{1}_{D_i = k}$ — Department indicator
- $\mathbf{1}_{E_i = m}$ — Education level indicator
- $\mathbf{1}_{\text{Female}_i}$ — Gender indicator (1 if female)

### 3.3 Interpreting the Gender Coefficient

The coefficient $\alpha$ represents the **unexplained gender pay gap** in log-percentage terms:

$$
\Delta_{\text{unexplained}} \approx |\alpha| \times 100\%
$$

Since we use log-transformed compensation, $\alpha$ can be interpreted as the approximate percentage difference in pay attributable to gender, **after controlling for** job level, experience, education, country, and department.

### 3.4 Model Quality

The model achieves $R^2 \approx 0.987$, meaning legitimate factors explain ~98.7% of pay variation. The remaining unexplained variance includes the gender effect plus noise.

---

## 4. Correction Engine

### 4.1 Fair Salary Estimation

For each female employee $i$, we estimate what she **would** earn if there were no gender penalty by predicting with $\mathbf{1}_{\text{Female}} = 0$:

$$
\widehat{TC}_i^{\text{fair}} = \exp\left(\hat{\beta}_0 + \hat{\beta}_1 L_i + \hat{\beta}_2 X_i + \sum_j \hat{\gamma}_j \mathbf{1}_{C_i=j} + \sum_k \hat{\delta}_k \mathbf{1}_{D_i=k} + \sum_m \hat{\phi}_m \mathbf{1}_{E_i=m}\right)
$$

### 4.2 Recommended Adjustment

$$
\Delta_i = \max\left(0, \; \widehat{TC}_i^{\text{fair}} - TC_i^{\text{current}}\right) \times \frac{B}{100}
$$

Where $B \in [0, 100]$ is the budget percentage (100% = full correction). Only positive adjustments (raises) are recommended.

### 4.3 Priority Ranking

Employees are ranked by $\frac{\Delta_i}{TC_i^{\text{current}}} \times 100$ (percentage raise), so the most underpaid employees relative to their fair value are corrected first.

### 4.4 Budget Simulation

The dashboard provides an interactive slider to adjust $B$, showing:
- **Total cost**: $\sum_i \Delta_i$
- **Employees affected**: $|\{i : \Delta_i > 0\}|$
- **Average raise %**: $\frac{1}{|\{i : \Delta_i > 0\}|} \sum_i \frac{\Delta_i}{TC_i} \times 100$

---

## 5. Limitations & Future Work

### Current Limitations

1. **Synthetic data only** — Real compensation data would require different noise structures and more complex feature engineering
2. **Binary gender model** — Does not account for non-binary gender identities
3. **Single regression** — A more robust approach would use quantile regression or hierarchical models to capture gap variation across the distribution
4. **No intersectionality** — Does not analyze compounding effects of gender × ethnicity × age
5. **Static snapshot** — Does not model temporal trends or promotion velocity gaps

### Recommended Extensions

- **Blinder-Oaxaca formal decomposition** — Separate the gap into endowments, coefficients, and interaction effects
- **Quantile regression** — Detect if gaps are larger at the top (glass ceiling) or bottom (sticky floor)
- **Hierarchical Bayesian model** — Country-level random effects for more stable estimates in small samples
- **Promotion velocity analysis** — Time-to-promotion by gender at each level
- **Bonus equity analysis** — Separate model for bonus allocation fairness

---

## 6. References

1. Blinder, A. S. (1973). "Wage Discrimination: Reduced Form and Structural Estimates." *Journal of Human Resources*, 8(4), 436–455.
2. Oaxaca, R. (1973). "Male-Female Wage Differentials in Urban Labor Markets." *International Economic Review*, 14(3), 693–709.
3. European Commission (2020). "Report on equality between women and men in the EU."
4. World Economic Forum (2023). "Global Gender Gap Report."
