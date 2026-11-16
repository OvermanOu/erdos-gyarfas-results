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

    Second, for connected simple $\{C_4, C_8\}$-free two-attachment cubic gadgets $H$ ($deg(0)=deg(1)=2$, internal vertices degree $3$) and $0$–$1$ path-length spectrum $S(H)$, we prove an exact closure equivalence showing $S(H) inter \{1,3,7\} = emptyset$ iff $H + \{0,1\}$ is simple $\{C_4, C_8\}$-free cubic; modulo-$3$ handshaking plus our $38$-vertex cubic bipartite theorem forces $S(H) inter \{1,3,7\} != emptyset$ for all bipartite gadgets with $n <= 36$ (sharp at $n = 38$), while exhaustive $C_8$-pruned enumeration shows no general $\{C_4, C_8\}$-free two-attachment cubic gadget exists at all for $n <= 18$ (forcing $n >= 40$ across any non-incident $0$–$1$ separating bridge). We also verify a 4,802-vertex girth-$14$ $\{C_4, C_8, C_(16)\}$-free gadget $cal(H)(U T_4(FF_7); \{I, I+E_(12)+E_(23), I+E_(23)+E_(34)\}) - e$ satisfying Garcia's stretch inequality ($min S = 13$, explicit $C_(32)-e$ simple path of length $31 >= 26$), and report an exhaustive $|G| <= 45$ cubic Haar census (`89` groups, `822` connected $\{C_4, C_8\}$-free classes) in which every witness contains both $C_(16)$ and $Theta(8,8,8)$.
  ]
]
#v(0.6em)

= Introduction

In Paper I, we unconditionally resolved the Erdős–Gyárfás conjecture for simple cubic three-shift Haar graphs $cal(H)(Gamma; S)$ whenever $Gamma slash N$ is nilpotent of class at most four for a normal $2$-subgroup $N lt.eq.tri Gamma$. The smallest non-nilpotent solvable cubic Haar graphs arise from cyclic-by-abelian semidirect extensions $Gamma = A times.r_sigma C_3$, where Burkhart's odd-order Cayley induction (`arXiv:2611.05060`) fails both because no odd-order cubic Cayley graph exists and because cubic graphs admit no single-vertex figure-eight. Independently, Paper II established that every nonempty simple $\{C_4, C_8\}$-free cubic bipartite graph has at least $38$ vertices, while Garcia (`arXiv:2609.04686`) and Carr (`arXiv:2605.22844`) isolated two-attachment cubic gadget reductions with path-spectrum stretch inequalities $max S(H) >= 2 min S(H)$ as a central bottleneck for general cubic graphs.

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

#theorem(title: [1.3 — Two-attachment $\{C_4, C_8\}$-free cubic gadget bounds and witness])[
  Let $H$ be a connected simple $\{C_4, C_8\}$-free two-attachment cubic gadget on $n$ vertices. \
  (a) *Exact closure equivalence & bipartite bound ($n <= 36$):* The cubic closure $H^+ = H + \{0,1\}$ is simple and $\{C_4, C_8\}$-free iff $S(H) inter \{1,3,7\} = emptyset$. Moreover, if $H$ is bipartite, handshaking modulo $3$ places $0$ and $1$ in opposite shores; by Paper II, $S(H) inter \{1,3,7\} != emptyset$ holds unconditionally for all bipartite $\{C_4, C_8\}$-free gadgets with $n <= 36$, and fails sharply at $n = 38$ via $B(19; \{0,1,8\}) - e$. \
  (b) *General exhaustive bound ($n <= 18$) & bridge corollary:* No connected simple $\{C_4, C_8\}$-free two-attachment cubic gadget exists at all for any $n <= 18$. Consequently, letting $n_min >= 20$ be the minimum order of such a gadget, any $\{C_4, C_8\}$-free gadget possessing a bridge separating $0$ and $1$ that is not incident to $0$ or $1$ satisfies $n >= 2 n_min >= 40$. \
  (c) *Genuine $\{C_4, C_8, C_(16)\}$-free stretch witness (4,802 vertices):* Deleting the edge $e = \{(0,I), (1,I)\}$ from $cal(H)(U T_4(FF_7); \{I, I+E_(12)+E_(23), I+E_(23)+E_(34)\})$ produces a bipartite $\{C_4, C_8, C_(16)\}$-free two-attachment gadget of girth $14$ with $min S = 13$ and an explicit simple $0$–$1$ path of length $31 >= 2 dot 13 = 26$ (stretch ratio $>= 31 slash 13 approx 2.3846$).
]

#proposition(title: [1.4 — Low-order $\{C_4, C_8\}$-free cubic Haar census, $|G| <= 45$])[
  Across $89$ finite groups ($16$ cyclic cross-checks $C_3 dots.c C_(18)$, all $27$ cyclic groups $C_(19) dots.c C_(45)$, all $14$ rank-$2$ non-cyclic abelian groups of order $19 <= |G| <= 45$ plus $C_3^3$, and $32$ nonabelian groups complete for all orders $|G| <= 45$ outside $\{24, 32, 36, 40\}$ together with six key order-$24$ groups), there are exactly $822$ connected $\{C_4, C_8\}$-free cubic Haar re-anchoring classes ($105$ cyclic, $223$ non-cyclic abelian, $494$ nonabelian; $2 <= |V| <= 90$). Every single class ($822 slash 822$) contains both a simple $C_(16)$ and an equal-length dyadic theta subgraph $Theta(8,8,8)$.
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
  For (a), adding $\{0,1\}$ makes $H^+ = H + \{0,1\}$ $3$-regular, and $H^+$ is simple iff $\{0,1\} in.not E(H)$ ($1 in.not S(H)$). Assuming $H$ is simple $\{C_4, C_8\}$-free with $1 in.not S(H)$, every $C_4$ or $C_8$ in $H^+$ traverses $\{0,1\}$, leaving a simple $0$–$1$ path in $H$ of length $3$ or $7$. If $H = (A union.sq B, E)$ is bipartite, then $sum_(u in A) deg_H (u) = |E| = sum_(v in B) deg_H (v) mod 3$ forbids $0$ and $1$ from lying in the same shore ($-2 != 0 mod 3$). Hence $H^+$ remains bipartite; by Paper II Theorem 1.3, $S(H) inter \{1,3,7\} != emptyset$ holds for all bipartite $\{C_4, C_8\}$-free gadgets with $n <= 36$, sharp at $n = 38$ via $B(19; \{0,1,8\}) - e$.

  For (b), because $H$ is simple and $C_4$-free with $deg_H (0)=deg_H (1)=2$, $\{0,1\}$ has at most one common neighbor, yielding exactly four neighborhood seeds: `Ia_tri_012` ($\{0,1\},\{0,2\},\{1,2\}$), `Ib_adj_01` ($\{0,1\},\{0,2\},\{1,3\}$), `II_dist2` ($\{0,2\},\{0,3\},\{1,2\},\{1,4\}$), and `III_dist_ge3` ($\{0,2\},\{0,3\},\{1,4\},\{1,5\}$). Exhaustive $C_8$-pruned enumeration across $n in \{4,6,8,10,12,14,16,18\}$ gives zero canonical classes everywhere. Any bridge $e = u_0 u_1$ separating $0$ and $1$ with $u_0, u_1 in.not \{0,1\}$ leaves two connected simple $\{C_4, C_8\}$-free two-attachment gadgets on $(0, u_0)$ and $(1, u_1)$, each of order $>= n_min >= 20$, forcing $n >= 40$.

  For (c), BFS on $G = cal(H)(U T_4(FF_7); \{I, I+E_(12)+E_(23), I+E_(23)+E_(34)\})$ (4,802 vertices) establishes exact girth $14$, bidirectional depth-$8$ DFS excluding endpoints from intermediate sets proves $C_(16)$-freeness on both shores, and deleting $e = \{(0,I), (1,I)\}$ (step $0$ of $w_(32) = #raw("01010102012012101012012010212012")$) leaves exact distance $min S = 13$ alongside a simple $31$-edge residual path ($31 >= 2 dot 13$).
]

Proposition 1.4 is exhaustively certified by `verify_paper3.py`, yielding `0` $\{C_4, C_8\}$-free classes in $C_3 dots.c C_(18)$, `105` in cyclic $C_(19) dots.c C_(45)$ (`0` in $C_(20)$), `223` in non-cyclic abelian groups ($19 <= |G| <= 45$, with `0` in `C2xC10`, `C2xC12`, `C3xC3xC3`, `C4xC8`), and `494` in nonabelian groups (`C7_rtimes_C3`: 14, `C3_rtimes_C8`: 12, `UT3(F3)_exp3`: 72, `C3_x_D5`: 20, `C13_rtimes_C3`: 208, `C3_x_D7`: 42, `(C7_rtimes_C3)_x_C2`: 126; and `0` in the `25` other nonabelian groups checked), with `822 / 822` classes admitting both $C_(16)$ and $Theta(8,8,8)$.

*Reproducibility and AI Disclosure.* Every theorem and finite census is deterministically reproduced by the standalone Python~3 standard-library verifier `paper3_semidirect_and_gadgets/verify_paper3.py` against `certificates/paper3_certificates.json`. Portions of the discovery scripts and manuscript preparation were assisted by AI systems; all theorems, proofs, and executable assertions were audited by the author and rest directly on the deterministic verifiers.

*References.* Burkhart (`arXiv:2611.05060`, 2026); Carr (`arXiv:2605.22844`, 2026); Garcia (`arXiv:2609.04686`, 2026); OvermanOu, companion Paper I & Paper II (2026).
