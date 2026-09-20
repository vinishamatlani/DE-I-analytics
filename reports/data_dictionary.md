# Data Dictionary

## Purpose

This document describes the main fields used in the Global Inclusion
& Belonging Analytics project.

All employee and DE&I event data in this project is synthetic.

---

# Survey Data

File:

`data/survey_responses.csv`

| Field | Meaning | Type |
|---|---|---|
| response_id | Synthetic survey response identifier | String |
| team_id | Synthetic team identifier | String |
| department | Employee department | Category |
| country | Synthetic country grouping | Category |
| region | Workforce region | Category |
| gender_group | Synthetic grouped gender category | Category |
| age_band | Synthetic age band | Category |
| job_level | Organisational level | Category |
| tenure_band | Employee tenure category | Category |
| work_model | Working arrangement | Category |
| shift_worker | Whether the synthetic employee is a shift worker | Boolean |
| responded | Whether the employee responded to the survey | Boolean |
| submitted_date | Synthetic survey submission date | Date |
| enps | Synthetic employee advocacy outcome | Numeric |
| bel_01–bel_03 | Belonging items | 1–5 Likert |
| voi_01–voi_03 | Employee Voice items | 1–5 Likert |
| psy_01–psy_03 | Psychological Safety items | 1–5 Likert |
| fair_01–fair_03 | Fairness & Opportunity items | 1–5 Likert |
| ldr_01–ldr_03 | Inclusive Leadership items | 1–5 Likert |
| inc_out_01–inc_out_03 | Overall inclusion outcome items | 1–5 Likert |

---

# Inclusion Dimensions

## Belonging

Measures employees' sense of connection, authenticity and value
within the organisation and their team.

## Employee Voice

Measures whether employees feel able to express opinions,
concerns and different perspectives.

## Psychological Safety

Measures whether employees feel safe speaking openly, challenging
existing practices and asking for help.

## Fairness & Opportunity

Measures perceptions of fair treatment, promotion and access to
career development.

## Inclusive Leadership

Measures whether leaders and managers demonstrate inclusive
behaviours and respond to inclusion concerns.

---

# Derived Inclusion Measures

File:

`data/inclusion_scored.csv`

| Field | Meaning |
|---|---|
| Belonging | Mean score of the three Belonging items |
| Employee Voice | Mean score of the three Employee Voice items |
| Psychological Safety | Mean score of the three Psychological Safety items |
| Fairness & Opportunity | Mean score of the three Fairness & Opportunity items |
| Inclusive Leadership | Mean score of the three Inclusive Leadership items |
| inclusion_index_1_5 | Mean of the five dimension scores |
| inclusion_index_0_100 | Inclusion Index transformed to a 0–100 scale |
| inclusion_outcome | Mean of the three overall inclusion outcome items |

### Inclusion Index transformation

The 1–5 Inclusion Index is transformed to a 0–100 scale using:

`((score - 1) / 4) × 100`

---

# Favourable Percentage

Favourable percentage represents the share of responses scoring
4 or 5 on the relevant Likert-scale items.

---

# Segment Data

The project analyses inclusion across:

- Region
- Gender group
- Age band
- Department
- Job level
- Tenure
- Work model

Groups with fewer than five respondents are suppressed.

---

# Driver Analysis

File:

`data/inclusion_driver_summary.csv`

The project uses Pearson correlation to describe the association
between each inclusion dimension and the separate overall inclusion
outcome.

Correlation ranges from -1 to +1.

This analysis is descriptive and does not establish causality.

---

# DE&I Event Data

File:

`data/dei_events.csv`

| Field | Meaning |
|---|---|
| event_id | Synthetic event identifier |
| event_name | Synthetic DE&I event name |
| event_type | Event category |
| region | Synthetic event region |
| invited | Number invited |
| attended | Number attending |
| attendance_rate | Attendance divided by invitations |
| no_show_rate | Share of invitees who did not attend |
| knowledge_before | Self-reported knowledge before event |
| knowledge_after | Self-reported knowledge after event |
| knowledge_gain | Difference between after and before |
| satisfaction_1_5 | Event satisfaction |
| recommendation_1_5 | Recommendation score |
| repeat_participation_pct | Intended future participation |
| estimated_cost | Synthetic estimated event cost |

---

# Data Ethics

All data is synthetic and intended for portfolio demonstration.

No real employee records are included.

Segment-level reporting applies a minimum group threshold of five
respondents to demonstrate confidentiality-aware reporting.

Synthetic relationships should not be interpreted as real-world
organisational findings.