# Paper II: The Sharp 38-Vertex Bound for $\{C_4, C_8\}$-Free Cubic Bipartite Graphs and Dyadic Theta Cover Obstructions

- Manuscript (LaTeX): [`paper2_cubic_bipartite_c4c8.tex`](paper2_cubic_bipartite_c4c8.tex)
- Manuscript (Typst / PDF): [`paper2_cubic_bipartite_c4c8.typ`](paper2_cubic_bipartite_c4c8.typ), [`paper2_cubic_bipartite_c4c8.pdf`](paper2_cubic_bipartite_c4c8.pdf)
- Standalone Python 3 Verifier: [`verify_paper2.py`](verify_paper2.py)
- Machine-readable Certificate Bundle: [`certificates/paper2_certificates.json`](certificates/paper2_certificates.json)

## Main Results Verified Here

1. **Exact Point-Graph $C_8$ Gap Identity & Star/Triangle Decomposition (Theorem 1.1):** Exact nonnegative gap formula for $2 C_8(H)$ in terms of edge and nonedge codegrees of the $6$-regular point graph $Q$, plus decomposition of codegree-$3$ edges into $K_4$ stars and residual codegree-$2$ edges into nonblock triangles.
2. **Solver-Free Analytic Bounds (Theorem 1.2):** Every nonempty $\{C_4, C_8\}$-free simple cubic bipartite graph has at least $18$ vertices per shore ($|V| \ge 36$), and at least $19$ per shore ($|V| \ge 38$) whenever $E_1 = 0$.
3. **Sharp 38-Vertex Bound (Theorem 1.3):** Combining analytic eliminations of five $E_1 > 0$ profiles and branch $(1,6,11)$ of $(6,27,21)$ with an exhaustive census of $352{,}716$ labeled duals ($9{,}240$ admissible in $6$ orbits) and $156{,}240$ point-graph relaxations excludes $n = 18$. The cyclic Haar graph $B(19; \{0,1,8\})$ attains $38$ vertices with $C_4 = C_8 = 0$, $C_6 = 19$, and an explicit $C_{16}$.
4. **Dyadic Theta Cover Obstruction (Corollary 1.4):** Every covering graph of degree $d \le 18$ of a connected base containing $\Theta(2^k, 2^k, 2^k)$ has $C_{2^{k+1}}, C_{2^{k+2}},$ or $C_{2^{k+3}}$ in every component (solver-free for $d \le 17$).

## Reproduction

```bash
python verify_paper2.py
```
