"""
Synthetic Inclusion & Belonging workforce survey generator.

Builds a complete annual survey for a fictional multinational services
organisation across APAC, EMEA, and North America
(~3,800 invited employees across 6 countries and approximately 149 teams):

    data/teams.csv             one row per team, with its manager
    data/survey_responses.csv  one row per *invited* employee - answers only
                               where the person actually responded
    data/survey_comments.csv   free-text verbatims

The invite list is included in full, non-respondents and all, because response
rate and non-response patterns are part of the analysis rather than a footnote.

Everything is stdlib with a fixed seed, so the files are reproducible across
machines. The synthetic effects, segment variation, comment themes and
response patterns are documented in data/README.md for portfolio review.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

SEED = 7
N_EMPLOYEES = 3800
SURVEY_NAME = "Voice 2026"
FIELD_START = "2026-05-04"
FIELD_END = "2026-05-22"

rng = random.Random(SEED)

# --------------------------------------------------------------------------
# Survey instrument
# --------------------------------------------------------------------------

# dimension -> (target favourable rate, synthetic outcome weight)
#
# The first value controls the approximate response level. The second shapes
# the synthetic inclusion outcome used for descriptive association analysis.
# These are simulation settings, not estimated causal effects.

DIMENSIONS = {
    "Belonging":                 (0.68, 0.22),
    "Employee Voice":            (0.60, 0.18),
    "Psychological Safety":      (0.59, 0.24),
    "Fairness & Opportunity":    (0.55, 0.17),
    "Inclusive Leadership":      (0.65, 0.19),
}


# item id -> (dimension, wording, item difficulty offset)
#
# Each inclusion dimension has 3 survey questions.
# Together these 15 questions will later be used to calculate
# the five construct scores and the overall Inclusion Index.

ITEMS = {
    # -------------------------
    # Belonging
    # -------------------------
    "bel_01": (
        "Belonging",
        "I feel a sense of belonging at this organisation",
        0.05,
    ),
    "bel_02": (
        "Belonging",
        "I can be myself at work",
        0.15,
    ),
    "bel_03": (
        "Belonging",
        "I feel valued as a member of my team",
        -0.10,
    ),

    # -------------------------
    # Employee Voice
    # -------------------------
    "voi_01": (
        "Employee Voice",
        "My opinions and ideas are taken seriously",
        -0.10,
    ),
    "voi_02": (
        "Employee Voice",
        "I feel comfortable raising concerns in my team",
        0.05,
    ),
    "voi_03": (
        "Employee Voice",
        "Employees are encouraged to share different perspectives",
        -0.05,
    ),

    # -------------------------
    # Psychological Safety
    # -------------------------
    "psy_01": (
        "Psychological Safety",
        "I can speak openly about mistakes without fear of unfair consequences",
        -0.15,
    ),
    "psy_02": (
        "Psychological Safety",
        "It is safe to challenge the way things are done in my team",
        -0.20,
    ),
    "psy_03": (
        "Psychological Safety",
        "I feel comfortable asking for help when I need it",
        0.15,
    ),

    # -------------------------
    # Fairness & Opportunity
    # -------------------------
    "fair_01": (
        "Fairness & Opportunity",
        "People have fair access to career development opportunities",
        -0.20,
    ),
    "fair_02": (
        "Fairness & Opportunity",
        "Promotion decisions are made fairly",
        -0.25,
    ),
    "fair_03": (
        "Fairness & Opportunity",
        "People are treated fairly regardless of their background",
        0.05,
    ),

    # -------------------------
    # Inclusive Leadership
    # -------------------------
    "ldr_01": (
        "Inclusive Leadership",
        "Leaders demonstrate that inclusion is important",
        0.10,
    ),
    "ldr_02": (
        "Inclusive Leadership",
        "My manager values different perspectives",
        0.15,
    ),
    "ldr_03": (
        "Inclusive Leadership",
        "Leaders take action when inclusion concerns are raised",
        -0.15,
    ),
}
# Overall inclusion outcome items.
#
# These are kept separate from the five Inclusion Index dimensions.
# This allows association analysis without correlating a composite with
# an outcome that directly contains the same component scores.

OUTCOME_ITEMS = {
    "inc_out_01": "Overall, this organisation is a place where people from different backgrounds can thrive",
    "inc_out_02": "I would recommend this organisation as an inclusive place to work",
    "inc_out_03": "I believe this organisation creates an environment where everyone can contribute",
}

RESPONSE_LABELS = {1: "Strongly disagree", 2: "Disagree", 3: "Neither",
                   4: "Agree", 5: "Strongly agree"}

# --------------------------------------------------------------------------
# Organisation
# --------------------------------------------------------------------------

COUNTRIES = {
    "IN": 0.18,
    "SG": 0.07,
    "DE": 0.15,
    "PL": 0.20,
    "US": 0.25,
    "CA": 0.15,
}

COUNTRY_TO_REGION = {
    "IN": "APAC",
    "SG": "APAC",
    "DE": "EMEA",
    "PL": "EMEA",
    "US": "North America",
    "CA": "North America",
}

# Additional workforce segments for inclusion analysis.
# These are synthetic demographic/grouping variables for portfolio analysis.

GENDER_GROUPS = {
    "Women": 0.48,
    "Men": 0.47,
    "Non-binary / self-described": 0.05,
}

AGE_BANDS = {
    "18-29": 0.22,
    "30-39": 0.31,
    "40-49": 0.25,
    "50-59": 0.16,
    "60+": 0.06,
}

DEPARTMENTS = {
    "Operations": (0.31, 0.75),
    "Customer Service": (0.24, 0.55),
    "Commercial": (0.14, 0.05),
    "Technology": (0.13, 0.02),
    "Finance & Legal": (0.09, 0.0),
    "People & Workplace": (0.09, 0.05),
}

LEVELS = {
    "Individual contributor": 0.72,
    "Team lead": 0.18,
    "Manager": 0.08,
    "Senior leader": 0.02,
}

TENURES = {
    "< 1 year": 0.19,
    "1-2 years": 0.24,
    "3-5 years": 0.27,
    "6-10 years": 0.19,
    "10 years +": 0.11,
}

WORK_MODELS = {
    "Onsite": 0.46,
    "Hybrid": 0.40,
    "Remote": 0.14,
}
# Country and department pull each dimension around a little, so the heatmap
# has real structure instead of noise.
# Synthetic effects used to create realistic inclusion differences across
# workforce segments.

# Small synthetic country-level offsets create variation in the simulated
# workforce. They are not empirical claims about employees or workplace
# inclusion in these countries.
COUNTRY_EFFECT = {
    "IN": -0.02,
    "SG": 0.04,
    "DE": -0.04,
    "PL": 0.03,
    "US": 0.05,
    "CA": 0.02,
}

REGION_EFFECT = {
    "APAC": -0.05,
    "EMEA": 0.03,
    "North America": 0.06,
}

DEPARTMENT_EFFECT = {
    "Operations": {
        "Psychological Safety": -0.20,
        "Employee Voice": -0.15,
        "Belonging": -0.10,
    },
    "Customer Service": {
        "Psychological Safety": -0.15,
        "Fairness & Opportunity": -0.10,
    },
    "Technology": {
        "Inclusive Leadership": 0.05,
        "Employee Voice": 0.05,
    },
    "Commercial": {
        "Belonging": 0.05,
        "Employee Voice": 0.03,
    },
    "Finance & Legal": {
        "Fairness & Opportunity": -0.08,
    },
    "People & Workplace": {
        "Belonging": 0.12,
        "Inclusive Leadership": 0.10,
        "Fairness & Opportunity": 0.08,
    },
}

LEVEL_EFFECT = {
    "Individual contributor": -0.10,
    "Team lead": 0.05,
    "Manager": 0.18,
    "Senior leader": 0.35,
}

TENURE_EFFECT = {
    "< 1 year": 0.18,
    "1-2 years": 0.05,
    "3-5 years": -0.05,
    "6-10 years": -0.08,
    "10 years +": 0.02,
}

GENDER_EFFECT = {
    "Women": -0.03,
    "Men": 0.04,
    "Non-binary / self-described": -0.10,
}

AGE_EFFECT = {
    "18-29": -0.05,
    "30-39": 0.02,
    "40-49": 0.04,
    "50-59": 0.01,
    "60+": -0.02,
}


# --------------------------------------------------------------------------
# Small maths helpers
# --------------------------------------------------------------------------

def phi(z: float) -> float:
    """Standard normal CDF."""
    return 0.5 * math.erfc(-z / math.sqrt(2))


def probit(p: float) -> float:
    """Inverse normal CDF by bisection - accurate enough and dependency-free."""
    lo, hi = -6.0, 6.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if phi(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def pick(weights: dict) -> str:
    keys = list(weights)
    w = [weights[k][0] if isinstance(weights[k], tuple) else weights[k] for k in keys]
    return rng.choices(keys, weights=w, k=1)[0]


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


# Latent responses are mapped to the 1-5 scale with these cut points; the
# spread of the latent variable is roughly one standard deviation.
CUTS = (-1.15, -0.35, 0.35, 1.15)
LATENT_SD = 0.95


def to_scale(latent: float) -> int:
    return 1 + sum(latent > c for c in CUTS)


def dimension_base(target_favourable: float) -> float:
    """Centre a dimension so that the company-wide favourable rate lands on target."""
    return CUTS[2] - probit(1 - target_favourable) * LATENT_SD


DIM_BASE = {dim: dimension_base(target) for dim, (target, _w) in DIMENSIONS.items()}
WEIGHTS = {dim: w for dim, (_t, w) in DIMENSIONS.items()}


# --------------------------------------------------------------------------
# Teams
# --------------------------------------------------------------------------

def make_teams() -> list[dict]:
    teams = []
    team_no = 0
    for dept, (share, _shift) in DEPARTMENTS.items():
        headcount = int(N_EMPLOYEES * share)
        assigned = 0
        while assigned < headcount:
            size = min(headcount - assigned, max(4, int(rng.triangular(4, 60, 18))))
            if headcount - assigned - size < 4:
                size = headcount - assigned
            team_no += 1
            country = pick(COUNTRIES)

            # Synthetic manager-quality variation is included to create
            # realistic team-level differences in inclusion-related responses.
            manager_quality = rng.gauss(0, 0.52)
            teams.append({
                "team_id": f"T{team_no:03d}",
                "team_name": f"{dept.split(' ')[0]} {country} {team_no:03d}",
                "department": dept,
                "country": country,
                "manager_id": f"M{team_no:03d}",
                "manager_tenure_months": int(clamp(rng.expovariate(1 / 30) + 2, 2, 140)),
                "team_size": size,
                "_manager_quality": manager_quality,
                "_team_effect": rng.gauss(0, 0.22),
            })
            assigned += size
    return teams


# --------------------------------------------------------------------------
# Respondents
# --------------------------------------------------------------------------

def make_responses(teams: list[dict]) -> list[dict]:
    rows = []
    person_no = 0

    for team in teams:
        dept = team["department"]
        shift_share = DEPARTMENTS[dept][1]

        for _ in range(team["team_size"]):
            person_no += 1
            level = pick(LEVELS)
            tenure = pick(TENURES)
            region = COUNTRY_TO_REGION[team["country"]]
            gender_group = pick(GENDER_GROUPS)
            age_band = pick(AGE_BANDS)
            work_model = "Onsite" if rng.random() < shift_share else pick(WORK_MODELS)
            shift_worker = int(work_model == "Onsite" and rng.random() < shift_share)

            # ---- latent satisfaction per dimension ----------------------
            latent = {}
            for dim in DIMENSIONS:
                value = (
                    DIM_BASE[dim]
                    + team["_team_effect"]
                    + COUNTRY_EFFECT[team["country"]]
                    + REGION_EFFECT[region]
                    + DEPARTMENT_EFFECT.get(dept, {}).get(dim, 0.0)
                    + LEVEL_EFFECT[level]
                    + TENURE_EFFECT[tenure]
                    + GENDER_EFFECT[gender_group]
                    + AGE_EFFECT[age_band]
                    + rng.gauss(0, 0.55)
                )

                # Manager quality has a stronger relationship with
                # inclusive leadership and psychological safety.
                if dim == "Inclusive Leadership":
                    value += team["_manager_quality"] * 0.85
                elif dim in ("Psychological Safety", "Belonging"):
                    value += team["_manager_quality"] * 0.40

                # Shift-based work can create a small inclusion disadvantage
                # through reduced flexibility and access to communication.
                if shift_worker and dim in ("Employee Voice", "Belonging"):
                    value -= 0.12

                latent[dim] = value

            inclusion_outcome_latent = (
                sum(WEIGHTS[d] * latent[d] for d in DIMENSIONS)
                / sum(WEIGHTS.values())
                + rng.gauss(0, 0.42)
            )

            # ---- who actually responds ---------------------------------
            # Disengaged people and shift workers answer less often: the
            # non-response bias the representativeness check has to find.
            p_response = clamp(0.74
                               + 0.11 * inclusion_outcome_latent
                               + 0.10 * (level in ("Manager", "Senior leader"))
                               - 0.16 * shift_worker
                               - 0.07 * (dept == "Operations")
                               + 0.06 * (work_model == "Remote"),
                               0.22, 0.96)
            responded = int(rng.random() < p_response)

            row = {
                "response_id": f"R{person_no:05d}",
                "team_id": team["team_id"],
                "department": dept,
                "country": team["country"],
                "region": region,
                "gender_group": gender_group,
                "age_band": age_band,
                "job_level": level,
                "tenure_band": tenure,
                "work_model": work_model,
                "shift_worker": shift_worker,
                "responded": responded,
                "submitted_date": "",
                "enps": "",
            }
            for item_id in ITEMS:
                row[item_id] = ""
            for item_id in OUTCOME_ITEMS:
                row[item_id] = ""

            if responded:
                row["submitted_date"] = random_field_date()
                for item_id, (dim, _text, bias) in ITEMS.items():
                    row[item_id] = to_scale(latent[dim] + bias + rng.gauss(0, 0.5))
                for i, item_id in enumerate(OUTCOME_ITEMS):
                    row[item_id] = to_scale(inclusion_outcome_latent + (0.15, -0.10, -0.25)[i]
                                            + rng.gauss(0, 0.5))
                row["enps"] = enps_score(inclusion_outcome_latent)

            row["_latent"] = latent
            row["_inclusion_outcome"] = inclusion_outcome_latent
            rows.append(row)

    return rows


def random_field_date() -> str:
    """Responses cluster in the first days of fieldwork and after the reminder."""
    day = rng.choices(range(19), weights=[9, 8, 6, 4, 3, 2, 2, 3, 3, 2, 2,
                                          7, 6, 4, 3, 2, 3, 5, 8], k=1)[0]
    return f"2026-05-{4 + day:02d}"


def enps_score(inclusion_outcome_latent: float) -> int:
    """0-10 recommendation score, driven by the same latent inclusion outcome."""
    raw = 6.15 + 2.1 * inclusion_outcome_latent + rng.gauss(0, 1.15)
    return int(clamp(round(raw), 0, 10))


# --------------------------------------------------------------------------
# Free-text comments
# --------------------------------------------------------------------------

# Each theme carries fragments for both survey questions and both tones.
# Comments are illustrative synthetic verbatims aligned to the current
# inclusion constructs; they are not analysed as evidence about real people.
THEMES = {
    "belonging": {
        "dimension": "Belonging",
        "negative": [
            "I rarely feel connected to the wider organisation.",
            "Some colleagues still feel like outsiders in everyday team decisions.",
            "I do not always feel valued as a member of this team.",
        ],
        "positive": [
            "My team is welcoming and people look out for one another.",
            "I feel valued and able to be myself at work.",
        ],
    },
    "voice": {
        "dimension": "Employee Voice",
        "negative": [
            "The same voices dominate meetings and other perspectives are missed.",
            "I raised a concern but did not see any follow-up.",
            "Ideas are requested, but it is not clear how they are considered.",
        ],
        "positive": [
            "Different perspectives are actively invited in our discussions.",
            "People can raise concerns and receive a visible response.",
        ],
    },
    "psychological_safety": {
        "dimension": "Psychological Safety",
        "negative": [
            "It does not always feel safe to challenge how things are done.",
            "Mistakes can feel risky to discuss openly.",
            "People sometimes hold back rather than ask for help.",
        ],
        "positive": [
            "I can raise a difficult issue without fear of unfair consequences.",
            "Questions and mistakes are treated as opportunities to learn.",
        ],
    },
    "fairness": {
        "dimension": "Fairness & Opportunity",
        "negative": [
            "Access to development opportunities does not always feel equitable.",
            "Promotion decisions are difficult to understand from an employee perspective.",
            "People from some backgrounds appear to face more barriers to opportunity.",
        ],
        "positive": [
            "Career opportunities are discussed openly and fairly.",
            "The criteria for progression are clear and applied consistently.",
        ],
    },
    "inclusive_leadership": {
        "dimension": "Inclusive Leadership",
        "negative": [
            "Leaders do not always act when inclusion concerns are raised.",
            "Leadership messages about inclusion are not always matched by visible action.",
            "Different perspectives are not consistently reflected in decisions.",
        ],
        "positive": [
            "Leaders make inclusion visible in decisions and everyday behaviour.",
            "Leadership listens seriously when employees raise inclusion concerns.",
        ],
    },
}

# The labels are retained in the generated truth file as transparent metadata
# for any future qualitative-text evaluation.
THEME_LABELS = {
    "belonging": "Belonging",
    "voice": "Employee Voice",
    "psychological_safety": "Psychological Safety",
    "fairness": "Fairness & Opportunity",
    "inclusive_leadership": "Inclusive Leadership",
}

OPENERS_NEGATIVE = ["", "", "", "Honestly, ", "To be direct: ", "The main issue is that "]
OPENERS_POSITIVE = ["", "", "Genuinely, ", "One thing that works: "]
# How a complaint ends depends on how the person feels about the company as a
# whole: the disengaged sign off with an exit threat, the engaged with a
# caveat. This is what gives free text information the scores do not already
# carry - and what makes validating a sentiment model against eNPS meaningful.
CLOSERS_ANGRY = [" It is the main reason people are looking elsewhere.",
                 " I am already looking at other options.",
                 " Nothing has changed since the last survey.",
                 " Frankly it is exhausting."]
CLOSERS_NEUTRAL = ["", "", " This needs fixing this year.", " It should not be this hard."]
CLOSERS_SOFT = ["", " Otherwise this is a good place to work.",
                " It is the one thing I would change.",
                " The rest of my experience here is positive."]
CLOSERS_POSITIVE = ["", "", " Please keep it.", " That should be the standard everywhere."]


def make_comments(responses: list[dict]) -> list[dict]:
    comments = []
    comment_no = 0

    for row in responses:
        if not row["responded"]:
            continue
        if rng.random() > comment_probability(row):
            continue

        latent = row["_latent"]
        weakest = sorted(latent, key=lambda d: latent[d])[:3]
        strongest = sorted(latent, key=lambda d: -latent[d])[:2]

        for question in ("what_to_change", "what_works"):
            negative = question == "what_to_change"
            # People comment about their own low scores, which is what makes
            # text and numbers agree - and what the analysis then shows.
            pool = [name for name, theme in THEMES.items()
                    if theme["dimension"] in (weakest if negative else strongest)]
            if not pool:
                pool = list(THEMES)
            # Whether someone answers the critical question, the positive one,
            # or both is itself driven by how they feel: detractors write far
            # more "what to change" than promoters. The comment mix carries
            # signal before a single word is read.
            inclusion_signal = row["_inclusion_outcome"]
            if negative:
                p_write = clamp(0.80 - 0.22 * inclusion_signal, 0.35, 0.97)
            else:
                p_write = clamp(0.45 + 0.28 * inclusion_signal, 0.08, 0.90)
            if rng.random() > p_write:
                continue

            theme_name = rng.choice(pool)
            theme = THEMES[theme_name]
            bank = theme["negative"] if negative else theme["positive"]
            if not bank:
                continue
            themes_used = [theme_name]

            text = rng.choice(bank)
            opener = rng.choice(OPENERS_NEGATIVE if negative else OPENERS_POSITIVE)
            if opener:
                text = opener + text[0].lower() + text[1:]
            if negative:
                inclusion_signal = row["_inclusion_outcome"]
                if inclusion_signal < -0.35:
                    pool = CLOSERS_ANGRY if rng.random() < 0.8 else CLOSERS_NEUTRAL
                elif inclusion_signal > 0.35:
                    pool = CLOSERS_SOFT if rng.random() < 0.8 else CLOSERS_NEUTRAL
                else:
                    pool = CLOSERS_NEUTRAL
                text += rng.choice(pool)
            else:
                text += rng.choice(CLOSERS_POSITIVE)

            # A second sentence from another theme, sometimes - real verbatims
            # are rarely single-topic.
            if rng.random() < 0.22:
                other = rng.choice([n for n in THEMES if n != theme_name])
                bank2 = THEMES[other]["negative"] if negative else THEMES[other]["positive"]
                if bank2:
                    text += " " + rng.choice(bank2)
                    themes_used.append(other)

            comment_no += 1
            comments.append({
                "comment_id": f"C{comment_no:05d}",
                "response_id": row["response_id"],
                "question": question,
                "comment_text": text.strip(),
                "_true_themes": themes_used,
                "_true_tone": "positive" if not negative else "negative",
            })

    return comments


def comment_probability(row: dict) -> float:
    """Unhappy people and long-tenure people write more; new joiners write less."""
    p = 0.42 - 0.12 * row["_inclusion_outcome"]
    if row["tenure_band"] in ("6-10 years", "10 years +"):
        p += 0.06
    if row["tenure_band"] == "< 1 year":
        p -= 0.08
    return clamp(p, 0.12, 0.8)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict], drop: tuple[str, ...] = ()) -> None:
    fields = [f for f in rows[0] if not f.startswith("_") and f not in drop]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_instrument(path: Path) -> None:
    """The questionnaire itself, so the dataset is readable without the code."""
    rows = [{"item_id": item_id, "dimension": dim, "wording": text, "type": "driver"}
            for item_id, (dim, text, _bias) in ITEMS.items()]
    rows += [{"item_id": item_id, "dimension": "Inclusion (outcome)",
              "wording": text, "type": "outcome"}
             for item_id, text in OUTCOME_ITEMS.items()]
    rows.append({"item_id": "enps", "dimension": "Inclusion (outcome)",
                 "wording": "How likely are you to recommend this company as a place to "
                            "work? (0-10)", "type": "outcome"})
    write_csv(path, rows)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    teams = make_teams()
    responses = make_responses(teams)
    comments = make_comments(responses)

    write_csv(DATA / "teams.csv", teams)
    write_csv(DATA / "survey_responses.csv", responses)
    write_csv(DATA / "survey_comments.csv", comments)
    write_instrument(DATA / "survey_instrument.csv")

    # Transparent labels for the synthetic themes used to build each comment.
    write_csv(DATA / "comment_themes_truth.csv",
              [{"comment_id": c["comment_id"],
                "true_themes": "; ".join(THEME_LABELS[t] for t in c["_true_themes"]),
                "true_tone": c["_true_tone"]} for c in comments])

    answered = sum(r["responded"] for r in responses)
    print(f"teams.csv              : {len(teams):>6,} teams")
    print(f"survey_responses.csv   : {len(responses):>6,} invited, {answered:,} responded "
          f"({answered / len(responses):.1%})")
    print(f"survey_comments.csv    : {len(comments):>6,} verbatims")
    print(f"survey_instrument.csv  : {len(ITEMS) + len(OUTCOME_ITEMS) + 1:>6,} questions")


if __name__ == "__main__":
    main()
