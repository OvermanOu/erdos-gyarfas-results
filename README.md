# Erdős–Gyárfás Conjecture: Manuscripts and Reproducible Verification Artifacts

[![Verify All](https://img.shields.io/badge/python-3.10%2B%20stdlib%20only-blue)](verify_all.py)
[![License](https://img.shields.io/badge/license-MIT%20%2F%20CC--BY--4.0-green)](LICENSE)

This repository archives two standalone mathematical papers and their zero-dependency Python verification suites establishing structural power-of-two cycle results toward the **Erdős–Gyárfás conjecture** (every finite simple graph with $\delta(G) \ge 3$ contains a simple cycle of length $2^k$ for some $k \ge 2$).

> **繁體中文簡介**：本公開倉庫彙整作者（OvermanOu）針對 **Erdős–Gyárfás 猜想** 的兩項主要已驗證數學成果，各自附有完整 AMS-LaTeX / Typst 論文手稿、編譯 PDF、無外部依賴的 Python 標準庫驗證腳本與 JSON 憑證檔案；執行 `python verify_all.py` 約兩秒即可全數重現驗證。

---

## Papers and Main Theorems

### Paper I — *Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Four*
- **Files**: [`paper1_nilpotent_haar/`](paper1_nilpotent_haar/README.md) · [LaTeX](paper1_nilpotent_haar/paper1_nilpotent_haar.tex) · [Typst](paper1_nilpotent_haar/paper1_nilpotent_haar.typ) · [PDF](paper1_nilpotent_haar/paper1_nilpotent_haar.pdf) · [Verifier](paper1_nilpotent_haar/verify_paper1.py) · [Certificates](paper1_nilpotent_haar/certificates/paper1_certificates.json)
- **Highlights**:
  - **2-kernel & nilpotency class $\le 3$**: Every connected component of every simple cubic $3$-shift Haar graph $\mathcal{H}(\Gamma; S)$ where $\Gamma/N$ is nilpotent of class $\le 3$ for a normal $2$-subgroup $N \trianglelefteq \Gamma$ contains a simple $2^k$-cycle (specifically $C_4, C_8, C_{16}$, or $C_{32}$ when $\Gamma$ is nilpotent of class $\le 3$ and odd order).
  - **Class $4$ for $p \ge 5$ (arbitrary exponent)**: Every finite $p$-group of class $\le 4$ ($p \ge 5$, arbitrary exponent) yields $C_4, C_8, C_{16}, C_{32}$, or $C_{64}$ via three universal $64$-color words ($\det = 27 \neq 0 \bmod p$); extended via normal $2$-kernels when the quotient's Sylow $3$-subgroup has class $\le 3$.
  - **Dyadic theta cover obstruction**: Any regular $\Gamma$-cover of a connected graph containing three internally disjoint equal-length paths $\Theta(2^k, 2^k, 2^k)$ contains a simple $2^s$-cycle in every component.
  - **Tight boundaries**: Universal $C_{64}$ in $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^5$ for all primes $p \ge 2, k \ge 1$, alongside girth-$14$ ($UT_4(\mathbb{F}_p)$, $p \ge 7$) and girth-$\ge 18$ ($UT_6(\mathbb{F}_p)/\langle I+E_{16}\rangle$, $p \ge 11$) families avoiding $\{C_4, C_8, C_{16}\}$.

### Paper II — *The Sharp 38-Vertex Bound for $\{C_4, C_8\}$-Free Cubic Bipartite Graphs and Dyadic Theta Cover Obstructions*
- **Files**: [`paper2_cubic_bipartite_c4c8/`](paper2_cubic_bipartite_c4c8/README.md) · [LaTeX](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.tex) · [Typst](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.typ) · [PDF](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.pdf) · [Verifier](paper2_cubic_bipartite_c4c8/verify_paper2.py) · [Certificates](paper2_cubic_bipartite_c4c8/certificates/paper2_certificates.json)
- **Highlights**:
  - **Point-graph $C_8$ gap identity & star decomposition**: Exact algebraic identity relating $2C_8(H)$ to edge/nonedge codegrees of the $6$-regular point graph $Q$, forcing edge-disjoint star-$K_4$ blocks and residual codegree-$2$ triangle partitions when $C_8(H) = 0$.
  - **Solver-free bound $|V(H)| \ge 36$ ($n \ge 18$)**: Proved completely analytically via mutual-center impossibility for locally-$K_{1,3}$ $4$-regular dual line graphs (plus $|V(H)| \ge 38$ whenever $E_1 = 0$).
  - **Sharp $38$-vertex bound ($n \ge 19$)**: Eliminates $5$ profiles and $(1,6,11)$ analytically at $n = 18$, and closes the sole remaining $(6,27,21)$, $(0,8,10)$ branch over all $352{,}716$ labeled $7$-vertex $10$-edge duals and $156{,}240$ point-graph relaxations ($0$ survivors). Tightness is witnessed by the connected $38$-vertex cyclic Haar graph $B(19; \{0,1,8\})$ containing $C_{16}$.
  - **General (non-regular) theta cover corollary**: Any connected component of any finite covering graph of degree $d \le 18$ over a graph containing $\Theta(2^k, 2^k, 2^k)$ contains a cycle of length $2^{k+1}, 2^{k+2}$, or $2^{k+3}$.

---

## Relation to Recent Literature (2026)

| Reference | Scope | Relationship to This Repository |
| --- | --- | --- |
| Burkhart (`arXiv:2611.05060`) | Odd-order & nilpotent **Cayley** graphs | Odd-order Cayley graphs have $\delta \ge 4$, and cubic nilpotent Cayley graphs collapse involutions into Sylow-$2$; Paper I handles genuinely cubic, non-Cayley **Haar graphs** where figure-eight induction fails. |
| Tranquilli (`arXiv:2608.02675`) | Certified bound $n_{\text{bip}} \ge 60$ for $\{C_4, C_8, C_{16}\}$-free cubic bipartite graphs | Complementary finite-order theorem: Paper II determines the sharp $\{C_4, C_8\}$-free cubic bipartite minimum order ($38$ vs. Markström's non-bipartite $24$) via a mostly analytic point-graph duality proof. |
| Garcia (`arXiv:2609.04686`) | DRAT $n \ge 24$ for $\{C_4, C_8\}$-free $\delta \ge 3$ graphs, $f(6) \le 32640$, $2$-attachment stretch | Motivates our Paper II comparison ($24$ general vs. $38$ cubic bipartite) and cover-obstruction viewpoint. |
| Ducoffe–Dumitru (`arXiv:2609.28594`) | Structured SAT searches up to $40 / 48 / 66$ vertices; $2^j$-subdivisions | Independent computational frontier on general minimal counterexamples. |
| Carr (`arXiv:2605.22844`) | Predominantly cubic structure of minimal counterexamples | Confirms that cubic and bipartite-cubic reductions sit at the structural core of the conjecture. |

---

## Quick Verification

Requires **Python 3.10+** (standard library only; no external solvers or packages required):

```bash
python verify_all.py
```

Both individual verifiers also check byte-for-byte parity against the committed JSON certificates:

```bash
python paper1_nilpotent_haar/verify_paper1.py
python paper2_cubic_bipartite_c4c8/verify_paper2.py
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
└── paper2_cubic_bipartite_c4c8/
    ├── README.md
    ├── paper2_cubic_bipartite_c4c8.tex
    ├── paper2_cubic_bipartite_c4c8.typ
    ├── paper2_cubic_bipartite_c4c8.pdf
    ├── verify_paper2.py
    └── certificates/paper2_certificates.json
```

---

## AI Assistance & Provenance Disclosure

Portions of the discovery scripts, finite census engineering, and manuscript formatting in this repository were assisted by AI systems. Every mathematical claim rests either on a complete human-auditable proof in the manuscripts or on deterministic, self-contained standard-library Python verifiers (`verify_paper1.py`, `verify_paper2.py`, `verify_all.py`) and SHA-256-checksummed certificates audited by the author.
