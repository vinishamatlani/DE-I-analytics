import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "inclusion_dashboard.html"


def read_csv(filename):
    path = DATA / filename
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fmt(value, decimals=1):
    if value in ("", None):
        return "—"
    return f"{float(value):.{decimals}f}"


def esc(value):
    return html.escape(str(value))


def build_dimension_rows(rows):
    output = []

    for row in rows:
        score = float(row["score_0_100"])
        favourable = float(row["favourable_pct"])

        output.append(
            f"""
            <tr>
                <td>{esc(row["dimension"])}</td>
                <td><strong>{score:.1f}</strong></td>
                <td>{favourable:.1f}%</td>
            </tr>
            """
        )

    return "".join(output)


def build_segment_rows(rows):
    visible = [
        row for row in rows
        if row["inclusion_index"] != "SUPPRESSED"
    ]

    visible.sort(
        key=lambda r: float(r["gap_vs_company"])
    )

    output = []

    for row in visible[:15]:
        gap = float(row["gap_vs_company"])

        output.append(
            f"""
            <tr>
                <td>{esc(row["segment_type"])}</td>
                <td>{esc(row["segment"])}</td>
                <td>{row["n"]}</td>
                <td>{float(row["inclusion_index"]):.1f}</td>
                <td>{gap:+.1f}</td>
            </tr>
            """
        )

    return "".join(output)


def build_driver_rows(rows):
    output = []

    for row in rows:
        correlation = float(
            row["correlation_with_inclusion_outcome"]
        )

        output.append(
            f"""
            <tr>
                <td>{esc(row["dimension"])}</td>
                <td>{float(row["average_score_1_5"]):.2f}</td>
                <td>{correlation:.3f}</td>
            </tr>
            """
        )

    return "".join(output)


def build_event_rows(rows):
    output = []

    for row in rows:
        output.append(
            f"""
            <tr>
                <td>{esc(row["event_name"])}</td>
                <td>{esc(row["event_type"])}</td>
                <td>{row["attended"]}</td>
                <td>{float(row["attendance_rate"]) * 100:.1f}%</td>
                <td>{float(row["knowledge_gain"]):.2f}</td>
                <td>{float(row["satisfaction_1_5"]):.2f}</td>
            </tr>
            """
        )

    return "".join(output)


def main():
    dimensions = read_csv(
        "inclusion_dimension_summary.csv"
    )

    segments = read_csv(
        "inclusion_segment_summary.csv"
    )

    drivers = read_csv(
        "inclusion_driver_summary.csv"
    )

    events = read_csv(
        "dei_events.csv"
    )

    event_summary = read_csv(
        "dei_event_summary.csv"
    )[0]

    overall_index = sum(
        float(row["score_0_100"])
        for row in dimensions
    ) / len(dimensions)

    lowest_dimension = min(
        dimensions,
        key=lambda row: float(row["score_0_100"])
    )

    top_driver = max(
        drivers,
        key=lambda row: float(
            row["correlation_with_inclusion_outcome"]
        )
    )

    html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">

<title>Global Inclusion & Belonging Analytics</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f5f7fa;
    color: #1f2937;
}}

header {{
    background: #172554;
    color: white;
    padding: 32px 50px;
}}

header h1 {{
    margin: 0 0 8px 0;
}}

header p {{
    margin: 0;
    opacity: 0.85;
}}

.container {{
    max-width: 1250px;
    margin: 30px auto;
    padding: 0 25px;
}}

.grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 22px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}

.card h3 {{
    margin-top: 0;
    font-size: 14px;
    color: #6b7280;
}}

.metric {{
    font-size: 32px;
    font-weight: bold;
}}

.section {{
    background: white;
    padding: 25px;
    margin-bottom: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 11px;
    border-bottom: 1px solid #e5e7eb;
    text-align: left;
}}

th {{
    background: #f8fafc;
}}

.note {{
    background: #f8fafc;
    padding: 15px;
    border-left: 4px solid #64748b;
    margin-top: 15px;
}}

</style>
</head>

<body>

<header>

<h1>Global Inclusion & Belonging Analytics</h1>

<p>
Synthetic workforce survey and DE&I event analytics
</p>

</header>

<div class="container">

<div class="grid">

<div class="card">
<h3>OVERALL INCLUSION INDEX</h3>
<div class="metric">
{overall_index:.1f}/100
</div>
</div>

<div class="card">
<h3>LOWEST DIMENSION</h3>
<div class="metric">
{esc(lowest_dimension["dimension"])}
</div>
<div>
{float(lowest_dimension["score_0_100"]):.1f}/100
</div>
</div>

<div class="card">
<h3>EVENTS ANALYSED</h3>
<div class="metric">
{event_summary["number_of_events"]}
</div>
</div>

<div class="card">
<h3>EVENT ATTENDANCE</h3>
<div class="metric">
{event_summary["attendance_rate_pct"]}%
</div>
</div>

</div>


<div class="section">

<h2>1. Executive Inclusion Overview</h2>

<p>
The Inclusion Index is calculated from five dimensions:
Belonging, Employee Voice, Psychological Safety,
Fairness & Opportunity, and Inclusive Leadership.
</p>

<table>

<thead>
<tr>
<th>Dimension</th>
<th>Score / 100</th>
<th>Favourable</th>
</tr>
</thead>

<tbody>
{build_dimension_rows(dimensions)}
</tbody>

</table>

</div>


<div class="section">

<h2>2. Workforce Inclusion Gaps</h2>

<p>
Segment results are compared with the company-wide Inclusion Index.
Groups with fewer than five respondents are suppressed.
</p>

<table>

<thead>
<tr>
<th>Segment Type</th>
<th>Segment</th>
<th>N</th>
<th>Index</th>
<th>Gap vs Company</th>
</tr>
</thead>

<tbody>
{build_segment_rows(segments)}
</tbody>

</table>

</div>


<div class="section">

<h2>3. What Drives Inclusion?</h2>

<p>
The table below shows Pearson correlations between each
Inclusion Index dimension and the separate overall inclusion
outcome.
</p>

<table>

<thead>
<tr>
<th>Dimension</th>
<th>Average Score</th>
<th>Correlation</th>
</tr>
</thead>

<tbody>
{build_driver_rows(drivers)}
</tbody>

</table>

<div class="note">
<strong>Interpretation:</strong>
{esc(top_driver["dimension"])} has the strongest observed
association with the synthetic inclusion outcome
in this dataset. This is an association, not evidence of
causation.
</div>

</div>


<div class="section">

<h2>4. DE&I Event Effectiveness</h2>

<table>

<thead>
<tr>
<th>Event</th>
<th>Type</th>
<th>Attended</th>
<th>Attendance</th>
<th>Knowledge Gain</th>
<th>Satisfaction</th>
</tr>
</thead>

<tbody>
{build_event_rows(events)}
</tbody>

</table>

<br>

<p>
<strong>Average knowledge gain:</strong>
{event_summary["average_knowledge_gain"]}
</p>

<p>
<strong>Average satisfaction:</strong>
{event_summary["average_satisfaction_1_5"]}/5
</p>

<p>
<strong>Repeat participation:</strong>
{event_summary["repeat_participation_pct"]}%
</p>

<p>
<strong>Estimated cost per attendee:</strong>
{event_summary["cost_per_attendee"]}
</p>

</div>


<div class="section">

<h2>Methodology & Ethics</h2>

<p>
This project uses synthetic data for portfolio demonstration.
No real employee information is used.
</p>

<p>
Segment results with fewer than five respondents are suppressed
to demonstrate a basic confidentiality protection.
</p>

<p>
Driver analysis describes statistical association only and
should not be interpreted as causal evidence.
</p>

</div>

</div>

</body>
</html>
"""

    OUTPUT.write_text(
        html_output,
        encoding="utf-8"
    )

    print()
    print("INCLUSION DASHBOARD")
    print("-------------------")
    print(f"Overall Inclusion Index : {overall_index:.1f}/100")
    print(f"Lowest dimension        : {lowest_dimension['dimension']}")
    print(f"Strongest association   : {top_driver['dimension']}")
    print(f"Created                 : {OUTPUT}")


if __name__ == "__main__":
    main()