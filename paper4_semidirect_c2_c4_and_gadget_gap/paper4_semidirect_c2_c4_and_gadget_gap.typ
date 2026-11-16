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
  #text(size: 14.5pt, weight: "bold")[Sharp $C_(16)$ Bounds for Semidirect $C_2$-, $C_4$-, and Klein-Bottle Cubic Haar Graphs and the Defect Point-Graph $C_8$ Identity for Bipartite Gadgets]
  #v(0.5em)
  #text(size: 11pt)[OvermanOu (`ad110158@gmail.com`)] \
  #text(size: 9.5pt, fill: luma(80))[November 17, 2026]
]

#v(0.8em)
#block(inset: (x: 1.5em))[
  #text(size: 9.5pt)[
    *Abstract.* We establish two unconditional advances toward the Erdős–Gyárfás conjecture: sharp $C_(16)$ power-of-two cycle forcing across all Klein-bottle, semidirect $C_2$-, and semidirect $C_4$-extension cubic Haar graphs (extending Paper III from $C_3$ to $2$-cyclic semidirect extensions), and an exact Defect Point-Graph $C_8 (H)$ identity for simple $C_4$-free bipartite two-attachment cubic gadgets $H$. First, let $cal(K)_0 = chevron.l a, b divides a b a^(-1) = b^(-1) chevron.r tilde.equiv ZZ times.r_(-1) ZZ$ be the fundamental group of the Klein bottle. A single $16$-step walk $w_"KB" = #raw("0101010210121202")$ forces a simple $C_4, C_8$, or $C_(16)$ in every connected component of every cubic Haar graph over any quotient of $cal(K)_0$. Via exact prefix-difference partitioning in the universal semidirect groups $ZZ[C_2]^2 times.r C_2$ and $ZZ[C_4]^2 times.r C_4$, the $16$-word $w_(G,10) = #raw("0102021021202012")$ reduces **every** abelian group $A$ and **every** automorphism $sigma in "Aut"(A)$ satisfying $sigma^4 = "id"_A$ (with no further restriction) to either an abelian subgroup (Paper I Theorem 2.1) or the Klein-bottle relation $a b a^(-1) = b^(-1)$, unconditionally forcing $C_4, C_8$, or $C_(16)$ in every component of $cal(H)(A times.r_sigma C_2; S)$ and $cal(H)(A times.r_sigma C_4; S)$. Normal $2$-kernel lifting extends power-of-two cycle forcing to all finite $A times.r_sigma C_(2^r)$ ($sigma^4 = "id"_A$), $"GL"(2,3)$ (`416` pairs), $"Dic"_(4m)$, and regular covers of $Theta(2^k, 2^k, 2^k)$.

    Second, for any simple $C_4$-free bipartite two-attachment cubic gadget $H = (P, L; E)$ on $|V(H)| = 2n$ vertices ($deg_H (p_0) = deg_H (ell_0) = 2$), we prove an exact defect quadratic gap identity expressing $2 C_8 (H)$ via codegrees of its point graph $Q$ modulo the $2$-line edge $e_0 = N_H (ell_0)$, together with a Defect Star-$K_4$ decomposition and local $K_(2,2)$-free neighborhood capacities (`6, 6, 4, -2`), eliminating all $\{C_4, C_8\}$-free bipartite two-attachment gadgets with $|V(H)| <= 28$ ($n <= 14$) completely solver-free and independently of the $0$–$1$ attachment distance.
  ]
]
#v(0.6em)

= Introduction

In companion Paper I and Paper III, we resolved the Erdős–Gyárfás conjecture for simple cubic three-shift Haar graphs $cal(H)(Gamma; S)$ whenever $Gamma$ lies in the normal-$2$-kernel hull of nilpotent groups of class at most six (yielding $C_4, dots.c, C_(64)$) or arbitrary semidirect $C_3$-extensions $A times.r_sigma C_3$ (yielding $C_4, dots.c, C_(32)$, and $C_4, C_8, C_(16)$ under $1 + sigma + sigma^2 = 0$). A natural algebraic question is whether non-nilpotent $2$-step cyclic extensions $A times.r_sigma C_2$ and $A times.r_sigma C_4$—where dihedral, metacyclic, wreath, and Klein-bottle quotients arise directly—satisfy an equally unconditional theorem, and whether a sharper $C_(16)$ bound holds throughout. In parallel, Paper II derived an exact point-graph $C_8$ gap identity for closed cubic bipartite graphs, whereas Paper III showed via Theorem 1.3(a) that every bipartite two-attachment $\{C_4, C_8\}$-free cubic gadget $H = (P, L; E)$ has one degree-$2$ attachment in $P$ ($p_0$) and one in $L$ ($ell_0$), leaving open a structural point-graph obstruction independent of the $0$–$1$ distance.

This paper settles both problems: Theorems 1.1 and 1.2 prove sharp $C_(16)$ forcing for all Klein-bottle quotients, all $A times.r_sigma C_2$, and all $A times.r_sigma C_4$ ($sigma^4 = "id"_A$), while Theorem 1.3 extends Paper II's gap identity to two-attachment bipartite gadgets and eliminates $|V(H)| <= 28$ purely analytically.

== Main results

#theorem(title: [1.1 — Klein-bottle quotients and universal semidirect $A times.r_sigma C_2$])[
  (a) *Klein-bottle quotients:* Let $K = chevron.l a, b chevron.r$ be any group satisfying $a b a^(-1) = b^(-1)$ (any quotient of $cal(K)_0 = chevron.l a, b divides a b a^(-1) = b^(-1) chevron.r tilde.equiv ZZ times.r_(-1) ZZ$) with $1, a, b$ distinct. Then $cal(H)(K; \{1, a, b\})$ contains a simple cycle of length $4, 8$, or $16$. \
  (b) *Universal $A times.r_sigma C_2$:* Let $A$ be any abelian group (finite or infinite) and $sigma in "Aut"(A)$ satisfy $sigma^2 = "id"_A$. Then every connected component of every simple cubic three-shift Haar graph $cal(H)(A times.r_sigma C_2; S)$ contains a simple cycle of length $4, 8$, or $16$.
]

#theorem(title: [1.2 — Universal general $A times.r_sigma C_4$ ($sigma^4 = "id"_A$) and normal $2$-kernel extensions])[
  Let $A$ be any abelian group (finite or infinite) and $sigma in "Aut"(A)$ satisfy *only* $sigma^4 = "id"_A$. \
  (a) *Sharp $C_(16)$ bound:* Every connected component of every simple cubic three-shift Haar graph $cal(H)(A times.r_sigma C_4; S)$ contains a simple cycle of length $4, 8$, or $16$. \
  (b) *Gaussian / Frobenius direct refinement:* When $sigma^2 = -"id"_A$ (covering every abelian-kernel Frobenius group $A times.r C_4$), every normalized shift class admits an explicit $16$-word closing all $56$ same-shore differences directly without conjugation or commutator/Klein-bottle branching (`0` uncovered pairs). \
  (c) *Normal $2$-kernel lifting & covers:* Let $G$ be any finite group admitting a normal $2$-subgroup $N lt.eq.tri G$ such that $G slash N$ embeds in $A times.r_sigma C_2$ or $A times.r_sigma C_4$ for some abelian $A$ and $sigma^4 = "id"_A$—in particular, every finite $A times.r_sigma C_(2^r)$ ($sigma^4 = "id"_A$), $"GL"(2,3)$ (via $Q_8 lt.eq.tri "GL"(2,3)$), and every dicyclic group $"Dic"_(4m)$ (via $C_2 lt.eq.tri "Dic"_(4m)$)—and let $B$ be a connected finite graph containing $Theta(2^k, 2^k, 2^k)$ ($k >= 1$). Then every connected component of $cal(H)(G; S)$ contains $C_(2^m)$ ($m >= 2$) and every connected component of every regular $G$-cover of $B$ contains $C_(2^m)$ ($m >= k + 2$).
]

Next let $H = (P, L; E)$ be any simple $C_4$-free bipartite two-attachment cubic gadget with $|P| = |L| = n$ ($|V(H)| = 2n$), attachments $deg_H (p_0) = deg_H (ell_0) = 2$, and $deg_H (v) = 3$ for all other vertices. Define its _point graph_ $Q$ on $P$ by joining two points iff they share a line of $L$; write $e_0 = N_H (ell_0)$ for the unique $2$-line edge, $E_3 = E(Q) without \{e_0\}$ for the $3n - 3$ edges of $3$-lines, and $lambda_Q (u,v) = |N_Q (u) inter N_Q (v)|$.

#theorem(title: [1.3 — Exact Defect Point-Graph $C_8 (H)$ identity and solver-free bound $|V(H)| >= 30$])[
  For every simple $C_4$-free bipartite two-attachment cubic gadget $H = (P, L; E)$ on $|V(H)| = 2n$ vertices: \
  (a) *Exact Defect Gap Identity:* Let $R_"set" = binom(P, 2) without E_3$. Then
  $ 2 C_8 (H) = sum_(e in E_3) binom(lambda_Q (e) - 3, 2) + sum_(p in R_"set") binom(lambda_Q (p) - 1, 2) - S_"def" (H), $
  where $S_"def" (H) = (n^2 - 13n + 20) slash 2$ in Case 1 ($(p_0, ell_0) in.not E(H)$, where $deg_Q$ has profile $(4, 5, 5, 6^(n-3))$), and $S_"def" (H) = (n^2 - 13n + 16) slash 2$ in Case 2 ($(p_0, ell_0) in E(H)$, where $deg_Q$ has profile $(3, 5, 6^(n-2))$). \
  (b) *Defect Star-$K_4$ structure and solver-free bound $|V(H)| >= 30$:* If $C_8 (H) = 0$, then every $e in E_3$ has $1 <= lambda_Q (e) <= 3$, edge-disjoint star-$K_4$ blocks enforce $E_2 >= E_3^"cnt"$ (where $E_k = \#\{e in E_3 : lambda_Q (e) = k\}$), and $3n - 3 <= 2(3 E_1 + E_2) <= 2 S_"def" (H)$ forces $n^2 - 16n + 23 >= 0$ (Case 1) or $n^2 - 16n + 19 >= 0$ (Case 2). Consequently, no $\{C_4, C_8\}$-free bipartite two-attachment cubic gadget exists for any $4 <= n <= 14$ ($|V(H)| <= 28$), completely solver-free and regardless of the $p_0$–$ell_0$ attachment distance.
]

= Proof of Theorems 1.1 and 1.2

As in Papers I and III, represent closed alternating walks in $cal(H)(K; \{1,a,b\})$ from $(1,0)$ by even-length cyclically nonbacktracking words $w in \{0,1,2\}^(2m)$ with shifts $s_0 = 1, s_1 = a, s_2 = b$ and prefixes $P_0 = 1$, $P_(i+1) = P_i s_(c_i)^((-1)^i)$. Any same-shore collision $P_i = P_j$ ($i != j mod 2$ excluded; $i equiv j mod 2$) yields $d = P_i^(-1) P_j = 1$.

== Proof of Theorem 1.1 (Klein-bottle and $A times.r_sigma C_2$)

#proof(title: "Proof of Theorem 1.1")[
  For (a), realize the universal Klein-bottle group $cal(K)_0 = chevron.l a, b divides a b a^(-1) = b^(-1) chevron.r$ on $ZZ times ZZ$ via $(u_1, t_1)(u_2, t_2) = (u_1 + (-1)^(t_1) u_2, t_1 + t_2)$ with $a = (0, 1)$ and $b = (1, 0)$ (verified $a b a^(-1) = (-1, 0) = b^(-1)$). Evaluating
  $ w_"KB" = #raw("0101010210121202") quad ("length " 16) $
  in $cal(K)_0$ closes identically to $(0, 0)$ while visiting $8 + 8$ distinct vertices. Partitioning all $2 binom(8, 2) = 56$ same-shore prefix differences $d = P_i^(-1) P_j$ modulo conjugation by length-$<= 2$ words in $\{a^(plus.minus 1), b^(plus.minus 1)\}$ yields: `31` shift collapses ($a^(plus.minus 1), b^(plus.minus 1), (a^(-1)b)^(plus.minus 1)$, impossible since $1,a,b$ are distinct), `11` direct and `5` conjugate cyclically nonbacktracking $4$-walks, and `2` direct and `7` conjugate cyclically nonbacktracking $8$-walks, leaving `0` uncovered pairs. Because homomorphic pushforwards preserve closures and conjugation, every quotient $K$ of $cal(K)_0$ with $1,a,b$ distinct either suffers a collision closing a simple $C_4$ or $C_8$ or embeds $w_"KB"$ as a simple $C_(16)$.

  For (b), normalize $cal(H)(K; \{1,a,b\})$ modulo $A$ inside $A times.r_sigma C_2$: if both $a, b in A$ (Case `(0,0)`), $K <= A$ is abelian and Paper I Theorem 2.1 gives $C_4, C_8$, or $C_(16)$; otherwise re-anchoring at $a$ if both project to $1 mod A$ (and swapping $a <-> b$ if needed) puts us in Case `(1,0)`: $a = (u, 1), b = (v, 0)$. The canonical map from $ZZ[C_2]^2 times.r C_2$ sending $e_1 = ((1,0,0,0), 1) |-> a$ and $e_2 = ((0,0,1,0), 0) |-> b$ evaluates
  $ w_(G,10) = #raw("0102021021202012") quad ("length " 16) $
  to the identity with $8 + 8$ distinct vertices and $0$ uncovered same-shore differences modulo length-$<= 2$ conjugation: `27` shift collapses, `15` $4$-walks, `8` $8$-walks, `3` conjugates of $[a,b]^(plus.minus 1)$ (`((0,0,1,-1), 0)`), and `3` conjugates of $(a b a^(-1) b)^(plus.minus 1)$ (`((0,0,1,1), 0)`). Vanishing of $[a,b]$ makes $K$ abelian ($C_4, C_8, C_(16)$), while vanishing of $a b a^(-1) b$ imposes $a b a^(-1) = b^(-1)$, resolved to $C_4, C_8$, or $C_(16)$ by part (a).
]

== Proof of Theorem 1.2 (Universal $A times.r_sigma C_4$ and $2$-kernel lifting)

#proof(title: "Proof of Theorem 1.2")[
  For (a), normalize $S$ to $\{1, a, b\}$ in $K = chevron.l a, b chevron.r <= A times.r_sigma C_4$ and write $overline(S) = \{0, overline(a), overline(b)\} subset.eq C_4$. If $overline(S) subset.eq \{0, 2\}$, then $K <= A times.r_(sigma^2) 2C_4 tilde.equiv A times.r_tau C_2$ ($tau = sigma^2$, $tau^2 = "id"_A$), which reduces directly to Theorem 1.1(b). Otherwise at least one element projects to $1$ or $3 mod 4$; swapping $a <-> b$ and replacing $sigma$ by $sigma^(-1)$ if needed sets $overline(a) = 1$. Further re-anchoring $\{1, a, b\}$ at $a$ gives $\{1, a^(-1), a^(-1) b\}$ with $C_4$-cosets $\{0, 3, (t_b - 1) mod 4\}$, which under $sigma <-> sigma^(-1)$ sends Case `(1,1)` to `(3,0)` $tilde.equiv$ `(1,0)` and `(1,3)` to `(3,2)` $tilde.equiv$ `(1,2)`. Hence only two coset configurations remain: Case `(1,0)` ($t_b = 0$) and Case `(1,2)` ($t_b = 2$).

  Inside the universal semidirect group $ZZ[C_4]^2 times.r C_4$ (where $sigma$ cyclically shifts the four $ZZ$-coordinates of each $ZZ[C_4]$ factor, $e_1 = ((1,0,0,0,0,0,0,0), 1)$, $e_2 = ((0,0,0,0,1,0,0,0), t_b)$), direct evaluation verifies that $w_(G,10) = #raw("0102021021202012")$ closes identically in *both* Case `(1,0)` and Case `(1,2)` with $8 + 8$ distinct vertices, and that under conjugation of depth at most $3$ every one of the $56$ same-shore prefix differences falls cleanly into the same five classes: `27` shift collapses, `15` $4$-walks, `8` $8$-walks, `3` conjugates of $[e_1, e_2]^(plus.minus 1)$ (`(0,0,0,0,1,0,0,-1)` in Case `(1,0)` and `(0,1,0,-1,0,-1,1,0)` in Case `(1,2)`), and `3` conjugates of $(e_1 e_2 e_1^(-1) e_2)^(plus.minus 1)$ (`((0,0,0,0,1,1,0,0), 0)` in Case `(1,0)` and `((1,0,-1,0,0,1,1,0), 0)` in Case `(1,2)`), leaving `0` uncovered pairs in both cases. Since conjugation by $A times.r_sigma C_4$ preserves triviality of $d$, any collision yields either $C_4$, $C_8$, $[a,b]=1$ (abelian subgroup, Paper I Theorem 2.1), or $a b a^(-1) b = 1$ (Klein-bottle relation $a b a^(-1) = b^(-1)$, Theorem 1.1(a)), and no collision yields a simple $C_(16)$.

  For (b), when $sigma^2 = -"id"_A$, every element $(u, 2)$ satisfies $(u, 2)^2 = (u + sigma^2(u), 0) = (0, 0) = 1$, closing `0101` directly in Case `(2,0)`. Using the canonical map from $ZZ[i]^2 times.r C_4$ (where $sigma$ acts as multiplication by $i$), direct word evaluations resolve Cases `(1,0)`, `(1,2)`, and `(1,3)` without conjugation (`0` uncovered pairs), summarized with all finite controls in Table 1.

  For (c), note that $4 C_(2^r)$ is central and normal of $2$-power index inside $A times.r_sigma C_(2^r)$ whenever $sigma^4 = "id"_A$, with quotient $A times.r_sigma C_4$; $Q_8 lt.eq.tri "GL"(2,3)$ has quotient $"GL"(2,3) slash Q_8 tilde.equiv S_3 tilde.equiv C_3 times.r_(-1) C_2$; and $C_2 lt.eq.tri "Dic"_(4m)$ has quotient $D_m tilde.equiv C_m times.r_(-1) C_2$. Applying Paper I Lemma 2.3 (normal $2$-kernel holonomy lifting) and Lemma 2.4 (dyadic equal-path theta reduction) proves all power-of-two cycle and regular cover claims.
]

#figure(
  table(
    columns: 4,
    stroke: 0.5pt + luma(160),
    inset: 5pt,
    fill: (x, y) => if y == 0 { luma(240) },
    align: (left, left, center, left),
    table.header([Family / Control], [Word / Scope], [Uncovered], [Verified Partition / Cycle Lengths]),
    [$cal(K)_0 = ZZ times.r_(-1) ZZ$], [`0101010210121202` (`16`)], [`0 / 56`], [`31` collapse, `11+5` len-$4$, `2+7` len-$8$],
    [$ZZ[C_2]^2 times.r C_2$ (`1,0`)], [`0102021021202012` (`16`)], [`0 / 56`], [`27` collapse, `15` len-$4$, `8` len-$8$, `3` $[a,b]$, `3` $a b a^(-1) b$],
    [$ZZ[C_4]^2 times.r C_4$ (`1,0` & `1,2`)], [`0102021021202012` (`16`)], [`0 / 56`], [`27` collapse, `15` len-$4$, `8` len-$8$, `3` $[a,b]$, `3` $a b a^(-1) b$],
    [$ZZ[i]^2 times.r C_4$ (`1,0`, `1,2`, `1,3`)], [`Gauss_Case_{1_0,1_2,1_3}` (`16`)], [`0 / 56`], [`(18,18,20)`, `(19,22,15)`, `(22,20,14)` direct],
    [$"GL"(2,3)$ (`48` elems)], [`416` generating pairs], [`0`], [$C_4$: `272`, $C_8$: `144`],
    [$C_(13) times.r_5 C_4$ (`52` elems)], [`312` re-anchoring classes], [`0`], [$C_4$: `156`, $C_8$: `156`],
    [$FF_5^4 times.r_"shift" C_4$ (2,500)], [Non-Gaussian `(1,0)`, `(1,2)`], [`0`], [$C_(16)$ in `(1,0)` and $C_(16)$ in `(1,2)`],
    [$25$ Klein-bottle quotients], [$3 <= m, n <= 7$], [`0`], [All `25` realize $C_4, C_8$, or $C_(16)$],
  ),
  caption: [Exact word partitions and finite physical controls certified by `verify_paper4.py`.],
)

= Proof of Theorem 1.3 (Defect Point-Graph Identity & Solver-Free Bound)

#proof(title: "Proof of Theorem 1.3")[
  For (a), because $H = (P, L; E)$ is simple and $C_4$-free, distinct blocks share at most one point, so $Q$ is simple with $|E(Q)| = 3n - 2$, $E(Q) = \{e_0\} union.sq E_3$, and $|E_3| = 3n - 3$. In Case 1 ($p_0 in.not e_0$), $deg_Q$ has profile $(4, 5, 5, 6^(n-3))$, giving $S_2 := sum_(v in P) binom(deg_Q (v), 2) = 6 + 20 + 15(n - 3) = 15n - 19$; in Case 2 ($p_0 in e_0$), $deg_Q$ has profile $(3, 5, 6^(n-2))$, giving $S_2 = 3 + 10 + 15(n - 2) = 15n - 17$.

  Now relate $C_8 (H)$ to $C_4 (Q)$. Each simple $8$-cycle in $H$ lifts from a $4$-cycle in $Q$ using four distinct blocks. A $4$-cycle in $Q$ cannot repeat $e_0$ (a single edge) and can repeat a $3$-line $\{u, v, z\}$ only at two consecutive edges $u z, v z$. Conversely, each $e = u v in E_3$ in $3$-line $\{u, v, z\}$ and each $w in (N_Q (u) inter N_Q (v)) without \{z\}$ yields a unique non-lifting $4$-cycle $u - z - v - w - u$ repeating $\{u, v, z\}$. Hence $C_8 (H) = C_4 (Q) - W$ with $W = sum_(e in E_3) (lambda_Q (e) - 1)$. Moreover, $2 C_4 (Q) = sum_(\{u,v\}) binom(lambda_Q (u,v), 2)$ and $S_2 = sum_(\{u,v\}) lambda_Q (u,v)$, so $sum_(p in R_"set") lambda_Q (p) = S_2 - sum_(e in E_3) lambda_Q (e)$. Expanding $g_E (k) = (k-3)(k-4) slash 2$ and $g_N (k) = (k-1)(k-2) slash 2$ over $E_3$ (size $3n - 3$) and $R_"set" = binom(P, 2) without E_3$ (size $binom(n, 2) - (3n - 3)$) gives
  $ &sum_(e in E_3) g_E (lambda_Q (e)) + sum_(p in R_"set") g_N (lambda_Q (p)) \
    &= 2 C_4 (Q) - 3 sum_(e in E_3) lambda_Q (e) - (S_2 - sum_(e in E_3) lambda_Q (e)) + 6(3n - 3) + binom(n, 2) - (3n - 3) \
    &= 2 (C_4 (Q) - W) + (n(n-1))/2 + 9n - 9 - S_2 = 2 C_8 (H) + S_"def" (H), $
  since $(n^2 - n)/2 + 9n - 9 - (15n - 19) = (n^2 - 13n + 20)/2$ (Case 1) and $(n^2 - n)/2 + 9n - 9 - (15n - 17) = (n^2 - 13n + 16)/2$ (Case 2). All seven finite controls in Table 2 verify both $C_8 (H) = C_4 (Q) - W$ and this identity verbatim.

  For (b), assume $C_8 (H) = 0$. Every edge $e = u v in E_3$ (in $3$-line $\{u, v, z\}$) has $lambda_Q (e) >= 1$ (via $z$) and $lambda_Q (e) <= 3$: if $lambda_Q (e) >= 4$, picking three common neighbors $\{x_1, x_2, x_3\} subset.eq (N_Q (u) inter N_Q (v)) without \{z\}$ leaves only two pairs among $\{x_1, x_2, x_3\}$ inside the remaining blocks at $u$ and $v$ ($<= 1$ pair at $u$ and $<= 1$ pair at $v$), so at least one pair $\{x_i, x_j\}$ uses distinct blocks at both $u$ and $v$, lifting $u - x_i - v - x_j - u$ to a $C_8$ in $H$. Since $g_N (k) >= 0$ for all integers $k$, the gap identity immediately gives $3 E_1 + E_2 <= S_"def" (H)$ with $E_1 + E_2 + E_3^"cnt" = 3n - 3$.

  Next inspect each edge $u v in E_3$ with $lambda_Q (u,v) = 3$ (on $3$-line $\{u,v,z\}$, with extra common neighbors $x, y$). Avoiding $C_8$ on $u - x - v - y - u$ and preserving linearity forces $x, y$ to share a block at *one* endpoint, say $u$; that block $\{u, x, y\}$ has size $3$ (hence cannot be $ell_0$), giving a unique star $(v, T)$ with center $v$ and leaf $3$-line $T = \{u, x, y\} subset.eq E_3$. Each star $(v, T)$ contains at most $3$ spoke edges in $E_3$ ($2$ if $e_0$ is a spoke). Conversely, for every leaf edge $a b in E(T)$ of $T = \{a, b, c\}$ (with spoke blocks $l_a, l_b, l_c$ through $v$), $a b$ has common neighbors $c$ and $v$, and cannot have a third common neighbor $q in.not \{c, v\}$: if $a q, b q$ use blocks $L_a, L_b$ distinct from $l_a, l_b$, then $a - l_a - v - l_b - b - L_b - q - L_a - a$ is a $C_8$ in $H$, whereas if say $L_b = l_b$ ($q in l_b$), then $a - T - c - l_c - v - l_b - q - L_a - a$ is a $C_8$ in $H$! Hence every leaf edge of $(v, T)$ lies in $E_3$ with $lambda_Q = 2$, preventing two distinct stars from sharing a leaf $3$-line and proving $E_2 >= 3 m >= E_3^"cnt"$.

  Combining $E_2 >= E_3^"cnt"$ with $E_1 + E_2 + E_3^"cnt" = 3n - 3$ yields $2(3 E_1 + E_2) >= 2 E_2 + E_1 >= 3n - 3$, so $2 S_"def" (H) >= 3n - 3$. That reduces to $n^2 - 16n + 23 >= 0$ (Case 1) or $n^2 - 16n + 19 >= 0$ (Case 2), both strictly negative for all $4 <= n <= 14$ (`0` feasible $(E_1, E_2, E_3^"cnt")$ profiles at every $n <= 14$; feasible profiles first appear at $n = 15$, with `7` in Case 1 and `3` in Case 2). Complementarily, exhaustive enumeration of $K_(2,2)$-free local point neighborhoods verifies $max (3 c_3 - d) = 6, 6, 4, -2$ across `769, 121, 15, 4` configurations at degrees $6, 5, 4, 3$ respectively.
]

#figure(
  table(
    columns: 7,
    stroke: 0.5pt + luma(160),
    inset: 4.5pt,
    fill: (x, y) => if y == 0 { luma(240) },
    align: (left, center, center, right, right, right, right),
    table.header([Control Gadget], [$n$], [Case], [$C_8 (H)$], [$C_4 (Q) - W$], [$S_"def" (H)$], [`eg3 + rest`]),
    [`Fano_minus_e`], [$7$], [Case 1], [$13$], [$69 - 56$], [$-11$], [$6 + 9 = 15$],
    [`MobiusKantor_minus_e`], [$8$], [Case 1], [$20$], [$71 - 51$], [$-10$], [$2 + 28 = 30$],
    [`Desargues_minus_e`], [$10$], [Case 1], [$22$], [$68 - 46$], [$-5$], [$9 + 30 = 39$],
    [`B19_minus_e`], [$19$], [Case 1], [$0$], [$50 - 50$], [$67$], [$62 + 5 = 67$],
    [`Case2_n9`], [$9$], [Case 2], [$23$], [$79 - 56$], [$-10$], [$9 + 27 = 36$],
    [`Case2_n11`], [$11$], [Case 2], [$28$], [$83 - 55$], [$-3$], [$23 + 30 = 53$],
    [`Fano_disjoint_FanoMinusE`], [$14$], [Case 1], [$34$], [$174 - 140$], [$17$], [$27 + 58 = 85$],
  ),
  caption: [Exact verification of $C_8 (H) = C_4 (Q) - W$ and $2 C_8 (H) = "eg3" + "rest" - S_"def" (H)$ across all seven controls.],
)

*Reproducibility and AI Disclosure.* Every word evaluation, prefix-difference classification, physical group control, defect gap control, local $K_(2,2)$-free capacity count, and solver-free profile exclusion ($n <= 14$) is deterministically reproduced by `paper4_semidirect_c2_c4_and_gadget_gap/verify_paper4.py` against `certificates/paper4_certificates.json`. Portions of the discovery scripts and manuscript preparation were assisted by AI systems; all theorems, proofs, and executable assertions were audited by the author and rest directly on the deterministic verifiers.

*References.* Burkhart (`arXiv:2611.05060`, 2026); Carr (`arXiv:2605.22844`, 2026); Garcia (`arXiv:2609.04686`, 2026); Markström (*Congr. Numer.* 171 (2004), 179–192); OvermanOu, companion Paper I, Paper II, & Paper III (2026).
