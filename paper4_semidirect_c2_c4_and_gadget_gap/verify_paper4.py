#!/usr/bin/env python3
"""Standalone standard-library verifier for Paper IV:
Sharp C_16 Bounds for Semidirect C_2-, C_4-, and Klein-Bottle Cubic Haar Graphs
and the Defect Point-Graph C_8 Identity for Bipartite Gadgets.

Run from repository root or paper4_semidirect_c2_c4_and_gadget_gap/:
    python verify_paper4.py
    python verify_paper4.py --write-certificates
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from itertools import combinations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "certificates" / "paper4_certificates.json"

W_KB = "0101010210121202"
W_G10 = "0102021021202012"
W_C4_GAUSS = {
    "Gauss_Case_1_0": "0101010212012102",
    "Gauss_Case_1_2": "0101010212102012",
    "Gauss_Case_1_3": "0101010201010102",
}


# ---------------------------------------------------------------------------
# Generic closure & short-walk analysis helpers
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


def build_conj_coverage(id_elem, sha, shb, mul_fn, inv_fn, conj_depth: int = 2):
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

    conj_short = {}
    for st, info in short48.items():
        for sgn in (st, inv_fn(st)):
            conj_short.setdefault(sgn, (info[0], info[1], "direct"))
            for g in conj_set:
                cg = mul_fn(inv_fn(g), mul_fn(sgn, g))
                conj_short.setdefault(cg, (info[0], info[1], "conjugate"))

    return short48, conj_colls, conj_short, conj_set


def shortest_pow2_haar(elems: list, id_elem, a, b, mul_fn, lengths=(4, 8, 16, 32)) -> int | None:
    idx = {g: i for i, g in enumerate(elems)}
    n = len(elems)
    adj: list[list[int]] = [[] for _ in range(2 * n)]
    for i, g in enumerate(elems):
        for s in (id_elem, a, b):
            v = n + idx[mul_fn(g, s)]
            adj[i].append(v)
            adj[v].append(i)
    for L in lengths:
        if L == 4:
            n1 = adj[0]
            if any(len(set(adj[n1[i]]) & set(adj[n1[j]])) >= 2 for i in range(3) for j in range(i + 1, 3)):
                return 4
            continue
        half = L // 2
        bkt = [defaultdict(set) for _ in range(3)]
        for br, f0 in enumerate(adj[0]):
            def dfs(u: int, dep: int, msk: int) -> None:
                if dep == half:
                    bkt[br][u].add(msk)
                    return
                m2 = msk | (1 << u)
                for w in adj[u]:
                    if w != 0 and not ((m2 >> w) & 1):
                        dfs(w, dep + 1, m2)
            dfs(f0, 1, 0)
        for b1 in range(3):
            for b2 in range(b1 + 1, 3):
                for t in set(bkt[b1]) & set(bkt[b2]):
                    for m1 in bkt[b1][t]:
                        for m2 in bkt[b2][t]:
                            if (m1 & m2) == 0:
                                return L
    return None


# ---------------------------------------------------------------------------
# 1. Klein bottle group K0 & Universal A |>_sigma C_2
# ---------------------------------------------------------------------------

def verify_klein_and_semidirect_c2() -> dict:
    id_k = (0, 0)
    mul_k = lambda x, y: (x[0] + ((-1) if (x[1] & 1) else 1) * y[0], x[1] + y[1])
    inv_k = lambda x: (-((-1) if (x[1] & 1) else 1) * x[0], -x[1])
    ak, bk = (0, 1), (1, 0)
    assert mul_k(mul_k(ak, bk), inv_k(ak)) == inv_k(bk)

    assert len(W_KB) == 16 and all(W_KB[i] != W_KB[(i + 1) % 16] for i in range(16))
    end_k, st_k = walk_word(W_KB, id_k, ak, bk, mul_k, inv_k)
    assert end_k == id_k and len(set(st_k[0::2])) == 8 and len(set(st_k[1::2])) == 8
    _, colls_k, short_k, _ = build_conj_coverage(id_k, ak, bk, mul_k, inv_k, conj_depth=2)
    kb_counts = Counter()
    for i in range(16):
        for j in range(i + 2, 16, 2):
            d = mul_k(inv_k(st_k[i]), st_k[j])
            if d in colls_k:
                kb_counts["collapse"] += 1
            elif d in short_k:
                kb_counts[f"len{short_k[d][0]}_{short_k[d][2]}"] += 1
            else:
                raise AssertionError(f"Uncovered diff in Klein bottle: {d}")

    id_c2 = ((0, 0, 0, 0), 0)
    def rot2(v, t): return v if (t % 2 == 0) else (v[1], v[0], v[3], v[2])
    def mul_c2(x, y):
        rv = rot2(y[0], x[1])
        return (tuple(x[0][i] + rv[i] for i in range(4)), (x[1] + y[1]) % 2)
    def inv_c2(x):
        nt = (-x[1]) % 2
        rv = rot2(x[0], nt)
        return (tuple(-u for u in rv), nt)

    a2, b2 = ((1, 0, 0, 0), 1), ((0, 0, 1, 0), 0)
    assert len(W_G10) == 16 and all(W_G10[i] != W_G10[(i + 1) % 16] for i in range(16))
    end2, st2 = walk_word(W_G10, id_c2, a2, b2, mul_c2, inv_c2)
    assert end2 == id_c2 and len(set(st2[0::2])) == 8 and len(set(st2[1::2])) == 8
    _, colls2, short2, _ = build_conj_coverage(id_c2, a2, b2, mul_c2, inv_c2, conj_depth=2)

    comm2 = mul_c2(mul_c2(inv_c2(a2), inv_c2(b2)), mul_c2(a2, b2))
    comm2_orbs = {(rot2(sgn[0], k), 0) for sgn in (comm2, inv_c2(comm2)) for k in range(2)}
    kb_rel2 = mul_c2(mul_c2(mul_c2(a2, b2), inv_c2(a2)), b2)
    assert kb_rel2 == ((0, 0, 1, 1), 0)
    kb_orbs2 = {(rot2(sgn[0], k), 0) for sgn in (kb_rel2, inv_c2(kb_rel2)) for k in range(2)}

    c2_counts = Counter()
    for i in range(16):
        for j in range(i + 2, 16, 2):
            d = mul_c2(inv_c2(st2[i]), st2[j])
            if d in colls2:
                c2_counts["collapse"] += 1
            elif d in short2:
                c2_counts[f"len{short2[d][0]}"] += 1
            elif d in comm2_orbs:
                c2_counts["commutator_ab"] += 1
            elif d in kb_orbs2:
                c2_counts["klein_bottle_relation_abab"] += 1
            else:
                raise AssertionError(f"Uncovered diff in Z[C2]^2 |> C2: {d}")

    return {
        "klein_bottle_word16": W_KB,
        "klein_bottle_pair_classification": dict(sorted(kb_counts.items())),
        "klein_bottle_uncovered": 0,
        "general_c2_case10_word16": W_G10,
        "general_c2_comm_ab": list(comm2[0]),
        "general_c2_kb_rel": list(kb_rel2[0]),
        "general_c2_pair_classification": dict(sorted(c2_counts.items())),
        "general_c2_uncovered": 0,
    }


# ---------------------------------------------------------------------------
# 2. Universal General A |>_sigma C_4 (sigma^4 = 1) & Gaussian C_4
# ---------------------------------------------------------------------------

def verify_semidirect_c4() -> dict:
    id_c4 = ((0,) * 8, 0)
    def rot4(v, k):
        k %= 4; a, b = v[:4], v[4:]
        return (a[-k:] + a[:-k] if k else a) + (b[-k:] + b[:-k] if k else b)
    def mul_c4(x, y):
        rv = rot4(y[0], x[1])
        return (tuple(x[0][i] + rv[i] for i in range(8)), (x[1] + y[1]) % 4)
    def inv_c4(x):
        nt = (-x[1]) % 4; rv = rot4(x[0], nt)
        return (tuple(-u for u in rv), nt)

    general_c4 = {}
    for label, tb in [("General_C4_Case_1_0", 0), ("General_C4_Case_1_2", 2)]:
        sha = ((1, 0, 0, 0, 0, 0, 0, 0), 1)
        shb = ((0, 0, 0, 0, 1, 0, 0, 0), tb)
        end4, st4 = walk_word(W_G10, id_c4, sha, shb, mul_c4, inv_c4)
        assert end4 == id_c4 and len(set(st4[0::2])) == 8 and len(set(st4[1::2])) == 8
        _, colls4, short4, _ = build_conj_coverage(id_c4, sha, shb, mul_c4, inv_c4, conj_depth=3)

        comm4 = mul_c4(mul_c4(inv_c4(sha), inv_c4(shb)), mul_c4(sha, shb))
        comm4_orbs = {(rot4(sgn[0], k), 0) for sgn in (comm4, inv_c4(comm4)) for k in range(4)}
        kb4 = mul_c4(mul_c4(mul_c4(sha, shb), inv_c4(sha)), shb)
        kb4_orbs = {(rot4(sgn[0], k), 0) for sgn in (kb4, inv_c4(kb4)) for k in range(4)}

        counts = Counter()
        for i in range(16):
            for j in range(i + 2, 16, 2):
                d = mul_c4(inv_c4(st4[i]), st4[j])
                if d in colls4: counts["collapse"] += 1
                elif d in short4: counts[f"len{short4[d][0]}"] += 1
                elif d in comm4_orbs: counts["abelian_commutator_ab"] += 1
                elif d in kb4_orbs: counts["klein_bottle_relation_abab"] += 1
                else: raise AssertionError(f"Uncovered diff in {label}: {d}")
        general_c4[label] = {
            "word16": W_G10, "comm_ab": list(comm4[0]), "kb_rel": list(kb4[0]),
            "pair_classification": dict(sorted(counts.items())), "uncovered_pairs": 0,
        }

    id_g = ((0, 0, 0, 0), 0)
    def rot_i(x0, x1, k):
        k %= 4
        if k == 0: return (x0, x1)
        if k == 1: return (-x1, x0)
        if k == 2: return (-x0, -x1)
        return (x1, -x0)
    def mul_gi(x, y):
        u1, t1 = x; u2, t2 = y
        a0, a1 = rot_i(u2[0], u2[1], t1); b0, b1 = rot_i(u2[2], u2[3], t1)
        return ((u1[0] + a0, u1[1] + a1, u1[2] + b0, u1[3] + b1), (t1 + t2) % 4)
    def inv_gi(x):
        u, t = x; nt = (-t) % 4
        a0, a1 = rot_i(u[0], u[1], nt); b0, b1 = rot_i(u[2], u[3], nt)
        return ((-a0, -a1, -b0, -b1), nt)

    assert mul_gi(((1, 0, 0, 0), 2), ((1, 0, 0, 0), 2)) == id_g

    gaussian_cases = {}
    for label, tb in [("Gauss_Case_1_0", 0), ("Gauss_Case_1_2", 2), ("Gauss_Case_1_3", 3)]:
        w = W_C4_GAUSS[label]
        sha = ((1, 0, 0, 0), 1); shb = ((0, 0, 1, 0), tb)
        end_gi, st_gi = walk_word(w, id_g, sha, shb, mul_gi, inv_gi)
        assert end_gi == id_g and len(set(st_gi[0::2])) == 8 and len(set(st_gi[1::2])) == 8
        short_gi, _, _, _ = build_conj_coverage(id_g, sha, shb, mul_gi, inv_gi, conj_depth=1)
        colls_direct = {sha, inv_gi(sha), shb, inv_gi(shb), mul_gi(inv_gi(sha), shb), mul_gi(inv_gi(shb), sha)}
        cnt = Counter()
        for i in range(16):
            for j in range(i + 2, 16, 2):
                d = mul_gi(inv_gi(st_gi[i]), st_gi[j])
                if d in colls_direct: cnt["collapse_direct"] += 1
                elif d in short_gi: cnt[f"len{short_gi[d][0]}_direct"] += 1
                elif inv_gi(d) in short_gi: cnt[f"len{short_gi[inv_gi(d)][0]}_inverse"] += 1
                else: raise AssertionError(f"Uncovered Gaussian diff in {label}: {d}")
        gaussian_cases[label] = {"word16": w, "pair_classification": dict(sorted(cnt.items())), "uncovered_pairs": 0}

    controls = {}

    gl23 = [(a, b, c, d) for a in range(3) for b in range(3) for c in range(3) for d in range(3) if (a * d - b * c) % 3 != 0]
    id23 = (1, 0, 0, 1)
    def mul23(X, Y): return ((X[0]*Y[0]+X[1]*Y[2])%3, (X[0]*Y[1]+X[1]*Y[3])%3, (X[2]*Y[0]+X[3]*Y[2])%3, (X[2]*Y[1]+X[3]*Y[3])%3)
    def inv23(X):
        det = (X[0] * X[3] - X[1] * X[2]) % 3; invd = 1 if det == 1 else 2
        return ((X[3]*invd)%3, (-X[1]*invd)%3, (-X[2]*invd)%3, (X[0]*invd)%3)
    invs23 = {x: inv23(x) for x in gl23}
    gl_hist = Counter()
    for i in range(1, 48):
        a = gl23[i]; ia = invs23[a]
        for j in range(i + 1, 48):
            b = gl23[j]; ib = invs23[b]
            seen = {id23, a, b}; q = deque([id23, a, b])
            while q:
                u = q.popleft()
                for g in (a, b, ia, ib):
                    nu = mul23(u, g)
                    if nu not in seen: seen.add(nu); q.append(nu)
            if len(seen) != 48: continue
            L = shortest_pow2_haar(gl23, id23, a, b, mul23, (4, 8, 16, 32))
            assert L is not None; gl_hist[L] += 1
    controls["GL_2_3_all_generating_pairs"] = {str(k): v for k, v in sorted(gl_hist.items())}

    el52 = [(u, t) for u in range(13) for t in range(4)]
    mul52 = lambda x, y: ((x[0] + pow(5, x[1], 13) * y[0]) % 13, (x[1] + y[1]) % 4)
    inv52 = lambda x: ((-pow(5, (4 - x[1]) % 4, 13) * x[0]) % 13, (4 - x[1]) % 4)
    f52_hist = Counter(); seen_reanch = set()
    for i in range(1, 52):
        a = el52[i]
        for j in range(i + 1, 52):
            b = el52[j]; best = None
            for t in ((0, 0), a, b):
                it = inv52(t); pair = tuple(sorted(mul52(it, x) for x in ((0, 0), a, b) if x != t))
                if best is None or pair < best: best = pair
            if best in seen_reanch: continue
            seen_reanch.add(best)
            seen = {(0, 0), a, b}; q = deque([(0, 0), a, b])
            while q:
                u = q.popleft()
                for g in (a, b, inv52(a), inv52(b)):
                    nu = mul52(u, g)
                    if nu not in seen: seen.add(nu); q.append(nu)
            if len(seen) != 52: continue
            L = shortest_pow2_haar(el52, (0, 0), a, b, mul52, (4, 8, 16))
            assert L in (4, 8, 16); f52_hist[L] += 1
    controls["C13_rtimes_5_C4_all_generating_classes"] = {str(k): v for k, v in sorted(f52_hist.items())}

    id_w = ((0, 0, 0, 0), 0)
    def mul_w(x, y):
        k = x[1] % 4; vy = y[0][-k:] + y[0][:-k] if k else y[0]
        return (tuple((x[0][r] + vy[r]) % 5 for r in range(4)), (x[1] + y[1]) % 4)
    def inv_w(x):
        nt = (-x[1]) % 4; vx = x[0][-nt:] + x[0][:-nt] if nt else x[0]
        return (tuple((-u) % 5 for u in vx), nt)
    w_res = {}
    for nm, a, b in [("case10", ((1, 0, 2, 0), 1), ((0, 1, 0, 2), 0)), ("case12", ((1, 2, 0, 0), 1), ((0, 1, 3, 1), 2))]:
        ew, sw = walk_word(W_G10, id_w, a, b, mul_w, inv_w)
        assert ew == id_w and len(set(sw[0::2])) == 8 and len(set(sw[1::2])) == 8
        w_res[nm] = 16
    controls["F5_4_wreath_C4_order_2500"] = w_res

    kb_finite = 0
    for m in range(3, 8):
        for n in range(3, 8):
            mul_f = lambda x, y, mm=m, nn=n: ((x[0] + ((-1) if (x[1] & 1) else 1) * y[0]) % nn, (x[1] + y[1]) % (2 * mm))
            inv_f = lambda x, mm=m, nn=n: ((-((-1) if (x[1] & 1) else 1) * x[0]) % nn, (-x[1]) % (2 * mm))
            endf, stf = walk_word(W_KB, (0, 0), (0, 1), (1, 0), mul_f, inv_f)
            assert endf == (0, 0)
            if not (len(set(stf[0::2])) == 8 and len(set(stf[1::2])) == 8):
                el_f = [(u, t) for u in range(n) for t in range(2 * m)]
                assert shortest_pow2_haar(el_f, (0, 0), (0, 1), (1, 0), mul_f, (4, 8, 16)) in (4, 8, 16)
            kb_finite += 1
    controls["finite_klein_bottle_quotients_checked"] = kb_finite

    return {
        "general_C4_sigma4_eq_1_sharp_C16": general_c4,
        "gaussian_C4_sigma2_eq_minus1": gaussian_cases,
        "physical_controls": controls,
    }


# ---------------------------------------------------------------------------
# 3. Defect Point-Graph C8(H) Gap Identity & Solver-Free Star-K4 Bounds
# ---------------------------------------------------------------------------

def count_cycles_simple(adj: list[set[int]], length: int) -> int:
    total = 0
    for start in range(len(adj)):
        path = [start]; used = {start}
        def dfs(v: int) -> None:
            nonlocal total
            if len(path) == length:
                if start in adj[v] and path[1] < path[-1]: total += 1
                return
            for w in adj[v]:
                if w <= start or w in used: continue
                used.add(w); path.append(w); dfs(w); path.pop(); used.remove(w)
        dfs(start)
    return total


def check_defect_gap_identity(name: str, n: int, p0: int, l0_idx: int, blocks: list[list[int]]) -> dict:
    assert len(blocks) == n
    deg_p = [sum(v in b for b in blocks) for v in range(n)]
    assert deg_p[p0] == 2 and all(deg_p[v] == 3 for v in range(n) if v != p0)
    assert len(blocks[l0_idx]) == 2 and all(len(b) == 3 for j, b in enumerate(blocks) if j != l0_idx)

    owner = {}
    for j, b in enumerate(blocks):
        assert len(set(b)) == len(b)
        for u, v in combinations(sorted(b), 2):
            assert (u, v) not in owner
            owner[(u, v)] = j

    e0 = tuple(sorted(blocks[l0_idx]))
    case_type = "Case2_p0_in_l0" if p0 in e0 else "Case1_p0_notin_l0"
    q = [set() for _ in range(n)]; inc = [set() for _ in range(2 * n)]
    for u, v in owner: q[u].add(v); q[v].add(u)
    for j, b in enumerate(blocks):
        for v in b: inc[v].add(n + j); inc[n + j].add(v)

    pairs = list(combinations(range(n), 2))
    lam = {p: len(q[p[0]] & q[p[1]]) for p in pairs}
    edges3 = set(owner) - {e0}; rest = set(lam) - edges3

    c8_h = count_cycles_simple(inc, 8)
    c4_q = count_cycles_simple(q, 4)
    w_sum = sum(lam[e] - 1 for e in edges3)
    assert c8_h == c4_q - w_sum

    eg3 = sum((lam[e] - 3) * (lam[e] - 4) // 2 for e in edges3)
    ng_rest = sum((lam[p] - 1) * (lam[p] - 2) // 2 for p in rest)
    s_def = (n * n - 13 * n + 16) // 2 if p0 in e0 else (n * n - 13 * n + 20) // 2
    assert 2 * c8_h == eg3 + ng_rest - s_def

    return {"name": name, "n_per_shore": n, "case": case_type, "C8_H": c8_h, "C4_Q": c4_q, "W_3lines": w_sum, "S_def": s_def, "eg3_sum": eg3, "rest_gap_sum": ng_rest}


def verify_defect_point_graph_theory() -> dict:
    fano = [[0, 1, 2], [0, 3, 4], [0, 5, 6], [1, 3, 5], [1, 4, 6], [2, 3, 6], [2, 4, 5]]
    mk8 = [[i, (i + 1) % 8, (i + 3) % 8] for i in range(8)]
    des10 = [[0, 3, 7], [2, 4, 8], [1, 4, 5], [4, 6, 7], [1, 7, 8], [0, 2, 6], [0, 8, 9], [2, 5, 9], [1, 3, 9], [3, 5, 6]]
    b19 = [[(y - s) % 19 for s in (0, 1, 8)] for y in range(19)]

    controls = []
    for nm, nv, blks in [("Fano_minus_e", 7, fano), ("MobiusKantor_minus_e", 8, mk8), ("Desargues_minus_e", 10, des10), ("B19_minus_e", 19, b19)]:
        nb = [b[:] for b in blks]; p0 = nb[0][0]; nb[0].remove(p0)
        controls.append(check_defect_gap_identity(nm, nv, p0, 0, nb))

    def build_case2_gadget(n: int):
        rem = [1, 2] + [3] * (n - 2); used = {(0, 1)}; blks = [[0, 1]]
        def bt():
            if len(blks) == n: return True
            v = next(i for i in range(n) if rem[i] > 0)
            cands = [u for u in range(v + 1, n) if rem[u] > 0 and (v, u) not in used]
            for u, w in combinations(cands, 2):
                if (u, w) in used: continue
                for x in (v, u, w): rem[x] -= 1
                for a, b in ((v, u), (v, w), (u, w)): used.add((a, b))
                blks.append([v, u, w])
                if bt(): return True
                blks.pop()
                for a, b in ((v, u), (v, w), (u, w)): used.remove((a, b))
                for x in (v, u, w): rem[x] += 1
            return False
        assert bt(); return blks

    for n2 in (9, 11):
        controls.append(check_defect_gap_identity(f"Case2_n{n2}", n2, 0, 0, build_case2_gadget(n2)))

    fano_disc = [b[:] for b in fano] + [[v + 7 for v in b] for b in fano]; fano_disc[7].remove(7)
    controls.append(check_defect_gap_identity("Fano_disjoint_FanoMinusE", 14, 7, 7, fano_disc))

    cap_bounds = {}
    for label, nv, pairs, e3_verts in [
        ("deg6", 6, [(0, 1), (2, 3), (4, 5)], range(6)),
        ("deg5_e0_endpoint", 5, [(0, 1), (2, 3)], range(4)),
        ("deg4_Case1_p0", 4, [(0, 1), (2, 3)], range(4)),
        ("deg3_Case2_p0", 3, [(0, 1)], range(2)),
    ]:
        pair_set = set(pairs); others = [(a, b) for a, b in combinations(range(nv), 2) if (a, b) not in pair_set]
        max_expr = -999; checked = 0
        for mask in range(1 << len(others)):
            nbrs = [0] * nv
            for i, (a, b) in enumerate(others):
                if (mask >> i) & 1: nbrs[a] |= 1 << b; nbrs[b] |= 1 << a
            degs = [x.bit_count() for x in nbrs]
            if max(degs) > 2: continue
            k22 = False
            for (a, b), (c, d) in combinations(pairs, 2):
                req = (1 << c) | (1 << d)
                if (nbrs[a] & req) == req and (nbrs[b] & req) == req: k22 = True; break
            if k22: continue
            checked += 1
            d_val = sum(3 for v in e3_verts if degs[v] == 0) + sum(1 for v in e3_verts if degs[v] == 1)
            c3 = sum(1 for v in e3_verts if degs[v] == 2 and tuple(i for i in range(nv) if (nbrs[v] >> i) & 1) in pair_set)
            max_expr = max(max_expr, 3 * c3 - d_val)
        cap_bounds[label] = {"no_K22_configs": checked, "max_3c3_minus_d": max_expr}

    assert cap_bounds["deg6"]["max_3c3_minus_d"] == 6
    assert cap_bounds["deg5_e0_endpoint"]["max_3c3_minus_d"] == 6
    assert cap_bounds["deg4_Case1_p0"]["max_3c3_minus_d"] == 4
    assert cap_bounds["deg3_Case2_p0"]["max_3c3_minus_d"] == -2

    feas_counts = {}
    for n in range(4, 16):
        s1 = (n * n - 13 * n + 20) // 2; s2 = (n * n - 13 * n + 16) // 2
        c1 = sum(1 for e1 in range(n + 1) for e2 in range(3 * n - 2 - e1) if 3 * e1 + e2 <= s1 and e2 >= (3 * n - 3 - e1 - e2))
        c2 = sum(1 for e1 in range(n + 1) for e2 in range(3 * n - 2 - e1) if 3 * e1 + e2 <= s2 and e2 >= (3 * n - 3 - e1 - e2))
        if n <= 14: assert c1 == 0 and c2 == 0
        feas_counts[str(n)] = {"Case1": c1, "Case2": c2}

    return {
        "gap_identity_controls": controls,
        "local_k22_free_capacities": cap_bounds,
        "solver_free_n_le_14_zero_feasible": True,
        "star_k4_feasible_counts_by_n": feas_counts,
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    cert_payload = {
        "paper": "Paper IV: Sharp C_16 Bounds for Semidirect C_2-, C_4-, and Klein-Bottle Cubic Haar Graphs and the Defect Point-Graph C_8 Identity for Bipartite Gadgets",
        "status": "PASS",
        "klein_and_c2": verify_klein_and_semidirect_c2(),
        "semidirect_c4": verify_semidirect_c4(),
        "defect_point_graph": verify_defect_point_graph_theory(),
    }
    serialized = json.dumps(cert_payload, indent=2) + "\n"
    if write_certs:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(serialized, encoding="utf-8")
    elif CERT_PATH.exists():
        assert CERT_PATH.read_text(encoding="utf-8") == serialized, "Certificate byte-for-byte mismatch!"
        saved = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        current = json.loads(serialized)
        for k in ("klein_and_c2", "semidirect_c4", "defect_point_graph"):
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
        "kb_uncovered": out["klein_and_c2"]["klein_bottle_uncovered"],
        "c2_uncovered": out["klein_and_c2"]["general_c2_uncovered"],
        "c4_case10_uncovered": out["semidirect_c4"]["general_C4_sigma4_eq_1_sharp_C16"]["General_C4_Case_1_0"]["uncovered_pairs"],
        "c4_case12_uncovered": out["semidirect_c4"]["general_C4_sigma4_eq_1_sharp_C16"]["General_C4_Case_1_2"]["uncovered_pairs"],
        "gl23_pairs": out["semidirect_c4"]["physical_controls"]["GL_2_3_all_generating_pairs"],
        "c13_c4_classes": out["semidirect_c4"]["physical_controls"]["C13_rtimes_5_C4_all_generating_classes"],
        "defect_controls_checked": len(out["defect_point_graph"]["gap_identity_controls"]),
        "solver_free_n_le_14_zero_feasible": out["defect_point_graph"]["solver_free_n_le_14_zero_feasible"],
    }, indent=2))
