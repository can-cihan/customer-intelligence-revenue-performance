# Signature Tableau viz — reverse-engineered recipes

Notes extracted from two reference workbooks (WOW2021 Calendar Circle, "Inside the Beautiful ADHD Mind"), adapted to the Online Retail II dataset. Use these in the Tableau build step.

---

## 1. Radial "calendar circle" — daily revenue ring

**What it shows:** each dot = one calendar day; angle = position in the year (by week), radius = day-of-week band, **color = month**, **size = daily revenue**. Mirrors the WOW submission tracker, but encodes revenue instead of submission counts.

### Original WOW logic (decoded from the .twb)
- `Index = INDEX() - 1`
- `Multiplier = 360 / 53`  *(spreads 53 weeks evenly around 360°)*
- `Item` (angle, degrees) = week number derived from `Index / 7`, times `Multiplier`
- `Distance` (radius) = `(Index % 7) + 7`  *(day-of-week 0–6, plus a 7-unit center hole)*
- `X = SIN(RADIANS([Item])) * [Distance]`
- `Y = COS(RADIANS([Item])) * [Distance]`

Parameters used: `Depth = 7` (marks per spoke = days per week), spokes = 53 weeks.

### Adapted calculated fields for our data
Build on a **daily table with one row per calendar day** of the chosen year (see densify tip below).

```
// 0-based running index over days, sorted by date ascending
Index           = INDEX() - 1

// constants
Days Per Spoke  = 7
Spokes (weeks)  = 53
Multiplier      = 360 / [Spokes (weeks)]      // = 360/53

// angle (degrees): which week-spoke this day sits on
Angle = IF ([Index] % [Days Per Spoke]) < [Days Per Spoke]/2
        THEN ROUND([Index] / [Days Per Spoke], 0)
        ELSE ROUND([Index] / [Days Per Spoke], 0) - 1
        END * [Multiplier]

// radius: day-of-week band (0..6) + center hole
Radius = ([Index] % [Days Per Spoke]) + 7      // raise the +7 for a bigger hole

// cartesian coords
X = SIN(RADIANS([Angle])) * [Radius]
Y = COS(RADIANS([Angle])) * [Radius]
```

### Shelf setup
- Columns: `X`  ·  Rows: `Y`
- Marks card: **Circle**
- Detail: `DAY([InvoiceDate])` (exact date) — produces one mark per day
- Color: `MONTH([InvoiceDate])` → apply a custom 12-step rainbow palette
- Size: `SUM([Revenue])`
- On `X`, `Y`, and `Index`: Edit Table Calculation → **Compute Using → the date (Day), ascending**
- Format: hide both axes, gridlines, zero lines; set a fixed square aspect ratio; dark dashboard background; add a center text (e.g. total revenue + year).

### Key practical tip — densify to a full date spine
The store does not trade every day (~298 active days in 2010), so plotting raw transaction dates leaves gaps in the ring. To get an evenly spaced ring like the reference, feed Tableau **one row per calendar day** (Jan 1 – Dec 31), with revenue = 0 (or null) on non-trading days. We will produce this as `data/processed/daily_summary.csv` during cleaning (left-join a complete date range onto daily revenue). Then `INDEX()` runs 0..364 evenly.

---

## 2. Gradient "stream / 3D" area — revenue flow over time

**Reality check:** the ADHD "3D gradient" chart is not 3D. It is a **stacked area chart** with many thin bands plus a **continuous color gradient** mapped to a measure — the layering creates the depth illusion. No trig involved.

### How to build it for our data
- A streamgraph / stacked area of `SUM([Revenue])` over `MONTH([InvoiceDate])` (continuous date on Columns).
- Split into bands by a dimension: `Country` (top N + "Other") or product category.
- Color: map a continuous measure (e.g. revenue, or a sequential index) to a smooth gradient. Use a stepped/diverging palette for the blue→pink look.
- For the "stream" centering (bands flow around a center baseline rather than stacking from zero), use Tableau's area chart with a manual offset or the stream layout technique; a standard stacked area is the simpler, recruiter-clear version.

---

## 3. Radial gauge / donut KPI ("5x" style) — optional

The ADHD comorbidity gauges are two-layer donuts: a faint full background ring + a colored value arc. Good for a single KPI like **return rate** or **repeat-customer rate**.
- Simplest route: two-mark donut (background ring at 100%, value arc at the metric) using a dual-axis pie, hole created with a white/transparent inner circle.
- Keep to one or two of these max — they are decorative; the executive dashboard's KPI tiles carry the real load.

---

## Recommendation for a Business Analyst portfolio
Keep the main executive dashboard clean and readable (KPI tiles, trend line, map, RFM, cohort heatmap, dual-axis Pareto). Use the **radial daily-revenue ring as a single "signature" piece** — published as its own Tableau Public viz and linked from the README — to demonstrate Tableau range without compromising the clarity recruiters score on.
