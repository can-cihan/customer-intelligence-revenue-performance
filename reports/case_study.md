# Customer Intelligence & Revenue Performance

A strategic analysis of revenue concentration, customer value segments, and retention behavior for a UK online retailer.

**Tools:** Python (pandas) · Tableau Public · GitHub
**Dataset:** UCI Online Retail II — 1M+ transactions, Dec 2009 – Dec 2011, 43 markets, 5,878 identified customers, £20.5M revenue.
**Live dashboard:** [Customer Intelligence & Revenue Performance — Tableau Public](https://public.tableau.com/app/profile/can.cihan/viz/CustomerIntelligenceRetentionAnalytics/CustomerIntelligence)
**Code & methodology:** *(GitHub link — add after pushing)*

---

## The question

A UK-based online gift retailer wants to know where its revenue really comes from, which customers drive its growth, and whether those customers come back. The answer should be honest enough to act on — not a slide of vanity metrics.

## The story, in three acts

### Act 1 — Where does the money come from?

Revenue is heavily concentrated. The UK alone accounts for 85% of all sales; the next eight markets together explain most of the rest. Across the entire customer base, 72.4% of identified customers come back at least once — a remarkably loyal core for a 2-year window in retail. The premium segment (Champions, defined by recency, frequency, and monetary value) generates 68% of the revenue tracked to identified customers.

The headline is simple: this is not a broad-market business. It is a small-loyal-core business anchored in one market.

### Act 2 — Who actually drives the value?

The Champions segment is 22% of the identified customer base and produces £11.9M of revenue. Every Champion customer generates an average of **£9,144** over the two-year window — roughly **3× the average customer (£2,956)** and **21× a one-time customer**. They place an average of **17 orders** versus a portfolio-wide 6.

Loyal Customers, the second segment, generate £2.6M but at a meaningfully lower per-customer rate (£2,255). At-Risk and Others trail far behind. The treemap tells a story most retailers would prefer to ignore: the business is built on a small group of people whose ongoing engagement is the entire commercial story.

### Act 3 — Do they come back?

Cohort retention is healthy. Early cohorts (Dec 2009 – mid 2010) maintain repeat purchase activity well into year two, visible as the dark band along the top of the cohort heat map. The most important signal: **Champions retain at 46% on average over 12 months — nearly 2× the rate of At-Risk customers (25%).** This is the natural place to spend retention dollars: where the customer is already worth 3× and the response rate is 2× the alternative.

## The strategic implication

The data prescribes a clear playbook:

1. **Defend and grow Champions.** They are 22% of customers but 68% of revenue and retain at twice the rate of weaker segments. Loyalty programs, account management, and personalized retention should concentrate here.
2. **Win back At-Risk before they decay.** They still spend at a meaningful clip (£3,620 per customer average) and their retention gap suggests recoverable behavior.
3. **Treat the UK market as the anchor, not the ceiling.** UK delivers 85% of revenue today. Of the four markets with statistically meaningful customer bases (UK, Germany, France, Spain), Germany and France post higher Premium Revenue Share than the UK — signaling an underweight commercial opportunity in continental Europe.

## How the analysis was built

The pipeline runs end-to-end in Python and feeds a clean executive dashboard in Tableau Public.

- **Cleaning:** 1.07M raw rows reduced to 1.0M valid sales after removing 34k exact duplicates, isolating 22k returns/cancellations into a separate ledger, and filtering invalid-price entries. Two sales layers are produced: one for commercial KPIs (all sales) and one for customer-level analysis (identified customers only).
- **Segmentation:** RFM scoring on quintiles, mapped to five named segments (Champions, Loyal Customers, At-Risk, Others, Potential Loyalists).
- **Cohort retention:** monthly acquisition cohorts × months since acquisition, both portfolio-wide and per segment.
- **Tableau Story:** three dashboards — global overview with country-interactive KPIs, segment deep-dive linked to a treemap, and retention dynamics anchored on a real cohort heat map.

## Methodology notes

- All financial figures are in **GBP**.
- Commercial KPIs (Total Revenue, Avg Order Value) include unidentified-customer transactions. Customer-level metrics (RFM, retention, segment splits) are restricted to identified customers (5,878) to keep the analysis honest.
- The "Repeat Customer Rate" KPI is shown as a portfolio-wide benchmark rather than per country because only four markets contain ≥30 identified customers; per-country rates would be statistically unstable.
- For the same reason, per-country Premium Revenue Share displays "—" for markets with fewer than 30 identified customers.
- Retention "advantage" between segments is reported in **percentage points**, not as a ratio of percentages, to avoid misleading framing.

## Headline numbers (at a glance)

| Metric | Value |
|---|---|
| Total revenue | £20.5M |
| Identified customers | 5,878 |
| Orders | 40,079 |
| Avg order value | £511 |
| Repeat customer rate | 72.4% |
| Premium revenue share (Champions) | 68.3% |
| Avg revenue per customer | £2,956 |
| Avg Champion customer value | £9,144 |
| Champions 12-month retention | 46% (avg), 44.5% (month 12) |
| At-Risk 12-month retention | 25% (avg), 14.7% (month 12) |
| Return rate (value) | 7.1% |
