# Global Inclusion & Belonging Analytics

An end-to-end people analytics portfolio project for measuring workplace inclusion, identifying segment-level signals, analysing associated factors, and designing a responsible measurement cycle.

**Live dashboard:** [Open the Global Inclusion & Belonging Analytics dashboard](https://vinishamatlani.github.io/DE-I-analytics/)

**Executive presentation:** [Download the five-slide executive brief](presentation/global_inclusion_executive_brief_polished.pptx)

> **Important:** This project uses synthetic data. The results do not represent real employees, a real organisation, real policies, or real organisational outcomes. The project demonstrates an analytical method and reporting workflow rather than making claims about a real workforce.

## Table of Contents

- [Project Overview](#project-overview)
- [Business Questions](#business-questions)
- [What the Project Measures](#what-the-project-measures)
- [Dataset](#dataset)
- [Analytical Method](#analytical-method)
- [Key Findings](#key-findings)
- [DE&I Event Analytics](#dei-event-analytics)
- [Responsible Analytics](#responsible-analytics)
- [Project Workflow](#project-workflow)
- [Repository Structure](#repository-structure)
- [How to Run the Project](#how-to-run-the-project)
- [Outputs](#outputs)
- [Limitations](#limitations)
- [Portfolio Skills Demonstrated](#portfolio-skills-demonstrated)
- [Attribution](#attribution)

## Project Overview

This project demonstrates how an organisation could build an inclusion measurement system from survey and event data.

It moves through the complete analytical lifecycle:

1. Generate a reproducible synthetic workforce dataset.
2. Calculate scores for five inclusion dimensions.
3. Build an overall Inclusion Index.
4. Compare inclusion across workforce segments.
5. Identify statistical associations with a separate inclusion outcome.
6. Analyse DE&I event participation and experience.
7. Publish the results through a dashboard, executive report, and presentation.
8. Translate the findings into a repeatable measurement framework.

The project is designed to answer a practical question:

> How can inclusion data help leaders decide what to investigate, what to measure next, and how to evaluate change responsibly?

## Business Questions

The analysis is structured around five executive questions:

1. What is the overall Inclusion Index?
2. Which inclusion dimensions are strongest and weakest?
3. Which workforce segments show the largest observed gaps?
4. Which inclusion dimensions are associated with the overall inclusion outcome?
5. How effectively are DE&I events performing?

These questions deliberately combine descriptive reporting, segmentation, statistical analysis, event measurement, and practical decision support.

## What the Project Measures

### Five inclusion dimensions

Each dimension is calculated from three survey items measured on a 1-to-5 Likert scale.

| Dimension | What it represents |
|---|---|
| **Belonging** | Whether employees feel connected, valued, included, and able to be themselves. |
| **Employee Voice** | Whether employees feel able to share opinions, concerns, and different perspectives. |
| **Psychological Safety** | Whether employees feel safe speaking openly, challenging existing practices, and asking for help. |
| **Fairness & Opportunity** | Perceptions of fair treatment, promotion, development, and access to opportunity. |
| **Inclusive Leadership** | Whether leaders and managers demonstrate inclusive behaviours and respond to inclusion concerns. |

### Inclusion Index

The overall Inclusion Index is the mean of the five dimension scores.

The survey scores are first calculated on a 1-to-5 scale and then transformed to 0-100 using:

```text
((score - 1) / 4) x 100
```

The transformation produces an intuitive executive scale:

| Survey score | Index score |
|---:|---:|
| 1 | 0 |
| 2 | 25 |
| 3 | 50 |
| 4 | 75 |
| 5 | 100 |

### Favourable percentage

Favourable percentage is the share of survey responses scoring 4 or 5, equivalent to Agree or Strongly Agree on the Likert scale.

### Segment gaps

For every sufficiently sized workforce segment, the project compares the segment Inclusion Index with the company-wide Inclusion Index:

```text
Segment gap = segment Inclusion Index - company Inclusion Index
```

A negative number means the segment score is below the company-wide score. A positive number means it is above the company-wide score.

### Driver analysis

The project calculates Pearson correlation between each of the five inclusion dimensions and a separate overall inclusion outcome. This identifies association, not causation.

## Dataset

The survey dataset represents a fictional multinational workforce:

| Dataset characteristic | Value |
|---|---:|
| Employees invited | 3,800 |
| Survey respondents | 2,753 |
| Response rate | 72.4% |
| Teams | 149 |
| Countries | 4 |
| Departments | 6 |
| Respondents who left comments | 879 |
| Survey fieldwork | 4-22 May 2026 |

The main data files are:

- [survey_responses.csv](data/survey_responses.csv): one row per invited employee, including respondents and non-respondents.
- [survey_instrument.csv](data/survey_instrument.csv): survey item wording and dimension mapping.
- [survey_comments.csv](data/survey_comments.csv): synthetic employee comments.
- [teams.csv](data/teams.csv): synthetic team roster and team attributes.
- [dei_events.csv](data/dei_events.csv): synthetic DE&I event-level data.

The full field definitions are documented in [data/README.md](data/README.md) and [reports/data_dictionary.md](reports/data_dictionary.md).

## Analytical Method

### 1. Synthetic data generation

The survey generator creates a reproducible dataset using seed `7`. Regenerating the data produces the same files on Python 3.10 or later.

The generator deliberately includes realistic structure rather than pure random noise, including:

- Differences between workforce segments.
- Latent team and manager effects.
- Lower response probability among some workforce groups.
- Correlated inclusion dimensions.
- Noisy five-point survey responses.
- Synthetic comments with themes and tone.

The mechanisms are described in [data/README.md](data/README.md), which is useful for understanding how to evaluate the analysis against known planted patterns.

### 2. Scoring respondents

Only employees marked as respondents receive dimension scores. Non-respondents remain in the original invite file so participation and response-rate analysis remain possible.

The scoring logic is implemented in [inclusion_metrics.py](src/inclusion_metrics.py).

It produces:

- Five dimension scores for each respondent.
- A 1-to-5 Inclusion Index.
- A 0-to-100 Inclusion Index.
- A separate overall inclusion outcome used for driver analysis.

### 3. Dimension summaries

The project aggregates the dimension scores across all respondents and calculates:

- Mean score on the 1-to-5 scale.
- Score on the 0-to-100 scale.
- Favourable percentage.
- Number of item responses included.

### 4. Segment analysis

The project analyses inclusion by:

- Region.
- Gender group.
- Age band.
- Department.
- Job level.
- Tenure band.
- Work model.

Groups with fewer than five respondents are suppressed. This demonstrates a basic confidentiality-aware reporting rule and prevents very small groups from being presented as stable organisational findings.

### 5. Correlation analysis

Pearson correlation is calculated for each inclusion dimension against the separate overall inclusion outcome.

The analysis is intentionally descriptive. It does not estimate intervention impact, prove a causal mechanism, or establish that changing one dimension will change the outcome.

The implementation is in [inclusion_drivers.py](src/inclusion_drivers.py).

### 6. Event analysis

The project evaluates synthetic DE&I events using participation, learning, experience, and cost measures.

The calculations are implemented in [event_analysis.py](src/event_analysis.py).

## Key Findings

### Overall scorecard

The synthetic workforce produces an overall Inclusion Index of **68.2/100**.

| Dimension | Score / 100 | Favourable |
|---|---:|---:|
| Belonging | 75.1 | 72.9% |
| Inclusive Leadership | 74.8 | 71.7% |
| Employee Voice | 66.3 | 59.2% |
| Psychological Safety | 64.3 | 56.0% |
| Fairness & Opportunity | 60.6 | 49.8% |

The strongest dimension is **Belonging**. The lowest-scoring dimension is **Fairness & Opportunity**, making perceived fairness and access to development useful areas for further investigation.

### Largest observed segment gaps

| Segment | Gap versus company |
|---|---:|
| 6-10 years tenure | -3.2 |
| Commercial | -3.1 |
| Non-binary / self-described | -2.4 |
| Operations | -2.4 |
| 3-5 years tenure | -2.1 |

These are observed differences in synthetic data. They are not explanations of why the differences exist.

### Strongest observed associations

| Dimension | Pearson correlation |
|---|---:|
| Psychological Safety | 0.372 |
| Belonging | 0.356 |
| Inclusive Leadership | 0.353 |
| Employee Voice | 0.297 |
| Fairness & Opportunity | 0.272 |

Psychological Safety has the strongest observed association with the separate overall inclusion outcome. The correct interpretation is:

> Correlation describes association, not causation.

Because the outcome is generated from the underlying synthetic dimensions, these relationships are partly design-driven. They demonstrate the workflow rather than establish empirical organisational evidence.

## DE&I Event Analytics

The synthetic event dataset contains eight events.

| Metric | Result |
|---|---:|
| Events analysed | 8 |
| Attendance rate | 63.3% |
| Average knowledge gain | 0.70 |
| Average satisfaction | 4.21 / 5 |
| Repeat participation intention | 74.7% |
| Estimated cost per attendee | 34.17 |

These measures provide a starting point for evaluating whether events attract participation, create perceived learning, deliver a positive experience, and encourage future participation.

They should not be interpreted as proof that an event caused a change in inclusion outcomes. A stronger evaluation would connect participation to later survey responses using an appropriate longitudinal design.

## Responsible Analytics

This project is designed to model responsible people analytics practices:

- **Synthetic data only:** no real employee records are included.
- **Confidentiality threshold:** groups with fewer than five respondents are suppressed.
- **No individual conclusions:** the analysis is intended for group-level patterns, not employee-level judgement.
- **Causal restraint:** correlations and segment gaps are not presented as causal explanations.
- **Context before action:** quantitative signals should be followed by qualitative investigation and operational context.
- **Measurement over assumptions:** proposed interventions include follow-up measures rather than being presented as guaranteed solutions.

## Project Workflow

The main orchestration script is [run_inclusion.py](src/run_inclusion.py). It runs seven stages in sequence:

```text
1. Generate synthetic inclusion survey
2. Calculate Inclusion Index and segment gaps
3. Run inclusion driver analysis
4. Generate DE&I event data
5. Analyse DE&I event effectiveness
6. Build inclusion dashboard
7. Build executive inclusion report
```

The overall measurement concept is:

```text
Baseline
   ->
Intervention
   ->
Follow-up measurement
   ->
Segment analysis
   ->
Qualitative investigation
   ->
Adjust intervention
   ->
Repeat measurement
```

The recommended areas for follow-up are:

1. Psychological Safety.
2. Employee Voice.
3. Fairness & Opportunity.

The recommendations and suggested measures are described in [executive_action_plan.md](reports/executive_action_plan.md) and [intervention_framework.md](reports/intervention_framework.md).

## Repository Structure

```text
DE-I-analytics/
├── data/
│   ├── survey_responses.csv
│   ├── survey_instrument.csv
│   ├── survey_comments.csv
│   ├── teams.csv
│   ├── dei_events.csv
│   └── generated summary files
├── reports/
│   ├── data_dictionary.md
│   ├── inclusion_executive_report.md
│   ├── executive_action_plan.md
│   └── intervention_framework.md
├── presentation/
│   ├── build_presentation.py
│   └── global_inclusion_executive_brief_polished.pptx
├── src/
│   ├── run_inclusion.py
│   ├── generate_survey.py
│   ├── inclusion_metrics.py
│   ├── inclusion_drivers.py
│   ├── generate_events.py
│   ├── event_analysis.py
│   ├── build_inclusion_dashboard.py
│   ├── build_inclusion_report.py
│   └── validate_inclusion_data.py
├── index.html
├── ATTRIBUTION.md
└── README.md
```

## How to Run the Project

### Prerequisites

- Python 3.10 or later.
- PowerShell, Command Prompt, or another terminal.
- `python-pptx` if you want to regenerate the PowerPoint presentation.

The core analytics pipeline uses Python’s standard library. The presentation generator uses `python-pptx`.

### Run the analytics pipeline

From the repository root:

```powershell
python src/run_inclusion.py
```

This regenerates the synthetic data, summary CSV files, dashboard HTML, and executive report.

### Validate the generated data

```powershell
python src/validate_inclusion_data.py
```

The validation script checks file structure, required columns, valid Likert values, score ranges, confidentiality suppression, driver correlations, and event data integrity.

### Regenerate the PowerPoint

Install the presentation dependency if needed:

```powershell
python -m pip install python-pptx
```

Then run:

```powershell
python presentation/build_presentation.py
```

## Outputs

### Analysis outputs

- [inclusion_scored.csv](data/inclusion_scored.csv): respondent-level derived inclusion scores.
- [inclusion_dimension_summary.csv](data/inclusion_dimension_summary.csv): dimension scorecard and favourable percentages.
- [inclusion_segment_summary.csv](data/inclusion_segment_summary.csv): segment scores and company gaps.
- [inclusion_driver_summary.csv](data/inclusion_driver_summary.csv): dimension correlations with the separate outcome.
- [dei_events.csv](data/dei_events.csv): event-level metrics.
- [dei_event_summary.csv](data/dei_event_summary.csv): aggregate event results.

### Communication outputs

- [Live GitHub Pages dashboard](https://vinishamatlani.github.io/DE-I-analytics/).
- [Executive report](reports/inclusion_executive_report.md).
- [Executive action plan](reports/executive_action_plan.md).
- [Intervention framework](reports/intervention_framework.md).
- [Five-slide executive presentation](presentation/global_inclusion_executive_brief_polished.pptx).

## Limitations

The project is intentionally a portfolio demonstration and has important limitations:

1. The data is synthetic and cannot support claims about a real organisation.
2. The survey is cross-sectional, so it does not show how scores change over time.
3. The correlation analysis is descriptive and does not establish causation.
4. The synthetic outcome is partly generated from the inclusion dimensions, so associations are partly design-driven.
5. Segment differences may reflect multiple factors that are not separately identified.
6. A five-point Likert scale limits precision.
7. Response bias may mean respondents are not perfectly representative of all invited employees.
8. Event participation metrics do not independently prove event impact.

A real organisational deployment would require stronger governance, approved data access, privacy review, longitudinal measurement, qualitative research, and an evaluation design appropriate to the intervention.

## Portfolio Skills Demonstrated

This project demonstrates:

- Survey data generation and reproducibility.
- Data modelling and CSV-based pipelines.
- Likert-scale measurement design.
- Composite index construction.
- Favourable percentage calculation.
- Workforce segmentation.
- Confidentiality-aware reporting.
- Pearson correlation analysis.
- DE&I event effectiveness measurement.
- Executive dashboard development.
- Automated report generation.
- PowerPoint generation with editable presentation elements.
- Responsible interpretation of people analytics.
- Translation of analysis into measurable business action.

## Attribution

The project was adapted from the open-source [engagement-survey-analytics repository](https://github.com/D0M3N1C0X/engagement-survey-analytics) and substantially reframed for inclusion and belonging analytics.

See [ATTRIBUTION.md](ATTRIBUTION.md) for the adaptation notes, licensing information, and clarification that the project does not use real organisational data or proprietary branding.
