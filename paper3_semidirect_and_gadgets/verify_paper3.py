#!/usr/bin/env python3
"""Standalone standard-library verifier for Paper III:
Power-of-Two Cycles in Semidirect C_3-Extension Cubic Haar Graphs and
Two-Attachment Cubic Gadget Bounds (v3.0.0: exact n_min = 20 classification &
zero-gap 3 <= |G| <= 47 all-2-generated-groups Haar census).

Run from repository root or paper3_semidirect_and_gadgets/:
    python verify_paper3.py
    python verify_paper3.py --write-certificates
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "certificates" / "paper3_certificates.json"

WORD32_CLASS3 = "01010102012012101012012010212012"

# Semidirect A |>_sigma C_3 universal color words (0=1, 1=a, 2=b)
W_E10 = "0101020120102102"
W_E12 = "1021212021210202"
W_G10 = "0102021021202012"
W_G12 = "01202021020201021210201020210212"

# 24-vertex connected {C4, C8}-free cubic graph edges (sharp closure witness n_min^cl = 24)
MARKSTROM24_EDGES = [
    (0, 1), (0, 9), (0, 10), (1, 5), (1, 7), (2, 6), (2, 12), (2, 15),
    (3, 8), (3, 11), (3, 21), (4, 7), (4, 11), (4, 23), (5, 14), (5, 19),
    (6, 11), (6, 15), (7, 8), (8, 15), (9, 14), (9, 23), (10, 16), (10, 19),
    (12, 21), (12, 22), (13, 16), (13, 20), (13, 21), (14, 23), (16, 22),
    (17, 18), (17, 20), (17, 22), (18, 19), (18, 20),
]

# OEIS A000001 total group counts per order for 3 <= |G| <= 47
OEIS_GROUP_COUNTS = {
    3: 1, 4: 2, 5: 1, 6: 2, 7: 1, 8: 5, 9: 2, 10: 2, 11: 1, 12: 5,
    13: 1, 14: 2, 15: 1, 16: 14, 17: 1, 18: 5, 19: 1, 20: 5, 21: 2, 22: 2,
    23: 1, 24: 15, 25: 2, 26: 2, 27: 5, 28: 4, 29: 1, 30: 4, 31: 1, 32: 51,
    33: 1, 34: 2, 35: 1, 36: 14, 37: 1, 38: 2, 39: 2, 40: 14, 41: 1, 42: 6,
    43: 1, 44: 4, 45: 2, 46: 2, 47: 1,
}


# ---------------------------------------------------------------------------
# Shared Finite Haar Graph / MITM Cycle Helpers
# ---------------------------------------------------------------------------

def build_haar_adj_connected(elems: list, id_elem, a, b, mul_fn) -> tuple[list[list[int]], bool]:
    idx = {g: i for i, g in enumerate(elems)}
    n = len(elems)
    adj: list[list[int]] = [[] for _ in range(2 * n)]
    for i, g in enumerate(elems):
        for s in (id_elem, a, b):
            v = n + idx[mul_fn(g, s)]
            adj[i].append(v)
            adj[v].append(i)
    seen = {0}
    q = deque([0])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    return adj, len(seen) == 2 * n


def has_simple_cycle_mitm(adj: list[list[int]], roots: list[int], length: int) -> bool:
    for r in roots:
        if length == 4:
            n1 = adj[r]
            for i in range(3):
                for j in range(i + 1, 3):
                    if len(set(adj[n1[i]]) & set(adj[n1[j]])) >= 2:
                        return True
            continue
        half = length // 2
        bkt: list[dict[int, set[int]]] = [defaultdict(set) for _ in range(3)]
        for br, f0 in enumerate(adj[r]):
            def dfs(u: int, dep: int, msk: int) -> None:
                if dep == half:
                    bkt[br][u].add(msk)
                    return
                m2 = msk | (1 << u)
                for w in adj[u]:
                    if w != r and not ((m2 >> w) & 1):
                        dfs(w, dep + 1, m2)
            dfs(f0, 1, 0)
        for b1 in range(3):
            for b2 in range(b1 + 1, 3):
                for t in set(bkt[b1]) & set(bkt[b2]):
                    for m1 in bkt[b1][t]:
                        for m2 in bkt[b2][t]:
                            if (m1 & m2) == 0:
                                return True
    return False


def has_dyadic_theta_mitm(adj: list[list[int]], roots: list[int], branch_len: int) -> bool:
    for r in roots:
        bkt: list[dict[int, set[int]]] = [defaultdict(set) for _ in range(3)]
        for br, f0 in enumerate(adj[r]):
            def dfs(u: int, dep: int, msk: int) -> None:
                if dep == branch_len:
                    bkt[br][u].add(msk)
                    return
                m2 = msk | (1 << u)
                for w in adj[u]:
                    if w != r and not ((m2 >> w) & 1):
                        dfs(w, dep + 1, m2)
            dfs(f0, 1, 0)
        common = set(bkt[0]) & set(bkt[1]) & set(bkt[2])
        for t in common:
            l0, l1, l2 = bkt[0][t], bkt[1][t], bkt[2][t]
            for m0 in l0:
                for m1 in l1:
                    if m0 & m1:
                        continue
                    u01 = m0 | m1
                    for m2 in l2:
                        if (u01 & m2) == 0:
                            return True
    return False


# ---------------------------------------------------------------------------
# 1. Semidirect Extensions A \rtimes_sigma C_3 (Universal & Finite Controls)
# ---------------------------------------------------------------------------

def verify_semidirect_c3() -> dict:
    def rot_e(p0: int, p1: int, k: int) -> tuple[int, int]:
        k %= 3
        if k == 0:
            return (p0, p1)
        if k == 1:
            return (-p1, p0 - p1)
        return (p1 - p0, -p0)

    def mul_e(g1, g2):
        v1, t1 = g1; v2, t2 = g2
        a0, a1 = rot_e(v2[0], v2[1], t1); b0, b1 = rot_e(v2[2], v2[3], t1)
        return ((v1[0] + a0, v1[1] + a1, v1[2] + b0, v1[3] + b1), (t1 + t2) % 3)

    def inv_e(g):
        v, t = g; nt = (-t) % 3
        a0, a1 = rot_e(v[0], v[1], nt); b0, b1 = rot_e(v[2], v[3], nt)
        return ((-a0, -a1, -b0, -b1), nt)

    id_e = ((0, 0, 0, 0), 0)

    def rot_g(v: tuple[int, ...], k: int) -> tuple[int, ...]:
        k %= 3
        if k == 0:
            return v
        if k == 1:
            return (v[2], v[0], v[1], v[5], v[3], v[4])
        return (v[1], v[2], v[0], v[4], v[5], v[3])

    def mul_g(g1, g2):
        v1, t1 = g1; v2, t2 = g2; rv = rot_g(v2, t1)
        return (tuple(v1[i] + rv[i] for i in range(6)), (t1 + t2) % 3)

    def inv_g(g):
        v, t = g; nt = (-t) % 3; rv = rot_g(v, nt)
        return (tuple(-x for x in rv), nt)

    id_g = ((0, 0, 0, 0, 0, 0), 0)

    def walk_word(word: str, id_elem, sha, shb, mul_fn, inv_fn):
        sh = (id_elem, sha, shb); iv = (id_elem, inv_fn(sha), inv_fn(shb))
        cur = id_elem; states = []
        for i, ch in enumerate(word):
            states.append(cur)
            cur = mul_fn(cur, sh[int(ch)] if i % 2 == 0 else iv[int(ch)])
        return cur, states

    def analyze_short_closure(word: str, id_elem, sha, shb, mul_fn, inv_fn, expected_len: int) -> dict:
        assert len(word) == expected_len
        assert all(word[i] != word[(i + 1) % expected_len] for i in range(expected_len))
        end_el, states = walk_word(word, id_elem, sha, shb, mul_fn, inv_fn)
        assert end_el == id_elem
        half = expected_len // 2
        assert len(set(states[0::2])) == half and len(set(states[1::2])) == half
        sh = (id_elem, sha, shb); iv = (id_elem, inv_fn(sha), inv_fn(shb))
        colls = {sha, inv_fn(sha), shb, inv_fn(shb), mul_fn(inv_fn(sha), shb), mul_fn(inv_fn(shb), sha)}
        short48: dict = {}
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
        conj_set = [id_elem, sha, inv_fn(sha), shb, inv_fn(shb)]
        for x in (sha, inv_fn(sha), shb, inv_fn(shb)):
            for y in (sha, inv_fn(sha), shb, inv_fn(shb)):
                conj_set.append(mul_fn(x, y))
        conj_short: dict = {}
        for st, info in short48.items():
            for sign_st in (st, inv_fn(st)):
                conj_short.setdefault(sign_st, (info[0], info[1], "direct"))
                for g in conj_set:
                    cg = mul_fn(inv_fn(g), mul_fn(sign_st, g))
                    conj_short.setdefault(cg, (info[0], info[1], "conjugate"))
        conj_colls = set(colls)
        for st in colls:
            for g in conj_set:
                conj_colls.add(mul_fn(inv_fn(g), mul_fn(st, g)))
        return {"states": states, "colls": colls, "short48_direct": short48, "conj_short": conj_short, "conj_colls": conj_colls}

    eisenstein = {}
    for label, word, sha, shb in [
        ("Eisen_Case_1_0", W_E10, ((1, 0, 0, 0), 1), ((0, 0, 1, 0), 0)),
        ("Eisen_Case_1_2", W_E12, ((1, 0, 0, 0), 1), ((0, 0, 1, 0), 2)),
    ]:
        data = analyze_short_closure(word, id_e, sha, shb, mul_e, inv_e, 16)
        states = data["states"]; counts: Counter[str] = Counter(); witnesses = set()
        for i in range(16):
            for j in range(i + 2, 16, 2):
                d = mul_e(inv_e(states[i]), states[j])
                if d in data["colls"]:
                    counts["collapse"] += 1
                elif d in data["short48_direct"]:
                    counts[f"len{data['short48_direct'][d][0]}_direct"] += 1; witnesses.add(str(d))
                elif inv_e(d) in data["short48_direct"]:
                    counts[f"len{data['short48_direct'][inv_e(d)][0]}_inverse"] += 1; witnesses.add(str(d))
                else:
                    raise AssertionError(f"Uncovered Eisenstein diff in {label}: {d}")
        eisenstein[label] = {"word": word, "pair_classification_counts": dict(counts), "unique_short_witness_count": len(witnesses), "uncovered_pairs": 0}

    sha10, shb10 = ((1, 0, 0, 0, 0, 0), 1), ((0, 0, 0, 1, 0, 0), 0)
    d10 = analyze_short_closure(W_G10, id_g, sha10, shb10, mul_g, inv_g, 16)
    comm_10 = mul_g(mul_g(inv_g(sha10), inv_g(shb10)), mul_g(sha10, shb10))
    comm_orbits10 = {(rot_g(sgn[0], k), 0) for sgn in (comm_10, inv_g(comm_10)) for k in range(3)}
    b_sq_rel = ((0, 0, 0, 1, 1, 0), 0)
    c10: Counter[str] = Counter(); special10 = set()
    for i in range(16):
        for j in range(i + 2, 16, 2):
            d = mul_g(inv_g(d10["states"][i]), d10["states"][j])
            if d in d10["conj_colls"]: c10["collapse"] += 1
            elif d in d10["conj_short"]: c10[f"len{d10['conj_short'][d][0]}"] += 1
            elif d in comm_orbits10: c10["commutator_ab"] += 1; special10.add("[a,b]=1 => abelian")
            elif d == b_sq_rel: c10["sigma_plus_1_b"] += 1; special10.add("(1+sigma)b=0 => 2b=0 => C4 (0202)")
            else: raise AssertionError(f"Unexpected diff in General Case(1,0): {d}")

    sha12, shb12 = ((1, 0, 0, 0, 0, 0), 1), ((0, 0, 0, 1, 0, 0), 2)
    d12 = analyze_short_closure(W_G12, id_g, sha12, shb12, mul_g, inv_g, 32)
    comm_12 = mul_g(mul_g(inv_g(sha12), inv_g(shb12)), mul_g(sha12, shb12))
    assert comm_12 == ((1, 0, -1, -1, 1, 0), 0)
    comm_orbits12 = {(rot_g(sgn[0], k), 0) for sgn in (comm_12, inv_g(comm_12)) for k in range(3)}
    c12: Counter[str] = Counter()
    for i in range(32):
        for j in range(i + 2, 32, 2):
            d = mul_g(inv_g(d12["states"][i]), d12["states"][j])
            if d in d12["conj_colls"]: c12["collapse"] += 1
            elif d in d12["conj_short"]: c12[f"len{d12['conj_short'][d][0]}"] += 1
            elif d in comm_orbits12: c12["abelian_commutator_sigma_k_ab"] += 1
            else: raise AssertionError(f"Unexpected diff in General Case(1,2): {d}")

    general = {
        "General_Case_1_0": {"word16": W_G10, "pair_classification_counts": dict(c10), "algebraic_reductions": sorted(special10), "uncovered_pairs": 0},
        "General_Case_1_2": {"word32": W_G12, "comm_ab": list(comm_12[0]), "pair_classification_counts": dict(c12), "uncovered_pairs": 0},
    }

    def shortest_pow2_at_root(elems: list, id_elem, a, b, mul_fn, lengths=(4, 8, 16, 32)) -> int | None:
        adj, _ = build_haar_adj_connected(elems, id_elem, a, b, mul_fn)
        for L in lengths:
            if has_simple_cycle_mitm(adj, [0], L):
                return L
        return None

    controls = {}
    for p in (2, 3, 5):
        def mul_fp3(x, y, modp=p):
            v1, t1 = x; v2, t2 = y; t = t1 % 3
            rv = v2 if t == 0 else ((v2[2], v2[0], v2[1]) if t == 1 else (v2[1], v2[2], v2[0]))
            return (((v1[0] + rv[0]) % modp, (v1[1] + rv[1]) % modp, (v1[2] + rv[2]) % modp), (t1 + t2) % 3)
        def inv_fp3(x, modp=p):
            v, t = x; nt = (-t) % 3
            rv = v if nt == 0 else ((v[2], v[0], v[1]) if nt == 1 else (v[1], v[2], v[0]))
            return (((-rv[0]) % modp, (-rv[1]) % modp, (-rv[2]) % modp), nt)
        id_fp3 = ((0, 0, 0), 0)
        elems = [((x, y, z), t) for x in range(p) for y in range(p) for z in range(p) for t in range(3)]
        if p == 5:
            pairs = [("case10", ((1, 2, 0), 1), ((1, 0, 3), 0)), ("case12", ((1, 2, 0), 1), ((0, 1, 3), 2))]
        else:
            pairs = [("case10", ((1, 0, 0), 1), ((1, 1, 0), 0) if p != 2 else ((1, 0, 0), 0)), ("case12", ((1, 0, 0), 1), ((0, 1, 0), 2))]
        lens = {}
        for tag, a, b in pairs:
            if p < 5:
                found = shortest_pow2_at_root(elems, id_fp3, a, b, mul_fp3, (4, 8, 16, 32))
                assert found is not None; lens[tag] = found
            else:
                w_target = W_G10 if tag == "case10" else W_G12
                end_el, states = walk_word(w_target, id_fp3, a, b, mul_fp3, inv_fp3)
                half = len(w_target) // 2
                simple_w = end_el == id_fp3 and len(set(states[0::2])) == half and len(set(states[1::2])) == half
                lens[tag] = len(w_target) if simple_w else shortest_pow2_at_root(elems, id_fp3, a, b, mul_fp3, (4, 8, 16))
        controls[f"F_{p}^3_rtimes_C3_order_{3*(p**3)}"] = lens

    def mul_105(x, y): return ((x[0] + y[0]) % 5, (x[1] + pow(2, x[2], 7) * y[1]) % 7, (x[2] + y[2]) % 3)
    elems_105 = [(c, u, t) for c in range(5) for u in range(7) for t in range(3)]
    controls["C5_x_(C7_rtimes_C3)_order_105"] = {
        "case10_pow2": shortest_pow2_at_root(elems_105, (0, 0, 0), (1, 1, 1), (2, 1, 0), mul_105, (4, 8, 16, 32)),
        "case12_pow2": shortest_pow2_at_root(elems_105, (0, 0, 0), (1, 1, 1), (2, 2, 2), mul_105, (4, 8, 16, 32)),
    }

    def mul_93(x, y): return ((x[0] + pow(5, x[1], 31) * y[0]) % 31, (x[1] + y[1]) % 3)
    elems_93 = [(u, t) for u in range(31) for t in range(3)]
    c93_hist: Counter[int] = Counter()
    for u1 in (0, 1, 3):
        for t1 in (1, 2):
            for u2 in (1, 2, 7, 11):
                for t2 in (0, 1, 2):
                    a, b = (u1, t1), (u2, t2)
                    if len({(0, 0), a, b}) < 3: continue
                    L = shortest_pow2_at_root(elems_93, (0, 0), a, b, mul_93, (4, 8, 16))
                    assert L is not None; c93_hist[L] += 1
    controls["C31_rtimes_C3_order_93"] = {str(k): v for k, v in sorted(c93_hist.items())}

    def mul_sl23(X, Y):
        return ((X[0]*Y[0]+X[1]*Y[2])%3, (X[0]*Y[1]+X[1]*Y[3])%3, (X[2]*Y[0]+X[3]*Y[2])%3, (X[2]*Y[1]+X[3]*Y[3])%3)
    elems_sl23 = [(a, b, c, d) for a in range(3) for b in range(3) for c in range(3) for d in range(3) if (a*d-b*c)%3 == 1]
    id_sl = (1, 0, 0, 1); sl_hist: Counter[int] = Counter()
    for i in range(1, 24):
        a = elems_sl23[i]; inv_a = (a[3], (-a[1])%3, (-a[2])%3, a[0])
        for j in range(i + 1, 24):
            b = elems_sl23[j]; inv_b = (b[3], (-b[1])%3, (-b[2])%3, b[0])
            seen = {id_sl, a, b}; q = deque([id_sl, a, b])
            while q:
                x = q.popleft()
                for s in (a, b, inv_a, inv_b):
                    nx = mul_sl23(x, s)
                    if nx not in seen: seen.add(nx); q.append(nx)
            if len(seen) != 24: continue
            L = shortest_pow2_at_root(elems_sl23, id_sl, a, b, mul_sl23, (4, 8, 16, 32))
            assert L is not None; sl_hist[L] += 1
    controls["SL_2_3_all_generating_pairs"] = {str(k): v for k, v in sorted(sl_hist.items())}

    return {"eisenstein_C4_C8_C16": eisenstein, "general_C4_to_C32": general, "physical_controls": controls}


# ---------------------------------------------------------------------------
# 2. Two-Attachment Cubic Gadgets (n <= 20), Markstrom24-e & 4802V Witness
# ---------------------------------------------------------------------------

def has_cycle_len_exact(n: int, adj: list[list[int]], length: int) -> bool:
    if n < length:
        return False
    half = length // 2
    for s in range(n - length + 1):
        if len(adj[s]) < 2:
            continue
        paths_half: dict[int, list[int]] = defaultdict(list)

        def dfs(u: int, depth: int, mask: int) -> None:
            if depth == half:
                paths_half[u].append(mask)
                return
            for w in adj[u]:
                if w <= s or (mask & (1 << w)):
                    continue
                dfs(w, depth + 1, mask | (1 << w))

        dfs(s, 0, 0)
        for t, masks in paths_half.items():
            if len(masks) < 2:
                continue
            tbit = 1 << t
            uniq = sorted(set(masks))
            for i in range(len(uniq)):
                mi = uniq[i] & ~tbit
                for j in range(i + 1, len(uniq)):
                    if (mi & uniq[j]) == 0:
                        return True
    return False


def canonical_gadget_key(n: int, adj: list[list[int]]) -> tuple:
    def dists_from(src: int) -> list[int]:
        d = [99] * n; d[src] = 0; q = deque([src])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if d[w] == 99: d[w] = d[u] + 1; q.append(w)
        return d
    d0 = dists_from(0); d1 = dists_from(1)

    def solve_for_01(swap01: bool) -> tuple:
        p0, p1 = (1, 0) if swap01 else (0, 1)
        da, db = (d1, d0) if swap01 else (d0, d1)
        init_feats = {v: (da[v], db[v], len(adj[v])) for v in range(2, n)}
        init_ranks = {k: i for i, k in enumerate(sorted(set(init_feats.values())))}
        colors = {v: init_ranks[init_feats[v]] for v in range(2, n)}
        for _ in range(4):
            nxt = {}
            for v in range(2, n):
                nb = tuple(sorted((-2 if w == p0 else (-1 if w == p1 else colors[w])) for w in adj[v]))
                nxt[v] = (colors[v], nb)
            ranks = {k: i for i, k in enumerate(sorted(set(nxt.values())))}
            colors = {v: ranks[nxt[v]] for v in range(2, n)}
        buckets: dict[int, list[int]] = defaultdict(list)
        for v in range(2, n): buckets[colors[v]].append(v)
        ordered_buckets = [buckets[r] for r in sorted(buckets)]
        best_edges = None; perm = [0] * n; perm[0], perm[1] = p0, p1

        def search_buckets(bidx: int, pos: int) -> None:
            nonlocal best_edges
            if bidx == len(ordered_buckets):
                inv_map = [0] * n
                for ni, ov in enumerate(perm): inv_map[ov] = ni
                edges = []
                for nu in range(n):
                    ou = perm[nu]
                    for ov in adj[ou]:
                        nv = inv_map[ov]
                        if nu < nv: edges.append((nu, nv))
                edges.sort(); tup = tuple(edges)
                if best_edges is None or tup < best_edges: best_edges = tup
                return
            grp = ordered_buckets[bidx]
            for choice in permutations(grp):
                for off, ov in enumerate(choice): perm[pos + off] = ov
                search_buckets(bidx + 1, pos + len(grp))

        search_buckets(0, 2)
        return best_edges  # type: ignore

    return min(solve_for_01(False), solve_for_01(True))


def _solve_gadget_subproblem(task: tuple) -> tuple[int, int, list[tuple[str, list[list[int]]]]]:
    """Top-level picklable worker for Windows ProcessPoolExecutor."""
    (n, seed_name, adj_tup, need_tup, u_start, ff_start, rem_start, act_start,
     enable_c8_prune, enable_cap_prune, enable_sym, check_c8_parity, c8_so_far) = task
    adj_mask = list(adj_tup)
    need = list(need_tup)
    is_s3 = (seed_name == "III_dist_ge3")

    c4_free_raw = 0
    c8_parity_disc = 0
    found_c4: list[list[list[int]]] = []
    found_c4c8: list[tuple[str, list[list[int]]]] = []

    def creates_c8_fast(u: int) -> bool:
        m_u = adj_mask[u]
        if (m_u & (m_u - 1)) == 0:
            return False
        u_bit = 1 << u; prev_reach: list[list[int]] = [[] for _ in range(n)]
        mm = m_u; first_nbr = True
        while mm:
            la = mm & -mm; mm ^= la; a = la.bit_length() - 1; ua = u_bit | la
            cur_entries = []; m1 = adj_mask[a] & ~u_bit
            while m1:
                l1 = m1 & -m1; m1 ^= l1; x1 = l1.bit_length() - 1; ual1 = ua | l1
                m2 = adj_mask[x1] & ~ua
                while m2:
                    l2 = m2 & -m2; m2 ^= l2; x2 = l2.bit_length() - 1; internal = ual1 | l2
                    m3 = adj_mask[x2] & ~ual1
                    while m3:
                        l3 = m3 & -m3; m3 ^= l3; x3 = l3.bit_length() - 1
                        if not first_nbr:
                            for pm in prev_reach[x3]:
                                if (pm & internal) == 0:
                                    return True
                        cur_entries.append((x3, internal & ~u_bit))
            for x3, im in cur_entries:
                prev_reach[x3].append(im)
            first_nbr = False
        return False

    def bt(u: int, ff: int, rem_deg_sum: int, act_mask: int, pruned_c8: bool) -> None:
        nonlocal c4_free_raw, c8_parity_disc
        while u < n and need[u] == 0:
            u += 1
        if u == n:
            seen = 1; q = deque([0])
            while q:
                x = q.popleft(); m = adj_mask[x] & ~seen
                while m:
                    l = m & -m; seen |= l; q.append(l.bit_length() - 1); m ^= l
            if seen != (1 << n) - 1:
                return
            adj = [[w for w in range(n) if (adj_mask[x] >> w) & 1] for x in range(n)]
            c4_free_raw += 1
            if not enable_c8_prune:
                found_c4.append(adj)
            has8 = has_cycle_len_exact(n, adj, 8)
            if check_c8_parity and (pruned_c8 != has8):
                c8_parity_disc += 1
            if not has8:
                found_c4c8.append((seed_name, adj))
            return
        if u >= ff:
            return
        kn = need[u]; r_after = rem_deg_sum - 2 * kn
        if enable_cap_prune and (r_after < 0 or r_after > (n - 1 - u) * (n - 2 - u)):
            return
        two_u = 0; m = adj_mask[u]
        while m:
            l = m & -m; two_u |= adj_mask[l.bit_length() - 1]; m ^= l
        two_u &= ~(1 << u)

        forbid_mask = 0
        if enable_sym and is_s3:
            if u == 2:
                forbid_mask |= 1 << 5
            elif u == 3 and not (adj_mask[2] & ((1 << 4) | (1 << 5))):
                forbid_mask |= (1 << 4) | (1 << 5)
            elif u == 4 and not ((adj_mask[2] >> 3) & 1):
                forbid_mask |= 1 << 5

        used_c = [
            w for w in range(u + 1, ff)
            if need[w] > 0 and not ((adj_mask[u] >> w) & 1) and (adj_mask[w] & two_u) == 0 and not ((forbid_mask >> w) & 1)
        ]
        tmax = min(kn, n - ff); tmin = max(0, kn - len(used_c))
        act_without_u = act_mask & ~(1 << u)

        for tf in range(tmax, tmin - 1, -1):
            ff_next = ff + tf; rem_f = n - ff_next
            fresh_bits = ((1 << ff_next) - (1 << ff)) if tf else 0
            nu = kn - tf; fc_list = list(range(ff, ff_next))
            if nu == 0:
                for w in fc_list:
                    adj_mask[u] |= 1 << w; adj_mask[w] |= 1 << u; need[w] -= 1
                need[u] = 0; nxt_act = act_without_u | fresh_bits; possible = True
                if enable_cap_prune:
                    chk = nxt_act
                    while chk:
                        lw = chk & -chk; chk ^= lw; w_idx = lw.bit_length() - 1
                        if need[w_idx] > (nxt_act & ~lw & ~adj_mask[w_idx]).bit_count() + rem_f:
                            possible = False; break
                if possible:
                    c8_now = creates_c8_fast(u)
                    if (not enable_c8_prune) or (not c8_now):
                        bt(u + 1, ff_next, r_after, nxt_act, pruned_c8 or c8_now)
                need[u] = kn
                for w in fc_list:
                    adj_mask[u] ^= 1 << w; adj_mask[w] ^= 1 << u; need[w] += 1
            else:
                for comb in combinations(used_c, nu):
                    ok = True
                    for i1 in range(nu):
                        a = comb[i1]
                        for i2 in range(i1 + 1, nu):
                            if adj_mask[a] & adj_mask[comb[i2]]:
                                ok = False; break
                        if not ok:
                            break
                    if not ok:
                        continue
                    nxt_act = act_without_u | fresh_bits
                    for w in comb:
                        adj_mask[u] |= 1 << w; adj_mask[w] |= 1 << u; need[w] -= 1
                        if need[w] == 0:
                            nxt_act ^= 1 << w
                    for w in fc_list:
                        adj_mask[u] |= 1 << w; adj_mask[w] |= 1 << u; need[w] -= 1
                    need[u] = 0; possible = True
                    if enable_cap_prune:
                        chk = nxt_act
                        while chk:
                            lw = chk & -chk; chk ^= lw; w_idx = lw.bit_length() - 1
                            if need[w_idx] > (nxt_act & ~lw & ~adj_mask[w_idx]).bit_count() + rem_f:
                                possible = False; break
                    if possible:
                        c8_now = creates_c8_fast(u)
                        if (not enable_c8_prune) or (not c8_now):
                            bt(u + 1, ff_next, r_after, nxt_act, pruned_c8 or c8_now)
                    need[u] = kn
                    for w in fc_list:
                        adj_mask[u] ^= 1 << w; adj_mask[w] ^= 1 << u; need[w] += 1
                    for w in comb:
                        adj_mask[u] ^= 1 << w; adj_mask[w] ^= 1 << u; need[w] += 1

    bt(u_start, ff_start, rem_start, act_start, c8_so_far)
    return c4_free_raw, c8_parity_disc, found_c4c8 + ([("__C4__", a) for a in found_c4] if not enable_c8_prune else [])


def _expand_tasks(n: int, split_u: int, enable_c8_prune: bool, enable_cap_prune: bool,
                  enable_sym: bool, check_c8_parity: bool) -> list[tuple]:
    seeds = [
        ("Ia_tri_012", [(0, 1), (0, 2), (1, 2)], 3),
        ("Ib_adj_01", [(0, 1), (0, 2), (1, 3)], 4),
        ("II_dist2", [(0, 2), (0, 3), (1, 2), (1, 4)], 5),
        ("III_dist_ge3", [(0, 2), (0, 3), (1, 4), (1, 5)], 6),
    ]
    tasks: list[tuple] = []
    for seed_name, init_edges, k_used in seeds:
        if k_used > n:
            continue
        adj_mask = [0] * n; need = [0, 0] + [3] * (n - 2)
        for a, b in init_edges:
            adj_mask[a] |= 1 << b; adj_mask[b] |= 1 << a
            if a >= 2: need[a] -= 1
            if b >= 2: need[b] -= 1
        is_s3 = (seed_name == "III_dist_ge3")

        def creates_c8_fast_prefix(u: int) -> bool:
            m_u = adj_mask[u]
            if (m_u & (m_u - 1)) == 0: return False
            u_bit = 1 << u; prev_reach: list[list[int]] = [[] for _ in range(n)]
            mm = m_u; first_nbr = True
            while mm:
                la = mm & -mm; mm ^= la; a = la.bit_length() - 1; ua = u_bit | la
                cur_entries = []; m1 = adj_mask[a] & ~u_bit
                while m1:
                    l1 = m1 & -m1; m1 ^= l1; x1 = l1.bit_length() - 1; ual1 = ua | l1
                    m2 = adj_mask[x1] & ~ua
                    while m2:
                        l2 = m2 & -m2; m2 ^= l2; x2 = l2.bit_length() - 1; internal = ual1 | l2
                        m3 = adj_mask[x2] & ~ual1
                        while m3:
                            l3 = m3 & -m3; m3 ^= l3; x3 = l3.bit_length() - 1
                            if not first_nbr:
                                for pm in prev_reach[x3]:
                                    if (pm & internal) == 0: return True
                            cur_entries.append((x3, internal & ~u_bit))
                for x3, im in cur_entries: prev_reach[x3].append(im)
                first_nbr = False
            return False

        def expand(u: int, ff: int, rem_deg_sum: int, act_mask: int, pruned_c8: bool) -> None:
            while u < n and need[u] == 0: u += 1
            if u >= split_u or u == n:
                tasks.append((n, seed_name, tuple(adj_mask), tuple(need), u, ff, rem_deg_sum, act_mask,
                              enable_c8_prune, enable_cap_prune, enable_sym, check_c8_parity, pruned_c8))
                return
            if u >= ff: return
            kn = need[u]; r_after = rem_deg_sum - 2 * kn
            if enable_cap_prune and (r_after < 0 or r_after > (n - 1 - u) * (n - 2 - u)): return
            two_u = 0; m = adj_mask[u]
            while m: l = m & -m; two_u |= adj_mask[l.bit_length() - 1]; m ^= l
            two_u &= ~(1 << u)
            forbid_mask = 0
            if enable_sym and is_s3:
                if u == 2: forbid_mask |= 1 << 5
                elif u == 3 and not (adj_mask[2] & ((1 << 4) | (1 << 5))): forbid_mask |= (1 << 4) | (1 << 5)
                elif u == 4 and not ((adj_mask[2] >> 3) & 1): forbid_mask |= 1 << 5
            used_c = [
                w for w in range(u + 1, ff)
                if need[w] > 0 and not ((adj_mask[u] >> w) & 1) and (adj_mask[w] & two_u) == 0 and not ((forbid_mask >> w) & 1)
            ]
            tmax = min(kn, n - ff); tmin = max(0, kn - len(used_c)); act_without_u = act_mask & ~(1 << u)
            for tf in range(tmax, tmin - 1, -1):
                ff_next = ff + tf; rem_f = n - ff_next
                fresh_bits = ((1 << ff_next) - (1 << ff)) if tf else 0
                nu = kn - tf; fc_list = list(range(ff, ff_next))
                for comb in combinations(used_c, nu):
                    ok = True
                    for i1 in range(nu):
                        for i2 in range(i1 + 1, nu):
                            if adj_mask[comb[i1]] & adj_mask[comb[i2]]: ok = False; break
                        if not ok: break
                    if not ok: continue
                    nxt_act = act_without_u | fresh_bits
                    for w in comb:
                        adj_mask[u] |= 1 << w; adj_mask[w] |= 1 << u; need[w] -= 1
                        if need[w] == 0: nxt_act ^= 1 << w
                    for w in fc_list: adj_mask[u] |= 1 << w; adj_mask[w] |= 1 << u; need[w] -= 1
                    need[u] = 0; possible = True
                    if enable_cap_prune:
                        chk = nxt_act
                        while chk:
                            lw = chk & -chk; chk ^= lw; w_idx = lw.bit_length() - 1
                            if need[w_idx] > (nxt_act & ~lw & ~adj_mask[w_idx]).bit_count() + rem_f: possible = False; break
                    if possible:
                        c8_now = creates_c8_fast_prefix(u)
                        if (not enable_c8_prune) or (not c8_now):
                            expand(u + 1, ff_next, r_after, nxt_act, pruned_c8 or c8_now)
                    need[u] = kn
                    for w in fc_list: adj_mask[u] ^= 1 << w; adj_mask[w] ^= 1 << u; need[w] += 1
                    for w in comb: adj_mask[u] ^= 1 << w; adj_mask[w] ^= 1 << u; need[w] += 1

        expand(2, k_used, sum(need[2:]), (1 << k_used) - (1 << 2), False)
    return tasks


def enumerate_2att_order(n: int, *, enable_c8_prune: bool = True, enable_cap_prune: bool = True,
                         enable_sym: bool = True, check_c8_parity: bool = False,
                         executor: ProcessPoolExecutor | None = None) -> dict:
    split_u = 7 if (executor is not None and n >= 18) else 2
    tasks = _expand_tasks(n, split_u, enable_c8_prune, enable_cap_prune, enable_sym, check_c8_parity)
    if executor is not None and len(tasks) > 1 and n >= 18:
        results = list(executor.map(_solve_gadget_subproblem, tasks, chunksize=4))
    else:
        results = [_solve_gadget_subproblem(t) for t in tasks]

    c4_raw = 0; c8_disc = 0; c4_classes: set[tuple] = set()
    c4c8_map: dict[tuple, tuple[str, list[list[int]]]] = {}; c4c8_raw = 0
    for r_c4, r_disc, adjs in results:
        c4_raw += r_c4; c8_disc += r_disc
        for sname, adj in adjs:
            if sname == "__C4__":
                c4_classes.add(canonical_gadget_key(n, adj))
            else:
                c4c8_raw += 1
                key = canonical_gadget_key(n, adj)
                if key not in c4c8_map: c4c8_map[key] = (sname, adj)

    survivors = []
    for key in sorted(c4c8_map):
        sname, adj = c4c8_map[key]
        spec = set()
        def dfs_sp(u: int, dep: int, msk: int) -> None:
            if u == 1: spec.add(dep); return
            for w in adj[u]:
                if not ((msk >> w) & 1): dfs_sp(w, dep + 1, msk | (1 << w))
        dfs_sp(0, 0, 1); sp = sorted(spec)
        col = {0: 0}; q = deque([0]); bip = True
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in col: col[w] = 1 - col[u]; q.append(w)
                elif col[w] == col[u]: bip = False
        girth = 99
        for s in range(n):
            dist = {s: 0}; par = {}; qq = deque([s])
            while qq:
                u = qq.popleft()
                for w in adj[u]:
                    if w not in dist: dist[w] = dist[u] + 1; par[w] = u; qq.append(w)
                    elif par.get(u) != w: girth = min(girth, dist[u] + dist[w] + 1)
        has16 = has_cycle_len_exact(n, adj, 16)
        min_s, max_s = sp[0], sp[-1]
        survivors.append({
            "seed_origin": sname,
            "edges": [list(e) for e in key],
            "girth": girth, "bipartite": bip, "has_C16": has16,
            "min_S": min_s, "max_S": max_s,
            "stretch_ratio": round(max_s / min_s, 6),
            "satisfies_garcia_ge_2": max_s >= 2 * min_s,
            "analytic_closure_hit_1_3_7": sorted(spec & {1, 3, 7}),
            "spectrum": sp,
        })

    return {
        "n": n, "c4_free_raw": c4_raw,
        "c4_free_canonical": len(c4_classes) if not enable_c8_prune else None,
        "c4_c8_free_raw_leaves_sym": c4c8_raw,
        "c4_c8_free_canonical_classes": len(survivors),
        "c4_c8_c16_free_canonical_classes": sum(1 for r in survivors if not r["has_C16"]),
        "c8_parity_discrepancies": c8_disc,
        "survivors": survivors, "_c4_set": c4_classes,
    }


def verify_gadgets_n20_and_witness() -> dict:
    soundness = []
    for n in (6, 8, 10, 12):
        ref = enumerate_2att_order(n, enable_c8_prune=False, enable_cap_prune=False, enable_sym=False, check_c8_parity=(n in (8, 10)))
        fast = enumerate_2att_order(n, enable_c8_prune=False, enable_cap_prune=True, enable_sym=True, check_c8_parity=(n in (8, 10)))
        assert ref["c4_free_canonical"] == fast["c4_free_canonical"] and ref["_c4_set"] == fast["_c4_set"]
        assert ref["c8_parity_discrepancies"] == 0 and fast["c8_parity_discrepancies"] == 0
        soundness.append({"n": n, "unpruned_c4_classes": ref["c4_free_canonical"], "pruned_sym_c4_classes": fast["c4_free_canonical"], "exact_class_match": True, "c8_parity_discrepancies": 0})

    cpus = min(os.cpu_count() or 4, 8)
    by_order = []; n20_survivors = []
    with ProcessPoolExecutor(max_workers=cpus) as ex:
        for n in range(4, 21, 2):
            r = enumerate_2att_order(n, enable_c8_prune=True, enable_cap_prune=True, enable_sym=True, executor=ex if n >= 18 else None)
            if n <= 18:
                assert r["c4_c8_free_canonical_classes"] == 0 and r["c4_c8_free_raw_leaves_sym"] == 0
            else:
                assert r["c4_c8_free_canonical_classes"] == 3 and r["c4_c8_c16_free_canonical_classes"] == 0
                assert all(s["satisfies_garcia_ge_2"] and s["analytic_closure_hit_1_3_7"] for s in r["survivors"])
                n20_survivors = r["survivors"]
            by_order.append({
                "n": n, "c4_c8_free_raw_leaves_sym": r["c4_c8_free_raw_leaves_sym"],
                "c4_c8_free_canonical_classes": r["c4_c8_free_canonical_classes"],
                "c4_c8_c16_free_canonical_classes": r["c4_c8_c16_free_canonical_classes"],
            })

    # Closure-admissible sharpness control: Markstrom-order 24-vertex {C4, C8}-free cubic graph minus an edge
    adj24 = [[] for _ in range(24)]
    for u, v in MARKSTROM24_EDGES: adj24[u].append(v); adj24[v].append(u)
    assert all(len(row) == 3 for row in adj24) and not has_cycle_len_exact(24, adj24, 4) and not has_cycle_len_exact(24, adj24, 8)
    assert has_cycle_len_exact(24, adj24, 16)
    adj_h24 = [row[:] for row in adj24]; adj_h24[0].remove(1); adj_h24[1].remove(0)
    vis = {0}; q = deque([0])
    while q:
        u = q.popleft()
        for w in adj_h24[u]:
            if w not in vis: vis.add(w); q.append(w)
    assert len(vis) == 24
    sp24_set = set()
    def dfs24(u: int, dep: int, msk: int) -> None:
        if u == 1: sp24_set.add(dep); return
        for w in adj_h24[u]:
            if not ((msk >> w) & 1): dfs24(w, dep + 1, msk | (1 << w))
    dfs24(0, 0, 1); sp24 = sorted(sp24_set); assert not (sp24_set & {1, 3, 7})

    # Genuine {C4, C8, C16}-free 4,802-vertex stretch witness: Haar(UT4(F7); {I, I+E12+E23, I+E23+E34}) - e
    def ut4_mul_7(X, Y):
        x01, x12, x23, x02, x13, x03 = X; y01, y12, y23, y02, y13, y03 = Y
        return ((x01+y01)%7, (x12+y12)%7, (x23+y23)%7, (x02+x01*y12+y02)%7, (x13+x12*y23+y13)%7, (x03+x01*y13+x02*y23+y03)%7)
    def ut4_inv_7(X):
        c = (0,) * 6
        for _ in range(7):
            nx = ut4_mul_7(c, X)
            if nx == (0,) * 6: return c
            c = nx
        raise RuntimeError("bad ut4 inverse")
    A7 = (1, 1, 0, 0, 0, 0); B7 = (0, 1, 1, 0, 0, 0); id7 = (0,) * 6
    sh = (id7, A7, B7); iv = (id7, ut4_inv_7(A7), ut4_inv_7(B7))

    dist_girth = {(0, id7): 0}; par = {}; q = deque([(0, id7)]); girth = 999
    while q:
        side, g = q.popleft(); d = dist_girth[(side, g)]
        if 2 * d >= girth: continue
        ns = 1 - side; steps = sh if side == 0 else iv
        for s in steps:
            ng = ut4_mul_7(g, s)
            if (ns, ng) not in dist_girth: dist_girth[(ns, ng)] = d + 1; par[(ns, ng)] = (side, g); q.append((ns, ng))
            elif par.get((side, g)) != (ns, ng): girth = min(girth, d + dist_girth[(ns, ng)] + 1)
    assert girth == 14

    for root in ((0, id7), (1, id7)):
        bkt = [defaultdict(set) for _ in range(3)]
        for br in range(3):
            def dfs8(side_u, g_u, dep, vis) -> None:
                if dep == 8: bkt[br][(side_u, g_u)].add(vis); return
                vis2 = vis | {(side_u, g_u)}; ns = 1 - side_u; steps = sh if side_u == 0 else iv
                for s in steps:
                    ng = ut4_mul_7(g_u, s); nv = (ns, ng)
                    if nv != root and nv not in vis2: dfs8(ns, ng, dep + 1, vis2)
            first_nv = (1 - root[0], ut4_mul_7(root[1], sh[br] if root[0] == 0 else iv[br]))
            dfs8(first_nv[0], first_nv[1], 1, frozenset())
        for b1 in range(3):
            for b2 in range(b1 + 1, 3):
                for tgt in set(bkt[b1]) & set(bkt[b2]):
                    for v1 in bkt[b1][tgt]:
                        for v2 in bkt[b2][tgt]:
                            assert v1 & v2

    dist_del = {(0, id7): 0}; q = deque([(0, id7)])
    while q:
        side, g = q.popleft(); d = dist_del[(side, g)]
        if (side, g) == (1, id7): break
        ns = 1 - side; steps = sh if side == 0 else iv
        for s in steps:
            ng = ut4_mul_7(g, s)
            if {(side, g), (ns, ng)} == {(0, id7), (1, id7)}: continue
            if (ns, ng) not in dist_del: dist_del[(ns, ng)] = d + 1; q.append((ns, ng))
    min_s = dist_del[(1, id7)]; assert min_s == 13

    path = [(0, id7)]; cur = id7
    for idx_c, ch in enumerate(WORD32_CLASS3):
        cur = ut4_mul_7(cur, sh[int(ch)] if idx_c % 2 == 0 else iv[int(ch)])
        path.append(((idx_c + 1) % 2, cur))
    path_31 = path[1:]
    assert path[-1] == (0, id7) and len(set(path[:-1])) == 32 and path_31[0] == (1, id7) and path_31[-1] == (0, id7) and len(set(path_31)) == 32

    return {
        "soundness_cross_checks": soundness,
        "by_order": by_order,
        "exact_n_min_c4_c8_free": 20,
        "n_min_c4_c8_c16_free_lower_bound": 22,
        "bridge_bound_c4_c8_free": 40,
        "bridge_bound_c4_c8_c16_free": 44,
        "extremal_n20_gadgets": n20_survivors,
        "sharp_closure_admissible_n_min": 24,
        "markstrom24_minus_e_witness": {
            "vertices": 24, "connected": True, "c4_c8_free": True, "closed_has_C16": True,
            "deleted_edge": [0, 1], "min_S": sp24[0], "max_S": sp24[-1],
            "closure_forbidden_1_3_7_disjoint": True, "path_spectrum": sp24,
        },
        "genuine_c4_c8_c16_free_witness": {
            "graph": "Haar(UT4(F7); {I, I+E12+E23, I+E23+E34})",
            "total_vertices": 2 * (7 ** 4),
            "exact_girth": girth, "c16_free_verified": True,
            "deleted_edge": ["(0, id)", "(1, id)"],
            "exact_min_S": min_s, "explicit_simple_path_len_lower_bound_on_max_S": 31,
            "stretch_ratio_lower_bound": round(31 / min_s, 6),
            "bridged_ratio_lower_bound": round((31 + 2) / (min_s + 2), 6),
            "satisfies_garcia_ge_2": 31 >= 2 * min_s,
        },
    }


# ---------------------------------------------------------------------------
# 3. Complete Zero-Gap All-2-Generated-Groups Haar Census (3 <= |G| <= 47)
# ---------------------------------------------------------------------------

def make_table(elems: list, mul_fn) -> list[list[int]]:
    idx = {e: i for i, e in enumerate(elems)}; n = len(elems)
    return [[idx[mul_fn(elems[i], elems[j])] for j in range(n)] for i in range(n)]


def table_sig_and_rank(t: list[list[int]]):
    n = len(t)
    id_i = next(i for i in range(n) if all(t[i][j] == j and t[j][i] == j for j in range(n)))
    inv = [next(j for j in range(n) if t[i][j] == id_i) for i in range(n)]
    step = max(1, n // 5)
    for i in range(0, n, step):
        for j in range(0, n, step):
            for k in range(0, n, step):
                assert t[t[i][j]][k] == t[i][t[j][k]]
    ords = []
    for i in range(n):
        c = id_i; k = 0
        while True:
            c = t[c][i]; k += 1
            if c == id_i: ords.append(k); break
    gen_pair = None
    for i in range(n):
        for j in range(i, n):
            vis = {id_i, i, j}; q = deque([id_i, i, j])
            while q:
                u = q.popleft()
                for g in (i, j, inv[i], inv[j]):
                    v = t[u][g]
                    if v not in vis: vis.add(v); q.append(v)
            if len(vis) == n: gen_pair = (i, j); break
        if gen_pair is not None: break
    is_le3gen = gen_pair is not None
    if not is_le3gen and (n & (n - 1)) == 0:
        gens_phi = {t[i][i] for i in range(n)} | {t[t[inv[i]][inv[j]]][t[i][j]] for i in range(n) for j in range(n)}
        phi = set(gens_phi); q = deque(gens_phi)
        while q:
            u = q.popleft()
            for g in gens_phi:
                for w in (t[u][g], t[g][u]):
                    if w not in phi: phi.add(w); q.append(w)
        is_le3gen = (n // len(phi)) <= 8
    center = 0; seen = [False] * n; ccls = []
    for i in range(n):
        if seen[i]: continue
        cls = {t[t[g][i]][inv[g]] for g in range(n)}
        for x in cls: seen[x] = True
        if len(cls) == 1: center += 1
        ccls.append((ords[i], len(cls)))
    ccls.sort()
    comms = {t[t[inv[i]][inv[j]]][t[i][j]] for i in range(n) for j in range(n)}
    der = set(comms); q = deque(comms)
    while q:
        u = q.popleft()
        for c in comms:
            for w in (t[u][c], t[c][u]):
                if w not in der: der.add(w); q.append(w)
    sig = (n, center, len(der), tuple(sorted(Counter(ords).items())), tuple(ccls))
    return sig, gen_pair, is_le3gen, id_i, inv, ords


def tables_iso(d1, d2, t1, t2) -> bool:
    if d1[0] != d2[0]: return False
    _, _, _, id1, _, ords1 = d1; _, _, _, id2, _, ords2 = d2; n = len(t1)
    gens1 = []; gen_sub = {id1}
    for x in range(n):
        if x not in gen_sub:
            gens1.append(x); gen_sub.add(x)
            while True:
                old = len(gen_sub)
                for u in list(gen_sub):
                    for v in list(gen_sub): gen_sub.add(t1[u][v])
                if len(gen_sub) == old: break
            if len(gen_sub) == n: break
    def bt(idx: int, mp: dict[int, int], u2: set[int]) -> bool:
        if idx == len(gens1): return len(mp) == n
        g = gens1[idx]
        if g in mp: return bt(idx + 1, mp, u2)
        og = ords1[g]
        for c2 in range(n):
            if c2 in u2 or ords2[c2] != og: continue
            mp2 = dict(mp); uu = set(u2); mp2[g] = c2; uu.add(c2)
            q = deque([g]); ok = True
            while q and ok:
                x = q.popleft(); fx = mp2[x]
                for y in list(mp2):
                    xy = t1[x][y]; fxy = t2[fx][mp2[y]]
                    if xy in mp2:
                        if mp2[xy] != fxy: ok = False; break
                    else:
                        if ords2[fxy] != ords1[xy] or fxy in uu: ok = False; break
                        mp2[xy] = fxy; uu.add(fxy); q.append(xy)
                    yx = t1[y][x]; fyx = t2[mp2[y]][fx]
                    if yx in mp2:
                        if mp2[yx] != fyx: ok = False; break
                    else:
                        if ords2[fyx] != ords1[yx] or fyx in uu: ok = False; break
                        mp2[yx] = fyx; uu.add(fyx); q.append(yx)
            if ok and bt(idx + 1, mp2, uu): return True
        return False
    return bt(0, {id1: id2}, {id2})


def all_automorphisms(t, id_i, inv, ords):
    n = len(t); gens = []; sub = {id_i}
    for x in range(n):
        if x not in sub:
            gens.append(x); sub.add(x)
            while True:
                old = len(sub)
                for u in list(sub):
                    for v in list(sub): sub.add(t[u][v])
                if len(sub) == old: break
            if len(sub) == n: break
    autos = []
    def bt(idx: int, mp: dict[int, int], u2: set[int]) -> None:
        if idx == len(gens):
            if len(mp) == n: autos.append(tuple(mp[i] for i in range(n)))
            return
        g = gens[idx]
        if g in mp: bt(idx + 1, mp, u2); return
        og = ords[g]
        for c2 in range(n):
            if c2 in u2 or ords[c2] != og: continue
            mp2 = dict(mp); uu = set(u2); mp2[g] = c2; uu.add(c2)
            q = deque([g]); ok = True
            while q and ok:
                x = q.popleft(); fx = mp2[x]
                for y in list(mp2):
                    xy = t[x][y]; fxy = t[fx][mp2[y]]
                    if xy in mp2:
                        if mp2[xy] != fxy: ok = False; break
                    else:
                        if ords[fxy] != ords[xy] or fxy in uu: ok = False; break
                        mp2[xy] = fxy; uu.add(fxy); q.append(xy)
                    yx = t[y][x]; fyx = t[mp2[y]][fx]
                    if yx in mp2:
                        if mp2[yx] != fyx: ok = False; break
                    else:
                        if ords[fyx] != ords[yx] or fyx in uu: ok = False; break
                        mp2[yx] = fyx; uu.add(fyx); q.append(yx)
            if ok: bt(idx + 1, mp2, uu)
    bt(0, {id_i: id_i}, {id_i})
    return autos


def cyclic_c2_extensions(groups_tables: list[list[list[int]]], only_2gen: bool = False):
    res = []; by_sig = {}
    for t in groups_tables:
        m = len(t); d = table_sig_and_rank(t); _, _, _, id_i, inv, ords = d
        autos = all_automorphisms(t, id_i, inv, ords)
        inn = [tuple(t[t[h0][x]][inv[h0]] for x in range(m)) for h0 in range(m)]
        for phi in autos:
            phi2 = tuple(phi[phi[x]] for x in range(m))
            for h0 in range(m):
                if phi[h0] != h0 or phi2 != inn[h0]: continue
                nt = [[0] * (2 * m) for _ in range(2 * m)]
                for h1 in range(m):
                    for h2 in range(m):
                        nt[h1][h2] = t[h1][h2]; nt[h1][m + h2] = m + t[h1][h2]
                        ph2 = phi[h2]; nt[m + h1][h2] = m + t[h1][ph2]; nt[m + h1][m + h2] = t[t[h1][ph2]][h0]
                nd = table_sig_and_rank(nt)
                if only_2gen and nd[1] is None: continue
                sig = nd[0]; bucket = by_sig.setdefault(sig, [])
                if not any(tables_iso(nd, od, nt, ot) for od, ot in bucket):
                    bucket.append((nd, nt)); res.append((nd, nt))
    return res


def verify_low_order_haar_census() -> dict:
    g4 = [make_table(list(range(4)), lambda x, y: (x + y) % 4),
          make_table([(a, b) for a in (0, 1) for b in (0, 1)], lambda x, y: (x[0] ^ y[0], x[1] ^ y[1]))]
    g8 = cyclic_c2_extensions(g4, only_2gen=False)
    g16 = cyclic_c2_extensions([t for _, t in g8], only_2gen=False)
    g32_2gen = cyclic_c2_extensions([t for d, t in g16 if d[2]], only_2gen=True)
    assert len(g8) == 5 and len(g16) == 14 and len(g32_2gen) == 20

    s4 = list(permutations(range(4)))
    a4 = [p for p in s4 if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
    g12 = [
        make_table(list(range(12)), lambda x, y: (x + y) % 12),
        make_table([(a, b) for a in range(6) for b in (0, 1)], lambda x, y: ((x[0] + y[0]) % 6, x[1] ^ y[1])),
        make_table([(a, b) for a in range(6) for b in (0, 1)], lambda x, y: ((x[0] + (-1 if x[1] else 1) * y[0]) % 6, x[1] ^ y[1])),
        make_table([(a, b) for a in range(3) for b in range(4)], lambda x, y: ((x[0] + (2 if x[1] % 2 else 1) * y[0]) % 3, (x[1] + y[1]) % 4)),
        make_table(a4, lambda p, q: tuple(p[q[i]] for i in range(4))),
    ]
    g24_all = cyclic_c2_extensions(g12, only_2gen=False)
    sl23 = [(a, b, c, d) for a in range(3) for b in range(3) for c in range(3) for d in range(3) if (a * d - b * c) % 3 == 1]
    t_sl23 = make_table(sl23, lambda x, y: ((x[0]*y[0]+x[1]*y[2])%3, (x[0]*y[1]+x[1]*y[3])%3, (x[2]*y[0]+x[3]*y[2])%3, (x[2]*y[1]+x[3]*y[3])%3))
    d_sl23 = table_sig_and_rank(t_sl23)
    if not any(tables_iso(d_sl23, od, t_sl23, ot) for od, ot in g24_all if od[0] == d_sl23[0]):
        g24_all.append((d_sl23, t_sl23))
    assert len(g24_all) == 15

    cyc = lambda m: (f"C_{m}", make_table(list(range(m)), lambda x, y: (x + y) % m))
    ab2 = lambda d1, d2: (f"C{d1}xC{d2}", make_table([(x, y) for x in range(d1) for y in range(d2)],
                                                     lambda a, b: ((a[0] + b[0]) % d1, (a[1] + b[1]) % d2)))
    semi = lambda nm, q, m, alpha: (nm, make_table([(u, t) for u in range(q) for t in range(m)],
                                                   lambda x, y: ((x[0] + pow(alpha, x[1], q) * y[0]) % q, (x[1] + y[1]) % m)))
    def dic(m4: int):
        half = m4 // 2; q = half // 2
        return (f"Dic_{m4}", make_table([(k, e) for k in range(half) for e in (0, 1)],
                                        lambda x, y: (((x[0] - y[0] + q) % half, 0) if (x[1] == 1 and y[1] == 1)
                                                      else (((x[0] + y[0]) % half, y[1]) if x[1] == 0 else ((x[0] - y[0]) % half, 1)))))

    by_order: dict[int, list[tuple[str, list[list[int]], bool]]] = {}
    def label_2gp(prefix: str, items):
        out = []; ab_idx = 0; nab_idx = 0
        for d, t in items:
            if d[1] is None: continue
            is_ab = (d[0][2] == 1)
            if is_ab: ab_idx += 1; nm = f"{prefix}_ab{ab_idx}"
            else: nab_idx += 1; nm = f"{prefix}_nab{nab_idx}"
            out.append((nm, t, is_ab))
        return out

    by_order[8] = label_2gp("O8", g8); by_order[16] = label_2gp("O16", g16)
    by_order[32] = label_2gp("O32", g32_2gen); by_order[24] = label_2gp("O24", g24_all)
    assert len(by_order[8]) == 4 and len(by_order[16]) == 9 and len(by_order[32]) == 20 and len(by_order[24]) == 13

    def p23(A, k):
        r = (1, 0, 0, 1)
        for _ in range(k): r = ((r[0]*A[0]+r[1]*A[2])%3, (r[0]*A[1]+r[1]*A[3])%3, (r[2]*A[0]+r[3]*A[2])%3, (r[2]*A[1]+r[3]*A[3])%3)
        return r
    ap23 = lambda A, v: ((A[0]*v[0]+A[1]*v[1])%3, (A[2]*v[0]+A[3]*v[1])%3)
    mm23 = lambda X, Y: ((X[0]*Y[0]+X[1]*Y[2])%3, (X[0]*Y[1]+X[1]*Y[3])%3, (X[2]*Y[0]+X[3]*Y[2])%3, (X[2]*Y[1]+X[3]*Y[3])%3)
    c36 = [
        cyc(36), ab2(2, 18), ab2(3, 12), ab2(6, 6), semi("Dic_36", 9, 4, 8),
        ("D_18", make_table([(u, t) for u in range(18) for t in (0, 1)], lambda x, y: ((x[0] + (17 if x[1] else 1) * y[0]) % 18, x[1] ^ y[1]))),
        ("A4xC3", make_table([(p, c) for p in a4 for c in range(3)], lambda x, y: (tuple(x[0][y[0][i]] for i in range(4)), (x[1] + y[1]) % 3))),
        ("V4:C9", make_table([(x, y, t) for x in (0, 1) for y in (0, 1) for t in range(9)],
                             lambda a, b: (lambda rot: (a[0] ^ rot[0], a[1] ^ rot[1], (a[2] + b[2]) % 9))([(b[0], b[1]), (b[1], b[0] ^ b[1]), (b[0] ^ b[1], b[0])][a[2] % 3]))),
        ("F9:C4", make_table([(u, v, t) for u in range(3) for v in range(3) for t in range(4)],
                             lambda x, y: (lambda rv: ((x[0] + rv[0]) % 3, (x[1] + rv[1]) % 3, (x[2] + y[2]) % 4))(ap23(p23((0, 1, 2, 0), x[2]), (y[0], y[1]))))),
        ("Dic12xC3", make_table([(u, v, t) for u in range(3) for v in range(3) for t in range(4)],
                                lambda x, y: (lambda rv: ((x[0] + rv[0]) % 3, (x[1] + rv[1]) % 3, (x[2] + y[2]) % 4))(ap23(p23((1, 0, 0, 2), x[2]), (y[0], y[1]))))),
        ("S3xC6", make_table([(u, v, a, b) for u in range(3) for v in range(3) for a in (0, 1) for b in (0, 1)],
                             lambda x, y: (lambda rv: ((x[0] + rv[0]) % 3, (x[1] + rv[1]) % 3, x[2] ^ y[2], x[3] ^ y[3]))(ap23(mm23(p23((1, 0, 0, 1), x[2]), p23((1, 0, 0, 2), x[3])), (y[0], y[1]))))),
        ("S3xS3", make_table([(u, v, a, b) for u in range(3) for v in range(3) for a in (0, 1) for b in (0, 1)],
                             lambda x, y: (lambda rv: ((x[0] + rv[0]) % 3, (x[1] + rv[1]) % 3, x[2] ^ y[2], x[3] ^ y[3]))(ap23(mm23(p23((1, 0, 0, 2), x[2]), p23((2, 0, 0, 1), x[3])), (y[0], y[1]))))),
    ]
    by_order[36] = []; seen36: dict = {}
    for nm, t in c36:
        d = table_sig_and_rank(t)
        assert d[1] is not None and not any(tables_iso(d, od, t, ot) for od, ot in seen36.get(d[0], []))
        seen36.setdefault(d[0], []).append((d, t)); by_order[36].append((nm, t, d[0][2] == 1))
    assert len(by_order[36]) == 12

    def mul_d4(x, y): return ((x[0] + y[0]) % 4, y[1]) if x[1] == 0 else ((x[0] - y[0]) % 4, 1 ^ y[1])
    def mul_q8(x, y):
        a1, b1 = x; a2, b2 = y
        if b1 == 0: return ((a1 + a2) % 4, b2)
        if b2 == 0: return ((a1 - a2) % 4, 1)
        return ((a1 - a2 + 2) % 4, 0)
    c40 = [cyc(40), ab2(2, 20), semi("C5:C8_2", 5, 8, 2), semi("C5:C8_4", 5, 8, 4)]
    for a, b, nm in ((1, 4, "D5xC4"), (2, 1, "AGL15xC2"), (4, 1, "Dic20xC2")):
        c40.append((nm, make_table([(u, x, y) for u in range(5) for x in range(4) for y in (0, 1)],
                                   lambda p, q, aa=a, bb=b: ((p[0] + pow(aa, p[1], 5) * pow(bb, p[2], 5) * q[0]) % 5, (p[1] + q[1]) % 4, p[2] ^ q[2]))))
    for r, s, nm in ((1, 1, "C5xD4"), (1, 4, "C5:sD4"), (4, 1, "C5:rD4")):
        c40.append((nm, make_table([(u, a, b) for u in range(5) for a in range(4) for b in (0, 1)],
                                   lambda x, y, rr=r, ss=s: ((x[0] + pow(rr, x[1], 5) * pow(ss, x[2], 5) * y[0]) % 5, mul_d4((x[1], x[2]), (y[1], y[2]))[0], mul_d4((x[1], x[2]), (y[1], y[2]))[1]))))
    for i_, j_, nm in ((1, 1, "C5xQ8"), (1, 4, "C5:Q8")):
        c40.append((nm, make_table([(u, a, b) for u in range(5) for a in range(4) for b in (0, 1)],
                                   lambda x, y, ii=i_, jj=j_: ((x[0] + pow(ii, x[1], 5) * pow(jj, x[2], 5) * y[0]) % 5, mul_q8((x[1], x[2]), (y[1], y[2]))[0], mul_q8((x[1], x[2]), (y[1], y[2]))[1]))))
    by_order[40] = []; seen40: dict = {}
    for nm, t in c40:
        d = table_sig_and_rank(t)
        assert d[1] is not None and not any(tables_iso(d, od, t, ot) for od, ot in seen40.get(d[0], []))
        seen40.setdefault(d[0], []).append((d, t)); by_order[40].append((nm, t, d[0][2] == 1))
    assert len(by_order[40]) == 12

    remaining_specs: dict[int, list[tuple[str, list[list[int]]]]] = {
        3: [cyc(3)], 4: [cyc(4), ab2(2, 2)], 5: [cyc(5)], 6: [cyc(6), semi("S_3", 3, 2, 2)],
        7: [cyc(7)], 9: [cyc(9), ab2(3, 3)], 10: [cyc(10), semi("D_5", 5, 2, 4)], 11: [cyc(11)],
        12: [cyc(12), ab2(2, 6), semi("D_6", 6, 2, 5), dic(12), ("A_4", make_table(a4, lambda p, q: tuple(p[q[i]] for i in range(4))))],
        13: [cyc(13)], 14: [cyc(14), semi("D_7", 7, 2, 6)], 15: [cyc(15)], 17: [cyc(17)],
        18: [cyc(18), ab2(3, 6), semi("D_9", 9, 2, 8),
             ("S3xC3", make_table([(u, t, z) for u in range(3) for t in (0, 1) for z in range(3)],
                                  lambda x, y: ((x[0] + (2 if x[1] else 1) * y[0]) % 3, x[1] ^ y[1], (x[2] + y[2]) % 3)))],
        19: [cyc(19)], 20: [cyc(20), ab2(2, 10), semi("D_10", 10, 2, 9), dic(20), semi("AGL(1,5)", 5, 4, 2)],
        21: [cyc(21), semi("C7:C3", 7, 3, 2)], 22: [cyc(22), semi("D_11", 11, 2, 10)], 23: [cyc(23)],
        25: [cyc(25), ab2(5, 5)], 26: [cyc(26), semi("D_13", 13, 2, 12)],
        27: [cyc(27), ab2(3, 9), semi("M27_exp9", 9, 3, 4),
             ("UT3(F3)_exp3", make_table([(i, j, k) for i in range(3) for j in range(3) for k in range(3)],
                                         lambda x, y: ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3, (x[2] + y[2] + x[0] * y[1]) % 3)))],
        28: [cyc(28), ab2(2, 14), semi("D_14", 14, 2, 13), dic(28)], 29: [cyc(29)],
        30: [cyc(30), semi("D_15", 15, 2, 14), semi("C5xS3", 15, 2, 11), semi("C3xD5", 15, 2, 4)],
        31: [cyc(31)], 33: [cyc(33)], 34: [cyc(34), semi("D_17", 17, 2, 16)], 35: [cyc(35)],
        37: [cyc(37)], 38: [cyc(38), semi("D_19", 19, 2, 18)], 39: [cyc(39), semi("C13:C3", 13, 3, 3)], 41: [cyc(41)],
        42: [cyc(42), semi("D_21", 21, 2, 20), semi("C7xS3", 21, 2, 8), semi("C3xD7", 21, 2, 13),
             ("(C7:C3)xC2", make_table([(u, t, e) for u in range(7) for t in range(3) for e in (0, 1)],
                                       lambda x, y: ((x[0] + pow(2, x[1], 7) * y[0]) % 7, (x[1] + y[1]) % 3, x[2] ^ y[2]))),
             semi("C7:C6", 7, 6, 3)],
        43: [cyc(43)], 44: [cyc(44), ab2(2, 22), semi("D_22", 22, 2, 21), dic(44)],
        45: [cyc(45), ab2(3, 15)], 46: [cyc(46), semi("D_23", 23, 2, 22)], 47: [cyc(47)],
    }
    for m, lst in remaining_specs.items():
        by_order[m] = []; seen_m: dict = {}
        for nm, t in lst:
            d = table_sig_and_rank(t)
            assert d[1] is not None and not any(tables_iso(d, od, t, ot) for od, ot in seen_m.get(d[0], []))
            seen_m.setdefault(d[0], []).append((d, t)); by_order[m].append((nm, t, d[0][2] == 1))

    non_2gen_counts = {8: 1, 16: 5, 18: 1, 24: 2, 27: 1, 32: 31, 36: 2, 40: 2}
    for m in range(3, 48):
        assert len(by_order[m]) + non_2gen_counts.get(m, 0) == OEIS_GROUP_COUNTS[m]

    total_groups = 0; total_reanch = 0; total_c4c8 = 0; total_c16_free = 0
    by_order_summary = []
    for m in range(3, 48):
        order_c4c8 = 0; order_ab_c4c8 = 0; order_nab_c4c8 = 0; order_reanch = 0
        nontrivial_groups = []
        for nm, t, is_ab in by_order[m]:
            total_groups += 1
            id_i = next(i for i in range(m) if all(t[i][j] == j and t[j][i] == j for j in range(m)))
            inv = [next(j for j in range(m) if t[i][j] == id_i) for i in range(m)]
            seen_reanch = set(); roots = [0, m]; gp_c4c8 = 0
            for a in range(m):
                if a == id_i: continue
                ia = inv[a]
                for b in range(a + 1, m):
                    if b == id_i: continue
                    best = None
                    for r in (id_i, a, b):
                        ir = inv[r]
                        pair = tuple(sorted(t[ir][x] for x in (id_i, a, b) if x != r))
                        if best is None or pair < best: best = pair
                    if best in seen_reanch: continue
                    seen_reanch.add(best)
                    ib = inv[b]
                    if len({ia, ib, a, t[a][ib], b, t[b][ia]}) < 6: continue
                    seen_g = {id_i, a, b, ia, ib}; q = deque(seen_g); gens = (a, b, ia, ib)
                    while q:
                        x = q.popleft()
                        for g in gens:
                            nx = t[x][g]
                            if nx not in seen_g: seen_g.add(nx); q.append(nx)
                    if len(seen_g) != m: continue
                    adj = [[] for _ in range(2 * m)]
                    for u in range(m):
                        for s in (id_i, a, b):
                            v = m + t[u][s]; adj[u].append(v); adj[v].append(u)
                    if has_simple_cycle_mitm(adj, roots, 8): continue
                    has16 = has_simple_cycle_mitm(adj, roots, 16)
                    has16_32 = True if has16 else has_simple_cycle_mitm(adj, roots, 32)
                    has_th8 = has_dyadic_theta_mitm(adj, roots, 8)
                    assert has16_32 and has_th8
                    if not has16: total_c16_free += 1
                    gp_c4c8 += 1
            order_reanch += len(seen_reanch); total_reanch += len(seen_reanch)
            order_c4c8 += gp_c4c8; total_c4c8 += gp_c4c8
            if is_ab: order_ab_c4c8 += gp_c4c8
            else: order_nab_c4c8 += gp_c4c8
            if gp_c4c8 > 0: nontrivial_groups.append({"group": nm, "abelian": is_ab, "c4c8_free_classes": gp_c4c8})

        if m <= 18: assert order_c4c8 == 0
        by_order_summary.append({
            "order": m, "vertices": 2 * m,
            "oeis_total_groups": OEIS_GROUP_COUNTS[m],
            "two_gen_groups": len(by_order[m]),
            "reanchored_pairs_checked": order_reanch,
            "c4_c8_free_classes": order_c4c8,
            "abelian_c4_c8_free": order_ab_c4c8,
            "nonabelian_c4_c8_free": order_nab_c4c8,
            "groups_with_c4c8_free": nontrivial_groups,
        })

    return {
        "order_range": "3..47", "vertex_range": "6..94",
        "oeis_total_groups_accounted": sum(OEIS_GROUP_COUNTS.values()),
        "two_gen_groups_checked_total": total_groups,
        "reanchored_pairs_checked_total": total_reanch,
        "total_c4_c8_free_classes": total_c4c8,
        "total_c4_c8_c16_free_classes": total_c16_free,
        "missing_C16_or_C32": 0,
        "missing_Theta_8_8_8": 0,
        "all_c4_c8_free_have_C16_and_Theta8": total_c16_free == 0,
        "by_order": by_order_summary,
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    cert_payload = {
        "paper": "Paper III: Power-of-Two Cycles in Semidirect C_3-Extension Cubic Haar Graphs and Two-Attachment Cubic Gadget Bounds",
        "status": "PASS",
        "semidirect_c3": verify_semidirect_c3(),
        "gadgets_n20_and_witness": verify_gadgets_n20_and_witness(),
        "low_order_haar_census": verify_low_order_haar_census(),
    }
    serialized = json.dumps(cert_payload, indent=2) + "\n"
    if write_certs:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(serialized, encoding="utf-8")
    elif CERT_PATH.exists():
        assert CERT_PATH.read_text(encoding="utf-8") == serialized, "Certificate byte-for-byte mismatch!"
        saved = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        current = json.loads(serialized)
        for k in ("semidirect_c3", "gadgets_n20_and_witness", "low_order_haar_census"):
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
        "semidirect_general_case12_wordlen": len(out["semidirect_c3"]["general_C4_to_C32"]["General_Case_1_2"]["word32"]),
        "sl23_pairs_verified": out["semidirect_c3"]["physical_controls"]["SL_2_3_all_generating_pairs"],
        "gadgets_n20_c4c8_classes": [(o["n"], o["c4_c8_free_canonical_classes"]) for o in out["gadgets_n20_and_witness"]["by_order"]],
        "gadgets_n20_c16_free": [o["c4_c8_c16_free_canonical_classes"] for o in out["gadgets_n20_and_witness"]["by_order"]],
        "markstrom24_spectrum_minmax": [
            out["gadgets_n20_and_witness"]["markstrom24_minus_e_witness"]["min_S"],
            out["gadgets_n20_and_witness"]["markstrom24_minus_e_witness"]["max_S"],
        ],
        "ut4_f7_stretch_ge_2": out["gadgets_n20_and_witness"]["genuine_c4_c8_c16_free_witness"]["satisfies_garcia_ge_2"],
        "haar_census_two_gen_groups": out["low_order_haar_census"]["two_gen_groups_checked_total"],
        "haar_census_oeis_groups": out["low_order_haar_census"]["oeis_total_groups_accounted"],
        "haar_census_c4c8_classes": out["low_order_haar_census"]["total_c4_c8_free_classes"],
        "haar_census_c16_free": out["low_order_haar_census"]["total_c4_c8_c16_free_classes"],
        "haar_census_missing_theta8": out["low_order_haar_census"]["missing_Theta_8_8_8"],
    }, indent=2))
