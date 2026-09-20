# Data Dictionary

This folder contains the synthetic data used by the **Global Inclusion & Belonging Analytics** project.

All employee and DE&I event records are synthetic. No real employee data, confidential organisational data, or data from a real company is included.

The survey generator uses fixed random seed `7`, so regenerating the data produces reproducible outputs with the same supported Python version.

## Dataset Overview

The synthetic workforce survey represents approximately:

| Attribute | Value |
|---|---:|
| Employees invited | 3,800 |
| Survey respondents | Approximately 2,800 |
| Teams | Approximately 149 |
| Countries | 4 |
| Departments | 6 |
| Survey fieldwork | 4-22 May 2026 |

The invite list includes both respondents and non-respondents. This allows the project to calculate participation rates and demonstrate how response patterns can affect interpretation.

## Files

### `survey_responses.csv`

One row per invited employee. Non-respondents are retained with empty survey-answer fields.

Important fields include:

| Field | Description |
|---|---|
| `response_id` | Synthetic response identifier. |
| `team_id` | Synthetic team identifier. |
| `department` | Synthetic department category. |
| `country` | Synthetic country category. |
| `region` | Synthetic region category. |
| `gender_group` | Synthetic grouped gender category. |
| `age_band` | Synthetic age category. |
| `job_level` | Individual contributor, team lead, manager, or senior leader. |
| `tenure_band` | Synthetic tenure category. |
| `work_model` | Onsite, hybrid, or remote. |
| `shift_worker` | Whether the synthetic role is shift-based. |
| `responded` | `1` when the employee responded and `0` otherwise. |
| `submitted_date` | Synthetic survey submission date. |
| `enps` | Synthetic 0-10 recommendation score. |

### `survey_instrument.csv`

The questionnaire used to generate the survey responses. It contains the item ID, construct, wording, and whether the item is a dimension item or a separate outcome item.

### `survey_comments.csv`

Synthetic free-text responses to `what_to_change` and `what_works`. The comments are illustrative and should not be interpreted as real employee verbatims.

### `comment_themes_truth.csv`

Synthetic metadata identifying the inclusion construct and tone used when generating each comment. It is included as transparent metadata for possible future qualitative-text evaluation; it is not a real-world annotation set.

### `teams.csv`

Synthetic team roster data, including department, country, manager identifier, manager tenure, and team size.

### `dei_events.csv`

Synthetic DE&I event-level data used for participation, learning, experience, and cost analysis.

## Survey Constructs

The survey contains five inclusion dimensions. Each dimension has three items measured on a five-point Likert scale:

- `1` = Strongly disagree
- `2` = Disagree
- `3` = Neither agree nor disagree
- `4` = Agree
- `5` = Strongly agree

### Belonging

- `bel_01`: I feel a sense of belonging at this organisation.
- `bel_02`: I can be myself at work.
- `bel_03`: I feel valued as a member of my team.

### Employee Voice

- `voi_01`: My opinions and ideas are taken seriously.
- `voi_02`: I feel comfortable raising concerns in my team.
- `voi_03`: Employees are encouraged to share different perspectives.

### Psychological Safety

- `psy_01`: I can speak openly about mistakes without fear of unfair consequences.
- `psy_02`: It is safe to challenge the way things are done in my team.
- `psy_03`: I feel comfortable asking for help when I need it.

### Fairness & Opportunity

- `fair_01`: People have fair access to career development opportunities.
- `fair_02`: Promotion decisions are made fairly.
- `fair_03`: People are treated fairly regardless of their background.

### Inclusive Leadership

- `ldr_01`: Leaders demonstrate that inclusion is important.
- `ldr_02`: My manager values different perspectives.
- `ldr_03`: Leaders take action when inclusion concerns are raised.

The categories, item wordings, and responses are synthetic examples created for a portfolio demonstration.

## Separate Inclusion Outcome

The project includes three separate overall inclusion outcome items:

- `inc_out_01`: Overall, this organisation is a place where people from different backgrounds can thrive.
- `inc_out_02`: I would recommend this organisation as an inclusive place to work.
- `inc_out_03`: I believe this organisation creates an environment where everyone can contribute.

These items are kept separate from the five Inclusion Index dimensions. The separate outcome allows the association analysis to examine how each dimension relates to an overall outcome without simply correlating a composite score with itself.

The outcome is descriptive and synthetic. It is not a validated organisational criterion.

## Workforce Segmentation

The current analysis compares groups across these synthetic variables:

- `region`
- `gender_group`
- `age_band`
- `department`
- `job_level`
- `tenure_band`
- `work_model`

These categories are generated for portfolio analysis. They do not represent the demographics, organisational structure, or workforce taxonomy of a real organisation.

## Inclusion Index

For each respondent:

1. The three items for each construct are averaged to produce a dimension score.
2. The five dimension scores are averaged to produce the 1-5 Inclusion Index.
3. The 1-5 Index is transformed to a 0-100 scale using:

```text
((score - 1) / 4) * 100
```

The project reports both the dimension scores and the overall Inclusion Index.

## Favourable Percentage

A response is counted as favourable when it is scored `4` or `5` on the five-point Likert scale.

```text
Favourable percentage = favourable responses / valid responses * 100
```

## Confidentiality

Groups with fewer than five respondents are suppressed in segment-level reporting.

This is a portfolio demonstration of confidentiality-aware People Analytics. A threshold of five is not universally sufficient for production HR reporting. Real organisations would need to consider re-identification risk, combinations of attributes, local privacy requirements, and organisational governance.

## Synthetic Data Design

The generator includes deliberate synthetic mechanisms so the analytical workflow has interpretable structure rather than pure random noise:

- Team-level effects create variation between synthetic teams.
- Manager-related effects influence inclusive leadership, psychological safety, and belonging scores.
- Country and region effects create small geographic differences.
- Demographic and group effects create variation across synthetic gender and age categories.
- Department effects influence selected inclusion dimensions.
- Tenure effects create differences across tenure bands.
- Job-level effects create differences across organisational levels.
- Work-model and shift-worker patterns influence some response and inclusion values.
- Response and non-response patterns create a demonstrable participation-bias consideration.
- Synthetic comments are more likely to be written in relation to a respondent's stronger or weaker inclusion signals.

These mechanisms are design choices for a portfolio dataset. They are not empirical findings about real employees.

## DE&I Event Dataset

`dei_events.csv` contains one row per synthetic event.

| Field | Description |
|---|---|
| `event_id` | Synthetic event identifier. |
| `event_name` | Synthetic event name. |
| `event_type` | Synthetic event category. |
| `region` | Synthetic event region. |
| `invited` | Number of people invited. |
| `attended` | Number of attendees. |
| `attendance_rate` | Attendees divided by invitees. |
| `no_show_rate` | Invitees who did not attend divided by invitees. |
| `knowledge_before` | Self-reported knowledge before the event. |
| `knowledge_after` | Self-reported knowledge after the event. |
| `knowledge_gain` | Knowledge after minus knowledge before. |
| `satisfaction_1_5` | Self-reported event satisfaction on a 1-5 scale. |
| `recommendation_1_5` | Event recommendation score on a 1-5 scale. |
| `repeat_participation_pct` | Intended future participation percentage. |
| `estimated_cost` | Synthetic estimated event cost. |

Event effectiveness is described through attendance, no-show rate, pre/post knowledge change, satisfaction, recommendation, repeat participation intention, and estimated cost per attendee.

These metrics indicate participation, learning, and participant experience. They do not by themselves prove long-term improvement in organisational inclusion. A stronger evaluation could connect event participation with repeated inclusion measurements over time.

The project does not claim return on investment because it does not implement a genuine financial-benefit calculation.

## Generated Analytical Outputs

The pipeline creates the following derived files:

- `inclusion_scored.csv`: respondent-level dimension scores, Inclusion Index values, segment fields, and the separate inclusion outcome.
- `inclusion_dimension_summary.csv`: five dimension scores, favourable percentages, and response counts.
- `inclusion_segment_summary.csv`: segment counts, Inclusion Index values, and gaps versus the company-wide score. Small groups are suppressed.
- `inclusion_driver_summary.csv`: Pearson correlations between each inclusion dimension and the separate inclusion outcome. The filename is retained for compatibility; user-facing documentation calls this association analysis.
- `dei_event_summary.csv`: aggregate event count, attendance, knowledge gain, satisfaction, repeat participation, and cost metrics.

## Limitations

- All data is synthetic and cannot support claims about a real organisation.
- The analysis is cross-sectional and does not show change over time.
- Pearson correlation does not establish causation.
- The survey instrument is illustrative and has not undergone external psychometric validation. A production implementation would require appropriate reliability, construct-validity, measurement-invariance, and fairness evaluation before organisational decision-making.
- The survey instrument uses a five-point response scale and simplified synthetic demographic categories.
- Segment differences may have several possible explanations that are not separately identified.
- Response patterns may mean that respondents are not perfectly representative of all invited employees.
- Event metrics do not establish long-term behavioural or organisational impact.
- The synthetic outcome is partly generated from the underlying dimensions, so observed associations are partly design-driven.
