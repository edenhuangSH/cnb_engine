---
name: computational-journalism
description: Create NYT-style scrollytelling HTML with interactive data viz and PDF reports
type: skill
---

## When to Use
When building data-driven journalism pieces with interactive visualizations.

## Key Patterns
- Single self-contained HTML file, libraries via CDN only
- Chart.js for charts, Leaflet.js for maps, KaTeX for LaTeX formulas
- Google Fonts: Playfair Display (headlines), Source Serif 4 (body), Inter (UI)
- Intersection Observer API for scroll-triggered fade-in animations
- Animated number counters: requestAnimationFrame + easeOutCubic
- Dark mode toggle with CSS custom properties + localStorage
- Interactive toggles for chart data switching
- Collapsible sections for technical appendix
- Personal stories as blockquote interviews with circular portrait photos
- PDF companion via matplotlib PdfPages

## Checklist
- [ ] All CSS/JS inline (single file, no build step)
- [ ] Mobile responsive with @media queries
- [ ] Dark mode with localStorage persistence
- [ ] Cite real studies with proper attribution
- [ ] Include technical appendix with methodology
- [ ] Use placeholder portraits (i.pravatar.cc) for interview subjects
