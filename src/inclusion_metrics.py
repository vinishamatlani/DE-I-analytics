import csv
from collections import defaultdict
from pathlib import Path

from generate_survey import ITEMS, DIMENSIONS, OUTCOME_ITEMS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

INPUT_FILE = DATA / "survey_responses.csv"

SCORED_FILE = DATA / "inclusion_scored.csv"
DIMENSION_FILE = DATA / "inclusion_dimension_summary.csv"
SEGMENT_FILE = DATA / "inclusion_segment_summary.csv"

MIN_GROUP = 5


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def mean(values):
    values = [float(v) for v in values if v not in ("", None)]

    if not values:
        return None

    return sum(values) / len(values)


def favourable(values):
    """
    Percentage of responses that are Agree (4) or Strongly Agree (5).
    """
    values = [float(v) for v in values if v not in ("", None)]

    if not values:
        return None

    return sum(v >= 4 for v in values) / len(values)


def score_0_100(score):
    """
    Converts the 1-5 Likert scale to a 0-100 scale.

    1 -> 0
    2 -> 25
    3 -> 50
    4 -> 75
    5 -> 100
    """
    if score is None:
        return None

    return ((score - 1) / 4) * 100


def read_csv(path):
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, rows):
    if not rows:
        return

    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Map survey questions to their five inclusion dimensions
# ---------------------------------------------------------------------------

DIMENSION_ITEMS = defaultdict(list)

for item_id, (dimension, _wording, _bias) in ITEMS.items():
    DIMENSION_ITEMS[dimension].append(item_id)


# ---------------------------------------------------------------------------
# Respondent scoring
# ---------------------------------------------------------------------------

def score_respondents(rows):

    scored = []

    for row in rows:

        # Nonrespondents remain in the source dataset for participation analysis,
        # but cannot receive an Inclusion Index.
        if row["responded"] != "1":
            continue

        result = {
            "response_id": row["response_id"],
            "department": row["department"],
            "country": row["country"],
            "region": row.get("region", ""),
            "gender_group": row.get("gender_group", ""),
            "age_band": row.get("age_band", ""),
            "job_level": row["job_level"],
            "tenure_band": row["tenure_band"],
            "work_model": row["work_model"],
        }

        dimension_scores = []

        for dimension in DIMENSIONS:

            item_ids = DIMENSION_ITEMS[dimension]

            values = [
                row[item_id]
                for item_id in item_ids
                if row.get(item_id, "") != ""
            ]

            dimension_score = mean(values)

            result[dimension] = round(dimension_score, 3)

            dimension_scores.append(dimension_score)

        # Overall Inclusion Index = mean of the five construct scores.
        inclusion_index = mean(dimension_scores)

        result["inclusion_index_1_5"] = round(inclusion_index, 3)

        result["inclusion_index_0_100"] = round(
            score_0_100(inclusion_index),
            1,
        )

        # Separate outcome scale used for driver analysis.
        outcome_values = [
            row[item_id]
            for item_id in OUTCOME_ITEMS
            if row.get(item_id, "") != ""
        ]

        outcome_score = mean(outcome_values)

        result["inclusion_outcome"] = round(outcome_score, 3)

        scored.append(result)

    return scored


# ---------------------------------------------------------------------------
# Overall dimension scorecard
# ---------------------------------------------------------------------------

def dimension_summary(rows):

    output = []

    respondents = [r for r in rows if r["responded"] == "1"]

    for dimension in DIMENSIONS:

        item_ids = DIMENSION_ITEMS[dimension]

        all_values = []

        for row in respondents:
            for item_id in item_ids:
                value = row.get(item_id, "")

                if value != "":
                    all_values.append(value)

        avg = mean(all_values)
        fav = favourable(all_values)

        output.append({
            "dimension": dimension,
            "n_responses": len(all_values),
            "mean_score_1_5": round(avg, 3),
            "score_0_100": round(score_0_100(avg), 1),
            "favourable_pct": round(fav * 100, 1),
        })

    return output


# ---------------------------------------------------------------------------
# Segment analysis
# ---------------------------------------------------------------------------

SEGMENT_COLUMNS = [
    "region",
    "gender_group",
    "age_band",
    "department",
    "job_level",
    "tenure_band",
    "work_model",
]


def segment_summary(scored_rows):

    company_mean = mean(
        r["inclusion_index_0_100"]
        for r in scored_rows
    )

    output = []

    for segment_column in SEGMENT_COLUMNS:

        groups = defaultdict(list)

        for row in scored_rows:

            value = row.get(segment_column, "")

            if value:
                groups[value].append(row)

        for group_name, group_rows in groups.items():

            n = len(group_rows)

            # Confidentiality suppression.
            if n < MIN_GROUP:
                output.append({
                    "segment_type": segment_column,
                    "segment": group_name,
                    "n": n,
                    "inclusion_index": "SUPPRESSED",
                    "gap_vs_company": "SUPPRESSED",
                })

                continue

            group_mean = mean(
                r["inclusion_index_0_100"]
                for r in group_rows
            )

            output.append({
                "segment_type": segment_column,
                "segment": group_name,
                "n": n,
                "inclusion_index": round(group_mean, 1),
                "gap_vs_company": round(group_mean - company_mean, 1),
            })

    return output


def main():

    rows = read_csv(INPUT_FILE)

    scored = score_respondents(rows)

    dimensions = dimension_summary(rows)

    segments = segment_summary(scored)

    write_csv(SCORED_FILE, scored)
    write_csv(DIMENSION_FILE, dimensions)
    write_csv(SEGMENT_FILE, segments)

    overall = mean(
        r["inclusion_index_0_100"]
        for r in scored
    )

    print()
    print("INCLUSION ANALYTICS")
    print("-------------------")
    print(f"Respondents scored : {len(scored):,}")
    print(f"Inclusion Index    : {overall:.1f} / 100")
    print(f"Dimensions         : {len(DIMENSIONS)}")
    print(f"Segment rows       : {len(segments)}")
    print()
    print(f"Created {SCORED_FILE.name}")
    print(f"Created {DIMENSION_FILE.name}")
    print(f"Created {SEGMENT_FILE.name}")


if __name__ == "__main__":
    main()