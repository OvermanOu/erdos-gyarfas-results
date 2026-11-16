# Erdős–Gyárfás Conjecture: Manuscripts and Reproducible Verification Artifacts

[![Verify All](https://img.shields.io/badge/python-3.10%2B%20stdlib%20only-blue)](verify_all.py)
[![License](https://img.shields.io/badge/license-MIT%20%2F%20CC--BY--4.0-green)](LICENSE)

This repository archives three standalone mathematical papers and their zero-dependency Python verification suites establishing structural power-of-two cycle results toward the **Erdős–Gyárfás conjecture** (every finite simple graph with $\delta(G) \ge 3$ contains a simple cycle of length $2^k$ for some $k \ge 2$).

> **繁體中文簡介**：本公開倉庫彙整作者（OvermanOu）針對 **Erdős–Gyárfás 猜想** 的三項已驗證數學研究成果，各自附有完整 AMS-LaTeX / Typst 論文手稿、編譯 PDF、無外部依賴的 Python 標準庫驗證腳本與確定性 JSON 憑證檔案；執行 `python verify_all.py` 約 30 秒即可全數重現驗證並核對憑證一致性。

---

## Papers and Main Theorems

### Paper I — *Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four* (`v2.0.0` Unconditional Update)
- **Files**: [`paper1_nilpotent_haar/`](paper1_nilpotent_haar/README.md) · [LaTeX](paper1_nilpotent_haar/paper1_nilpotent_haar.tex) · [Typst](paper1_nilpotent_haar/paper1_nilpotent_haar.typ) · [PDF](paper1_nilpotent_haar/paper1_nilpotent_haar.pdf) · [Verifier](paper1_nilpotent_haar/verify_paper1.py) · [Certificates](paper1_nilpotent_haar/certificates/paper1_certificates.json)
- **Highlights**:
  - **2-kernel & nilpotency class $\le 3$**: Every connected component of every simple cubic $3$-shift Haar graph $\mathcal{H}(\Gamma; S)$ where $\Gamma/N$ is nilpotent of class $\le 3$ for a normal $2$-subgroup $N \trianglelefteq \Gamma$ contains a simple $2^k$-cycle (specifically $C_4, C_8, C_{16}$, or $C_{32}$ when $\Gamma$ is nilpotent of class $\le 3$ and odd order).
  - **Unconditional nilpotency class $\le 4$ & sharp odd-order $C_{32}$ bound**: Completely closes the $p=3$ class-$4$ branch and arbitrary exponents for all primes. Every component of $\mathcal{H}(\Gamma; S)$ over any finite group admitting $N \trianglelefteq \Gamma$ with $\Gamma/N$ nilpotent of class $\le 4$ (with **no** restriction on the Sylow $3$-subgroup or on exponents) contains a simple $2^k$-cycle ($k \ge 2$). Moreover, all finite odd-order nilpotent class-$\le 4$ cubic Haar graphs contain $C_4, C_8, C_{16}$, or $C_{32}$ (`W4` for $p \ge 5$, two-stage elimination + Algebraic Rigidity Lemma down to the $9$-group order-$243$ family $G_{\mathrm{crit}}(\alpha,\beta)$ for $p = 3$).
  - **Dyadic theta cover obstruction**: Any regular $\Gamma$-cover of a connected graph containing $\Theta(2^k, 2^k, 2^k)$ inherits a simple $2^s$-cycle in every component.
  - **Tight boundaries**: Complementary det-$27$ $C_{64}$ certificates in $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^5$ for all primes $p \ge 2, k \ge 1$, alongside girth-$14$ ($UT_4(\mathbb{F}_p)$, $p \ge 7$) and girth-$\ge 18$ ($UT_6(\mathbb{F}_p)/\langle I+E_{16}\rangle$, $p \ge 11$) families avoiding $\{C_4, C_8, C_{16}\}$ (proving $C_{32}$ is sharp).

### Paper II — *The Sharp 38-Vertex Bound for $\{C_4, C_8\}$-Free Cubic Bipartite Graphs and Dyadic Theta Cover Obstructions*
- **Files**: [`paper2_cubic_bipartite_c4c8/`](paper2_cubic_bipartite_c4c8/README.md) · [LaTeX](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.tex) · [Typst](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.typ) · [PDF](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.pdf) · [Verifier](paper2_cubic_bipartite_c4c8/verify_paper2.py) · [Certificates](paper2_cubic_bipartite_c4c8/certificates/paper2_certificates.json)
- **Highlights**:
  - **Point-graph $C_8$ gap identity & star decomposition**: Exact algebraic identity relating $2C_8(H)$ to edge/nonedge codegrees of the $6$-regular point graph $Q$, forcing edge-disjoint star-$K_4$ blocks and residual codegree-$2$ triangle partitions when $C_8(H) = 0$.
  - **Solver-free bound $|V(H)| \ge 36$ ($n \ge 18$)**: Proved completely analytically via mutual-center impossibility for locally-$K_{1,3}$ $4$-regular dual line graphs (plus $|V(H)| \ge 38$ whenever $E_1 = 0$).
  - **Sharp $38$-vertex bound ($n \ge 19$)**: Eliminates $5$ profiles and $(1,6,11)$ analytically at $n = 18$, and closes the sole remaining $(6,27,21)$, $(0,8,10)$ branch over all $352{,}716$ labeled $7$-vertex $10$-edge duals and $156{,}240$ point-graph relaxations ($0$ survivors). Tightness is witnessed by the connected $38$-vertex cyclic Haar graph $B(19; \{0,1,8\})$ containing $C_{16}$.
  - **General (non-regular) theta cover corollary**: Any connected component of any finite covering graph of degree $d \le 18$ over a graph containing $\Theta(2^k, 2^k, 2^k)$ contains a cycle of length $2^{k+1}, 2^{k+2}$, or $2^{k+3}$.

### Paper III — *Power-of-Two Cycles in Semidirect $C_3$-Extension Cubic Haar Graphs and Two-Attachment Cubic Gadget Bounds*
- **Files**: [`paper3_semidirect_and_gadgets/`](paper3_semidirect_and_gadgets/README.md) · [LaTeX](paper3_semidirect_and_gadgets/paper3_semidirect_and_gadgets.tex) · [Typst](paper3_semidirect_and_gadgets/paper3_semidirect_and_gadgets.typ) · [PDF](paper3_semidirect_and_gadgets/paper3_semidirect_and_gadgets.pdf) · [Verifier](paper3_semidirect_and_gadgets/verify_paper3.py) · [Certificates](paper3_semidirect_and_gadgets/certificates/paper3_certificates.json)
- **Highlights**:
  - **General $A \rtimes_\sigma C_3$ Theorem**: For any abelian group $A$ (finite or infinite) and $\sigma \in \mathrm{Aut}(A)$ with $\sigma^3 = \mathrm{id}_A$, every connected component of $\mathcal{H}(A \rtimes_\sigma C_3; S)$ contains $C_4, C_8, C_{16}$, or $C_{32}$ (via `W_G10` in Case `(1,0)` and `W_G12` in Case `(1,2)`), extending via normal $2$-kernels (such as $\mathrm{SL}(2,3)$) and to regular covers of $\Theta(2^k, 2^k, 2^k)$.
  - **Eisenstein / Frobenius $C_{16}$ bound**: Whenever $(1 + \sigma + \sigma^2)(A) = 0$ (including abelian-kernel Frobenius groups $A \rtimes C_3$, $A_4$, and fixed-point-free $\mathbb{F}_p$-actions) or $|S \bmod A| \le 2$, every component contains $C_4, C_8$, or $C_{16}$.
  - **Two-attachment $\{C_4, C_8\}$-free cubic gadget bounds & $4{,}802$-vertex witness**: Proves exact closure equivalence $S(H) \cap \{1,3,7\} = \emptyset \iff H + \{0,1\}$ simple $\{C_4,C_8\}$-free cubic; proves $S(H) \cap \{1,3,7\} \ne \emptyset$ analytically for all bipartite gadgets of order $n \le 36$ (sharp at $n=38$); excludes general $\{C_4,C_8\}$-free $2$-attachment gadgets for $n \le 18$ ($n_{\min} \ge 20$, bridge bound $n \ge 40$); and verifies Garcia stretch ($\min S = 13$, path $31 \ge 26$) on the girth-$14$ $C_{16}$-free witness $\mathcal{H}(UT_4(\mathbb{F}_7); \{I, I+E_{12}+E_{23}, I+E_{23}+E_{34}\}) - e$.
  - **Low-order Haar $\Theta(8,8,8)$ & $C_{16}$ census ($|G| \le 45$)**: Exhaustively verifies all `822 / 822` connected $\{C_4, C_8\}$-free Haar classes across `89` groups ($V \le 90$) contain both $C_{16}$ and $\Theta(8,8,8)$.

---

## Relation to Recent Literature (2026)

| Reference | Scope | Relationship to This Repository |
| --- | --- | --- |
| Burkhart (`arXiv:2611.05060`) | Odd-order & nilpotent **Cayley** graphs | Odd-order Cayley graphs have $\delta \ge 4$, and cubic nilpotent Cayley graphs collapse involutions into Sylow-$2$; Papers I & III handle genuinely cubic, non-Cayley **Haar graphs** where figure-eight induction fails. |
| Tranquilli (`arXiv:2608.02675`) | Certified bound $n_{\text{bip}} \ge 60$ for $\{C_4, C_8, C_{16}\}$-free cubic bipartite graphs | Complementary finite-order theorem: Paper II determines the sharp $\{C_4, C_8\}$-free cubic bipartite minimum order ($38$ vs. Markström's non-bipartite $24$). |
| Garcia (`arXiv:2609.04686`) | DRAT $n \ge 24$ for $\{C_4, C_8\}$-free $\delta \ge 3$ graphs, $f(6) \le 32640$, $2$-attachment stretch | Directly motivates Paper II ($24$ general vs. $38$ cubic bipartite) and Paper III's $2$-attachment gadget bounds and $4{,}802$-vertex stretch witness. |
| Ducoffe–Dumitru (`arXiv:2609.28594`) | Structured SAT searches up to $40 / 48 / 66$ vertices; $2^j$-subdivisions | Independent computational frontier on general minimal counterexamples. |
| Carr (`arXiv:2605.22844`) | Predominantly cubic structure of minimal counterexamples | Confirms that cubic and $2$-attachment cubic reductions sit at the structural core of the conjecture. |

---

## Quick Verification

Requires **Python 3.10+** (standard library only; no external solvers or packages required):

```bash
python verify_all.py
```

All three individual verifiers also check byte-for-byte parity against their committed JSON certificates:

```bash
python paper1_nilpotent_haar/verify_paper1.py
python paper2_cubic_bipartite_c4c8/verify_paper2.py
python paper3_semidirect_and_gadgets/verify_paper3.py
```

Checksum verification on releases:

```bash
sha256sum -c SHA256SUMS.txt
```

---

## Repository Structure

```text
erdos-gyarfas-results/
├── LICENSE
├── CITATION.cff
├── README.md
├── SHA256SUMS.txt
├── verify_all.py
├── paper1_nilpotent_haar/
│   ├── README.md
│   ├── paper1_nilpotent_haar.tex
│   ├── paper1_nilpotent_haar.typ
│   ├── paper1_nilpotent_haar.pdf
│   ├── verify_paper1.py
│   └── certificates/paper1_certificates.json
├── paper2_cubic_bipartite_c4c8/
│   ├── README.md
│   ├── paper2_cubic_bipartite_c4c8.tex
│   ├── paper2_cubic_bipartite_c4c8.typ
│   ├── paper2_cubic_bipartite_c4c8.pdf
│   ├── verify_paper2.py
│   └── certificates/paper2_certificates.json
└── paper3_semidirect_and_gadgets/
    ├── README.md
    ├── paper3_semidirect_and_gadgets.tex
    ├── paper3_semidirect_and_gadgets.typ
    ├── paper3_semidirect_and_gadgets.pdf
    ├── verify_paper3.py
    └── certificates/paper3_certificates.json
```

---

## AI Assistance & Provenance Disclosure

Portions of the discovery scripts, finite census engineering, and manuscript formatting in this repository were assisted by AI systems. Every mathematical claim rests either on a complete human-auditable proof in the manuscripts or on deterministic, self-contained standard-library Python verifiers (`verify_paper1.py`, `verify_paper2.py`, `verify_paper3.py`, `verify_all.py`) and SHA-256-checksummed certificates audited by the author.
