from typing import Dict, List, Tuple
from math import isfinite

def hm_to_min(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m

def overlap_minutes(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    s = max(a[0], b[0])
    e = min(a[1], b[1])
    return max(0, e - s)

def availability_score(tutor_avail: List[Dict], student_windows: List[Dict]) -> float:
    """Fraction (0..1) of requested time that overlaps with tutor availability."""
    if not tutor_avail or not student_windows:
        return 0.0

    need = 0
    got = 0
    for sw in student_windows:
        sw_len = hm_to_min(sw["end"]) - hm_to_min(sw["start"])
        need += max(0, sw_len)
        for tw in tutor_avail:
            if tw["dow"] == sw["dow"]:
                got += overlap_minutes(
                    (hm_to_min(sw["start"]), hm_to_min(sw["end"])),
                    (hm_to_min(tw["start"]), hm_to_min(tw["end"]))
                )
    return (got / need) if need > 0 else 0.0

def price_fit(rate: float, mn: int, mx: int) -> float:
    """1.0 inside budget, decays gently outside (within 30% buffer)."""
    if mn is None or mx is None:
        return 0.5
    if mn <= rate <= mx:
        return 1.0

    buffer_amt = max(int(0.3 * mx), 1)  # allow small stretch
    if rate < mn:
        return max(0.0, 1.0 - (mn - rate) / buffer_amt)
    else:
        return max(0.0, 1.0 - (rate - mx) / buffer_amt)

def bayesian_rating(avg: float, n: int, mu: float = 4.2, alpha: int = 8) -> float:
    """Smoothed rating (prevents low-review tutors from looking artificially perfect)."""
    return (mu * alpha + avg * n) / (alpha + n) if (alpha + n) > 0 else mu

def course_match_score(tutor_courses: List[str], student_courses: List[Dict]) -> float:
    """
    Student courses include priority.
    Priority 1 match -> 1.0, 2 -> 0.8, 3 -> 0.6, others -> 0.5, none -> 0.0
    """
    if not student_courses:
        return 0.0

    # map: course -> priority
    pref_map = {c["name"]: c.get("priority", 10) for c in student_courses}

    best = 0.0
    best_course = None
    for course, pr in pref_map.items():
        if course in tutor_courses:
            if pr == 1:
                score = 1.0
            elif pr == 2:
                score = 0.8
            elif pr == 3:
                score = 0.6
            else:
                score = 0.5
            if score > best:
                best = score
                best_course = course

    return best

def recommend(student_prefs: Dict, tutors: List[Dict]) -> List[Dict]:
    """
    Returns ranked list with score + reasons.
    Content-based: level, courses, budget, time, language, ratings.
    """
    level = student_prefs["level"]
    language = student_prefs["language"]
    mn = student_prefs["min_budget"]
    mx = student_prefs["max_budget"]
    student_courses = student_prefs["courses"]
    time_windows = student_prefs["preferred_time"]

    # weights (simple & adjustable later)
    W = {
        "availability": 0.30,
        "price": 0.20,
        "rating": 0.20,
        "course": 0.25,
        "language": 0.05
    }

    results = []

    for t in tutors:
        # Hard filters
        if not t.get("verified", False):
            continue
        if level not in t.get("levels", []):
            continue
        if language not in t.get("languages", []):
            continue

        A = availability_score(t.get("availability", []), time_windows)
        if A <= 0:
            continue

        CM = course_match_score(t.get("courses", []), student_courses)
        if CM <= 0:
            continue

        P = price_fit(t.get("hourly_rate", 0), mn, mx)
        R = bayesian_rating(t.get("rating_avg", 0), t.get("rating_count", 0)) / 5.0
        L = 1.0  # already filtered by language match

        score = (
            W["availability"] * A +
            W["price"] * P +
            W["rating"] * R +
            W["course"] * CM +
            W["language"] * L
        )

        # Reasons: pick top contributions
        contribs = [
            (W["course"] * CM, "teaches one of your selected courses"),
            (W["availability"] * A, "matches your preferred time"),
            (W["price"] * P, f"fits your budget (NPR {mn}–{mx})"),
            (W["rating"] * R, f"strong rating ({t['rating_avg']}★ from {t['rating_count']} reviews)"),
            (W["language"] * L, f"teaches in {language}")
        ]
        contribs.sort(key=lambda x: x[0], reverse=True)
        reasons = [text for val, text in contribs if val > 0][:3]

        results.append({
            "tutor_id": t["tutor_id"],
            "name": t["name"],
            "hourly_rate": t["hourly_rate"],
            "score": round(score, 4),
            "reasons": reasons,
            "tutor": t
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
