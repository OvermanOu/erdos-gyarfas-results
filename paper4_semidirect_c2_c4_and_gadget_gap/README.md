# Paper IV: Sharp $C_{16}$ Bounds for Semidirect $C_2$-, $C_4$-, and Klein-Bottle Cubic Haar Graphs and the Defect Point-Graph $C_8$ Identity for Bipartite Gadgets

- Manuscript (LaTeX): [`paper4_semidirect_c2_c4_and_gadget_gap.tex`](paper4_semidirect_c2_c4_and_gadget_gap.tex)
- Manuscript (Typst / PDF): [`paper4_semidirect_c2_c4_and_gadget_gap.typ`](paper4_semidirect_c2_c4_and_gadget_gap.typ), [`paper4_semidirect_c2_c4_and_gadget_gap.pdf`](paper4_semidirect_c2_c4_and_gadget_gap.pdf)
- Standalone Python 3 Verifier: [`verify_paper4.py`](verify_paper4.py)
- Machine-readable Certificate Bundle: [`certificates/paper4_certificates.json`](certificates/paper4_certificates.json)

## Main Results Verified Here

1. **Universal Klein-Bottle & Semidirect $A \rtimes_\sigma C_2$ Theorem (Theorem 1.1):** Every cubic three-shift Haar graph over any quotient of $\mathcal{K}_0 = \langle a, b \mid a b a^{-1} = b^{-1} \rangle$ (via `w_KB = 0101010210121202`) or over **any** semidirect product $A \rtimes_\sigma C_2$ ($\sigma^2 = \mathrm{id}_A$, via `w_G10 = 0102021021202012`) contains a simple $C_4, C_8,$ or $C_{16}$ in every connected component.
2. **Universal General $A \rtimes_\sigma C_4$ Theorem & $2$-Kernel Extensions (Theorem 1.2):** For **any** abelian group $A$ and **any** $\sigma \in \mathrm{Aut}(A)$ satisfying $\sigma^4 = \mathrm{id}_A$ (no further restriction), every component of $\mathcal{H}(A \rtimes_\sigma C_4; S)$ contains a simple $C_4, C_8,$ or $C_{16}$ (`w_G10` reduces every Case `(1,0)` and `(1,2)` pair to abelian commutators or the Klein-bottle relation `a b a^{-1} = b^{-1}`). Gaussian/Frobenius $C_4$-actions ($\sigma^2 = -\mathrm{id}_A$) admit direct $16$-words without conjugation (`0101010212012102`, `0101010212102012`, `0101010201010102`), and normal $2$-kernel lifting extends power-of-two cycle forcing to all $A \rtimes_\sigma C_{2^r}$ ($\sigma^4 = \mathrm{id}_A$), $\mathrm{GL}(2,3)$ (`416` generating pairs), $C_{13} \rtimes_5 C_4$ (`312` classes), $\mathbb{F}_5^4 \rtimes_{\mathrm{shift}} C_4$ (order $2,500$), and regular covers of $\Theta(2^k, 2^k, 2^k)$.
3. **Defect Point-Graph $C_8(H)$ Identity & Solver-Free Bipartite Gadget Bound (Theorem 1.3):** Generalizes Paper II's point-graph gap identity to arbitrary simple $C_4$-free bipartite two-attachment cubic gadgets $H$ ($|V(H)| = 2n$), proving a Defect Star-$K_4$ decomposition and $K_{2,2}$-free local capacities (`6, 6, 4, -2`) that eliminate every $\{C_4, C_8\}$-free bipartite gadget of order $|V(H)| \le 28$ ($n \le 14$) completely solver-free regardless of the $0\text{--}1$ attachment distance.

## Reproduction

```bash
python verify_paper4.py
```
