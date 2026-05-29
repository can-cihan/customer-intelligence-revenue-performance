# Customer Intelligence & Revenue Performance

An end-to-end BI case study on 1M+ transactions from a UK online retailer (UCI Online Retail II, Dec 2009 – Dec 2011). Built to answer three commercial questions: where does revenue come from, who actually drives the value, and do customers come back?

**🔗 Live dashboard:** [Customer Intelligence & Revenue Performance — Tableau Public](https://public.tableau.com/app/profile/can.cihan/viz/CustomerIntelligenceRetentionAnalytics/CustomerIntelligence)

---

## TL;DR

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

**Headline finding:** 22% of customers (Champions segment) drive 68% of revenue, are worth ~3× the average customer, and retain at ~2× the rate of At-Risk customers. The business is built on a small loyal core — that is where retention investment compounds.

For the full written-up case study, see [`reports/case_study.md`](reports/case_study.md).

---

## What's in this repo

```
ecommerce-commercial-analytics/
├── notebooks/
│   ├── 01_data_cleaning_rfm_cohort.ipynb   ← full pipeline (cleaning + RFM + cohort)
│   └── 01_data_cleaning_reference.py        ← same pipeline as a reproducible script
├── data/
│   ├── raw/                                  ← place online_retail_II.csv here (gitignored)
│   └── processed/                            ← output CSVs that feed the Tableau dashboards
├── dashboards/
│   └── signature_viz_notes.md                ← reverse-engineered Tableau viz techniques
├── reports/
│   └── case_study.md                         ← written case study (PDF-ready)
├── requirements.txt
└── README.md
```

---

## Methodology in 60 seconds

1. **Cleaning** — 1.07M raw rows. Removed 34k exact duplicates; isolated 22k cancellations/returns into a separate ledger; filtered invalid-price entries; produced two sales layers.
2. **Two sales layers** — *all sales* (£20.5M, includes unidentified customers) feed commercial KPIs; *identified-only* (£17.4M, 5,878 customers) feeds RFM, cohort, and segment analyses. This is the honest split: commercial revenue isn't understated by the ~15% of transactions without a customer ID, and customer-level work stays on a clean base.
3. **RFM segmentation** — quintile scoring on Recency, Frequency, and Monetary; mapped to five named segments (Champions, Loyal Customers, Potential Loyalists, At Risk, Others).
4. **Cohort retention** — monthly acquisition cohorts × months-since-acquisition, computed both portfolio-wide and per segment.
5. **Tableau Story** — three connected dashboards: global overview with country-interactive KPIs, segmentation deep-dive with action-filtered KPIs tied to a treemap, and retention dynamics anchored on a real cohort heat map.

## Honest methodology notes

These were deliberate choices I'd defend in an interview, not gloss:

- All financial figures are in **GBP**. The retailer is UK-based.
- Commercial KPIs (Total Revenue, AOV) include unidentified-customer transactions. Customer-level metrics (RFM, cohorts, segments) are restricted to identified customers (5,878) to keep the analysis honest.
- "Repeat Customer Rate" is shown as a **portfolio-wide benchmark** rather than per country. Only four markets contain ≥30 identified customers; per-country rates would be statistically unstable.
- Per-country Premium Revenue Share displays "—" for markets below the 30-customer threshold for the same reason.
- Retention "advantage" between segments is reported in **percentage points**, not as a ratio of percentages, to avoid misleading framing.

---

## How to reproduce

**Requirements:** Python 3.10+, pandas, jupyter. See `requirements.txt`.

```bash
pip install -r requirements.txt
```

**Get the data:**
- Download `online_retail_II.csv` from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- Place it in `data/raw/`

**Run the pipeline:**
```bash
cd notebooks
jupyter notebook 01_data_cleaning_rfm_cohort.ipynb
# Run all cells. Outputs land in data/processed/.
```

Or run the equivalent script:
```bash
cd notebooks
python 01_data_cleaning_reference.py
```

---

## Tools

Python (pandas) · Tableau Public · Jupyter

## Author

Can Cihan ([Tableau Public profile](https://public.tableau.com/app/profile/can.cihan))
