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
#let corollary(title: none, body) = block(
  width: 100%,
  inset: (top: 4pt, bottom: 4pt),
  [
    *Corollary#if title != none [ (#title)].* #emph(body)
  ]
)
#let remark(title: none, body) = block(
  width: 100%,
  inset: (top: 4pt, bottom: 4pt),
  [
    *Remark#if title != none [ (#title)].* #body
  ]
)
#let proof(title: "Proof", body) = block(
  width: 100%,
  inset: (top: 2pt, bottom: 6pt),
  [
    #emph[#title.] #body #h(1fr) $square$
  ]
)
#let numbered_eq(tag, body) = grid(
  columns: (1fr, auto),
  align: (center + horizon, right + horizon),
  body,
  [(#tag)]
)

#align(center)[
  #text(size: 15pt, weight: "bold")[The Sharp 38-Vertex Bound for ${C_4, C_8}$-Free Cubic Bipartite Graphs and Dyadic Theta Cover Obstructions]
  #v(0.5em)
  #text(size: 11pt)[OvermanOu (`ad110158@gmail.com`)] \
  #text(size: 9.5pt, fill: luma(80))[November 16, 2026]
]

#v(0.8em)
#block(inset: (x: 1.5em))[
  #text(size: 9.5pt)[
    *Abstract.* Motivated by the Erdős–Gyárfás conjecture on power-of-two cycles in graphs of minimum degree at least three, we determine the exact minimum order of a nonempty simple $3$-regular (cubic) bipartite graph containing neither a $4$-cycle nor an $8$-cycle. While Markström showed that the smallest ${C_4, C_8}$-free cubic graph has $24$ vertices and Garcia recently proved by DRAT-certified SAT search that every ${C_4, C_8}$-free graph with minimum degree at least $3$ has at least $24$ vertices, imposing bipartiteness raises the threshold significantly.

    Representing any $C_4$-free cubic bipartite graph $H$ on $n + n$ vertices as a linear $3$-uniform $3$-regular incidence system with $6$-regular point graph $Q$, we establish an exact nonnegative gap identity for $2 C_8(H)$ in terms of edge and nonedge codegrees of $Q$. When $C_8(H) = 0$, the codegree-$3$ edges of $Q$ decompose into edge-disjoint $3$-spoke stars forming $K_4$ blocks, while the residual codegree-$2$ edges partition into nonblock triangles. Using a mutual-center impossibility argument on locally-$K_(1,3)$ $4$-regular dual line graphs, we prove completely analytically (without SAT solvers or search) that $n >= 18$ (at least $36$ vertices), and that $n >= 19$ whenever every point-graph edge has codegree at least $2$. At the boundary $n = 18$, we eliminate five of the six remaining point-graph profiles and one star-membership branch purely analytically, and close the single remaining branch—profile $(E_1, E_2, E_3) = (6, 27, 21)$ with star memberships $(k_0, k_1, k_2) = (0, 8, 10)$—by an exhaustive dual-graph and boundary-assignment enumeration over all 352,716 labeled $7$-vertex $10$-edge duals and 156,240 point-graph relaxations. Consequently, every nonempty simple ${C_4, C_8}$-free cubic bipartite graph has at least $38$ vertices ($n >= 19$). The connected $38$-vertex cyclic Haar graph $B(19; \{0,1,8\})$ attains this bound and contains a simple $C_(16)$. As a topological consequence, every covering graph of degree at most $18$ of a connected graph containing an equal-length dyadic theta subgraph $Theta(2^k, 2^k, 2^k)$ contains a cycle of length $2^(k+1), 2^(k+2)$, or $2^(k+3)$ in every connected component.
  ]
]
#v(0.6em)

= Introduction

The Erdős–Gyárfás conjecture asks whether every finite simple graph with minimum degree at least $3$ contains a simple cycle of length $2^k$ for some $k >= 2$. Following Liu and Montgomery's resolution for large average degree, the open core of the conjecture resides in cubic and near-cubic graphs. In the finite-order regime, let $f(k)$ denote the smallest order of a cubic graph avoiding all cycles of length $2^m$ ($2 <= m <= k$). Known thresholds give $f(2) = 10$ (Petersen), $f(3) = 24$ (Markström; extended to all minimum-degree-three graphs by Garcia), and $f(4) <= 78$, while general searches have reached order $40$ for minimum degree at least $3$, $48$ for cubic graphs, and $66$ for bipartite graphs (Ducoffe–Dumitru), and Tranquilli proved via certified configuration enumeration that every simple cubic bipartite graph on at most $58$ vertices contains $C_4, C_8$, or $C_(16)$.

Here we establish the sharp bipartite counterpart of $f(3) = 24$ by determining the exact minimum order of a nonempty simple cubic bipartite graph avoiding ${C_4, C_8}$. Beyond its intrinsic extremal interest, this threshold governs topological cover reductions: any $d$-sheeted covering graph of a base graph containing three internally vertex-disjoint paths of equal dyadic length $L = 2^k$ induces a $3$-regular bipartite matching multigraph on $d+d$ vertices, so excluding ${C_4, C_8}$-free simple cubic bipartite graphs through $d <= 18$ forces short power-of-two cycles in every such cover.

== Main results

Let $H = (P, L; E)$ be a finite nonempty simple cubic bipartite graph with $|P| = |L| = n$ (equality follows from $3|P| = |E| = 3|L|$). When $H$ is $C_4$-free, viewing each vertex $y in L$ as a $3$-element block $N_H (y) subset.eq P$ defines a linear $3$-uniform $3$-regular incidence structure on $n$ points, whose $6$-regular point graph $Q$ joins pairs of points occurring together in a block. For distinct $x, y in P$, let $lambda(x,y) = |N_Q (x) inter N_Q (y)|$ denote their codegree in $Q$.

#theorem(title: [1.1 — Point-graph $C_8$ gap identity and residual decomposition])[
  Let $H$ be a finite nonempty simple cubic bipartite $C_4$-free graph with $n$ vertices in each part and point graph $Q$. Then:

  (a) The number $C_8(H)$ of unoriented simple $8$-cycles in $H$ satisfies
  #numbered_eq(1)[
    $ 2 C_8(H) = sum_(u v in E(Q)) ((lambda(u,v) - 3)(lambda(u,v) - 4)) / 2 + sum_(u v in.not E(Q) \ u != v) ((lambda(u,v) - 1)(lambda(u,v) - 2)) / 2 - (n(n - 13)) / 2. $
  ]

  (b) If $C_8(H) = 0$, every edge of $Q$ has codegree $lambda in \{1, 2, 3\}$. Letting $E_i$ count edges of $Q$ of codegree $i$, we have $3 divides E_i$ for $i=1,2,3$, $C_6(H) = (E_2 + 2 E_3) slash 3$, and $E_2 >= E_3$. Moreover, the codegree-$3$ edges partition into $E_3 slash 3$ edge-disjoint $3$-spoke stars forming edge-disjoint $K_4$ subgraphs of $Q$ (each having three codegree-$3$ spokes and three codegree-$2$ leaf edges), and the remaining $E_2 - E_3$ codegree-$2$ edges partition into $(E_2 - E_3) slash 3$ edge-disjoint nonblock triangles of $Q$.
]

#theorem(title: "1.2 — Solver-free analytic lower bound")[
  Every nonempty simple cubic bipartite graph $H$ containing neither $C_4$ nor $C_8$ has at least $18$ vertices in each part ($|V(H)| >= 36$). Moreover, if $E_1 = 0$, then $H$ has at least $19$ vertices in each part ($|V(H)| >= 38$).
]

#theorem(title: "1.3 — Sharp 38-vertex bound")[
  Every nonempty simple cubic bipartite graph $H$ containing neither $C_4$ nor $C_8$ has at least $19$ vertices in each part ($|V(H)| >= 38$). This bound is sharp: the connected $38$-vertex cyclic Haar graph $B(19; \{0,1,8\})$ is ${C_4, C_8}$-free, has point-graph profile $(E_1, E_2, E_3) = (0, 57, 0)$ and $C_6 = 19$, and contains an explicit simple $C_(16)$.
]

#corollary(title: "1.4 — Dyadic theta cover obstruction")[
  Let $B$ be a finite connected simple graph containing three internally vertex-disjoint paths of common length $L = 2^k$ ($k >= 1$) between two vertices, and let $tilde(B)$ be any covering graph of $B$ (not necessarily regular) of finite degree $d <= 18$. Then every connected component of $tilde(B)$ contains a simple cycle of length $2L, 4L$, or $8L$. For $d <= 17$, the proof is completely solver-free.
]

= The Exact $C_8$ Gap Identity and Star Packing

== Linear triple systems and edge codegrees

Let $H = (P, L; E)$ be nonempty, simple, cubic, bipartite, and $C_4$-free with $|P|=|L|=n$. Identifying each $y in L$ with the triple $B_y = N_H (y) subset.eq P$ gives $n$ blocks of size $3$ with each point in $3$ blocks. Since $H$ has no $C_4$, distinct blocks share at most one point, so the triple system is _linear_. Its point graph $Q$ on $P$ joins pairs in a common block; linearity implies $Q$ is simple and $6$-regular, with $3n$ edges and $binom(n, 2) - 3n = n(n-7)/2$ nonedges. Because $3n > binom(n, 2)$ for $1 <= n <= 6$, no nonempty graph exists for $n <= 6$.

#lemma(title: "2.1 — Edge codegree upper bound")[
  If $H$ is ${C_4, C_8}$-free, then $1 <= lambda(u,v) <= 3$ for every edge $u v in E(Q)$.
]

#proof[
  The unique block $\{u, v, z\}$ containing $u, v$ provides at least one common neighbor $z$, so $lambda(u,v) >= 1$. Suppose $lambda(u,v) >= 4$, and choose three common neighbors $x_1, x_2, x_3 in N_Q (u) inter N_Q (v) without \{z\}$. The three blocks through $u$ pair $N_Q (u)$ into three disjoint pairs, one being $\{v, z\}$. Thus $\{x_1, x_2, x_3\}$ meets only two pairs at $u$, so at most one pair inside $\{x_1, x_2, x_3\}$ lies in a common block at $u$, and similarly at most one pair lies in a common block at $v$. Out of $binom(3, 2) = 3$ pairs, at least one pair $\{x_i, x_j\}$ lies in different blocks at $u$ and different blocks at $v$. Since $u, v$ share only $\{u,v,z\}$, the four edges of the $Q$-cycle $u - x_i - v - x_j - u$ lie in four distinct blocks, lifting to a simple $C_8$ in $H$, contradiction.
]

== Proof of Theorem 1.1

#proof(title: "Proof of Theorem 1.1")[
  Let $T$ be the number of unoriented simple $4$-cycles in $Q$. Counting each $4$-cycle twice via its opposite vertex pairs gives $2T = sum_(\{u,v\}) binom(lambda(u,v), 2)$. A $4$-cycle in $Q$ lifts to a simple $C_8$ in $H$ iff its four edges come from four distinct blocks. Because each block induces a triangle in $Q$, a $4$-cycle in $Q$ cannot use three edges of one block and can repeat a block only at two consecutive edges sharing a corner $w$. Conversely, for each edge $u v in E(Q)$ in block $\{u,v,w\}$ and each $z in (N_Q (u) inter N_Q (v)) without \{w\}$, linearity ensures $u z$ and $v z$ belong to distinct blocks different from $\{u,v,w\}$, giving a unique $4$-cycle $u - w - v - z - u$ with one repeated-block corner. Hence
  $ C_8(H) = T - W, #h(2em) W = sum_(u v in E(Q)) (lambda(u,v) - 1). $
  Counting length-$2$ paths in $Q$ by their midpoints yields $sum_(\{u,v\}) lambda(u,v) = n binom(6, 2) = 15n$. Let $t$ be the number of triangles in $Q$; each triangle contributes $1$ to $lambda$ on its three edges, so $sum_(u v in E(Q)) lambda(u,v) = 3t$, $sum_(u v in.not E(Q)) lambda(u,v) = 15n - 3t$, and $W = 3t - 3n$. Setting $g_E (k) = (k-3)(k-4)/2 >= 0$ and $g_N (k) = (k-1)(k-2)/2 >= 0$, we expand
  $ sum_(u v in E(Q)) g_E (lambda) + sum_(u v in.not E(Q)) g_N (lambda) &= 2T - [ 3(3t) - 6(3n) + (15n - 3t) - (n(n-7))/2 ] \ &= 2T - 6t + 3n + (n(n-7))/2 = 2(T - W) + (n(n-13))/2, $
  which gives identity (1) and proves (a) without assuming connectedness.

  Now suppose $C_8(H) = 0$. By Lemma 2.1, $E_1 + E_2 + E_3 = 3n$, and (1) becomes
  #numbered_eq(2)[
    $ 3E_1 + E_2 + R = (n(n-13))/2, #h(2em) R := sum_(u v in.not E(Q) \ u != v) ((lambda - 1)(lambda - 2))/2 >= 0. $
  ]
  Since $3t = E_1 + 2 E_2 + 3 E_3$ and every nonblock triangle of $Q$ lifts to a unique simple $C_6$ in $H$, we have
  $ C_6(H) = t - n = (E_1 + 2E_2 + 3E_3)/3 - (E_1 + E_2 + E_3)/3 = (E_2 + 2E_3)/3. $

  For each codegree-$3$ edge $u v in E(Q)$ with block $\{u,v,z\}$ and additional common neighbors $x, y$, avoiding $C_8$ on $u - x - v - y - u$ and preserving linearity forces $x, y$ to lie in a common block at _exactly one_ endpoint, say $u$. This assigns $u v$ uniquely to the star $(v, T)$ with center $v$ and leaf block $T = \{u,x,y\}$. Conversely, if an external point $v$ is $Q$-adjacent to all three points of a block $T=\{a,b,c\}$, then $v a, v b, v c$ all have codegree $3$ and are assigned to $(v, T)$, so $E_3 = 3m$ where $m$ is the number of stars, and $3 divides E_3$.

  Each star $(v, T)$ produces three nonblock triangles $\{v,a,b\}$, $\{v,b,c\}$, $\{v,c,a\}$ in $Q$, using two codegree-$3$ spokes and one face edge. These $3m = E_3$ nonblock triangles are pairwise distinct across stars: two distinct stars $(v,T)$ and $(v',T')$ cannot share a nonblock triangle, because if $v'=v$ linearity forces $T'=T$, whereas if $v' != v$ then $v' in \{a,b\}$ forces the spoke $v v'$ to belong to both stars, contradicting unique $E_3$-edge assignment. Furthermore, every codegree-$3$ spoke $v a$ of $(v,T)$ has common neighbors $\{z, b, c\}$, so its only two nonblock triangles are $\{v,a,b\}$ and $\{v,a,c\}$; hence _no nonblock triangle outside these $E_3$ star triangles contains a codegree-$3$ edge_.

  Consequently, every face edge $a b$ of $(v, T)$ has $lambda(a,b) >= 2$ (via $c$ and $v$), and cannot have $lambda(a,b) = 3$ (else its unique star would duplicate $\{v,a,b\}$ with a different center); thus $lambda(a,b) = 2$. Moreover, no two distinct centers $v != v'$ can cover the same leaf block $T$ (otherwise $lambda(a,b) >= 3$). Hence the $E_3 slash 3$ star $K_4$ subgraphs are pairwise edge-disjoint, each consisting of three codegree-$3$ spokes and three codegree-$2$ leaf edges. Also $C_6(H) >= E_3$ gives $E_2 >= E_3$, and $C_6(H) = (E_2 + 2E_3)/3 in ZZ$ yields $3 divides E_2$ and $3 divides E_1$. Finally, there are $C_6(H) - E_3 = (E_2 - E_3)/3$ remaining nonblock triangles outside the star triangles; none uses a codegree-$3$ edge, while $E_2 - E_3$ codegree-$2$ edges remain outside the star $K_4$s, and every such remaining codegree-$2$ edge lies in one remaining nonblock triangle (its unique nonblock triangle cannot be a star triangle). Equality forces every remaining nonblock triangle to consist entirely of three residual codegree-$2$ edges, partitioning the residual codegree-$2$ graph into $(E_2 - E_3)/3$ triangles.
]

#remark(title: [2.2 — Baseline bound $n >= 16$])[
  From $E_2 >= E_3$ and $E_1 + E_2 + E_3 = 3n$, we get $2E_2 + E_1 >= 3n$, so $3E_1 + E_2 >= (3n + 5E_1)/2 >= 3n/2$. By (2), $n(n-13)/2 >= 3n/2$, immediately forcing $n >= 16$ whenever $H$ is nonempty. (Exhausting local neighborhoods also excludes $n <= 14$ directly via $3 c(u) <= 6 + d(u)$.)
]

= Residual Graph Structure and Analytic Exclusion through $n <= 17$

Let $F$ be the _residual graph_ obtained by deleting all edges of the $E_3 slash 3$ star-$K_4$ blocks from $Q$. Partition $E(F) = E(F_1) union.sq E(F_2)$, where $F_1$ consists of the $E_1$ edges of codegree $1$ and $F_2$ consists of the $E_2 - E_3$ residual edges of codegree $2$. Thus $|E(F)| = E_1 + E_2 - E_3$. Since the star-$K_4$ blocks are edge-disjoint and $Q$ is $6$-regular, each point $v in P$ lies in $k(v) in \{0, 1, 2\}$ star blocks and has $deg_F (v) = 6 - 3k(v) in \{6, 3, 0\}$. Let $k_0, k_1, k_2$ denote the counts of points in $0, 1, 2$ star blocks, respectively.

#lemma(title: [3.1 — Mutual-center impossibility for locally-$K_(1,3)$ $4$-regular graphs])[
  There is no nonempty simple $4$-regular graph $D$ in which every vertex $u$ has open neighborhood $D[N_D (u)] tilde.eq K_(1,3)$.
]

#proof[
  Suppose such a graph $D$ exists, and for each $u in V(D)$ let $p(u) in N_D (u)$ denote the unique center of the star $D[N_D (u)] tilde.eq K_(1,3)$. If $p(u) = v$, then $u$ is adjacent to all three remaining neighbors of $v$, so $u$ has degree $3$ in $D[N_D (v)]$, forcing $p(v) = u$. Let $x in N_D (u) without \{v\}$. Then $x$ is adjacent to both $u$ and $v$, and $u v in E(D)$, so $u$ and $v$ are adjacent vertices inside $N_D (x)$. Since $D[N_D (x)]$ is a star, its center $p(x)$ must be either $u$ or $v$. By the mutual-center property, $p(x) = u$ forces $p(u) = x$, and $p(x) = v$ forces $p(v) = x$, contradicting $p(u) = v$ and $p(v) = u$.
]

#lemma(title: "3.2 — Line-graph obstruction and residual lower bound")[
  In any nonempty ${C_4, C_8}$-free simple cubic bipartite graph $H$:
  (a) If $E_3 > 0$, then $k_1 > 0$ (and in fact $k_1 >= 2$ since $k_1 + 2 k_2 = 4 E_3 slash 3$ is even).
  (b) $|E(F)| = E_1 + E_2 - E_3 >= 6$.
]

#proof[
  Suppose $E_3 > 0$ and $k_1 = 0$, or suppose $E(F) = emptyset$ (which forces $k_1 = 0$ and $k_0 = 0$, hence $E_3 = 3n > 0$). In either case, every point lying in at least one star-$K_4$ lies in _exactly two_ star-$K_4$s, and has $F$-degree $0$. Define a multigraph $D$ whose vertices are the $E_3 slash 3$ star-$K_4$s and whose edges correspond to the points in $k_2$, joining the two star-$K_4$s containing each point. Since two distinct star-$K_4$s are edge-disjoint, they share at most one point, so $D$ is simple and $4$-regular, and the subgraph of $Q$ induced on the $k_2$ points is precisely the line graph $L(D)$.

  For any vertex $u in V(D)$ representing a star $(v, \{a,b,c\})$, let its center $v$ correspond to edge $u v$ of $D$ and its leaves $a, b, c$ to edges $u x, u y, u z$. In $L(D)$, two edges $u e, u e'$ share two common neighbors from the other edges at $u$, plus a third common neighbor iff $e e' in E(D)$. Because the three spokes $v a, v b, v c$ have codegree $3$ in $Q$ (and all $Q$-neighbors of $k_2$ points lie within their two star blocks) while the leaf edges $a b, b c, c a$ have codegree $2$ in $Q$, $v$ must be adjacent in $D$ to $x, y, z$, while $x, y, z$ are pairwise nonadjacent. Thus $D[N_D (u)] tilde.eq K_(1,3)$ with center $v$ for every $u in V(D)$, contradicting Lemma 3.1. This proves (a). Consequently $F$ is nonempty; its nonisolated vertices have degree $3$ or $6$ in $F$, so $delta >= 3$ on that subgraph gives at least $4$ vertices and $|E(F)| >= 6$, proving (b).
]

#proof(title: "Proof of Theorem 1.2")[
  At $n = 16$, Remark 2.2 forces equality in $24 = S >= 3E_1 + E_2 >= (48 + 5E_1)/2 >= 24$, so $E_1 = 0$ and $E_2 = E_3 = 24$, contradicting Lemma 3.2(b). Thus $n >= 17$.

  Next suppose $E_1 = 0$ (at any $n$). By Theorem 1.1(b), $F = F_2$ is edge-partitioned into triangles, so every vertex of $F$ has _even_ degree in $F$. Since $deg_F (v) = 6 - 3k(v) in \{6,3,0\}$, evenness forces $k_1 = 0$. Lemma 3.2(a) then forces $E_3 = 0$, whence $E_2 = 3n$. Substituting into (2) gives $n(n-13)/2 = 3n + R >= 3n$, and since $n > 0$ we obtain $n >= 19$.

  Finally, at $n = 17$, (2), $E_1 + E_2 + E_3 = 51$, $E_2 >= E_3$, $3 divides E_i$, and $E_1 + E_2 - E_3 >= 6$ yield $3E_1 + E_2 <= 34$ and $E_2 >= (51 - E_1)/2$, forcing $5E_1 <= 17$, i.e., $E_1 in \{0, 3\}$. Checking $E_1 = 3$ requires $24 <= E_2 <= 25$, impossible since $3 divides E_2$. Thus only $E_1 = 0$ (specifically $(0,30,21)$ and $(0,33,18)$) survives arithmetic, which is impossible by $E_1 = 0 => n >= 19$. Hence $n >= 18$.
]

= Order $n = 18$, Sharpness at $n = 19$, and Dyadic Cover Obstructions

At $n = 18$, Theorem 1.2 requires $E_1 > 0$. Combining $E_1 + E_2 + E_3 = 54$, $3E_1 + E_2 + R = 45$ ($R >= 0$), $E_2 >= E_3$, $3 divides E_i$, and $E_1 + E_2 - E_3 >= 6$ restricts $(54 - E_1)/2 <= E_2 <= 45 - 3E_1$, forcing $E_1 in \{3, 6\}$ and leaving exactly six necessary profiles:
$ (3,27,24), #h(1.2em) (3,30,21), #h(1.2em) (3,33,18), #h(1.2em) (3,36,15), #h(1.2em) (6,24,24), #h(1.2em) (6,27,21). $
Furthermore, since $F_2$ has even degrees at every vertex, $deg_(F_1)(v) equiv deg_F (v) mod 2$, so every $k_1$ point has odd $deg_(F_1)(v) >= 1$ and $2 <= k_1 <= 2E_1$ (using Lemma 3.2(a) and even parity of $k_1 + 2 k_2 = 4E_3 slash 3$). Together with
$ k_0 + k_1 + k_2 = 18, #h(1.5em) k_1 + 2 k_2 = (4 E_3)/3, #h(1.5em) 6 k_0 + 3 k_1 = 2(E_1 + E_2 - E_3), $
and simplicity $k_0 + k_1 >= 7$ whenever $k_0 > 0$, we eliminate five of these six profiles analytically.

== Analytic eliminations at $n = 18$

#proposition(title: [4.1 — Analytic profile eliminations at $n = 18$])[
  No ${C_4, C_8}$-free simple cubic bipartite graph on $18 + 18$ vertices can realize any of the five profiles $(3,27,24)$, $(6,24,24)$, $(3,30,21)$, $(3,33,18)$, $(3,36,15)$, or the star-membership case $(k_0, k_1, k_2) = (1, 6, 11)$ of $(6,27,21)$.
]

#proof[
  We examine each case in turn:

  *Case 1: $(3,27,24)$ and $(6,24,24)$.* Both force $(k_0, k_1, k_2) = (0, 4, 14)$, so $F$ is a simple $3$-regular graph on $4$ vertices, i.e., $F tilde.eq K_4$. At least three edges of $F$ belong to $F_1$ (codegree $1$ in $Q$), yet every edge in $K_4$ already has two common neighbors inside $K_4$, contradicting codegree $1$.

  *Case 2: $(3,30,21)$.* The equations force $(k_0, k_1, k_2) = (1, 6, 11)$, with $|E(F)| = 12$, $|E(F_1)| = 3$, and $|E(F_2)| = 9$ (three triangles). Let $h$ be the unique $k_0$ point ($deg_F (h) = 6$), and call the six $k_1$ points boundary points ($deg_F = 3$). Because $deg_(F_2)$ is even, every boundary point has odd $deg_(F_1) >= 1$; since $|E(F_1)| = 3$, $F_1$ is a perfect matching on the six boundary points, and $h$ is incident to no $F_1$-edge. Thus in $F_2$, $deg_(F_2)(h) = 6$ and each boundary point has $deg_(F_2) = 2$. All three $F_2$-triangles must contain $h$ to cover its $6$ edges, so their opposite edges form a second perfect matching on the $6$ boundary points, disjoint from $F_1$. Hence $F$ is a wheel centered at $h$ with alternating $F_1 slash F_2$ rim $C_6$.

  Observe a local property of star blocks: _a point $p$ shared by two star-$K_4$s cannot be the center of one and a leaf of the other_. Indeed, if $(p, \{a,b,c\})$ and $(y, \{p,q,r\})$ were two star blocks, $N_Q (p) = \{a,b,c,y,q,r\}$ would have to be partitioned by the three blocks through $p$; one block is $\{p,q,r\}$, leaving $\{a,b,c,y\}$ to be partitioned into two pairs without pairing any two of $\{a,b,c\}$ (which already form a block), impossible.

  Now consider any $F_2$-rim edge $u v$. Its two common $Q$-neighbors are $h$ (from its $F_2$-triangle) and a third point $z$ from its unique block triangle $\{u,v,z\}$. Let $K_u != K_v$ be the unique star-$K_4$s containing $u$ and $v$. Consider the edge $u z$: it cannot be in $F_1$ (since $h, v$ are two common neighbors of $u, z$), cannot be in $F_2$ (the only $F_2$-neighbors of $u$ are $h$ and $v$), and cannot be a leaf edge of $K_u$ (whose unique block triangle is the leaf triple of $K_u$, which would force $v in K_u$). Thus $u z$ is a codegree-$3$ spoke of $K_u$, and symmetrically $v z$ is a spoke of $K_v$, putting $z in K_u inter K_v$. By the shared-role observation, $u$ and $v$ have the same role (both centers or both leaves) in their stars. Thus the three $F_2$-rim pairs give an _even_ number $c$ of boundary star-centers. However, there are $7$ star blocks in total, and each shared ($k_2$) star-center is a center in both of its stars, so $7 - c$ is even, forcing $c$ to be odd—contradiction.

  *Case 3: $(3,33,18)$.* Here $|E(F_1)| = 3$, $|E(F_2)| = 15$ ($5$ triangles), $2k_0 + k_1 = 12$, and $2 <= k_1 <= 6$, leaving $(a,b) = (k_0,k_1) in \{(3,6), (4,4), (5,2)\}$. Each $k_1$ point uses at least one $F_1$-edge, so $sum_(v in k_0) deg_(F_1)(v) <= 6 - b$. The number $I$ of incidences between $k_0$-points and the $5$ triangles satisfies
  $ I = 1/2 sum_(v in k_0) deg_(F_2)(v) >= (6a - (6 - b))/2 = 2a + 3. $
  If triangle $j$ contains $i_j in \{0,1,2,3\}$ points of $k_0$, then $binom(i_j, 2) >= max(i_j - 1, 2 i_j - 3)$, and because distinct $F_2$-triangles are edge-disjoint, $P := sum_(j=1)^5 binom(i_j, 2) <= binom(a, 2)$. Yet $P >= max(I - 5, 2I - 15)$ yields $P >= 4 > binom(3, 2) = 3$ for $(3,6)$, $P >= 7 > binom(4, 2) = 6$ for $(4,4)$, and $P >= 11 > binom(5, 2) = 10$ for $(5,2)$, contradiction.

  *Case 4: $(3,36,15)$.* Here $|E(F_1)| = 3$, $|E(F_2)| = 21$ ($T=7$ triangles), $2 k_0 + k_1 = 16$, and $(a,b) = (k_0, k_1) in \{(5,6), (6,4), (7,2)\}$. As above, $I >= (6a - (6-b))/2 = 2a + 5$, so the induced graph $G = F_2[k_0]$ has $e = |E(G)| = sum_(j=1)^7 binom(i_j, 2) >= 2I - 3T >= 4a - 11$, giving $e >= 9, 13, 17$ for $a = 5, 6, 7$. Counting length-$2$ wedges in $G$ gives
  $ W_G := sum_(v in V(G)) binom(deg_G (v), 2) = 3 T_G + sum_(x y in.not E(G)) "codeg"_G (x,y) <= 2e + (binom(a, 2) - e)(a - 2), $
  since every edge of $G$ has codegree $2$ in $Q$, bounding $3 T_G <= 2e$. By convexity of $binom(d, 2)$ and monotonicity of $W_G$ in $e$ (while the right-hand side decreases as $e$ increases since $a >= 5$), we evaluate at $e_min$: for $a=5, e >= 9$, balanced degrees $(4,4,4,3,3)$ give $W_G >= 24 > 21$; for $a=6, e >= 13$, $(5,5,4,4,4,4)$ gives $W_G >= 44 > 34$; for $a=7, e >= 17$, $(5,5,5,5,5,5,4)$ gives $W_G >= 66 > 54$, contradiction.

  *Case 5: $(6,27,21)$ with $(k_0, k_1, k_2) = (1, 6, 11)$.* Let $x$ be the unique $k_0$ point ($deg_F (x) = 6$). All $k_2$ points are isolated in $F$, so $x$ is $F$-adjacent to all six $k_1$ points. Each $k_1$ point $u$ has $deg_F (u) = 3$, so besides $x$, $u$ has two $k_1$-neighbors, both adjacent to $x$. Thus $x, u$ have at least two common neighbors in $Q$, forcing every edge at $x$ into $F_2$. However, $|E(F_2)| = 27 - 21 = 6$ consists of just two triangles, which can contribute at most $4$ to $deg_(F_2)(x)$, contradicting $deg_(F_2)(x) = 6$.
]

== Closing $(6,27,21)$ branch $(0,8,10)$ and Proof of Theorem 1.3

Only $(E_1, E_2, E_3, R) = (6, 27, 21, 0)$ with $(k_0, k_1, k_2) = (0, 8, 10)$ remains at $n=18$. Here $Q$ has $7$ star-$K_4$ blocks forming a simple $7$-vertex, $10$-edge dual graph $D$ (whose $10$ edges are the $k_2$ points) with $Delta(D) <= 4$. Each dual vertex $v in V(D)$ receives $4 - deg_D (v)$ private $k_1$ boundary points.

#lemma(title: "4.2 — Dual and boundary reduction")[
  In any realization of $(6,27,21)$ with $(0,8,10)$:
  (a) Every $4$-vertex induced subgraph of $D$ has at most $4$ edges and is not isomorphic to $2 K_2$.
  (b) The two $F_2$-triangles are vertex-disjoint; relabeling them as $\{0,1,2\}$ and $\{3,4,5\}$ with remaining boundary points $6, 7$, the graph $F_1$ has degree sequence $(1,1,1,1,1,1,3,3)$, is edge-disjoint from $F_2$, and satisfies $"codeg"_(F_1 union F_2)(u v) <= 1$ for every $u v in E(F_1)$. Up to the $144$ automorphisms preserving $F_2$, there are exactly $3$ canonical $F_1$ orbits (sizes $18, 18, 36$).
]

#proof[
  For (a), two disjoint edges $a b, c d in E(D)$ represent two $k_2$ points that lie in no common star block and have no incident $F$-edges, so they are nonadjacent in $Q$. A private boundary point belongs to only one star block and cannot join both edges; thus common $Q$-neighbors of $a b$ and $c d$ correspond bijectively to cross edges between $\{a,b\}$ and $\{c,d\}$ in $D$. Since $R = 0$, every $Q$-nonedge has $lambda in \{1,2\}$, forbidding $0$ cross edges (induced $2 K_2$) and $3$ or $4$ cross edges (forcing $5$ or $6$ edges on the $4$-subset).

  For (b), $E_2 - E_3 = 6$ gives two edge-disjoint $F_2$-triangles; if they shared a point, its $F_2$-degree would be $4$, impossible since $deg_F (v) in \{0, 3\}$. Their six vertices are $k_1$ points with $deg_(F_2)=2$, hence $deg_(F_1)=1$, while the other two $k_1$ points $6, 7$ have $deg_(F_1)=3$. Every $F_1$-edge has $Q$-codegree $1$, hence codegree $<= 1$ in $F_1 union F_2$. Let $c in \{0,1\}$ indicate $67 in E(F_1)$ and $t$ count $F_1$-edges among $0 dots.c 5$; degree sums give $2t + p = 6 = 2c + p$, so $t = c$. If $c = 0$, each of $6, 7$ joins $3$ low vertices; splitting $(3,0)$ or $(0,3)$ on a triangle gives a $Q$-codegree $>= 2$ on an $F_1$-edge, leaving only split $(2,1)$ (type A). If $c = 1$, the single low-low edge connects the two triangles and the remaining four low vertices split evenly as $(2,0)$ or $(1,1)$ at vertex $6$ (types B and C).
]

#proof(title: "Proof of Theorem 1.3 and Corollary 1.4")[
  By Theorem 1.2 and Proposition 4.1, any ${C_4, C_8}$-free simple cubic bipartite graph on $<= 36$ vertices must have $n=18$ and realize Lemma 4.2. Exhausting all $binom(21, 10) = 352,716$ labeled $10$-edge graphs on $7$ vertices yields exactly 9,240 admissible duals $D$, forming six $S_7$-orbits with representatives (`graph6` codes `FMowo`, `FhUk_`, `FhdQW`, `FlUk?`, `FsdoW`, `FxckG`; orbit sizes $630, 630, 2520, 420, 2520, 2520$). Exhausting all $binom(28, 6)$ $6$-edge graphs on $8$ boundary vertices finds $110$ with degree sequence $(1^6, 3^2)$, $74$ disjoint from $F_2$, and $72$ obeying the local $F_1$-codegree bound, decomposing into three orbits of sizes $18, 18, 36$ matching representatives A, B, C. Testing all 52,080 star-slot boundary assignments across each of the $3$ shapes (156,240 candidate point graphs across all $18$ blocks) finds _zero_ configurations satisfying $6$-regularity, $F_1 slash F_2 slash$nonedge codegrees, and star-block patterns. Thus $n >= 19$ ($|V(H)| >= 38$).

  For sharpness, let $H = B(19; \{0,1,8\})$ have shores $P = ZZ slash 19 ZZ$, $L = ZZ slash 19 ZZ$ with edges $p_x tilde l_(x+s)$ ($s in \{0,1,8\}$). Direct cycle enumeration confirms $H$ is connected, simple, $3$-regular, bipartite, with $C_4 = C_8 = 0$, $C_6 = 19$, $C_(10) = 171$, $(E_1, E_2, E_3) = (0, 57, 0)$, and an explicit simple $C_(16)$ given by $(p_0, l_0, p_(11), l_(11), p_3, l_3, p_2, l_2, p_1, l_9, p_8, l_(16), p_(15), l_(15), p_7, l_8, p_0)$.

  For Corollary 1.4, take any connected component $tilde(C)$ of $tilde(B)$; it covers $B$ with sheet multiplicity $d' in \{1, dots.c, d\}$, so $d' <= 18$. Lifting the three internally disjoint $L$-paths between $u, v in V(B)$ gives three edge-disjoint perfect matchings between the $d'$ vertices over $u$ and the $d'$ vertices over $v$. A parallel edge pair produces a simple $C_(2L)$ in $tilde(C)$. Otherwise, the matching multigraph is a nonempty simple cubic bipartite graph on $d' + d'$ vertices with $d' <= 18$; by Theorems 1.2 and 1.3, it contains $C_4$ or $C_8$, which expands along the internally disjoint lifted $L$-paths to a simple $C_(4L)$ or $C_(8L)$ in $tilde(C)$. For $d <= 17$, only Theorem 1.2 is invoked.
]

*Reproducibility and AI Disclosure.* The standalone Python~3 standard-library script `paper2_cubic_bipartite_c4c8/verify_paper2.py` executes in under $2$ seconds to re-verify: (i) the gap identity (1) on Fano, Möbius–Kantor, Desargues, two disjoint Fanos, and $B(19;\{0,1,8\})$; (ii) all 4,096 local $6$-point neighborhoods; (iii) all 19,355 labeled simple $4$-regular graphs on $8$ vertices; (iv) the $n=16,17,18$ profile arithmetic; (v) the complete 352,716-dual and 156,240-assignment $Q$-census; and (vi) the $38$-vertex witness $B(19;\{0,1,8\})$. Portions of the census software and manuscript drafting were assisted by AI systems; all proofs and deterministic verification checks were audited by the author.

*References.* Carr (`arXiv:2605.22844`, 2026); Ducoffe–Dumitru (`arXiv:2609.28594`, 2026); Erdős (*Discrete Math.* 165/166, 1997); Garcia (`arXiv:2609.04686`, 2026); Liu–Montgomery (*J. Amer. Math. Soc.* 36, 2023); Markström (*Congressus Numerantium* 171, 2004); Tranquilli (`arXiv:2608.02675`, 2026).
