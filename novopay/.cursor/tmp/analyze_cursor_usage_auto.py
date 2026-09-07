import csv
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path

path = Path(r"C:\Users\ashutosh.kumar\Downloads\usage-events-2026-08-31.csv")


def to_int(x):
    if x is None:
        return 0
    s = str(x).strip()
    if not s:
        return 0
    try:
        return int(float(s.replace(",", "")))
    except ValueError:
        return 0


def cost_at(rates, cw, inp, cr, out):
    pin, pcw, pcr, pout = rates
    c = (inp / 1e6) * pin
    c += (cw / 1e6) * (pcw if pcw is not None else pin)
    c += (cr / 1e6) * pcr
    c += (out / 1e6) * pout
    return c


SCENARIOS = {
    "composer25": (0.5, None, 0.2, 2.5),
    "composer25fast": (3, None, 0.5, 15),
    "grok46": (2, None, 0.5, 6),
    "grok46fast": (4, None, 1, 12),
}

KIMI = (3, None, 0.3, 15)
GLM = (1.4, None, 0.26, 4.4)
OPUS48 = (5, 6.25, 0.5, 25)

rows = []
with path.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

auto_month = defaultdict(lambda: {"n": 0, "cw": 0, "inp": 0, "cr": 0, "out": 0, "tok": 0})
auto_day = defaultdict(lambda: {"n": 0, "cw": 0, "inp": 0, "cr": 0, "out": 0, "tok": 0})
other_missed = defaultdict(lambda: {"n": 0, "cw": 0, "inp": 0, "cr": 0, "out": 0})
priced_day = defaultdict(float)
aug_model = Counter()
aug_model_cost = defaultdict(float)

RATES_NAMED = {
    "cursor-grok-4.6-high": (2, None, 0.5, 6),
    "cursor-grok-4.6-high-fast": (4, None, 1, 12),
    "cursor-grok-4.6-medium-fast": (4, None, 1, 12),
    "cursor-grok-4.5-high": (2, None, 0.5, 6),
    "cursor-grok-4.5-high-fast": (4, None, 1, 18),
    "cursor-grok-4.5-medium": (2, None, 0.5, 6),
    "composer-2.5-fast": (3, None, 0.5, 15),
    "composer-2-fast": (3, None, 0.5, 15),
    "composer-2": (0.5, None, 0.2, 2.5),
    "claude-opus-5-thinking-high": (5, 6.25, 0.5, 25),
    "gpt-5.6-terra-medium": (2, 2.5, 0.2, 12),
    "kimi-k3-max": KIMI,
    "glm-5.2-high": GLM,
    "claude-opus-4-8-thinking-high": OPUS48,
}

for r in rows:
    dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
    model = r.get("Model", "")
    cw = to_int(r.get("Input (w/ Cache Write)"))
    inp = to_int(r.get("Input (w/o Cache Write)"))
    cr = to_int(r.get("Cache Read"))
    out = to_int(r.get("Output Tokens"))
    tok = to_int(r.get("Total Tokens")) or (cw + inp + cr + out)
    month = dt.strftime("%Y-%m")
    day = dt.date().isoformat()
    if model == "auto":
        m = auto_month[month]
        m["n"] += 1
        m["cw"] += cw
        m["inp"] += inp
        m["cr"] += cr
        m["out"] += out
        m["tok"] += tok
        d = auto_day[day]
        d["n"] += 1
        d["cw"] += cw
        d["inp"] += inp
        d["cr"] += cr
        d["out"] += out
        d["tok"] += tok
    elif model in ("kimi-k3-max", "glm-5.2-high", "claude-opus-4-8-thinking-high"):
        mm = other_missed[model]
        mm["n"] += 1
        mm["cw"] += cw
        mm["inp"] += inp
        mm["cr"] += cr
        mm["out"] += out
    rates = RATES_NAMED.get(model)
    if rates:
        priced_day[day] += cost_at(rates, cw, inp, cr, out)
    if dt.year == 2026 and dt.month == 8:
        aug_model[model] += 1
        if rates:
            aug_model_cost[model] += cost_at(rates, cw, inp, cr, out)

print("=== AUTO BY MONTH ===")
for month in sorted(auto_month):
    m = auto_month[month]
    print(f"{month} n={m['n']} tok={m['tok']:,} inp={m['inp']:,} cw={m['cw']:,} cr={m['cr']:,} out={m['out']:,}")
    for name, rates in SCENARIOS.items():
        print(f"  {name}: ${cost_at(rates, m['cw'], m['inp'], m['cr'], m['out']):.2f}")

print("\n=== PREVIOUSLY UNPRICED OTHER ===")
for model, m in other_missed.items():
    rates = RATES_NAMED[model]
    print(
        f"{model} n={m['n']} est=${cost_at(rates, m['cw'], m['inp'], m['cr'], m['out']):.2f} "
        f"inp={m['inp']:,} cw={m['cw']:,} cr={m['cr']:,} out={m['out']:,}"
    )

print("\n=== AUG MODEL COST (priced + newly priced) ===")
for model, n in aug_model.most_common():
    print(f"  {model}: n={n} est=${aug_model_cost.get(model, 0):.2f}")

# Combined monthly: priced named + auto scenarios
print("\n=== MONTHLY TOTALS priced_named + auto scenarios ===")
named_month = defaultdict(float)
auto_only_month = {}
for r in rows:
    dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
    model = r.get("Model", "")
    if model == "auto":
        continue
    rates = RATES_NAMED.get(model)
    if not rates:
        continue
    cw = to_int(r.get("Input (w/ Cache Write)"))
    inp = to_int(r.get("Input (w/o Cache Write)"))
    cr = to_int(r.get("Cache Read"))
    out = to_int(r.get("Output Tokens"))
    named_month[dt.strftime("%Y-%m")] += cost_at(rates, cw, inp, cr, out)

for month in sorted(set(list(named_month) + list(auto_month))):
    named = named_month.get(month, 0)
    am = auto_month.get(month, {"cw": 0, "inp": 0, "cr": 0, "out": 0})
    print(f"{month} named=${named:.2f}")
    for name, rates in SCENARIOS.items():
        auto_c = cost_at(rates, am["cw"], am["inp"], am["cr"], am["out"])
        print(f"  +auto {name}: ${named + auto_c:.2f} (auto ${auto_c:.2f})")

# last 7 / 14 / 30 combined
end = datetime.fromisoformat(rows[0]["Date"].replace("Z", "+00:00"))
for r in rows:
    dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
    if dt > end:
        end = dt

print("\n=== WINDOWS priced + auto ===")
for label, days in [("L7", 7), ("L14", 14), ("L30", 30), ("AUG", None)]:
    named = 0.0
    auto = {"cw": 0, "inp": 0, "cr": 0, "out": 0, "n": 0}
    start = end - timedelta(days=days) if days else None
    for r in rows:
        dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
        if days and dt < start:
            continue
        if label == "AUG" and not (dt.year == 2026 and dt.month == 8):
            continue
        model = r.get("Model", "")
        cw = to_int(r.get("Input (w/ Cache Write)"))
        inp = to_int(r.get("Input (w/o Cache Write)"))
        cr = to_int(r.get("Cache Read"))
        out = to_int(r.get("Output Tokens"))
        if model == "auto":
            auto["n"] += 1
            auto["cw"] += cw
            auto["inp"] += inp
            auto["cr"] += cr
            auto["out"] += out
        else:
            rates = RATES_NAMED.get(model)
            if rates:
                named += cost_at(rates, cw, inp, cr, out)
    print(f"{label} named=${named:.2f} auto_n={auto['n']}")
    for name, rates in SCENARIOS.items():
        ac = cost_at(rates, auto["cw"], auto["inp"], auto["cr"], auto["out"])
        print(f"  {name}: total=${named + ac:.2f} auto=${ac:.2f}")

print("\n=== AUG DAILY priced + auto composer25 / grok46 ===")
aug_days = sorted({d for d in priced_day if d.startswith("2026-08")})
for day in aug_days:
    a = auto_day.get(day, {"cw": 0, "inp": 0, "cr": 0, "out": 0, "n": 0})
    ac = cost_at(SCENARIOS["composer25"], a["cw"], a["inp"], a["cr"], a["out"])
    ag = cost_at(SCENARIOS["grok46"], a["cw"], a["inp"], a["cr"], a["out"])
    print(
        f"{day} priced=${priced_day.get(day, 0):7.2f} auto_n={a['n']:3d} "
        f"auto_comp=${ac:7.2f} auto_grok=${ag:7.2f} "
        f"tot_comp=${priced_day.get(day, 0) + ac:7.2f} tot_grok=${priced_day.get(day, 0) + ag:7.2f}"
    )
