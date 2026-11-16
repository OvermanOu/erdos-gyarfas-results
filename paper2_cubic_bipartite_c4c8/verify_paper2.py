#!/usr/bin/env python3
"""Standalone standard-library verifier for Paper II:
The Sharp 38-Vertex Bound for {C4, C8}-Free Cubic Bipartite Graphs
and Dyadic Theta Cover Obstructions.

Run from repository root or paper2_cubic_bipartite_c4c8/:
    python verify_paper2.py
    python verify_paper2.py --write-certificates
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations
import json
import math
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "certificates" / "paper2_certificates.json"


# ---------------------------------------------------------------------------
# Helpers: cycle counting & graph6 decoder
# ---------------------------------------------------------------------------

def count_cycles(adj: list[set[int]], length: int) -> int:
    """Count unoriented simple cycles of fixed length once (min vertex, min neighbor)."""
    total = 0
    for start in range(len(adj)):
        path = [start]
        used = {start}

        def dfs(v: int) -> None:
            nonlocal total
            if len(path) == length:
                if start in adj[v] and path[1] < path[-1]:
                    total += 1
                return
            for w in adj[v]:
                if w <= start or w in used:
                    continue
                used.add(w)
                path.append(w)
                dfs(w)
                path.pop()
                used.remove(w)

        dfs(start)
    return total


def decode_graph6_edges(g6: str) -> tuple[int, set[tuple[int, int]]]:
    """Decode small (n <= 62) graph6 string without header."""
    bs = [ord(ch) - 63 for ch in g6.strip()]
    n = bs[0]
    bits = []
    for val in bs[1:]:
        for shift in range(5, -1, -1):
            bits.append((val >> shift) & 1)
    edges = set()
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                edges.add((i, j))
            idx += 1
    return n, edges


def encode_graph6(n: int, edges: set[tuple[int, int]]) -> str:
    """Encode small (n <= 62) simple graph as graph6 without header."""
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (i, j) in edges else 0)
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(n + 63)]
    for k in range(0, len(bits), 6):
        val = 0
        for b in bits[k:k + 6]:
            val = (val << 1) | b
        chars.append(chr(val + 63))
    return "".join(chars)


# ---------------------------------------------------------------------------
# 1. Point-graph C8 gap identity on explicit incidence systems
# ---------------------------------------------------------------------------

EXPLICIT_INCIDENCE_CONTROLS = {
    "Fano_plane": (7, [[0, 1, 2], [0, 3, 4], [0, 5, 6], [1, 3, 5], [1, 4, 6], [2, 3, 6], [2, 4, 5]]),
    "Mobius_Kantor_8_3": (8, [[i, (i + 1) % 8, (i + 3) % 8] for i in range(8)]),
    "Desargues_10_3": (10, [[0, 3, 7], [2, 4, 8], [1, 4, 5], [4, 6, 7], [1, 7, 8], [0, 2, 6], [0, 8, 9], [2, 5, 9], [1, 3, 9], [3, 5, 6]]),
    "B19_0_1_8": (19, [[(y - s) % 19 for s in (0, 1, 8)] for y in range(19)]),
}


def check_gap_identity(name: str, n: int, blocks: list[list[int]]) -> dict:
    assert len(blocks) == n
    assert [sum(v in b for b in blocks) for v in range(n)] == [3] * n
    owner = {}
    for idx, b in enumerate(blocks):
        assert len(b) == 3 and len(set(b)) == 3
        for u, v in combinations(sorted(b), 2):
            assert (u, v) not in owner
            owner[(u, v)] = idx
    q = [set() for _ in range(n)]
    inc = [set() for _ in range(2 * n)]
    for u, v in owner:
        q[u].add(v)
        q[v].add(u)
    for idx, b in enumerate(blocks):
        for v in b:
            inc[v].add(n + idx)
            inc[n + idx].add(v)
    assert [len(row) for row in q] == [6] * n

    pairs = list(combinations(range(n), 2))
    lam = {p: len(q[p[0]] & q[p[1]]) for p in pairs}
    edges = set(owner)
    nonedges = set(lam) - edges
    t_dfs = count_cycles(q, 4)
    t_lam = sum(k * (k - 1) // 2 for k in lam.values()) // 2
    w_sum = sum(lam[p] - 1 for p in edges)
    c8_dfs = count_cycles(inc, 8)
    eg = sum((lam[p] - 3) * (lam[p] - 4) // 2 for p in edges)
    ng = sum((lam[p] - 1) * (lam[p] - 2) // 2 for p in nonedges)
    assert t_dfs == t_lam
    assert c8_dfs == t_dfs - w_sum
    assert 2 * c8_dfs == eg + ng - n * (n - 13) // 2
    if n <= 12:
        assert c8_dfs >= (n * (13 - n) + 3) // 4
    return {
        "name": name,
        "n_per_shore": n,
        "T": t_dfs,
        "W": w_sum,
        "C8": c8_dfs,
        "edge_gap_sum": eg,
        "nonedge_gap_sum": ng,
    }


def verify_gap_identity_controls() -> list[dict]:
    out = [check_gap_identity(name, n, blks) for name, (n, blks) in EXPLICIT_INCIDENCE_CONTROLS.items()]
    fano_n, fano_b = EXPLICIT_INCIDENCE_CONTROLS["Fano_plane"]
    union_b = [b[:] for b in fano_b] + [[v + fano_n for v in b] for b in fano_b]
    out.append(check_gap_identity("disjoint_two_Fano", 2 * fano_n, union_b))
    return out


# ---------------------------------------------------------------------------
# 2. Local capacity lemma (n<=14) & 8-vertex locally-K1,3 4-regular control
# ---------------------------------------------------------------------------

def verify_local_capacity_and_linegraph() -> dict:
    matching = {(0, 1), (2, 3), (4, 5)}
    others = [(a, b) for a, b in combinations(range(6), 2) if (a, b) not in matching]
    counts = Counter()
    examined = 0
    for mask in range(1 << 12):
        nbrs = [0] * 6
        for i, (a, b) in enumerate(others):
            if (mask >> i) & 1:
                nbrs[a] |= 1 << b
                nbrs[b] |= 1 << a
        degs = [x.bit_count() for x in nbrs]
        if max(degs) > 2:
            continue
        examined += 1
        d_val = 3 * degs.count(0) + degs.count(1)
        c_val = 0
        for bits in nbrs:
            if bits.bit_count() == 2:
                a, b = (i for i in range(6) if (bits >> i) & 1)
                c_val += (a, b) in matching
        assert 3 * c_val <= 6 + d_val and c_val != 3
        if c_val == 4:
            assert d_val == 6 and degs.count(0) == 2 and degs.count(2) == 4
        counts[c_val] += 1
    assert examined == 772 and dict(sorted(counts.items())) == {0: 343, 1: 252, 2: 174, 4: 3}

    # All 19,355 labeled simple 4-regular graphs on 8 vertices (via cubic complements)
    n8 = 8
    all_mask = (1 << n8) - 1
    deg = [0] * n8
    adj = [0] * n8
    total_4reg = 0
    all_k13 = 0

    def has_k13(g: tuple[int, ...], v: int) -> bool:
        ns = [u for u in range(n8) if (g[v] >> u) & 1]
        for center in ns:
            leaves = [u for u in ns if u != center]
            if all((g[center] >> u) & 1 for u in leaves) and all(not ((g[a] >> b) & 1) for a, b in combinations(leaves, 2)):
                return True
        return False

    def gen_cubic() -> None:
        nonlocal total_4reg, all_k13
        v = next((i for i, d in enumerate(deg) if d < 3), -1)
        if v == -1:
            total_4reg += 1
            g = tuple(all_mask ^ (1 << u) ^ adj[u] for u in range(n8))
            if all(has_k13(g, u) for u in range(n8)):
                all_k13 += 1
            return
        need = 3 - deg[v]
        cands = [u for u in range(v + 1, n8) if deg[u] < 3]
        for us in combinations(cands, need):
            for u in us:
                deg[v] += 1
                deg[u] += 1
                adj[v] |= 1 << u
                adj[u] |= 1 << v
            gen_cubic()
            for u in us:
                deg[v] -= 1
                deg[u] -= 1
                adj[v] ^= 1 << u
                adj[u] ^= 1 << v

    gen_cubic()
    assert total_4reg == 19355 and all_k13 == 0
    return {
        "local_capacity_graphs_checked": 4096,
        "local_capacity_max_deg2": examined,
        "local_capacity_c_distribution": dict(sorted(counts.items())),
        "labeled_4regular_order8": total_4reg,
        "locally_K13_order8_count": all_k13,
    }


# ---------------------------------------------------------------------------
# 3. Order 16, 17, 18 profile enumeration & analytic exclusions
# ---------------------------------------------------------------------------

def verify_profiles_16_17_18() -> dict:
    def valid_profiles(n: int):
        s_target = n * (n - 13) // 2
        res = []
        for e1 in range(0, 3 * n + 1, 3):
            for e2 in range(0, 3 * n - e1 + 1, 3):
                e3 = 3 * n - e1 - e2
                r = s_target - 3 * e1 - e2
                if e2 >= e3 and r >= 0 and e1 + e2 - e3 >= 6:
                    res.append((e1, e2, e3, r))
        return res

    p16 = valid_profiles(16)
    p17 = valid_profiles(17)
    p18 = valid_profiles(18)
    assert p16 == []  # E1+E2-E3>=6 already eliminates n=16!
    assert p17 == [(0, 30, 21, 4), (0, 33, 18, 1)]
    assert p18 == [
        (0, 30, 24, 15), (0, 33, 21, 12), (0, 36, 18, 9),
        (0, 39, 15, 6), (0, 42, 12, 3), (0, 45, 9, 0),
        (3, 27, 24, 9), (3, 30, 21, 6), (3, 33, 18, 3), (3, 36, 15, 0),
        (6, 24, 24, 3), (6, 27, 21, 0),
    ]
    p18_pos_e1 = [p for p in p18 if p[0] > 0]
    assert len(p18_pos_e1) == 6

    # Check (k0, k1, k2) membership equations for the 6 E1>0 n=18 profiles
    memberships = {}
    for e1, e2, e3, r in p18_pos_e1:
        ef = e1 + e2 - e3
        m_list = []
        for k0 in range(19):
            for k1 in range(2, min(2 * e1, 18 - k0) + 1):
                k2 = 18 - k0 - k1
                if k1 + 2 * k2 == 4 * (e3 // 3) and 6 * k0 + 3 * k1 == 2 * ef:
                    if k0 == 0 or (k0 + k1 >= 7):
                        m_list.append((k0, k1, k2))
        memberships[f"({e1},{e2},{e3})"] = m_list
    assert memberships == {
        "(3,27,24)": [(0, 4, 14)],
        "(3,30,21)": [(1, 6, 11)],
        "(3,33,18)": [(3, 6, 9), (4, 4, 10), (5, 2, 11)],
        "(3,36,15)": [(5, 6, 7), (6, 4, 8), (7, 2, 9)],
        "(6,24,24)": [(0, 4, 14)],
        "(6,27,21)": [(0, 8, 10), (1, 6, 11)],
    }

    # Check disjoint 6-point perfect matchings always form C6 (profile (3,30,21))
    def gen_pm(verts):
        if not verts:
            yield frozenset()
            return
        v0 = verts[0]
        for w in verts[1:]:
            rem = tuple(x for x in verts[1:] if x != w)
            for tail in gen_pm(rem):
                yield tail | {frozenset((v0, w))}

    pms = list(gen_pm(tuple(range(6))))
    assert len(pms) == 15
    for m1, m2 in combinations(pms, 2):
        if m1.isdisjoint(m2):
            edges = m1 | m2
            vis = {0}
            stk = [0]
            while stk:
                u = stk.pop()
                for e in edges:
                    if u in e:
                        w = next(iter(e - {u}))
                        if w not in vis:
                            vis.add(w)
                            stk.append(w)
            assert len(vis) == 6

    # Check (3,33,18) pair bound and (3,36,15) convex wedge bound
    for a, b in ((3, 6), (4, 4), (5, 2)):
        i_lb = (6 * a - 6 + b) // 2
        p_lb = (i_lb - 5) if a == 3 else (2 * i_lb - 15)
        assert p_lb > math.comb(a, 2)
    for a, b, min_e, min_w, max_w in ((5, 6, 9, 24, 21), (6, 4, 13, 44, 34), (7, 2, 17, 66, 54)):
        assert 4 * a - 11 == min_e
        assert 2 * min_e + (math.comb(a, 2) - min_e) * (a - 2) == max_w
        assert min_w > max_w

    return {
        "n16_profiles_with_residual_bound": p16,
        "n17_necessary_profiles": p17,
        "n18_pos_e1_memberships": memberships,
    }


# ---------------------------------------------------------------------------
# 4. Complete dual/Q enumeration for n=18, (6,27,21), (0,8,10)
# ---------------------------------------------------------------------------

F2_EDGES = {(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)}
F1_REPS = {
    "A": {(0, 6), (1, 6), (3, 6), (2, 7), (4, 7), (5, 7)},
    "B": {(0, 6), (1, 6), (3, 7), (4, 7), (6, 7), (2, 5)},
    "C": {(0, 6), (3, 6), (1, 7), (4, 7), (6, 7), (2, 5)},
}
EXPECTED_D_GRAPH6 = ["FlUk?", "FxckG", "FsdoW", "FMowo", "FhdQW", "FhUk_"]


def verify_n18_6_27_21_dual_q_census() -> dict:
    # A. Exhaustive check of 4-vertex 2K2/dense equivalence (all 64 graphs)
    pairs4 = list(combinations(range(4), 2))
    for mask in range(64):
        sel = [pairs4[i] for i in range(6) if (mask >> i) & 1]
        bad_pat = len(sel) >= 5 or (len(sel) == 2 and len(set(sel[0] + sel[1])) == 4)
        bad_lam = False
        for e1, e2 in combinations(sel, 2):
            if len(set(e1 + e2)) == 4:
                cross = sum(
                    1 for a, b in sel
                    if (a in e1 and b in e2) or (a in e2 and b in e1)
                )
                if cross not in (1, 2):
                    bad_lam = True
        assert bad_pat == bad_lam

    # B. Enumerate all C(21,10)=352,716 labeled 10-edge graphs on 7 vertices
    d_pairs = list(combinations(range(7), 2))
    d_idx = {e: i for i, e in enumerate(d_pairs)}
    quad_info = []
    for q in combinations(range(7), 4):
        qset = set(q)
        e_indices = [i for i, (u, v) in enumerate(d_pairs) if u in qset and v in qset]
        # Disjoint edge pairs inside the 6 pairs of quad
        e_tuples = [(d_pairs[i], 1 << i) for i in e_indices]
        disjoint_pairs = []
        for idx1 in range(6):
            for idx2 in range(idx1 + 1, 6):
                p1, b1 = e_tuples[idx1]
                p2, b2 = e_tuples[idx2]
                if len(set(p1 + p2)) == 4:
                    disjoint_pairs.append(b1 | b2)
        quad_mask = sum(1 << i for i in e_indices)
        quad_info.append((quad_mask, disjoint_pairs))

    def valid_dual_mask(mask: int) -> bool:
        for qmask, d_masks in quad_info:
            sub = mask & qmask
            cnt = sub.bit_count()
            if cnt >= 5:
                return False
            if cnt == 2 and sub in d_masks:
                return False
        return True

    valid_masks = set()
    for chosen in combinations(range(21), 10):
        deg = [0] * 7
        mask = 0
        for idx in chosen:
            u, v = d_pairs[idx]
            deg[u] += 1
            deg[v] += 1
            mask |= 1 << idx
        if max(deg) <= 4 and valid_dual_mask(mask):
            valid_masks.add(mask)
    assert len(valid_masks) == 9240

    # Partition valid_masks into S_7 isomorphism orbits (pure stdlib)
    perms7 = list(permutations(range(7)))
    perm_edge_bits = []
    for p in perms7:
        tbl = []
        for u, v in d_pairs:
            nu, nv = p[u], p[v]
            tbl.append(1 << d_idx[(nu, nv) if nu < nv else (nv, nu)])
        perm_edge_bits.append(tbl)

    def apply_perm(mask: int, tbl: list[int]) -> int:
        out = 0
        m = mask
        while m:
            lsb = m & -m
            idx = lsb.bit_length() - 1
            out |= tbl[idx]
            m ^= lsb
        return out

    # Also match the exact 6 reference graph6 representatives
    ref_reps = {}
    for g6 in EXPECTED_D_GRAPH6:
        n_v, ed = decode_graph6_edges(g6)
        assert n_v == 7 and len(ed) == 10
        m = sum(1 << d_idx[e] for e in ed)
        assert m in valid_masks
        ref_reps[g6] = m

    remaining = set(valid_masks)
    dual_orbits = []
    matched_g6 = []
    for g6, ref_mask in sorted(ref_reps.items()):
        assert ref_mask in remaining
        orbit = set()
        for tbl in perm_edge_bits:
            orbit.add(apply_perm(ref_mask, tbl))
        assert orbit <= remaining
        remaining -= orbit
        aut = 5040 // len(orbit)
        edges = [d_pairs[i] for i in range(21) if (ref_mask >> i) & 1]
        degs = [sum(v in e for e in edges) for v in range(7)]
        caps = [4 - d for d in degs]
        b_assign = math.factorial(8) // math.prod(math.factorial(c) for c in caps)
        dual_orbits.append({
            "graph6": g6,
            "automorphisms": aut,
            "orbit_size": len(orbit),
            "degree_sequence": degs,
            "capacities": caps,
            "boundary_assignments": b_assign,
            "edges": edges,
        })
        matched_g6.append(g6)
    assert not remaining and len(dual_orbits) == 6
    assert sum(r["orbit_size"] for r in dual_orbits) == 9240
    assert sum(r["boundary_assignments"] for r in dual_orbits) == 52080

    # C. Enumerate all F1 shapes on 8 boundary points
    all_pairs8 = list(combinations(range(8), 2))
    triangles = {frozenset((0, 1, 2)), frozenset((3, 4, 5))}
    f2_autos = []
    for p6 in permutations(range(6)):
        if {frozenset(p6[i] for i in t) for t in triangles} != triangles:
            continue
        f2_autos.append(tuple(p6) + (6, 7))
        f2_autos.append(tuple(p6) + (7, 6))
    assert len(f2_autos) == 144

    def canon_f1(es: set[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
        return min(
            tuple(sorted((p[u], p[v]) if p[u] < p[v] else (p[v], p[u]) for u, v in es))
            for p in f2_autos
        )

    deg_seq_cnt = 0
    disjoint_cnt = 0
    local_cnt = 0
    f1_orbits = Counter()
    target_deg = [1] * 6 + [3, 3]
    for chosen in combinations(all_pairs8, 6):
        deg = [0] * 8
        for u, v in chosen:
            deg[u] += 1
            deg[v] += 1
        if deg != target_deg:
            continue
        deg_seq_cnt += 1
        f1 = set(chosen)
        if f1 & F2_EDGES:
            continue
        disjoint_cnt += 1
        nbr = [0] * 8
        for u, v in f1 | F2_EDGES:
            nbr[u] |= 1 << v
            nbr[v] |= 1 << u
        if any((nbr[u] & nbr[v]).bit_count() > 1 for u, v in f1):
            continue
        local_cnt += 1
        f1_orbits[canon_f1(f1)] += 1

    assert (deg_seq_cnt, disjoint_cnt, local_cnt) == (110, 74, 72)
    assert sorted(f1_orbits.values()) == [18, 18, 36]
    rep_canon = {name: canon_f1(es) for name, es in F1_REPS.items()}
    assert set(rep_canon.values()) == set(f1_orbits)

    # D. Exhaust all 52,080 * 3 = 156,240 (D, F1, boundary assignment) trials
    def gen_owners(caps: list[int]):
        owner = [-1] * 8

        def rec(v: int, rem: tuple[int, ...]):
            if v == 7:
                yield tuple(owner)
                return
            for chosen in combinations(rem, caps[v]):
                cset = set(chosen)
                for b in chosen:
                    owner[b] = v
                yield from rec(v + 1, tuple(x for x in rem if x not in cset))
                for b in chosen:
                    owner[b] = -1

        yield from rec(0, tuple(range(8)))

    f2_mask = [0] * 18
    for u, v in F2_EDGES:
        f2_mask[u] |= 1 << v
        f2_mask[v] |= 1 << u

    blocks_summary = []
    total_trials = 0
    total_positives = 0

    for d_row in dual_orbits:
        d_edges = d_row["edges"]
        caps = d_row["capacities"]
        owners = list(gen_owners(caps))
        assert len(owners) == d_row["boundary_assignments"]
        # Precompute shared points per dual vertex v
        edge_pt = {e: 8 + idx for idx, e in enumerate(d_edges)}
        shared_pts = [[edge_pt[e] for e in d_edges if v in e] for v in range(7)]

        for f_name in ("A", "B", "C"):
            f1_edges = F1_REPS[f_name]
            f12_edges = f1_edges | F2_EDGES
            base_adj = [f2_mask[i] for i in range(18)]
            for u, v in f1_edges:
                base_adj[u] |= 1 << v
                base_adj[v] |= 1 << u

            rejects = Counter()
            positives = 0
            for owner in owners:
                total_trials += 1
                blocks = [shared_pts[v] + [b for b, w in enumerate(owner) if w == v] for v in range(7)]
                # Check category overlap & build star_edges
                adj = base_adj[:]
                overlap = False
                star_edges = set()
                for blk in blocks:
                    for a, b in combinations(blk, 2):
                        e = (a, b) if a < b else (b, a)
                        if e in f12_edges:
                            overlap = True
                            break
                        star_edges.add(e)
                        adj[a] |= 1 << b
                        adj[b] |= 1 << a
                    if overlap:
                        break
                if overlap:
                    rejects["category_overlap"] += 1
                    continue
                if any(m.bit_count() != 6 for m in adj):
                    rejects["Q_degree"] += 1
                    continue
                q_edges = star_edges | f12_edges
                reason = None
                for u, v in f1_edges:
                    if (adj[u] & adj[v]).bit_count() != 1:
                        reason = "F1_lambda"
                        break
                if reason is None:
                    for u, v in F2_EDGES:
                        if (adj[u] & adj[v]).bit_count() != 2:
                            reason = "F2_lambda"
                            break
                if reason is None:
                    for u in range(18):
                        au = adj[u]
                        for v in range(u + 1, 18):
                            if not ((au >> v) & 1):
                                if (au & adj[v]).bit_count() not in (1, 2):
                                    reason = "nonedge_lambda"
                                    break
                        if reason is not None:
                            break
                if reason is None:
                    for blk in blocks:
                        l3 = [(a, b) for a, b in combinations(blk, 2) if (adj[a] & adj[b]).bit_count() == 3]
                        l2 = [(a, b) for a, b in combinations(blk, 2) if (adj[a] & adj[b]).bit_count() == 2]
                        if len(l3) != 3 or len(l2) != 3:
                            reason = "star_codegree_pattern"
                            break
                        cdeg = Counter(x for e in l3 for x in e)
                        if sorted(cdeg.values()) != [1, 1, 1, 3]:
                            reason = "star_spoke_shape"
                            break
                if reason is None:
                    positives += 1
                    total_positives += 1
                else:
                    rejects[reason] += 1

            blocks_summary.append({
                "dual_graph6": d_row["graph6"],
                "F1_type": f_name,
                "assignments_tested": len(owners),
                "positive_candidates": positives,
                "rejected": dict(sorted(rejects.items())),
            })

    assert total_trials == 156240 and total_positives == 0
    return {
        "labeled_duals_checked": math.comb(21, 10),
        "valid_labeled_duals": 9240,
        "dual_orbits": [{k: v for k, v in d.items() if k != "edges"} for d in dual_orbits],
        "f1_staged_counts": [deg_seq_cnt, disjoint_cnt, local_cnt],
        "f1_orbit_sizes": sorted(f1_orbits.values()),
        "total_blocks": len(blocks_summary),
        "total_assignments_tested": total_trials,
        "total_positive_candidates": total_positives,
        "blocks": blocks_summary,
    }


# ---------------------------------------------------------------------------
# 5. Sharpness upper bound witness: B(19; {0, 1, 8}) on 38 vertices
# ---------------------------------------------------------------------------

def verify_b19_witness() -> dict:
    n = 19
    shifts = (0, 1, 8)
    adj = [set() for _ in range(2 * n)]
    for x in range(n):
        for s in shifts:
            y = n + (x + s) % n
            adj[x].add(y)
            adj[y].add(x)
    assert all(len(row) == 3 for row in adj)

    # Check connectedness
    seen = {0}
    stk = [0]
    while stk:
        u = stk.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stk.append(w)
    assert len(seen) == 2 * n

    counts = {L: count_cycles(adj, L) for L in (4, 6, 8, 10)}
    assert counts == {4: 0, 6: 19, 8: 0, 10: 171}

    c16_witness = [0, 19, 11, 30, 3, 22, 2, 21, 1, 28, 8, 35, 15, 34, 7, 27]
    assert len(c16_witness) == 16 and len(set(c16_witness)) == 16
    assert all(c16_witness[(i + 1) % 16] in adj[c16_witness[i]] for i in range(16))

    # Verify point-graph profile (E1, E2, E3) = (0, 57, 0)
    triples = [frozenset((y - s) % n for s in shifts) for y in range(n)]
    q = [set() for _ in range(n)]
    for tr in triples:
        for u, v in combinations(tr, 2):
            q[u].add(v)
            q[v].add(u)
    e_dist = Counter(len(q[u] & q[v]) for u in range(n) for v in q[u] if u < v)
    assert dict(e_dist) == {2: 57}

    return {
        "graph": "B(19; {0,1,8})",
        "vertices": 38,
        "connected": True,
        "simple_cubic_bipartite": True,
        "short_cycle_counts": counts,
        "point_graph_profile": {"E1": 0, "E2": 57, "E3": 0},
        "simple_C16_witness": c16_witness,
    }


def run(write_certs: bool = False) -> dict:
    t0 = time.monotonic()
    res = {
        "paper": "Paper II: The Sharp 38-Vertex Bound for {C4, C8}-Free Cubic Bipartite Graphs and Dyadic Theta Cover Obstructions",
        "status": "PASS",
        "gap_identity_controls": verify_gap_identity_controls(),
        "local_capacity_and_linegraph": verify_local_capacity_and_linegraph(),
        "profiles_16_17_18": verify_profiles_16_17_18(),
        "n18_6_27_21_census": verify_n18_6_27_21_dual_q_census(),
        "b19_witness": verify_b19_witness(),
        "elapsed_seconds": round(time.monotonic() - t0, 3),
    }
    if write_certs:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    elif CERT_PATH.exists():
        saved = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        current = json.loads(json.dumps(res))
        for k in ("gap_identity_controls", "local_capacity_and_linegraph", "profiles_16_17_18", "n18_6_27_21_census", "b19_witness"):
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
        "local_max_deg2": out["local_capacity_and_linegraph"]["local_capacity_max_deg2"],
        "order8_4reg_all_K13": out["local_capacity_and_linegraph"]["locally_K13_order8_count"],
        "n18_duals": out["n18_6_27_21_census"]["valid_labeled_duals"],
        "n18_assignments_tested": out["n18_6_27_21_census"]["total_assignments_tested"],
        "n18_positive": out["n18_6_27_21_census"]["total_positive_candidates"],
        "b19_cycles": out["b19_witness"]["short_cycle_counts"],
    }, indent=2))
