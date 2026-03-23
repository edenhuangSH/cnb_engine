---
name: Data Science Take-Home Challenge
description: Use when creating PhD-level data science take-home problems with Jupyter notebooks and separate solutions
type: skill
---

## When to Use
Use this skill when designing rigorous data science interview challenges or educational exercises. The format uses paired Jupyter notebooks — one problem statement and one fully-executed solution — targeting PhD-level candidates with multi-part analytical depth.

## Key Patterns

**Notebook Structure — Problem**
1. Title + context cell (markdown): company scenario, dataset description
2. `!pip install` cell at top for all dependencies
3. Dataset loading cell with inline path or URL
4. Multi-part questions with clear section headers:
   - Part 1: Exploratory Data Analysis
   - Part 2: Feature Engineering
   - Part 3: Statistical Modeling
   - Part 4: Interpretation and Recommendations
5. Rubric/evaluation criteria cell at the end

**Notebook Structure — Solution**
1. Same header and install cells as problem
2. Each part answered with code cells + markdown explanation
3. All cells executed with visible outputs (tables, charts, model summaries)
4. Commentary explains reasoning, not just code
5. Final summary cell with key findings

**PhD-Level Difficulty Markers**
- Require domain knowledge (e.g., econometrics, causal inference)
- Ask for methodology justification, not just implementation
- Include at least one open-ended interpretation question
- Expect candidates to identify and handle data quality issues unprompted
- Bonus/stretch questions that test depth (e.g., "propose an alternative identification strategy")

**Pip Install Cells**
```python
!pip3 install pandas numpy matplotlib seaborn statsmodels scikit-learn plotly -q
```
- Use `pip3` for compatibility
- Add `-q` flag to suppress verbose output
- Place at the very top before any imports

## Checklist
- [ ] Problem notebook has no solution code — only questions and scaffolding
- [ ] Solution notebook is fully executed with all outputs visible
- [ ] Include pip install cell at the top of both notebooks
- [ ] Use clear markdown headers for each section
- [ ] Provide evaluation rubric with point allocations in problem notebook
- [ ] Test that solution notebook runs end-to-end from a clean kernel
- [ ] Dataset is either bundled or generated inline (no external dependencies)
