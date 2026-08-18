# Domain Primer - Australian SMSF and Accounting Practice

Written for a team with no accounting background. Purpose: enough domain literacy to design the retrieval system, write benchmark questions, and not embarrass ourselves in front of the client.

Compiled 2026-08-17. Every substantive claim carries its source. Where the source is a secondary one (an advisory firm's blog rather than the ATO or legislation), it is marked `[secondary]` and the primary source to confirm against is named. That discipline is not decoration - it is a rehearsal of exactly what we are asking the assistant to do.

## 1. What an SMSF is, in one paragraph

A Self-Managed Superannuation Fund is a private superannuation fund with up to six members, where the members are also the trustees. It exists to pay retirement benefits, and in exchange for concessional tax treatment (15% on earnings in accumulation, 0% in retirement phase up to a cap) it must satisfy a dense set of conditions in the *Superannuation Industry (Supervision) Act 1993* (SIS Act) and its regulations. The ATO is the regulator. Every fund must be audited annually by an ASIC-approved SMSF auditor independent of whoever prepared the accounts. If a fund breaches the rules badly enough it can be made **non-complying**, at which point roughly half its assets can be taxed away. That asymmetry - small ongoing obligations, catastrophic tail risk - is why this domain is so procedural, and why accountants ask the same careful questions over and over.

## 2. Why this is a genuinely hard knowledge domain

Four properties, each of which forces a specific design decision in [`RAG-DESIGN.md`](RAG-DESIGN.md):

**(a) Everything is dated.** Contribution caps, thresholds, and rates change most 1 July. A correct answer for FY2025-26 is a wrong answer for FY2026-27. There is no such thing as an undated fact in this domain.

**(b) Answers compose.** A real question rarely maps to one rule. "Can this 63-year-old start a pension?" touches preservation age, a condition of release, the transfer balance cap, the member's personal TBC, and possibly Division 296. Single-shot retrieval will not do it.

**(c) The vocabulary is exact-token, not semantic.** "Division 296", "NALI", "LRBA", "TBAR", "s 62 SIS", "TR 2010/1", "in-house asset" - these are identifiers. Embedding similarity blurs them; "Division 293" and "Division 296" are near-identical vectors and completely different taxes. This is the strongest possible argument for hybrid retrieval with a lexical channel, and the reason `app/rag/retriever.py` must not be a bare pgvector cosine query.

**(d) The cost of a confident wrong answer is regulatory, not just embarrassing.** See section 5.

## 3. The regulatory sources that would form Corpus A

Ranked by authority. Retrieval should prefer higher tiers and the answer should say which tier it used.

| Tier | Source | What it is | Access |
|---|---|---|---|
| 1 | *Superannuation Industry (Supervision) Act 1993* and Regulations; *Income Tax Assessment Act 1997* | The law itself | legislation.gov.au, with point-in-time versions |
| 1 | [ATO Legal database](https://www.ato.gov.au/single-page-applications/legaldatabase) | Rulings (TR), determinations (TD), interpretative decisions, practical compliance guidelines (PCG) | Public, stable `DocID` URLs |
| 2 | ATO guidance pages and the [SMSF Newsroom](https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/self-managed-super-funds-smsf/smsf-newsroom) | The regulator's plain-English position and change announcements | Public web, the practical day-to-day source |
| 2 | Tax Practitioners Board - Code of Professional Conduct, practice notes | Binding on the firm as a registered tax agent | tpb.gov.au |
| 2 | APESB - **APES 110** (Code of Ethics), **APES 305** (terms of engagement), **APES 320** (quality management) | Binding on CA/CPA members | apesb.org.au |
| 3 | AASB accounting standards | Financial reporting; less central for SMSF than for general practice | [aasb.gov.au](https://aasb.gov.au/) |
| 3 | SMSF Association, CPA Australia, CA ANZ technical content | Professional-body interpretation. Useful, not authoritative | Partly member-gated |
| 4 | Advisory-firm blogs (Accurium, Heffron, etc.) | Fast, readable, often first to explain a change. Frequently right, occasionally wrong, never citable to a client as authority | Public |

**Design consequence:** `tier` is a column on the chunk table, drives ranking, and appears in the answer. An answer resting on tier 4 must say so.

## 4. What is changing right now - the "ever-evolving" problem, made concrete

The client's stated pain is keeping up. As it happens, 1 July 2026 was one of the largest single-day changes to Australian superannuation in a decade, which makes this an unusually good time to build this assistant and an unusually good source of benchmark questions. These are the live items:

### Division 296 - the tax on large super balances

Commences **1 July 2026**. An additional tax on earnings attributable to a member's total superannuation balance above a **large super balance threshold (LSBT) of $3 million**, at 15%, with a further 10% on the component above a **very large super balance threshold (VLSBT) of $10 million**. It is assessed to the *individual*, not the fund, but SMSF trustees must report member information to the ATO to support it. The first assessment is based on total super balance at **30 June 2027**.
Sources: [ATO - About Division 296 tax for SMSFs](https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/self-managed-super-funds-smsf/smsf-administration-and-reporting/about-division-296-tax-for-smsfs); [CPA Australia - Lowdown on Division 296](https://www.cpaaustralia.com.au/public-practice/inpractice/taxation/lowdown-on-division-296); draft regulations discussed by [Accurium, March 2026](https://www.accurium.com.au/blog/2026/03/division-296-draft-regulations-what-they-mean-for-smsf-trustees-and-actuaries/).

Why it matters to Alfa Focus: it creates a brand-new annual obligation touching their highest-value clients, and the mechanics were still settling in draft regulations months before commencement. This is precisely the class of question where a stale answer is dangerous.

### Payday super

From **1 July 2026**, employer superannuation guarantee contributions must be paid within **seven business days of each payday**, replacing the quarterly regime. The maximum contribution base moves from a quarterly $62,500 to an annual $270,830.
Sources: [ATO - Payday super regulations: further details for SMSFs](https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/self-managed-super-funds-smsf/smsf-newsroom/payday-super-regulations-further-details-for-smsfs); `[secondary]` [Super Informed summary](https://superinformed.com.au/newsletter/smsf-changes-1-july-2026/).

### Transfer balance cap indexation

The **general transfer balance cap rises from $2.0m to $2.1m on 1 July 2026**. The cap governs how much can be moved into the tax-free retirement phase. Each member also has a *personal* TBC, which the ATO computes from reported transfer balance account events - so **any TBAR event up to 30 June 2026 that was not reported will produce a wrong personal cap**.
Source: [ATO - General transfer balance cap indexation on 1 July 2026](https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/self-managed-super-funds-smsf/smsf-newsroom/general-transfer-balance-cap-indexation-on-1-july-2026).

This one is a gift for evaluation design: the general cap is a public fact, but the personal cap is fund-specific and depends on unreported data. The correct behaviour is to state the general cap with a citation and then **refuse to state the personal cap**, directing the user to the member's TBA record. A benchmark question that rewards that refusal is worth more than ten lookup questions.

### 2026-27 contribution caps

Concessional **$32,500**; non-concessional **$130,000**; maximum bring-forward **$390,000**.
Sources: `[secondary]` [Super Informed](https://superinformed.com.au/newsletter/smsf-changes-1-july-2026/); confirm against [ATO - Non-concessional contributions cap](https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/super/growing-and-keeping-track-of-your-super/caps-limits-and-tax-on-super-contributions/non-concessional-contributions-cap) before these numbers go into any evaluation golden answer. **Do not treat a blog-sourced cap as ground truth in a benchmark.**

### Administrative

Australia Post's SMSF Gateway closes permanently **30 June 2026** - funds using it for SuperStream rollovers and contributions must move to another provider. `[secondary]`

### Enforcement climate

The ATO increased referrals to ASIC for breaches of APES 110 during 2025-26. `[secondary]` Confirm against ATO and ASIC published enforcement data. Directionally, professional-conduct scrutiny is rising, which strengthens rather than weakens the case for a citation-first tool.

## 5. The professional-obligations constraint - read this before writing any code

This is not a compliance footnote. It determines the architecture and the hosting decisions already partly made in this repo.

**Client data must not go into public AI tools.** CPA Australia, through its Centre of Excellence in Ethics and Professional Standards, has stated that uploading client data into a public-facing AI tool is not acceptable, while in-house tools with adequate privacy and security attributes are.
Source: [CPA Australia - How far can you go with AI before you hit an ethical dilemma?](https://www.cpaaustralia.com.au/public-practice/inpractice/digital-technology/how-far-can-you-go-ai-before-hit-ethical-dilemma).

**APES 110 confidentiality and APES 320 quality management apply to AI use directly.** `[secondary]` Confirm against the APESB standards themselves.

**Under the TPB Code of Professional Conduct, an AI error the practitioner relied on is the practitioner's competence breach.** `[secondary]` Confirm against the TPB code and its practice notes. The design consequence is unambiguous: the assistant's job is to get a qualified human to the right primary source faster, with the reasoning laid out. It is not to be the answer. Every response should be reviewable in under a minute by someone who then owns the advice.

**Design decisions that follow directly, and what they mean for this repo:**

1. Corpus B and all query text stay inside the controlled boundary - Supabase (dev and prod projects) plus Render. Whatever model API `app/rag/generator.py` calls must have contractual no-training terms, and the choice belongs in the proposal, not in a commit message.
2. De-identify by construction. The assistant answers *rules* questions. It should not need a member's name or TFN, and the Chainlit interface should actively discourage pasting them - see [`PROMPTS.md`](PROMPTS.md).
3. Every answer carries provenance, and the citation must be one click from the primary source.
4. Log everything. A firm under APES 320 needs to show what the tool said and what the practitioner did with it. This is a reason the `EvalResult`-style tables in `app/db/models.py` should record production traces, not just test runs.

## 6. Glossary for the team

| Term | Meaning |
|---|---|
| SMSF | Self-Managed Superannuation Fund |
| SIS Act / SISR | *Superannuation Industry (Supervision) Act 1993* / Regulations - the governing law |
| SAR | SMSF Annual Return, lodged with the ATO |
| TBC | Transfer balance cap - lifetime limit on moving money into tax-free retirement phase |
| TBAR | Transfer Balance Account Report - how funds report TBC events to the ATO |
| TSB | Total superannuation balance - a member's total across all funds, drives eligibility for many things |
| Concessional contribution | Pre-tax contribution (employer SG, salary sacrifice), capped annually |
| Non-concessional contribution | After-tax contribution, capped, with a bring-forward option |
| Condition of release | The event (retirement, age 65, etc.) that legally unlocks benefits |
| Preservation age | Age before which benefits generally cannot be accessed |
| LRBA | Limited Recourse Borrowing Arrangement - the only way an SMSF may borrow, used for property |
| In-house asset | Investment in a related party; capped at 5% of fund assets |
| Sole purpose test | s 62 SIS - the fund must be maintained solely to provide retirement benefits |
| NALI / NALE | Non-Arm's Length Income / Expenditure - punitive 45% tax where dealings are not at arm's length |
| Division 296 | The new tax on earnings attributable to balances above $3m, from 1 July 2026 |
| Division 293 | An *older, different* tax - extra 15% on concessional contributions for high earners. Not the same thing. A classic confusion the assistant must not make |
| Contravention (ACR) | Auditor Contravention Report - what the auditor lodges with the ATO when a fund breaches |
| APES 110 | The accounting profession's Code of Ethics |
| TPB | Tax Practitioners Board - registers and regulates tax agents |

## 7. Where domain ground truth for evaluation must come from

We cannot author golden answers ourselves. Neither can an LLM. Three legitimate routes, in order of preference:

1. **An Alfa Focus accountant reviews and signs off** a golden set. Best quality, costs client time, and the ask has to be small and well-structured - roughly 40 questions with pre-drafted answers to correct rather than write.
2. **Derive golden answers from a tier-1 or tier-2 source and cite the paragraph.** Works well for factual and date-scoped questions. Verifiable by anyone, including a marker.
3. **Our own reasoning.** Only acceptable for behavioural questions - should the assistant refuse, did it cite, did it scope to a year - where correctness does not depend on tax expertise.

Route 3 covers more of the benchmark than you would expect, which is fortunate given the timeline. See [`EVALUATION.md`](EVALUATION.md).
