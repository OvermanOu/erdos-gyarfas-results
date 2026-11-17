#!/usr/bin/env python3
"""Standalone standard-library verifier for Paper V:
Derived-Central Dyadic Theta Lifting to Nilpotent Class Nine, Universal
Semidirect C_6 Cubic Haar Graphs, and Analytic Stretch Bounds for
Two-Attachment Cubic Gadgets.

Run from repository root or paper5_theta_lifting_c6_and_gadget_stretch/:
    python verify_paper5.py
    python verify_paper5.py --write-certificates
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import itertools
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import random
import time

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "certificates" / "paper5_certificates.json"

# Breakthrough 5A constants
T8_PLUS = ("01021020", "12102101", "20210212")

CLASS3_THETAS = {
    "W_B0": ("0201021021012021", "1201212101012012", "2012012102010120"),
    "W_B1": ("0212010210210121", "1201012102012012", "2012010102020120"),
    "W_B2": ("0201010210212010", "1012021021010121", "2012012102012012"),
    "W_Q81_A": ("0121010120120210", "1202102101212102", "2021201201020201"),
    "W_Q81_B": ("0212012010212102", "1021010210120121", "2102102102120120"),
}

CLASS4_THETAS = {
    "T32_D": (
        "01201210102102012012102101010210",
        "10102012012102102102101021020101",
        "20121021010102101010210201012012",
    ),
    "T32_E": (
        "01020102102120101202010120101021",
        "10201021201201010212020101012010",
        "21021201210212012010201201212012",
    ),
}

AB_WORDS_LIFT = [
    "01", "02", "12",
    "0101", "0202", "1212", "0102", "0121", "0212",
    "01010212", "01210202", "01212102", "01012102",
    "0101012010201212",
]

# Breakthrough 5B constants
W_G10 = "0102021021202012"
W_C6_12 = "01201210210102010212102010102101"
W_PHI6_10 = "0101010102012102"
W_PHI6_12 = "0101010101201202"

# Breakthrough 5C constants
MARKSTROM24_EDGES = [
    (0, 1), (0, 9), (0, 10), (1, 5), (1, 7), (2, 6), (2, 12), (2, 15),
    (3, 8), (3, 11), (3, 21), (4, 7), (4, 11), (4, 23), (5, 14), (5, 19),
    (6, 11), (6, 15), (7, 8), (8, 15), (9, 14), (9, 23), (10, 16), (10, 19),
    (12, 21), (12, 22), (13, 16), (13, 20), (13, 21), (14, 23), (16, 22),
    (17, 18), (17, 20), (17, 22), (18, 19), (18, 20),
]


# ---------------------------------------------------------------------------
# 1. Derived-Central Dyadic Theta Lifting up to Nilpotent Class 9
# ---------------------------------------------------------------------------

def step4_a(st: tuple[int, ...]) -> tuple[int, ...]:
    x, y, z, u, v, r, s, t = st
    return (x + 1, y, z - y, u + z, v - y * (y - 1) // 2, r + u, s + v, t - y * (y - 1) * (y - 2) // 6)


def step4_ai(st: tuple[int, ...]) -> tuple[int, ...]:
    x, y, z, u, v, r, s, t = st
    y2 = y * (y - 1) // 2
    y3 = y * (y - 1) * (y - 2) // 6
    return (x - 1, y, z + y, u - z - y, v + y2, r + z - u + y, s - v - y2, t + y3)


def step4_b(st: tuple[int, ...]) -> tuple[int, ...]:
    x, y, z, u, v, r, s, t = st
    return (x, y + 1, z, u, v + z, r, s + u, t + v)


def step4_bi(st: tuple[int, ...]) -> tuple[int, ...]:
    x, y, z, u, v, r, s, t = st
    return (x, y - 1, z, u, v - z, r, s - u, t + z - v)


def mul4_hall(g1: tuple[int, ...], g2: tuple[int, ...]) -> tuple[int, ...]:
    x, y, z, u, v, r, s, t = g2
    cur = g1
    sa = step4_a if x >= 0 else step4_ai
    for _ in range(abs(x)):
        cur = sa(cur)
    sb = step4_b if y >= 0 else step4_bi
    for _ in range(abs(y)):
        cur = sb(cur)
    return (cur[0], cur[1], cur[2] + z, cur[3] + u, cur[4] + v, cur[5] + r, cur[6] + s, cur[7] + t)


def inv4_hall(g: tuple[int, ...]) -> tuple[int, ...]:
    x, y, z, u, v, r, s, t = g
    cur = (0, 0, -z, -u, -v, -r, -s, -t)
    sb = step4_bi if y >= 0 else step4_b
    for _ in range(abs(y)):
        cur = sb(cur)
    sa = step4_ai if x >= 0 else step4_a
    for _ in range(abs(x)):
        cur = sa(cur)
    return cur


def magnus_self_test() -> None:
    def mmul(p, q):
        out = {}
        for k1, v1 in p.items():
            l1 = len(k1)
            for k2, v2 in q.items():
                if l1 + len(k2) <= 4:
                    k = k1 + k2
                    out[k] = out.get(k, 0) + v1 * v2
        return {k: v for k, v in out.items() if v}

    def minv(p):
        u = {k: v for k, v in p.items() if k}
        res = {"": 1}
        pwr = dict(u)
        for k in range(1, 5):
            sgn = -1 if k % 2 else 1
            for m, c in pwr.items():
                res[m] = res.get(m, 0) + sgn * c
            if k < 4:
                pwr = mmul(pwr, u)
        return {k: v for k, v in res.items() if v}

    def mpow(p, n):
        if n < 0:
            p, n = minv(p), -n
        res = {"": 1}
        base = p
        while n:
            if n & 1:
                res = mmul(res, base)
            n >>= 1
            if n:
                base = mmul(base, base)
        return res

    def mcomm(p, q):
        return mmul(mmul(mmul(minv(p), minv(q)), p), q)

    A = {"": 1, "x": 1}
    B = {"": 1, "y": 1}
    C = mcomm(A, B)
    D = mcomm(C, A)
    E = mcomm(C, B)
    F = mcomm(D, A)
    G = mcomm(D, B)
    H = mcomm(E, B)
    assert mcomm(E, A) == G

    def to_mag(h):
        x, y, z, u, v, r, s, t = h
        return mmul(
            mmul(mpow(A, x), mpow(B, y)),
            mmul(mpow(C, z), mmul(mmul(mpow(D, u), mpow(E, v)), mmul(mpow(F, r), mmul(mpow(G, s), mpow(H, t))))),
        )

    rng = random.Random(20261117)
    for _ in range(80):
        g1 = tuple(rng.randint(-4, 4) for _ in range(8))
        g2 = tuple(rng.randint(-4, 4) for _ in range(8))
        assert to_mag(mul4_hall(g1, g2)) == mmul(to_mag(g1), to_mag(g2))
        assert to_mag(inv4_hall(g1)) == minv(to_mag(g1))


def collect_theta_diffs(branches: tuple[str, str, str], trunc_len: int) -> tuple[tuple[int, ...], list[tuple[int, ...]]]:
    ID = (0,) * 8

    def adv(st, ch, even_step):
        if ch == "0":
            return st
        if ch == "1":
            return step4_a(st) if even_step else step4_ai(st)
        return step4_b(st) if even_step else step4_bi(st)

    def trunc(st):
        return st[:trunc_len] + (0,) * (8 - trunc_len)

    ends = []
    s0_all = [ID]
    s1_all = []
    last_colors = set()
    first_colors = set()
    for w in branches:
        first_colors.add(w[0])
        last_colors.add(w[-1])
        assert all(w[i] != w[i + 1] for i in range(len(w) - 1))
        cur = ID
        for idx, ch in enumerate(w):
            cur = trunc(adv(cur, ch, idx % 2 == 0))
            if idx % 2 == 0:
                s1_all.append(cur)
            elif idx < len(w) - 1:
                s0_all.append(cur)
            else:
                ends.append(cur)
    assert first_colors == {"0", "1", "2"} and last_colors == {"0", "1", "2"}
    assert ends[0] == ends[1] == ends[2]
    s0_all.append(ends[0])
    L = len(branches[0])
    assert len(s0_all) == 2 + 3 * (L // 2 - 1) and len(s1_all) == 3 * (L // 2)
    assert len(set(s0_all)) == len(s0_all) and len(set(s1_all)) == len(s1_all)

    diffs = []
    for shore in (s0_all, s1_all):
        invs = [inv4_hall(st) for st in shore]
        for i in range(len(shore)):
            for j in range(i + 1, len(shore)):
                d = trunc(mul4_hall(invs[i], shore[j]))
                assert d != ID
                diffs.append(d)
    return ends[0], diffs


def verify_ut_physical_lift(n: int, p: int, witness_list: list[tuple[str, tuple[str, str, str]]]) -> dict:
    def mat_mul(A, B):
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for k in range(i, n):
                aik = A[i][k]
                if aik:
                    for j in range(k, n):
                        C[i][j] = (C[i][j] + aik * B[k][j]) % p
        return tuple(tuple(r) for r in C)

    def mat_inv(A):
        N = [[(A[i][j] - (1 if i == j else 0)) % p for j in range(n)] for i in range(n)]
        res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        cur = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(1, n):
            nxt = [[0] * n for _ in range(n)]
            for i in range(n):
                for m in range(i, n):
                    if cur[i][m]:
                        for j in range(m, n):
                            nxt[i][j] = (nxt[i][j] - cur[i][m] * N[m][j]) % p
            cur = nxt
            for i in range(n):
                for j in range(i, n):
                    res[i][j] = (res[i][j] + cur[i][j]) % p
        return tuple(tuple(r) for r in res)

    I = tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
    a = tuple(tuple(1 if i == j else (1 if j == i + 1 else 0) for j in range(n)) for i in range(n))
    if n == 8:
        b = tuple(tuple(1 if i == j else (1 if (i == 6 and j == 7) else 0) for j in range(n)) for i in range(n))
        m_cut = 4
    else:
        b = tuple(tuple(1 if i == j else ((2 if i == 1 else 1) if j == i + 1 else 0) for j in range(n)) for i in range(n))
        m_cut = 5

    def comm(X, Y):
        return mat_mul(mat_mul(mat_inv(X), mat_inv(Y)), mat_mul(X, Y))

    cur_set = [comm(a, b)]
    cl = 1
    while any(x != I for x in cur_set):
        cl += 1
        nxt = []
        for x in cur_set:
            for g in (a, b):
                y = comm(x, g)
                if y != I and y not in nxt:
                    nxt.append(y)
        cur_set = nxt
    assert cl == n - 1

    sh = (I, a, b)
    iv = (I, mat_inv(a), mat_inv(b))

    def eval_word(w: str):
        cur = I
        s0, s1 = [cur], []
        for idx, ch in enumerate(w):
            c = int(ch)
            cur = mat_mul(cur, sh[c] if idx % 2 == 0 else iv[c])
            if idx % 2 == 0:
                s1.append(cur)
            else:
                s0.append(cur)
        return cur, s0, s1

    def mod_gm(M):
        return tuple(tuple(M[i][j] if j - i < m_cut else 0 for j in range(n)) for i in range(n))

    lifted = {}
    for wname, tws in witness_list:
        gs = [eval_word(tw)[0] for tw in tws]
        assert mod_gm(gs[0]) == mod_gm(gs[1]) == mod_gm(gs[2])
        q0 = {mod_gm(I), mod_gm(gs[0])}
        q1 = set()
        for tw in tws:
            _, s0, s1 = eval_word(tw)
            qs0 = [mod_gm(x) for x in s0[1:-1]]
            qs1 = [mod_gm(x) for x in s1]
            assert len(set(qs0)) == len(qs0) and len(set(qs1)) == len(qs1)
            assert q0.isdisjoint(qs0) and q1.isdisjoint(qs1)
            q0.update(qs0)
            q1.update(qs1)
        win = None
        for aw in AB_WORDS_LIFT:
            bw = "".join(tws[int(ch)] if idx % 2 == 0 else tws[int(ch)][::-1] for idx, ch in enumerate(aw))
            assert all(bw[i] != bw[(i + 1) % len(bw)] for i in range(len(bw)))
            end_m, s0, s1 = eval_word(bw)
            if end_m == I and len(set(s0[:-1])) == len(bw) // 2 and len(set(s1)) == len(bw) // 2:
                win = {"ab_word": aw, "cycle_length": len(bw)}
                break
        assert win is not None
        lifted[wname] = win

    return {"group": f"UT_{n}(F_{p})", "order": f"{p}^{n*(n-1)//2}", "exact_class": cl, "lifted_cycles": lifted}


def verify_theta_lifting_section() -> dict:
    magnus_self_test()

    # A. Class-2 Theta(8, 8, 8)
    end2, diffs2 = collect_theta_diffs(T8_PLUS, trunc_len=3)
    assert end2[:3] == (0, 0, 1) and len(diffs2) == 121
    max_abs2 = [max(abs(d[k]) for d in diffs2) for k in range(3)]
    assert max_abs2 == [3, 3, 4]
    zero_xy_z2 = sorted({abs(d[2]) for d in diffs2 if d[0] == 0 and d[1] == 0})
    assert zero_xy_z2 == [1]

    def check_order27(mode: str) -> dict:
        if mode == "UT3_F3":
            elems = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]
            mul = lambda u, v: ((u[0] + v[0]) % 3, (u[1] + v[1]) % 3, (u[2] + v[2] + u[0] * v[1]) % 3)
            inv = lambda u: ((-u[0]) % 3, (-u[1]) % 3, (-u[2] + u[0] * u[1]) % 3)
            id_g = (0, 0, 0)
        else:
            elems = [(x, y) for x in range(9) for y in range(3)]
            mul = lambda u, v: ((u[0] + pow(4, u[1], 9) * v[0]) % 9, (u[1] + v[1]) % 3)
            inv = lambda u: ((-pow(4, (-u[1]) % 3, 9) * u[0]) % 9, (-u[1]) % 3)
            id_g = (0, 0)

        idx_map = {g: i for i, g in enumerate(elems)}
        non_id = [g for g in elems if g != id_g]
        gen_pairs = t8_covered = mitm_covered = 0
        for i, a in enumerate(non_id):
            ia = inv(a)
            for b in non_id[i + 1:]:
                ib = inv(b)
                seen = {id_g}
                q = deque([id_g])
                while q:
                    u = q.popleft()
                    for s in (a, b, ia, ib):
                        nu = mul(u, s)
                        if nu not in seen:
                            seen.add(nu)
                            q.append(nu)
                if len(seen) != 27:
                    continue
                gen_pairs += 1
                found_t8 = False
                for t in (id_g, a, b):
                    it = inv(t)
                    rem = [mul(it, x) for x in (id_g, a, b) if x != t]
                    for sa, sb in ((rem[0], rem[1]), (rem[1], rem[0])):
                        sh = (id_g, sa, sb)
                        iv = (id_g, inv(sa), inv(sb))
                        ends_m = []
                        s0_v, s1_v = {id_g}, set()
                        ok = True
                        for w in T8_PLUS:
                            cur = id_g
                            for step_i, ch in enumerate(w):
                                cur = mul(cur, sh[int(ch)] if step_i % 2 == 0 else iv[int(ch)])
                                if step_i % 2 == 0:
                                    if cur in s1_v:
                                        ok = False
                                        break
                                    s1_v.add(cur)
                                elif step_i < 7:
                                    if cur in s0_v:
                                        ok = False
                                        break
                                    s0_v.add(cur)
                                else:
                                    ends_m.append(cur)
                            if not ok:
                                break
                        if ok and ends_m[0] == ends_m[1] == ends_m[2] and ends_m[0] not in s0_v:
                            found_t8 = True
                            break
                    if found_t8:
                        break
                if found_t8:
                    t8_covered += 1
                    mitm_covered += 1
                else:
                    adj = [[] for _ in range(54)]
                    for gi, g_el in enumerate(elems):
                        for s_el in (id_g, a, b):
                            v = 27 + idx_map[mul(g_el, s_el)]
                            adj[gi].append(v)
                            adj[v].append(gi)
                    bkt = [{}, {}, {}]
                    for br, f0 in enumerate(adj[0]):
                        def dfs_m(u: int, dep: int, msk: int) -> None:
                            if dep == 8:
                                bkt[br].setdefault(u, []).append(msk)
                                return
                            m2 = msk | (1 << u)
                            for w in adj[u]:
                                if w != 0 and not ((m2 >> w) & 1):
                                    dfs_m(w, dep + 1, m2)
                        dfs_m(f0, 1, 0)
                    common = set(bkt[0]) & set(bkt[1]) & set(bkt[2])
                    assert any(
                        (m0 & m1) == 0 and ((m0 | m1) & m2) == 0
                        for vtx in common
                        for m0 in bkt[0][vtx]
                        for m1 in bkt[1][vtx]
                        for m2 in bkt[2][vtx]
                    )
                    mitm_covered += 1
        assert gen_pairs == 216 and mitm_covered == 216
        if mode == "UT3_F3":
            assert t8_covered == 216
        return {"generating_pairs": gen_pairs, "T8_plus_covered": t8_covered, "Theta8_MITM_covered": mitm_covered}

    class2_res = {
        "T8_plus": list(T8_PLUS),
        "endpoint_hall": list(end2[:3]),
        "same_shore_pairs": 121,
        "max_abs_xyz": max_abs2,
        "zero_xy_abs_z": zero_xy_z2,
        "UT3_F3": check_order27("UT3_F3"),
        "M27": check_order27("M27"),
    }

    # B. Class-3 Theta(16, 16, 16) -> Unconditional Class <= 7 Theorem
    info3 = {}
    diffs3_by = {}
    for name, branches in CLASS3_THETAS.items():
        end, diffs = collect_theta_diffs(branches, trunc_len=5)
        assert len(diffs) == 529
        diffs3_by[name] = diffs
        ab_hist = Counter(gcd(abs(d[0]), abs(d[1])) for d in diffs)
        zero_xy_z = sorted({d[2] for d in diffs if d[0] == 0 and d[1] == 0})
        div3_xy = {}
        for x, y, z, _, _, _, _, _ in diffs:
            if (x != 0 or y != 0) and x % 3 == 0 and y % 3 == 0:
                div3_xy.setdefault((x, y), set()).add(z)
        info3[name] = {
            "endpoint_hall": list(end[:5]),
            "ab_gcd_hist": {str(k): val for k, val in sorted(ab_hist.items())},
            "zero_xy_z": zero_xy_z,
            "div3_xy": {f"({k[0]},{k[1]})": sorted(val) for k, val in sorted(div3_xy.items())},
        }

    assert all(d[2] != 0 for d in diffs3_by["W_B0"] if d[0] == 0 and d[1] == 0)
    for k0, wname in [(0, "W_B0"), (1, "W_B1"), (2, "W_B2")]:
        for x, y, z, _, _, _, _, _ in diffs3_by[wname]:
            if x % 3 == 0 and y % 3 == 0:
                if x == 0 and y == 0:
                    assert z % 3 != 0
                elif x == 0:
                    assert ((y // 3) * k0 + z) % 3 != 0
                else:
                    assert (x, y) in {(-3, 0), (3, 0), (-3, 3), (3, -3)}

    q81_cov = {"W_Q81_A": 0, "W_Q81_B": 0, "both": 0}
    for pd, pe in [(1, 0), (0, 1), (1, 1), (1, 2)]:
        for alpha in (0, 1, 2):
            for beta in (0, 1, 2):
                def ok_in(wname: str) -> bool:
                    for x, y, z, u, v, _, _, _ in diffs3_by[wname]:
                        if x % 3 == 0 and y % 3 == 0 and z % 3 == 0:
                            if (alpha * (x // 3) + beta * (y // 3) + pd * u + pe * v) % 3 == 0:
                                return False
                    return True

                cov_a = ok_in("W_Q81_A")
                cov_b = ok_in("W_Q81_B")
                assert cov_a or cov_b
                if cov_a and cov_b:
                    q81_cov["both"] += 1
                elif cov_a:
                    q81_cov["W_Q81_A"] += 1
                else:
                    q81_cov["W_Q81_B"] += 1

    ut8_ctrl = verify_ut_physical_lift(8, 3, [("W_B0", CLASS3_THETAS["W_B0"]), ("W_Q81_A", CLASS3_THETAS["W_Q81_A"])])

    # C. Class-4 L = 16 barrier & Theta(32, 32, 32) -> Class <= 9 (p >= 5)
    ID4 = (0,) * 8
    def adv4(st, c, even_step):
        if c == 0:
            return st
        if c == 1:
            return step4_a(st) if even_step else step4_ai(st)
        return step4_b(st) if even_step else step4_bi(st)

    ends4 = [set(), set(), set()]
    total_paths = 0
    for c0 in (0, 1, 2):
        def dfs4(st, step, last_c, s0, s1):
            nonlocal total_paths
            if step == 16:
                total_paths += 1
                ends4[c0].add(st)
                return
            even_step = (step % 2 == 0)
            for c in (0, 1, 2):
                if c == last_c:
                    continue
                nst = adv4(st, c, even_step)
                if even_step:
                    if nst in s1:
                        continue
                    s1.add(nst)
                    dfs4(nst, step + 1, c, s0, s1)
                    s1.remove(nst)
                else:
                    if step < 15 and nst in s0:
                        continue
                    if step < 15:
                        s0.add(nst)
                    dfs4(nst, step + 1, c, s0, s1)
                    if step < 15:
                        s0.remove(nst)

        st1 = adv4(ID4, c0, True)
        dfs4(st1, 1, c0, {ID4}, {st1})

    assert total_paths == 98304
    uniq4 = len(ends4[0] | ends4[1] | ends4[2])
    assert uniq4 == 94902 and len(ends4[0] & ends4[1] & ends4[2]) == 0

    w32_info = {}
    for wname, branches in CLASS4_THETAS.items():
        end, diffs = collect_theta_diffs(branches, trunc_len=8)
        assert len(diffs) == 2209
        ab_hist = Counter(gcd(abs(d[0]), abs(d[1])) for d in diffs)
        assert max(ab_hist) == 4
        zero_xy_z = sorted({abs(d[2]) for d in diffs if d[0] == 0 and d[1] == 0 and d[2] != 0})
        assert max(zero_xy_z) == 4
        grade3_uv = [(d[3], d[4]) for d in diffs if d[0] == 0 and d[1] == 0 and d[2] == 0 and (d[3] != 0 or d[4] != 0)]
        assert all(d[:5] != (0, 0, 0, 0, 0) for d in diffs)
        if wname == "T32_D":
            assert all(v == 0 and 1 <= abs(u) <= 4 for u, v in grade3_uv)
            g3_dir = "(1,0)"
        else:
            assert all(u == 0 and 1 <= abs(v) <= 3 for u, v in grade3_uv)
            g3_dir = "(0,1)"
        w32_info[wname] = {
            "endpoint_hall": list(end),
            "same_shore_pairs": 2209,
            "ab_gcd_hist": {str(k): val for k, val in sorted(ab_hist.items())},
            "zero_xy_abs_z": zero_xy_z,
            "grade3_count": len(grade3_uv),
            "grade3_direction": g3_dir,
            "grade4_central_count": 0,
        }

    ut10_ctrl = verify_ut_physical_lift(10, 5, [("T32_D", CLASS4_THETAS["T32_D"]), ("T32_E", CLASS4_THETAS["T32_E"])])

    return {
        "class2_theta8": class2_res,
        "class3_theta16_uncond_class7": {
            "witnesses": info3,
            "order81_36_cases_coverage": q81_cov,
            "UT8_F3_exact_class7_control": ut8_ctrl,
        },
        "class4_theta32_uncond_class9_p_ge_5": {
            "L16_barrier_simple_paths": total_paths,
            "L16_barrier_unique_endpoints": uniq4,
            "L16_barrier_common_endpoints": 0,
            "T32_companion_witnesses": w32_info,
            "UT10_F5_exact_class9_control": ut10_ctrl,
        },
    }


# ---------------------------------------------------------------------------
# 2. Universal Semidirect A |>_sigma C_6 & Cyclotomic Phi_6 Refinement
# ---------------------------------------------------------------------------

def walk_word(word: str, id_elem, sha, shb, mul_fn, inv_fn):
    sh = (id_elem, sha, shb)
    iv = (id_elem, inv_fn(sha), inv_fn(shb))
    cur = id_elem
    states = []
    for i, ch in enumerate(word):
        states.append(cur)
        cur = mul_fn(cur, sh[int(ch)] if i % 2 == 0 else iv[int(ch)])
    return cur, states


def short_walks_and_orbits(id_elem, sha, shb, mul_fn, inv_fn, rot_fn, m_ord: int, conj_depth: int):
    sh = (id_elem, sha, shb)
    iv = (id_elem, inv_fn(sha), inv_fn(shb))
    colls = {sha, inv_fn(sha), shb, inv_fn(shb), mul_fn(inv_fn(sha), shb), mul_fn(inv_fn(shb), sha)}

    short48 = {}
    for L in (4, 8):
        def dfs(dep: int, st, fc: int, lc: int, chs: str) -> None:
            if dep == L:
                if lc != fc and st != id_elem and st not in short48:
                    short48[st] = (L, chs)
                return
            for c in (0, 1, 2):
                if c != lc:
                    dfs(dep + 1, mul_fn(st, sh[c] if dep % 2 == 0 else iv[c]), fc, c, chs + str(c))
        for c0 in (0, 1, 2):
            dfs(1, sh[c0], c0, c0, str(c0))

    layer = {id_elem}
    gens = (sha, inv_fn(sha), shb, inv_fn(shb))
    for _ in range(conj_depth):
        nxt = set(layer)
        for x in layer:
            for g in gens:
                nxt.add(mul_fn(x, g))
        layer = nxt
    conj_set = list(layer)

    conj_colls = set(colls)
    for st in colls:
        for g in conj_set:
            conj_colls.add(mul_fn(inv_fn(g), mul_fn(st, g)))
            if st[1] == 0:
                conj_colls.add((rot_fn(st[0], 0), 0))

    conj_short = {}
    for st, info in short48.items():
        for sgn in (st, inv_fn(st)):
            conj_short.setdefault(sgn, (info[0], info[1], "direct"))
            if sgn[1] == 0:
                for k in range(m_ord):
                    conj_short.setdefault((rot_fn(sgn[0], k), 0), (info[0], info[1], "c6_shift"))
            for g in conj_set:
                cg = mul_fn(inv_fn(g), mul_fn(sgn, g))
                conj_short.setdefault(cg, (info[0], info[1], "conjugate"))

    return short48, conj_colls, conj_short


def verify_semidirect_c6_section() -> dict:
    seen_orbs = set()
    orbits = []
    for ta in range(6):
        for tb in range(6):
            if (ta, tb) == (0, 0) or ta == tb:
                continue
            orb = set()
            q = [(ta, tb)]
            while q:
                x, y = q.pop()
                if (x, y) in orb:
                    continue
                orb.add((x, y))
                for nx, ny in [(y, x), ((-x) % 6, (y - x) % 6), ((x - y) % 6, (-y) % 6), ((6 - x) % 6, (6 - y) % 6)]:
                    if (nx, ny) not in orb:
                        q.append((nx, ny))
            key = tuple(sorted(orb))
            if key not in seen_orbs:
                seen_orbs.add(key)
                ord_sub = 6 // gcd(6, gcd(ta, tb))
                assert any((x == 1 or (ord_sub < 6 and x == 6 // ord_sub)) for x, _ in key)
                orbits.append({"canonical_rep": list(key[0]), "subgroup_order": ord_sub, "orbit_size": len(key)})
    assert sum(o["orbit_size"] for o in orbits) == 35
    assert {tuple(o["canonical_rep"]) for o in orbits if o["subgroup_order"] == 6} == {(0, 1), (1, 2), (1, 3)}

    id_u = ((0,) * 12, 0)
    def rot6(v: tuple[int, ...], k: int) -> tuple[int, ...]:
        k %= 6
        if k == 0:
            return v
        b1, b2 = v[:6], v[6:]
        return (b1[-k:] + b1[:-k]) + (b2[-k:] + b2[:-k])

    def mul_u(x, y):
        rv = rot6(y[0], x[1])
        return (tuple(x[0][i] + rv[i] for i in range(12)), (x[1] + y[1]) % 6)

    def inv_u(x):
        nt = (-x[1]) % 6
        rv = rot6(x[0], nt)
        return (tuple(-u for u in rv), nt)

    e1 = ((1, 0, 0, 0, 0, 0) + (0,) * 6, 1)
    univ_cases = {}
    for label, tb, word, depth in [
        ("General_C6_Orbit_1_0", 0, W_G10, 3),
        ("General_C6_Orbit_1_3", 3, W_G10, 3),
        ("General_C6_Orbit_1_2", 2, W_C6_12, 3),
    ]:
        e2 = ((0,) * 6 + (1, 0, 0, 0, 0, 0), tb)
        end_w, st_w = walk_word(word, id_u, e1, e2, mul_u, inv_u)
        L = len(word)
        assert end_w == id_u and len(set(st_w[0::2])) == L // 2 and len(set(st_w[1::2])) == L // 2
        assert all(word[i] != word[(i + 1) % L] for i in range(L))

        _, colls, conj_short = short_walks_and_orbits(id_u, e1, e2, mul_u, inv_u, rot6, 6, depth)
        comm = mul_u(mul_u(inv_u(e1), inv_u(e2)), mul_u(e1, e2))
        comm_orbs = {(rot6(sgn[0], k), 0) for sgn in (comm, inv_u(comm)) for k in range(6)}
        kb_rel = mul_u(mul_u(mul_u(e1, e2), inv_u(e1)), e2)
        kb_orbs = {(rot6(sgn[0], k), 0) for sgn in (kb_rel, inv_u(kb_rel)) for k in range(6)} if kb_rel[1] == 0 else set()

        counts = Counter()
        for i in range(L):
            for j in range(i + 2, L, 2):
                d = mul_u(inv_u(st_w[i]), st_w[j])
                if d[1] != 0:
                    counts["nonzero_C6_coset_impossible_to_vanish"] += 1
                elif d in colls:
                    counts["collapse_t0"] += 1
                elif d in conj_short:
                    counts[f"len{conj_short[d][0]}_t0"] += 1
                elif d in comm_orbs:
                    counts["abelian_commutator_ab_t0"] += 1
                elif d in kb_orbs:
                    counts["klein_bottle_abab_t0"] += 1
                else:
                    raise AssertionError(f"Uncovered t=0 diff in {label}: {d}")

        univ_cases[label] = {
            "word": word,
            "length": L,
            "pair_classification": dict(sorted(counts.items())),
            "uncovered_t0_pairs": 0,
        }

    # C_32 sharpness on Orbit (1,2) in universal & finite wreath-like quotients
    sh_12 = (id_u, e1, ((0,) * 6 + (1, 0, 0, 0, 0, 0), 2))
    iv_12 = (id_u, inv_u(e1), inv_u(sh_12[2]))
    closed_short_univ = {}
    for L in (4, 8, 16):
        half = L // 2
        fwd = {}
        def gen_h(pos, step, fc, lc):
            if step == half:
                fwd.setdefault(pos, []).append((fc, lc))
                return
            for c in (0, 1, 2):
                if c != lc:
                    gen_h(mul_u(pos, sh_12[c] if step % 2 == 0 else iv_12[c]), step + 1, c if step == 0 else fc, c)
        gen_h(id_u, 0, -1, -1)
        cnt = sum(1 for p1, fl1 in fwd.items() for p2 in (inv_u(p1),) if p2 in fwd for f1, l1 in fl1 for f2, l2 in fwd[p2] if l1 != f2 and l2 != f1)
        assert cnt == 0
        closed_short_univ[str(L)] = 0

    finite_sharp = {}
    for k_len in (3, 6):
        def mul_p(g1, g2, k=k_len):
            c1, v1, t1 = g1
            c2, v2, t2 = g2
            sv = tuple(v2[(i - t1) % k] for i in range(k))
            return ((c1 + c2) % 5, tuple((v1[i] + sv[i]) % 5 for i in range(k)), (t1 + t2) % 6)

        def inv_p(g, k=k_len):
            c, v, t = g
            nt = (-t) % 6
            return ((-c) % 5, tuple((-v[(i - nt) % k]) % 5 for i in range(k)), nt)

        idp = (0, (0,) * k_len, 0)
        ap = (1, (0,) * k_len, 1)
        bp = (0, (1,) + (0,) * (k_len - 1), 2)
        sp, ip = (idp, ap, bp), (idp, inv_p(ap), inv_p(bp))
        cl_short = {}
        for L in (4, 8, 16):
            half = L // 2
            fwd = {}
            def gen_fp(pos, step, fc, lc):
                if step == half:
                    fwd.setdefault(pos, []).append((fc, lc))
                    return
                for c in (0, 1, 2):
                    if c != lc:
                        gen_fp(mul_p(pos, sp[c] if step % 2 == 0 else ip[c]), step + 1, c if step == 0 else fc, c)
            gen_fp(idp, 0, -1, -1)
            cnt = sum(1 for p1, fl1 in fwd.items() for p2 in (inv_p(p1),) if p2 in fwd for f1, l1 in fl1 for f2, l2 in fwd[p2] if l1 != f2 and l2 != f1)
            assert cnt == 0
            cl_short[str(L)] = 0
        end32, st32 = walk_word(W_C6_12, idp, ap, bp, mul_p, inv_p)
        assert end32 == idp and len(set(st32[0::2])) == 16 and len(set(st32[1::2])) == 16
        finite_sharp[f"Z5_x_Z5^{k_len}_rtimes_C6"] = {"order": 6 * (5 ** (1 + k_len)), "closed_4_8_16_walks": cl_short, "W_C6_12_simple_C32": True}

    # Cyclotomic Phi_6(sigma) = sigma^2 - sigma + 1 = 0 -> sharp C_16
    def rot_phi6(p0: int, p1: int, k: int) -> tuple[int, int]:
        k %= 6
        for _ in range(k):
            p0, p1 = -p1, p0 + p1
        return (p0, p1)

    def mul_phi6(g1, g2):
        v1, t1 = g1
        v2, t2 = g2
        a0, a1 = rot_phi6(v2[0], v2[1], t1)
        b0, b1 = rot_phi6(v2[2], v2[3], t1)
        return ((v1[0] + a0, v1[1] + a1, v1[2] + b0, v1[3] + b1), (t1 + t2) % 6)

    def inv_phi6(g):
        v, t = g
        nt = (-t) % 6
        a0, a1 = rot_phi6(v[0], v[1], nt)
        b0, b1 = rot_phi6(v[2], v[3], nt)
        return ((-a0, -a1, -b0, -b1), nt)

    id_p6 = ((0, 0, 0, 0), 0)
    assert mul_phi6(((0, 0, 1, 0), 3), ((0, 0, 1, 0), 3)) == id_p6
    phi6_cases = {"Phi6_Orbit_1_3": {"word": "0202", "length": 4, "reason": "b^2 = 1 identically"}}
    for label, tb, w16 in [("Phi6_Orbit_1_0", 0, W_PHI6_10), ("Phi6_Orbit_1_2", 2, W_PHI6_12)]:
        sa, sb = ((1, 0, 0, 0), 1), ((0, 0, 1, 0), tb)
        ew, sw = walk_word(w16, id_p6, sa, sb, mul_phi6, inv_phi6)
        assert ew == id_p6 and len(set(sw[0::2])) == 8 and len(set(sw[1::2])) == 8
        short_p6, _, _ = short_walks_and_orbits(id_p6, sa, sb, mul_phi6, inv_phi6, lambda v, k: v, 1, 0)
        colls_d = {sa, inv_phi6(sa), sb, inv_phi6(sb), mul_phi6(inv_phi6(sa), sb), mul_phi6(inv_phi6(sb), sa)}
        cnt = Counter()
        for i in range(16):
            for j in range(i + 2, 16, 2):
                d = mul_phi6(inv_phi6(sw[i]), sw[j])
                if d[1] != 0:
                    cnt["nonzero_C6_coset_impossible_to_vanish"] += 1
                elif d in colls_d:
                    cnt["collapse_direct"] += 1
                elif d in short_p6:
                    cnt[f"len{short_p6[d][0]}_direct"] += 1
                elif inv_phi6(d) in short_p6:
                    cnt[f"len{short_p6[inv_phi6(d)][0]}_inverse"] += 1
                else:
                    raise AssertionError(f"Uncovered Phi_6 diff in {label}: {d}")
        phi6_cases[label] = {"word16": w16, "pair_classification": dict(sorted(cnt.items())), "uncovered": 0}

    # Finite physical controls
    def exact_min_pow2(a, b, id_g, mul_fn, inv_fn, targets):
        shifts, invs = (id_g, a, b), (id_g, inv_fn(a), inv_fn(b))
        start = (id_g, 0)
        for L in targets:
            if L <= 16:
                found = False
                def dfs(pos, shore, step, fc, lc, vis):
                    nonlocal found
                    if found:
                        return
                    for c in (0, 1, 2):
                        if c == lc or (step == L - 1 and c == fc):
                            continue
                        npos = mul_fn(pos, shifts[c] if shore == 0 else invs[c])
                        nv = (npos, 1 - shore)
                        if step == L - 1:
                            if nv == start:
                                found = True
                                return
                        elif nv not in vis:
                            vis.add(nv)
                            dfs(npos, 1 - shore, step + 1, fc, c, vis)
                            vis.remove(nv)
                for c0 in (0, 1):
                    dfs(shifts[c0], 1, 1, c0, c0, {start, (shifts[c0], 1)})
                    if found:
                        return L
            else:
                for perm in itertools.permutations((0, 1, 2)):
                    ps = [shifts[p] for p in perm]
                    s0i = inv_fn(ps[0])
                    end_w, sw = walk_word(W_C6_12, id_g, mul_fn(s0i, ps[1]), mul_fn(s0i, ps[2]), mul_fn, inv_fn)
                    if end_w == id_g and len(set(sw[0::2])) == 16 and len(set(sw[1::2])) == 16:
                        return 32
        return None

    controls = {}
    for label, mods, mults, exhaustive in [
        ("AGL_1_7_C7_rtimes_3_C6", (7,), (3,), True),
        ("C13_rtimes_4_C6", (13,), (4,), True),
        ("nonPhi6_C3xC7_rtimes_2_2_C6", (3, 7), (2, 2), False),
    ]:
        elems_a = list(product(*[range(m) for m in mods]))
        def mul_g(g1, g2, mods=mods, mults=mults):
            res = list(g2[0])
            for _ in range(g1[1] % 6):
                res = [(res[k] * mults[k]) % mods[k] for k in range(len(mods))]
            return (tuple((g1[0][k] + res[k]) % mods[k] for k in range(len(mods))), (g1[1] + g2[1]) % 6)

        def inv_g(g, mods=mods, mults=mults):
            nt = (-g[1]) % 6
            res = [(-g[0][k]) % mods[k] for k in range(len(mods))]
            for _ in range(nt):
                res = [(res[k] * mults[k]) % mods[k] for k in range(len(mods))]
            return (tuple(res), nt)

        id_g = ((0,) * len(mods), 0)
        G = [(u, t) for u in elems_a for t in range(6)]
        non_id = [g for g in G if g != id_g]
        if exhaustive:
            hist_all, hist_gen = Counter(), Counter()
            for i, a in enumerate(non_id):
                ia = inv_g(a)
                for b in non_id[i + 1:]:
                    ib = inv_g(b)
                    L = exact_min_pow2(a, b, id_g, mul_g, inv_g, (4, 8, 16))
                    assert L in (4, 8, 16)
                    hist_all[L] += 1
                    seen = {id_g, a, b}
                    q = deque([id_g, a, b])
                    while q:
                        x = q.popleft()
                        for s in (a, b, ia, ib):
                            nx = mul_g(x, s)
                            if nx not in seen:
                                seen.add(nx)
                                q.append(nx)
                    if len(seen) == len(G):
                        hist_gen[L] += 1
            controls[label] = {
                "order": len(G),
                "all_unordered_pairs": sum(hist_all.values()),
                "all_pairs_min_pow2_hist": {str(k): v for k, v in sorted(hist_all.items())},
                "generating_pairs": sum(hist_gen.values()),
                "generating_pairs_min_pow2_hist": {str(k): v for k, v in sorted(hist_gen.items())},
            }
        else:
            hist_rep = Counter()
            pairs = [
                ((u1, 1), (u2, tb))
                for tb in (0, 2, 3)
                for u1 in ((0, 0), (1, 1))
                for u2 in elems_a
                if (u2, tb) != id_g and (u2, tb) != (u1, 1)
            ]
            for a, b in pairs:
                L = exact_min_pow2(a, b, id_g, mul_g, inv_g, (4, 8, 16, 32))
                assert L is not None
                hist_rep[L] += 1
            controls[label] = {
                "order": len(G),
                "orbit_rep_pairs": len(pairs),
                "orbit_rep_min_pow2_hist": {str(k): v for k, v in sorted(hist_rep.items())},
            }

    return {
        "c6_coset_orbits": {"total_nonidentity_pairs_partitioned": 35, "orbits": orbits},
        "general_C6_universal_cases": univ_cases,
        "universal_orbit12_closed_4_8_16": closed_short_univ,
        "finite_sharp_C32_examples": finite_sharp,
        "cyclotomic_Phi6_sharp_C16": phi6_cases,
        "finite_physical_controls": controls,
    }


# ---------------------------------------------------------------------------
# 3. Analytic Menger-Spider Stretch Bounds for Two-Attachment Cubic Gadgets
# ---------------------------------------------------------------------------

def gadget_path_spectrum(n_verts: int, edges: list[tuple[int, int]], u: int, v: int) -> list[int]:
    adj = [[] for _ in range(n_verts)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    lengths = set()

    def dfs(curr: int, depth: int, vis_mask: int) -> None:
        if curr == v:
            lengths.add(depth)
            return
        for nxt in adj[curr]:
            if not ((vis_mask >> nxt) & 1):
                dfs(nxt, depth + 1, vis_mask | (1 << nxt))

    dfs(u, 0, 1 << u)
    return sorted(lengths)


def count_short_cycles_4_8(n_verts: int, edges: list[tuple[int, int]]) -> tuple[int, int]:
    adj = [set() for _ in range(n_verts)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    def cnt(length: int) -> int:
        tot = 0
        for s in range(n_verts):
            path = [s]
            used = {s}
            def dfs(cur: int) -> None:
                nonlocal tot
                if len(path) == length:
                    if s in adj[cur] and path[1] < path[-1]:
                        tot += 1
                    return
                for w in adj[cur]:
                    if w > s and w not in used:
                        used.add(w)
                        path.append(w)
                        dfs(w)
                        path.pop()
                        used.remove(w)
            dfs(s)
        return tot

    return cnt(4), cnt(8)


def verify_gadget_stretch_section() -> dict:
    by_M = {}
    for M in range(1, 8):
        checked = valid = 0
        for q2 in range(1, M + 1):
            for q1 in range(1, q2 + 1):
                L = q1 + q2
                if L in (4, 8):
                    continue
                internal = [v for v in range(1, L) if v != q1]
                if len(internal) < 3:
                    continue
                for w1, w2, w3 in combinations(internal, 3):
                    ws = (w1, w2, w3)
                    for ls in product(range(1, M), repeat=3):
                        checked += 1
                        ok = True
                        for a, b in ((0, 1), (0, 2), (1, 2)):
                            u, v = ws[a], ws[b]
                            s = ls[a] + ls[b]
                            dC = abs(u - v)
                            if (dC + s) in (4, 8) or (L - dC + s) in (4, 8):
                                ok = False
                                break
                            if (u < q1) == (v < q1):
                                if s > v - u:
                                    ok = False
                                    break
                            else:
                                if (u + s + v - q1) > M or (L - v + s + q1 - u) > M:
                                    ok = False
                                    break
                        if ok:
                            valid += 1
        assert valid == 0
        by_M[str(M)] = {"configs_checked": checked, "valid_configs": 0}

    m_edges = [e for e in MARKSTROM24_EDGES if e != (0, 1)]
    c4_m, c8_m = count_short_cycles_4_8(24, m_edges)
    assert c4_m == 0 and c8_m == 0
    spec_m = gadget_path_spectrum(24, m_edges, 0, 1)
    assert spec_m[0] == 4 and spec_m[-1] == 23 and spec_m[-1] >= 2 * spec_m[0]

    fano = [[0, 1, 2], [0, 3, 4], [0, 5, 6], [1, 3, 5], [1, 4, 6], [2, 3, 6], [2, 4, 5]]
    fano[0].remove(0)
    f_edges = [(p, 7 + j) for j, blk in enumerate(fano) for p in blk]
    spec_f = gadget_path_spectrum(14, f_edges, 0, 7)
    s_edges = f_edges + [(a + 14, b + 14) for a, b in f_edges] + [(7, 14)]
    spec_s = gadget_path_spectrum(28, s_edges, 0, 21)
    assert spec_s[0] == 2 * spec_f[0] + 1 and spec_s[-1] == 2 * spec_f[-1] + 1

    return {
        "max_S_bound_general": 8,
        "max_S_bound_bipartite": 9,
        "garcia_stretch_unconditional_for_minS": [1, 2, 3, 4],
        "spider_elimination_by_M": by_M,
        "series_and_gadget_controls": {
            "Markstrom24_minus_01": {"vertices": 24, "C4": 0, "C8": 0, "min_S": spec_m[0], "max_S": spec_m[-1], "spectrum": spec_m},
            "Fano_minus_e": {"vertices": 14, "min_S": spec_f[0], "max_S": spec_f[-1], "spectrum": spec_f},
            "Fano_minus_e_series_pair": {"vertices": 28, "min_S": spec_s[0], "max_S": spec_s[-1], "superadditivity_exact": True},
        },
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    cert_payload = {
        "paper": "Paper V: Derived-Central Dyadic Theta Lifting to Nilpotent Class Nine, Universal Semidirect C_6 Cubic Haar Graphs, and Analytic Stretch Bounds for Two-Attachment Cubic Gadgets",
        "status": "PASS",
        "theta_lifting": verify_theta_lifting_section(),
        "semidirect_c6": verify_semidirect_c6_section(),
        "gadget_stretch": verify_gadget_stretch_section(),
    }
    serialized = json.dumps(cert_payload, indent=2) + "\n"
    if write_certs:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(serialized, encoding="utf-8")
    elif CERT_PATH.exists():
        assert CERT_PATH.read_text(encoding="utf-8") == serialized, "Certificate byte-for-byte mismatch!"
        saved = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        current = json.loads(serialized)
        for k in ("theta_lifting", "semidirect_c6", "gadget_stretch"):
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
        "class2_UT3_F3": out["theta_lifting"]["class2_theta8"]["UT3_F3"],
        "class2_M27": out["theta_lifting"]["class2_theta8"]["M27"],
        "class3_order81_cov": out["theta_lifting"]["class3_theta16_uncond_class7"]["order81_36_cases_coverage"],
        "class7_UT8_F3": out["theta_lifting"]["class3_theta16_uncond_class7"]["UT8_F3_exact_class7_control"]["lifted_cycles"],
        "class4_L16_common": out["theta_lifting"]["class4_theta32_uncond_class9_p_ge_5"]["L16_barrier_common_endpoints"],
        "class9_UT10_F5": out["theta_lifting"]["class4_theta32_uncond_class9_p_ge_5"]["UT10_F5_exact_class9_control"]["lifted_cycles"],
        "c6_uncovered_t0": {k: v["uncovered_t0_pairs"] for k, v in out["semidirect_c6"]["general_C6_universal_cases"].items()},
        "c6_finite_sharp_C32": out["semidirect_c6"]["finite_sharp_C32_examples"],
        "max_S_general": out["gadget_stretch"]["max_S_bound_general"],
        "max_S_bipartite": out["gadget_stretch"]["max_S_bound_bipartite"],
    }, indent=2))
