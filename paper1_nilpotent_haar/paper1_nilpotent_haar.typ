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
  #text(size: 15pt, weight: "bold")[Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four]
  #v(0.5em)
  #text(size: 11pt)[OvermanOu (`ad110158@gmail.com`)] \
  #text(size: 9.5pt, fill: luma(80))[November 17, 2026]
]

#v(0.8em)
#block(inset: (x: 1.5em))[
  #text(size: 9.5pt)[
    *Abstract.* The Erdős–Gyárfás conjecture asserts that every finite simple graph of minimum degree at least three contains a simple cycle whose length is a power of two. Recently, Burkhart proved that every odd-order Cayley graph, and consequently every Cayley graph of a finite nilpotent group, satisfies the conjecture. However, cubic three-shift Haar graphs (bipartite bi-Cayley graphs) over odd-order or nonabelian nilpotent groups are generally non-Cayley, and their $3$-regularity rules out the single-vertex figure-eight induction central to Burkhart's argument.

    Using exact integral Magnus expansions and Hall commutator collection in the free rank-two nilpotent groups of classes two, three, and four, we unconditionally prove that every connected component of every simple cubic three-shift Haar graph over any finite group admitting a normal $2$-subgroup with nilpotent class-at-most-four quotient (in particular, every finite nilpotent group of class at most four, for all primes $p$ and arbitrary exponents) contains a simple cycle of length $2^k$ ($k >= 2$). Moreover, for every finite odd-order nilpotent group of class at most four, every connected component contains a simple $C_4, C_8, C_(16)$, or $C_(32)$: a single $32$-color word resolves all $p >= 5$ class $<= 4$ groups cleanly, while at $p = 3$ a two-stage commutator descent together with an algebraic rigidity lemma reduces the entire branch to a $9$-member order-$243$ critical family $G_("crit")(alpha, beta)$, each admitting balanced $C_(32)$ and $C_(64)$ witnesses. These results yield obstructions for regular covers of connected graphs containing an equal-length dyadic theta subgraph. Finally, we record complementary determinant-$27$ $C_(64)$ certificates in truncated free algebras $(ZZ slash p^k ZZ) chevron.l X, Y chevron.r slash (X,Y)^5$ for all primes $p >= 2$ and $k >= 1$, together with explicit infinite families in $U T_4(FF_p)$ ($p >= 7$, girth $14$) and $U T_6(FF_p) slash chevron.l I + E_(16) chevron.r$ ($p >= 11$, girth at least $18$) demonstrating that $C_(32)$ is sharp in odd-order nilpotent class $<= 4$ Haar graphs. All finite word certificates, algebraic identities, and matrix controls are verified by a standalone zero-dependency Python verifier.
  ]
]
#v(0.6em)

= Introduction

In 1995, Erdős and Gyárfás conjectured that every finite simple graph $G$ with minimum degree $delta(G) >= 3$ contains a simple cycle of length $2^k$ for some integer $k >= 2$. While Liu and Montgomery (2023) settled the conjecture for graphs of sufficiently large average degree, the small-degree regime—particularly $3$-regular (cubic) graphs—remains open. Recent computational and structural progress includes verified lower bounds of $24$ vertices for $\{4,8\}$-free graphs (Garcia, arXiv:2609.04686), $41$ vertices for general minimal counterexamples and $50$ for cubic graphs (Ducoffe–Dumitru, arXiv:2609.28594), $60$ vertices for cubic bipartite graphs (Tranquilli, arXiv:2608.02675), and predominantly cubic structure theorems (Carr, arXiv:2605.22844).

On the algebraic side, Burkhart (arXiv:2611.05060, November 2026) recently proved that every Cayley graph of odd order with symmetric generating set $|S| >= 3$ satisfies the Erdős–Gyárfás conjecture, and deduced the same for Cayley graphs of all finite nilpotent groups. It is natural to ask how far algebraic cycle-forcing extends to the next most symmetric class of $3$-regular graphs: _cubic Haar graphs_ (also called $3$-regular bi-Cayley graphs).

#definition(title: "Three-shift cubic Haar graph")[
  Let $Gamma$ be a group and $S = \{s_0, s_1, s_2\} subset.eq Gamma$ be a set of three distinct elements. The _cubic Haar graph_ $cal(H)(Gamma; S)$ is the simple $3$-regular bipartite graph with vertex set $Gamma times \{0,1\}$ and edge set
  $ E = \{ \{(g,0), (g s_c, 1)\} : g in Gamma, c in \{0,1,2\} \}. $
]

Cubic Haar graphs fall outside Burkhart's Cayley-graph theorem for three structural reasons:
+ An odd-order group contains no involutions, so every undirected Cayley graph $"Cay"(G, S)$ of odd order with $|S| >= 3$ has even degree at least $4$; no cubic odd-order Cayley graph exists.
+ For a cubic Cayley graph over a finite nilpotent group $G$, the symmetric generating set $S$ of size $3$ must contain an involution, which necessarily lies in the normal Sylow $2$-subgroup $P_2 lt.eq.tri G$; consequently the odd quotient $G slash P_2$ receives at most two generators, bypassing the nonabelian odd-order case. By contrast, $cal(H)(K; \{1,a,b\})$ over an odd-order $p$-group $K$ is genuinely cubic, bipartite, and in general not a Cayley graph when $K$ is nonabelian.
+ Burkhart's inductive lifting lemma relies on lifting a _symmetric figure-eight_—two power-of-two simple cycles intersecting at a single vertex. In any $3$-regular graph, two simple cycles meeting at a vertex $v$ must share at least one edge incident to $v$ (since $2 + 2 > 3$), so _no figure-eight exists in any cubic graph_.

A different mechanism is therefore needed to force power-of-two cycles in nonabelian cubic Haar graphs. We use exact integral noncommutative Magnus expansions and Hall commutator collection to obtain universal short closed color words whose same-shore prefix collisions are algebraically obstructed across entire nilpotent group families.

== Main results

#theorem(title: "1.1 — Nilpotent class at most three")[
  Let $Gamma$ be a finite group having a normal $2$-subgroup $N$ such that $Gamma slash N$ is nilpotent of nilpotency class at most $3$ (in particular, $Gamma$ itself may be any finite nilpotent group of class at most $3$). Then every connected component of every simple cubic three-shift Haar graph $cal(H)(Gamma; S)$ contains a simple cycle of length $2^k$ for some $k >= 2$. Moreover, when $Gamma$ is nilpotent of class at most $3$ and odd order, every connected component contains a simple cycle of length $4, 8, 16$, or $32$.
]

#theorem(title: [1.2 — Unconditional nilpotent class at most four and sharp odd-order $C_(32)$ bound])[
  Let $Gamma$ be any finite group admitting a normal $2$-subgroup $N lt.eq.tri Gamma$ such that $Gamma slash N$ is nilpotent of nilpotency class at most $4$ (with no restriction on the Sylow $3$-subgroup or on exponents; in particular, $Gamma$ itself may be any finite nilpotent group of class at most $4$). Then every connected component of every simple cubic three-shift Haar graph $cal(H)(Gamma; S)$ contains a simple cycle of length $2^k$ for some $k >= 2$.

  Moreover, whenever $Gamma$ is a finite odd-order nilpotent group of nilpotency class at most $4$, every connected component of $cal(H)(Gamma; S)$ contains a simple cycle of length $4, 8, 16$, or $32$ (and $C_(32)$ is sharp against Proposition 1.4).
]

Note that Theorem 1.2 requires neither nilpotency of $Gamma$ itself nor any restriction on $exp(Gamma)$ or its $3$-Sylow class (covering nonnilpotent controls such as $P_7 times A_4$ of order $28{,}812$, as well as $U T_5(FF_3)$ and $G_("crit")(0,0) times C_5$ of order $1{,}215$). Moreover, Haar cores govern equal-length dyadic theta lifts in arbitrary regular covers:

#theorem(title: "1.3 — Dyadic theta cover obstruction")[
  Let $B$ be a connected finite simple graph containing a $Theta(L,L,L)$ subgraph, i.e., three internally vertex-disjoint paths of common length $L = 2^k$ ($k >= 1$) connecting two vertices of $B$. Let $Gamma$ be any finite group satisfying the hypotheses of Theorem 1.1 or Theorem 1.2. Then every connected component of every regular $Gamma$-cover of $B$ contains a simple cycle whose length is a power of two.
]

#proposition(title: "1.4 — Truncated free algebras and high-girth families")[
  (a) For every prime $p >= 2$ and every integer $k >= 1$, let $A_(p,k) = (ZZ slash p^k ZZ) chevron.l X, Y chevron.r slash (X,Y)^5$ and $K_(p,k) = chevron.l 1+X, 1+Y chevron.r <= A_(p,k)^times$. Then $cal(H)(K_(p,k); \{1, 1+X, 1+Y\})$ contains a simple $C_(64)$. \
  (b) For every prime $p >= 7$, $K = chevron.l I + E_(12) + E_(23), I + E_(23) + E_(34) chevron.r <= U T_4(FF_p)$ has order $p^4$ and class $3$, and $cal(H)(K; \{I, A, B\})$ has girth $14$ (no $C_4, C_8, C_(16)$) and a simple $C_(32)$. \
  (c) For every prime $p >= 11$, $K = chevron.l I + E_(12) + E_(34) + E_(56), I + E_(23) + E_(45) chevron.r <= U T_6(FF_p) slash chevron.l I + E_(16) chevron.r$ has order $p^6$ and class $4$, and $cal(H)(K; \{I, A, B\})$ has girth at least $18$ (no $C_4, C_8, C_(16)$) and simple $C_(32)$ and $C_(64)$.
]

= Preliminaries, Abelian and Class-2 Haar Graphs, and 2-Kernel Lifting

== Shift normalization and word conventions

Given $cal(H)(Gamma; \{s_0, s_1, s_2\})$, the bijection $(g, 0) |-> (g s_0, 0)$, $(h, 1) |-> (h, 1)$ is a graph isomorphism onto $cal(H)(Gamma; \{1, a, b\})$ where $a = s_0^(-1) s_1$ and $b = s_0^(-1) s_2$ are distinct nonidentity elements. Let $K = chevron.l a, b chevron.r <= Gamma$. The connected component of $(1,0)$ is $cal(H)(K; \{1, a, b\})$, and every component is a left coset translate isomorphic to $cal(H)(K; \{1, a, b\})$.

Represent a closed walk starting at $(1,0)$ in $cal(H)(K; \{1, a, b\})$ by an even-length cyclic word $w = c_0 c_1 dots.c c_(2m-1) in \{0,1,2\}^(2m)$, where colors $0, 1, 2$ denote shifts $s_0 = 1, s_1 = a, s_2 = b$. At even step $i$ (shore $0$ to shore $1$) we right-multiply by $s_(c_i)$; at odd step $i$ (shore $1$ to shore $0$) we right-multiply by $s_(c_i)^(-1)$. Define prefix elements $P_0 = 1$ and $P_(i+1) = P_i s_(c_i)^((-1)^i)$ ($0 <= i < 2m$). The walk is _cyclically nonbacktracking_ if $c_i != c_(i+1)$ for all $i mod 2m$, closes if $P_(2m) = 1$, and forms a _simple cycle_ $C_(2m)$ if $P_(2m) = 1$ and $P_i^(-1) P_j != 1$ for all $0 <= i < j < 2m$ with $i equiv j mod 2$.

== Abelian and class-two foundations

#theorem(title: "2.1 — Universal abelian Haar obstruction")[
  Let $A$ be any abelian group (finite or infinite), and let $0, a, b in A$ be three distinct elements. Then every connected component of $cal(H)(A; \{0, a, b\})$ contains a simple $C_4$, $C_8$, or $C_(16)$.
]

#proof[
  Normalize to $S = \{0, a, b\}$ inside $chevron.l a, b chevron.r <= A$, and evaluate the cyclically nonbacktracking $16$-color word $w_(16) = #raw("0101012010201212")$. In $ZZ^2$ with $a=(1,0)$ and $b=(0,1)$, $w_(16)$ closes at $(0,0)$ and visits $8$ distinct vertices on each shore. Taking canonical differences $v in ZZ^2$ (up to sign, with $v > (0,0)$ lexicographically) across all $56$ same-shore prefix pairs gives exactly $13$ nonzero vectors: three collapse vectors $(0,1)$, $(1,-1)$, $(1,0)$ (excluded since $0,a,b$ are distinct), and ten vectors realized as endpoints of cyclically nonbacktracking short words of length $4$ or $8$:

  #align(center)[
    #table(
      columns: 4,
      stroke: 0.5pt,
      [*Vector $v$*], [*Short word*], [*Vector $v$*], [*Short word*],
      [$(0,2)$], [`0202`], [$(2,-1)$], [`0121`],
      [$(1,-2)$], [`0212`], [$(2,0)$], [`0101`],
      [$(1,1)$], [`0102`], [$(2,1)$], [`01210202`],
      [$(1,2)$], [`01010212`], [$(3,-1)$], [`01212102`],
      [$(2,-2)$], [`1212`], [$(3,0)$], [`01012102`],
    )
  ]

  If $w_(16)$ is simple in $A$, it gives $C_(16)$. Otherwise some $v$ in the table vanishes in $A$, so its short word of length $4$ or $8$ closes. In a simple bipartite graph, a $4$-step cyclically nonbacktracking closed walk is a simple $C_4$, and an $8$-step cyclically nonbacktracking closed walk is either a simple $C_8$ or splits at distance $4$ into a simple $C_4$.
]

#proposition(title: "2.2 — Class-two Haar obstruction")[
  Let $K = chevron.l a, b chevron.r$ have nilpotency class at most $2$, and set $c = [a,b] = a^(-1) b^(-1) a b$. If $"ord"(c) >= 3$ (including $infinity$), then $cal(H)(K; \{1, a, b\})$ contains a simple $C_(16)$ given by one of the two cyclically nonbacktracking words
  $ W_0 = #raw("0101201210102102"), quad W_1 = #raw("0102012010121021"). $
]

#proof[
  In class $2$, $c$ is central and $a^x b^Y = b^Y a^x c^(x Y)$, so the free class-$2$ group is parameterized by triples $(x,y,z) in ZZ^3$ representing $b^y a^x c^z$ with product $(x,y,z)(X,Y,Z) = (x+X, y+Y, z+Z+x Y)$. Both $W_0$ and $W_1$ end at $(0,0,0)$ in the free class-$2$ group, hence close in $K$. Their $8$ prefix triples on each shore are pairwise distinct and satisfy $|Delta x| <= 3$, $|Delta y| <= 1$, and $|Delta z| <= 2$ for every same-shore difference $(Delta x, Delta y, Delta z) = (x_1 - x_2, y_1 - y_2, z_1 - z_2)$.

  If two same-shore prefixes $u=(x_1,y_1,z_1)$ and $v=(x_2,y_2,z_2)$ collide in $K$, then $v^(-1) u = 1$ in $K$. Commuting with $a$ and $b$ yields $c^(-Delta y) = [v^(-1) u, a] = 1$ and $c^(Delta x) = [v^(-1) u, b] = 1$. Since $"ord"(c) >= 3$ and $|Delta y| <= 1$, we get $Delta y = 0$, so $y_1 = y_2$ and $v^(-1) u = a^(Delta x) c^(Delta z)$ with $Delta z = z_1 - z_2$. If $"ord"(c) >= 4$ (or $infinity$), $|Delta x| <= 3$ forces $Delta x = 0$, leaving $c^(Delta z) = 1$ with $1 <= |Delta z| <= 2$, contradiction; thus $W_0$ is simple. If $"ord"(c) = 3$, collision forces $Delta y = 0$ and $Delta x in \{0, 3, -3\}$. The case $Delta x = 0$ again fails, while $Delta x = plus.minus 3$ forces $a^3 = c^h$ for a unique $h in \{0,1,2\}$, making $Delta z + h(Delta x slash 3) equiv 0 mod 3$. Checking all $56$ same-shore pairs shows $W_0$ avoids all collisions for $h in \{0,2\}$ and $W_1$ avoids all collisions for $h = 1$.
]

== Normal 2-kernel lifting and theta cover reductions

#lemma(title: "2.3 — Normal 2-subgroup holonomy lifting")[
  Let $K = chevron.l a, b chevron.r$ be finite with $1, a, b$ distinct, and let $N lt.eq.tri K$ be a normal $2$-subgroup. Put $Q = K slash N$ and $overline(x) = x N$.
  (a) If $|\{1, overline(a), overline(b)\}| < 3$, then $cal(H)(K; \{1, a, b\})$ contains a simple cycle of length $2^(t+1)$ for some $t >= 1$. \
  (b) If $|\{1, overline(a), overline(b)\}| = 3$ and $cal(H)(Q; \{1, overline(a), overline(b)\})$ contains a simple cycle $C_(2^s)$ ($s >= 2$), then $cal(H)(K; \{1, a, b\})$ contains a simple cycle $C_(2^(s+t))$ for some $t >= 0$.
]

#proof[
  In (a), two distinct shifts $s, s'$ satisfy $s' s^(-1) in N without \{1\}$, of order $2^t$ ($t >= 1$). Alternating colors $s$ and $s'$ gives a simple cycle of length $2^(t+1)$. In (b), let $w$ trace the simple $2^s$-cycle in $Q$. Lifting $w$ from $(0, 1_K)$ ends at $(0, h)$ with $h in N$ of order $2^t$. Repeating $w$ $2^t$ times yields a simple cycle of length $2^(s+t)$: distinct positions modulo $2^s$ have distinct images in $Q$, while congruent positions differ by left-multiplication by $h^r$ ($0 < r < 2^t$).
]

#lemma(title: "2.4 — Dyadic equal-path theta cover reduction")[
  Let $B$ be a finite connected simple graph containing three internally vertex-disjoint paths $pi_0, pi_1, pi_2$ of common length $L = 2^k$ ($k >= 1$) between two vertices $u, v in V(B)$. Let $tilde(B)$ be a regular $Gamma$-cover of $B$ for a finite group $Gamma$. If every component of every simple cubic three-shift Haar graph over every subgroup of $Gamma$ contains a power-of-two cycle, then every connected component of $tilde(B)$ contains a power-of-two cycle.
]

#proof[
  Let $g_0, g_1, g_2 in Gamma$ be the path voltages of $pi_0, pi_1, pi_2$ from $u$ to $v$. If $g_c = g_(c')$ for $c != c'$, lifting $pi_c$ and $pi_(c')$ from any vertex over $u$ yields a simple $C_(2L)$ in that component by unique path lifting. Otherwise $g_0, g_1, g_2$ are distinct; relabeling the $v$-fiber by $g_0^(-1)$ realizes the lifted branches as $cal(H)(Gamma; \{1, g_1 g_0^(-1), g_2 g_0^(-1)\})$. Since $B$ is connected, every component of $tilde(B)$ meets the $u$-fiber and contains a component of this Haar core; its simple $2^s$-cycle expands to a simple $2^(s+k)$-cycle in $tilde(B)$.
]

= Finite Nilpotent Groups of Class at Most Three

We use $[x,y] = x^(-1) y^(-1) x y$ and basic commutators $c = [a,b]$, $d = [c,a]$, $e = [c,b]$. In the free rank-two class-$3$ nilpotent group $F_2 slash gamma_4(F_2)$, every element has a unique ordered Hall normal form $a^x b^y c^z d^u e^v$ with $(x,y,z,u,v) in ZZ^5$, faithfully separated via the Magnus map $a |-> 1+X, b |-> 1+Y$ into $ZZ chevron.l X,Y chevron.r slash (X,Y)^4$.

== Universal $C_(32)$ for $p >= 5$ and $p = 3$ with exponent at least $9$

The cyclically nonbacktracking $32$-color word $w_(32) = #raw("01010102012012101012012010212012")$ evaluates to $1$ in $ZZ chevron.l X,Y chevron.r slash (X,Y)^4$ with Hall coordinates $(0,0,0,0,0)$, hence closes in every two-generator group of nilpotency class at most $3$.

#proposition(title: [3.1 — Universal $C_(32)$ for $p >= 5$])[
  Let $K = chevron.l a, b chevron.r$ have nilpotency class at most $3$ with $[a,b] != 1$. Suppose there exists a prime $p >= 5$ and a homomorphism $phi : K -> FF_p^2$ sending $a, b$ to a basis of $FF_p^2$. Then $w_(32)$ traces a simple $C_(32)$ in $cal(H)(K; \{1,a,b\})$. In particular, every simple cubic Haar graph component over a finite $p$-group of class at most $3$ ($p >= 5$) contains $C_4, C_8, C_(16)$, or $C_(32)$.
]

#proof[
  Across all $240$ same-shore prefix differences $P_i^(-1) P_j = a^x b^y c^z d^u e^v$, exact Hall collection yields the abelian gcd $gcd(|x|, |y|)$ histogram $0:7, #h(0.35em) 1:174, #h(0.35em) 2:39, #h(0.35em) 3:16, #h(0.35em) 4:4$. For $p >= 5$, none of the $233$ pairs with nonzero gcd can vanish under $phi$. The $7$ zero-abelian pairs $(1,27), (2,28), (7,13), (8,14), (17,23), (18,24), (19,25)$ correspond to $6$-step arcs `120120`, `201201`, or `012012`, whose closure is equivalent to $[a,b] = 1$, contradicting $[a,b] != 1$. If $K$ is a nonabelian finite $p$-group, Burnside's basis theorem gives $K slash Phi(K) tilde.equiv FF_p^2$; if $K$ is abelian, Theorem 2.1 applies.
]

#proposition(title: [3.2 — $p = 3$ with abelianization exponent $>= 9$])[
  Let $K = chevron.l a, b chevron.r$ be a finite nonabelian $3$-group of nilpotency class at most $3$. If $K_("ab") = K slash [K,K]$ has exponent at least $9$, then $cal(H)(K; \{1,a,b\})$ contains a simple $C_(32)$.
]

#proof[
  Let $alpha, beta$ be the images of $a, b$ in $K_("ab")$. If two of $alpha, beta, beta - alpha$ were killed by $3$, then $3 alpha = 3 beta = 0$ and $exp(K_("ab")) <= 3$, contradiction. Re-anchoring $\{1,a,b\}$ at an appropriate shift $t in \{1,a,b\}$ produces an isomorphic Haar graph generating $K$ whose new generators both satisfy $3 overline(a) != 0$ and $3 overline(b) != 0$ in $K_("ab")$. Evaluating $w_(32)$ on this pair, all $217$ pairs with $gcd(|x|,|y|) in \{1,2,4\}$ are nonzero in $K_("ab") slash 3 K_("ab") tilde.equiv FF_3^2$; all $16$ pairs with $gcd = 3$ satisfy $(x,y) in \{(-3,0)^5, (3,0)^9, (0,3)^2\}$, nonzero in $K_("ab")$; and the $7$ zero pairs force $[a,b]=1$.
]

== The remaining $p = 3$, $K_("ab") tilde.equiv C_3 times C_3$ branch

#lemma(title: "3.3 — Cube centrality")[
  Let $K = chevron.l a, b chevron.r$ be a finite nonabelian $3$-group of nilpotency class exactly $3$ with $K_("ab") tilde.equiv C_3 times C_3$. Then $a^3, b^3 in gamma_3(K) <= Z(K)$ and $c^3 = 1$, while $c in.not gamma_3(K)$.
]

#proof[
  In class $3$, $gamma_3(K) = chevron.l d, e chevron.r <= Z(K)$ and $gamma_2(K) = chevron.l c, d, e chevron.r$ is abelian, with $a^3, b^3 in gamma_2(K)$. The free class-$3$ collection identities $[a^3, b] = c^3 d^3$ and $[a, b^3] = c^3 e^3$ put $c^3 in gamma_3(K) <= Z(K)$, whence $d^3 = [c^3, a] = 1$ and $e^3 = [c^3, b] = 1$. Writing $a^3 = c^r d^s e^t$ and $b^3 = c^u d^v e^w$ ($r,u in \{0,1,2\}$), $[a^3, a] = [b^3, b] = 1$ gives $d^r = e^u = 1$, while $[a^3, b] = e^r$ and $[a, b^3] = d^(-u)$ yield $c^3 = e^r = d^(-u)$. If $r != 0 mod 3$, then $d = 1$ forces $c^3 = 1$, hence $e^r = 1$ and $e = 1$, contradicting class $3$. Thus $r = 0$, and symmetrically $u = 0$, so $a^3, b^3 in gamma_3(K)$ and $c^3 = 1$. Finally, $c in gamma_3(K)$ would imply $gamma_2(K) = gamma_3(K) <= Z(K)$, forcing $gamma_3(K) = 1$.
]

#proposition(title: [3.4 — Balanced $C_(32)$ for $K_("ab") tilde.eq C_3 times C_3$])[
  Let $K = chevron.l a, b chevron.r$ be a finite nonabelian $3$-group of class $3$ with $K_("ab") tilde.equiv C_3 times C_3$. Then $cal(H)(K; \{1,a,b\})$ contains a simple balanced $C_(32)$ (zero signed exponent sum in both $a$ and $b$). If $e = [[a,b],b] != 1$, it is given by $w_(32)^("bal") = #raw("01010201021201201020201210212012")$; if $e = 1$, swapping colors $1$ and $2$ works.
]

#proof[
  Exact Magnus collection shows $w_(32)^("bal")$ closes in $F_2 slash gamma_4(F_2)$ with signed exponents $(0,0)$. Among all $240$ same-shore prefix pairs $P_i^(-1) P_j = a^x b^y c^z d^u e^v$, _only five pairs_ satisfy $3 mid x, y, z$, namely $(3,23), (4,22), (5,21), (6,20), (7,19)$, and all five have exact integer Hall coordinates $(0,0,0,0,-1)$, i.e., $e^(-1)$. By Lemma 3.3, $P_i equiv P_j mod gamma_3(K)$ iff $3 mid x,y,z$. Thus if $e != 1$ no collision occurs; if $e = 1$, class $3$ forces $d != 1$, and swapping $a <-> b$ gives $e' = [[b,a],a] = [c^(-1), a] = d^(-1) != 1$.
]

#proof(title: "Proof of Theorem 1.1")[
  Normalize to $K = chevron.l a, b chevron.r <= Gamma$ and quotient by $N_K = K inter N$ via Lemma 2.3. If shifts collide in $Q = K slash N_K$, we get a power-of-two cycle immediately. Otherwise $Q$ is finite nilpotent of class at most $3$. If $Q$ is abelian, Theorem 2.1 gives $C_4, C_8$, or $C_(16)$. Otherwise $Q = product_p Q_p$ is nonabelian of odd order. If some $Q_p$ ($p >= 5$) is noncyclic, Proposition 3.1 yields $C_(32)$ in $Q$. Otherwise $Q = P_3 times C_m$ with $gcd(m,6) = 1$, $C_m$ cyclic central, and $P_3$ nonabelian of class $2$ or $3$. If $P_3$ has class $2$, then $Q$ has class $2$ and odd order, so $"ord"([overline(a), overline(b)]) >= 3$ and Proposition 2.2 gives $C_(16)$. If $P_3$ has class $3$ and $exp((P_3)_("ab")) >= 9$, Proposition 3.2 gives $C_(32)$. If $(P_3)_("ab") tilde.equiv C_3^2$, the balanced $C_(32)$ word of Proposition 3.4 closes identically in the central factor $C_m$ and has distinct vertices in $P_3$, hence gives a simple $C_(32)$ in $Q$.
]

= Unconditional Class-Four Theorem, Rigidity, and Boundary Families

In $F_2 slash gamma_5(F_2)$, let $f = [d,a]$, $g = [d,b]$, $h = [e,b]$; by Hall–Witt, $[e,a] = g$ modulo $gamma_5(F_2)$, and $gamma_2(G)$ is abelian in every class-$4$ group. Unique Hall normal forms are $a^x b^y c^z d^u e^v f^r g^s h^t in ZZ^8$, faithfully separated by the degree-$4$ Magnus expansion (whose degree-$4$ minor on $(f,g,h)$ has determinant $-1$), yielding the exact cube commutator identities
$ [a^3, b] = c^3 d^3 f, quad [a, b^3] = c^3 e^3 h, quad [c^3, a] = d^3, quad [c^3, b] = e^3. $

== Sharp $C_(32)$ for $p >= 5$ and two-stage descent for $p = 3$

Consider the two balanced cyclically nonbacktracking $32$-color words
$ w_4 = #raw("01012012102021010202102120101202"), $
$ w_5 = #raw("01012020101201210202101020210212"). $
Both evaluate to $(0)^8$ in $F_2 slash gamma_5(F_2)$ with abelian gcd histogram $0:19, #h(0.35em) 1:177, #h(0.35em) 2:44$ (hence zero pairs with nonzero $(x,y) equiv (0,0) mod 3$), and all $19$ zero-abelian differences satisfy $z in \{-1, 1, 3, 4\}$.

#proposition(title: [4.1 — Sharp $C_(32)$ for class-$<= 4$ $p$-groups with $p >= 5$])[
  Let $p >= 5$ be a prime and let $G = chevron.l a, b chevron.r$ be a nonabelian finite $p$-group of nilpotency class at most $4$ (arbitrary exponent). Then $w_4$ traces a simple balanced $C_(32)$ in $cal(H)(G; \{1,a,b\})$.
]

#proof[
  Since $G slash Phi(G) tilde.equiv FF_p^2$ on $a, b$ and $c = [a,b] in.not gamma_3(G)$ has order divisible by $p >= 5$ modulo $gamma_3(G)$, none of the $221$ differences with $gcd(|x|,|y|) in \{1,2\}$ vanish in $G slash Phi(G)$ and none of the $19$ differences with $x=y=0$ and $z in \{-1,1,3,4\}$ vanish modulo $gamma_3(G)$.
]

#lemma(title: [4.2 — Two-stage elimination for class-4 $3$-groups])[
  Let $G = chevron.l a, b chevron.r$ be a finite $3$-group of nilpotency class $4$. \
  (1) If $"ord"(c mod gamma_3(G)) >= 9$, then $w_4$ traces a simple balanced $C_(32)$ in $cal(H)(G; \{1,a,b\})$. \
  (2) Otherwise $c^3 in gamma_3(G)$. Then $w_4$ or $w_5$ traces a simple balanced $C_(32)$ unless BOTH $c^3 in gamma_3(G)^3 gamma_4(G)$ and $d e in gamma_3(G)^3 gamma_4(G)$. \
  (3) When $c^3, d e in gamma_3(G)^3 gamma_4(G)$, we have $gamma_3(G)^3 <= gamma_4(G)^3$ and $gamma_4(G) slash gamma_4(G)^3 tilde.equiv FF_3 dot overline(f)$. Setting $c^3 = overline(f)^mu$ and $d e = overline(f)^lambda$ modulo $gamma_4(G)^3$ defines the quotient $Q_("crit")(mu, lambda)$ ($mu, lambda in FF_3$), and $\{w_4, w_5\}$ eliminate $8 slash 9$ pairs, leaving uniquely $(mu, lambda) = (2, 1)$.
]

#proof[
  For (1), if $"ord"(c mod gamma_3(G)) >= 9$, then $c^z in.not gamma_3(G)$ for $z in \{-1,1,3,4\}$ while all remaining pairs have $gcd(|x|,|y|) in \{1,2\}$ (nonzero in $G slash Phi(G) tilde.equiv FF_3^2$). For (2), set $V = gamma_3(G) slash (gamma_3(G)^3 gamma_4(G)) != 0$. Every $(0,0,3 mid z)$ pair satisfies $(z, u mod 3, v mod 3) = (3,1,1)$ in $w_4$ and $(3,2,2)$ in $w_5$. Testing all $24$ triples $(D, E, C_3) in (FF_3^2 without \{(0,0)\}) times FF_3$ for linear functionals $phi : V -> FF_3$ eliminates $22 slash 24$, leaving only $(1,2,0)$ and $(2,1,0)$, forcing $c^3, d e in gamma_3(G)^3 gamma_4(G)$. For (3), commuting $c^3 = d^(3p) e^(3q) w_c$ ($w_c in gamma_4(G)$) with $a,b$ yields $d^3, e^3 in gamma_4(G)^3$, so $gamma_3(G)^3 <= gamma_4(G)^3$. Thus $d e in gamma_4(G) mod gamma_4(G)^3$, giving $f g, g h in gamma_4(G)^3$ and $W = gamma_4(G) slash gamma_4(G)^3 tilde.equiv FF_3 dot overline(f)$ (Burnside). Passing to $G slash gamma_4(G)^3$, $w_4$ and $w_5$ eliminate $8 slash 9$ pairs $(mu, lambda) in FF_3^2$, leaving only $(mu, lambda) = (2, 1)$.
]

Next set $w_0 = #raw("01010120121010210201210210102012")$ and $w_0^("swap") = #raw("02020210212020120102120120201021")$. Both close identically in $F_2 slash gamma_5(F_2)$; their nonzero $(x,y) equiv (0,0) mod 3$ pairs occur solely at $(plus.minus 3, 0)$ (for $w_0$) and $(0, plus.minus 3)$ (for $w_0^("swap")$), and both induce zero collisions in $Q_("crit")(2,1)$ among $(x,y)=(0,0)$ pairs. Hence whenever $exp(G_("ab")) >= 9$, either $3 overline(a) != 0$ ($w_0$ simple) or $3 overline(a) = 0, 3 overline(b) != 0$ ($w_0^("swap")$ simple), closing the $exp(G_("ab")) >= 9$ regime.

== Algebraic Rigidity Lemma for $G_("ab") tilde.equiv C_3^2$ and proofs of Theorems 1.2 and 1.3

#lemma(title: [4.3 — Algebraic rigidity at $G_("ab") tilde.equiv C_3 times C_3$])[
  Suppose $G = chevron.l a, b chevron.r$ is a finite $3$-group of class $4$ with $G_("ab") tilde.equiv C_3 times C_3$ in the surviving branch of Lemma 4.2 ($c^3, d e in gamma_3(G)^3 gamma_4(G)$ and $(mu, lambda) = (2,1)$). Then $f^3 = 1$ identically in $G$, $|G| = 243$, and $G tilde.equiv G_("crit")(alpha, beta)$ ($a^3 = f^alpha, b^3 = f^beta$) for some $(alpha, beta) in FF_3^2$. Moreover, $w_0$ ($alpha != 0$) or $w_0^("swap")$ ($alpha = 0, beta != 0$) resolves all $8$ pairs $(alpha, beta) != (0,0)$; and in $G_("crit")(0,0)$, $0 slash 288$ free-class-$4$ $32$-words survive, yet the balanced non-free word $w_(32,"crit")^("bal") = #raw("02020101210120101021021012101021")$ traces a simple balanced $C_(32)$, while
  $ w_(64,"crit") = #raw("0101210120120212102012020120102021012012120121202102121012021021") $
  traces a simple balanced $C_(64)$ in all $9$ groups $G_("crit")(alpha, beta)$.
]

#proof[
  Applying Lemma 3.3 to $G slash gamma_4(G)$ puts $c^3 in gamma_4(G) <= Z(G)$ and $a^3, b^3 in gamma_3(G)$ in $G$ itself. Commuting $c^3 in Z(G)$ forces $d^3 = e^3 = 1$ in $G$, whence $gamma_3(G)^3 = gamma_4(G)^3$. From $d e in gamma_3(G)^3 gamma_4(G) = gamma_4(G) <= Z(G)$, commuting with $a,b$ gives $f g = g h = 1$ in $G$, so $gamma_4(G) = chevron.l f chevron.r$ is cyclic. Writing $a^3 = d^s e^t w_a$ and $b^3 = d^u e^v w_b$ ($s,t,u,v in \{0,1,2\}$, $w_a, w_b in gamma_4(G)$), $1 = [a^3, a] = f^(s-t)$ and $1 = [b^3, b] = f^(v-u)$ force $s = t$ and $u = v$ (since $"ord"(f) >= 3$ is a power of $3$), putting $a^3, b^3 in gamma_4(G) = chevron.l f chevron.r$. Finally $d e = f^(lambda_0)$ ($lambda_0 equiv 1 mod 3$) gives $f^(3 lambda_0) = (d e)^3 = d^3 e^3 = 1$, forcing $f^3 = 1$ identically in $G$. Thus $|G| = 243$ and $G tilde.equiv G_("crit")(alpha, beta)$; the finite checks on $w_0, w_0^("swap"), w_(32,"crit")^("bal"), w_(64,"crit")$ and all $288$ free-class-$4$ $32$-words are verified exhaustively.
]

#proof(title: "Proof of Theorems 1.2 and 1.3")[
  Normalize to $K = chevron.l a, b chevron.r <= Gamma$ and pass to $Q = K slash (K inter N) = product_p Q_p$ via Lemma 2.3. If shifts collide in $Q$, Lemma 2.3(a) yields a power-of-two cycle upstairs. Otherwise $Q$ is finite nilpotent of class $<= 4$; if abelian or class $<= 3$, Theorems 1.1 and 2.1 yield $C_4, C_8, C_(16)$, or $C_(32)$ in $Q$, lifting via Lemma 2.3(b).

  If $Q$ has class $4$ and some $Q_p$ ($p >= 5$) is nonabelian, Proposition 4.1 (or Propositions 2.2, 3.1) yields a balanced $C_(16)$ or $C_(32)$ word closing in $F_2 slash gamma_5(F_2)$, hence closing in $Q$ and simple via $Q -> Q_p$. Otherwise $Q = P_3 times C_m$ with $gcd(m,6) = 1$, $C_m$ cyclic central, and $P_3$ of class $4$. By Lemmas 4.2 and 4.3, $cal(H)(P_3; \{1, overline(a), overline(b)\})$ always admits a balanced simple $C_(32)$ word ($w_4, w_5, w_0, w_0^("swap")$, or $w_(32,"crit")^("bal")$), which closes identically in $P_3 times C_m$ and separates all $32$ vertices in $Q$, lifting to $K$ via Lemma 2.3(b). Setting $N = 1$ for odd-order nilpotent class $<= 4$ groups establishes the sharp $C_(32)$ bound. Theorem 1.3 follows directly from Lemma 2.4.
]

== Determinant-$27$ $C_(64)$ certificates, truncated free algebras, and boundary controls

For $p >= 5$, an alternative $C_(64)$ certificate is provided by the three cyclically nonbacktracking $64$-color words:
$ w_(64)^((1)) = #raw("0101012012021020101021021012012101020120210210101012102101201201"), $
$ w_(64)^((2)) = #raw("0202021021012010202012012021021202010210120120202021201202102102"), $
$ w_(64)^((3)) = #raw("1010102102120121010120120102102010121021201201010102012010210210"). $

#lemma(title: "4.4 — Exact prefix structure")[
  Each $w_(64)^((k))$ ($k=1,2,3$) evaluates to $(0)^8$ in $F_2 slash gamma_5(F_2)$. Across its $992$ same-shore prefix differences:
  (1) $80$ pairs have $(x,y)=(0,0)$, and $912$ have $1 <= gcd(|x|,|y|) <= 4$ ($1:668, #h(0.35em) 2:136, #h(0.35em) 3:84, #h(0.35em) 4:24$).
  (2) Among the $80$ pairs with $x=y=0$, $28$ have $z != 0$ and $1 <= |z| <= 4$.
  (3) The remaining $52$ pairs split into $47$ pairs with $(u,v) = lambda_k (u_0^((k)), v_0^((k)))$ ($|lambda_k| in {1,2}$, directions $(1,-1), (1,-1), (0,1)$) and $5$ central pairs $plus.minus v_k$, where $v_1 = (-3,3,0)$, $v_2 = (0,-3,3)$, $v_3 = (0,3,0)$ ($det = 27$).
]

#proof(title: "Proof of Proposition 1.4")[
  For (a), the words $w_("p3") = #raw("0101010102020120101020121020201202102020121020101021020201010101")$ (for $p=3$) and $w_(64)^((1))$ (for $p != 3$) both equal $1$ in $ZZ chevron.l X,Y chevron.r slash (X,Y)^5$, and their $992$ same-shore coefficient gcds have histograms $1:978, #h(0.35em) 2:2, #h(0.35em) 5:8, #h(0.35em) 7:4$ (coprime to $3$) and $1:987, #h(0.35em) 3:5$ (coprime to every $p != 3$), respectively. Thus their vertices are distinct modulo $p$, hence modulo $p^k$ for all $k >= 1$. Parts (b) and (c) follow from exact integral enumeration of all 71,004 cyclically nonbacktracking words of lengths $4..16$ in $U T_4(ZZ)$ (max prime factor $5$, plus $C_(14)$ and $C_(32)$ witnesses) and all 87,390 words of lengths $4..16$ in $U T_6(ZZ) slash chevron.l E_(16) chevron.r$ (prime factors in $\{2,3,5,7\}$, plus $C_(32)$ and $C_(64)$ witnesses).
]

= Open Frontier, Reproducibility, and Provenance

With nilpotency class at most four unconditionally resolved across all primes and exponents, two natural algebraic frontiers remain open for cubic Haar graphs: (1) nilpotency class $c >= 5$, where inductive subgraph-lifting analogous to Burkhart's quotient reduction (adapted to cubic subgraphs such as equal-length dyadic thetas) appears far more promising than enumerating ever longer free-group words; and (2) non-nilpotent solvable cubic Haar extensions beyond $A times.r_sigma C_3$ (treated in the companion Paper III).

*Reproducibility and AI Disclosure.* All word identities, gcd histograms, Hall coordinates, matrix controls, and cycle certificates are independently reproduced in under one second by the zero-dependency Python~3 script `paper1_nilpotent_haar/verify_paper1.py`, archived with full outputs in `paper1_nilpotent_haar/certificates/paper1_certificates.json`. Portions of the discovery scripts and manuscript preparation were assisted by AI systems; all theorems, proofs, and executable verifier assertions were audited by the author and rest directly on the deterministic code and certificates.

*References.* Burkhart (`arXiv:2611.05060`, 2026); Carr (`arXiv:2605.22844`, 2026); Ducoffe–Dumitru (`arXiv:2609.28594`, 2026); Erdős (*Discrete Math.* 165/166, 1997); Garcia (`arXiv:2609.04686`, 2026); Liu–Montgomery (*J. Amer. Math. Soc.* 36, 2023); Tranquilli (`arXiv:2608.02675`, 2026).
