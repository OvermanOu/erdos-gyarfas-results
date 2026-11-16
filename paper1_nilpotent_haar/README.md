# Paper I: Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four

- Manuscript (LaTeX): [`paper1_nilpotent_haar.tex`](paper1_nilpotent_haar.tex)
- Manuscript (Typst / PDF): [`paper1_nilpotent_haar.typ`](paper1_nilpotent_haar.typ), [`paper1_nilpotent_haar.pdf`](paper1_nilpotent_haar.pdf)
- Standalone Python 3 Verifier: [`verify_paper1.py`](verify_paper1.py)
- Machine-readable Certificate Bundle: [`certificates/paper1_certificates.json`](certificates/paper1_certificates.json)

## Main Results Verified Here

1. **Finite Nilpotent Class $\le 3$ Haar Theorem (Theorem 1.1):** Every connected component of every simple cubic three-shift Haar graph over a finite group $\Gamma$ having a normal $2$-subgroup $N$ with $\Gamma/N$ nilpotent of class $\le 3$ contains a power-of-two simple cycle (and $C_4, C_8, C_{16},$ or $C_{32}$ whenever $\Gamma$ is odd-order nilpotent of class $\le 3$).
2. **Unconditional Class-4 Theorem & Sharp Odd-Order $C_{32}$ Bound (Theorem 1.2):** Every simple cubic Haar component over any finite group $\Gamma$ admitting a normal $2$-subgroup $N \trianglelefteq \Gamma$ with $\Gamma/N$ nilpotent of class $\le 4$ (with **no** restriction on the Sylow-$3$ subgroup or on exponents; in particular every finite nilpotent group of class $\le 4$) contains a simple $2^k$-cycle ($k \ge 2$). Moreover, for every finite odd-order nilpotent group of class $\le 4$, every connected component contains $C_4, C_8, C_{16},$ or $C_{32}$ (via `w4` for $p \ge 5$, and two-stage elimination + Algebraic Rigidity Lemma down to the 9-group order-243 family $G_{\mathrm{crit}}(\alpha,\beta)$ at $p = 3$).
3. **Dyadic Equal-Path Theta Cover Obstruction (Theorem 1.3):** Regular $\Gamma$-covers of connected bases containing $\Theta(2^k, 2^k, 2^k)$ inherit power-of-two cycles in every component.
4. **Det-27 $C_{64}$ Certificates, Truncated Free Algebras & High-Girth Controls (Proposition 1.4):** Complementary det-27 $C_{64}$ bounds extend across truncated free algebras $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^5$ for all primes $p \ge 2, k \ge 1$; explicit $UT_4(\mathbb{F}_p)$ ($p \ge 7$, girth $14$) and $UT_6(\mathbb{F}_p)/\langle I+E_{16}\rangle$ ($p \ge 11$, girth $\ge 18$) families show no uniform $\{C_4, C_8, C_{16}\}$ bound holds in class 3 or 4, establishing sharpness of $C_{32}$.

## Reproduction

```bash
python verify_paper1.py
```
