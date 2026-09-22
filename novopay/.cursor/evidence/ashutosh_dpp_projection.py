#!/usr/bin/env python3
"""One-off: Ashutosh career days/PR trajectory + days-to-0.2 projection."""
from __future__ import annotations

import math
from datetime import datetime


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def hits_target(span: float, n: int) -> bool:
    if n <= 1:
        return False
    ex = span / (n - 1)
    return round(ex, 1) == 0.2 or ex <= 0.25


def main() -> None:
    # Live GitHub (2026-09-09 query)
    first = parse("2026-02-23T07:13:17Z")
    last = parse("2026-09-08T09:10:52Z")  # mergedAt of most recently updated
    total = 622
    span_days = (last - first).days
    exact = span_days / max(total - 1, 1)
    rounded = round(exact, 1)

    print("=== CURRENT (live) ===")
    print(f"first={first.isoformat()}")
    print(f"last_event={last.isoformat()}")
    print(f"total={total}")
    print(f"span_days={span_days}")
    print(f"span_mo={round(max(span_days / 30.44, 0.01), 1)}")
    print(f"days_per_pr_exact={exact:.6f}")
    print(f"days_per_pr_rounded={rounded}")
    print(f"exact<=0.25? {exact <= 0.25}; rounded==0.2? {rounded == 0.2}")

    snaps = [
        ("2026-07-09", 390, 4.4),
        ("2026-08-04", 471, 5.2),
        ("2026-08-18", 551, 5.8),
        ("2026-08-27", 583, 6.1),
        ("2026-09-01", 593, 6.2),
        ("2026-09-09", 622, 6.5),
    ]
    print("\n=== SNAPSHOT TRAJECTORY ===")
    prev_exact = None
    trend_dirs: list[str] = []
    for as_of, n, span_mo in snaps:
        sd = span_mo * 30.44
        ex = sd / (n - 1)
        rnd = round(ex, 1)
        if prev_exact is None:
            print(
                f"{as_of}: total={n} span_mo={span_mo} "
                f"span_days~={sd:.2f} exact={ex:.6f} rounded={rnd}"
            )
        else:
            delta = ex - prev_exact
            if abs(delta) < 1e-9:
                d = "flat"
            elif delta < 0:
                d = "decreasing"
            else:
                d = "increasing"
            trend_dirs.append(d)
            print(
                f"{as_of}: total={n} span_mo={span_mo} "
                f"span_days~={sd:.2f} exact={ex:.6f} rounded={rnd} "
                f"delta={delta:+.6f} ({d})"
            )
        prev_exact = ex

    live_span_mo = round(max(span_days / 30.44, 0.01), 1)
    snap_exact_sep9 = (6.5 * 30.44) / (622 - 1)
    print(f"\nLive span_days={span_days} => span_mo rounded={live_span_mo}")
    print(f"Live exact={exact:.6f}; snapshot 6.5 formula exact={snap_exact_sep9:.6f}")

    print("\n=== RECENT PACE ===")
    d_aug = (datetime(2026, 9, 9) - datetime(2026, 8, 27)).days
    prs_aug = 622 - 583
    pace_aug = prs_aug / d_aug
    d_sep = (datetime(2026, 9, 9) - datetime(2026, 9, 1)).days
    prs_sep = 622 - 593
    pace_sep = prs_sep / d_sep
    print(f"Aug27->Sep9: dPR={prs_aug} days={d_aug} PRs/day={pace_aug:.4f}")
    print(f"Sep1->Sep9:  dPR={prs_sep} days={d_sep} PRs/day={pace_sep:.4f}")

    # Prefer closest-to-14d window for Model A (Aug27->Sep9 = 13d)
    paces = {
        "Aug27->Sep9 (~14d)": pace_aug,
        "Sep1->Sep9 (8d)": pace_sep,
    }

    n0 = total
    span0 = float(span_days)

    print("\n=== MODEL A: constant PR/day, span +=1/day ===")
    print("Rule: each day n = n0 + floor(pace*days), span = span0 + days")
    print("Stop when round(span/(n-1),1)==0.2 OR exact<=0.25")
    print(f"Feasibility: need pace > 4.0 PR/day (else span grows faster than 0.25*dn)")
    for label, pace in paces.items():
        hit = False
        for days in range(0, 200_000):
            n = n0 + int(pace * days)
            span = span0 + days
            ex = span / max(n - 1, 1)
            if hits_target(span, n):
                print(
                    f"pace={label} ({pace:.4f}/d): days={days}, n={n}, "
                    f"PRs_needed={n - n0}, exact={ex:.6f}, rounded={round(ex, 1)}"
                )
                hit = True
                break
        if not hit:
            asym = 1.0 / pace if pace else float("inf")
            print(
                f"pace={label} ({pace:.4f}/d): NEVER within 200k days "
                f"(asymptotic dpp~={asym:.4f} > 0.25)"
            )

    # Continuous analytic
    print("\n--- Model A continuous (exact<=0.25): f(d)=a+b*d ---")
    for label, pace in paces.items():
        a = 0.25 * (n0 - 1) - span0
        b = 0.25 * pace - 1
        print(f"{label}: a={a:.4f} b={b:.6f}")
        if b > 0:
            d_need = 0.0 if a >= 0 else -a / b
            print(f"  hits exact<=0.25 after {d_need:.2f} days")
        elif a >= 0:
            print("  already at target")
        else:
            print(f"  NEVER (pace {pace:.4f} < 4 PR/day)")

    print("\n=== MODEL B: span frozen (optimistic lower bound) ===")
    min_intervals = math.ceil(span0 / 0.25 - 1e-12)
    n_needed = min_intervals + 1
    prs_b = max(0, n_needed - n0)
    print(f"span_frozen={span0}")
    print(f"need n-1 >= {span0}/0.25 = {span0 / 0.25:.4f} => n >= {n_needed}")
    print(f"PRs_needed={prs_b}")
    print(
        f"verify exact={span0 / (n_needed - 1):.6f} "
        f"rounded={round(span0 / (n_needed - 1), 1)}"
    )
    for n in range(n0, n0 + 5000):
        if hits_target(span0, n):
            print(
                f"first frozen hit: n={n}, PRs={n - n0}, "
                f"exact={span0 / (n - 1):.6f}, rounded={round(span0 / (n - 1), 1)}"
            )
            break

    print("\n=== TREND VERDICT ===")
    e0 = (snaps[0][2] * 30.44) / (snaps[0][1] - 1)
    e1 = (snaps[-1][2] * 30.44) / (snaps[-1][1] - 1)
    overall = "decreasing" if e1 < e0 else ("increasing" if e1 > e0 else "flat")
    print(f"stepwise: {trend_dirs}")
    print(f"overall {snaps[0][0]}->{snaps[-1][0]}: {overall} ({e0:.6f} -> {e1:.6f}, d={e1 - e0:+.6f})")

    # Recent segment Aug27->Sep9
    e_aug = (6.1 * 30.44) / (583 - 1)
    e_now = (6.5 * 30.44) / (622 - 1)
    print(f"Aug27->Sep9 snapshot exact: {e_aug:.6f} -> {e_now:.6f} (d={e_now - e_aug:+.6f})")

    print("\n=== WHAT-IF paces (Model A) ===")
    for pace in [4.0, 4.01, 4.1, 4.5, 5.0]:
        hit = False
        for days in range(0, 500_000):
            n = n0 + int(pace * days)
            span = span0 + days
            if hits_target(span, n):
                print(
                    f"pace={pace:.2f}: days={days}, PRs={n - n0}, "
                    f"exact={span / max(n - 1, 1):.6f}"
                )
                hit = True
                break
        if not hit:
            print(f"pace={pace:.2f}: no hit in 500k days; asym~={1 / pace:.4f}")

    print("\n=== round() boundary checks ===")
    for x in [0.14, 0.15, 0.249, 0.25, 0.251]:
        print(f"round({x}, 1) = {round(x, 1)}")


if __name__ == "__main__":
    main()
