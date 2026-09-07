import csv
from collections import defaultdict, Counter
from datetime import datetime, timezone, timedelta
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


def to_float(x):
    if x is None:
        return None
    s = str(x).strip()
    if not s:
        return None
    try:
        return float(s.replace(",", "").replace("$", ""))
    except ValueError:
        return None


RATES = {
    "cursor-grok-4.6": (2, None, 0.5, 6),
    "cursor-grok-4.6-high": (2, None, 0.5, 6),
    "cursor-grok-4.6-fast": (4, None, 1, 12),
    "cursor-grok-4.6-high-fast": (4, None, 1, 12),
    "cursor-grok-4.5": (2, None, 0.5, 6),
    "cursor-grok-4.5-fast": (4, None, 1, 18),
    "cursor-grok-4.5-high-fast": (4, None, 1, 18),
    "composer-2.5": (0.5, None, 0.2, 2.5),
    "composer-2.5-fast": (3, None, 0.5, 15),
    "composer": (0.5, None, 0.2, 2.5),
    "claude-4-sonnet": (3, 3.75, 0.3, 15),
    "claude-4.5-sonnet": (3, 3.75, 0.3, 15),
    "claude-4.6-sonnet": (3, 3.75, 0.3, 15),
    "claude-4.5-opus": (5, 6.25, 0.5, 25),
    "claude-4.6-opus": (5, 6.25, 0.5, 25),
    "claude-4.7-opus": (5, 6.25, 0.5, 25),
    "claude-opus-4.8": (5, 6.25, 0.5, 25),
    "claude-opus-5": (5, 6.25, 0.5, 25),
    "claude-sonnet-5": (2, 2.5, 0.2, 10),
    "gpt-5": (1.25, None, 0.125, 10),
    "gpt-5-fast": (2.5, None, 0.25, 20),
    "gpt-5.2": (1.75, None, 0.175, 14),
    "gpt-5.4": (2.5, None, 0.25, 15),
    "gpt-5.5": (5, None, 0.5, 30),
    "gemini-3-flash": (0.5, None, 0.05, 3),
    "gemini-3-pro": (2, None, 0.2, 12),
}


def normalize(model):
    return (model or "").strip().lower()


def is_cursor_model(model):
    m = normalize(model)
    return m.startswith("cursor-grok") or m.startswith("composer") or m.startswith("grok")


def lookup_rate(model):
    m = normalize(model)
    if m in RATES:
        return RATES[m]
    for k, v in RATES.items():
        if k in m or m in k:
            return v
    if "grok-4.6" in m and "fast" in m:
        return RATES["cursor-grok-4.6-high-fast"]
    if "grok-4.6" in m:
        return RATES["cursor-grok-4.6"]
    if "grok-4.5" in m and "fast" in m:
        return RATES["cursor-grok-4.5-fast"]
    if "composer" in m and "fast" in m:
        return RATES["composer-2.5-fast"]
    if "composer" in m:
        return RATES["composer-2.5"]
    return None


def estimate_cost(model, cache_write, input_no_cw, cache_read, output):
    rates = lookup_rate(model)
    if rates is None:
        return None
    inp, cw, cr, out = rates
    cost = 0.0
    cost += (input_no_cw / 1_000_000.0) * inp
    if cw is None:
        cost += (cache_write / 1_000_000.0) * inp
    else:
        cost += (cache_write / 1_000_000.0) * cw
    cost += (cache_read / 1_000_000.0) * cr
    cost += (output / 1_000_000.0) * out
    return cost


rows = []
with path.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    print("COLUMNS", reader.fieldnames)
    for r in reader:
        rows.append(r)

print("N", len(rows))

kinds = Counter()
costs = Counter()
models = Counter()
max_mode = Counter()
numeric_costs = []
unpriced_models = Counter()

by_day = defaultdict(lambda: {"n": 0, "tokens": 0, "cost_est": 0.0, "cursor_est": 0.0, "other_est": 0.0, "unpriced": 0})
by_month = defaultdict(
    lambda: {
        "n": 0,
        "tokens": 0,
        "cost_est": 0.0,
        "cursor_est": 0.0,
        "other_est": 0.0,
        "unpriced": 0,
        "by_model": Counter(),
        "by_kind": Counter(),
        "by_costlabel": Counter(),
    }
)
by_model = defaultdict(lambda: {"n": 0, "tokens": 0, "cost_est": 0.0, "in": 0, "cw": 0, "cr": 0, "out": 0, "unpriced": 0})

cloud_n = 0
auto_n = 0
dates = []

for r in rows:
    kinds[r.get("Kind", "")] += 1
    costs[r.get("Cost", "")] += 1
    models[r.get("Model", "")] += 1
    max_mode[r.get("Max Mode", "")] += 1
    if r.get("Cloud Agent ID"):
        cloud_n += 1
    if r.get("Automation ID"):
        auto_n += 1
    dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
    dates.append(dt)
    day = dt.date().isoformat()
    month = dt.strftime("%Y-%m")
    model = r.get("Model", "")
    cw = to_int(r.get("Input (w/ Cache Write)"))
    inp = to_int(r.get("Input (w/o Cache Write)"))
    cr = to_int(r.get("Cache Read"))
    out = to_int(r.get("Output Tokens"))
    tot = to_int(r.get("Total Tokens"))
    if tot == 0:
        tot = cw + inp + cr + out
    raw_cost = r.get("Cost", "")
    if raw_cost not in ("Included", "Free", "", "Errored", "errored"):
        num = to_float(raw_cost)
        if num is not None:
            numeric_costs.append(num)
    est = estimate_cost(model, cw, inp, cr, out)
    if est is None:
        unpriced_models[model] += 1
        est = 0.0
        unp = 1
    else:
        unp = 0
    cursor = is_cursor_model(model)
    by_day[day]["n"] += 1
    by_day[day]["tokens"] += tot
    by_day[day]["cost_est"] += est
    by_day[day]["unpriced"] += unp
    if cursor:
        by_day[day]["cursor_est"] += est
    else:
        by_day[day]["other_est"] += est
    m = by_month[month]
    m["n"] += 1
    m["tokens"] += tot
    m["cost_est"] += est
    m["unpriced"] += unp
    if cursor:
        m["cursor_est"] += est
    else:
        m["other_est"] += est
    m["by_model"][model] += 1
    m["by_kind"][r.get("Kind", "")] += 1
    m["by_costlabel"][raw_cost] += 1
    bm = by_model[model]
    bm["n"] += 1
    bm["tokens"] += tot
    bm["cost_est"] += est
    bm["in"] += inp
    bm["cw"] += cw
    bm["cr"] += cr
    bm["out"] += out
    bm["unpriced"] += unp

print("DATE RANGE", min(dates), "->", max(dates), "span_days", (max(dates) - min(dates)).days + 1)
print("CLOUD", cloud_n, "AUTOMATION", auto_n)
print("KIND", dict(kinds))
print("MAX MODE", dict(max_mode))
print("COST LABELS")
for k, v in costs.most_common(30):
    print(f"  {k!r}: {v}")
print("numeric cost events", len(numeric_costs), "sum", round(sum(numeric_costs), 2) if numeric_costs else 0)
print("MODELS")
for k, v in models.most_common():
    print(f"  {k}: {v}")
print("UNPRICED MODELS")
for k, v in unpriced_models.most_common():
    print(f"  {k}: {v}")

print("=== BY MONTH ===")
for month in sorted(by_month):
    m = by_month[month]
    print(
        f"{month} n={m['n']} tokens={m['tokens']:,} est=${m['cost_est']:.2f} "
        f"cursor=${m['cursor_est']:.2f} other=${m['other_est']:.2f} unpriced={m['unpriced']}"
    )
    print("  kinds", dict(m["by_kind"]))
    print("  costlabels", dict(m["by_costlabel"]))
    print("  models", dict(m["by_model"].most_common(8)))

print("=== BY MODEL COST ===")
for model, bm in sorted(by_model.items(), key=lambda x: -x[1]["cost_est"]):
    print(
        f"{model}: n={bm['n']} tokens={bm['tokens']:,} est=${bm['cost_est']:.2f} "
        f"in={bm['in']:,} cw={bm['cw']:,} cr={bm['cr']:,} out={bm['out']:,} unpriced={bm['unpriced']}"
    )

print("=== LAST 45 DAYS ===")
for day in sorted(by_day)[-45:]:
    d = by_day[day]
    print(
        f"{day} n={d['n']:4d} est=${d['cost_est']:8.2f} cursor=${d['cursor_est']:8.2f} "
        f"other=${d['other_est']:8.2f} tokens={d['tokens']:,}"
    )

end = max(dates)
d30 = end - timedelta(days=30)
d7 = end - timedelta(days=7)
d14 = end - timedelta(days=14)


def slice_stats(pred):
    n = 0
    est = 0.0
    cur = 0.0
    oth = 0.0
    tok = 0
    days = set()
    mods = Counter()
    for r in rows:
        dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
        if not pred(dt):
            continue
        n += 1
        days.add(dt.date())
        mods[r.get("Model", "")] += 1
        cw = to_int(r.get("Input (w/ Cache Write)"))
        inp = to_int(r.get("Input (w/o Cache Write)"))
        cr = to_int(r.get("Cache Read"))
        out = to_int(r.get("Output Tokens"))
        tot = to_int(r.get("Total Tokens")) or (cw + inp + cr + out)
        tok += tot
        e = estimate_cost(r.get("Model", ""), cw, inp, cr, out) or 0.0
        est += e
        if is_cursor_model(r.get("Model", "")):
            cur += e
        else:
            oth += e
    return n, est, cur, oth, tok, len(days), mods


print("=== WINDOWS ===")
windows = [
    ("ALL", lambda dt: True),
    ("L30", lambda dt: dt >= d30),
    ("L14", lambda dt: dt >= d14),
    ("L7", lambda dt: dt >= d7),
    ("AUG2026", lambda dt: dt.year == 2026 and dt.month == 8),
    ("JUL2026", lambda dt: dt.year == 2026 and dt.month == 7),
    ("JUN2026", lambda dt: dt.year == 2026 and dt.month == 6),
]
for name, pred in windows:
    n, est, cur, oth, tok, ndays, mods = slice_stats(pred)
    print(f"{name}: n={n} days={ndays} est=${est:.2f} cursor=${cur:.2f} other=${oth:.2f} tokens={tok:,}")
    print("  models", dict(mods.most_common(6)))

wd = we = 0
wd_est = we_est = 0.0
wd_days = set()
we_days = set()
for r in rows:
    dt = datetime.fromisoformat(r["Date"].replace("Z", "+00:00"))
    if dt < d30:
        continue
    cw = to_int(r.get("Input (w/ Cache Write)"))
    inp = to_int(r.get("Input (w/o Cache Write)"))
    cr = to_int(r.get("Cache Read"))
    out = to_int(r.get("Output Tokens"))
    e = estimate_cost(r.get("Model", ""), cw, inp, cr, out) or 0.0
    if dt.weekday() >= 5:
        we += 1
        we_est += e
        we_days.add(dt.date())
    else:
        wd += 1
        wd_est += e
        wd_days.add(dt.date())
print(
    f"L30 weekday n={wd} days={len(wd_days)} est=${wd_est:.2f} "
    f"avg/day=${(wd_est / len(wd_days) if wd_days else 0):.2f}"
)
print(
    f"L30 weekend n={we} days={len(we_days)} est=${we_est:.2f} "
    f"avg/day=${(we_est / len(we_days) if we_days else 0):.2f}"
)

moneyish = [k for k in costs if k and k not in ("Included", "Free") and any(c.isdigit() for c in k)]
print("MONEYISH COST LABELS", moneyish[:40], "count", len(moneyish))
