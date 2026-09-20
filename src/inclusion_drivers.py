import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

INPUT_FILE = DATA / "inclusion_scored.csv"
OUTPUT_FILE = DATA / "inclusion_driver_summary.csv"


DIMENSIONS = [
    "Belonging",
    "Employee Voice",
    "Psychological Safety",
    "Fairness & Opportunity",
    "Inclusive Leadership",
]


def mean(values):
    return sum(values) / len(values)


def pearson(x, y):

    if len(x) != len(y) or len(x) < 2:
        return 0

    mean_x = mean(x)
    mean_y = mean(y)

    numerator = sum(
        (a - mean_x) * (b - mean_y)
        for a, b in zip(x, y)
    )

    denominator_x = math.sqrt(
        sum((a - mean_x) ** 2 for a in x)
    )

    denominator_y = math.sqrt(
        sum((b - mean_y) ** 2 for b in y)
    )

    denominator = denominator_x * denominator_y

    if denominator == 0:
        return 0

    return numerator / denominator


def read_csv(path):

    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, rows):

    with path.open("w", newline="", encoding="utf-8") as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(rows)


def main():

    rows = read_csv(INPUT_FILE)

    outcome = [
        float(r["inclusion_outcome"])
        for r in rows
    ]

    results = []

    for dimension in DIMENSIONS:

        dimension_values = [
            float(r[dimension])
            for r in rows
        ]

        correlation = pearson(
            dimension_values,
            outcome,
        )

        average_score = mean(dimension_values)

        results.append({
            "dimension": dimension,
            "average_score_1_5": round(average_score, 3),
            "correlation_with_inclusion_outcome": round(
                correlation,
                3,
            ),
        })

    results.sort(
        key=lambda r:
        r["correlation_with_inclusion_outcome"],
        reverse=True,
    )

    write_csv(
        OUTPUT_FILE,
        results,
    )

    print()
    print("INCLUSION ASSOCIATION ANALYSIS")
    print("------------------------------")

    for result in results:

        print(
            f'{result["dimension"]:<25} '
            f'r = {result["correlation_with_inclusion_outcome"]:.3f}'
        )

    print()
    print(f"Created {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()