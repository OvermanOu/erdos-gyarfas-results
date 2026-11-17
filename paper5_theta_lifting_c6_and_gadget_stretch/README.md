# Paper V: Derived-Central Dyadic Theta Lifting to Nilpotent Class Nine, Universal Semidirect $C_6$ Cubic Haar Graphs, and Analytic Stretch Bounds for Two-Attachment Cubic Gadgets

- Manuscript (LaTeX): [`paper5_theta_lifting_c6_and_gadget_stretch.tex`](paper5_theta_lifting_c6_and_gadget_stretch.tex)
- Manuscript (Typst / PDF): [`paper5_theta_lifting_c6_and_gadget_stretch.typ`](paper5_theta_lifting_c6_and_gadget_stretch.typ), [`paper5_theta_lifting_c6_and_gadget_stretch.pdf`](paper5_theta_lifting_c6_and_gadget_stretch.pdf)
- Standalone Python 3 Verifier: [`verify_paper5.py`](verify_paper5.py)
- Machine-readable Certificate Bundle: [`certificates/paper5_certificates.json`](certificates/paper5_certificates.json)

## Main Results Verified Here

1. **Derived-Central Dyadic $\Theta$ Lifting to Nilpotent Class $\le 7$ (Unconditional, All Primes & Exponents) and Class $\le 9$ ($p \ge 5$) (Theorem 1.1 & Propositions 2.1–2.2):** Using normal abelian lower-central subgroups $A = \gamma_m(H)$ ($m \le \mathrm{cl}(H) \le 2m-1$), any embedded $\Theta(2^k, 2^k, 2^k)$ in $\mathcal{H}(H/\gamma_m(H))$ lifts unconditionally across $A$ to $C_{2^{k+1}}, \dots, C_{2^{k+4}}$. Free class-$2$ $\Theta(8,8,8)$ (`T8_plus`), five explicit free class-$3$ $\Theta(16,16,16)$ triples (`W_B0, W_B1, W_B2, W_Q81_A, W_Q81_B`, covering all $36/36$ order-$81$ class-$3$ quotients, tested on exact class-$7$ $\mathrm{UT}_8(\mathbb{F}_3) \to C_{128}$), and companion free class-$4$ $\Theta(32,32,32)$ witnesses (`T32_D, T32_E`, proving `L=16` is impossible via `0/98,304` common endpoints and tested on exact class-$9$ $\mathrm{UT}_{10}(\mathbb{F}_5) \to C_{64}, C_{512}$) settle all nilpotent cubic Haar graphs of class $\le 7$ with **zero Sylow-$3$ restriction** and class $\le 9$ with $\mathrm{cl}(H_3) \le 7$, plus abelian-by-(class $\le 2$) non-nilpotent extensions.
2. **Universal Semidirect $A \rtimes_\sigma C_6$ Cubic Haar Theorem (Theorem 1.2):** Completes all crystallographic semidirect cyclic orders $m \in \{1, 2, 3, 4, 6\}$. Under only $\sigma^6 = \mathrm{id}_A$, every component of $\mathcal{H}(A \rtimes_\sigma C_6; S)$ contains $C_4, C_8, C_{16},$ or $C_{32}$ (sharp on $(\mathbb{Z}_5 \times \mathbb{Z}_5^6) \rtimes C_6$ of order `468,750`), sharpening to $C_4, C_8,$ or $C_{16}$ for every cyclotomic $\Phi_6(\sigma) = \sigma^2 - \sigma + 1 = 0$ / Frobenius $A \rtimes C_6$ action, and extending across normal $2$-kernels to $A \rtimes_\sigma C_{3 \cdot 2^r}$.
3. **Analytic Menger–Spider Stretch Theorem for Arbitrary Order $n$ (Theorem 1.3 & Lemma 3.1):** Proves $\max S(H) \ge 8$ unconditionally for every bridgeless simple $\{C_4, C_8\}$-free two-attachment cubic gadget of arbitrary order $n$ (establishing Garcia's stretch inequality $\max S(H) \ge 2 \min S(H)$ for all $\min S(H) \in \{1, 2, 3, 4\}$) and $\max S(H) \ge 9$ for every bipartite bridgeless $\{C_4, C_8\}$-free gadget of arbitrary order $n$, alongside exact series-bridge superadditivity ($\max S \ge 9k - 1$ general, $\ge 10k - 1$ bipartite across $k$ series blocks).

## Reproduction

```bash
python verify_paper5.py
```