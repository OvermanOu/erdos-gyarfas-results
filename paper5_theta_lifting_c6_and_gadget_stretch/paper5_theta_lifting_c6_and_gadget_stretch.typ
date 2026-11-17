#set page(paper: "us-letter", margin: (x: 0.92in, y: 0.92in), numbering: "1")
#set text(font: "New Computer Modern", size: 10.2pt)
#set par(justify: true, leading: 0.63em)
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
#let proof(title: "Proof", body) = block(
  width: 100%,
  inset: (top: 2pt, bottom: 6pt),
  [
    #emph[#title.] #body #h(1fr) $square$
  ]
)

#align(center)[
  #text(size: 14pt, weight: "bold")[Derived-Central Dyadic Theta Lifting to Nilpotent Class Nine, Universal Semidirect $C_6$ Cubic Haar Graphs, and Analytic Stretch Bounds for Two-Attachment Cubic Gadgets]
  #v(0.45em)
  #text(size: 11pt)[OvermanOu (`ad110158@gmail.com`)] \
  #text(size: 9.5pt, fill: luma(80))[November 17, 2026]
]

#v(0.65em)
#block(inset: (x: 1.4em))[
  #text(size: 9.3pt)[
    *Abstract.* We establish three unconditional structural advances toward the Erdős–Gyárfás conjecture across finite cubic Haar graphs and arbitrary-order two-attachment cubic gadgets. First, we introduce *derived-central dyadic theta lifting*: whenever a $2$-generated finite group $H = chevron.l a, b chevron.r$ has an abelian normal subgroup $A lt.eq.tri H$ with noncyclic quotient $Q = H slash A$, any embedded equal-path theta subgraph $Theta(2^k, 2^k, 2^k)$ ($k >= 1$) in $cal(H)(Q; \{1_Q, overline(a), overline(b)\})$ lifts in one shot across $A$ to $C_(2^(k+1)), C_(2^(k+2)), C_(2^(k+3))$, or $C_(2^(k+4))$. Taking $A = gamma_m (H)$ for $m <= "cl"(H) <= 2m - 1$: five free class-$3$ $Theta(16, 16, 16)$ triples resolve **every finite nilpotent group of class at most $7$ across all primes $p >= 2$, all exponents, and with zero Sylow-$3$ restriction** (settling Paper I Open Problem 1 up to class $7$, tested on exact class-$7$ $U T_8(FF_3)$ yielding $C_(128)$); at class $4$ we prove an exhaustive $L = 16$ free-group barrier (`0 / 98,304` common endpoints) and construct two companion $Theta(32, 32, 32)$ witnesses unconditionally resolving **nilpotency class at most $9$ for all $p >= 5$** (and Sylow-$3$ class $<= 7$, tested on exact class-$9$ $U T_(10)(FF_5)$ yielding $C_(64)$ and $C_(512)$).

    Second, completing the crystallographic cyclic semidirect family $A times.r_sigma C_m$ ($m in \{1, 2, 3, 4, 6\}$), we prove that **every** abelian group $A$ and **every** $sigma in "Aut"(A)$ with $sigma^6 = "id"_A$ forces $C_4, C_8, C_(16)$, or $C_(32)$ in every component of $cal(H)(A times.r_sigma C_6; S)$ (sharp on $(ZZ_5 times ZZ_5^6) times.r C_6$ of order `468,750`), sharpening to $C_4, C_8,$ or $C_(16)$ under $sigma^2 - sigma + 1 = 0$ (including every Frobenius $A times.r C_6$), and extending via normal $2$-kernels to all $A times.r_sigma C_(3 dot 2^r)$.

    Third, for two-attachment simple $\{C_4, C_8\}"-free"$ cubic gadgets $H$ of **arbitrary finite order $n$**, we prove via $2$-connectivity, minimum-order bounds, and an exhaustive `302,090`-configuration Menger–spider elimination that every bridgeless gadget satisfies $max S(H) >= 8$ (general) and $max S(H) >= 9$ (bipartite)—unconditionally proving Garcia's stretch inequality $max S(H) >= 2 min S(H)$ for all $min S(H) in \{1, 2, 3, 4\}$, together with exact $0$–$1$ bridge series superadditivity ($max S >= 9k - 1$ general, $>= 10k - 1$ bipartite across $k$ series blocks).
  ]
]
#v(0.5em)

= Introduction

Companion Papers I, III, and IV resolved cubic three-shift Haar graphs $cal(H)(Gamma; S)$ over normal-$2$-kernel extensions of nilpotent groups of class $<= 4$ (and class $<= 6$ when Sylow-$3$ has class $<= 4$), semidirect $C_2, C_3, C_4$ extensions, and Klein-bottle quotients, while proving exact small-gadget thresholds $n_"min" (\{C_4, C_8\}"-free") = 20$ (general) and $|V(H)| >= 30$ (bipartite). Three natural barriers remained open: (1) lifting nilpotent coverage past Paper I's Sylow-$3$ class-$4$ ceiling and past class $6$ without searching exponentially larger degree-$7+$ Magnus algebras; (2) resolving the final crystallographic semidirect order $m = 6$; and (3) proving asymptotic ($n -> infinity$) lower bounds on the longest $0$–$1$ simple path $max S(H)$ inside $\{C_4, C_8\}"-free"$ two-attachment cubic gadgets, as needed in Garcia's stretch framework (`arXiv:2609.04686`).

== Main Results

#theorem(title: [1.1 — Abelian normal theta lifting and nilpotent class $<= 7$ / class $<= 9$])[
  (a) *Abelian Normal Lifting Lemma:* Let $H = chevron.l a, b chevron.r$ be any finite group admitting an abelian normal subgroup $A lt.eq.tri H$ whose quotient $Q = H slash A$ is noncyclic. If $cal(H)(Q; \{1_Q, overline(a), overline(b)\})$ contains an embedded equal-path theta subgraph $Theta(2^k, 2^k, 2^k)$ ($k >= 1$), then $cal(H)(H; \{1, a, b\})$ contains a simple cycle of length $2^(k+1), 2^(k+2), 2^(k+3)$, or $2^(k+4)$. \
  (b) *Unconditional Class $<= 7$ (All Primes, All Exponents, No Sylow-$3$ Restriction):* Let $Gamma$ be any finite group with a normal $2$-subgroup $N lt.eq.tri Gamma$ such that $Gamma slash N$ is nilpotent of nilpotency class at most $7$. Then every connected component of $cal(H)(Gamma; S)$ contains a power-of-two cycle (explicitly in $\{C_4, C_8, C_(16), C_(32), C_(64), C_(128), C_(256)\}$ for odd-order nilpotent groups), and every connected component of every regular $Gamma$-cover of a finite graph containing $Theta(2^r, 2^r, 2^r)$ contains a power-of-two cycle. \
  (c) *Unconditional Class $<= 9$ ($p >= 5$ / Sylow-$3$ Class $<= 7$):* Let $Gamma$ be any finite group with normal $2$-subgroup $N lt.eq.tri Gamma$ such that $Gamma slash N$ is nilpotent of class at most $9$ whose Sylow-$3$ subgroup has class at most $7$ (in particular, **every** finite $p$-group of class at most $9$ with $p >= 5$ and arbitrary exponent). Then every component of $cal(H)(Gamma; S)$ (and regular covers of $Theta(2^r, 2^r, 2^r)$) contains a power-of-two cycle (in $\{C_4, dots.c, C_(512)\}$ for odd order).
]

#theorem(title: [1.2 — Universal semidirect $A times.r_sigma C_6$ and cyclotomic $Phi_6$ refinement])[
  Let $A$ be any abelian group (finite or infinite) and let $sigma in "Aut"(A)$ satisfy *only* $sigma^6 = "id"_A$. \
  (a) *General $A times.r_sigma C_6$ (Sharp $C_(32)$):* Every connected component of every simple cubic three-shift Haar graph $cal(H)(A times.r_sigma C_6; S)$ contains a simple cycle of length $4, 8, 16$, or $32$, and $C_(32)$ is sharp on finite quotients such as $(ZZ_5 times ZZ_5^6) times.r C_6$ (order `468,750`). \
  (b) *Cyclotomic $Phi_6 (sigma) = sigma^2 - sigma + 1 = 0$ / Frobenius $A times.r C_6$ (Sharp $C_(16)$):* Whenever $sigma^2 - sigma + 1 = 0$ (satisfied by every Frobenius group $A times.r_sigma C_6$ with abelian kernel $A$), every component contains a simple $C_4, C_8,$ or $C_(16)$ (sharp on $C_(13) times.r_4 C_6$, `1,872` generating pairs). \
  (c) *Normal $2$-kernel extensions:* Power-of-two cycle forcing extends to every finite $G$ with normal $2$-subgroup $N lt.eq.tri G$ and $G slash N$ embedding into $A times.r_sigma C_6$—in particular, every finite $A times.r_sigma C_(3 dot 2^r)$ ($sigma^6 = "id"_A$) via central $6 C_(3 dot 2^r)$—and to all regular $G$-covers of graphs containing $Theta(2^k, 2^k, 2^k)$.
]

#theorem(title: [1.3 — Analytic stretch bounds for arbitrary-order two-attachment cubic gadgets])[
  Let $H$ be any bridgeless simple $\{C_4, C_8\}"-free"$ two-attachment cubic gadget of *arbitrary finite order $n$* ($deg_H (0) = deg_H (1) = 2$ and $deg_H (v) = 3$ for $v in.not \{0, 1\}$), with $0$–$1$ simple path length spectrum $S(H)$. \
  (a) *General bound & Garcia stretch:* Unconditionally for all $n$, $max S(H) >= 8$. Consequently, Garcia's stretch inequality $max S(H) >= 2 min S(H)$ holds unconditionally for every bridgeless $\{C_4, C_8\}"-free"$ two-attachment cubic gadget with $min S(H) in \{1, 2, 3, 4\}$. \
  (b) *Bipartite bound:* If $H$ is bipartite, then $max S(H) >= 9$ unconditionally for all $n$. \
  (c) *Series composition:* Across $k >= 1$ bridgeless $\{C_4, C_8\}"-free"$ blocks connected in series by $0$–$1$ separating bridges, $max S(H) >= 9k - 1$ (general) and $max S(H) >= 10k - 1$ (bipartite).
]

= Proof of Theorem 1.1 (Derived-Central Dyadic Theta Lifting)

#proof(title: "Proof of Theorem 1.1(a)")[
  Because $Q = H slash A$ is noncyclic, $\{1_Q, overline(a), overline(b)\}$ cannot fail to be pairwise distinct—otherwise $Q = chevron.l overline(a), overline(b) chevron.r$ would be generated by at most one nonidentity element, hence cyclic. Under $(g, epsilon) |-> (g A, epsilon)$, free left multiplication by $A$ acts regularly on every vertex and edge fiber of $cal(H)(H; \{1, a, b\})$ over $cal(H)(Q; \{1_Q, overline(a), overline(b)\})$ (normality $A lt.eq.tri H$ suffices; centrality of $A$ is not required). Applying Paper I Lemma 2.4 directly to $Theta(2^k, 2^k, 2^k)$ yields a Haar core over a subgroup of the abelian group $A$; by Paper I Theorem 2.1, every component contains $C_4, C_8,$ or $C_(16)$ in $cal(H)(A; S')$, which lifts to a simple cycle of length $2^(k+1), 2^(k+2), 2^(k+3),$ or $2^(k+4)$ in $cal(H)(H; \{1, a, b\})$.
]

When $H = chevron.l a, b chevron.r$ is odd-order finite nilpotent of class $c$ with $m <= c <= 2m - 1$ ($m >= 3$), $A = gamma_m (H) lt.eq.tri H$ satisfies $[A, A] <= gamma_(2m) (H) = 1$ ($A$ abelian!), while $Q = H slash gamma_m (H)$ has nilpotency class *strictly equal to $m - 1 >= 2$* (if $gamma_(m-1) (H) <= gamma_m (H)$ then nilpotency forces $gamma_(m-1) (H) = 1$, contradicting $c >= m$).

#proposition(title: [2.1 — Free class-2 $Theta(8,8,8)$ and non-nilpotent abelian-by-(class 2) covers])[
  In ordered Hall coordinates $a^x b^y c^z$ of $F_2 slash gamma_3 (F_2)$ ($c = [a, b]$), the $3$-fold color-symmetric triple $T_(8,+) = (#raw("01021020"), #raw("12102101"), #raw("20210212"))$ ends at $(0, 0, 1) = c$, visits $11 + 12 = 23$ distinct vertices (`121` same-shore differences), satisfies $max (|Delta x|, |Delta y|, |Delta z|) = (3, 3, 4)$ with $(0, 0, Delta z)$ strictly at $|Delta z| = 1$, and embeds $Theta(8, 8, 8)$ in every class-$2$ $p$-group for $p >= 5$ as well as in `216 / 216` generating pairs of $U T_3(FF_3)$ and `27 / 216` of $M_(27)$ (where exhaustive MITM confirms `216 / 216` pairs contain $Theta(8, 8, 8)$). Consequently, any finite group $H = chevron.l a, b chevron.r$ with abelian $A lt.eq.tri H$ and odd class-$2$ quotient $Q = H slash A$ having a nonabelian Sylow-$p$ ($p >= 5$), $Q tilde.equiv U T_3(FF_3) times C_m$ ($gcd(m,6)=1$), or $Q tilde.equiv M_(27)$ contains $C_(16), C_(32), C_(64)$, or $C_(128)$.
]

For $m = 4$ ($F_2 slash gamma_4 (F_2)$, ordered Hall basis $a^x b^y c^z d^u e^v$ with $c = [a,b]$, $d = [c,a]$, $e = [c,b]$), we use five explicit free class-$3$ $Theta(16, 16, 16)$ witnesses (each visiting `23 + 24 = 47` distinct vertices, giving `529` unordered same-shore differences), certified in Table 1.

#figure(
  table(
    columns: 4,
    stroke: 0.5pt + luma(160),
    inset: 4.2pt,
    fill: (x, y) => if y == 0 { luma(240) },
    align: (left, left, left, left),
    table.header([Witness], [Three Length-$16$ Branches], [Hall End $(x,y,z,u,v)$], [Role in Theorem 1.1(b)]),
    [`W_B0`], [#raw("0201021021012021") \ #raw("1201212101012012") \ #raw("2012012102010120")], [`(-3,1,0,1,0)`], [All $p>=5$; $p=3$ non-$3$-torsion or $k_0 = 0$],
    [`W_B1`], [#raw("0212010210210121") \ #raw("1201012102012012") \ #raw("2012010102020120")], [`(-2,-1,-3,5,3)`], [$p=3$, $exp((Q_3)_("ab")) >= 9$, $k_0 = 1$],
    [`W_B2`], [#raw("0201010210212010") \ #raw("1012021021010121") \ #raw("2012012102012012")], [`(-1,0,-1,1,1)`], [$p=3$, $exp((Q_3)_("ab")) >= 9$, $k_0 = 2$],
    [`W_Q81_A`], [#raw("0121010120120210") \ #raw("1202102101212102") \ #raw("2021201201020201")], [`(-2,0,1,-2,0)`], [$27 slash 36$ order-$81$ class-$3$ quotients],
    [`W_Q81_B`], [#raw("0212012010212102") \ #raw("1021010210120121") \ #raw("2102102102120120")], [`(-1,0,1,-1,-2)`], [Remaining $9 slash 36$ order-$81$ quotients],
  ),
  caption: [Five free class-$3$ $Theta(16, 16, 16)$ witnesses embedding in every odd-order class-$3$ group ($p=3$ and $p>=5$).],
)

#proof(title: "Proof of Theorem 1.1(b) — Unconditional Class ≤ 7")[
  Normalize shifts to $\{1, a, b\}$ inside $K = chevron.l a, b chevron.r <= Gamma$ and pass to $H = K slash (K inter N)$ via Paper I Lemma 2.3. If shifts collide in $H$, a power-of-two cycle lifts immediately. If $"cl"(H) <= 4$, Paper I Theorem 1.2 gives $C_4, C_8, C_(16)$, or $C_(32)$ in $H$. Otherwise $"cl"(H) in \{5, 6, 7\}$, so $A = gamma_4 (H) lt.eq.tri H$ is abelian and $Q = H slash gamma_4 (H) = product_(p >= 3) Q_p$ has nilpotency class *exact $3$*. Because each triple in Table 1 meets at a single group element in $F_2 slash gamma_4 (F_2)$, its three branches meet at one vertex across all prime factors of $Q$ simultaneously, so internal disjointness in any single $Q_(p^*)$ embeds $Theta(16, 16, 16)$ in $Q$:
  + *Case $p^* >= 5$ nonabelian:* On `W_B0`, all $514$ nonzero-$(x, y)$ differences have $gcd(|x|, |y|) in \{1, 2, 3, 4\}$ (nonzero in $Q_(p^*) slash Phi(Q_(p^*)) tilde.equiv FF_(p^*)^2$), and all $15$ zero-$(x, y)$ differences have $Delta z in \{-1, 1\}$ (nonzero modulo $gamma_3 (Q_(p^*))$ as $"ord"(overline(c)) >= p^* >= 5$).
  + *Case $"cl"(Q_3) = 3$, $exp((Q_3)_("ab")) >= 9$:* At most one of $alpha, beta, beta - alpha in (Q_3)_("ab")$ can be $3$-torsion. If none is $3$-torsion, `W_B0` has zero collisions in $Q_3$ because all nonzero $3 divides (x, y)$ pairs lie strictly in $\{(-3, 0), (3, 0), (-3, 3)\}$ and zero-$(x, y)$ pairs satisfy $z in \{-1, 1\}$. If one is $3$-torsion, swapping $a <-> b$ (if $3 alpha = 0$) or re-anchoring $\{1, a, b\}$ at $a$ to $\{1, a^(-1), a^(-1) b\}$ (if $3(beta - alpha) = 0$) normalizes to $3 beta = 0$ with $3 alpha != 0$ and $3(beta - alpha) != 0$. Then $1 equiv [a, b^3] equiv c^3 mod gamma_3 (Q_3)$ while $c in.not gamma_3 (Q_3)$ (`cl = 3`), forcing $gamma_2 (Q_3) slash gamma_3 (Q_3) = chevron.l overline(c) chevron.r tilde.equiv C_3$ and $b^3 equiv c^(k_0) mod gamma_3 (Q_3)$ for a unique $k_0 in \{0, 1, 2\}$. Exact verification across all $529$ pairs shows zero collisions in `W_B0` ($k_0 = 0$), `W_B1` ($k_0 = 1$), and `W_B2` ($k_0 = 2$): every nonzero $3 divides (x, y)$ pair with $x != 0$ lies in $\{(plus.minus 3, 0), (-3, 3), (3, -3)\}$ (nonzero in $(Q_3)_("ab")$), while every $(0, plus.minus 3)$ pair satisfies $(y slash 3) k_0 + z != 0 mod 3$.
  + *Case $"cl"(Q_3) = 3$, $(Q_3)_("ab") tilde.equiv C_3 times C_3$:* By Paper I Lemma 3.3, $a^3, b^3 in gamma_3 (Q_3)$ and $c^3 = 1$, while $gamma_3 (Q_3) != 1$ admits a surjective homomorphism $phi : gamma_3 (Q_3) -> FF_3$ with projectivized coordinates $(p_d, p_e) = (phi(d), phi(e)) in \{(1, 0), (0, 1), (1, 1), (1, 2)\}$ and $(alpha, beta) = (phi(a^3), phi(b^3)) in FF_3^2$. Testing all $4 times 9 = 36$ resulting order-$81$ class-$3$ quotients shows `W_Q81_A` resolves `27 / 36` and `W_Q81_B` resolves all remaining `9 / 36` (`0` uncovered).
  Theorem 1.1(a) lifts $Theta(16, 16, 16)$ across $A = gamma_4 (H)$ to $\{C_(32), C_(64), C_(128), C_(256)\}$ in $H$, and Lemma 2.3 lifts to $Gamma$. A physical control in $U T_8 (FF_3)$ (order $3^(28)$, exact $chevron.l a, b chevron.r$ class $7$ for $a = I + sum_(i=1)^7 E_(i,i+1)$, $b = I + E_(78)$) lifts both `W_B0` and `W_Q81_A` via `01012102` to explicit simple $C_(128)$ cycles.
]

#proposition(title: [2.2 — Free class-4 length-16 barrier and companion $Theta(32,32,32)$ witnesses])[
  In $F_2 slash gamma_5 (F_2)$, exhaustive search of all $3 times 2^(15) = 98,304$ simple $16$-step paths finds `94,902` distinct endpoints and *`0` common endpoints* across the three start colors, so $L = 32$ is minimal. At $L = 32$ (`47 + 48 = 95` vertices, `2,209` unordered same-shore differences), both
  $ T_(32, D) &= (#raw("01201210102102012012102101010210"),\ #raw("10102012012102102102101021020101"),\ #raw("20121021010102101010210201012012")), \
    T_(32, E) &= (#raw("01020102102120101202010120101021"),\ #raw("10201021201201010212020101012010"),\ #raw("21021201210212012010201201212012")) $
  satisfy: $max gcd(|x|, |y|) = 4$, $1 <= |z| <= 4$ on $x = y = 0, z != 0$, **`0` grade-$4$ central $(r, s, t)$ pairs**, and strictly orthogonal grade-$3$ $(u, v)$ directions `(1, 0)` (`53` pairs, $1 <= |u| <= 4$) for $T_(32,D)$ and `(0, 1)` (`32` pairs, $1 <= |v| <= 3$) for $T_(32,E)$.
]

#proof(title: "Proof of Theorem 1.1(c) — Class ≤ 9 (p ≥ 5)")[
  For $"cl"(H) in \{8, 9\}$ with $"cl"(H_3) <= 7$, take $A = gamma_5 (H)$ (abelian) so $Q = H slash gamma_5 (H) = product_(p >= 3) Q_p$ has class $4$. If all $Q_p$ ($p >= 5$) had class $<= 3$, then $gamma_4 (H_p) <= gamma_5 (H_p)$ would force $gamma_4 (H_p) = 1$, contradicting $"cl"(H) >= 8$ since $"cl"(H_3) <= 7$. Thus some $p^* >= 5$ satisfies $"cl"(Q_(p^*)) = 4$. Since $d, e$ cannot both lie in $gamma_4 (Q_(p^*))$ (else $f = g = h = 1$ and $gamma_4 (Q_(p^*)) = 1$), at least one of $T_(32,D)$ or $T_(32,E)$ embeds $Theta(32, 32, 32)$ in $Q_(p^*)$, hence in $Q$, lifting across $A = gamma_5 (H)$ to $\{C_(64), C_(128), C_(256), C_(512)\}$. Physical control in $U T_(10) (FF_5)$ (order $5^(45)$, exact $chevron.l a, b chevron.r$ class $9$): $T_(32,D)$ lifts via `01` to $C_(64)$ and $T_(32,E)$ lifts via `0101012010201212` to $C_(512)$.
]

= Proof of Theorem 1.2 (Universal Semidirect $A times.r_sigma C_6$)

#proof(title: "Proof of Theorem 1.2")[
  Normalize shifts in $A times.r_sigma C_6$ to $\{1, a, b\}$ and project mod $A$ to coset pairs $(t_a, t_b) in C_6 times C_6$. Under swap $a <-> b$, $sigma <-> sigma^(-1)$, and re-anchoring, all `35` non-identity pairs partition into `6` orbits: `(0, 3)` (order `2`, inside $A times.r_(sigma^3) C_2$, settled to sharp $C_(16)$ by Paper IV Theorem 1.1(b)); `(0, 2)` and `(2, 4)` (order `3`, inside $A times.r_(sigma^2) C_3$, settled to $C_(32)$—and $C_(16)$ under $sigma^2 - sigma + 1 = 0 => 1 + sigma^2 + sigma^4 = 0$—by Paper III Theorem 1.1); and three order-$6$ orbits `(1, 0)`, `(1, 3)`, and `(1, 2)`.

  In any quotient $ZZ[C_6]^2 times.r C_6 -> A times.r_sigma C_6$, a difference $d = (v, t)$ can vanish only when $t equiv 0 mod 6$, and conjugation by $C_6$ shifts the $6$-blocks of $v$. Evaluating $w_(G,10) = #raw("0102021021202012")$ (`16` steps) on `(1, 0)` and `(1, 3)`, and
  $ w_(C_6, 12) = #raw("01201210210102010212102010102101") quad ("32 steps") $
  on `(1, 2)`, gives `0` uncovered $t = 0$ differences in every orbit (Table 2). Whenever $[a, b] = 1$, Paper I Theorem 2.1 yields $C_4, C_8,$ or $C_(16)$; whenever $a b a^(-1) b = 1$, Paper IV Theorem 1.1(a) yields $C_4, C_8,$ or $C_(16)$. Exhaustive MITM confirms `{4: 0, 8: 0, 16: 0}` closed walks on `(1, 2)` in $ZZ[C_6]^2 times.r C_6$ and in $(ZZ_5 times ZZ_5^3) times.r C_6$ (`3,750`) and $(ZZ_5 times ZZ_5^6) times.r C_6$ (`468,750`), proving $C_(32)$ is sharp.

  For (b), when $sigma^2 - sigma + 1 = 0$, $sigma^3 = -"id"_A$ forces $b^2 = 1$ (`0202`, $C_4$) in `(1, 3)`, while $w_(Phi_6, 10) = #raw("0101010102012102")$ closes `(1, 0)` (`4` direct collapses, `52` nonzero $C_6$-cosets) and $w_(Phi_6, 12) = #raw("0101010101201202")$ closes `(1, 2)` (`1` len-$4$, `4` len-$8$, `51` nonzero cosets), proving sharp $C_(16)$. Part (c) follows from central $6 C_(3 dot 2^r) lt.eq.tri A times.r_sigma C_(3 dot 2^r)$ and Paper I Lemmas 2.3–2.4.
]

#figure(
  table(
    columns: 4,
    stroke: 0.5pt + luma(160),
    inset: 4.5pt,
    fill: (x, y) => if y == 0 { luma(240) },
    align: (left, left, center, left),
    table.header([Family / Finite Control], [Scope / Word], [Uncovered], [Verified Partition / Cycle Histogram]),
    [$ZZ[C_6]^2 times.r C_6$ (`1,0`)], [$w_(G,10)$ (`16`)], [`0 / 56`], [`28` $t != 0$, `13` collapse, `5` len-$4$, `4` len-$8$, `3` $[a,b]$, `3` $a b a^(-1) b$],
    [$ZZ[C_6]^2 times.r C_6$ (`1,3`)], [$w_(G,10)$ (`16`)], [`0 / 56`], [`45` $t != 0$, `5` len-$4$, `3` $[a,b]$, `3` $a b a^(-1) b$],
    [$ZZ[C_6]^2 times.r C_6$ (`1,2`)], [$w_(C_6,12)$ (`32`)], [`0 / 240`], [`204` $t != 0$, `16` len-$4$, `13` len-$8$, `7` $[a,b]$],
    [$(ZZ_5 times ZZ_5^6) times.r C_6$ (`468,750`)], [Orbit `(1,2)` sharpness], [`0`], [`{4: 0, 8: 0, 16: 0}`, $w_(C_6,12)$ traces simple $C_(32)$],
    [$ZZ[zeta_6]^2 times.r C_6$ (`1,0`, `1,2`, `1,3`)], [$w_(Phi_6, 10)$, $w_(Phi_6, 12)$, `0202`], [`0`], [`(52, 4)`, `(51, 1, 4)`, $b^2 = 1$],
    [$"AGL"(1,7) = C_7 times.r_3 C_6$ (`42`)], [`820` all / `504` gen], [`0`], [All: `4:394, 8:384, 16:42`; Gen: `4:252, 8:252`],
    [$C_(13) times.r_4 C_6$ (`78`)], [`2,926` all / `1,872` gen], [`0`], [All: `4:1318, 8:516, 16:1092`; Gen: `4:936, 8:468, 16:468`],
    [$(C_3 times C_7) times.r_(2,2) C_6$ (`126`)], [`124` orbit reps], [`0`], [`4:8, 8:44, 16:72`],
  ),
  caption: [Exact $ZZ[C_6]^2 times.r C_6$ partitions and finite $C_6$ controls certified by `verify_paper5.py`.],
)

= Proof of Theorem 1.3 (Analytic Menger–Spider Stretch Bounds)

#lemma(title: "3.1 — Subcubic 2-connectivity and bridge series superadditivity")[
  Let $H$ be a connected subcubic two-attachment cubic gadget with $deg_H (0) = deg_H (1) = 2$ and $deg_H (v) = 3$ for $v in.not \{0, 1\}$. Then: (a) $H$ is $2$-connected iff it is bridgeless (since any cut-vertex $w$ has $deg_H (w) <= 3$, forcing a degree-$1$ neighbor component via a bridge); and (b) splitting at any $0$–$1$ separating bridge $e = u_0 v_0$ yields strictly smaller $\{C_4, C_8\}"-free"$ gadgets $H_0, H_1$ satisfying $min S(H) = min S(H_0) + min S(H_1) + 1$ and $max S(H) = max S(H_0) + max S(H_1) + 1$.
]

#proof(title: "Proof of Theorem 1.3")[
  We prove by strong induction on $|V(H)|$ that every bridgeless simple $\{C_4, C_8\}"-free"$ two-attachment cubic gadget satisfies $max S(H) >= 8$ in general and $max S(H) >= 9$ when bipartite. Suppose for contradiction that a minimal bridgeless counterexample $H$ satisfies $M = max S(H) <= 7$ (with $M in \{1, 3, 5, 7\}$ if bipartite, since Paper III Theorem 1.3(a) places $0$ and $1$ in opposite bipartition shores).

  By Lemma 3.1(a), $H$ is $2$-connected, so Menger's theorem provides simple cycles through $\{0, 1\}$. Choose a simple $0$–$1$ cycle $C = Q_1 union Q_2$ ($1 <= |Q_1| <= |Q_2| <= M <= 7$) maximizing $|C| = |Q_1| + |Q_2|$. Then $|V(C)| <= 14 < 20 <= |V(H)|$ in general (Paper III Theorem 1.4) and $|V(C)| <= 14 < 30 <= |V(H)|$ in the bipartite case (Paper IV Theorem 1.3(b)), so $V(H) without V(C) != emptyset$. Pick any connected component $U$ of $H - V(C)$, with boundary edge set $partial U$ between $U$ and $V(C)$.

  Because $H$ is bridgeless, $|partial U| >= 2$. Since $deg_H (0) = deg_H (1) = 2$ are saturated on $C$ and $deg_H (w) = 3$ for $w in V(C) without \{0, 1\}$, $partial U$ meets $|partial U|$ pairwise distinct internal vertices of $C without \{0, 1\}$.
  + *Case $|partial U| = 2$:* Let $partial U = \{x u_x, y u_y\}$ with $x != y in V(C) without \{0, 1\}$. We cannot have $u_x = u_y = u_0$: since $deg_H (u_0) = 3$, $|V(U)| >= 2$ and the third edge at $u_0$ would be a bridge of $H$. Thus $u_x != u_y$, making $U$ a strictly smaller connected $\{C_4, C_8\}"-free"$ two-attachment cubic gadget. Any bridge of $U$ must separate $u_x$ from $u_y$ (else it is a bridge of $H$), and internal vertices of $U$ have degree $3$, so $U$ contains at least one bridgeless block $B$ with $|V(B)| <= |V(U)| < |V(H)|$. By strong induction and Lemma 3.1(b), $max S(U) >= max S(B) >= 8$ ($>= 9$ if bipartite), yielding an $x$–$y$ path $R$ internally disjoint from $C$ of length $r = 2 + max S(U) >= 10$. If $x, y$ lie on the same arc $Q_i$ at distance $delta <= |Q_i| - 2 <= 5$, rerouting via $R$ produces a simple $0$–$1$ path of length $|Q_i| - delta + r >= 2 + 10 = 12 > 7$; if $x in Q_1$ and $y in Q_2$, the two cross $0$–$1$ paths through $R$ sum to $|C| + 2r >= 23$, forcing one of length $>= 12 > 7$, contradiction.
  + *Case $|partial U| >= 3$ (Spider Elimination):* Choose three distinct attachments $w_1, w_2, w_3 in V(C) without \{0, 1\}$ and a minimal spanning tree $T$ of $\{w_1, w_2, w_3\}$ inside $U union \{w_i u_i\}$. Since each $w_i$ is a leaf of $T$, $T$ is uniquely a spider with hub $z in V(U)$ and three internally disjoint legs of lengths $ell_1, ell_2, ell_3 >= 1$ ($s_(i j) = ell_i + ell_j >= 2$). For every pair $(i, j)$: the two cycles $d_C + s_(i j)$ and $|C| - d_C + s_(i j)$ avoid $\{4, 8\}$; same-arc replacements respect maximality of $|C|$ ($s_(i j) <= |w_j - w_i|$); and opposite-arc pairs induce two $0$–$1$ paths summing to $|C| + 2 s_(i j)$, both $<= M <= 7$ (forcing $s_(i j) <= M - 2$ and $ell_k < M$). Exhaustive verification over all `302,090` configurations (`40, 540, 8000, 53750, 239760` across $M = 3..7$) leaves *`0` valid configurations*.

  Hence $max S(H) >= 8$ unconditionally (general) and $max S(H) >= 9$ (bipartite). Whenever $min S(H) in \{1, 2, 3, 4\}$, $max S(H) >= 8 >= 2 min S(H)$; part (c) follows directly from Lemma 3.1(b). Control checks verify `Markstrom24 - (0,1)` ($24$ vertices, bridgeless, $\{C_4, C_8\}"-free"$) has $min S = 4$, $max S = 23$, and `Fano_minus_e` ($14$ vertices, $min S = 5$, $max S = 13$) in series (`28` vertices) gives $min S = 11$, $max S = 27$.
]

*Reproducibility and AI Disclosure.* All Hall calculus rules, class-$2$, $3$, and $4$ $Theta$ certificates, $L=16$ barrier exhaustion, matrix controls ($U T_8(FF_3)$ and $U T_(10)(FF_5)$), semidirect $C_6$ orbit and prefix-difference partitions, finite $C_6$ controls, Menger–spider elimination, and gadget series controls are reproduced in `~1.6` seconds by `paper5_theta_lifting_c6_and_gadget_stretch/verify_paper5.py` against `certificates/paper5_certificates.json`. Portions of the discovery scripts and manuscript preparation were assisted by AI systems; all theorems, proofs, and executable assertions were audited by the author and rest directly on the deterministic stdlib verifier.

*References.* Burkhart (`arXiv:2611.05060`, 2026); Carr (`arXiv:2605.22844`, 2026); Garcia (`arXiv:2609.04686`, 2026); Markström (*Congr. Numer.* 171 (2004), 179–192); OvermanOu, companion Papers I–IV (2026).
