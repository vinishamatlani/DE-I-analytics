import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

OUTPUT = REPORTS / "inclusion_executive_report.md"


def read_csv(filename):
    with (DATA / filename).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    REPORTS.mkdir(exist_ok=True)

    dimensions = read_csv(
        "inclusion_dimension_summary.csv"
    )

    segments = read_csv(
        "inclusion_segment_summary.csv"
    )

    drivers = read_csv(
        "inclusion_driver_summary.csv"
    )

    event_summary = read_csv(
        "dei_event_summary.csv"
    )[0]

    overall_index = sum(
        float(r["score_0_100"])
        for r in dimensions
    ) / len(dimensions)

    lowest = min(
        dimensions,
        key=lambda r: float(r["score_0_100"])
    )

    strongest_driver = max(
        drivers,
        key=lambda r:
        float(r["correlation_with_inclusion_outcome"])
    )

    visible_segments = [
        r for r in segments
        if r["inclusion_index"] != "SUPPRESSED"
    ]

    lowest_segments = sorted(
        visible_segments,
        key=lambda r: float(r["gap_vs_company"])
    )[:5]

    report = f"""# Global Inclusion & Belonging Analytics

## Executive Summary

The synthetic workforce survey produces an overall Inclusion
Index of **{overall_index:.1f}/100**.

The lowest-scoring inclusion dimension is
**{lowest["dimension"]}**, at **{float(lowest["score_0_100"]):.1f}/100**.

The dimension with the strongest statistical association with
the separate inclusion outcome is
**{strongest_driver["dimension"]}**
(r = {float(strongest_driver["correlation_with_inclusion_outcome"]):.3f}).

These results describe patterns in a synthetic dataset and should
not be interpreted as evidence of causal relationships.

---

## 1. Inclusion Scorecard

| Dimension | Score / 100 | Favourable % |
|---|---:|---:|
"""

    for row in dimensions:
        report += (
            f'| {row["dimension"]} | '
            f'{float(row["score_0_100"]):.1f} | '
            f'{float(row["favourable_pct"]):.1f}% |\n'
        )

    report += """
---

## 2. Workforce Gaps

The analysis compares each sufficiently sized workforce segment
with the overall company Inclusion Index.

Groups with fewer than five respondents are suppressed.

### Largest observed negative gaps

| Segment Type | Segment | N | Index | Gap |
|---|---|---:|---:|---:|
"""

    for row in lowest_segments:
        report += (
            f'| {row["segment_type"]} | '
            f'{row["segment"]} | '
            f'{row["n"]} | '
            f'{float(row["inclusion_index"]):.1f} | '
            f'{float(row["gap_vs_company"]):+.1f} |\n'
        )

    report += f"""

---

## 3. Inclusion Association Analysis

The association analysis uses Pearson correlation between the five
Inclusion Index dimensions and a separate overall inclusion outcome.
Pearson correlation describes the strength and direction of a linear
association; it does not establish causation.

| Dimension | Average Score | Correlation |
|---|---:|---:|
"""

    for row in drivers:
        report += (
            f'| {row["dimension"]} | '
            f'{float(row["average_score_1_5"]):.2f} | '
            f'{float(row["correlation_with_inclusion_outcome"]):.3f} |\n'
        )

    report += f"""

### Interpretation

The strongest association in this synthetic dataset is
**{strongest_driver["dimension"]}**.

Because the dataset is synthetic and the inclusion outcome was
generated from the underlying inclusion dimensions, these
relationships are partly design-driven. They demonstrate the
analytics workflow rather than establish empirical causal claims.

---

## 4. DE&I Event Effectiveness

| Metric | Result |
|---|---:|
| Events analysed | {event_summary["number_of_events"]} |
| Total invited | {event_summary["total_invited"]} |
| Total attended | {event_summary["total_attended"]} |
| Attendance rate | {event_summary["attendance_rate_pct"]}% |
| Average knowledge gain | {event_summary["average_knowledge_gain"]} |
| Average satisfaction | {event_summary["average_satisfaction_1_5"]}/5 |
| Repeat participation | {event_summary["repeat_participation_pct"]}% |
| Estimated total cost | {event_summary["estimated_total_cost"]} |
| Cost per attendee | {event_summary["cost_per_attendee"]} |

---

## 5. Suggested Intervention Areas

### 1. Strengthen Psychological Safety

Potential measures:

- Psychological safety score
- Percentage favourable
- Gap between departments
- Change in score over subsequent survey cycles

### 2. Strengthen Employee Voice

Potential measures:

- Employee Voice score
- Percentage favourable
- Participation in listening channels
- Percentage of raised issues receiving documented follow-up

### 3. Improve Fairness & Opportunity

Potential measures:

- Fairness & Opportunity score
- Career-development access
- Promotion fairness perceptions
- Segment-level inclusion gaps

These are proposed measurement areas rather than claims that
the synthetic analysis has established a causal intervention effect.

---

## 6. Confidentiality & Responsible Analytics

The project applies a minimum reporting threshold of five
respondents for segment reporting.

The data is entirely synthetic.

No individual-level employee conclusions should be drawn from
the dataset.

Association analysis is descriptive rather than causal.

The survey instrument is illustrative and has not undergone external
psychometric validation. A production implementation would require
appropriate reliability, construct-validity, measurement-invariance
and fairness evaluation before organisational decision-making.

---

## 7. Portfolio Positioning

This project demonstrates an end-to-end people analytics workflow:

1. Synthetic survey generation
2. Inclusion Index construction
3. Dimension-level analysis
4. Workforce segmentation
5. Confidentiality suppression
6. Inclusion association analysis
7. DE&I event effectiveness analysis
8. Executive dashboard creation
9. Business-oriented recommendations
"""

    OUTPUT.write_text(
        report,
        encoding="utf-8"
    )

    print()
    print("EXECUTIVE REPORT")
    print("----------------")
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()