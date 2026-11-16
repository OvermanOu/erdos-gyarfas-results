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
W4_UNCOND = "01012012102021010202102120101202"
W5_UNCOND = "01012020101201210202101020210212"
W0_CRIT = "01010120121010210201210210102012"
W0_CRIT_SWAP = "02020210212020120102120120201021"
W64_CRIT00 = "0101210120120212102012020120102021012012120121202102121012021021"

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


# ---------------------------------------------------------------------------
# 5. Unconditional Class <= 4 Verification (Sharp p >= 5 C32 & Full p = 3)
# ---------------------------------------------------------------------------

def verify_unconditional_class4(fn4: FreeNilpotentClass4) -> dict:
    def comb2(n: int) -> int:
        return n * (n - 1) // 2

    def comb3(n: int) -> int:
        return n * (n - 1) * (n - 2) // 6

    def mul_b_free(h: tuple[int, ...]) -> tuple[int, ...]:
        x, y, z, u, v, r, s, t = h
        return (x, y + 1, z, u, v + z, r, s + u, t + v)

    def mul_a_free(h: tuple[int, ...]) -> tuple[int, ...]:
        x, y, z, u, v, r, s, t = h
        return (x + 1, y, z - y, u + z, v - comb2(y), r + u, s + v, t - comb3(y))

    def proj_crit(h: tuple[int, ...], mu: int = 2, lam: int = 1) -> tuple[int, int, int, int, int]:
        x, y, z, u, v, r, s, t = h
        qz, rem_z = divmod(z, 3)
        du = (u - v) % 3
        fw = (mu * qz + lam * v + r - s + t) % 3
        return (x, y, rem_z, du, fw)

    def step_a_crit(st: tuple[int, int, int, int, int], mu: int = 2, lam: int = 1) -> tuple[int, int, int, int, int]:
        x, y, z0, u0, w0 = st
        return proj_crit(mul_a_free((x, y, z0, u0, 0, w0, 0, 0)), mu, lam)

    def step_b_crit(st: tuple[int, int, int, int, int], mu: int = 2, lam: int = 1) -> tuple[int, int, int, int, int]:
        x, y, z0, u0, w0 = st
        return proj_crit(mul_b_free((x, y, z0, u0, 0, w0, 0, 0)), mu, lam)

    def step_a_inv_crit(st: tuple[int, int, int, int, int], mu: int = 2, lam: int = 1) -> tuple[int, int, int, int, int]:
        x, y, z0, u0, w0 = st
        zp = z0 + y
        up = u0 - zp
        vp = comb2(y)
        return proj_crit((x - 1, y, zp, up, vp, w0 - up, -vp, comb3(y)), mu, lam)

    def step_b_inv_crit(st: tuple[int, int, int, int, int], mu: int = 2, lam: int = 1) -> tuple[int, int, int, int, int]:
        x, y, z0, u0, w0 = st
        return proj_crit((x, y - 1, z0, u0, -z0, w0, -u0, z0), mu, lam)

    def reduce_gcrit(st: tuple[int, int, int, int, int], alpha: int, beta: int) -> tuple[int, int, int, int, int]:
        qx, rx = divmod(st[0], 3)
        qy, ry = divmod(st[1], 3)
        return (rx, ry, st[2], st[3], (st[4] + alpha * qx + beta * qy) % 3)

    # 1. Identities in F2/gamma5(F2) and exact Q_crit(2,1) polynomial action
    assert magnus_comm(fn4.C, fn4.D, 4) == fn4.I
    assert magnus_comm(fn4.C, fn4.E, 4) == fn4.I
    assert magnus_comm(fn4.D, fn4.E, 4) == fn4.I
    a3 = magnus_pow(fn4.A, 3, 4)
    b3 = magnus_pow(fn4.B, 3, 4)
    c3 = magnus_pow(fn4.C, 3, 4)
    assert fn4.collect(magnus_comm(a3, fn4.B, 4)) == [0, 0, 3, 3, 0, 1, 0, 0]
    assert fn4.collect(magnus_comm(fn4.A, b3, 4)) == [0, 0, 3, 0, 3, 0, 0, 1]
    assert fn4.collect(magnus_comm(c3, fn4.A, 4)) == [0, 0, 0, 3, 0, 0, 0, 0]
    assert fn4.collect(magnus_comm(c3, fn4.B, 4)) == [0, 0, 0, 0, 3, 0, 0, 0]
    for y in range(-3, 5):
        by = magnus_pow(fn4.B, y, 4)
        assert fn4.collect(magnus_comm(by, fn4.A, 4)) == [0, 0, -y, 0, -comb2(y), 0, 0, -comb3(y)]

    gens = (fn4.A, fn4.B, fn4.C, fn4.D, fn4.E, fn4.F, fn4.G, fn4.H)
    for x in (-1, 0, 2):
        for y in (-2, 0, 1, 3):
            for z in (-1, 0, 2):
                h0 = (x, y, z, 1, -1, 2, 0, -1)
                el = fn4.I
                for g, ex in zip(gens, h0):
                    if ex:
                        el = magnus_mul(el, magnus_pow(g, ex, 4), 4)
                assert tuple(fn4.collect(magnus_mul(el, fn4.A, 4))) == mul_a_free(h0)
                assert tuple(fn4.collect(magnus_mul(el, fn4.B, 4))) == mul_b_free(h0)

    for x in (-2, 0, 3):
        for y in (-1, 1, 2):
            for z0 in range(3):
                for u0 in range(3):
                    for w0 in range(3):
                        st = (x, y, z0, u0, w0)
                        assert step_a_inv_crit(step_a_crit(st)) == st
                        assert step_b_inv_crit(step_b_crit(st)) == st
    for z_ex in (-3, 0, 3, 6):
        for vv in (-2, -1, 0, 1, 2):
            h1 = (1, 2, 1, 2, 0, 1, 0, 0)
            h2 = (1, 2, 1 + z_ex, 2 + vv, vv, 1 - 2 * (z_ex // 3) - vv, 0, 0)
            assert proj_crit(h1) == proj_crit(h2)
            assert proj_crit(mul_a_free(h2)) == step_a_crit(proj_crit(h1))
            assert proj_crit(mul_b_free(h2)) == step_b_crit(proj_crit(h1))

    # 2. Sharp p >= 5 C32 and p = 3 two-stage reduction
    def analyze_word_free(w: str) -> dict:
        n = len(w)
        assert all(w[i] != w[(i + 1) % n] for i in range(n))
        end_d, states = fn4.walk(w)
        assert fn4.collect(end_d) == [0] * 8
        inv_st = [magnus_inv(s, 4) for s in states]
        ab_hist = Counter()
        diffs = []
        for i in range(n):
            for j in range(i + 2, n, 2):
                h = fn4.collect(magnus_mul(inv_st[i], states[j], 4))
                diffs.append((i, j, h))
                ab_hist[gcd(abs(h[0]), abs(h[1]))] += 1
        return {"length": n, "ab_gcd_hist": dict(sorted(ab_hist.items())), "diffs": diffs}

    d_w4 = analyze_word_free(W4_UNCOND)
    d_w5 = analyze_word_free(W5_UNCOND)
    d_w0 = analyze_word_free(W0_CRIT)
    d_w0s = analyze_word_free(W0_CRIT_SWAP)
    assert d_w4["ab_gcd_hist"] == {0: 19, 1: 177, 2: 44}
    assert d_w5["ab_gcd_hist"] == {0: 19, 1: 177, 2: 44}
    w4_zero_ab_zs = sorted({h[2] for _, _, h in d_w4["diffs"] if h[0] == 0 and h[1] == 0})
    w5_zero_ab_zs = sorted({h[2] for _, _, h in d_w5["diffs"] if h[0] == 0 and h[1] == 0})
    assert w4_zero_ab_zs == [-1, 1, 3, 4] and w5_zero_ab_zs == [-1, 1, 3, 4]

    def extract_zuv_mod3(diffs):
        nz = [(i, j, h) for i, j, h in diffs if h[0] % 3 == 0 and h[1] % 3 == 0 and (h[0], h[1]) != (0, 0)]
        assert len(nz) == 0
        return sorted({(h[2], h[3] % 3, h[4] % 3) for _, _, h in diffs if h[0] == 0 and h[1] == 0 and h[2] % 3 == 0})

    zuv4 = extract_zuv_mod3(d_w4["diffs"])
    zuv5 = extract_zuv_mod3(d_w5["diffs"])
    assert zuv4 == [(3, 1, 1)] and zuv5 == [(3, 2, 2)]

    uncovered_v = []
    for D in range(3):
        for E in range(3):
            if (D, E) == (0, 0):
                continue
            for C3 in range(3):
                ok4 = all((((z // 3) % 3) * C3 + um * D + vm * E) % 3 != 0 for z, um, vm in zuv4)
                ok5 = all((((z // 3) % 3) * C3 + um * D + vm * E) % 3 != 0 for z, um, vm in zuv5)
                if not (ok4 or ok5):
                    uncovered_v.append([D, E, C3])
    assert uncovered_v == [[1, 2, 0], [2, 1, 0]]

    def extract_crit_forms(diffs):
        forms = set()
        for _, _, h in diffs:
            if h[0] % 3 == 0 and h[1] % 3 == 0:
                assert (h[0], h[1]) == (0, 0)
                if h[2] % 3 == 0 and (h[3] - h[4]) % 3 == 0:
                    forms.add(((h[2] // 3) % 3, h[4] % 3, (h[5] - h[6] + h[7]) % 3))
        return sorted(forms)

    f4 = extract_crit_forms(d_w4["diffs"])
    f5 = extract_crit_forms(d_w5["diffs"])
    assert f4 == [(1, 1, 0)] and f5 == [(1, 2, 2)]

    uncovered_w = []
    for mu in range(3):
        for lam in range(3):
            ok4 = all((z3 * mu + vm * lam + rst) % 3 != 0 for z3, vm, rst in f4)
            ok5 = all((z3 * mu + vm * lam + rst) % 3 != 0 for z3, vm, rst in f5)
            if not (ok4 or ok5):
                uncovered_w.append([mu, lam])
    assert uncovered_w == [[2, 1]]

    w0_nz = sorted({(h[0], h[1]) for _, _, h in d_w0["diffs"] if h[0] % 3 == 0 and h[1] % 3 == 0 and (h[0], h[1]) != (0, 0)})
    w0s_nz = sorted({(h[0], h[1]) for _, _, h in d_w0s["diffs"] if h[0] % 3 == 0 and h[1] % 3 == 0 and (h[0], h[1]) != (0, 0)})
    assert w0_nz == [(-3, 0), (3, 0)] and w0s_nz == [(0, -3), (0, 3)]
    assert all(proj_crit(tuple(h), 2, 1) != (0, 0, 0, 0, 0) for _, _, h in d_w0["diffs"] if h[0] == 0 and h[1] == 0)
    assert all(proj_crit(tuple(h), 2, 1) != (0, 0, 0, 0, 0) for _, _, h in d_w0s["diffs"] if h[0] == 0 and h[1] == 0)

    # 3. G_crit(alpha, beta) family, 0/288 free-class-4 32-word test in G_crit(0,0), and controls
    def eval_word_gcrit(word: str, alpha: int, beta: int) -> bool:
        cur = (0, 0, 0, 0, 0)
        ev, od = set(), set()
        for i, ch in enumerate(word):
            if i % 2 == 0:
                ev.add(cur)
                if ch == "1":
                    cur = reduce_gcrit(step_a_crit(cur), alpha, beta)
                elif ch == "2":
                    cur = reduce_gcrit(step_b_crit(cur), alpha, beta)
            else:
                od.add(cur)
                if ch == "1":
                    cur = reduce_gcrit(step_a_inv_crit(cur), alpha, beta)
                elif ch == "2":
                    cur = reduce_gcrit(step_b_inv_crit(cur), alpha, beta)
        return cur == (0, 0, 0, 0, 0) and len(ev) == len(word) // 2 and len(od) == len(word) // 2

    assert len(W64_CRIT00) == 64 and all(W64_CRIT00[i] != W64_CRIT00[(i + 1) % 64] for i in range(64))
    end64, _ = fn4.walk(W64_CRIT00)
    assert fn4.collect(end64) == [0] * 8

    gcrit_results = {}
    for a in range(3):
        for b in range(3):
            ok_w0 = eval_word_gcrit(W0_CRIT, a, b)
            ok_w0s = eval_word_gcrit(W0_CRIT_SWAP, a, b)
            ok_64 = eval_word_gcrit(W64_CRIT00, a, b)
            if a != 0:
                assert ok_w0
            elif b != 0:
                assert ok_w0s
            else:
                assert (not ok_w0) and (not ok_w0s)
            assert ok_64
            gcrit_results[f"({a},{b})"] = {
                "W0_simple": ok_w0,
                "W0_swap_simple": ok_w0s,
                "W64_crit00_simple": ok_64,
            }

    elems00 = [(x, y, z, u, w) for x in range(3) for y in range(3) for z in range(3) for u in range(3) for w in range(3)]
    idx00 = {g: i for i, g in enumerate(elems00)}
    adj00: list[list[int]] = [[] for _ in range(486)]
    edge_col = {}
    for i, g in enumerate(elems00):
        t0 = idx00[g]
        t1 = idx00[reduce_gcrit(step_a_crit(g), 0, 0)]
        t2 = idx00[reduce_gcrit(step_b_crit(g), 0, 0)]
        for col, tv in enumerate((t0, t1, t2)):
            v = 243 + tv
            adj00[i].append(v)
            adj00[v].append(i)
            edge_col[(i, v)] = str(col)
            edge_col[(v, i)] = str(col)

    def find_cycles_and_balanced(length: int) -> tuple[bool, str | None]:
        half = length // 2
        branches: list[dict[int, list[tuple[int, list[int]]]]] = [defaultdict(list) for _ in range(3)]
        for br, first in enumerate(adj00[0]):
            def dfs(u: int, dep: int, msk: int, path: list[int]) -> None:
                if dep == half:
                    branches[br][u].append((msk, path))
                    return
                m2 = msk | (1 << u)
                for w in adj00[u]:
                    if w != 0 and not ((m2 >> w) & 1):
                        dfs(w, dep + 1, m2, path + [w])
            dfs(first, 1, 0, [0, first])

        any_cyc = False
        for b1 in range(3):
            for b2 in range(b1 + 1, 3):
                for tgt in set(branches[b1]) & set(branches[b2]):
                    for m1, p1 in branches[b1][tgt]:
                        for m2, p2 in branches[b2][tgt]:
                            if (m1 & m2) == 0:
                                any_cyc = True
                                cyc = p1 + p2[-2:0:-1]
                                w_str = "".join(edge_col[(cyc[k], cyc[(k + 1) % length])] for k in range(length))
                                sx = sum((1 if i % 2 == 0 else -1) for i, ch in enumerate(w_str) if ch == "1")
                                sy = sum((1 if i % 2 == 0 else -1) for i, ch in enumerate(w_str) if ch == "2")
                                if sx == 0 and sy == 0:
                                    return True, w_str
        return any_cyc, None

    free_32_count = 0
    free_32_hits_in_00 = 0
    bkt_half: dict[tuple[int, ...], list[tuple[int, int, str]]] = defaultdict(list)

    def walk16_dfs(dep: int, st: tuple[int, ...], fc: int, lc: int, chars: list[str]) -> None:
        if dep == 16:
            bkt_half[st].append((fc, lc, "".join(chars)))
            return
        for c in (0, 1, 2):
            if c != lc:
                if dep % 2 == 0:
                    nxt = st if c == 0 else (mul_a_free(st) if c == 1 else mul_b_free(st))
                else:
                    if c == 0:
                        nxt = st
                    elif c == 1:
                        x, y, z, u, v, r, s, t = st
                        zp = z + y
                        up = u - zp
                        vp = v + comb2(y)
                        nxt = (x - 1, y, zp, up, vp, r - up, s - vp, t + comb3(y))
                    else:
                        x, y, z, u, v, r, s, t = st
                        nxt = (x, y - 1, z, u, v - z, r, s - u, t - v + z)
                walk16_dfs(dep + 1, nxt, fc, c, chars + [str(c)])

    zero8 = (0,) * 8
    for c0 in (0, 1, 2):
        s1 = zero8 if c0 == 0 else (mul_a_free(zero8) if c0 == 1 else mul_b_free(zero8))
        walk16_dfs(1, s1, c0, c0, [str(c0)])

    for items in bkt_half.values():
        for i in range(len(items)):
            fc1, lc1, s1 = items[i]
            for j in range(i + 1, len(items)):
                fc2, lc2, s2 = items[j]
                if fc1 != fc2 and lc1 != lc2:
                    free_32_count += 1
                    if eval_word_gcrit(s1 + s2[::-1], 0, 0):
                        free_32_hits_in_00 += 1
    assert free_32_count == 288 and free_32_hits_in_00 == 0

    has16_00, bal16_00 = find_cycles_and_balanced(16)
    has32_00, bal32_00 = find_cycles_and_balanced(32)
    assert bal32_00 is not None and len(bal32_00) == 32

    def eval_word_group(word: str, id_g, A, B, mul, inv) -> bool:
        sh = (id_g, A, B)
        iv = (id_g, inv(A), inv(B))
        cur = id_g
        ev, od = set(), set()
        for i, ch in enumerate(word):
            if i % 2 == 0:
                ev.add(cur)
                cur = mul(cur, sh[int(ch)])
            else:
                od.add(cur)
                cur = mul(cur, iv[int(ch)])
        return cur == id_g and len(ev) == len(word) // 2 and len(od) == len(word) // 2

    def ut5_mul_mod3(X, Y):
        a12, a13, a14, a15, a23, a24, a25, a34, a35, a45 = X
        b12, b13, b14, b15, b23, b24, b25, b34, b35, b45 = Y
        return (
            (a12 + b12) % 3,
            (a13 + a12 * b23 + b13) % 3,
            (a14 + a12 * b24 + a13 * b34 + b14) % 3,
            (a15 + a12 * b25 + a13 * b35 + a14 * b45 + b15) % 3,
            (a23 + b23) % 3,
            (a24 + a23 * b34 + b24) % 3,
            (a25 + a23 * b35 + a24 * b45 + b25) % 3,
            (a34 + b34) % 3,
            (a35 + a34 * b45 + b35) % 3,
            (a45 + b45) % 3,
        )

    def ut5_inv_mod3(X):
        c = (0,) * 10
        for _ in range(9):
            n = ut5_mul_mod3(c, X)
            if n == (0,) * 10:
                return c
            c = n
        raise RuntimeError("bad ut5 inverse")

    def mat_e(pairs):
        idx_map = {(1, 2): 0, (1, 3): 1, (1, 4): 2, (1, 5): 3, (2, 3): 4, (2, 4): 5, (2, 5): 6, (3, 4): 7, (3, 5): 8, (4, 5): 9}
        arr = [0] * 10
        for k, v in pairs.items():
            arr[idx_map[k]] = v % 3
        return tuple(arr)

    A_cs = mat_e({(1, 2): 1, (3, 4): 1})
    B_cs = mat_e({(2, 3): 1, (4, 5): 1})
    A_ma = mat_e({(1, 2): 1, (3, 4): 2, (4, 5): 1})
    B_ma = mat_e({(2, 3): 1, (3, 4): 1, (4, 5): 1})
    ut5_word_hits = {}
    for nm, AA, BB in [("ut5_chain_step", A_cs, B_cs), ("ut5_minimal_alt", A_ma, B_ma)]:
        hits = [
            wname for wname, ww in [("W4", W4_UNCOND), ("W5", W5_UNCOND), ("W0", W0_CRIT), ("W0_SWAP", W0_CRIT_SWAP), ("W64_CRIT00", W64_CRIT00)]
            if eval_word_group(ww, (0,) * 10, AA, BB, ut5_mul_mod3, ut5_inv_mod3)
        ]
        assert len(hits) >= 1, f"{nm} failed all words!"
        ut5_word_hits[nm] = hits

    def trace_in_gcrit00_x_c5(word: str) -> bool:
        c0 = (0, 0, 0, 0, 0)
        c5 = 0
        ev, od = set(), set()
        for i, ch in enumerate(word):
            st = (c0, c5)
            if i % 2 == 0:
                ev.add(st)
                if ch == "1":
                    c0 = reduce_gcrit(step_a_crit(c0), 0, 0)
                    c5 = (c5 + 1) % 5
                elif ch == "2":
                    c0 = reduce_gcrit(step_b_crit(c0), 0, 0)
                    c5 = (c5 + 2) % 5
            else:
                od.add(st)
                if ch == "1":
                    c0 = reduce_gcrit(step_a_inv_crit(c0), 0, 0)
                    c5 = (c5 - 1) % 5
                elif ch == "2":
                    c0 = reduce_gcrit(step_b_inv_crit(c0), 0, 0)
                    c5 = (c5 - 2) % 5
        return (c0, c5) == ((0, 0, 0, 0, 0), 0) and len(ev) == len(word) // 2 and len(od) == len(word) // 2

    assert trace_in_gcrit00_x_c5(bal32_00) and trace_in_gcrit00_x_c5(W64_CRIT00)
    w64_x = sum((1 if i % 2 == 0 else -1) for i, ch in enumerate(W64_CRIT00) if ch == "1")
    w64_y = sum((1 if i % 2 == 0 else -1) for i, ch in enumerate(W64_CRIT00) if ch == "2")
    assert w64_x == 0 and w64_y == 0

    return {
        "free_class4_identities": {
            "gamma2_abelian": True,
            "comm_a3_b": [0, 0, 3, 3, 0, 1, 0, 0],
            "comm_a_b3": [0, 0, 3, 0, 3, 0, 0, 1],
            "polynomial_mul_and_qcrit_exact": True,
        },
        "pge5_and_p3_reduction": {
            "W4": W4_UNCOND,
            "W5": W5_UNCOND,
            "W4_ab_gcd": d_w4["ab_gcd_hist"],
            "W4_zero_ab_z_values": w4_zero_ab_zs,
            "pge5_sharp_C32_verified": True,
            "p3_V_uncovered_pairs": uncovered_v,
            "p3_W_uncovered_mu_lam": uncovered_w,
            "W0": W0_CRIT,
            "W0_swap": W0_CRIT_SWAP,
            "W0_nonzero_mod3_xy": [list(p) for p in w0_nz],
            "W0_swap_nonzero_mod3_xy": [list(p) for p in w0s_nz],
            "W0_and_swap_Qcrit_2_1_zero_collisions": True,
        },
        "gcrit_and_controls": {
            "W64_CRIT00": W64_CRIT00,
            "W64_CRIT00_free_class4_closure": True,
            "W64_CRIT00_Z2_balanced": True,
            "free_class4_32words_total": free_32_count,
            "free_class4_32words_simple_in_Gcrit00": free_32_hits_in_00,
            "all_9_Gcrit_results": gcrit_results,
            "Gcrit_0_0_has_C16": has16_00,
            "Gcrit_0_0_balanced_C16": bal16_00,
            "Gcrit_0_0_has_C32": has32_00,
            "Gcrit_0_0_balanced_C32": bal32_00,
            "Gcrit00_x_C5_order1215_C32_and_C64_verified": True,
            "ut5_f3_hits": ut5_word_hits,
        },
    }


def verify_class6_and_deg6() -> dict:
    """Verify length-32 class-5 barrier (0/288), deg-6 closure of WORDS64_CLASS4,
    universal {1: 992} all-prime (Z/p^k Z)<X,Y>/(X,Y)^7 C64 certificate,
    and physical class-6 / mixed-class matrix controls (UT_7(F_5) exp 25).
    """
    def comb2(n: int) -> int:
        return n * (n - 1) // 2

    def comb3(n: int) -> int:
        return n * (n - 1) * (n - 2) // 6

    def mul_a_free(h):
        x, y, z, u, v, r, s, t = h
        return (x + 1, y, z - y, u + z, v - comb2(y), r + u, s + v, t - comb3(y))

    def mul_b_free(h):
        x, y, z, u, v, r, s, t = h
        return (x, y + 1, z, u, v + z, r, s + u, t + v)

    def mul_a_inv(h):
        x, y, z, u, v, r, s, t = h
        zp = z + y; up = u - zp; vp = v + comb2(y)
        return (x - 1, y, zp, up, vp, r - up, s - vp, t + comb3(y))

    def mul_b_inv(h):
        x, y, z, u, v, r, s, t = h
        return (x, y - 1, z, u, v - z, r, s - u, t - v + z)

    bkt: dict[tuple[int, ...], list[tuple[int, int, str]]] = defaultdict(list)

    def dfs32(dep: int, st: tuple[int, ...], fc: int, lc: int, chars: list[str]) -> None:
        if dep == 16:
            bkt[st].append((fc, lc, "".join(chars)))
            return
        for c in (0, 1, 2):
            if c == lc:
                continue
            if dep % 2 == 0:
                nxt = st if c == 0 else (mul_a_free(st) if c == 1 else mul_b_free(st))
            else:
                nxt = st if c == 0 else (mul_a_inv(st) if c == 1 else mul_b_inv(st))
            dfs32(dep + 1, nxt, fc, c, chars + [str(c)])

    z8 = (0,) * 8
    for c0 in (0, 1, 2):
        s1 = z8 if c0 == 0 else (mul_a_free(z8) if c0 == 1 else mul_b_free(z8))
        dfs32(1, s1, c0, c0, [str(c0)])

    words32 = []
    for items in bkt.values():
        for i in range(len(items)):
            fc1, lc1, s1 = items[i]
            for j in range(i + 1, len(items)):
                fc2, lc2, s2 = items[j]
                if fc1 != fc2 and lc1 != lc2:
                    words32.append(s1 + s2[::-1])
    assert len(words32) == 288 and len(set(words32)) == 288

    def m_walk(word: str, deg: int):
        ident = {"": 1}
        sh = {"0": ident, "1": {"": 1, "x": 1}, "2": {"": 1, "y": 1}}
        iv = {"0": ident, "1": magnus_inv(sh["1"], deg), "2": magnus_inv(sh["2"], deg)}
        cur = ident
        states = []
        for i, ch in enumerate(word):
            states.append(cur)
            cur = magnus_mul(cur, sh[ch] if i % 2 == 0 else iv[ch], deg)
        return cur, states

    closes_deg5 = 0
    for w in words32:
        end5, _ = m_walk(w, 5)
        if end5 == {"": 1}:
            closes_deg5 += 1
    assert closes_deg5 == 0

    deg7_counts = {}
    w0_deg6_hist = None
    for idx, w in enumerate(WORDS64_CLASS4):
        end7, states7 = m_walk(w, 7)
        end6 = {k: v for k, v in end7.items() if len(k) <= 6}
        assert end6 == {"": 1}
        deg7_counts[f"w64_{idx + 1}"] = sum(1 for k in end7 if len(k) == 7)
        states6 = [{k: v for k, v in s.items() if len(k) <= 6} for s in states7]
        inv6 = [magnus_inv(s, 6) for s in states6]
        hist6 = Counter()
        for i in range(64):
            for j in range(i + 2, 64, 2):
                d = magnus_mul(inv6[i], states6[j], 6)
                hist6[gcd(*(abs(v) for k, v in d.items() if k))] += 1
        assert sum(hist6.values()) == 992 and 0 not in hist6
        if idx == 0:
            assert dict(hist6) == {1: 992}
            w0_deg6_hist = dict(sorted(hist6.items()))

    def trunc6_mul(a, b, mod):
        out = defaultdict(int)
        for u, cu in a.items():
            lu = len(u)
            for v, cv in b.items():
                if lu + len(v) <= 6:
                    out[u + v] += cu * cv
        return {k: c % mod for k, c in out.items() if c % mod}

    def trunc6_inv(x, mod):
        u = {k: v for k, v in x.items() if k}
        res = {(): 1}; pwr = dict(u)
        for k in range(1, 7):
            sgn = -1 if k % 2 else 1
            for m, c in pwr.items():
                res[m] = (res.get(m, 0) + sgn * c) % mod
            if k < 6:
                pwr = trunc6_mul(pwr, u, mod)
        return {k: v % mod for k, v in res.items() if v % mod}

    gx, gy = {(): 1, (0,): 1}, {(): 1, (1,): 1}
    monos6 = [m for d in range(1, 7) for m in product(range(2), repeat=d)]
    alg6_controls = []
    w0 = WORDS64_CLASS4[0]
    for p in (2, 3, 5):
        for mod in (p, p * p):
            sh = ({(): 1}, gx, gy)
            iv = ({(): 1}, trunc6_inv(gx, mod), trunc6_inv(gy, mod))
            st = {(): 1}; vs = []
            for i, ch in enumerate(w0):
                vs.append(st)
                st = trunc6_mul(st, sh[int(ch)] if i % 2 == 0 else iv[int(ch)], mod)
            assert st == {(): 1}
            for par in (0, 1):
                verts = vs[par::2]
                assert all(any((a.get(m, 0) - b.get(m, 0)) % mod for m in monos6) for a, b in combinations(verts, 2))
        cur = gx; ord_p2 = 1
        while cur != {(): 1}:
            nxt = {(): 1}
            for _ in range(p):
                nxt = trunc6_mul(nxt, cur, p * p)
            cur = nxt; ord_p2 *= p
        alg6_controls.append({"p": p, "mod_p2": p * p, "ord_1_plus_X_in_deg6": ord_p2, "word0_simple_C64": True})

    # Physical controls: UT_7(F_5) (order 5^21, class 6, exp 25) & G_crit(0,0) x UT_7(F_5)
    id7 = (0,) * 21

    def ut7_mul(X, Y, mod=5):
        M = [[0] * 7 for _ in range(7)]; N = [[0] * 7 for _ in range(7)]
        idx = 0
        for i in range(7):
            M[i][i] = 1; N[i][i] = 1
            for j in range(i + 1, 7):
                M[i][j] = X[idx]; N[i][j] = Y[idx]; idx += 1
        out = []
        for i in range(7):
            for j in range(i + 1, 7):
                s = N[i][j] + M[i][j]
                for k in range(i + 1, j):
                    s += M[i][k] * N[k][j]
                out.append(s % mod)
        return tuple(out)

    def ut7_pow(X, k, mod=5):
        r = id7; b = X
        while k:
            if k & 1: r = ut7_mul(r, b, mod)
            b = ut7_mul(b, b, mod); k >>= 1
        return r

    def ut7_comm(X, Y, mod=5):
        return ut7_mul(ut7_mul(ut7_pow(X, 24, mod), ut7_pow(Y, 24, mod), mod), ut7_mul(X, Y, mod), mod)

    def make_ut7(entries):
        arr = [0] * 21; idx = 0
        for i in range(7):
            for j in range(i + 1, 7):
                arr[idx] = entries.get((i, j), 0) % 5; idx += 1
        return tuple(arr)

    A7 = make_ut7({(0, 1): 1, (1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 5): 1, (5, 6): 1})
    B7 = make_ut7({(0, 1): 1, (2, 3): 2, (4, 5): 1})
    assert ut7_pow(A7, 5) != id7 and ut7_pow(A7, 25) == id7
    c5 = ut7_comm(ut7_comm(ut7_comm(ut7_comm(ut7_comm(A7, B7), A7), A7), A7), A7)
    assert c5 != id7 and ut7_comm(c5, A7) == id7

    def proj_crit(h):
        x, y, z, u, v, r, s, t = h
        qz, rem_z = divmod(z, 3)
        return (x % 3, y % 3, rem_z, (u - v) % 3, (2 * qz + v + r - s + t) % 3)

    def g00_step(st, ch, pos):
        if ch == "0": return st
        x, y, z0, u0, w0 = st
        if pos and ch == "1": h = (x + 1, y, z0 - y, u0 + z0, -comb2(y), w0 + u0, 0, -comb3(y))
        elif pos and ch == "2": h = (x, y + 1, z0, u0, z0, w0, u0, 0)
        elif (not pos) and ch == "1":
            zp = z0 + y; up = u0 - zp; vp = comb2(y)
            h = (x - 1, y, zp, up, vp, w0 - up, -vp, comb3(y))
        else: h = (x, y - 1, z0, u0, -z0, w0, -u0, z0)
        return proj_crit(h)

    sh7 = (id7, A7, B7); iv7 = (id7, ut7_pow(A7, 24), ut7_pow(B7, 24))
    ut7_hits = []; mixed_hits = []
    for k, w in enumerate(WORDS64_CLASS4):
        c3 = (0, 0, 0, 0, 0); c5_s = id7; ev, od = set(), set()
        for i, ch in enumerate(w):
            st = (c3, c5_s)
            if i % 2 == 0:
                ev.add(st); c3 = g00_step(c3, ch, True); c5_s = ut7_mul(c5_s, sh7[int(ch)])
            else:
                od.add(st); c3 = g00_step(c3, ch, False); c5_s = ut7_mul(c5_s, iv7[int(ch)])
        if (c3, c5_s) == ((0, 0, 0, 0, 0), id7) and len(ev) == 32 and len(od) == 32:
            ut7_hits.append(f"w64_{k + 1}")
            mixed_hits.append(f"w64_{k + 1}")
    assert len(ut7_hits) == 3 and len(mixed_hits) == 3

    return {
        "length32_class5_barrier": {"free_class4_32words_checked": 288, "closes_in_deg5": closes_deg5},
        "deg6_magnus_closure": {"all_three_close_deg6": True, "deg7_nonzero_monomial_counts": deg7_counts, "word0_deg6_integral_gcd_hist": w0_deg6_hist},
        "literal_mod_p_p2_deg6_controls": alg6_controls,
        "ut7_f5_order_5pow21_exp25_class6_hits": ut7_hits,
        "mixed_Gcrit00_x_ut7f5_hits": mixed_hits,
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    fn4 = FreeNilpotentClass4()
    cert_payload = {
        "paper": "Paper I: Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Six",
        "status": "PASS",
        "abelian": verify_abelian_haar(),
        "class2": verify_class2_haar(),
        "class3": verify_class3_theorems(fn4),
        "class4": verify_class4_theorems(fn4),
        "unconditional_class4": verify_unconditional_class4(fn4),
        "class6_and_deg6": verify_class6_and_deg6(),
        "boundary_controls": verify_boundary_controls(),
    }
    serialized = json.dumps(cert_payload, indent=2) + "\n"
    if write_certs:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(serialized, encoding="utf-8")
    elif CERT_PATH.exists():
        assert CERT_PATH.read_text(encoding="utf-8") == serialized, "Certificate byte-for-byte mismatch!"
        saved = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        current = json.loads(serialized)
        for k in ("abelian", "class2", "class3", "class4", "unconditional_class4", "class6_and_deg6", "boundary_controls"):
            assert saved[k] == current[k], f"Certificate mismatch in section {k}"
    out = dict(cert_payload)
    out["elapsed_seconds"] = round(time.monotonic() - t0, 3)
    return out


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
        "unconditional_pge5_sharp_C32": out["unconditional_class4"]["pge5_and_p3_reduction"]["pge5_sharp_C32_verified"],
        "unconditional_Gcrit00_balanced_C32": out["unconditional_class4"]["gcrit_and_controls"]["Gcrit_0_0_balanced_C32"],
        "class5_32words_closing": out["class6_and_deg6"]["length32_class5_barrier"]["closes_in_deg5"],
        "deg6_w0_gcd_hist": out["class6_and_deg6"]["deg6_magnus_closure"]["word0_deg6_integral_gcd_hist"],
        "ut7_f5_c64_hits": out["class6_and_deg6"]["ut7_f5_order_5pow21_exp25_class6_hits"],
        "ut4_words_checked": out["boundary_controls"]["ut4_girth14_words_checked"],
        "ut6_words_checked": out["boundary_controls"]["ut6_girth18_words_checked"],
    }, indent=2))
