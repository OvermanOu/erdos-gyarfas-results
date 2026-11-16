# Paper III: Power-of-Two Cycles in Semidirect $C_3$-Extension Cubic Haar Graphs and Two-Attachment Cubic Gadget Bounds

- Manuscript (LaTeX): [`paper3_semidirect_and_gadgets.tex`](paper3_semidirect_and_gadgets.tex)
- Manuscript (Typst / PDF): [`paper3_semidirect_and_gadgets.typ`](paper3_semidirect_and_gadgets.typ), [`paper3_semidirect_and_gadgets.pdf`](paper3_semidirect_and_gadgets.pdf)
- Standalone Python 3 Verifier: [`verify_paper3.py`](verify_paper3.py)
- Machine-readable Certificate Bundle: [`certificates/paper3_certificates.json`](certificates/paper3_certificates.json)

## Main Results Verified Here

1. **General Semidirect $A \rtimes_\sigma C_3$ Theorem (Theorem 1.1):** Every connected component of every simple cubic three-shift Haar graph $\mathcal{H}(A \rtimes_\sigma C_3; S)$ ($\sigma^3 = \mathrm{id}_A$, finite or infinite abelian $A$) contains $C_4, C_8, C_{16}$, or $C_{32}$ (via `W_G10` for Case `(1,0)` and `W_G12` for Case `(1,2)`), extending via normal $2$-kernels to $\mathrm{SL}(2,3)$ (`176` pairs) and regular covers of $\Theta(2^k, 2^k, 2^k)$.
2. **Eisenstein / Frobenius $C_{16}$ Bound (Theorem 1.2):** Whenever $1 + \sigma + \sigma^2 = 0$ on $A$ (or $|S \bmod A| \le 2$), every connected component contains $C_4, C_8$, or $C_{16}$ directly via `W_E10` and `W_E12` (zero uncovered differences even without conjugation).
3. **Exact $n_{\min} = 20$ Classification, $n_{\min}^{\mathrm{cl}} = 24$, and 4,802-Vertex Witness (Theorem 1.3):** Exact closure equivalence $S(H) \cap \{1,3,7\} = \emptyset \iff H + \{0,1\}$ simple $\{C_4,C_8\}$-free cubic; Analytic Bipartite Closure Lemma for $n \le 36$ (sharp at $n=38$ via $B(19;\{0,1,8\}) - e$); soundness-verified exhaustive enumeration (unpruned vs pruned+sym $C_4$-free match at $n \in \{6,8,10,12\}$: `0, 1, 11, 75` classes, `0` $C_8$-parity discrepancies) proving $0$ $\{C_4, C_8\}$-free gadgets across $n \in \{4,\dots,18\}$ and **exact $n_{\min}(\{C_4, C_8\}\text{-free}) = 20$** with **three** canonical classes (`324` leaves, all `III_dist_ge3`, girth $3$, all containing $C_{16}$ and hitting $\{3,7\}$, stretch $19/3, 19/5, 19/6$); hence $n_{\min}(\{C_4, C_8, C_{16}\}\text{-free}) \ge 22$ (bridge bound $n \ge 44$), sharp closure-admissible order $n_{\min}^{\mathrm{cl}} = 24$ via `MARKSTROM24 - {0,1}` ($\min S = 4, \max S = 23$), and girth-$14$ $C_{16}$-free witness $\mathcal{H}(UT_4(\mathbb{F}_7); \{I, I+E_{12}+E_{23}, I+E_{23}+E_{34}\}) - e$ ($\min S = 13$, explicit $C_{32}-e$ simple path $= 31 \ge 26$).
4. **Complete Zero-Gap Haar $\Theta(8,8,8)$ & $C_{16}$ Census ($3 \le |G| \le 47$, $6 \le |V| \le 94$, Proposition 1.4):** Exhaustive check across all `151` two-generated finite groups accounting for all `196` OEIS A000001 groups across all `45` orders (`20,114` re-anchoring pairs) yields `3,518` connected $\{C_4, C_8\}$-free classes (`2,752` abelian $+$ `766` nonabelian across `13` groups; `0` below $|G|=19$) and confirms `3,518 / 3,518` contain both $C_{16}$ and $\Theta(8,8,8)$.

## Reproduction

```bash
python verify_paper3.py
```
