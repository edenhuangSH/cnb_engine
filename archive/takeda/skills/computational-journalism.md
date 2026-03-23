---
name: Computational Journalism
description: Use when building NYT-style interactive data journalism pieces with scrollytelling, animated charts, and narrative-driven data visualization
type: skill
---

## When to Use
Use this skill when creating long-form, narrative-driven data stories as self-contained HTML pages. These pieces combine investigative data analysis with interactive visualizations, scroll-triggered animations, and editorial design inspired by the New York Times and The Pudding.

## Key Patterns

**Scrollytelling with Intersection Observer**
```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            triggerAnimation(entry.target.dataset.step);
        }
    });
}, { threshold: 0.3 });
document.querySelectorAll('.scroll-step').forEach(el => observer.observe(el));
```

**Self-Contained HTML with CDN Libraries**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Serif+Pro&family=Inter:wght@400;600&display=swap" rel="stylesheet">
```

**Typography System**
- Headlines: `Playfair Display`, 700 weight, 2.5-3.5rem
- Body text: `Source Serif Pro`, 1.1rem, line-height 1.8
- UI elements / labels / captions: `Inter`, 400/600 weight

**Color Palette**
- Primary navy: `#1a1a2e`
- Background warm gray: `#f5f5f5`
- Accent red: `#e63946`
- Supporting: `#457b9d` (steel blue), `#2a9d8f` (teal), `#e9c46a` (gold)

**Animated Number Counters**
```javascript
function animateCounter(el, target, duration = 2000) {
    let start = 0;
    const step = (timestamp) => {
        if (!start) start = timestamp;
        const progress = Math.min((timestamp - start) / duration, 1);
        el.textContent = Math.floor(progress * target).toLocaleString();
        if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
}
```

**Interactive Chart Toggles**
- Country selector buttons that filter/update chart data
- Scenario simulator sliders (e.g., "What if the gap closed by X%?")
- Smooth transitions with CSS `transition` or D3 `.transition().duration(800)`

**Narrative Design Elements**
- Pull-quotes: large italic text with left border accent, woven between data sections
- Personal story vignettes alongside aggregate statistics
- "Key finding" callout boxes with icon + bold summary
- Collapsible technical appendix using `<details><summary>` elements

**Dark Mode Toggle**
```css
:root { --bg: #f5f5f5; --text: #1a1a2e; --accent: #e63946; }
[data-theme="dark"] { --bg: #1a1a2e; --text: #f5f5f5; --accent: #e63946; }
body { background: var(--bg); color: var(--text); transition: all 0.3s; }
```

**Mobile Responsiveness**
```css
@media (max-width: 768px) {
    .article-body { padding: 0 1rem; font-size: 1rem; }
    .chart-container { width: 100%; overflow-x: auto; }
    .hero-title { font-size: 2rem; }
}
```

**PDF Companion Report**
- Use matplotlib for static chart versions of interactive visualizations
- reportlab for assembling multi-page PDF with cover, executive summary, charts, appendix
- Match color palette between web and PDF versions

## Checklist
- [ ] Single self-contained HTML file — no build step required
- [ ] All libraries loaded via CDN with fallback
- [ ] Scroll animations trigger only once (or re-trigger gracefully)
- [ ] Charts are interactive with tooltips and hover states
- [ ] Typography hierarchy is consistent throughout
- [ ] Dark mode toggle persists via localStorage
- [ ] Mobile-responsive at 768px and 480px breakpoints
- [ ] Pull-quotes and stories humanize the data
- [ ] Technical appendix is collapsible, not inline
- [ ] Page loads in under 3 seconds on 3G
- [ ] PDF companion matches web narrative and color palette
