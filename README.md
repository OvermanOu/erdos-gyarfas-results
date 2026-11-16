# Erdős–Gyárfás Conjecture — Published Theorems, Manuscripts & Verifiers

[![Verification](https://img.shields.io/badge/verification-4%2F4%20PASS%20(stdlib%20only)-brightgreen)](verify_all.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v3.0.0-orange)](https://github.com/OvermanOu/erdos-gyarfas-results/releases/tag/v3.0.0)

Self-contained manuscripts (`Typst` / `PDF` and `LaTeX`), machine-readable JSON certificate bundles, and zero-dependency Python 3 standard-library verifiers advancing the **Erdős–Gyárfás conjecture** (1995): *every finite simple graph of minimum degree at least $3$ contains a simple cycle of length $2^k$ ($k \ge 2$).*

> **繁體中文摘要 / Summary in Traditional Chinese**  
> 本公開倉庫收錄針對 Erdős–Gyárfás 猜想的四篇完整論文手稿（`.pdf` / `.typ` / `.tex`）、可重現機器證書（`certificates/*.json`）與零外部套件依賴的 Python 3 標準函式庫驗證腳本：
> 1. **Paper I（無條件至多類 6 冪零群立方 Haar 圖）**：無條件解決所有正規 $2$-子群商為至多類 $4$ 冪零群之立方三平移 Haar 圖（任意質數與指數，奇數階至多類 $4$ 必含 $C_4,C_8,C_{16},C_{32}$）；進一步將自由群 Magnus 展開推至 **6 次（nilpotency class $\le 6$）**，無條件解決所有奇數質數 $p \ge 5$ 與任意指數之至多類 $6$ 有限冪零群（含 Sylow-$3$ 子群至多類 $4$ 之混合群），構造出全質數 $p \ge 2, k \ge 1$ 通用的 $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^7$ 通用 $C_{64}$ 證書（`992/992` 前綴差整數係數 $\gcd = 1$），並證明類 $\ge 5$ 不存在長度 $32$ 的自由群通用字（`0/288` 閉合）。
> 2. **Paper II（二分立方無 $\{C_4, C_8\}$ 圖之精確 $38$ 頂點下界與 Theta 覆蓋障礙）**：藉點圖 $C_8$ 共度差恆等式與「星-$K_4$ 裝填 + $K_{1,3}$ 區域結構不可能定理」，嚴格證明每個非空簡單無 $\{C_4, C_8\}$ 二分立方圖至少有 $38$ 個頂點（於 $B(19; \{0,1,8\})$ 達到等號，亦涵蓋所有有限度數 $d \le 18$ 的等長二進 Theta 覆蓋）。
> 3. **Paper III（半直積 $C_3$-擴張立方 Haar 圖與二端點構件精確分類）**：無條件證明任意阿貝爾群之半直積 $A \rtimes_\sigma C_3$（$\sigma^3 = \mathrm{id}_A$）立方 Haar 圖必含 $C_4, C_8, C_{16}$ 或 $C_{32}$（於 Eisenstein / Frobenius 情形強化至銳界 $C_{16}$）；於二端點立方構件方面完成健全性雙重校驗之窮舉分類，證明 $4 \le n \le 18$ 零構件存在，確定精確最小階數 $n_{\min}(\{C_4,C_8\}\text{-free}) = 20$（僅餘 `3` 個極值同構類，全含 $C_{16}$ 且命中 $\{3,7\}$，故 $n_{\min}(\{C_4,C_8,C_{16}\}\text{-free}) \ge 22$、分離橋下界 $n \ge 44$、閉合允許最小階數 $n_{\min}^{\mathrm{cl}} = 24$）；並驗證 $4,802$ 頂點 girth-$14$ 無 $\{C_4,C_8,C_{16}\}$ 拉伸見證，以及橫跨全數 $3 \le |G| \le 47$（全 `196` 個 OEIS A000001 群之 `151` 個二生成群、`20,114` 類、`3,518` 無 $\{C_4,C_8\}$ 實例，零遺漏階數）之 $100\%$ 含 $C_{16}$ 與 $\Theta(8,8,8)$ 普查。
> 4. **Paper IV（Klein 瓶、半直積 $C_2$/$C_4$ 銳界 $C_{16}$ 定理與二分構件缺陷點圖 $C_8$ 恆等式）**：證明所有 Klein 瓶群 $\mathcal{K}_0 = \langle a,b \mid a b a^{-1}=b^{-1}\rangle$ 商群、所有半直積 $A \rtimes_\sigma C_2$ 與所有（無額外條件之）$\sigma^4 = \mathrm{id}_A$ 半直積 $A \rtimes_\sigma C_4$ 立方 Haar 圖皆必含 $C_4, C_8$ 或 **$C_{16}$**（並於正規 $2$-核提升下涵蓋 $A \rtimes_\sigma C_{2^r}$、$\mathrm{GL}(2,3)$ 與 $\mathrm{Dic}_{4m}$）；同時推廣 Paper II 恆等式為**二分二端點構件之精確缺陷點圖 $C_8(H)$ 恆等式**，免求解器純解析排除所有 $|V(H)| \le 28$（每側 $n \le 14$）的無 $\{C_4,C_8\}$ 二分二端點立方構件（與 $0\text{--}1$ 端點距離無關）。

---

## Papers & Main Results

| Paper | Title & Downloads | Key Theorems & Verified Certificates |
| :--- | :--- | :--- |
| **Paper I** | **Power-of-Two Cycles in Cubic Haar Graphs over Nilpotent Groups of Class at Most Six**<br>[PDF](paper1_nilpotent_haar/paper1_nilpotent_haar.pdf) · [Typst](paper1_nilpotent_haar/paper1_nilpotent_haar.typ) · [LaTeX](paper1_nilpotent_haar/paper1_nilpotent_haar.tex) · [Verifier](paper1_nilpotent_haar/verify_paper1.py) · [Certs](paper1_nilpotent_haar/certificates/paper1_certificates.json) | Unconditional class $\le 4$ (any prime/exponent/3-Sylow + normal $2$-kernels, sharp $C_{32}$ odd-order); unconditional classes $5, 6$ for Sylow-3 class $\le 4$ (all $p \ge 5$ groups of class $\le 6$, verified on $UT_7(\mathbb{F}_5)$ of order $5^{21}$, class $6$, $\exp 25$); universal $(\mathbb{Z}/p^k\mathbb{Z})\langle X,Y\rangle/(X,Y)^7$ $C_{64}$ certificate (`992/992` deg-6 gcds $= 1$); `0/288` deg-5 length-32 barrier; high-girth $UT_4(\mathbb{F}_p)$ & $UT_6(\mathbb{F}_p)/\langle I+E_{16}\rangle$; regular $\Theta(2^k,2^k,2^k)$ covers. |
| **Paper II** | **The Sharp 38-Vertex Bound for $\{C_4, C_8\}$-Free Cubic Bipartite Graphs and Dyadic Theta Cover Obstructions**<br>[PDF](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.pdf) · [Typst](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.typ) · [LaTeX](paper2_cubic_bipartite_c4c8/paper2_cubic_bipartite_c4c8.tex) · [Verifier](paper2_cubic_bipartite_c4c8/verify_paper2.py) · [Certs](paper2_cubic_bipartite_c4c8/certificates/paper2_certificates.json) | Exact quadratic $C_8$ point-graph gap identity; Star-$K_4$ & $L(D)$ ($K_{1,3}$) structural obstruction eliminating $n \le 17$ analytically; elimination of $5/6$ profiles + degree-$18$ solver certificate at $n=18$; sharp $38$-vertex minimum ($n \ge 19$) via $B(19;\{0,1,8\})$; dyadic cover obstruction $\Theta(2^k,2^k,2^k)$ for all finite cover degrees $d \le 18$. |
| **Paper III** | **Power-of-Two Cycles in Semidirect $C_3$-Extension Cubic Haar Graphs and Two-Attachment Cubic Gadget Bounds**<br>[PDF](paper3_semidirect_and_gadgets/paper3_semidirect_and_gadgets.pdf) · [Typst](paper3_semidirect_and_gadgets/paper3_semidirect_and_gadgets.typ) · [LaTeX](paper3_semidirect_and_gadgets/paper3_semidirect_and_gadgets.tex) · [Verifier](paper3_semidirect_and_gadgets/verify_paper3.py) · [Certs](paper3_semidirect_and_gadgets/certificates/paper3_certificates.json) | Unconditional $A \rtimes_\sigma C_3$ ($\sigma^3=\mathrm{id}_A$) theorem ($C_4\dots C_{32}$; sharp $C_{16}$ for $1+\sigma+\sigma^2=0$, $|S\bmod A|\le 2$) + $\mathrm{SL}(2,3)$ (`176` pairs); exact two-attachment closure equivalence + bipartite $n\le 36$ bound (sharp at $n=38$); soundness-checked exact $n_{\min}(\{C_4,C_8\}\text{-free}) = 20$ (`0` for $n\le 18$; `3` classes at $n=20$, all girth $3$, non-bipartite, hitting $\{3,7\}$, $C_{16}$ present), forcing $n_{\min}(\{C_4,C_8,C_{16}\}\text{-free}) \ge 22$ (bridge $\ge 44$) and sharp $n_{\min}^{\mathrm{cl}} = 24$ via `MARKSTROM24 - {0,1}`; $4,802$-vertex girth-$14$ $\{C_4,C_8,C_{16}\}$-free stretch witness (`min S = 13`, path `31 >= 26`); zero-gap `3 <= |G| <= 47` census (`151` 2-gen / `196` OEIS groups, `20,114` pairs, `3,518` `{C_4,C_8}`-free classes = `2,752` abelian + `766` nonabelian, `3,518/3,518` contain both $C_{16}$ & $\Theta(8,8,8)$). |
| **Paper IV** | **Sharp $C_{16}$ Bounds for Semidirect $C_2$-, $C_4$-, and Klein-Bottle Cubic Haar Graphs and the Defect Point-Graph $C_8$ Identity for Bipartite Gadgets**<br>[PDF](paper4_semidirect_c2_c4_and_gadget_gap/paper4_semidirect_c2_c4_and_gadget_gap.pdf) · [Typst](paper4_semidirect_c2_c4_and_gadget_gap/paper4_semidirect_c2_c4_and_gadget_gap.typ) · [LaTeX](paper4_semidirect_c2_c4_and_gadget_gap/paper4_semidirect_c2_c4_and_gadget_gap.tex) · [Verifier](paper4_semidirect_c2_c4_and_gadget_gap/verify_paper4.py) · [Certs](paper4_semidirect_c2_c4_and_gadget_gap/certificates/paper4_certificates.json) | Sharp $C_{16}$ for all Klein-bottle quotients $\mathcal{K}_0 = \langle a,b \mid a b a^{-1} = b^{-1} \rangle$ (`w_KB`), all $A \rtimes_\sigma C_2$ (`w_G10`), and **all** general $A \rtimes_\sigma C_4$ ($\sigma^4 = \mathrm{id}_A$ only, `w_G10` in both `(1,0)` and `(1,2)`); Gaussian/Frobenius ($\sigma^2=-\mathrm{id}_A$) direct $16$-words without conjugation; normal $2$-kernel lifting (`A \rtimes_\sigma C_{2^r}`, $\mathrm{GL}(2,3)$ `416` pairs, $\mathrm{Dic}_{4m}$, $C_{13}\rtimes_5 C_4$ `312` classes, $\mathbb{F}_5^4 \rtimes_{\mathrm{shift}} C_4$ order `2,500`, `25` Klein-bottle quotients); Exact Defect Point-Graph $C_8(H)$ identity on `7` controls, local $K_{2,2}$-free capacities (`6, 6, 4, -2`), and solver-free Defect Star-$K_4$ bound $\|V(H)\| \ge 30$ ($n \le 14$) regardless of $p_0\text{--}\ell_0$ distance. |

---

## Comparison with Related Literature (2023–2026)

| Reference | Regime / Family | Sharpness & Comparison with Our Results |
| :--- | :--- | :--- |
| Liu–Montgomery (*J. Amer. Math. Soc.* 36, 2023) | Sufficiently large average degree | Leaves bounded-degree / cubic graphs completely open. |
| Markström (*Congr. Numer.* 171, 2004); Garcia (`arXiv:2609.04686`, 2026) | Small $\{4,8\}$-free bounds & two-attachment stretch | Cubic $f(3)=24$ (Markström) & general $\delta \ge 3$ $n \ge 24$ (Garcia). Our Paper III establishes $n_{\min}(\{C_4,C_8\}\text{-free}) = 20$ (`3` classes), $n_{\min}(\{C_4,C_8,C_{16}\}\text{-free}) \ge 22$ (bridge $\ge 44$), sharp $n_{\min}^{\mathrm{cl}} = 24$ via `MARKSTROM24 - {0,1}`, and $4,802$-vertex stretch witness (`31 >= 26`). |
| Carr (`arXiv:2605.22844`, 2026) | Predominantly cubic structure of minimal counterexamples | Motivates Paper II, Paper III, and Paper IV cubic & two-attachment reductions. |
| Ducoffe–Dumitru (`arXiv:2609.28594`, 2026) | General $n \ge 41$, cubic $n \ge 50$, bipartite cubic $n \ge 66$ ($\{4,8,16,32\}$-free) | Complements Paper II's sharp $38$-vertex $\{C_4, C_8\}$-free cubic bipartite threshold and Paper IV's distance-independent $|V(H)| \ge 30$ bipartite gadget bound. |
| Tranquilli (`arXiv:2608.02675`, 2026) | Cubic bipartite minimal counterexamples $\ge 60$ | Orthogonal computational bound vs. our algebraic/analytic point-graph gap identities. |
| Burkhart (`arXiv:2611.05060`, 2026) | Odd-order Cayley & finite nilpotent Cayley graphs | Figure-eight & involution arguments fail on cubic non-Cayley Haar graphs. Papers I, III, and IV unconditionally resolve nilpotent class $\le 6$ ($p \ge 5$ / Sylow-3 class $\le 4$), class $\le 4$ ($p=3$), and all $A \rtimes_\sigma C_2, C_3, C_4$ cubic Haar families + regular $\Theta(2^k,2^k,2^k)$ covers. |

---

## Reproducing All Verifications

Requires **Python 3.10+** with **zero third-party packages** (standard library only):

```bash
python verify_all.py
```

Or run each paper's standalone verifier individually:

```bash
python paper1_nilpotent_haar/verify_paper1.py
python paper2_cubic_bipartite_c4c8/verify_paper2.py
python paper3_semidirect_and_gadgets/verify_paper3.py
python paper4_semidirect_c2_c4_and_gadget_gap/verify_paper4.py
```

All outputs are checked deterministically against the committed files in `*/certificates/*.json`, and every file in the repository is checksummed in [`SHA256SUMS.txt`](SHA256SUMS.txt).

---

## Repository Structure

```text
.
├── CITATION.cff
├── LICENSE
├── README.md
├── SHA256SUMS.txt
├── verify_all.py
├── paper1_nilpotent_haar/
│   ├── README.md
│   ├── verify_paper1.py
│   ├── certificates/paper1_certificates.json
│   ├── paper1_nilpotent_haar.typ
│   ├── paper1_nilpotent_haar.tex
│   └── paper1_nilpotent_haar.pdf
├── paper2_cubic_bipartite_c4c8/
│   ├── README.md
│   ├── verify_paper2.py
│   ├── certificates/paper2_certificates.json
│   ├── paper2_cubic_bipartite_c4c8.typ
│   ├── paper2_cubic_bipartite_c4c8.tex
│   └── paper2_cubic_bipartite_c4c8.pdf
├── paper3_semidirect_and_gadgets/
│   ├── README.md
│   ├── verify_paper3.py
│   ├── certificates/paper3_certificates.json
│   ├── paper3_semidirect_and_gadgets.typ
│   ├── paper3_semidirect_and_gadgets.tex
│   └── paper3_semidirect_and_gadgets.pdf
└── paper4_semidirect_c2_c4_and_gadget_gap/
    ├── README.md
    ├── verify_paper4.py
    ├── certificates/paper4_certificates.json
    ├── paper4_semidirect_c2_c4_and_gadget_gap.typ
    ├── paper4_semidirect_c2_c4_and_gadget_gap.tex
    └── paper4_semidirect_c2_c4_and_gadget_gap.pdf
```

---

## AI Assistance & Provenance

Portions of the search scripts, symbolic verifiers, and manuscript preparation were assisted by AI systems. Every theorem, proof, finite exhaustion, and numerical certificate was audited by the author and stands on the deterministic standard-library Python verifiers included in this repository.
