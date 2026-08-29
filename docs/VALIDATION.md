# Wireframe validation

Team 83, Alfa Focus Knowledge Assistant.
Validated by Ronith Mugundakumar (requirements owner), 2026-08-21.
Baseline: [`REQUIREMENTS.md`](REQUIREMENTS.md).

## Scope

Validated the UX wireframe set against every requirement in REQUIREMENTS.md that has a screen surface. Requirements that are behavioural, contractual, or process-level are listed in section 6 and are not judged here.

Artboards reviewed:

| # | Artboard |
|---|---|
| 01 | Main chat interface |
| 02 | Document upload page |
| 03 | Chat loading and no-answer states |

Artboard 03 was added in the revision. The first version of the set had two artboards.

## Result

**Validated.** Both screens address the requirements listed in REQUIREMENTS.md sections 4, 5 and 7.

Round one raised 12 change requests, 5 of which blocked acceptance. All 12 were addressed in the revision. Three minor items remain open and are recorded in section 5; none of them blocks build.

## 1. Round one and what changed

| CR | Requirement | Issue raised | Resolution in revision |
|---|---|---|---|
| CR-1 | UP-2 | Upload captured no metadata. Files went straight from drop to the document table. | Two step flow added. Step 2 requires source type (official source or internal firm procedure) with no default, and an applies-from date. Upload stays disabled until both are set. |
| CR-2 | DH-3 | Composer helper text read "Responses may reference uploaded documents." The requirement needs a client identifier warning in that position. | Replaced with "Do not enter client names, TFNs, member numbers or other identifying information", fixed under the composer. Artboard 03 confirms it persists in every state. |
| CR-3 | CH-6, CH-10, CH-11, CH-15, CH-16, CH-17, EC-12 | No not-found state, no refusal state, no outage state. The set designed only the path where the assistant answers. | Artboard 03 added with four mutually exclusive states: no match in documents, outside SMSF scope, refused for privacy or advice, system unavailable. |
| CR-4 | UP-3, UP-4, UP-5 | Statuses were `Processed` and `Uploaded`, which are indistinguishable in meaning. No failure or supersede state. | Four statuses: Processing, Processed, Failed, Superseded. Failure reason shown inline on the row. |
| CR-5 | UP-5, UP-6 | Row overflow menu present but contents undefined. | Menu specified: view document, remove from search, upload new version. |
| CR-6 | CH-2, CH-3, CH-8 | Answer body was a single paragraph. CH-2 requires law and firm procedure never be combined in one sentence. | Answer card split into "Legal position" and "How Alfa Focus handles it" as separate labelled sections. |
| CR-7 | CH-4 | No income year on the answer. | Income year badge added to the answer card header. |
| CR-8 | UP-8, DH-5 | No signed-in user, no sign out, no visible evidence either page sits behind authentication. | Signed-in user and role shown in the rail on both screens, with a sign out control. |
| CR-9 | NF-1 | No state between send and answer. | Loading state added, naming what is being checked. |
| CR-10 | UP-2, UP-8 | Composer attachment icon was a second ingest path that bypassed metadata capture and authorisation. | Removed. Upload is now a single governed path. |
| CR-11 | Client fidelity | Sample content was general financial accounting. The client is SMSF only. | Recast to SMSF throughout. Product renamed to Alfa Focus SMSF Assistant. |
| CR-12 | UP-2 | `Type` column held file format, easy to mistake for corpus. | Renamed to `Format`. `Source Type` and `Applies From` added as separate columns. |

## 2. Chat interface, artboards 01 and 03

| ID | P | Requirement surface | Where it is met |
|---|---|---|---|
| CH-1 | M | Citations openable from the response | Sources block lists each source separately with its own open control. Sources are prefixed by corpus (ATO, Alfa Focus), which maps them to the answer sections above. |
| CH-2 | M | Law and firm procedure in distinct labelled sections | Two labelled regions in the answer card: "Legal position" and "How Alfa Focus handles it". |
| CH-3 | S | Firm procedure shown alongside the legal position | Second region is part of the standard answer card, not an optional extra. |
| CH-4 | M | Income year stated where correctness depends on it | Income year badge on the answer card header, plus the year in the answer body. |
| CH-6 | M | Says so where no source supports an answer | No-match state on artboard 03. |
| CH-8 | S | Consistent answer structure | Fixed region order across the answer card: header and year, legal position, firm procedure, sources. |
| CH-10 | M | States plainly it could not find an answer, no hedging | No-match state reads "I couldn't find this in the approved documents", with no speculative content. |
| CH-11 | M | Distinguishes no source from out of scope | Two visually separate states on artboard 03, different colour treatment and different copy. |
| CH-13 | S | Gives a next step | Each no-answer state carries a suggested next action. |
| CH-15 | M | Does not state member specific figures | Refusal state covers member and client specific questions. |
| CH-16 | M | Does not recommend a course of action for a member | Same refusal state, directing to the approved client advice workflow. |
| CH-17 | S | Refusals follow a consistent format | All four non-answer states share one card frame, so they read as a family. |
| DH-3 | M | Warns against client identifiers at the point of entry | Warning fixed under the composer, present in every state. |
| DH-5 | M | Only authenticated users reach the assistant | Signed-in user and sign out control in the rail. |
| DH-7 | S | Questions and answers retained | Recent conversations list in the rail. |
| EC-1 | M | Out of subject area handled and distinguished from a missing source | Outside scope state, separate from the no-match state. |
| EC-12 | M | Plain failure message, never a partial or unsourced answer | System unavailable state states the question was not processed and that no answer or sources can be shown. |
| NF-1 | S | Answer arrives quickly enough that the user waits | Loading state names what is being checked, so the wait is legible. |
| NF-2 | M | Usable with a short walkthrough | Conventional chat layout, one primary action per screen. |

## 3. Document upload, artboard 02

| ID | P | Requirement surface | Where it is met |
|---|---|---|---|
| UP-1 | M | Upload and index without developer involvement | Drag and drop plus browse, reachable from the rail. |
| UP-2 | M | Corpus and applies-from captured at upload | Step 2 of the upload flow. Source type has no default. Both fields required, upload disabled until complete. |
| UP-3 | M | Uploader sees processing, succeeded or failed | Status column with Processing, Processed, Failed. |
| UP-4 | S | Failure states why in actionable terms | Reason shown on the row, for example "scanned PDF has no readable text". |
| UP-5 | S | New version supersedes rather than deletes | Superseded status, with the row noting it is retained for historical questions. |
| UP-6 | S | Documents listed, individual document withdrawn from search | Document table plus a per row menu with remove from search. |
| UP-8 | M | Only authorised firm users can upload | Signed-in user shown in the rail. Role gating itself is open, see section 5. |
| DH-5 | M | Only authenticated users reach any page | Same rail treatment as the chat screen. |

## 4. Edge cases with a screen surface

| ID | P | Required behaviour | Where it is met |
|---|---|---|---|
| EC-1 | M | Say so, and distinguish from a missing source | Outside scope state. |
| EC-7 | S | Answer without repeating a client identifier | Composer warning is preventive. The refusal state covers the case where one is entered anyway. |
| EC-12 | M | Plain failure message | System unavailable state. |

## 5. Open items

None of these block build. All three are recorded so they are picked up during implementation rather than found in review.

**1. No changed-rule flag on the answer card.** CH-5, EC-2 and EC-10 require an answer to say when it rests on a rule that has changed or a source that predates a known change. The income year badge landed, this marker did not. The document model now supports superseded sources, so an answer can be built on stale material with nothing on the card saying so. This is the only gap of the three that has a requirement behind it at `S` priority or above.

**2. The no-match state does not say what was searched.** CH-12 asks the response to name what was searched and how current that material is, so the user can tell a coverage gap from a currency gap. The current copy says there is not enough approved material, which does not separate the two.

**3. The refusal state does not name where the figure is held.** CH-15 requires the assistant to name where a member specific figure lives rather than only declining. The state directs to the client advice workflow, which is a next step but not an answer to "so where do I get the balance".

Two smaller notes for build:

- Remove from search is styled as a destructive action in the row menu. The wording is correct but the treatment reads as delete, and UP-5 depends on users understanding those documents are kept.
- There is no not-permitted variant of the Documents page. UP-8 and DH-6 are evidenced by the signed-in user but the nav entry is unconditional, so role gating remains an assumption. See section 7.

## 6. Not judged in this validation

Listed so their absence is not read as coverage. Verification for these sits in [`TRACEABILITY.md`](TRACEABILITY.md).

| Requirements | Why not judged here | Verified by |
|---|---|---|
| CH-7, DH-2, DH-4, EC-4, EC-5, EC-6, EC-8, EC-9, EC-11 | Model behaviour with no screen surface | [`EVALUATION.md`](EVALUATION.md) |
| DH-1, DH-8, DH-9 | Contractual, retention policy, and configuration | Client agreement and repository configuration |
| NF-3, NF-4, NF-5, NF-6, NF-7 | Process and non-functional | Evaluation harness and handover documentation |
| CH-9, UP-7 | `C` priority, out of current scope | Deferred |

## 7. Assumptions still open

REQUIREMENTS.md marks these `[ASSUMED]` pending the first client meeting. The wireframes do not resolve them and should not be read as having done so.

| Assumption | Requirements affected | Effect on the design |
|---|---|---|
| Who may upload | UP-8, DH-5 | The Documents page currently shows one permission state. A restricted variant is needed once roles are confirmed. |
| Who may see firm procedure content | DH-6, DH-10 | Answer cards show the firm procedure section unconditionally. If access is role limited, that section needs a hidden state. |
| Retention period for questions and answers | DH-7, DH-8 | Recent conversations implies retention. No period is stated anywhere in the interface. |

Flag these at the client meeting rather than designing roles into the interface ahead of an answer.

## 8. Sign-off

The wireframes are validated against REQUIREMENTS.md as at 2026-08-21 and are cleared for build.

Validation confirms the requirements have been designed for. It does not confirm they are met. Rows in sections 2 to 4 should be read as designed for, and the corresponding rows in [`TRACEABILITY.md`](TRACEABILITY.md) stay unverified until there is a running system to test.
