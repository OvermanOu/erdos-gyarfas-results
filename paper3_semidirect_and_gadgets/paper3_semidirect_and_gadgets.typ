#set page(paper: "us-letter", margin: (x: 0.95in, y: 0.95in), numbering: "1")
#set text(font: "New Computer Modern", size: 10.5pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")

#let theorem(title: none, body) = block(
  width: 100%,
  inset: (top: 4pt, bottom: 4pt),
  [
    *Theorem#if title != none [ (#title)].* #emph(body)
  ]
)
#let lemma(title: none, body) = block(
  width: 100%,
  inset: (top: 4pt, bottom: 4pt),
  [
    *Lemma#if title != none [ (#title)].* #emph(body)
  ]
)
#let proposition(title: none, body) = block(
  width: 100%,
  inset: (top: 4pt, bottom: 4pt),
  [
    *Proposition#if title != none [ (#title)].* #emph(body)
  ]
)
#let definition(title: none, body) = block(
  width: 100%,
  inset: (top: 4pt, bottom: 4pt),
  [
    *Definition#if title != none [ (#title)].* #body
  ]
)
#let proof(title: "Proof", body) = block(
  width: 100%,
  inset: (top: 2pt, bottom: 6pt),
  [
    #emph[#title.] #body #h(1fr) $square$
  ]
)

#align(center)[
  #text(size: 15pt, weight: "bold")[Power-of-Two Cycles in Semidirect $C_3$-Extension Cubic Haar Graphs and Two-Attachment Cubic Gadget Bounds]
  #v(0.5em)
  #text(size: 11pt)[OvermanOu (`ad110158@gmail.com`)] \
  #text(size: 9.5pt, fill: luma(80))[November 17, 2026]
]

#v(0.8em)
#block(inset: (x: 1.5em))[
  #text(size: 9.5pt)[
    *Abstract.* We advance two complementary structural directions toward the Erdős–Gyárfás conjecture on power-of-two cycles in graphs of minimum degree at least three: non-nilpotent solvable cubic Haar graphs and two-attachment $\{C_4, C_8\}$-free cubic gadgets. First, let $A$ be any abelian group (finite or infinite) and $sigma in "Aut"(A)$ any automorphism of order dividing $3$. Using exact word evaluations and conjugation closures in the universal semidirect extensions $ZZ[omega]^2 times.r C_3$ and $ZZ[C_3]^2 times.r C_3$, we prove that every connected component of every simple cubic three-shift Haar graph $cal(H)(A times.r_sigma C_3; S)$ contains a simple cycle of length $4, 8, 16$, or $32$, improving sharply to $C_4, C_8$, or $C_(16)$ whenever $1 + sigma + sigma^2 = 0$ on $A$ (covering all abelian-kernel Frobenius groups $A times.r C_3$, alternating group $A_4$, and fixed-point-free $C_3$-actions) or $|S mod A| <= 2$. Normal $2$-kernel lifting extends the theorem to any finite group $G$ admitting $N lt.eq.tri G$ with $G slash N tilde.equiv A times.r_sigma C_3$ (such as $"SL"(2,3)$) and to regular $G$-covers of connected bases containing $Theta(2^k, 2^k, 2^k)$.

    Second, for connected simple $\{C_4, C_8\}$-free two-attachment cubic gadgets $H$ ($deg(0)=deg(1)=2$, internal vertices degree $3$) and $0$–$1$ path-length spectrum $S(H)$, we prove an exact closure equivalence showing $S(H) inter \{1,3,7\} = emptyset$ iff $H + \{0,1\}$ is simple $\{C_4, C_8\}$-free cubic; modulo-$3$ handshaking plus our $38$-vertex cubic bipartite theorem forces $S(H) inter \{1,3,7\} != emptyset$ for all bipartite gadgets with $n <= 36$ (sharp at $n = 38$). In general, soundness-verified exhaustive enumeration establishes zero $\{C_4, C_8\}$-free gadgets for $4 <= n <= 18$ and **exact** $n_min(\{C_4, C_8\}"-free") = 20$ with **three** canonical isomorphism classes (`324` symmetry-reduced leaves, all non-bipartite of girth $3$, all containing $C_(16)$ and intersecting $\{3,7\}$), forcing $n_min(\{C_4, C_8, C_(16)\}"-free") >= 22$ (bridge bound $>= 44$) and sharp closure-admissible order $n_min^"cl" = 24$ via `MARKSTROM24 - {0,1}` ($min S = 4$, $max S = 23$). We also verify a 4,802-vertex girth-$14$ $\{C_4, C_8, C_(16)\}$-free gadget $cal(H)(U T_4(FF_7); \{I, I+E_(12)+E_(23), I+E_(23)+E_(34)\}) - e$ ($min S = 13$, explicit $C_(32)-e$ simple path of length $31 >= 26$), and report a complete zero-gap cubic Haar census across $3 <= |G| <= 47$ (`151` two-generated groups accounting for all `196` OEIS A000001 groups across $45$ orders, `20,114` re-anchoring pairs, and `3,518` connected $\{C_4, C_8\}$-free classes = `2,752` abelian + `766` nonabelian) in which every witness contains both $C_(16)$ and $Theta(8,8,8)$.
  ]
]
#v(0.6em)

= Introduction

In Paper I, we unconditionally resolved the Erdős–Gyárfás conjecture for simple cubic three-shift Haar graphs $cal(H)(Gamma; S)$ whenever $Gamma slash N$ is nilpotent of class at most six for a normal $2$-subgroup $N lt.eq.tri Gamma$. The smallest non-nilpotent solvable cubic Haar graphs arise from cyclic-by-abelian semidirect extensions $Gamma = A times.r_sigma C_3$, where Burkhart's odd-order Cayley induction (`arXiv:2611.05060`) fails both because no odd-order cubic Cayley graph exists and because cubic graphs admit no single-vertex figure-eight. Independently, Paper II established that every nonempty simple $\{C_4, C_8\}$-free cubic bipartite graph has at least $38$ vertices, while Markström (`2004`), Garcia (`arXiv:2609.04686`), and Carr (`arXiv:2605.22844`) isolated small $\{C_4, C_8\}$-free bounds and two-attachment cubic gadget reductions with path-spectrum stretch inequalities $max S(H) >= 2 min S(H)$ as central bottlenecks for general cubic graphs.

This paper settles the entire semidirect family $A times.r_sigma C_3$ unconditionally and establishes rigorous finite and analytic bounds for $\{C_4, C_8\}$-free two-attachment gadgets and low-order Haar covers.

== Main results

#definition(title: [Semidirect $C_3$-extension cubic Haar graph])[
  Let $A$ be an additive abelian group and $sigma in "Aut"(A)$ satisfy $sigma^3 = "id"_A$. The semidirect product $Gamma = A times.r_sigma C_3$ has underlying set $A times \{0,1,2\}$ and multiplication
  $ (u, t_1)(v, t_2) = (u + sigma^(t_1)(v), t_1 + t_2 mod 3). $
  For distinct $S = \{s_0, s_1, s_2\} subset.eq Gamma$, the simple $3$-regular bipartite Haar graph $cal(H)(Gamma; S)$ joins $(g, 0)$ to $(g s_c, 1)$ for $g in Gamma$ and $c in \{0,1,2\}$.
]

#theorem(title: [1.1 — Universal semidirect $A times.r_sigma C_3$ cubic Haar theorem])[
  Let $A$ be any abelian group (finite or infinite), let $sigma in "Aut"(A)$ satisfy $sigma^3 = "id"_A$, and set $Gamma = A times.r_sigma C_3$. Then every connected component of every simple cubic three-shift Haar graph $cal(H)(Gamma; S)$ contains a simple cycle of length $4, 8, 16$, or $32$.

  More generally, let $G$ be any finite group admitting a normal $2$-subgroup $N lt.eq.tri G$ such that $G slash N tilde.equiv A times.r_sigma C_3$ (for example $G = "SL"(2,3)$ with $N tilde.equiv C_2$ and $G slash N tilde.equiv A_4$), and let $B$ be a connected finite graph containing an equal-length dyadic theta subgraph $Theta(2^k, 2^k, 2^k)$ ($k >= 1$). Then: \
  (a) every connected component of every simple cubic Haar graph $cal(H)(G; S)$ contains a simple cycle of length $2^m$ for some $m >= 2$; and \
  (b) every connected component of every regular $G$-cover of $B$ contains a simple cycle of length $2^m$ for some $m >= k + 2$.
]

#theorem(title: [1.2 — Sharp $C_(16)$ bound for Eisenstein / Frobenius $C_3$-extensions])[
  Let $A$ be any abelian group and $sigma in "Aut"(A)$ satisfy $1 + sigma + sigma^2 = 0$ on $A$ (in particular, every Frobenius group $A times.r C_3$ with abelian Frobenius kernel $A$, every finite fixed-point-free $FF_p$-action of $C_3$, $A_4 = V_4 times.r C_3$, and every $p=3$ extension with $(sigma - "id")^2 = 0$), OR suppose that $|S mod A| <= 2$. Then every connected component of every simple cubic Haar graph $cal(H)(A times.r_sigma C_3; S)$ contains a simple cycle of length $4, 8$, or $16$.
]

Next, call $H = (V, E)$ a _connected simple two-attachment cubic gadget_ on $n$ vertices ($n >= 4$ even) if $H$ is connected and simple, $deg_H (0) = deg_H (1) = 2$, and $deg_H (v) = 3$ for all $v in \{2, dots.c, n-1\}$. Let $S(H) subset.eq ZZ_(>= 1)$ denote the set of lengths of all simple $0$–$1$ paths in $H$.

#theorem(title: [1.3 — Exact $n_min = 20$ classification, closure threshold $n_min^"cl" = 24$, and stretch witness])[
  Let $H$ be a connected simple $\{C_4, C_8\}$-free two-attachment cubic gadget on $n$ vertices. \
  (a) *Exact closure equivalence, bipartite $n <= 36$, and sharp $n_min^"cl" = 24$:* The cubic closure $H^+ = H + \{0,1\}$ is simple and $\{C_4, C_8\}$-free iff $S(H) inter \{1,3,7\} = emptyset$. If $H$ is bipartite, handshaking modulo $3$ places $0$ and $1$ in opposite shores, forcing $S(H) inter \{1,3,7\} != emptyset$ for all bipartite gadgets with $n <= 36$ (sharp at $n = 38$ via $B(19; \{0,1,8\}) - e$). In general, combining part (b) ($n <= 20$ non-admissibility), Markström's $f(3) = 24$ lower bound for $\{C_4, C_8\}$-free cubic graphs (`2004`; Garcia `arXiv:2609.04686`) which excludes $n = 22$ closures, and deleting $\{0,1\}$ from the connected $24$-vertex $\{C_4, C_8\}$-free cubic witness `MARKSTROM24` (spectrum $S(H) = \{4, 5, 6, 8, 9, dots.c, 23\}$; $H^+$ contains $C_(16)$) yields the sharp closure-admissible minimum order $n_min^"cl" = 24$. \
  (b) *Exact minimum order $n_min = 20$ ($3$ classes) & bridge corollaries:* Zero connected simple $\{C_4, C_8\}$-free two-attachment cubic gadgets exist for any $n in \{4, 6, dots.c, 18\}$, and at $n = 20$ there are **exactly three** canonical isomorphism classes (`324` symmetry-reduced leaves, all in neighborhood seed `III_dist_ge3`, non-bipartite of girth $3$, Hamiltonian $max S = 19$, stretch $19 slash 3, 19 slash 5, 19 slash 6 >= 2$). Every $20$-vertex survivor contains $C_(16)$ and hits $\{3,7\} subset.eq \{1,3,7\}$. Consequently, $n_min(\{C_4, C_8\}"-free") = 20$ (forcing $n >= 40$ across any non-incident $0$–$1$ separating bridge) and **$n_min(\{C_4, C_8, C_(16)\}"-free") >= 22$** (forcing $n >= 44$ across any non-incident $0$–$1$ separating bridge). \
  (c) *Genuine $\{C_4, C_8, C_(16)\}$-free stretch witness (4,802 vertices):* Deleting the edge $e = \{(0,I), (1,I)\}$ from $cal(H)(U T_4(FF_7); \{I, I+E_(12)+E_(23), I+E_(23)+E_(34)\})$ produces a bipartite $\{C_4, C_8, C_(16)\}$-free two-attachment gadget of girth $14$ with $min S = 13$ and an explicit simple $0$–$1$ path of length $31 >= 2 dot 13 = 26$ (stretch ratio $>= 31 slash 13 approx 2.384615$, bridged ratio $>= 33 slash 15 = 2.2$).
]

#proposition(title: [1.4 — Complete zero-gap $\{C_4, C_8\}$-free cubic Haar census, $3 <= |G| <= 47$])[
  Across all $45$ group orders $3 <= |G| <= 47$ (covering all $196$ OEIS A000001 isomorphism classes via all $151$ two-generated finite groups, checking `20,114` re-anchoring pairs; $6 <= |V| <= 94$), there are `0` $\{C_4, C_8\}$-free classes for $|G| <= 18$ and **exactly `3,518`** connected $\{C_4, C_8\}$-free cubic Haar re-anchoring classes overall (`2,752` abelian and `766` nonabelian across $13$ nonabelian groups). Every single class (`3,518 / 3,518`) contains both a simple $C_(16)$ and an equal-length dyadic theta subgraph $Theta(8,8,8)$.
]

= Proof of Theorems 1.1 and 1.2

As in Paper I, normalize the component shifts to $\{1, a, b\}$ inside $K = chevron.l a, b chevron.r <= Gamma = A times.r_sigma C_3$, representing walks starting at $(1,0)$ by even-length cyclic words $w in \{0,1,2\}^(2m)$ with prefix coordinates $P_0 = 1$, $P_(i+1) = P_i s_(c_i)^((-1)^i)$ ($s_0=1, s_1=a, s_2=b$). Let $overline(S) = \{0, overline(a), overline(b)\} subset.eq Gamma slash A tilde.equiv C_3$ denote the $C_3$-coset profile.

#lemma(title: [2.1 — $C_3$-coset reduction])[
  After possibly replacing $sigma$ by $sigma^(-1)$, re-anchoring $\{1,a,b\}$ to $\{1, a^(-1), a^(-1) b\}$ if $overline(a) = overline(b) != 0$, and swapping $a <-> b$, every component $cal(H)(K; \{1,a,b\})$ falls into one of three normalized forms: \
  (1) *Case `(0, 0)`*: $a, b in A$, so $K <= A$ is abelian and Paper I Theorem 2.1 gives $C_4, C_8$, or $C_(16)$. \
  (2) *Case `(1, 0)`*: $a = (u, 1)$ and $b = (v, 0)$ ($|overline(S)| = 2$). \
  (3) *Case `(1, 2)`*: $a = (u, 1)$ and $b = (v, 2)$ ($|overline(S)| = 3$).
]

== Universal Eisenstein obstruction (Theorem 1.2)

Suppose $(1 + sigma + sigma^2)(A) = 0$. Then $A$ carries a canonical $ZZ[omega]$-module structure ($omega$ acting as $sigma$, $omega^2 = -1 - omega$), yielding a canonical homomorphism $pi : ZZ[omega]^2 times.r C_3 -> Gamma$ sending $((1,0,0,0), 1) |-> a$ and $((0,0,1,0), t_b) |-> b$ ($t_b in \{0,2\}$ in Cases `(1,0)` and `(1,2)`). Evaluate the two cyclically nonbacktracking $16$-color words
$ w_(E,10) = #raw("0101020120102102") quad ("Case "(1,0)), wide w_(E,12) = #raw("1021212021210202") quad ("Case "(1,2)). $
Direct evaluation verifies that both close identically to $((0,0,0,0), 0)$ in $ZZ[omega]^2 times.r C_3$, visiting $8$ distinct vertices per shore. Across all $56$ same-shore prefix differences $d = P_i^(-1) P_j$, every single difference satisfies one of two conditions directly without requiring conjugation: either $d$ is one of the six shift-collapse words $\{a^(plus.minus 1), b^(plus.minus 1), (a^(-1) b)^(plus.minus 1)\}$ (`20` pairs for $w_(E,10)$, `18` pairs for $w_(E,12)$, excluded since $1,a,b$ are distinct), or $d^(plus.minus 1)$ equals the endpoint of an explicit cyclically nonbacktracking closed walk of length $4$ or $8$ (`14` len-$4$ and `22` len-$8$ for $w_(E,10)$; `21` len-$4$ and `17` len-$8$ for $w_(E,12)$; `0` uncovered pairs in both). Any collision yields a simple $C_4$ or $C_8$, while collision-free lifting yields $C_(16)$. Combining with the Case `(1,0)` $16$-word below settles the $|overline(S)| <= 2$ clause of Theorem 1.2.

== General $sigma^3 = "id"_A$ obstruction (Theorem 1.1)

Without assuming $1 + sigma + sigma^2 = 0$, any pair $a = (u, 1), b = (v, t_b) in A times.r_sigma C_3$ receives a canonical homomorphism $pi : ZZ[C_3]^2 times.r C_3 -> Gamma$ mapping standard basis generators $e_1 = ((1,0,0,0,0,0), 1) |-> a$ and $e_2 = ((0,0,0,1,0,0), t_b) |-> b$. Consider
$ w_(G,10) = #raw("0102021021202012") quad ("len " 16), wide w_(G,12) = #raw("01202021020201021210201020210212") quad ("len " 32). $

In Case `(1, 0)` ($t_b = 0$), $w_(G,10)$ closes identically in $ZZ[C_3]^2 times.r C_3$ with $8$ distinct vertices per shore. Partitioning all $56$ same-shore differences modulo length-$<= 2$ conjugation yields: `27` conjugates of shift collapses (impossible); `15` conjugates of $4$-walks and `8` conjugates of $8$-walks (forcing $C_4$ or $C_8$); `3` conjugates of $sigma^k ([a,b]^(plus.minus 1))$ (vanishing iff $[a,b] = 1$, making $K$ abelian and giving $C_4, C_8$, or $C_(16)$ by Paper I Theorem 2.1); and `3` occurrences of $d = (1 + sigma)(b) = ((0,0,0,1,1,0), 0)$, whose vanishing in $A$ implies $2v = (1 - sigma + sigma^2)(1 + sigma)(v) = 0$, closing the $4$-cycle `0202` (`0` uncovered pairs).

In Case `(1, 2)` ($t_b = 2$), $w_(G,12)$ closes identically in $ZZ[C_3]^2 times.r C_3$ with $16$ distinct vertices per shore and commutator $[e_1, e_2] = ((1,0,-1,-1,1,0), 0)$. Across all $240$ same-shore prefix differences, conjugation closure yields: `78` shift collapses, `77` conjugates of $4$-walks, `78` conjugates of $8$-walks, and `7` elements equal to $sigma^k ([e_1, e_2]^(plus.minus 1))$ (`0` uncovered pairs). Since $sigma$ is an automorphism, $sigma^k ([a,b]) = 0$ iff $[a,b] = 1$ ($K$ abelian). Normal $2$-kernel lifting (Paper I Lemma 2.3) and dyadic equal-path theta reduction (Paper I Lemma 2.4) yield parts (a) and (b). Explicitly, $w_(G,12)$ traces a simple $C_(32)$ in $FF_5^3 times.r C_3$ (order $375$), and finite controls verify all generating pairs in $FF_2^3 times.r C_3$ (`4, 8`), $FF_3^3 times.r C_3$ (`16, 16`), $C_5 times (C_7 times.r C_3)$ (`16, 16`), $C_(31) times.r C_3$ (`70` pairs all `16`), and all `176` generating Haar graphs of $"SL"(2,3)$ (`8`). #h(1fr) $square$

= Proof of Theorem 1.3 and Census Results (Proposition 1.4)

#proof(title: "Proof of Theorem 1.3")[
  For (a), adding $\{0,1\}$ makes $H^+ = H + \{0,1\}$ $3$-regular, and $H^+$ is simple iff $\{0,1\} in.not E(H)$ ($1 in.not S(H)$). Assuming $H$ is simple $\{C_4, C_8\}$-free with $1 in.not S(H)$, every $C_4$ or $C_8$ in $H^+$ traverses $\{0,1\}$, leaving a simple $0$–$1$ path in $H$ of length $3$ or $7$. If $H = (A union.sq B, E)$ is bipartite, then $sum_(u in A) deg_H (u) = |E| = sum_(v in B) deg_H (v) mod 3$ forbids $0$ and $1$ from lying in the same shore ($-2 != 0 mod 3$). Hence $H^+$ remains bipartite; by Paper II Theorem 1.3, $S(H) inter \{1,3,7\} != emptyset$ holds for all bipartite $\{C_4, C_8\}$-free gadgets with $n <= 36$, sharp at $n = 38$ via $B(19; \{0,1,8\}) - e$. In general, part (b) rules out closure-admissible gadgets for $n <= 20$, while any closure-admissible gadget at $n = 22$ would produce a simple $\{C_4, C_8\}$-free cubic graph $H^+$ on $22$ vertices, contradicting Markström's theorem ($f(3) = 24$, `2004`; Garcia `arXiv:2609.04686`). At $n = 24$, deleting $\{0,1\}$ from the connected $\{C_4, C_8\}$-free cubic graph `MARKSTROM24` (whose closure contains $C_(16)$) leaves a connected gadget with path spectrum $S(H) = \{4, 5, 6, 8, 9, dots.c, 23\}$ ($min S = 4$, $max S = 23$, $S(H) inter \{1,3,7\} = emptyset$), proving sharpness of $n_min^"cl" = 24$.

  For (b), because $H$ is simple and $C_4$-free with $deg_H (0)=deg_H (1)=2$, $\{0,1\}$ has at most one common neighbor, yielding exactly four neighborhood seeds: `Ia_tri_012` ($\{0,1\},\{0,2\},\{1,2\}$), `Ib_adj_01` ($\{0,1\},\{0,2\},\{1,3\}$), `II_dist2` ($\{0,2\},\{0,3\},\{1,2\},\{1,4\}$), and `III_dist_ge3` ($\{0,2\},\{0,3\},\{1,4\},\{1,5\}$). To certify soundness of our capacity-pruned, $D_4$-symmetry-broken, $C_8$-pruned search, we first compare unpruned $C_4$-free enumeration against capacity-pruned + symmetry-reduced enumeration at $n in \{6, 8, 10, 12\}$: canonical $C_4$-free class counts match identically (`0`, `1`, `11`, `75`) with identical canonical class sets and `0` $C_8$-parity discrepancies at $n in \{8, 10\}$. Full search over $n in \{4,6,8,10,12,14,16,18\}$ gives `0` canonical classes everywhere, whereas $n = 20$ produces `324` symmetry-reduced leaves collapsing to **exactly three** canonical isomorphism classes (Table 1). Since all three contain $C_(16)$, **$n_min(\{C_4, C_8\}"-free") = 20$** and **$n_min(\{C_4, C_8, C_(16)\}"-free") >= 22$**. Deleting any bridge $e = u_0 u_1$ separating $0$ and $1$ with $u_0, u_1 in.not \{0,1\}$ splits $H - e$ into two connected gadgets on $(0, u_0)$ and $(1, u_1)$, forcing $n >= 2 n_min = 40$ (and $n >= 44$ when $C_(16)$-free).

  For (c), BFS on $G = cal(H)(U T_4(FF_7); \{I, I+E_(12)+E_(23), I+E_(23)+E_(34)\})$ (4,802 vertices) establishes exact girth $14$, bidirectional depth-$8$ DFS excluding endpoints from intermediate sets proves $C_(16)$-freeness on both shores, and deleting $e = \{(0,I), (1,I)\}$ (step $0$ of $w_(32) = #raw("01010102012012101012012010212012")$) leaves exact distance $min S = 13$ alongside a simple $31$-edge residual path ($31 >= 2 dot 13$, bridged ratio $33 slash 15 = 2.2$).
]

#figure(
  table(
    columns: 6,
    stroke: 0.5pt + luma(160),
    inset: 5pt,
    fill: (x, y) => if y == 0 { luma(240) },
    align: (center, center, center, center, center, left),
    table.header([Class], [Seed / Girth / Bip.], [$min S$], [$max S$], [Stretch], [$S inter \{1,3,7\}$, $C_(16)$, and Spectrum $S(H)$]),
    [1], [`III_dist_ge3` / $3$ / No], [$3$], [$19$], [$19 slash 3 approx 6.333333$], [$\{3, 7\}$, $C_(16)$ yes; $S = \{3, 6, 7, dots.c, 19\}$],
    [2], [`III_dist_ge3` / $3$ / No], [$5$], [$19$], [$19 slash 5 = 3.8$], [$\{7\}$, $C_(16)$ yes; $S = \{5, 6, dots.c, 19\}$],
    [3], [`III_dist_ge3` / $3$ / No], [$6$], [$19$], [$19 slash 6 approx 3.166667$], [$\{7\}$, $C_(16)$ yes; $S = \{6, 7, dots.c, 19\}$],
  ),
  caption: [Exact canonical classification of connected simple $\{C_4, C_8\}$-free two-attachment cubic gadgets at $n_min = 20$ (`324` symmetry-reduced leaves, `0` $\{C_4, C_8, C_(16)\}$-free).],
)

Proposition 1.4 is exhaustively certified by `verify_paper3.py` (`verify_low_order_haar_census`). Using first-principles Schreier index-$2$ extensions (`8 -> 16 -> 32`, `12 -> 24`), exact Sylow classifications at orders `36` and `40`, and direct finite constructions for all remaining orders $3 <= |G| <= 47$, the verifier covers all `151` unique two-generated finite groups accounting for all `196` OEIS A000001 groups across all $45$ orders (`13 / 15` at order `24`, `20 / 51` at order `32`, `12 / 14` at order `36`, `12 / 14` at order `40`). Across `20,114` re-anchoring shift classes, `0` $\{C_4, C_8\}$-free classes exist below $|G| = 19$, and `3,518` $\{C_4, C_8\}$-free classes occur overall: `2,752` abelian plus `766` nonabelian (`21:C7:C3`: 14, `24:O24_nab2`: 12, `27:UT3(F3)_exp3`: 72, `30:C3xD5`: 20, `32:O32_nab10`: 32, `36:A4xC3`: 96, `36:Dic12xC3`: 12, `36:S3xC6`: 12, `39:C13:C3`: 208, `40:C5:C8_2`: 40, `40:C5:C8_4`: 80, `42:C3xD7`: 42, `42:(C7:C3)xC2`: 126). Every single class (`3,518 / 3,518`) admits both a simple $C_(16)$ and an equal-length dyadic theta subgraph $Theta(8,8,8)$.

*Reproducibility and AI Disclosure.* Every theorem, soundness cross-check, $n <= 20$ classification, `MARKSTROM24 - {0,1}` witness, and $3 <= |G| <= 47$ Haar census is deterministically reproduced by the standalone Python~3 standard-library verifier `paper3_semidirect_and_gadgets/verify_paper3.py` against `certificates/paper3_certificates.json`. Portions of the discovery scripts and manuscript preparation were assisted by AI systems; all theorems, proofs, and executable assertions were audited by the author and rest directly on the deterministic verifiers.

*References.* Burkhart (`arXiv:2611.05060`, 2026); Carr (`arXiv:2605.22844`, 2026); Garcia (`arXiv:2609.04686`, 2026); Markström (*Congr. Numer.* 171 (2004), 179–192); OvermanOu, companion Paper I, Paper II, & Paper IV (2026).
