"""Recalculate published numbers and explicitly hypothetical examples; no device simulation."""
import argparse
import json
import math
from pathlib import Path


def calculate():
    rows = [
        ('process_overlay', 80, [15, 60, 5], 'linear_candidate', sum([15, 60, 5])),
        ('matched_machine', 60, [25, 30, 5], 'linear_candidate', sum([25, 30, 5])),
        ('single_machine', 30, [6, 12, 5, 5], 'linear_candidate', sum([6, 12, 5, 5])),
        ('global_alignment', 6, [4, 4, 2], 'rss_explicit_in_paper', math.hypot(4, 4, 2)),
        ('stage_overlay', 12, [7, 5], 'linear_explicit_in_paper', 7 + 5),
        ('position_measurement', 4, [3, 1, 2.5], 'rss_hypothesis', math.hypot(3, 1, 2.5)),
        ('alignment_repeatability', 5, [3, 3], 'rss_hypothesis', math.hypot(3, 3)),
        ('tracking_xy', 2.5, [2, 1], 'same_plane_uncorrelated_rss_hypothesis', math.hypot(2, 1)),
    ]
    data = {
        'purpose': 'Arithmetic and sensitivity audit of Figure 3; not reconstruction or validation of the confidential ASML model',
        'length_unit': 'nm',
        'rows': [{'id': key, 'parent_nm': parent, 'children_nm': children, 'rule_status': rule,
                  'calculated_nm': result, 'parent_minus_calculated_nm': parent-result}
                 for key, parent, children, rule, result in rows],
        'global_alignment_correlation_example': {
            'assumptions': '4,4,2 nm interpreted as standard deviations; positive unit sensitivities; only the two 4 nm inputs correlated',
            'cases': [{'rho': rho, 'sigma_nm': math.sqrt(36+32*rho)} for rho in [0, .25, .5]],
        },
        'rotation_example': {
            'assumptions': 'Hypothetical effective lever arms, not machine geometry; small-angle displacement magnitude r*theta',
            'theta_nrad': 75,
            'cases': [{'lever_arm_mm': r, 'displacement_nm': r*75*1e-3} for r in [10, 20, 100]],
            'counterexample_to_inferring_geometry_from_closure': {
                'linear_r_mm': (7-1-2.5-2.5)/75*1000,
                'rss_r_mm': math.sqrt(7**2-1**2-2.5**2-2.5**2)/75*1000,
                'warning': 'Two different assumed rules fit 7 nm with different lever arms; neither establishes the physical geometry',
            },
        },
        'rounding': {'display_decimal_places': 3, 'numeric_comparison_absolute_tolerance_nm': 1e-12,
                     'note': 'Tolerance is computational only, not an engineering acceptance tolerance; 4.031 nm is not <=4.000 nm'},
        'not_proven': ['2 nm is a design reserve', 'all input values are standard deviations', 'all shared inputs are uncorrelated',
                       'the public values are unmodified commercial specifications', 'a device meets the allocated budget'],
    }
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('calculations.json'))
    args = parser.parse_args()
    text = json.dumps(calculate(), ensure_ascii=False, indent=2) + '\n'
    args.output.write_text(text, encoding='utf-8', newline='\n')
    print(text)
