# Paper I: Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Six

- Manuscript (LaTeX): [`paper1_nilpotent_haar.tex`](paper1_nilpotent_haar.tex)
- Manuscript (Typst / PDF): [`paper1_nilpotent_haar.typ`](paper1_nilpotent_haar.typ), [`paper1_nilpotent_haar.pdf`](paper1_nilpotent_haar.pdf)
- Standalone Python 3 Verifier: [`verify_paper1.py`](verify_paper1.py)
- Machine-readable Certificate Bundle: [`certificates/paper1_certificates.json`](certificates/paper1_certificates.json)

## Main Results Verified Here

1. **Finite Nilpotent Class $\le 3$ Haar Theorem (Theorem 1.1):** Every connected component of every simple cubic three-shift Haar graph over a finite group $\Gamma$ having a normal $2$-subgroup $N$ with $\Gamma/N$ nilpotent of class $\le 3$ contains a power-of-two simple cycle (and $C_4, C_8, C_{16},$ or $C_{32}$ whenever $\Gamma$ is odd-order nilpotent of class $\le 3$).
2. **Unconditional Class-4 Theorem & Sharp Odd-Order $C_{32}$ Bound (Theorem 1.2):** Every simple cubic Haar component over any finite group $\Gamma$ admitting a normal $2$-subgroup $N \trianglelefteq \Gamma$ with $\Gamma/N$ nilpotent of class $\le 4$ (with **no** restriction on the Sylow-$3$ subgroup or on exponents; in particular every finite nilpotent group of class $\le 4$) contains a simple $2^k$-cycle ($k \ge 2$). Moreover, for every finite odd-order nilpotent group of class $\le 4$, every connected component contains $C_4, C_8, C_{16},$ or $C_{32}$ (via `w4` for $p \ge 5$, and two-stage elimination + Algebraic Rigidity Lemma down to the 9-group order-243 family $G_{\mathrm{crit}}(\alpha,\beta)$ at $p = 3$).
3. **Nilpotency Class $\le 6$ Theorem ($p \ge 5$ Arbitrary Exponent / Sylow-$3$ Class $\le 4$, Theorem 1.3):** Every connected component of every simple cubic Haar graph $\mathcal{H}(\Gamma; S)$ where $\Gamma/N$ is nilpotent of class $\le 6$ ($N \trianglelefteq \Gamma$ normal $2$-subgroup) and $P_3(\Gamma/N)$ has class $\le 4$ (in particular, **every** finite $p$-group of class $\le 6$ for $p \ge 5$ and arbitrary exponent) contains a simple $2^k$-cycle ($k \ge 2$; $C_4\text{--}C_{64}$ when $N=1$). Verified on physical controls $UT_7(\mathbb{F}_5)$ (order $5^{21}$, class $6$, exponent $25$) and $G_{\mathrm{crit}}(0,0) \times UT_7(\mathbb{F}_5)$.
4. **Dyadic Equal-Path Theta Cover Obstruction (Theorem 1.4):** Regular $\Gamma$-covers of connected bases containing $\Theta(2^k, 2^k, 2^k)$ inherit power-of-two cycles in every component for all $\Gamma$ satisfying Theorems 1.1–1.3.
5. **Degree-6 Truncated Free Algebras, Length-32 Class-5 Barrier & High-Girth Controls (Propositions 1.5 & 1.6):** All three words $w_{64}^{(1)}, w_{64}^{(2)}, w_{64}^{(3)}$ vanish identically in $\mathbb{Z}\langle X,Y\rangle/(X,Y)^7 = \gamma_7(F_2)$ and $w_{64}^{(1)}$ yields `{1: 992}` integral deg-6 gcds (simple $C_{64}$ in $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^7$ for **all** primes $p \ge 2, k \ge 1$). Conversely, **0 / 288** cyclically nonbacktracking free-class-4 $32$-color words close at degree $5$, proving $64$ is the minimal universal free-group dyadic length for class $c \ge 5$. Explicit $UT_4(\mathbb{F}_p)$ ($p \ge 7$, girth $14$) and $UT_6(\mathbb{F}_p)/\langle I+E_{16}\rangle$ ($p \ge 11$, girth $\ge 18$) families establish sharpness of $C_{32}$ in class $\le 4$.

## Reproduction

```bash
python verify_paper1.py
```
