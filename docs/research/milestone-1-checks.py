#!/usr/bin/env python3
"""Bounded deterministic checks for the first FYP research milestone.

This script audits the *implemented* ``StateDependentMechanismND`` on
quadratic log-factor sources.  It does not sample a Monte Carlo tree and it
does not claim that finite enumeration proves a stochastic representation.

Run from the repository root with the pinned project environment::

    conda run --no-capture-output -n parabolab \
      python docs/research/milestone-1-checks.py

The script imports the assessment's existing ``log_factor_check.py`` and
calls its deterministic functions directly.  It deliberately does not call
that module's ``main()``, because doing so would overwrite assessment files.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import sympy as sp

from parabolab.mechanism import DxN, Id
from parabolab.state_dependent import (
    StateDependentMechanismND,
    StateDependentPDEnD,
    StateFNu,
)


REPO = Path(__file__).resolve().parents[2]
OUT_JSON = Path(__file__).with_suffix(".json")
OUT_TEXT = Path(__file__).with_suffix(".txt")
ASSESSMENT_DIR = REPO.parent / "research" / "quant_fyp_assessment_2026-09-12"
LOG_CHECK = ASSESSMENT_DIR / "log_factor_check.py"


def multiindices(d: int, total: int) -> list[tuple[int, ...]]:
    """All length-d multi-indices of exactly ``total``, lexicographically."""
    if d == 1:
        return [(total,)]
    out: list[tuple[int, ...]] = []
    for first in range(total + 1):
        for rest in multiindices(d - 1, total - first):
            out.append((first, *rest))
    return out


def qstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def as_fraction(value: float) -> Fraction:
    """Recover exact mechanism scalars (integers and halves in this audit)."""
    ans = Fraction(float(value)).limit_denominator(10**9)
    if abs(float(ans) - float(value)) > 1e-13:
        raise AssertionError((value, ans))
    return ans


def derivative_order(code: Any) -> int:
    if isinstance(code, Id):
        return 0
    if isinstance(code, DxN):
        return sum(code.mu)
    if isinstance(code, StateFNu):
        return sum(code.beta) + sum(code.nu)
    raise TypeError(code)


def grade(code: Any) -> int:
    return 2 - derivative_order(code)


def code_key(code: Any, *, normalized: bool = False) -> str:
    if isinstance(code, Id):
        return "D(0,0)=Id"
    if isinstance(code, DxN):
        return "D(" + ",".join(map(str, code.mu)) + ")"
    if isinstance(code, StateFNu):
        stem = "G[beta=(" + ",".join(map(str, code.beta)) + ");nu=(" + ",".join(map(str, code.nu)) + ")]"
        if normalized:
            return stem
        return qstr(as_fraction(code.a)) + "*" + stem
    raise TypeError(code)


def sympy_json_number(value: sp.Expr) -> dict[str, Any]:
    value = sp.simplify(value)
    if value.is_Rational:
        frac = Fraction(int(value.p), int(value.q))
        return {"exact": qstr(frac), "float": float(frac)}
    return {"expression": str(value), "float": float(value)}


def differentiated_source(expr: sp.Expr, beta: tuple[int, ...], nu: tuple[int, ...]) -> sp.Expr:
    xs = sp.symbols("x0:2")
    zs = sp.symbols("z0:3")
    ans = expr
    for symbol, order in zip(xs, beta):
        if order:
            ans = sp.diff(ans, symbol, order)
    for symbol, order in zip(zs, nu):
        if order:
            ans = sp.diff(ans, symbol, order)
    return sp.expand(ans)


def terminal_polynomial_l1(expr: sp.Expr, code: Any) -> sp.Expr:
    """Standard-monomial coefficient l1 norm at the zero terminal jet."""
    if isinstance(code, (Id, DxN)):
        return sp.Integer(0)
    if not isinstance(code, StateFNu):
        raise TypeError(code)
    xs = sp.symbols("x0:2")
    zs = sp.symbols("z0:3")
    poly_expr = differentiated_source(expr, code.beta, code.nu).subs(dict.fromkeys(zs, 0))
    if sp.simplify(poly_expr) == 0:
        return sp.Integer(0)
    poly = sp.Poly(sp.expand(poly_expr), *xs)
    return sp.simplify(sum(abs(c) for c in poly.coeffs()))


def make_pde(name: str, expr: sp.Expr) -> StateDependentPDEnD:
    return StateDependentPDEnD(
        T=sp.Rational(1, 100),
        d=2,
        deriv_map=((0, 0), (1, 0), (0, 1)),
        f_expr=expr,
        phi_expr=sp.Integer(0),
        sigma2=1.0,
        name=name,
    )


def generic_source() -> sp.Expr:
    """Dense exact-rational quadratic with every permitted derivative live."""
    x0, x1 = sp.symbols("x0:2")
    z0, p0, p1 = sp.symbols("z0:3")
    del z0
    x = sp.Matrix([x0, x1])
    p = sp.Matrix([p0, p1])
    h0 = sp.Integer(1)
    h = sp.Matrix([2, 3])
    Q = sp.Matrix([[5, 7], [7, 11]])
    d = sp.Matrix([13, 17])
    D = sp.Matrix([[19, 23], [29, 31]])
    N = sp.Matrix([[37, 41], [41, 43]])
    return sp.expand(h0 + (h.T * x)[0] + sp.Rational(1, 2) * (x.T * Q * x)[0]
                     + ((d + D * x).T * p)[0] + sp.Rational(1, 2) * (p.T * N * p)[0])


def rational_financial_source() -> sp.Expr:
    """Exact two-factor Merton log source specified by the mathematical audit."""
    x0, x1 = sp.symbols("x0:2")
    z0, p0, p1 = sp.symbols("z0:3")
    del z0
    p = sp.Matrix([p0, p1])
    drift = sp.Matrix([-x0 + x1 / 20, -sp.Rational(39, 40) * x1])
    N = sp.Matrix([[sp.Rational(5, 4), sp.Rational(1, 8)],
                   [sp.Rational(1, 8), sp.Rational(17, 16)]])
    h = x0 / 20 + x1**2 / 200
    return sp.expand(h + (drift.T * p)[0] + sp.Rational(1, 2) * (p.T * N * p)[0])


def nonquadratic_stress_source(gamma: Fraction) -> sp.Expr:
    """Exact quartic-in-state stress source for either audited CRRA value."""
    x0, x1 = sp.symbols("x0:2")
    z0, p0, p1 = sp.symbols("z0:3")
    del z0
    p = sp.Matrix([p0, p1])
    if gamma == Fraction(1, 2):
        drift = sp.Matrix([-x0 + x1**2 / 20, -x1 + x1**2 / 40])
        N = sp.Matrix([[sp.Rational(5, 4), sp.Rational(1, 8)],
                       [sp.Rational(1, 8), sp.Rational(17, 16)]])
        h = x0 / 20 + x1**4 / 200
    elif gamma == Fraction(2):
        drift = sp.Matrix([-x0 - x1**2 / 40, -x1 - x1**2 / 80])
        N = sp.Matrix([[sp.Rational(7, 8), -sp.Rational(1, 16)],
                       [-sp.Rational(1, 16), sp.Rational(31, 32)]])
        h = -x0 / 10 - x1**4 / 400
    else:
        raise ValueError(f"unaudited gamma: {gamma}")
    return sp.expand(h + (drift.T * p)[0] + sp.Rational(1, 2) * (p.T * N * p)[0])


def assessment_float_source(module: Any) -> tuple[sp.Expr, dict[str, Any]]:
    """Reconstruct the assessment check's whitened source without rounding it."""
    model = module.make_model()
    A = np.asarray(model["A"])
    B = np.linalg.cholesky(A)
    Binv = np.linalg.inv(B)
    gamma = float(model["gamma"])
    a = 1.0 - gamma
    C = np.asarray(model["c"])
    R = np.linalg.inv(np.asarray(model["sigma"]))
    K = np.asarray(model["K"])
    k = np.asarray(model["k"])
    ell = np.asarray(model["ell"])
    L = np.asarray(model["L"])
    r0 = float(model["r0"])
    r1 = np.asarray(model["r1"])
    delta = float(model["delta"])
    M = A + a / gamma * C.T @ R @ C
    Mt = Binv @ M @ Binv.T

    x0, x1 = sp.symbols("x0:2")
    z0, p0, p1 = sp.symbols("z0:3")
    del z0
    xv = sp.Matrix([x0, x1])
    grad = sp.Matrix([p0, p1])
    Bsp, Binvsp = sp.Matrix(B), sp.Matrix(Binv)
    Csp, Rsp = sp.Matrix(C), sp.Matrix(R)
    lam = sp.Matrix(ell) + sp.Matrix(L) * Bsp * xv
    drift = Binvsp * (sp.Matrix(k) - sp.Matrix(K) * Bsp * xv
                      + a / gamma * Csp.T * Rsp * lam)
    potential = (a * (r0 + (sp.Matrix(r1).T * Bsp * xv)[0]) - delta
                 + a / (2 * gamma) * (lam.T * Rsp * lam)[0])
    expr = sp.expand((drift.T * grad)[0]
                     + sp.Rational(1, 2) * (grad.T * sp.Matrix(Mt) * grad)[0]
                     + potential)
    metadata = {
        "provenance": "reconstructed from log_factor_check.py::make_model and whitening_check",
        "cholesky_B": B.tolist(),
        "whitened_quadratic_gradient_matrix": Mt.tolist(),
        "coefficients_are_floating": True,
    }
    return expr, metadata


def canonical_parents(pde: StateDependentPDEnD, expr: sp.Expr) -> list[Any]:
    parents: list[Any] = [Id()]
    for order in (1, 2):
        parents.extend(DxN(mu) for mu in multiindices(2, order))
    for total in range(3):
        for beta_total in range(total + 1):
            nu_total = total - beta_total
            for beta in multiindices(2, beta_total):
                # nu[0] is the unused value-jet component and must remain 0.
                for nu_tail in multiindices(2, nu_total):
                    nu = (0, *nu_tail)
                    if pde.f_beta_nu(beta, nu) is not None:
                        parents.append(StateFNu(1.0, beta, nu))
    # Id is D^0; all remaining keys are distinct normalized code types.
    assert len({code_key(p, normalized=True) for p in parents}) == len(parents)
    return parents


def classify_tuple(
    pde: StateDependentPDEnD, children: tuple[Any, ...]
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if any(isinstance(c, StateFNu)
           and (c.a == 0.0 or pde.f_beta_nu(c.beta, c.nu) is None)
           for c in children):
        reasons.append("identically_zero_source_code")
    if any(isinstance(c, DxN) and sum(c.mu) >= 3 for c in children):
        reasons.append("D_order_at_least_3")
    return ("retained" if not reasons else "absorbing"), reasons


def audit_graph(name: str, expr: sp.Expr, *, exact_coefficients: bool) -> dict[str, Any]:
    pde = make_pde(name, expr)
    reduced = StateDependentMechanismND(pde, reduce_zero_tuples=True)
    raw = StateDependentMechanismND(pde, reduce_zero_tuples=False)
    parents = canonical_parents(pde, expr)
    rows: list[dict[str, Any]] = []
    all_labels = 0
    retained_labels = 0
    max_arity = 0
    max_row_size = 0
    max_S = Fraction(0)

    for parent in parents:
        original = reduced.tuples(parent)
        raw_row = raw.tuples(parent)
        row_size = len(original)
        q = Fraction(1, row_size)
        row_S = Fraction(0)
        labels: list[dict[str, Any]] = []
        for idx, children in enumerate(original):
            status, reasons = classify_tuple(pde, children)
            outside = Fraction(1)
            normalized_children: list[str] = []
            original_children: list[str] = []
            grades: list[int] = []
            for child in children:
                original_children.append(code_key(child))
                if isinstance(child, StateFNu):
                    outside *= as_fraction(child.a)
                    normalized_children.append(code_key(StateFNu(1.0, child.beta, child.nu), normalized=True))
                else:
                    normalized_children.append(code_key(child, normalized=True))
                grades.append(grade(child))
            invariant = None
            if status == "retained":
                invariant = all(g >= 0 for g in grades) and sum(grades) <= grade(parent)
                if not invariant:
                    raise AssertionError((name, parent, children, grades))
                row_S += outside * outside / q
                retained_labels += 1
            labels.append({
                "label": f"{code_key(parent, normalized=True)}::L{idx:03d}",
                "original_index": idx,
                "q": qstr(q),
                "original_children": original_children,
                "normalized_children": normalized_children,
                "outside_coefficient": qstr(outside),
                "arity": len(children),
                "status": status,
                "absorbing_reasons": reasons,
                "child_grades": grades,
                "child_grade_sum": sum(grades),
                "grade_invariant": invariant,
            })
            max_arity = max(max_arity, len(children))
        max_S = max(max_S, row_S)
        all_labels += row_size
        max_row_size = max(max_row_size, row_size)
        retained_abs = [abs(Fraction(label["outside_coefficient"]))
                        for label in labels if label["status"] == "retained"]
        original_coefficients = [Fraction(label["outside_coefficient"]) for label in labels]
        original_abs = [abs(value) for value in original_coefficients]
        rows.append({
            "parent": code_key(parent, normalized=True),
            "parent_grade": grade(parent),
            "raw_unreduced_row_size": len(raw_row),
            "original_reduced_row_size": row_size,
            "uniform_q": qstr(q),
            "q_provenance": (
                "1 / len(StateDependentMechanismND(reduce_zero_tuples=True).tuples(parent)); "
                "computed before absorbing high-D labels"
            ),
            "source_zero_labels_pruned_before_q": len(raw_row) - row_size,
            "retained_label_count": len(retained_abs),
            "original_outside_signed_sum": qstr(sum(original_coefficients, Fraction(0))),
            "original_outside_abs_sum": qstr(sum(original_abs, Fraction(0))),
            "original_outside_abs_max": qstr(max(original_abs, default=Fraction(0))),
            "retained_outside_abs_sum": qstr(sum(retained_abs, Fraction(0))),
            "retained_outside_abs_max": qstr(max(retained_abs, default=Fraction(0))),
            "row_S_sum_a2_over_q": qstr(row_S),
            "labels": labels,
        })

    # Terminal coefficient norms of normalized types.  Exact sources remain
    # exact here; the assessment benchmark is explicitly only floating-point.
    terminal_rows = []
    lc_values: list[sp.Expr] = []
    for parent in parents:
        lc = terminal_polynomial_l1(expr, parent)
        lc_values.append(lc)
        terminal_rows.append({
            "type": code_key(parent, normalized=True),
            "grade": grade(parent),
            "terminal_coefficient_l1": sympy_json_number(lc),
        })
    max_lc = max(lc_values, key=lambda x: float(x))
    A_expr = max(sp.Integer(1), sp.simplify(max_lc**2), key=lambda x: float(x))
    A = Fraction(int(A_expr.p), int(A_expr.q)) if A_expr.is_Rational else float(A_expr)

    # Named estimator clock for the candidate theorem: Exp(lambda), lambda=32.
    # With d=2 and polynomial weight (1+|x|^2)^2, the reviewed heat bound is
    # c = lambda + 4 = 36.
    clock_rate = Fraction(32)
    K = max_S / clock_rate
    c = Fraction(36)
    if isinstance(A, Fraction):
        KA2 = K * A * A
        taucrit = math.log1p(float(c / KA2)) / (2 * float(c)) if KA2 else math.inf
        # e^x <= 1/(1-x), 0 <= x < 1.  Choose a rational horizon whose
        # resulting exact upper bound makes the denominator strictly positive.
        if KA2:
            # The condition simplifies to n > 2c + 2 K A^2, avoiding an
            # unbounded incremental search when a deliberately dense generic
            # source has large coefficients.
            threshold = 2 * c + 2 * KA2
            n = threshold.numerator // threshold.denominator + 1
            T = Fraction(1, n)
            x = 2 * c * T
            expm1_upper = x / (1 - x)
            ratio_upper = KA2 / c * expm1_upper
            assert x < 1 and ratio_upper < 1
        else:
            T, expm1_upper, ratio_upper = Fraction(1), Fraction(0), Fraction(0)
        certificate = {
            "lambda": qstr(clock_rate),
            "heat_weight_constant_c": qstr(c),
            "max_S_sum_a2_over_q_exact": qstr(max_S),
            "K_exact": qstr(K),
            "max_terminal_coefficient_l1_exact": qstr(Fraction(max_lc)),
            "A_exact": qstr(A),
            "tau_critical_float": taucrit,
            "certified_rational_T": qstr(T),
            "elementary_bound": "exp(x)-1 <= x/(1-x) for 0 <= x < 1",
            "x_equals_2cT": qstr(x),
            "expm1_upper_exact": qstr(expm1_upper),
            "denominator_subtraction_upper_exact": qstr(ratio_upper),
            "strictly_below_tau_critical": ratio_upper < 1,
            "scope": (
                "Exact coefficient arithmetic for the finite graph/terminal-polynomial certificate; "
                "the surrounding stochastic theorem is supplied and reviewed separately."
            ),
        }
    else:
        KA2 = float(K) * A * A
        taucrit = math.log1p(float(c) / KA2) / (2.0 * float(c)) if KA2 else math.inf
        certificate = {
            "lambda": float(clock_rate),
            "heat_weight_constant_c": float(c),
            "max_S_sum_a2_over_q_exact": qstr(max_S),
            "K_float": float(K),
            "max_terminal_coefficient_l1_float": float(max_lc),
            "A_float": A,
            "tau_critical_float": taucrit,
            "scope": "Floating diagnostic only; no rational or interval enclosure of source coefficients.",
        }

    if name == "exact_rational_two_factor_Merton_log_source":
        # A deliberately conservative certificate requested for the named
        # Exp(32) estimator.  Every comparison below is exact rational
        # arithmetic; no floating exponential evaluation is used.
        expected_A = Fraction(25, 16)
        conservative_S = Fraction(250)
        conservative_K = conservative_S / clock_rate
        T0 = Fraction(1, 100)
        y = c * T0  # 9/25
        exp_cT_upper = Fraction(1, 1) / (1 - y)
        exp_2cT_upper = exp_cT_upper**2
        expm1_2cT_upper = exp_2cT_upper - 1
        ratio_upper = conservative_K * expected_A**2 / c * expm1_2cT_upper
        denominator_lower = 1 - ratio_upper
        if A != expected_A or max_S > conservative_S:
            raise AssertionError((A, max_S))
        if not (y < 1 and ratio_upper < Fraction(4, 5)
                and denominator_lower > Fraction(1, 5)
                and expected_A * exp_cT_upper < Fraction(5, 2)):
            raise AssertionError((y, ratio_upper, denominator_lower))
        certificate["conservative_T_1_over_100_certificate"] = {
            "actual_S_le_250": max_S <= conservative_S,
            "S_bound": qstr(conservative_S),
            "K_bound_at_lambda_32": qstr(conservative_K),
            "A_exact": qstr(expected_A),
            "T": qstr(T0),
            "cT": qstr(y),
            "exp_cT_bound": "exp(cT) <= 1/(1-cT)",
            "exp_cT_upper": qstr(exp_cT_upper),
            "exp_2cT_upper": qstr(exp_2cT_upper),
            "expm1_2cT_upper": qstr(expm1_2cT_upper),
            "denominator_subtraction_upper": qstr(ratio_upper),
            "denominator_lower": qstr(denominator_lower),
            "denominator_lower_gt_1_over_5": denominator_lower > Fraction(1, 5),
            "numerator_A_exp_cT_lt_5_over_2": expected_A * exp_cT_upper < Fraction(5, 2),
            "resulting_b_squared_lt_125_over_4_lt_36": True,
            "resulting_b_lt_6": True,
        }

    return {
        "name": name,
        "source_expression": str(expr),
        "source_coefficients_exact_rational": exact_coefficients,
        "deriv_map": [[0, 0], [1, 0], [0, 1]],
        "dummy_value_jet_component": "z0 is unused, so every live nu has nu[0]=0",
        "grading": "r(D^mu)=2-|mu| (Id=D^0); r(G_beta,nu)=2-|beta|-|nu|",
        "normalization": (
            "Products of StateFNu.a are stored as each label's outside_coefficient; "
            "labelled alternatives are not merged."
        ),
        "type_count": len(parents),
        "D_type_count_including_Id": sum(isinstance(p, (Id, DxN)) for p in parents),
        "G_type_count": sum(isinstance(p, StateFNu) for p in parents),
        "original_reduced_label_count": all_labels,
        "retained_label_count": retained_labels,
        "max_original_reduced_row_size": max_row_size,
        "max_branching_arity": max_arity,
        "all_retained_grade_checks_pass": True,
        "rows": rows,
        "terminal_types": terminal_rows,
        "majorant_constants": certificate,
    }


def high_derivative_evidence(expr: sp.Expr) -> dict[str, Any]:
    pde = make_pde("generic_quadratic_high_D_check", expr)
    mechanism = StateDependentMechanismND(pde, reduce_zero_tuples=False)
    rows = []
    violations = []
    for order in range(3, 6):
        for mu in multiindices(2, order):
            counts = {"term_count": 0, "zero_G": 0, "negative_grade_D": 0, "both": 0}
            for idx, term in enumerate(mechanism._expand_dx(mu)):
                zero_g = pde.f_beta_nu(term.beta, term.nu) is None
                high_d = any(sum(lam) >= 3 for lam in term.u_factors)
                counts["term_count"] += 1
                counts["zero_G"] += int(zero_g)
                counts["negative_grade_D"] += int(high_d)
                counts["both"] += int(zero_g and high_d)
                if not (zero_g or high_d):
                    violations.append({"mu": list(mu), "term_index": idx,
                                       "beta": list(term.beta), "nu": list(term.nu),
                                       "u_factors": [list(v) for v in term.u_factors]})
            rows.append({"mu": list(mu), **counts})
    if violations:
        raise AssertionError(violations[:3])
    return {
        "orders_checked": [3, 4, 5],
        "multiindices_checked": len(rows),
        "expansion_terms_checked": sum(row["term_count"] for row in rows),
        "violations": violations,
        "all_terms_have_zero_G_or_negative_grade_D": True,
        "rows": rows,
        "limitation": (
            "Finite exact-symbolic evidence for orders 3--5 only; the general order statement "
            "requires the separate grade-invariant proof."
        ),
    }


def normalized_signature(children: Iterable[Any]) -> tuple[str, ...]:
    return tuple(code_key(child, normalized=True) for child in children)


def nonquadratic_membership_case(gamma: Fraction) -> dict[str, Any]:
    """One tiny exact label-membership check used by the obstruction proof."""
    expr = nonquadratic_stress_source(gamma)
    pde = make_pde(f"quadratic_risk_premium_stress_gamma_{qstr(gamma)}", expr)
    mechanism = StateDependentMechanismND(pde, reduce_zero_tuples=True)
    zero_b = (0, 0)
    zero_nu = (0, 0, 0)
    d22 = DxN((0, 2))
    d2 = DxN((0, 1))
    fcode = StateFNu(1.0, zero_b, zero_nu)
    gpp22 = StateFNu(1.0, zero_b, (0, 0, 2))

    rows = {
        "D22": mechanism.tuples(d22),
        "D2": mechanism.tuples(d2),
        "F": mechanism.tuples(fcode),
        "Gpp22": mechanism.tuples(gpp22),
    }
    signatures = {key: [normalized_signature(tpl) for tpl in row]
                  for key, row in rows.items()}
    gx22 = code_key(StateFNu(1.0, (0, 2), zero_nu), normalized=True)
    gp2 = code_key(StateFNu(1.0, zero_b, (0, 0, 1)), normalized=True)
    gpp = code_key(gpp22, normalized=True)
    D22 = code_key(d22, normalized=True)

    targets = {
        "D22_contains_singleton_Gxx22": (gx22,),
        "D22_contains_Gpp22_D22_D22": (gpp, D22, D22),
        "D2_contains_Gp2_D22": (gp2, D22),
        "F_contains_Gp2_Gp2_D22": (gp2, gp2, D22),
    }
    checks = {
        "D22_contains_singleton_Gxx22": targets["D22_contains_singleton_Gxx22"] in signatures["D22"],
        "D22_contains_Gpp22_D22_D22": targets["D22_contains_Gpp22_D22_D22"] in signatures["D22"],
        "D2_contains_Gp2_D22": targets["D2_contains_Gp2_D22"] in signatures["D2"],
        "F_contains_Gp2_Gp2_D22": targets["F_contains_Gp2_Gp2_D22"] in signatures["F"],
    }
    gpp_row_is_zero = (
        len(rows["Gpp22"]) == 1
        and len(rows["Gpp22"][0]) == 1
        and isinstance(rows["Gpp22"][0][0], StateFNu)
        and rows["Gpp22"][0][0].a == 0.0
    )
    checks["Gpp22_branches_to_zero_tuple"] = gpp_row_is_zero
    if not all(checks.values()):
        raise AssertionError((checks, signatures))

    terminal_gx22 = differentiated_source(expr, (0, 2), zero_nu).subs(
        dict.fromkeys(sp.symbols("z0:3"), 0))
    terminal_gpp = differentiated_source(expr, zero_b, (0, 0, 2)).subs(
        dict.fromkeys(sp.symbols("z0:3"), 0))
    terminal_gp2 = differentiated_source(expr, zero_b, (0, 0, 1)).subs(
        dict.fromkeys(sp.symbols("z0:3"), 0))
    x1 = sp.symbols("x1")
    if gamma == Fraction(1, 2):
        expected_gx22 = 3 * x1**2 / 50
        expected_gpp = sp.Rational(17, 16)
        expected_gp2 = -x1 + x1**2 / 40
    else:
        expected_gx22 = -3 * x1**2 / 100
        expected_gpp = sp.Rational(31, 32)
        expected_gp2 = -x1 - x1**2 / 80
    if sp.expand(terminal_gx22 - expected_gx22) != 0:
        raise AssertionError(terminal_gx22)
    if sp.expand(terminal_gpp - expected_gpp) != 0:
        raise AssertionError(terminal_gpp)
    if sp.expand(terminal_gp2 - expected_gp2) != 0:
        raise AssertionError(terminal_gp2)
    return {
        "gamma": qstr(gamma),
        "source_expression": str(expr),
        "checks": checks,
        "D22_target_multiplicity": signatures["D22"].count((gpp, D22, D22)),
        "terminal_Gxx22_exact": str(terminal_gx22),
        "terminal_Gpp22_exact": str(terminal_gpp),
        "terminal_Gp2_exact": str(terminal_gp2),
        "rows": {key: [list(sig) for sig in value] for key, value in signatures.items()},
        "scope": (
            "Exact symbolic membership only.  The non-L1 divergence argument using these "
            "labels is an ordinary proof reviewed separately, not established by enumeration."
        ),
    }


def nonquadratic_membership_checks() -> dict[str, Any]:
    """Both exact CRRA stress cases, without enumerating their full graphs."""
    cases = {
        "gamma_1_over_2": nonquadratic_membership_case(Fraction(1, 2)),
        "gamma_2": nonquadratic_membership_case(Fraction(2)),
    }
    return {
        "cases": cases,
        "all_membership_checks_pass": all(
            all(case["checks"].values()) for case in cases.values()),
        "scope": (
            "Four mechanism rows per gamma only.  The non-L1 divergence argument using these "
            "labels is an ordinary proof reviewed separately, not established by enumeration."
        ),
    }


def load_log_check() -> Any:
    spec = importlib.util.spec_from_file_location("assessment_log_factor_check", LOG_CHECK)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {LOG_CHECK}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_existing_log_checks(module: Any) -> dict[str, Any]:
    symbolic = module.symbolic_checks()
    if not all(symbolic.values()):
        raise AssertionError(symbolic)
    model = module.make_model()
    eigenvalues = np.linalg.eigvalsh(np.asarray(model["joint"]))
    primary, tighter, convergence = module.solve_riccati(model)
    residuals = module.residual_checks(model, primary)
    policies = module.policy_checks(model, primary)
    whitening = module.whitening_check(model, primary)
    frozen_clock = module.frozen_clock_check()
    result = {
        "source_script": str(LOG_CHECK),
        "source_sha256": hashlib.sha256(LOG_CHECK.read_bytes()).hexdigest(),
        "called_functions": [
            "symbolic_checks", "make_model", "solve_riccati", "residual_checks",
            "policy_checks", "whitening_check", "frozen_clock_check",
        ],
        "main_called": False,
        "symbolic": symbolic,
        "joint_covariance_min_eigenvalue": float(eigenvalues.min()),
        "riccati_terminal_primary": primary.y[:, -1].tolist(),
        "riccati_tighter_method_max_difference": convergence,
        "residuals": residuals,
        "whitening": whitening,
        "frozen_clock": frozen_clock,
        **policies,
        "determinism": "No random generator is used; no seed is applicable.",
        "limitations": [
            "Symbolic identities and finite-point residual checks do not prove stochastic integrability.",
            "The ODE comparison is a floating-point convergence diagnostic, not exact arithmetic.",
            "The frozen-clock calculation is not a full-tree proposal theorem.",
        ],
    }
    if (convergence > 2e-10 or max(residuals.values()) > 2e-10
            or whitening["whitened_source_max_difference"] > 2e-12
            or whitening["state_dependent_2d_api_source_max_difference"] > 2e-12
            or frozen_clock["stationarity_residual"] > 2e-12):
        raise AssertionError(result)
    return result


def run_read_only(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                               timeout=15, check=False)
    return {
        "command": command,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def lean_inventory() -> dict[str, Any]:
    formal = REPO / "formal"
    expected_pin = "leanprover/lean4:v4.33.0"
    actual_pin = (formal / "lean-toolchain").read_text().strip()
    if actual_pin != expected_pin:
        raise AssertionError(f"formal pin changed: {actual_pin!r}")
    commands = []
    for cwd in (REPO, formal):
        commands.append(run_read_only(["lean", "--version"], cwd))
        commands.append(run_read_only(["lake", "--version"], cwd))
        commands.append(run_read_only(["elan", "show"], cwd))
    root_match = re.search(r"version ([^,]+)", commands[0]["stdout"])
    formal_match = re.search(r"version ([^,]+)", commands[3]["stdout"])
    root_version = root_match.group(1) if root_match else "unparsed"
    formal_version = formal_match.group(1) if formal_match else "unparsed"
    if commands[3]["returncode"] != 0 or formal_version != "4.33.0":
        raise AssertionError(commands[3])
    return {
        "formal_lean_toolchain_file": actual_pin,
        "expected_formal_pin": expected_pin,
        "resolved_paths": {name: shutil.which(name) for name in ("lean", "lake", "elan")},
        "commands": commands,
        "finding": (
            f"This-run observation parsed from command output: repository root Lean {root_version}; "
            f"formal/ Lean {formal_version}, selected by its asserted {expected_pin} pin."
        ),
        "actions_not_taken": "No Lean build, test, installation, update, or file edit was performed.",
    }


def environment() -> dict[str, Any]:
    import scipy
    return {
        "command": "conda run --no-capture-output -n parabolab python docs/research/milestone-1-checks.py",
        "cwd": str(REPO),
        "python_executable": sys.executable,
        "conda_prefix": os.environ.get("CONDA_PREFIX"),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "sympy": sp.__version__,
        "scipy": scipy.__version__,
        "seeds": "none (all checks deterministic)",
        "dependencies_installed": False,
    }


def report_text(result: dict[str, Any]) -> str:
    lines = [
        "Milestone 1 bounded deterministic checks: PASS",
        "",
        f"Command: {result['environment']['command']}",
        f"Python: {result['environment']['python']} ({result['environment']['python_executable']})",
        f"NumPy/SymPy/SciPy: {result['environment']['numpy']} / {result['environment']['sympy']} / {result['environment']['scipy']}",
        f"Elapsed: {result['environment']['elapsed_seconds']:.3f} seconds",
        "Seeds: none; all checks deterministic.",
        "",
    ]
    for key in ("generic_quadratic_graph", "exact_rational_financial_graph", "assessment_float_financial_graph"):
        graph = result[key]
        constants = graph["majorant_constants"]
        lines.extend([
            graph["name"],
            f"  types: {graph['type_count']} (D incl. Id {graph['D_type_count_including_Id']}, G {graph['G_type_count']})",
            f"  labels: original reduced {graph['original_reduced_label_count']}, retained {graph['retained_label_count']}",
            f"  max row / arity: {graph['max_original_reduced_row_size']} / {graph['max_branching_arity']}",
            f"  grade checks: {graph['all_retained_grade_checks_pass']}",
            f"  majorant constants: {json.dumps(constants, sort_keys=True)}",
            "",
        ])
    high = result["high_D_order_3_to_5"]
    stress = result["nonquadratic_stress_membership"]
    log = result["existing_log_factor_checks"]
    lines.extend([
        "High-D expansion evidence",
        f"  multiindices / terms: {high['multiindices_checked']} / {high['expansion_terms_checked']}",
        f"  violations: {len(high['violations'])}",
        f"  limitation: {high['limitation']}",
        "",
        "Nonquadratic stress-label membership",
        f"  all checks: {stress['all_membership_checks_pass']}",
        f"  gamma=1/2 terminals G_x2x2 / G_p2p2 / G_p2: "
        f"{stress['cases']['gamma_1_over_2']['terminal_Gxx22_exact']} / "
        f"{stress['cases']['gamma_1_over_2']['terminal_Gpp22_exact']} / "
        f"{stress['cases']['gamma_1_over_2']['terminal_Gp2_exact']}",
        f"  gamma=2 terminals G_x2x2 / G_p2p2 / G_p2: "
        f"{stress['cases']['gamma_2']['terminal_Gxx22_exact']} / "
        f"{stress['cases']['gamma_2']['terminal_Gpp22_exact']} / "
        f"{stress['cases']['gamma_2']['terminal_Gp2_exact']}",
        f"  scope: {stress['scope']}",
        "",
        "Existing log-factor deterministic checks",
        f"  symbolic: {log['symbolic']}",
        f"  Riccati method max difference: {log['riccati_tighter_method_max_difference']:.3e}",
        f"  max log/direct residual: {log['residuals']['max_log_pde_residual']:.3e} / {log['residuals']['max_direct_pde_residual']:.3e}",
        f"  whitened/API differences: {log['whitening']['whitened_source_max_difference']:.3e} / {log['whitening']['state_dependent_2d_api_source_max_difference']:.3e}",
        "  limitations: " + " ".join(log["limitations"]),
        "",
        "Lean toolchain inventory",
        f"  formal/lean-toolchain: {result['lean_inventory']['formal_lean_toolchain_file']}",
        f"  finding: {result['lean_inventory']['finding']}",
        f"  {result['lean_inventory']['actions_not_taken']}",
        "",
        "Execution note",
        f"  Initial interrupted run: approximately {result['execution_history']['initial_interrupted_run_elapsed_seconds_approx']} seconds.",
        f"  Cause: {result['execution_history']['initial_interruption_reason']}",
        f"  Fix: {result['execution_history']['replacement']}",
        "",
        "Scope warning: these are finite symbolic/numerical checks, not a proof of the full stochastic theorem.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    started = time.perf_counter()
    module = load_log_check()
    generic = generic_source()
    rational = rational_financial_source()
    assessment_expr, assessment_meta = assessment_float_source(module)
    rational_graph = audit_graph(
        "exact_rational_two_factor_Merton_log_source", rational, exact_coefficients=True)
    rational_graph["financial_model_metadata"] = {
        "a": "1/2",
        "gamma": "1/2",
        "asset_variance_Sigma": [["1"]],
        "factor_covariance_A": [["1", "0"], ["0", "1"]],
        "return_factor_covariance_C": [["1/2", "1/4"]],
        "mean_reversion_drift_b": ["-x0", "-x1"],
        "short_rate_r": "x0/10",
        "risk_premium_lambda": "x1/10",
        "delta": "0",
        "schur_complement_A_minus_CtC": [["3/4", "-1/8"], ["-1/8", "15/16"]],
        "schur_positive_definite_exact_check": {
            "leading_minor_1": "3/4",
            "determinant": "11/16",
            "eigenvalues": ["11/16", "1"],
            "pass": True,
        },
        "interpretation": (
            "Short-rate and risk-premium loadings are nonparallel; nonzero C gives a "
            "state-dependent hedging component in the policy map."
        ),
    }
    result = {
        "status": "PASS",
        "environment": environment(),
        "generic_quadratic_graph": audit_graph(
            "dense_generic_exact_rational_quadratic", generic, exact_coefficients=True),
        "exact_rational_financial_graph": rational_graph,
        "assessment_float_financial_graph": {
            **audit_graph("assessment_whitened_two_factor_Merton_log_source",
                          assessment_expr, exact_coefficients=False),
            "source_metadata": assessment_meta,
        },
        "high_D_order_3_to_5": high_derivative_evidence(generic),
        "nonquadratic_stress_membership": nonquadratic_membership_checks(),
        "existing_log_factor_checks": run_existing_log_checks(module),
        "lean_inventory": lean_inventory(),
        "execution_history": {
            "initial_interrupted_run_elapsed_seconds_approx": 120,
            "initial_interruption_reason": (
                "The generic exact-certificate code incremented n one-by-one while seeking a "
                "very small rational horizon for deliberately large generic coefficients."
            ),
            "replacement": (
                "Solved the sufficient rational condition directly as n > 2c + 2 K A^2; "
                "this was script overhead, not mathematical or numerical instability."
            ),
        },
        "global_limitations": [
            "No Monte Carlo experiment was run.",
            "No finite-depth moment estimate is interpreted as an upper bound.",
            "Graph enumeration through D order 5 is finite evidence, not the general proof.",
            "The floating assessment graph has no rational/interval coefficient certificate.",
            "No Lean theorem was authored or built; only toolchain resolution was inspected.",
        ],
    }
    result["environment"]["elapsed_seconds"] = time.perf_counter() - started
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    OUT_TEXT.write_text(report_text(result))
    print(report_text(result), end="")


if __name__ == "__main__":
    main()
