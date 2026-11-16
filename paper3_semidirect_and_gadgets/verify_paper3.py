#!/usr/bin/env python3
"""Standalone standard-library verifier for Paper III:
Power-of-Two Cycles in Semidirect C_3-Extension Cubic Haar Graphs and
Two-Attachment Cubic Gadget Bounds.

Run from repository root or paper3_semidirect_and_gadgets/:
    python verify_paper3.py
    python verify_paper3.py --write-certificates
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "certificates" / "paper3_certificates.json"

# Universal class-3 word reused verbatim for the 4802-vertex UT4(F7) witness
WORD32_CLASS3 = "01010102012012101012012010212012"

# Semidirect A |>_sigma C_3 universal color words (0=1, 1=a, 2=b)
W_E10 = "0101020120102102"
W_E12 = "1021212021210202"
W_G10 = "0102021021202012"
W_G12 = "01202021020201021210201020210212"


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
        v1, t1 = g1
        v2, t2 = g2
        a0, a1 = rot_e(v2[0], v2[1], t1)
        b0, b1 = rot_e(v2[2], v2[3], t1)
        return ((v1[0] + a0, v1[1] + a1, v1[2] + b0, v1[3] + b1), (t1 + t2) % 3)

    def inv_e(g):
        v, t = g
        nt = (-t) % 3
        a0, a1 = rot_e(v[0], v[1], nt)
        b0, b1 = rot_e(v[2], v[3], nt)
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
        v1, t1 = g1
        v2, t2 = g2
        rv = rot_g(v2, t1)
        return (tuple(v1[i] + rv[i] for i in range(6)), (t1 + t2) % 3)

    def inv_g(g):
        v, t = g
        nt = (-t) % 3
        rv = rot_g(v, nt)
        return (tuple(-x for x in rv), nt)

    id_g = ((0, 0, 0, 0, 0, 0), 0)

    def walk_word(word: str, id_elem, sha, shb, mul_fn, inv_fn):
        sh = (id_elem, sha, shb)
        iv = (id_elem, inv_fn(sha), inv_fn(shb))
        cur = id_elem
        states = []
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

        sh = (id_elem, sha, shb)
        iv = (id_elem, inv_fn(sha), inv_fn(shb))
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

        return {
            "states": states,
            "colls": colls,
            "short48_direct": short48,
            "conj_short": conj_short,
            "conj_colls": conj_colls,
        }

    # A. Eisenstein theorem (1 + sigma + sigma^2 = 0 => C4, C8, or C16)
    eisenstein = {}
    for label, word, sha, shb in [
        ("Eisen_Case_1_0", W_E10, ((1, 0, 0, 0), 1), ((0, 0, 1, 0), 0)),
        ("Eisen_Case_1_2", W_E12, ((1, 0, 0, 0), 1), ((0, 0, 1, 0), 2)),
    ]:
        data = analyze_short_closure(word, id_e, sha, shb, mul_e, inv_e, 16)
        states = data["states"]
        counts: Counter[str] = Counter()
        witnesses = set()
        for i in range(16):
            for j in range(i + 2, 16, 2):
                d = mul_e(inv_e(states[i]), states[j])
                if d in data["colls"]:
                    counts["collapse"] += 1
                elif d in data["short48_direct"]:
                    counts[f"len{data['short48_direct'][d][0]}_direct"] += 1
                    witnesses.add(str(d))
                elif inv_e(d) in data["short48_direct"]:
                    counts[f"len{data['short48_direct'][inv_e(d)][0]}_inverse"] += 1
                    witnesses.add(str(d))
                else:
                    raise AssertionError(f"Uncovered Eisenstein diff in {label}: {d}")
        eisenstein[label] = {
            "word": word,
            "pair_classification_counts": dict(counts),
            "unique_short_witness_count": len(witnesses),
            "uncovered_pairs": 0,
        }

    # B. General theorem (sigma^3 = 1 => C4, C8, C16, or C32)
    sha10, shb10 = ((1, 0, 0, 0, 0, 0), 1), ((0, 0, 0, 1, 0, 0), 0)
    d10 = analyze_short_closure(W_G10, id_g, sha10, shb10, mul_g, inv_g, 16)
    comm_10 = mul_g(mul_g(inv_g(sha10), inv_g(shb10)), mul_g(sha10, shb10))
    comm_orbits10 = {(rot_g(sgn[0], k), 0) for sgn in (comm_10, inv_g(comm_10)) for k in range(3)}
    assert ((0, 0, 0, -1, 1, 0), 0) in comm_orbits10
    b_sq_rel = ((0, 0, 0, 1, 1, 0), 0)

    c10: Counter[str] = Counter()
    special10 = set()
    for i in range(16):
        for j in range(i + 2, 16, 2):
            d = mul_g(inv_g(d10["states"][i]), d10["states"][j])
            if d in d10["conj_colls"]:
                c10["collapse"] += 1
            elif d in d10["conj_short"]:
                c10[f"len{d10['conj_short'][d][0]}"] += 1
            elif d in comm_orbits10:
                c10["commutator_ab"] += 1
                special10.add("[a,b]=1 => abelian")
            elif d == b_sq_rel:
                c10["sigma_plus_1_b"] += 1
                special10.add("(1+sigma)b=0 => 2b=0 => C4 (0202)")
            else:
                raise AssertionError(f"Unexpected diff in General Case(1,0): {d}")

    sha12, shb12 = ((1, 0, 0, 0, 0, 0), 1), ((0, 0, 0, 1, 0, 0), 2)
    d12 = analyze_short_closure(W_G12, id_g, sha12, shb12, mul_g, inv_g, 32)
    comm_12 = mul_g(mul_g(inv_g(sha12), inv_g(shb12)), mul_g(sha12, shb12))
    assert comm_12 == ((1, 0, -1, -1, 1, 0), 0)
    comm_orbits12 = {(rot_g(sgn[0], k), 0) for sgn in (comm_12, inv_g(comm_12)) for k in range(3)}

    c12: Counter[str] = Counter()
    for i in range(32):
        for j in range(i + 2, 32, 2):
            d = mul_g(inv_g(d12["states"][i]), d12["states"][j])
            if d in d12["conj_colls"]:
                c12["collapse"] += 1
            elif d in d12["conj_short"]:
                c12[f"len{d12['conj_short'][d][0]}"] += 1
            elif d in comm_orbits12:
                c12["abelian_commutator_sigma_k_ab"] += 1
            else:
                raise AssertionError(f"Unexpected diff in General Case(1,2): {d}")

    general = {
        "General_Case_1_0": {
            "word16": W_G10,
            "pair_classification_counts": dict(c10),
            "algebraic_reductions": sorted(special10),
            "uncovered_pairs": 0,
        },
        "General_Case_1_2": {
            "word32": W_G12,
            "comm_ab": list(comm_12[0]),
            "pair_classification_counts": dict(c12),
            "uncovered_pairs": 0,
        },
    }

    # C. Physical non-nilpotent control families
    def shortest_pow2_at_root(elems: list, id_elem, a, b, mul_fn, lengths=(4, 8, 16, 32)) -> int | None:
        adj, _ = build_haar_adj_connected(elems, id_elem, a, b, mul_fn)
        for L in lengths:
            if has_simple_cycle_mitm(adj, [0], L):
                return L
        return None

    controls = {}
    for p in (2, 3, 5):
        def mul_fp3(x, y, modp=p):
            v1, t1 = x
            v2, t2 = y
            t = t1 % 3
            rv = v2 if t == 0 else ((v2[2], v2[0], v2[1]) if t == 1 else (v2[1], v2[2], v2[0]))
            return (((v1[0] + rv[0]) % modp, (v1[1] + rv[1]) % modp, (v1[2] + rv[2]) % modp), (t1 + t2) % 3)

        def inv_fp3(x, modp=p):
            v, t = x
            nt = (-t) % 3
            rv = v if nt == 0 else ((v[2], v[0], v[1]) if nt == 1 else (v[1], v[2], v[0]))
            return (((-rv[0]) % modp, (-rv[1]) % modp, (-rv[2]) % modp), nt)

        id_fp3 = ((0, 0, 0), 0)
        elems = [((x, y, z), t) for x in range(p) for y in range(p) for z in range(p) for t in range(3)]
        if p == 5:
            pairs = [("case10", ((1, 2, 0), 1), ((1, 0, 3), 0)), ("case12", ((1, 2, 0), 1), ((0, 1, 3), 2))]
        else:
            pairs = [
                ("case10", ((1, 0, 0), 1), ((1, 1, 0), 0) if p != 2 else ((1, 0, 0), 0)),
                ("case12", ((1, 0, 0), 1), ((0, 1, 0), 2)),
            ]
        lens = {}
        for tag, a, b in pairs:
            if p < 5:
                found = shortest_pow2_at_root(elems, id_fp3, a, b, mul_fp3, (4, 8, 16, 32))
                assert found is not None
                lens[tag] = found
            else:
                w_target = W_G10 if tag == "case10" else W_G12
                end_el, states = walk_word(w_target, id_fp3, a, b, mul_fp3, inv_fp3)
                half = len(w_target) // 2
                simple_w = end_el == id_fp3 and len(set(states[0::2])) == half and len(set(states[1::2])) == half
                if not simple_w:
                    found = shortest_pow2_at_root(elems, id_fp3, a, b, mul_fp3, (4, 8, 16))
                    assert found is not None
                    lens[tag] = found
                else:
                    lens[tag] = len(w_target)
        controls[f"F_{p}^3_rtimes_C3_order_{3*(p**3)}"] = lens

    def mul_105(x, y):
        return ((x[0] + y[0]) % 5, (x[1] + pow(2, x[2], 7) * y[1]) % 7, (x[2] + y[2]) % 3)

    elems_105 = [(c, u, t) for c in range(5) for u in range(7) for t in range(3)]
    c10_105 = shortest_pow2_at_root(elems_105, (0, 0, 0), (1, 1, 1), (2, 1, 0), mul_105, (4, 8, 16, 32))
    c12_105 = shortest_pow2_at_root(elems_105, (0, 0, 0), (1, 1, 1), (2, 2, 2), mul_105, (4, 8, 16, 32))
    assert c10_105 is not None and c12_105 is not None
    controls["C5_x_(C7_rtimes_C3)_order_105"] = {"case10_pow2": c10_105, "case12_pow2": c12_105}

    def mul_93(x, y):
        return ((x[0] + pow(5, x[1], 31) * y[0]) % 31, (x[1] + y[1]) % 3)

    elems_93 = [(u, t) for u in range(31) for t in range(3)]
    c93_hist: Counter[int] = Counter()
    for u1 in (0, 1, 3):
        for t1 in (1, 2):
            for u2 in (1, 2, 7, 11):
                for t2 in (0, 1, 2):
                    a, b = (u1, t1), (u2, t2)
                    if len({(0, 0), a, b}) < 3:
                        continue
                    L = shortest_pow2_at_root(elems_93, (0, 0), a, b, mul_93, (4, 8, 16))
                    assert L is not None
                    c93_hist[L] += 1
    controls["C31_rtimes_C3_order_93"] = {str(k): v for k, v in sorted(c93_hist.items())}

    def mul_sl23(X, Y):
        return (
            (X[0] * Y[0] + X[1] * Y[2]) % 3,
            (X[0] * Y[1] + X[1] * Y[3]) % 3,
            (X[2] * Y[0] + X[3] * Y[2]) % 3,
            (X[2] * Y[1] + X[3] * Y[3]) % 3,
        )

    elems_sl23 = [
        (a, b, c, d)
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a * d - b * c) % 3 == 1
    ]
    assert len(elems_sl23) == 24
    id_sl = (1, 0, 0, 1)
    sl_hist: Counter[int] = Counter()
    for i in range(1, 24):
        a = elems_sl23[i]
        inv_a = (a[3], (-a[1]) % 3, (-a[2]) % 3, a[0])
        for j in range(i + 1, 24):
            b = elems_sl23[j]
            inv_b = (b[3], (-b[1]) % 3, (-b[2]) % 3, b[0])
            seen = {id_sl, a, b}
            q = deque([id_sl, a, b])
            while q:
                x = q.popleft()
                for s in (a, b, inv_a, inv_b):
                    nx = mul_sl23(x, s)
                    if nx not in seen:
                        seen.add(nx)
                        q.append(nx)
            if len(seen) != 24:
                continue
            L = shortest_pow2_at_root(elems_sl23, id_sl, a, b, mul_sl23, (4, 8, 16, 32))
            assert L is not None
            sl_hist[L] += 1
    controls["SL_2_3_all_generating_pairs"] = {str(k): v for k, v in sorted(sl_hist.items())}

    return {
        "eisenstein_C4_C8_C16": eisenstein,
        "general_C4_to_C32": general,
        "physical_controls": controls,
    }


# ---------------------------------------------------------------------------
# 2. Two-Attachment Cubic Gadgets (n <= 18) & 4802-Vertex Stretch Witness
# ---------------------------------------------------------------------------

def verify_gadgets_n18_and_witness() -> dict:
    def is_connected(n: int, adj_mask: list[int]) -> bool:
        seen = 1
        q = deque([0])
        while q:
            u = q.popleft()
            m = adj_mask[u] & ~seen
            while m:
                lsb = m & -m
                seen |= lsb
                q.append(lsb.bit_length() - 1)
                m ^= lsb
        return seen == (1 << n) - 1

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

    def bfs_distance_0_1(adj: list[list[int]]) -> int:
        dist = [-1] * len(adj)
        dist[0] = 0
        q = deque([0])
        while q:
            u = q.popleft()
            if u == 1:
                return dist[1]
            for w in adj[u]:
                if dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return -1

    def path_spectrum_0_1(n: int, adj: list[list[int]]) -> list[int]:
        lengths = set()

        def dfs(u: int, depth: int, mask: int) -> None:
            if u == 1:
                lengths.add(depth)
                return
            for w in adj[u]:
                if mask & (1 << w):
                    continue
                dfs(w, depth + 1, mask | (1 << w))

        dfs(0, 0, 1)
        return sorted(lengths)

    def canonical_key(n: int, adj: list[list[int]]) -> tuple:
        def dists_from(src: int) -> list[int]:
            d = [99] * n
            d[src] = 0
            q = deque([src])
            while q:
                u = q.popleft()
                for w in adj[u]:
                    if d[w] == 99:
                        d[w] = d[u] + 1
                        q.append(w)
            return d

        d0 = dists_from(0)
        d1 = dists_from(1)

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
            for v in range(2, n):
                buckets[colors[v]].append(v)
            ordered_buckets = [buckets[r] for r in sorted(buckets)]
            best_edges = None
            perm = [0] * n
            perm[0], perm[1] = p0, p1

            def search_buckets(bidx: int, pos: int) -> None:
                nonlocal best_edges
                if bidx == len(ordered_buckets):
                    inv_map = [0] * n
                    for ni, ov in enumerate(perm):
                        inv_map[ov] = ni
                    edges = []
                    for nu in range(n):
                        ou = perm[nu]
                        for ov in adj[ou]:
                            nv = inv_map[ov]
                            if nu < nv:
                                edges.append((nu, nv))
                    edges.sort()
                    tup = tuple(edges)
                    if best_edges is None or tup < best_edges:
                        best_edges = tup
                    return
                grp = ordered_buckets[bidx]
                for choice in permutations(grp):
                    for off, ov in enumerate(choice):
                        perm[pos + off] = ov
                    search_buckets(bidx + 1, pos + len(grp))

            search_buckets(0, 2)
            return best_edges  # type: ignore

        return min(solve_for_01(False), solve_for_01(True))

    def enumerate_order(n: int) -> dict:
        seeds = [
            ("Ia_tri_012", [(0, 1), (0, 2), (1, 2)], 3),
            ("Ib_adj_01", [(0, 1), (0, 2), (1, 3)], 4),
            ("II_dist2", [(0, 2), (0, 3), (1, 2), (1, 4)], 5),
            ("III_dist_ge3", [(0, 2), (0, 3), (1, 4), (1, 5)], 6),
        ]
        c4_c8_free_raw = 0
        c4_c8_c16_free_raw = 0
        c4_c8_map: dict[tuple, dict] = {}
        c4_c8_c16_map: dict[tuple, dict] = {}

        for seed_name, init_edges, k_used in seeds:
            if k_used > n:
                continue
            adj_mask = [0] * n
            need = [0, 0] + [3] * (n - 2)
            for u, v in init_edges:
                adj_mask[u] |= 1 << v
                adj_mask[v] |= 1 << u
                if u >= 2:
                    need[u] -= 1
                if v >= 2:
                    need[v] -= 1

            def creates_c8_at_u(u: int) -> bool:
                nbrs = [v for v in range(n) if (adj_mask[u] >> v) & 1]
                if len(nbrs) < 2:
                    return False
                b_masks = []
                u_bit = 1 << u
                for a in nbrs:
                    reach3 = defaultdict(list)
                    m1 = adj_mask[a] & ~u_bit
                    while m1:
                        l1 = m1 & -m1
                        x1 = l1.bit_length() - 1
                        m1 ^= l1
                        m2 = adj_mask[x1] & ~(u_bit | (1 << a))
                        while m2:
                            l2 = m2 & -m2
                            x2 = l2.bit_length() - 1
                            m2 ^= l2
                            m3 = adj_mask[x2] & ~(u_bit | (1 << a) | l1)
                            while m3:
                                l3 = m3 & -m3
                                x3 = l3.bit_length() - 1
                                m3 ^= l3
                                reach3[x3].append((1 << a) | l1 | l2)
                    b_masks.append(reach3)
                for i in range(len(nbrs)):
                    for j in range(i + 1, len(nbrs)):
                        for mid, ms1 in b_masks[i].items():
                            ms2 = b_masks[j].get(mid)
                            if ms2:
                                for p1 in ms1:
                                    for p2 in ms2:
                                        if (p1 & p2) == 0:
                                            return True
                return False

            def bt(u: int, ff: int) -> None:
                nonlocal c4_c8_free_raw, c4_c8_c16_free_raw
                while u < n and need[u] == 0:
                    u += 1
                if u < n and u >= ff:
                    return
                if u == n:
                    if not is_connected(n, adj_mask):
                        return
                    adj = [[v for v in range(n) if (adj_mask[x] >> v) & 1] for x in range(n)]
                    if has_cycle_len_exact(n, adj, 8):
                        return
                    c4_c8_free_raw += 1
                    key = canonical_key(n, adj)
                    has16 = has_cycle_len_exact(n, adj, 16)
                    if key not in c4_c8_map:
                        spec = path_spectrum_0_1(n, adj)
                        min_s, max_s = spec[0], spec[-1]
                        closure_hit = bool(set(spec) & {1, 3, 7})
                        rec = {
                            "edges": [list(e) for e in key],
                            "dist_0_1": bfs_distance_0_1(adj),
                            "has_C16": has16,
                            "analytic_closure_hit_1_3_7": closure_hit,
                            "spectrum": spec,
                            "min_S": min_s,
                            "max_S": max_s,
                            "stretch_ratio": round(max_s / min_s, 6),
                            "bridged_ratio": round((max_s + 2) / (min_s + 2), 6),
                            "seed_origin": seed_name,
                        }
                        c4_c8_map[key] = rec
                        if not has16:
                            c4_c8_c16_free_raw += 1
                            c4_c8_c16_map[key] = rec
                    elif not has16:
                        c4_c8_c16_free_raw += 1
                    return

                kn = need[u]
                two_u = 0
                m = adj_mask[u]
                while m:
                    l = m & -m
                    two_u |= adj_mask[l.bit_length() - 1]
                    m ^= l
                two_u &= ~(1 << u)
                used_c = [
                    v for v in range(u + 1, ff)
                    if need[v] > 0 and not ((adj_mask[u] >> v) & 1) and (adj_mask[v] & two_u) == 0
                ]
                tmax = min(kn, n - ff)
                tmin = max(0, kn - len(used_c))
                for tf in range(tmax, tmin - 1, -1):
                    fc_list = list(range(ff, ff + tf))
                    nu = kn - tf
                    if nu == 0:
                        for v in fc_list:
                            adj_mask[u] |= 1 << v
                            adj_mask[v] |= 1 << u
                            need[u] -= 1
                            need[v] -= 1
                        if not creates_c8_at_u(u):
                            bt(u + 1, ff + tf)
                        for v in fc_list:
                            adj_mask[u] ^= 1 << v
                            adj_mask[v] ^= 1 << u
                            need[u] += 1
                            need[v] += 1
                    else:
                        for comb in combinations(used_c, nu):
                            ok = True
                            for i1 in range(nu):
                                a = comb[i1]
                                for i2 in range(i1 + 1, nu):
                                    if adj_mask[a] & adj_mask[comb[i2]]:
                                        ok = False
                                        break
                                if not ok:
                                    break
                            if not ok:
                                continue
                            ch = list(comb) + fc_list
                            for v in ch:
                                adj_mask[u] |= 1 << v
                                adj_mask[v] |= 1 << u
                                need[u] -= 1
                                need[v] -= 1
                            if not creates_c8_at_u(u):
                                bt(u + 1, ff + tf)
                            for v in ch:
                                adj_mask[u] ^= 1 << v
                                adj_mask[v] ^= 1 << u
                                need[u] += 1
                                need[v] += 1

            bt(2, k_used)

        c4c8_surv = sorted(c4_c8_map.values(), key=lambda r: (r["stretch_ratio"], r["min_S"], r["max_S"]))
        return {
            "n": n,
            "c4_c8_free_raw_leaves": c4_c8_free_raw,
            "c4_c8_free_canonical_classes": len(c4c8_surv),
            "c4_c8_c16_free_raw_leaves": c4_c8_c16_free_raw,
            "c4_c8_c16_free_canonical_classes": len(c4_c8_c16_map),
            "stretch_violations": sum(1 for r in c4c8_surv if r["max_S"] < 2 * r["min_S"]),
            "closure_violations": sum(1 for r in c4c8_surv if not r["analytic_closure_hit_1_3_7"]),
            "c4_c8_survivors_preview": c4c8_surv[:10],
        }

    by_order = [enumerate_order(n) for n in (4, 6, 8, 10, 12, 14, 16, 18)]
    assert all(o["c4_c8_free_canonical_classes"] == 0 and o["stretch_violations"] == 0 for o in by_order)

    # Genuine {C4, C8, C16}-free stretch witness: Haar(UT4(F7); {I, I+E12+E23, I+E23+E34}) - e
    def ut4_mul_7(X, Y):
        x01, x12, x23, x02, x13, x03 = X
        y01, y12, y23, y02, y13, y03 = Y
        return (
            (x01 + y01) % 7,
            (x12 + y12) % 7,
            (x23 + y23) % 7,
            (x02 + x01 * y12 + y02) % 7,
            (x13 + x12 * y23 + y13) % 7,
            (x03 + x01 * y13 + x02 * y23 + y03) % 7,
        )

    def ut4_inv_7(X):
        c = (0,) * 6
        for _ in range(7):
            nx = ut4_mul_7(c, X)
            if nx == (0,) * 6:
                return c
            c = nx
        raise RuntimeError("bad ut4 inverse")

    A7 = (1, 1, 0, 0, 0, 0)
    B7 = (0, 1, 1, 0, 0, 0)
    id7 = (0,) * 6
    sh = (id7, A7, B7)
    iv = (id7, ut4_inv_7(A7), ut4_inv_7(B7))

    dist_girth = {(0, id7): 0}
    par = {}
    q = deque([(0, id7)])
    girth = 999
    while q:
        side, g = q.popleft()
        d = dist_girth[(side, g)]
        if 2 * d >= girth:
            continue
        ns = 1 - side
        steps = sh if side == 0 else iv
        for s in steps:
            ng = ut4_mul_7(g, s)
            if (ns, ng) not in dist_girth:
                dist_girth[(ns, ng)] = d + 1
                par[(ns, ng)] = (side, g)
                q.append((ns, ng))
            elif par.get((side, g)) != (ns, ng):
                girth = min(girth, d + dist_girth[(ns, ng)] + 1)
    assert girth == 14

    for root in ((0, id7), (1, id7)):
        bkt = [defaultdict(set) for _ in range(3)]
        for br in range(3):
            def dfs8(side_u, g_u, dep, vis) -> None:
                if dep == 8:
                    bkt[br][(side_u, g_u)].add(vis)
                    return
                vis2 = vis | {(side_u, g_u)}
                ns = 1 - side_u
                steps = sh if side_u == 0 else iv
                for s in steps:
                    ng = ut4_mul_7(g_u, s)
                    nv = (ns, ng)
                    if nv != root and nv not in vis2:
                        dfs8(ns, ng, dep + 1, vis2)
            first_nv = (1 - root[0], ut4_mul_7(root[1], sh[br] if root[0] == 0 else iv[br]))
            dfs8(first_nv[0], first_nv[1], 1, frozenset())
        for b1 in range(3):
            for b2 in range(b1 + 1, 3):
                for tgt in set(bkt[b1]) & set(bkt[b2]):
                    for v1 in bkt[b1][tgt]:
                        for v2 in bkt[b2][tgt]:
                            assert v1 & v2, "Unexpected C16 in UT4(F7)!"

    dist_del = {(0, id7): 0}
    q = deque([(0, id7)])
    while q:
        side, g = q.popleft()
        d = dist_del[(side, g)]
        if (side, g) == (1, id7):
            break
        ns = 1 - side
        steps = sh if side == 0 else iv
        for s in steps:
            ng = ut4_mul_7(g, s)
            if {(side, g), (ns, ng)} == {(0, id7), (1, id7)}:
                continue
            if (ns, ng) not in dist_del:
                dist_del[(ns, ng)] = d + 1
                q.append((ns, ng))
    min_s = dist_del[(1, id7)]
    assert min_s == 13

    assert WORD32_CLASS3[0] == "0"
    path = [(0, id7)]
    cur = id7
    for idx_c, ch in enumerate(WORD32_CLASS3):
        cur = ut4_mul_7(cur, sh[int(ch)] if idx_c % 2 == 0 else iv[int(ch)])
        path.append(((idx_c + 1) % 2, cur))
    assert path[-1] == (0, id7) and len(set(path[:-1])) == 32
    path_31 = path[1:]
    assert path_31[0] == (1, id7) and path_31[-1] == (0, id7) and len(path_31) == 32 and len(set(path_31)) == 32

    return {
        "by_order": by_order,
        "genuine_c4_c8_c16_free_witness": {
            "graph": "Haar(UT4(F7); {I, I+E12+E23, I+E23+E34})",
            "total_vertices": 2 * (7 ** 4),
            "exact_girth": girth,
            "c16_free_verified": True,
            "deleted_edge": ["(0, id)", "(1, id)"],
            "exact_min_S": min_s,
            "explicit_simple_path_len_lower_bound_on_max_S": 31,
            "stretch_ratio_lower_bound": round(31 / min_s, 6),
            "bridged_ratio_lower_bound": round((31 + 2) / (min_s + 2), 6),
            "satisfies_garcia_ge_2": 31 >= 2 * min_s,
        },
    }


# ---------------------------------------------------------------------------
# 3. Exhaustive {C4, C8}-Free Cubic Haar C16 & Theta(8,8,8) Census (|G| <= 45)
# ---------------------------------------------------------------------------

def verify_low_order_haar_census() -> dict:
    v4: set[tuple[int, int]] = set()
    v8: set[tuple[int, int]] = set()
    shifts_z2 = ((0, 0), (1, 0), (0, 1))
    for L, target in ((4, v4), (8, v8)):
        def dfs_vec(dep: int, x: int, y: int, fc: int, lc: int) -> None:
            if dep == L:
                if lc != fc and (x, y) != (0, 0):
                    target.add((x, y))
                return
            sgn = 1 if dep % 2 == 0 else -1
            for c in (0, 1, 2):
                if c != lc:
                    dfs_vec(dep + 1, x + sgn * shifts_z2[c][0], y + sgn * shifts_z2[c][1], fc, c)
        for c0 in (0, 1, 2):
            dfs_vec(1, shifts_z2[c0][0], shifts_z2[c0][1], c0, c0)

    def abelian_enum(name: str, dims: tuple[int, ...]) -> dict:
        order = 1
        for d in dims:
            order *= d
        add_ab = lambda u, v: tuple((u[k] + v[k]) % dims[k] for k in range(len(dims)))
        sub_ab = lambda u, v: tuple((u[k] - v[k]) % dims[k] for k in range(len(dims)))
        neg_ab = lambda u: tuple((-u[k]) % dims[k] for k in range(len(dims)))
        elems = list(product(*(range(d) for d in dims)))
        zero = (0,) * len(dims)
        units = [u for u in range(1, order) if math.gcd(u, order) == 1]

        def canon_pair(a: tuple[int, ...], b: tuple[int, ...]) -> tuple:
            best = None
            for t in (zero, a, b):
                s_pair = tuple(sorted(sub_ab(x, t) for x in (zero, a, b) if x != t))
                if len(s_pair) != 2:
                    continue
                sa, sb = s_pair
                if len(dims) == 1:
                    for u in units:
                        cand = tuple(sorted(((u * sa[0]) % order, (u * sb[0]) % order)))
                        if best is None or cand < best:
                            best = cand
                else:
                    for sign in (1, -1):
                        cand = tuple(sorted((sa, sb)) if sign == 1 else sorted((neg_ab(sa), neg_ab(sb))))
                        if best is None or cand < best:
                            best = cand
            return best  # type: ignore

        seen_canon = set()
        witnesses = []
        for i in range(1, order):
            a = elems[i]
            for j in range(i + 1, order):
                b = elems[j]
                cp = canon_pair(a, b)
                if cp in seen_canon:
                    continue
                seen_canon.add(cp)
                if any(tuple((dx * a[k] + dy * b[k]) % dims[k] for k in range(len(dims))) == zero for dx, dy in v4):
                    continue
                if any(tuple((dx * a[k] + dy * b[k]) % dims[k] for k in range(len(dims))) == zero for dx, dy in v8):
                    continue
                seen_g = {zero, a, b}
                q = deque([zero, a, b])
                gens = (a, b, neg_ab(a), neg_ab(b))
                while q:
                    x = q.popleft()
                    for g in gens:
                        nx = add_ab(x, g)
                        if nx not in seen_g:
                            seen_g.add(nx)
                            q.append(nx)
                if len(seen_g) != order:
                    continue
                adj, conn = build_haar_adj_connected(elems, zero, a, b, add_ab)
                assert conn
                assert not has_simple_cycle_mitm(adj, [0], 4)
                assert not has_simple_cycle_mitm(adj, [0], 8)
                has16 = has_simple_cycle_mitm(adj, [0], 16)
                has16_or_32 = True if has16 else has_simple_cycle_mitm(adj, [0], 32)
                has_th8 = has_dyadic_theta_mitm(adj, [0], 8)
                has_th16 = False if has_th8 or 2 * order < 47 else has_dyadic_theta_mitm(adj, [0], 16)
                witnesses.append({
                    "a": list(a),
                    "b": list(b),
                    "has_C16": has16,
                    "has_C16_or_C32": has16_or_32,
                    "has_Theta_8_8_8": has_th8,
                    "has_Theta_16_16_16": has_th16,
                })
        return {
            "group": name,
            "order": order,
            "graph_vertices": 2 * order,
            "distinct_reanchored_pairs_checked": len(seen_canon),
            "c4_c8_free_connected_classes": len(witnesses),
            "c4_c8_c16_free_classes": sum(1 for r in witnesses if not r["has_C16"]),
            "missing_C16_or_C32": [r for r in witnesses if not r["has_C16_or_C32"]],
            "all_c4c8_free_have_Theta8": all(r["has_Theta_8_8_8"] for r in witnesses) if witnesses else None,
            "missing_Theta8": [r for r in witnesses if not r["has_Theta_8_8_8"]],
            "witnesses_preview": witnesses[:8],
        }

    def check_group_axioms(name: str, elems: list, id_elem, mul_fn, inv_fn) -> None:
        elem_set = set(elems)
        assert len(elem_set) == len(elems), f"{name}: duplicate elements"
        assert id_elem in elem_set, f"{name}: missing identity"
        for x in elems:
            assert mul_fn(x, id_elem) == x and mul_fn(id_elem, x) == x
            ix = inv_fn(x)
            assert ix in elem_set and mul_fn(x, ix) == id_elem and mul_fn(ix, x) == id_elem
        for x in elems:
            for y in elems:
                assert mul_fn(x, y) in elem_set
        sample_y = elems[::3] + elems[1:4]
        sample_z = elems[::4] + elems[1:4]
        for x in elems[::2] + elems[1:5]:
            for y in sample_y:
                xy = mul_fn(x, y)
                for z in sample_z:
                    assert mul_fn(xy, z) == mul_fn(x, mul_fn(y, z))

    def nonabelian_enum(name: str, elems: list, id_elem, mul_fn, inv_fn) -> dict:
        check_group_axioms(name, elems, id_elem, mul_fn, inv_fn)
        order = len(elems)
        seen_reanch = set()
        witnesses = []

        def canon_reanch(a, b):
            best = None
            for t in (id_elem, a, b):
                it = inv_fn(t)
                pair = tuple(sorted(mul_fn(it, x) for x in (id_elem, a, b) if x != t))
                if best is None or pair < best:
                    best = pair
            return best

        for i in range(1, order):
            a = elems[i]
            for j in range(i + 1, order):
                b = elems[j]
                cp = canon_reanch(a, b)
                if cp in seen_reanch:
                    continue
                seen_reanch.add(cp)
                ia, ib = inv_fn(a), inv_fn(b)
                if len({ia, ib, a, mul_fn(a, ib), b, mul_fn(b, ia)}) < 6:
                    continue
                seen_g = {id_elem, a, b, ia, ib}
                q = deque(seen_g)
                gens = (a, b, ia, ib)
                while q:
                    x = q.popleft()
                    for g in gens:
                        nx = mul_fn(x, g)
                        if nx not in seen_g:
                            seen_g.add(nx)
                            q.append(nx)
                if len(seen_g) != order:
                    continue
                adj, conn = build_haar_adj_connected(elems, id_elem, a, b, mul_fn)
                assert conn
                roots = [0, order]
                if has_simple_cycle_mitm(adj, roots, 8):
                    continue
                has16 = has_simple_cycle_mitm(adj, roots, 16)
                has16_or_32 = True if has16 else has_simple_cycle_mitm(adj, roots, 32)
                has_th8 = has_dyadic_theta_mitm(adj, roots, 8)
                has_th16 = False if has_th8 or 2 * order < 47 else has_dyadic_theta_mitm(adj, roots, 16)
                witnesses.append({
                    "a": list(a) if isinstance(a, tuple) else a,
                    "b": list(b) if isinstance(b, tuple) else b,
                    "has_C16": has16,
                    "has_C16_or_C32": has16_or_32,
                    "has_Theta_8_8_8": has_th8,
                    "has_Theta_16_16_16": has_th16,
                })
        return {
            "group": name,
            "order": order,
            "graph_vertices": 2 * order,
            "distinct_reanchored_pairs_checked": len(seen_reanch),
            "c4_c8_free_connected_classes": len(witnesses),
            "c4_c8_c16_free_classes": sum(1 for r in witnesses if not r["has_C16"]),
            "missing_C16_or_C32": [r for r in witnesses if not r["has_C16_or_C32"]],
            "all_c4c8_free_have_Theta8": all(r["has_Theta_8_8_8"] for r in witnesses) if witnesses else None,
            "missing_Theta8": [r for r in witnesses if not r["has_Theta_8_8_8"]],
            "witnesses_preview": witnesses[:8],
        }

    for m in range(3, 19):
        assert abelian_enum(f"C_{m}", (m,))["c4_c8_free_connected_classes"] == 0

    cyclic_records = [abelian_enum(f"C_{m}", (m,)) for m in range(19, 46)]
    noncyclic_dims = [
        ("C2xC10", (2, 10)), ("C2xC12", (2, 12)), ("C5xC5", (5, 5)), ("C3xC9", (3, 9)),
        ("C3xC3xC3", (3, 3, 3)), ("C2xC14", (2, 14)), ("C2xC16", (2, 16)), ("C4xC8", (4, 8)),
        ("C2xC18", (2, 18)), ("C3xC12", (3, 12)), ("C6xC6", (6, 6)), ("C2xC20", (2, 20)),
        ("C2xC22", (2, 22)), ("C3xC15", (3, 15)),
    ]
    noncyclic_records = [abelian_enum(nm, dm) for nm, dm in noncyclic_dims]
    assert next(x for x in noncyclic_records if x["group"] == "C3xC3xC3")["c4_c8_free_connected_classes"] == 0

    nonabelian_records = []

    def enum_semidirect(label: str, q: int, m: int, alpha: int) -> dict:
        el = [(u, t) for u in range(q) for t in range(m)]
        mul_f = lambda x, y, mq=q, mm=m, a=alpha: ((x[0] + pow(a, x[1], mq) * y[0]) % mq, (x[1] + y[1]) % mm)
        inv_f = lambda x, mq=q, mm=m, a=alpha: ((-pow(a, (mm - x[1]) % mm, mq) * x[0]) % mq, (mm - x[1]) % mm)
        return nonabelian_enum(label, el, (0, 0), mul_f, inv_f)

    nonabelian_records.append(enum_semidirect("Dic_20", 5, 4, 4))
    nonabelian_records.append(enum_semidirect("AGL(1,5)", 5, 4, 2))
    nonabelian_records.append(enum_semidirect("C7_rtimes_C3", 7, 3, 2))
    nonabelian_records.append(enum_semidirect("M27_exp9", 9, 3, 4))
    nonabelian_records.append(enum_semidirect("C13_rtimes_C3", 13, 3, 3))
    nonabelian_records.append(enum_semidirect("C3_rtimes_C8", 3, 8, 2))

    el_dic24 = [(k, e) for k in range(12) for e in (0, 1)]
    mul_dic24 = lambda x, y: (
        ((x[0] - y[0] + 6) % 12, 0) if (x[1] == 1 and y[1] == 1)
        else (((x[0] + y[0]) % 12, y[1]) if x[1] == 0 else ((x[0] - y[0]) % 12, 1))
    )
    inv_dic24 = lambda x: (((x[0] + 6) % 12, 1) if x[1] == 1 else ((-x[0]) % 12, 0))
    nonabelian_records.append(nonabelian_enum("Dic_24", el_dic24, (0, 0), mul_dic24, inv_dic24))

    elems_s4 = list(permutations(range(4)))
    mul_s4 = lambda p, q: tuple(p[q[i]] for i in range(4))
    inv_s4 = lambda p: tuple(p.index(i) for i in range(4))
    nonabelian_records.append(nonabelian_enum("S_4", elems_s4, (0, 1, 2, 3), mul_s4, inv_s4))

    even_a4 = [p for p in elems_s4 if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
    el_a4c2 = [(p, e) for p in even_a4 for e in (0, 1)]
    nonabelian_records.append(nonabelian_enum(
        "A4_x_C2", el_a4c2, ((0, 1, 2, 3), 0),
        lambda x, y: (mul_s4(x[0], y[0]), x[1] ^ y[1]),
        lambda x: (inv_s4(x[0]), x[1]),
    ))

    el_sl23 = [
        (a, b, c, d) for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a * d - b * c) % 3 == 1
    ]
    nonabelian_records.append(nonabelian_enum(
        "SL(2,3)", el_sl23, (1, 0, 0, 1),
        lambda x, y: ((x[0] * y[0] + x[1] * y[2]) % 3, (x[0] * y[1] + x[1] * y[3]) % 3,
                      (x[2] * y[0] + x[3] * y[2]) % 3, (x[2] * y[1] + x[3] * y[3]) % 3),
        lambda x: (x[3] % 3, (-x[1]) % 3, (-x[2]) % 3, x[0] % 3),
    ))

    el_ut3 = [(i, j, k) for i in range(3) for j in range(3) for k in range(3)]
    nonabelian_records.append(nonabelian_enum(
        "UT3(F3)_exp3", el_ut3, (0, 0, 0),
        lambda x, y: ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3, (x[2] + y[2] + x[0] * y[1]) % 3),
        lambda x: ((-x[0]) % 3, (-x[1]) % 3, (-x[2] + x[0] * x[1]) % 3),
    ))

    nonabelian_records.append(enum_semidirect("Dic_28", 7, 4, 6))
    nonabelian_records.append(enum_semidirect("C5_x_S3", 15, 2, 11))
    nonabelian_records.append(enum_semidirect("C3_x_D5", 15, 2, 4))
    for n_dih in range(10, 23):
        nonabelian_records.append(enum_semidirect(f"D_{n_dih}", n_dih, 2, n_dih - 1))
    nonabelian_records.append(enum_semidirect("C7_x_S3", 21, 2, 8))
    nonabelian_records.append(enum_semidirect("C3_x_D7", 21, 2, 13))
    el_21x2 = [(u, t, e) for u in range(7) for t in range(3) for e in (0, 1)]
    nonabelian_records.append(nonabelian_enum(
        "(C7_rtimes_C3)_x_C2", el_21x2, (0, 0, 0),
        lambda x, y: ((x[0] + pow(2, x[1], 7) * y[0]) % 7, (x[1] + y[1]) % 3, x[2] ^ y[2]),
        lambda x: ((-pow(2, (3 - x[1]) % 3, 7) * x[0]) % 7, (3 - x[1]) % 3, x[2]),
    ))
    nonabelian_records.append(enum_semidirect("C7_rtimes_C6", 7, 6, 3))
    nonabelian_records.append(enum_semidirect("Dic_44", 11, 4, 10))

    all_recs = cyclic_records + noncyclic_records + nonabelian_records
    total_c4c8 = sum(r["c4_c8_free_connected_classes"] for r in all_recs)
    total_c4c8c16 = sum(r["c4_c8_c16_free_classes"] for r in all_recs)
    missing_theta8_groups = [
        {"group": r["group"], "order": r["order"], "count": len(r["missing_Theta8"]), "examples": r["missing_Theta8"][:2]}
        for r in all_recs if r["missing_Theta8"]
    ]
    missing_c16_or_c32 = [
        {"group": r["group"], "order": r["order"], "witness": w}
        for r in all_recs for w in r["missing_C16_or_C32"]
    ]
    assert not missing_c16_or_c32 and not missing_theta8_groups

    return {
        "m_le_18_cyclic_c4c8_free_verified_zero": True,
        "groups_checked_total": 16 + len(all_recs),
        "total_c4_c8_free_classes": total_c4c8,
        "total_c4_c8_c16_free_classes": total_c4c8c16,
        "all_c4_c8_free_have_C16_or_C32": True,
        "missing_Theta8_groups": missing_theta8_groups,
        "cyclic_19_to_45": cyclic_records,
        "noncyclic_abelian": noncyclic_records,
        "nonabelian": nonabelian_records,
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    cert_payload = {
        "paper": "Paper III: Power-of-Two Cycles in Semidirect C_3-Extension Cubic Haar Graphs and Two-Attachment Cubic Gadget Bounds",
        "status": "PASS",
        "semidirect_c3": verify_semidirect_c3(),
        "gadgets_n18_and_witness": verify_gadgets_n18_and_witness(),
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
        for k in ("semidirect_c3", "gadgets_n18_and_witness", "low_order_haar_census"):
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
        "gadgets_n18_c4c8_classes": [o["c4_c8_free_canonical_classes"] for o in out["gadgets_n18_and_witness"]["by_order"]],
        "ut4_f7_stretch_ge_2": out["gadgets_n18_and_witness"]["genuine_c4_c8_c16_free_witness"]["satisfies_garcia_ge_2"],
        "haar_census_groups_checked": out["low_order_haar_census"]["groups_checked_total"],
        "haar_census_c4c8_classes": out["low_order_haar_census"]["total_c4_c8_free_classes"],
        "haar_census_c16_free": out["low_order_haar_census"]["total_c4_c8_c16_free_classes"],
        "haar_census_missing_theta8": len(out["low_order_haar_census"]["missing_Theta8_groups"]),
    }, indent=2))
