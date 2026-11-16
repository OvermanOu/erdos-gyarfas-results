#!/usr/bin/env python3
"""Standalone standard-library verifier for Paper I:
Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four.

Run from repository root or paper1_nilpotent_haar/:
    python verify_paper1.py
    python verify_paper1.py --write-certificates
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from functools import reduce
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "certificates" / "paper1_certificates.json"

# Universal cyclically nonbacktracking color words (0=1, 1=a, 2=b; even=s, odd=s^-1)
WORD16_ABELIAN = "0101012010201212"
WORDS16_CLASS2 = ("0101201210102102", "0102012010121021")
WORD32_CLASS3 = "01010102012012101012012010212012"
WORD32_P3_BAL = "01010201021201201020201210212012"
WORDS64_CLASS4 = [
    "0101012012021020101021021012012101020120210210101012102101201201",
    "0202021021012010202012012021021202010210120120202021201202102102",
    "1010102102120121010120120102102010121021201201010102012010210210",
]
WORD64_ALLPRIME_P3 = "0101010102020120101020121020201202102020121020101021020201010101"
WORD32_UT6 = "01010101201210210210102102102012"

# ---------------------------------------------------------------------------
# 1. Abelian Haar universal 16-word & 10 short collision words
# ---------------------------------------------------------------------------

ABELIAN_COLLAPSE = {(0, 1), (1, -1), (1, 0)}
ABELIAN_SHORT = {
    (0, 2): "0202",
    (1, -2): "0212",
    (1, 1): "0102",
    (1, 2): "01010212",
    (2, -2): "1212",
    (2, -1): "0121",
    (2, 0): "0101",
    (2, 1): "01210202",
    (3, -1): "01212102",
    (3, 0): "01012102",
}


def verify_abelian_haar() -> dict:
    shifts = ((0, 0), (1, 0), (0, 1))

    def walk_z2(word: str):
        pos = [(0, (0, 0))]
        for i, ch in enumerate(word):
            x, y = pos[-1][1]
            dx, dy = shifts[int(ch)]
            sgn = 1 if i % 2 == 0 else -1
            pos.append(((i + 1) % 2, (x + sgn * dx, y + sgn * dy)))
        return pos

    def canon_vec(v: tuple[int, int]) -> tuple[int, int]:
        return v if v > (0, 0) else (-v[0], -v[1])

    assert len(WORD16_ABELIAN) == 16
    assert all(WORD16_ABELIAN[i] != WORD16_ABELIAN[(i + 1) % 16] for i in range(16))
    pos = walk_z2(WORD16_ABELIAN)
    assert pos[-1] == pos[0] and len(set(pos[:-1])) == 16

    diffs = set()
    for i, (side, (x, y)) in enumerate(pos[:-1]):
        for j in range(i):
            other_side, (u, v) = pos[j]
            if side == other_side:
                diffs.add(canon_vec((x - u, y - v)))
    assert diffs == ABELIAN_COLLAPSE | set(ABELIAN_SHORT) and len(diffs) == 13

    for vec, sw in ABELIAN_SHORT.items():
        assert len(sw) in (4, 8)
        assert all(sw[i] != sw[(i + 1) % len(sw)] for i in range(len(sw)))
        delta = walk_z2(sw)[-1][1]
        assert delta == vec or delta == (-vec[0], -vec[1])

    # Finite exhaustive physical control on Z/n x Z/m for 1 <= n,m <= 5
    def walk_mod(word: str, n: int, m: int, a: tuple[int, int], b: tuple[int, int]):
        sh = ((0, 0), a, b)
        out = [(0, (0, 0))]
        for i, ch in enumerate(word):
            x, y = out[-1][1]
            dx, dy = sh[int(ch)]
            sgn = 1 if i % 2 == 0 else -1
            out.append(((i + 1) % 2, ((x + sgn * dx) % n, (y + sgn * dy) % m)))
        return out

    counts = Counter()
    cases = 0
    for n, m in product(range(1, 6), repeat=2):
        elems = list(product(range(n), range(m)))
        for a in elems:
            for b in elems:
                if len({(0, 0), a, b}) != 3:
                    continue
                cases += 1
                u_walk = walk_mod(WORD16_ABELIAN, n, m, a, b)
                assert u_walk[0] == u_walk[-1]
                if len(set(u_walk[:-1])) == 16:
                    cyc = u_walk[:-1]
                else:
                    cyc = None
                    for i in range(16):
                        for j in range(i):
                            if u_walk[i] == u_walk[j]:
                                diff = canon_vec((pos[i][1][0] - pos[j][1][0], pos[i][1][1] - pos[j][1][1]))
                                assert diff not in ABELIAN_COLLAPSE
                                sw = ABELIAN_SHORT[diff]
                                vs = walk_mod(sw, n, m, a, b)
                                assert vs[0] == vs[-1]
                                vs.pop()
                                if len(set(vs)) == len(vs):
                                    cyc = vs
                                else:
                                    assert len(sw) == 8
                                    for k in range(8):
                                        if vs[k] == vs[(k + 4) % 8]:
                                            c4 = [vs[(k + t) % 8] for t in range(4)]
                                            assert len(set(c4)) == 4
                                            cyc = c4
                                            break
                                break
                        if cyc is not None:
                            break
                assert cyc is not None and len(cyc) in (4, 8, 16) and len(set(cyc)) == len(cyc)
                counts[len(cyc)] += 1

    assert cases == 2400
    return {
        "universal_word16": WORD16_ABELIAN,
        "formal_same_shore_differences": 13,
        "short_words_count": len(ABELIAN_SHORT),
        "finite_torus_cases_checked": cases,
        "witness_length_counts": dict(sorted(counts.items())),
    }


def verify_class2_haar() -> dict:
    """Verify W0, W1 for free class-2 group and ord([a,b]) >= 3 (including ord=3 branches)."""
    shifts = ((0, 0, 0), (1, 0, 0), (0, 1, 0))

    def mul2(u, v):
        x, y, z = u
        a, b, c = v
        return (x + a, y + b, z + c + x * b)

    def inv2(u):
        x, y, z = u
        return (-x, -y, -z + x * y)

    def prefixes(word):
        u = (0, 0, 0)
        shores = [[], []]
        for i, ch in enumerate(word):
            shores[i % 2].append(u)
            s = shifts[int(ch)]
            u = mul2(u, s if i % 2 == 0 else inv2(s))
        assert u == (0, 0, 0)
        assert len(word) == 16 and all(word[i] != word[(i + 1) % 16] for i in range(16))
        return shores

    max_bounds = {}
    for w in WORDS16_CLASS2:
        sh = prefixes(w)
        mx_dx = mx_dy = mx_dz = 0
        for shore in sh:
            assert len(set(shore)) == 8
            for u, v in combinations(shore, 2):
                dx, dy, dz = (u[k] - v[k] for k in range(3))
                mx_dx = max(mx_dx, abs(dx))
                mx_dy = max(mx_dy, abs(dy))
                mx_dz = max(mx_dz, abs(dz))
                assert abs(dx) <= 3 and abs(dy) <= 1 and abs(dz) <= 2
                if dx == 0 and dy == 0:
                    assert dz != 0
        max_bounds[w] = [mx_dx, mx_dy, mx_dz]

    # Commutator order 3 branches: a^3 = c^h for h in {0,1,2}
    for h in range(3):
        w = WORDS16_CLASS2[1] if h == 1 else WORDS16_CLASS2[0]
        for shore in prefixes(w):
            for u, v in combinations(shore, 2):
                dx, dy, dz = (u[k] - v[k] for k in range(3))
                assert not (dx % 3 == 0 and dy % 3 == 0 and (dz + h * (dx // 3)) % 3 == 0)

    return {
        "words16_class2": list(WORDS16_CLASS2),
        "max_diff_bounds": max_bounds,
        "ord_c_eq_3_branches_verified": [0, 1, 2],
    }


# ---------------------------------------------------------------------------
# 2. Exact Integral Magnus Algebra & Free Nilpotent Hall Collection (Class 3 & 4)
# ---------------------------------------------------------------------------

def magnus_mul(x: dict[str, int], y: dict[str, int], deg: int) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for u, cu in x.items():
        lu = len(u)
        for v, cv in y.items():
            if lu + len(v) <= deg:
                out[u + v] += cu * cv
    return {k: v for k, v in out.items() if v}


def magnus_inv(x: dict[str, int], deg: int) -> dict[str, int]:
    u = {k: v for k, v in x.items() if k}
    res: dict[str, int] = {"": 1}
    pwr = dict(u)
    for k in range(1, deg + 1):
        sgn = -1 if k % 2 else 1
        for m, c in pwr.items():
            res[m] = res.get(m, 0) + sgn * c
        if k < deg:
            pwr = magnus_mul(pwr, u, deg)
    return {k: v for k, v in res.items() if v}


def magnus_pow(x: dict[str, int], n: int, deg: int) -> dict[str, int]:
    if n < 0:
        x = magnus_inv(x, deg)
        n = -n
    res: dict[str, int] = {"": 1}
    base = x
    while n:
        if n & 1:
            res = magnus_mul(res, base, deg)
        n >>= 1
        if n:
            base = magnus_mul(base, base, deg)
    return res


def magnus_comm(x: dict[str, int], y: dict[str, int], deg: int) -> dict[str, int]:
    # Convention [x, y] = x^-1 y^-1 x y
    return magnus_mul(
        magnus_mul(magnus_mul(magnus_inv(x, deg), magnus_inv(y, deg), deg), x, deg),
        y,
        deg,
    )


class FreeNilpotentClass4:
    """Exact integral free rank-2 nilpotent group of class 4 via Magnus expansion."""

    def __init__(self) -> None:
        self.deg = 4
        self.I = {"": 1}
        self.A = {"": 1, "x": 1}
        self.B = {"": 1, "y": 1}
        self.C = magnus_comm(self.A, self.B, 4)
        self.D = magnus_comm(self.C, self.A, 4)
        self.E = magnus_comm(self.C, self.B, 4)
        self.F = magnus_comm(self.D, self.A, 4)
        self.G = magnus_comm(self.D, self.B, 4)
        self.H = magnus_comm(self.E, self.B, 4)
        assert magnus_comm(self.E, self.A, 4) == self.G
        # Verify unit triangularity of Hall leading terms
        assert self.C.get("xy") == 1 and self.C.get("yx") == -1
        assert (self.D.get("xxy", 0), self.E.get("xxy", 0), self.D.get("xyy", 0), self.E.get("xyy", 0)) == (-1, 0, 0, 1)
        minor4 = [[q.get(m, 0) for q in (self.F, self.G, self.H)] for m in ("xxxy", "xxyy", "xyyy")]
        det4 = (
            minor4[0][0] * (minor4[1][1] * minor4[2][2] - minor4[1][2] * minor4[2][1])
            - minor4[0][1] * (minor4[1][0] * minor4[2][2] - minor4[1][2] * minor4[2][0])
            + minor4[0][2] * (minor4[1][0] * minor4[2][1] - minor4[1][1] * minor4[2][0])
        )
        assert det4 == -1
        # Verify class-3 cube identities modulo gamma4
        c3_lhs1 = self.truncate3(magnus_comm(magnus_pow(self.A, 3, 4), self.B, 4))
        c3_rhs1 = self.truncate3(magnus_mul(magnus_pow(self.C, 3, 4), magnus_pow(self.D, 3, 4), 4))
        c3_lhs2 = self.truncate3(magnus_comm(self.A, magnus_pow(self.B, 3, 4), 4))
        c3_rhs2 = self.truncate3(magnus_mul(magnus_pow(self.C, 3, 4), magnus_pow(self.E, 3, 4), 4))
        assert c3_lhs1 == c3_rhs1 and c3_lhs2 == c3_rhs2

    @staticmethod
    def truncate3(s: dict[str, int]) -> dict[str, int]:
        return {k: v for k, v in s.items() if len(k) <= 3}

    def walk(self, word: str) -> tuple[dict[str, int], list[dict[str, int]]]:
        steps = {"0": self.I, "1": self.A, "2": self.B}
        invs = {"0": self.I, "1": magnus_inv(self.A, 4), "2": magnus_inv(self.B, 4)}
        state = self.I
        states = []
        for i, ch in enumerate(word):
            states.append(state)
            state = magnus_mul(state, steps[ch] if i % 2 == 0 else invs[ch], 4)
        return state, states

    def collect(self, s: dict[str, int]) -> list[int]:
        x, y = s.get("x", 0), s.get("y", 0)
        t = magnus_mul(magnus_mul(magnus_pow(self.B, -y, 4), magnus_pow(self.A, -x, 4), 4), s, 4)
        z = t.get("xy", 0)
        t = magnus_mul(magnus_pow(self.C, -z, 4), t, 4)
        u, v = -t.get("xxy", 0), t.get("xyy", 0)
        t = magnus_mul(magnus_mul(magnus_pow(self.E, -v, 4), magnus_pow(self.D, -u, 4), 4), t, 4)
        r, ss, tt = t.get("xxxy", 0), -t.get("xxyy", 0), t.get("xyyy", 0)
        rebuilt = magnus_mul(
            magnus_mul(magnus_pow(self.F, r, 4), magnus_pow(self.G, ss, 4), 4),
            magnus_pow(self.H, tt, 4),
            4,
        )
        assert t == rebuilt
        return [x, y, z, u, v, r, ss, tt]


def verify_class3_theorems(fn4: FreeNilpotentClass4) -> dict:
    # A. Universal C32 for p>=5 and p=3 (exp>=9)
    n = len(WORD32_CLASS3)
    assert n == 32 and all(WORD32_CLASS3[i] != WORD32_CLASS3[(i + 1) % n] for i in range(n))
    end, states = fn4.walk(WORD32_CLASS3)
    assert fn4.truncate3(end) == fn4.I
    end_hall = fn4.collect(end)
    assert end_hall[:5] == [0, 0, 0, 0, 0]

    inv_states = [magnus_inv(s, 4) for s in states]
    ab_hist = Counter()
    xyz_hist = Counter()
    zero_ab = []
    gcd3_deltas = Counter()
    for i in range(32):
        for j in range(i + 2, 32, 2):
            diff = magnus_mul(inv_states[i], states[j], 4)
            h = fn4.collect(diff)
            gab = gcd(abs(h[0]), abs(h[1]))
            gxyz = gcd(abs(h[0]), abs(h[1]), abs(h[2]))
            ab_hist[gab] += 1
            xyz_hist[gxyz] += 1
            if gab == 3:
                gcd3_deltas[(h[0], h[1])] += 1
            if gab == 0:
                gap = j - i
                start = i
                if gap > 16:
                    start = j
                    gap = 32 - gap
                seg = "".join(WORD32_CLASS3[(start + t) % 32] for t in range(gap))
                assert gap == 6 and len(set(seg[:3])) == 3 and seg == seg[:3] * 2
                zero_ab.append({"i": i, "j": j, "segment": seg})

    assert sum(ab_hist.values()) == 240
    assert dict(ab_hist) == {0: 7, 1: 174, 2: 39, 3: 16, 4: 4}
    assert dict(xyz_hist) == {1: 217, 2: 21, 3: 2}
    assert [(r["i"], r["j"]) for r in zero_ab] == [(1, 27), (2, 28), (7, 13), (8, 14), (17, 23), (18, 24), (19, 25)]
    assert dict(gcd3_deltas) == {(-3, 0): 5, (3, 0): 9, (0, 3): 2}

    # Control: UT4(F3) x C9 (order 243, class 3, exp_ab = 9)
    def mul_ut4_c9(x, y):
        a, b, c, d, e, f = x[0]
        A, B, C, D, E, F = y[0]
        m = ((a + A) % 3, (b + B + a * D) % 3, (c + C + a * E + b * F) % 3, (d + D) % 3, (e + E + d * F) % 3, (f + F) % 3)
        return (m, (x[1] + y[1]) % 9)

    ident = ((0,) * 6, 0)

    def pow_ut4_c9(x, k):
        r = ident
        while k:
            if k & 1:
                r = mul_ut4_c9(r, x)
            x = mul_ut4_c9(x, x)
            k >>= 1
        return r

    a = ((1, 0, 0, 1, 0, 0), 1)
    b = ((0, 0, 0, 1, 0, 1), 0)
    ai = pow_ut4_c9(a, 8)
    bi = pow_ut4_c9(b, 8)
    assert pow_ut4_c9(a, 3)[1] == 3 and pow_ut4_c9(b, 3) == ident
    seen = {ident}
    q = deque([ident])
    while q:
        u = q.popleft()
        for g in (a, b, ai, bi):
            v = mul_ut4_c9(u, g)
            if v not in seen:
                seen.add(v)
                q.append(v)
    assert len(seen) == 243
    # Re-anchor at a: shifts (1, a^-1, a^-1 b)
    A_r, B_r = ai, mul_ut4_c9(ai, b)
    assert pow_ut4_c9(A_r, 3)[1] != 0 and pow_ut4_c9(B_r, 3)[1] != 0
    for w_test, sh in ((WORD32_CLASS3, (ident, A_r, B_r)), ("".join({"0": "1", "1": "0", "2": "2"}[c] for c in WORD32_CLASS3), (ident, a, b))):
        invs = tuple(pow_ut4_c9(g, 8) for g in sh)
        v = ident
        vis = set()
        for i, ch in enumerate(w_test):
            assert (i % 2, v) not in vis
            vis.add((i % 2, v))
            v = mul_ut4_c9(v, (sh if i % 2 == 0 else invs)[int(ch)])
        assert v == ident and len(vis) == 32

    # B. Balanced C32 for p=3, K_ab = C3 x C3
    assert len(WORD32_P3_BAL) == 32 and all(WORD32_P3_BAL[i] != WORD32_P3_BAL[(i + 1) % 32] for i in range(32))
    end_b, states_b = fn4.walk(WORD32_P3_BAL)
    assert fn4.truncate3(end_b) == fn4.I
    assert fn4.collect(end_b)[:5] == [0, 0, 0, 0, 0]
    inv_b = [magnus_inv(s, 4) for s in states_b]
    mod3_divisible = []
    for i in range(32):
        for j in range(i + 2, 32, 2):
            h5 = fn4.collect(magnus_mul(inv_b[i], states_b[j], 4))[:5]
            if all(val % 3 == 0 for val in h5[:3]):
                mod3_divisible.append((i, j, h5))
    assert mod3_divisible == [(idx, 26 - idx, [0, 0, 0, 0, -1]) for idx in range(3, 8)]

    # Physical order-81 3-group control (both e != 1 and swap a<->b branches)
    I4 = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))

    def mm4(x, y):
        return tuple(tuple(sum(x[i][k] * y[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))

    def mp4(x, k):
        z = I4
        while k:
            if k & 1:
                z = mm4(z, x)
            x = mm4(x, x)
            k >>= 1
        return z

    def cm4(x, y):
        return mm4(mm4(mm4(mp4(x, 8), mp4(y, 8)), x), y)

    A_mat = [[int(i == j) for j in range(4)] for i in range(4)]
    B_mat = [[int(i == j) for j in range(4)] for i in range(4)]
    A_mat[0][1] = 1
    B_mat[0][1] = B_mat[1][2] = B_mat[2][3] = 1
    A_m = tuple(map(tuple, A_mat))
    B_m = tuple(map(tuple, B_mat))
    C_m = cm4(A_m, B_m)
    D_m = cm4(C_m, A_m)
    E_m = cm4(C_m, B_m)
    assert mp4(A_m, 3) == I4 and mp4(B_m, 3) == E_m and mp4(B_m, 9) == I4
    assert D_m == I4 and E_m != I4
    # Replay both original (e != 1) and swapped (e' = d^-1 != 1)
    swapped_w = "".join({"0": "0", "1": "2", "2": "1"}[ch] for ch in WORD32_P3_BAL)
    for w_test, sh in ((WORD32_P3_BAL, (I4, A_m, B_m)), (swapped_w, (I4, B_m, A_m))):
        invs = tuple(mp4(g, 8) for g in sh)
        v = I4
        vis = set()
        for i, ch in enumerate(w_test):
            assert (i % 2, v) not in vis
            vis.add((i % 2, v))
            v = mm4(v, (sh if i % 2 == 0 else invs)[int(ch)])
        assert v == I4 and len(vis) == 32

    return {
        "universal_word32": WORD32_CLASS3,
        "universal_word32_end_hall_prefix5": end_hall[:5],
        "universal_word32_abelian_gcd_hist": dict(sorted(ab_hist.items())),
        "universal_word32_xyz_gcd_hist": dict(sorted(xyz_hist.items())),
        "universal_word32_gcd3_deltas": {str(k): v for k, v in sorted(gcd3_deltas.items())},
        "ut4_f3_x_c9_control_order": 243,
        "balanced_word32_p3": WORD32_P3_BAL,
        "balanced_word32_mod3_eligible_pairs": [(i, j, h) for i, j, h in mod3_divisible],
        "order81_control_verified_both_branches": True,
    }


# ---------------------------------------------------------------------------
# 3. Class <= 4 Arbitrary Exponent (p>=5) + Truncated Free Algebras (all p)
# ---------------------------------------------------------------------------

def verify_class4_theorems(fn4: FreeNilpotentClass4) -> dict:
    directions = [(1, -1), (1, -1), (0, 1)]
    central_vecs = [(-3, 3, 0), (0, -3, 3), (0, 3, 0)]
    word_summaries = []

    for w, d_exp, c_exp in zip(WORDS64_CLASS4, directions, central_vecs):
        assert len(w) == 64 and all(w[i] != w[(i + 1) % 64] for i in range(64))
        end, states = fn4.walk(w)
        assert end == fn4.I and fn4.collect(end) == [0] * 8
        inv_states = [magnus_inv(s, 4) for s in states]

        ab_hist = Counter()
        xyz_hist = Counter()
        grade3_rows = []
        central_rows = []
        for i in range(64):
            for j in range(i + 2, 64, 2):
                h = fn4.collect(magnus_mul(inv_states[i], states[j], 4))
                ab_hist[gcd(abs(h[0]), abs(h[1]))] += 1
                gxyz = gcd(abs(h[0]), abs(h[1]), abs(h[2]))
                xyz_hist[gxyz] += 1
                if gxyz == 0:
                    if h[3] or h[4]:
                        u, v = h[3], h[4]
                        assert gcd(abs(u), abs(v)) in (1, 2)
                        assert u * d_exp[1] == v * d_exp[0]
                        grade3_rows.append((i, j, h))
                    else:
                        cv = tuple(h[5:8])
                        assert cv == c_exp or cv == tuple(-t for t in c_exp)
                        central_rows.append((i, j, h))

        assert dict(ab_hist) == {0: 80, 1: 668, 2: 136, 3: 84, 4: 24}
        assert sum(xyz_hist.values()) == 992 and max(xyz_hist) <= 4
        assert len(grade3_rows) == 47 and len(central_rows) == 5
        word_summaries.append({
            "word": w,
            "abelian_gcd_hist": dict(sorted(ab_hist.items())),
            "xyz_gcd_hist": dict(sorted(xyz_hist.items())),
            "grade3_direction": list(d_exp),
            "grade3_pair_count": len(grade3_rows),
            "central_vector": list(c_exp),
            "central_pair_count": len(central_rows),
        })

    # Verify determinant of the three central vectors is +-27
    det_c = (
        central_vecs[0][0] * (central_vecs[1][1] * central_vecs[2][2] - central_vecs[1][2] * central_vecs[2][1])
        - central_vecs[0][1] * (central_vecs[1][0] * central_vecs[2][2] - central_vecs[1][2] * central_vecs[2][0])
        + central_vecs[0][2] * (central_vecs[1][0] * central_vecs[2][1] - central_vecs[1][1] * central_vecs[2][0])
    )
    assert abs(det_c) == 27

    # All-prime integral Magnus histograms for WORD64_ALLPRIME_P3 and WORDS64_CLASS4[0]
    all_prime_records = []
    for label, w, expected in (
        ("characteristic_3", WORD64_ALLPRIME_P3, {1: 978, 2: 2, 5: 8, 7: 4}),
        ("characteristic_not_3", WORDS64_CLASS4[0], {1: 987, 3: 5}),
    ):
        assert len(w) == 64 and all(w[i] != w[(i + 1) % 64] for i in range(64))
        end, states = fn4.walk(w)
        assert end == fn4.I
        inv_states = [magnus_inv(s, 4) for s in states]
        hist = Counter()
        for i in range(64):
            for j in range(i + 2, 64, 2):
                diff = magnus_mul(inv_states[i], states[j], 4)
                assert diff != fn4.I
                g = gcd(*(abs(v) for k, v in diff.items() if k))
                hist[g] += 1
        assert dict(hist) == expected and sum(hist.values()) == 992
        all_prime_records.append({"label": label, "word": w, "magnus_gcd_hist": dict(sorted(hist.items()))})

    # Literal higher-exponent truncated algebra checks mod p and mod p^2 for p=2,3,5,7,11
    def trunc_mul(a, b, mod):
        out = defaultdict(int)
        for u, cu in a.items():
            for v, cv in b.items():
                if len(u) + len(v) <= 4:
                    out[u + v] += cu * cv
        return {k: c % mod for k, c in out.items() if c % mod}

    def trunc_walk(w, mod):
        s = {(): 1}
        out = [s]
        for i, ch in enumerate(w):
            c = int(ch)
            if c:
                let = c - 1
                if i % 2 == 0:
                    fac = {(): 1, (let,): 1}
                else:
                    fac = {(): 1, (let,): -1, (let, let): 1, (let, let, let): -1, (let, let, let, let): 1}
                s = trunc_mul(s, fac, mod)
            out.append(s)
        return out

    monos = [m for d in range(1, 5) for m in product(range(2), repeat=d)]
    p2_checks = []
    for p in (2, 3, 5, 7, 11):
        w = WORD64_ALLPRIME_P3 if p == 3 else WORDS64_CLASS4[0]
        for mod in (p, p * p):
            st = trunc_walk(w, mod)
            assert st[-1] == {(): 1}
            for parity in (0, 1):
                verts = [st[i] for i in range(parity, 64, 2)]
                assert all(any((a.get(m, 0) - b.get(m, 0)) % mod for m in monos) for a, b in combinations(verts, 2))
        x = {(): 1, (0,): 1}
        xp = {(): 1}
        for _ in range(p):
            xp = trunc_mul(xp, x, p * p)
        assert xp.get((0,), 0) == p and xp != {(): 1}
        # Order of 1+X in (Z/p^2 Z)<X,Y>/(deg>=5): p^3 for p in {2,3}, and p^2 for p>=5.
        cur = xp
        mult_order = p
        while cur != {(): 1}:
            next_cur = {(): 1}
            for _ in range(p):
                next_cur = trunc_mul(next_cur, cur, p * p)
            cur = next_cur
            mult_order *= p
        expected_order = {2: 16, 3: 27}.get(p, p * p)
        assert mult_order == expected_order
        p2_checks.append({"p": p, "mod_p2": p * p, "generator_order": mult_order, "simple_C64": True})

    return {
        "three_words_c64": word_summaries,
        "central_matrix_determinant": det_c,
        "all_prime_truncated_algebra": all_prime_records,
        "explicit_mod_p2_controls": p2_checks,
    }


# ---------------------------------------------------------------------------
# 4. Nonnilpotent & High-Girth Boundary Controls (UT4 girth 14, UT6 girth >=18, P7 x A4)
# ---------------------------------------------------------------------------

def verify_boundary_controls() -> dict:
    # A. Nonnilpotent P7 x A4 (order 28,812; gamma3=28, gamma4=4): C32 lifts to C64
    p7 = 7
    M0 = (0,) * 6
    P0 = tuple(range(4))
    I_pa = (M0, P0)

    def mat7(u, v):
        a, b, c, d, e, f = u
        A, B, C, D, E, F = v
        return ((a + A) % 7, (b + B + a * D) % 7, (c + C + a * E + b * F) % 7, (d + D) % 7, (e + E + d * F) % 7, (f + F) % 7)

    def invmat7(z):
        a, b, c, d, e, f = z
        return ((-a) % 7, (-b + a * d) % 7, (-c + a * e + b * f - a * d * f) % 7, (-d) % 7, (-e + d * f) % 7, (-f) % 7)

    def perm4(u, v):
        return tuple(u[v[i]] for i in range(4))

    def pinv4(z):
        return tuple(z.index(i) for i in range(4))

    def mul_pa(u, v):
        return (mat7(u[0], v[0]), perm4(u[1], v[1]))

    def inv_pa(u):
        return (invmat7(u[0]), pinv4(u[1]))

    g = ((1, 0, 0, 1, 0, 0), (1, 2, 0, 3))
    h = ((0, 0, 0, 1, 0, 1), (1, 0, 3, 2))
    sh = (I_pa, g, h)
    bk = tuple(inv_pa(z) for z in sh)
    st = I_pa
    vis = set()
    mid = None
    for i, ch in enumerate(WORD32_CLASS3 * 2):
        assert (i % 2, st) not in vis
        vis.add((i % 2, st))
        st = mul_pa(st, (sh if i % 2 == 0 else bk)[int(ch)])
        if i == 31:
            mid = st
    assert mid == (M0, (3, 2, 1, 0)) and mul_pa(mid, mid) == I_pa and st == I_pa and len(vis) == 64

    # B. UT4(Fp) class-3 girth-14 boundary family (all primes p>=7)
    A4 = (1, 0, 0, 1, 0, 0)
    B4 = (0, 0, 0, 1, 0, 1)
    I4z = (0,) * 6

    def mul4z(x, y):
        a, b, c, d, e, f = x
        A, B, C, D, E, F = y
        return (a + A, b + B + a * D, c + C + a * E + b * F, d + D, e + E + d * F, f + F)

    def inv4z(x):
        a, b, c, d, e, f = x
        return (-a, -b + a * d, -c + a * e + b * f - a * d * f, -d, -e + d * f, -f)

    sh4 = (I4z, A4, B4)
    bk4 = tuple(inv4z(x) for x in sh4)

    def word_hist_ut4(n):
        out = Counter()

        def dfs(gv, prev, first, depth):
            if depth == n:
                if prev != first:
                    out[reduce(gcd, map(abs, gv))] += 1
                return
            for col in range(3):
                if col != prev:
                    dfs(mul4z(gv, (sh4 if depth % 2 == 0 else bk4)[col]), col, col if first < 0 else first, depth + 1)

        dfs(I4z, -1, -1, 0)
        return dict(sorted(out.items()))

    ut4_exp = {
        4: {1: 18},
        6: {1: 60, 3: 6},
        8: {1: 248, 2: 10},
        10: {1: 950, 2: 40, 3: 30, 5: 6},
        12: {1: 3888, 2: 144, 3: 66},
        16: {1: 62688, 2: 1720, 3: 928, 4: 106, 5: 64, 6: 32},
    }
    ut4_hists = {}
    for L, exp in ut4_exp.items():
        wh = word_hist_ut4(L)
        assert wh == exp and 0 not in wh and sum(wh.values()) == 2**L + 2
        ut4_hists[str(L)] = wh

    for w_ut4, exp_c in (("01010210202012", {1: 42}), ("02101020201010120210210101010101", {1: 219, 2: 5, 3: 13, 5: 3})):
        st = I4z
        vs = []
        for i, ch in enumerate(w_ut4):
            vs.append((i % 2, st))
            st = mul4z(st, (sh4 if i % 2 == 0 else bk4)[int(ch)])
        assert st == I4z
        chist = Counter(
            reduce(gcd, (abs(x - y) for x, y in zip(u[1], v[1])))
            for i, u in enumerate(vs)
            for v in vs[i + 1:]
            if u[0] == v[0]
        )
        assert dict(chist) == exp_c

    # C. UT6(Fp)/<I+E16> class-4 girth>=18 boundary family (all primes p>=11)
    pos6 = [(i, j) for i in range(6) for j in range(i + 1, 6) if (i, j) != (0, 5)]
    idx6 = {x: i for i, x in enumerate(pos6)}
    I6z = (0,) * 14

    def step6(v, col, pos):
        if col == 0:
            return v
        z = list(v)
        sgn = 1 if pos else -1
        for k in ((0, 2, 4) if col == 1 else (1, 3)):
            j = k + 1
            for i in range(k + 1):
                if (i, j) == (0, 5):
                    continue
                z[idx6[i, j]] += sgn * (1 if i == k else v[idx6[i, k]])
        return tuple(z)

    ut6_exp = {
        4: {1: 14, 2: 4},
        6: {1: 56, 2: 6, 3: 4},
        8: {1: 238, 2: 16, 4: 4},
        10: {1: 920, 2: 90, 3: 10, 5: 6},
        12: {1: 3800, 2: 276, 3: 12, 4: 6, 6: 4},
        14: {1: 15148, 2: 1092, 3: 84, 4: 56, 7: 6},
        16: {1: 61068, 2: 4210, 3: 160, 4: 96, 8: 4},
    }
    ut6_hists = {}
    for L, exp in ut6_exp.items():
        wh = Counter()

        def dfs6(v, prev, first, k):
            if k == L:
                if first != prev:
                    wh[reduce(gcd, map(abs, v))] += 1
                return
            for col in range(3):
                if col != prev:
                    dfs6(step6(v, col, k % 2 == 0), col, col if first < 0 else first, k + 1)

        dfs6(I6z, -1, -1, 0)
        assert dict(sorted(wh.items())) == exp and 0 not in wh and sum(wh.values()) == 2**L + 2
        ut6_hists[str(L)] = dict(sorted(wh.items()))

    for w_ut6, exp_c in (
        (WORD32_UT6, {1: 224, 2: 11, 3: 3, 4: 2}),
        (WORD64_ALLPRIME_P3, {1: 814, 2: 126, 3: 12, 4: 18, 5: 8, 6: 6, 7: 4, 8: 4}),
    ):
        st = I6z
        vs = []
        for i, ch in enumerate(w_ut6):
            vs.append((i % 2, st))
            st = step6(st, int(ch), i % 2 == 0)
        assert st == I6z
        chist = Counter(
            reduce(gcd, (abs(x - y) for x, y in zip(u[1], v[1])))
            for i, u in enumerate(vs)
            for v in vs[i + 1:]
            if u[0] == v[0]
        )
        assert dict(chist) == exp_c

    return {
        "nonnilpotent_P7xA4_lifted_C64": True,
        "ut4_girth14_words_checked": 71004,
        "ut4_word_histograms": ut4_hists,
        "ut6_girth18_words_checked": 87390,
        "ut6_word_histograms": ut6_hists,
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    fn4 = FreeNilpotentClass4()
    res = {
        "paper": "Paper I: Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four",
        "status": "PASS",
        "abelian": verify_abelian_haar(),
        "class2": verify_class2_haar(),
        "class3": verify_class3_theorems(fn4),
        "class4": verify_class4_theorems(fn4),
        "boundary_controls": verify_boundary_controls(),
        "elapsed_seconds": round(time.monotonic() - t0, 3),
    }
    if write_certs:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    elif CERT_PATH.exists():
        saved = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        current = json.loads(json.dumps(res))
        for k in ("abelian", "class2", "class3", "class4", "boundary_controls"):
            assert saved[k] == current[k], f"Certificate mismatch in section {k}"
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificates", action="store_true")
    args = parser.parse_args()
    out = run(write_certs=args.write_certificates)
    print(json.dumps({
        "status": out["status"],
        "elapsed_seconds": out["elapsed_seconds"],
        "abelian_torus_cases": out["abelian"]["finite_torus_cases_checked"],
        "class3_p3_mod3_pairs": len(out["class3"]["balanced_word32_mod3_eligible_pairs"]),
        "class4_det": out["class4"]["central_matrix_determinant"],
        "ut4_words_checked": out["boundary_controls"]["ut4_girth14_words_checked"],
        "ut6_words_checked": out["boundary_controls"]["ut6_girth18_words_checked"],
    }, indent=2))
