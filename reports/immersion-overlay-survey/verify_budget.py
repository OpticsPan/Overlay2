"""Recalculate a proposed overlay budget; standard library only.

Run: python reports/immersion-overlay-survey/verify_budget.py
No scanner data are simulated. Checks establish arithmetic, not device capability.
"""
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40
HERE = Path(__file__).resolve().parent
D = lambda x: Decimal(str(x))


def ss(values):
    return sum((D(v) ** 2 for v in values), Decimal(0))


def calculate(data):
    out = {"unit": "nm", "metric": "Q = B + 3sigma, under stated allocation assumptions", "scenarios": {}}
    for key, s in data["scenarios"].items():
        v_d = ss(s["dco_3sigma"].values())
        v_m = v_d + ss(s["matching_increment_3sigma"].values())
        b_d, b_m = D(s["dco_total_mean_bound"]), D(s["mmo_total_mean_bound"])
        q_d, q_m = b_d + v_d.sqrt(), b_m + v_m.sqrt()
        v_st = ss(s["stage_children_3sigma"].values())
        assert v_st.sqrt() <= D(s["dco_3sigma"]["stage"])
        assert q_d <= D(s["dco_numeric_anchor"])
        assert q_m <= D(s["mmo_numeric_anchor"])
        # One positive-correlation sensitivity case, not a measured rho.
        cross = 2 * D("0.3") * D(s["dco_3sigma"]["stage"]) * D(s["dco_3sigma"]["alignment"])
        row = {
            "dco_variance_3sigma_squared": float(v_d),
            "dco_R": float(v_d.sqrt()), "dco_B": float(b_d), "dco_Q": float(q_d),
            "dco_arithmetic_headroom": float(D(s["dco_numeric_anchor"]) - q_d),
            "mmo_variance_3sigma_squared": float(v_m),
            "mmo_R": float(v_m.sqrt()), "mmo_B": float(b_m), "mmo_Q": float(q_m),
            "mmo_arithmetic_headroom": float(D(s["mmo_numeric_anchor"]) - q_m),
            "stage_children_R": float(v_st.sqrt()),
            "dco_variance_shares_percent": {k: float(D(v) ** 2 / v_d * 100) for k, v in s["dco_3sigma"].items()},
            "sensitivity_stage_alignment_rho_0_3": {
                "dco_Q": float(b_d + (v_d + cross).sqrt()),
                "mmo_Q": float(b_m + (v_m + cross).sqrt()),
                "dco_anchor_exceeded": b_d + (v_d + cross).sqrt() > D(s["dco_numeric_anchor"])
            }
        }
        assert abs(sum(row["dco_variance_shares_percent"].values()) - 100) < 1e-10
        out["scenarios"][key] = row
    # A constructed geometric case tests the distinction between center shift and edges.
    dx, dcd = D(2), D(4)
    out["edge_example"] = {"center_shift": float(dx), "CD_change": float(dcd),
                           "left_edge_shift_positive_x": float(dx - dcd / 2),
                           "right_edge_shift_positive_x": float(dx + dcd / 2)}
    assert out["edge_example"]["left_edge_shift_positive_x"] == 0
    assert out["edge_example"]["right_edge_shift_positive_x"] == 4
    # Analytical error propagation, compared to the original missing-factor form.
    sig_ovl, sig_cd, sig_local = D(1), D(2), D("0.5")
    out["epe_sigma_example"] = {
        "inputs_1sigma": [float(sig_ovl), float(sig_cd), float(sig_local)],
        "EPE_1sigma": float((sig_ovl**2 + sig_cd**2 / 4 + sig_local**2).sqrt()),
        "EPE_3sigma": float(3 * (sig_ovl**2 + sig_cd**2 / 4 + sig_local**2).sqrt())
    }
    assert out["epe_sigma_example"]["EPE_3sigma"] == 4.5
    out["limits"] = "Arithmetic consistency only; correlations, distributions, spatial sampling and device performance require data."
    return out


if __name__ == "__main__":
    data = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))
    result = calculate(data)
    (HERE / "calculations.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    for key, row in result["scenarios"].items():
        print(f"{key}: DCO Q={row['dco_Q']:.6f}, MMO Q={row['mmo_Q']:.6f}, stage children={row['stage_children_R']:.6f} nm")
    print("All arithmetic and bookkeeping checks passed; no equipment performance certification.")
