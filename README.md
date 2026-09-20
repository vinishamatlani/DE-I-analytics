# Global Inclusion & Belonging Analytics

## Overview

This project demonstrates an end-to-end people analytics workflow
for measuring workplace inclusion and belonging using synthetic
employee survey data and DE&I event data.

The project was adapted from an open-source employee engagement
analytics workflow and reframed around inclusion analytics.

---

## Business Questions

The project addresses five questions:

1. What is the overall Inclusion Index?
2. Which inclusion dimensions are strongest and weakest?
3. Which workforce segments show meaningful inclusion gaps?
4. Which inclusion dimensions are associated with the overall
   inclusion outcome?
5. How effectively are DE&I events performing?

---

## Inclusion Framework

The Inclusion Index contains five dimensions:

- Belonging
- Employee Voice
- Psychological Safety
- Fairness & Opportunity
- Inclusive Leadership

Each dimension is measured using three 1–5 Likert-scale survey
items.

The overall Inclusion Index is the mean of the five dimension
scores and is also presented on a 0–100 scale.

---

## Analytics

The project includes:

### Inclusion Index

Measures the overall inclusion experience.

### Dimension Analysis

Examines the five component dimensions.

### Segment Analysis

Examines differences across:

- Region
- Gender group
- Age band
- Department
- Job level
- Tenure
- Work model

### Confidentiality

Groups with fewer than five respondents are suppressed.

### Driver Analysis

Pearson correlation is used to identify associations between
inclusion dimensions and a separate overall inclusion outcome.

The analysis does not make causal claims.

### DE&I Event Analytics

Synthetic event data measures:

- Attendance
- No-show rate
- Knowledge gain
- Satisfaction
- Recommendation
- Repeat participation
- Estimated cost
- Cost per attendee

---

## Data Ethics

The project uses synthetic data only.

It should not be interpreted as representing the actual workforce,
employees, policies, or organisational outcomes of any real company.

The project demonstrates analytical methods rather than reporting
real organisational findings.

---

## Outputs

Key generated outputs include:

```text
data/inclusion_scored.csv
data/inclusion_dimension_summary.csv
data/inclusion_segment_summary.csv
data/inclusion_driver_summary.csv
data/dei_events.csv
data/dei_event_summary.csv

inclusion_dashboard.html

reports/inclusion_executive_report.md
reports/intervention_framework.md
