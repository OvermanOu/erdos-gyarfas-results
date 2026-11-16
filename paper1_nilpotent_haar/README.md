# Paper I: Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four

- Manuscript (LaTeX): [`paper1_nilpotent_haar.tex`](paper1_nilpotent_haar.tex)
- Manuscript (Typst / PDF): [`paper1_nilpotent_haar.typ`](paper1_nilpotent_haar.typ), [`paper1_nilpotent_haar.pdf`](paper1_nilpotent_haar.pdf)
- Standalone Python 3 Verifier: [`verify_paper1.py`](verify_paper1.py)
- Machine-readable Certificate Bundle: [`certificates/paper1_certificates.json`](certificates/paper1_certificates.json)

## Main Results Verified Here

1. **Finite Nilpotent Class $\le 3$ Haar Theorem (Theorem 1.1):** Every connected component of every simple cubic three-shift Haar graph over a finite group $\Gamma$ having a normal $2$-subgroup $N$ with $\Gamma/N$ nilpotent of class $\le 3$ contains a power-of-two simple cycle (and $C_4, C_8, C_{16},$ or $C_{32}$ whenever $\Gamma$ is odd-order nilpotent of class $\le 3$).
2. **Class-4 $p$-Groups of Arbitrary Exponent ($p \ge 5$, Theorem 1.2):** Every simple cubic Haar component over a finite $p$-group of class $\le 4$ ($p \ge 5$) and arbitrary exponent contains $C_4, C_8, C_{16}, C_{32},$ or $C_{64}$ (extending to finite $\Gamma$ with normal $2$-kernel whose quotient is class $\le 4$ nilpotent with Sylow-$3$ of class $\le 3$).
3. **Dyadic Equal-Path Theta Cover Obstruction (Theorem 1.3):** Regular $\Gamma$-covers of connected bases containing $\Theta(2^k, 2^k, 2^k)$ inherit power-of-two cycles in every component.
4. **Truncated Free Algebras & High-Girth Sharpness Controls (Proposition 1.4):** $C_{64}$ holds in $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^5$ for all primes $p \ge 2, k \ge 1$; explicit $UT_4(\mathbb{F}_p)$ ($p \ge 7$, girth $14$) and $UT_6(\mathbb{F}_p)/\langle I+E_{16}\rangle$ ($p \ge 11$, girth $\ge 18$) families show no uniform $\{C_4, C_8, C_{16}\}$ bound holds in class 3 or 4.

## Reproduction

```bash
python verify_paper1.py
```
