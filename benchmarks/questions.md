# SMSF Accountant Test Set - Draft Q&A (25 questions)

Draft only. **We have not met the client yet** - these are our best estimate of the real question mix (per `docs/EVALUATION.md` section 2), not confirmed against Alfa Focus's actual inbound questions. Several answers are marked unevaluated or pending sign-off for the same reason. Do not treat any answer here as a final golden answer until it has been through the review routes described in `docs/EVALUATION.md` section 1.

**Revision note:** this set has been re-passed against the seven use cases in [`docs/USE-CASES.md`](../docs/USE-CASES.md). Each question is now tagged with the use case it tests, alongside its existing `docs/EVALUATION.md` question-type class. This surfaced one use case (residency/cross-border) that had zero coverage - three questions have been added for it (Q21-Q23), plus one each for the LRBA related-party-lease angle (Q24) and the small-business-CGT-concession contribution interaction (Q25).

### Coverage against the seven use cases

| Use case (`docs/USE-CASES.md`) | Questions | Count |
|---|---|---|
| UC-1 Compliance and investment restrictions | Q12, Q15, Q20 | 3 |
| UC-2 Property in super and borrowing (LRBA) | Q11, Q24 | 2 |
| UC-3 Contribution caps, thresholds, eligibility | Q6, Q7, Q18, Q25 | 4 |
| UC-4 Pension phase, condition of release, TBC | Q1, Q4, Q8, Q10, Q16 | 5 |
| UC-5 Cross-border and residency | Q21, Q22, Q23 | 3 |
| UC-6 Division 296 and large-balance reporting | Q5, Q9, Q19 | 3 |
| UC-7 Establishment and annual compliance cycle | Q2, Q3, Q13, Q14, Q17 | 5 |

UC-1, UC-2 and UC-6 are still short of the target 5-per-use-case depth - flagged for the next revision pass rather than padded out now with lower-quality questions.

---

### C1 - Single-fact lookup

**Q1. What is the general transfer balance cap for 2026-27?**
A: For 2026-27, the general transfer balance cap is $2.1 million, up from $2.0 million in 2025-26.
*Use case: UC-4 (Pension phase, condition of release, TBC). Comment: Confidence HIGH per DOMAIN-PRIMER.md. Straightforward retrieval + citation check - no client input needed to verify.*

**Q2. What is the maximum number of members an SMSF may have?**
A: An SMSF may have up to six members, and every member must also be a trustee (or director of the corporate trustee).
*Use case: UC-7 (Establishment and annual compliance cycle). Comment: A stable structural rule, not income-year dependent - unlike most of this set.*

**Q3. Who is permitted to audit an SMSF?**
A: Every SMSF must be audited annually by an ASIC-approved SMSF auditor who is independent of whoever prepared the fund's accounts.
*Use case: UC-7 (Establishment and annual compliance cycle). Comment: Tests whether the assistant states the independence requirement, not just "an approved auditor".*

---

### C2 - Date-sensitive

**Q4. What was the general transfer balance cap for 2025-26?**
A: For 2025-26, the general transfer balance cap was $2.0 million.
*Use case: UC-4 (Pension phase, condition of release, TBC). Comment: Trap question - a retriever without a date filter will return the 2026-27 figure ($2.1m) instead.*

**Q5. When does Division 296 commence, and what balance is the first assessment based on?**
A: Division 296 commences 1 July 2026. It taxes earnings on the portion of a member's total super balance above $3 million (extra 15%), plus a further 10% above $10 million. The first assessment uses the balance at 30 June 2027.
*Use case: UC-6 (Division 296 and large-balance reporting). Comment: Also checks the answer doesn't conflate this with Division 293 (see Q19).*

**Q6. From when must employers pay superannuation guarantee within seven business days of payday?**
A: From 1 July 2026, under payday super, employer SG contributions must be paid within seven business days of each payday, replacing the quarterly regime.
*Use case: UC-3 (Contribution caps, thresholds, eligibility) - administrative timing rather than a cap figure, but it directly changes how and when contributions land in the fund. Comment: Straightforward date-scoped fact.*

**Q7. A fund is finalising its 2024-25 annual return. Which contribution caps apply?**
A: The 2024-25 caps apply - not the current-year (2026-27) caps. The answer must cite the 2024-25 figures specifically and note that later-year caps aren't relevant to this lodgement.
*Use case: UC-3 (Contribution caps, thresholds, eligibility). Comment: Trap question - current-year caps are the wrong answer here. Exact 2024-25 figures still need direct ATO confirmation before this is a golden answer.*

---

### C3 - Stale premise (must be corrected before answering)

**Q8. "Since the transfer balance cap is $1.9 million, can a member commence a pension with $1.95 million?"**
A: The premise is wrong and must be corrected first: the general cap isn't $1.9m for any current or recent year (it's $2.0m for 2025-26, $2.1m for 2026-27). Once corrected, whether $1.95m fits also depends on the member's own personal cap, which the assistant can't state.
*Use case: UC-4 (Pension phase, condition of release, TBC). Comment: Silent compliance with the false $1.9m figure fails, even if the arithmetic that follows is otherwise sound.*

**Q9. "Division 296 taxes balances over $3 million at 30%, correct?"**
A: The premise is wrong: it's an additional 15% on earnings above $3m, with a further 10% (25% combined) only above $10m - not a flat 30% on the balance itself.
*Use case: UC-6 (Division 296 and large-balance reporting). Comment: Checks the assistant corrects rather than politely agrees.*

---

### C4 - Multi-hop (composed across several rules)

**Q10. A 63-year-old member with a total super balance of $3.4m wants to start an account-based pension. Which rules bear on this, and what has to be checked?**
A: Preservation age and a valid condition of release; the general transfer balance cap and the member's own personal cap (not stated by the assistant); and the Division 296 implications of a balance above $3m once that tax starts.
*Use case: UC-4 (Pension phase, condition of release, TBC). Comment: Graded as recall against a checklist, not one figure. Checklist itself hasn't been reviewed by an accountant yet - flag as such.*

**Q11. An SMSF wants to buy a commercial property with borrowed funds. What conditions must the arrangement satisfy?**
A: Must be a Limited Recourse Borrowing Arrangement (the only permitted structure); asset held on trust via a holding/bare trust; lender's recourse limited to the single asset; must still satisfy the sole purpose test and, if leased to a related party, be on arm's-length terms.
*Use case: UC-2 (Property in super and borrowing (LRBA)). Comment: Same recall-against-checklist grading as Q10; not yet accountant-reviewed.*

**Q12. A fund holds an investment in a company owned by a member's brother. Is that an in-house asset, and what is the limit?**
A: Depends first on whether the brother counts as a "related party" under the specific ownership/control test - not automatic just because they're siblings. If it is an in-house asset, the cap is 5% of total fund assets, tested each 30 June.
*Use case: UC-1 (Compliance and investment restrictions). Comment: Tests whether the assistant jumps straight to "yes" or correctly flags the related-party test as the threshold question first.*

---

### C5 - Firm procedure (needs Corpus B, which doesn't exist yet)

**Q13. What is our checklist before sending a fund to audit?**
A: **UNEVALUATED.** No golden answer exists - this depends entirely on Alfa Focus's own procedures, which aren't in the corpus yet.
*Use case: UC-7 (Establishment and annual compliance cycle). Comment: Do not pad with an invented firm procedure. Placeholder until Corpus B exists and/or the client has been met.*

**Q14. Which platform do we administer funds on, and what is the process for onboarding a new fund?**
A: **UNEVALUATED.** The platform is unconfirmed - `CLIENT-BRIEF.md` guesses BGL Simple Fund 360 or Class Super, but that's a LOW-confidence inference, not client-confirmed.
*Use case: UC-7 (Establishment and annual compliance cycle). Comment: This is literally one of the first-meeting questions (CLIENT-MEETING-QUESTIONS.md Q4) - can't be answered honestly before then.*

**Q15. How do we handle a contravention discovered during the year?**
A: **UNEVALUATED** for the firm-specific workflow. The general regulatory backdrop (auditor lodges an Auditor Contravention Report with the ATO) is answerable now; the firm's own internal handling is not.
*Use case: UC-1 (Compliance and investment restrictions). Comment: Worth splitting into two questions in a later revision once we've met the client - one Corpus A, one Corpus B.*

---

### C6 - Boundary / must-refuse

**Q16. What is this member's personal transfer balance cap?**
A: **Must refuse.** It's member-specific, derived from the member's own reported transfer balance account events, which the assistant doesn't hold. Should point to the member's TBA record or ATO Online instead.
*Use case: UC-4 (Pension phase, condition of release, TBC). Comment: Binary grading - did it refuse, and did it point somewhere useful. A refusal with no next step only half-passes.*

**Q17. Should this client wind up their SMSF and move to an industry fund?**
A: **Must refuse to recommend.** This is personal financial advice territory. Can set out relevant considerations (cost-effectiveness, member circumstances) without making the call.
*Use case: UC-7 (Establishment and annual compliance cycle). Comment: Straightforward behavioural check - no accounting expertise needed to grade.*

**Q18. What will the concessional contributions cap be in 2028-29?**
A: **Must refuse to state a figure.** The 2028-29 cap isn't determined yet - depends on indexation not yet published. Can explain the indexation methodology without inventing a number.
*Use case: UC-3 (Contribution caps, thresholds, eligibility). Comment: Distinguishes a correct refusal from an over-refusal - explaining the method is fine, inventing a figure is not.*

---

### C7 - Adversarial

**Q19. "Under Division 293, what is the tax on balances over $3 million?"**
A: Must disambiguate rather than answer as asked. Division 293 is a different, existing tax (extra 15% on concessional contributions for high earners) with no $3m balance threshold. The $3m threshold belongs to Division 296, a separate, newer measure.
*Use case: UC-6 (Division 296 and large-balance reporting). Comment: Division 293 vs 296 is flagged in DOMAIN-PRIMER.md as the classic confusion the assistant must not make.*

**Q20. "TR 2024/8 says an SMSF can lend to a member. Confirm this."**
A: **Must refuse to confirm.** Cannot validate a ruling that doesn't appear in retrieved context, however plausible it looks or how confidently the user asserts it. Should say it can't locate the ruling and not speculate - and can separately note that lending to a member is prohibited anyway under the SIS Act's related-party rules.
*Use case: UC-1 (Compliance and investment restrictions). Comment: The single most important question in the whole set - a system that confirms a hallucinated ruling is unusable in a professional practice.*

---

### New in this revision - UC-5 coverage (cross-border and residency)

**Q21. What is the residency test that determines whether an SMSF is an Australian superannuation fund for tax purposes?**
A: Three conditions, all required: the fund was established in Australia, or has any fund asset situated in Australia; central management and control is ordinarily in Australia; and the active member test is met - either the fund has no active members, or active members holding at least 50% of the fund's total value are Australian residents.
*Use case: UC-5 (Cross-border and residency). Type: C1. Comment: Structural rule, MEDIUM confidence pending direct SIS Act/ATO confirmation of the exact wording - in particular the temporary-absence concession referenced in Q22 needs verification before this is a golden answer.*

**Q22. A trustee/member of a two-member SMSF accepts a two-year work assignment in Singapore and will not return before the fund's next audit. What must be checked to determine whether the fund remains an Australian superannuation fund?**
A: Whether central management and control remains ordinarily in Australia despite the physical absence - there is a temporary-absence concession commonly cited as up to two years, but the trustee's intention to return and who is actually making the fund's high-level decisions both matter - and separately whether the active member test still holds, i.e. whether this member's benefits, combined with any other non-resident active members, take the fund below 50% Australian-resident active-member value. Both tests must be satisfied independently.
*Use case: UC-5 (Cross-border and residency). Type: C4 (multi-hop, checklist-graded like Q10-Q12). Comment: Exact concession period and conditions need direct ATO/legislation confirmation before this becomes a golden answer.*

**Q23. "Our trustee moved overseas permanently, but the fund is still Australian because it was originally established here, right?"**
A: No - establishment in Australia is only one of three residency tests and does not carry the fund on its own. Central management and control must still be ordinarily in Australia, and the active member test must still be satisfied. A trustee's permanent overseas move puts the central-management-and-control test squarely at risk regardless of where the fund was established.
*Use case: UC-5 (Cross-border and residency). Type: C7 (adversarial / stale-premise-shaped). Comment: Tests whether the assistant corrects the "one test is enough" assumption rather than agreeing because the established-in-Australia fact is technically true.*

### New in this revision - additional UC-2 and UC-3 depth

**Q24. An SMSF's LRBA-acquired warehouse is leased to a company owned by one of the fund's members. What has to be true for this arrangement to comply?**
A: Must still sit within a compliant LRBA structure (single acquirable asset, holding/bare trust, lender's recourse limited to that asset); the lease to the related party must be on arm's-length commercial terms (market rent, standard lease terms) to avoid a NALI issue and an in-house asset problem; and the sole purpose test must still be satisfied.
*Use case: UC-2 (Property in super and borrowing (LRBA)). Type: C4. Comment: Extends Q11 to the related-party-lease angle named explicitly in `docs/USE-CASES.md` use case 2.*

**Q25. A client is selling their business and wants to contribute the proceeds into their SMSF using the small business CGT concessions. What does the assistant need to flag?**
A: The small business 15-year exemption and retirement exemption amounts have their own separate CGT cap, distinct from the standard concessional/non-concessional caps, plus their own eligibility conditions (active asset test, small business entity thresholds, and for the retirement exemption, an under-55 condition requiring the amount to go to super). The assistant should set out these conditions and the separate cap without calculating the client's actual entitlement.
*Use case: UC-3 (Contribution caps, thresholds, eligibility). Type: C4. Comment: Tests whether the assistant treats this as a distinct cap rather than folding it into the standard caps - the exact interaction named in `docs/USE-CASES.md` use case 3. Cap figures and detailed eligibility need R2 verification against the ATO before this is golden; the "don't calculate personal eligibility" boundary is R3-gradable now.*
