---
name: thermo-nuclear-code-review
description: Unusually strict code-quality review of the current branch's changes (or a given PR / branch / path) - implementation quality, maintainability, abstraction quality, codebase health. Hunts for "code judo" restructurings that keep behaviour and delete complexity. Use when the user invokes /thermo-nuclear-code-review or asks for a thermo-nuclear / brutal / no-mercy quality review.
argument-hint: "[PR number | branch | path | (blank = current branch vs base)]"
---

# Thermo-Nuclear Code Quality Review

An unusually strict review focused on implementation quality, maintainability, abstraction quality,
and codebase health. Above all, be ambitious about code structure. Do not merely identify local
cleanup opportunities. Actively search for "code judo" moves: restructurings that preserve behaviour
while making the implementation dramatically simpler, smaller, more direct, and more elegant.

## Step 0 - scope the review (do this before reading code)

1. Resolve the target from `$ARGUMENTS`:
   - blank: the current branch. Diff `origin/ddp-prod...HEAD` in a `novopay-platform-*` / `trustt-platform-*`
     repo (workspace rule: baseline is always `origin/ddp-prod`); otherwise the repo's default branch. Include
     uncommitted changes (`git diff HEAD` + untracked files) - the user often reviews before committing.
   - a PR number: `gh pr diff <n>` and `gh pr view <n> --json files,title,body`.
   - a branch: `git diff <default-base>...<branch>`.
   - a path: `git diff` restricted to that path, plus its current contents.
2. List every changed file with its line count **before** and **after** (`git show <base>:<file> | wc -l` vs
   `wc -l <file>`). Any file that crosses 1000 lines because of this change is a presumptive blocker (rule 2).
3. Read each changed file in full, not just the hunks. The review is about the code the diff leaves behind,
   not the diff in isolation. For each changed function, read its callers and the canonical helpers in the
   same package so you can tell a bespoke one-off from a reuse.
4. Read the repo's `docs/design-patterns.md` and `docs/project-overview.md` when present, and the workspace
   `CLAUDE.md` coding standards. "Canonical layer" and "existing helper" in the rules below mean *these*.

Do not run the build or tests as part of this skill unless the user asks; this is a design review.

## Core prompt

Perform a deep code quality audit of the changes. Rethink how to structure / implement the changes to
meaningfully improve code quality without impacting behaviour. Work to improve abstractions, modularity,
reduce spaghetti code, improve succinctness and legibility. Be ambitious: if there is a clear path to
improving the implementation that involves restructuring some of the codebase, go for it. Be extremely
thorough and rigorous. Measure twice, cut once.

## Non-negotiable standards

1. **Be ambitious about structural simplification.** Do not stop at "this could be a bit cleaner". Look for
   reframings where whole branches, helpers, modes, conditionals, or layers disappear. Prefer the solution
   that makes the code feel inevitable in hindsight. Assume a code-judo move is often available: a
   reorganisation that uses the existing architecture more effectively. If complexity can be deleted rather
   than rearranged, push hard for that.
2. **Do not let a change push a file from under 1000 lines to over 1000 lines** without a very strong reason.
   Treat it as a strong smell. Prefer extracting helpers, subcomponents, modules, or local abstractions. If
   the diff crosses the threshold, explicitly ask whether the code should be decomposed first. Waive only for
   a compelling structural reason and only if the resulting file is still clearly organised.
3. **Do not allow random spaghetti growth.** Be highly suspicious of new ad-hoc conditionals, scattered
   special cases, or one-off branches inserted into unrelated flows. "Weird if statements in random places"
   are a design problem, not a stylistic nit. Push the logic into a dedicated abstraction, helper, state
   machine, policy object, or module instead of tangling an existing path. Call out changes that make the
   surrounding code harder to reason about even if they technically work.
4. **Bias toward cleaning the design, not just accepting working code.** If behaviour can stay the same while
   the structure becomes meaningfully cleaner, push for the cleaner version. Do not rubber-stamp "it works".
   Prefer simplifications that remove moving pieces over refactors that spread the same complexity around.
5. **Prefer direct, boring, maintainable code over hacky or magical code.** Brittle, ad-hoc, or "magic"
   behaviour is a quality problem. Be skeptical of generic mechanisms that hide simple data-shape assumptions.
   Flag thin abstractions, identity wrappers, and pass-through helpers that add indirection without clarity.
6. **Push hard on type and boundary cleanliness.** Question unnecessary optionality, `Object`, raw types,
   unchecked casts, `@Nullable` sprinkled to silence NullAway, `Map<String,Object>` blobs, `any` / `unknown`,
   when a clearer typed boundary could exist. Prefer explicit typed models or shared contracts over
   loosely-shaped ad-hoc objects. If a branch relies on silent fallback to paper over an unclear invariant,
   ask whether the boundary should be made explicit instead.
7. **Keep logic in the canonical layer and reuse existing helpers.** Call out feature logic leaking into shared
   paths or implementation details leaking through APIs. Prefer existing canonical utilities over bespoke
   one-offs. Push code toward the right package, service, or module instead of normalising drift.
8. **Treat unnecessary sequential orchestration and non-atomic updates as design smells** when the cleaner
   structure is obvious. If independent work is serialised for no reason, ask whether it should run in
   parallel. If related updates can leave state half-applied, push for an atomic structure. Do not
   micro-optimise, but flag avoidable orchestration complexity that makes the implementation brittle.

## Primary review questions (ask for every meaningful change)

- Is there a code-judo move that would make this dramatically simpler?
- Can the change be reframed so fewer concepts, branches, or helper layers are needed?
- Does it improve or worsen the local architecture?
- Did it add branching complexity where a better abstraction should exist?
- Did a previously cohesive module become more coupled, more stateful, or harder to scan?
- Is the logic living in the right file and layer?
- Did it enlarge a file or component past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or helper?
- Is the implementation direct and legible, or does it rely on special cases and incidental control flow?
- Is each abstraction earning its keep, or is it just a wrapper?
- Did it introduce casts, optionality, or ad-hoc object shapes that obscure the real invariant?
- Did details leak across a boundary that should have stayed canonical?
- Is the orchestration more sequential or less atomic than it needs to be?

## What to flag aggressively

- A complicated implementation where a cleaner reframing could delete whole categories of complexity.
- Refactors that move code around without reducing the number of concepts a reader must hold.
- A file crossing 1000 lines because of the change, especially if the new code could be split out.
- New conditionals bolted onto unrelated code paths.
- One-off booleans, nullable modes, or flags that complicate existing control flow.
- Feature-specific logic leaking into general-purpose modules.
- Generic "magic" handling that hides simple structure.
- Thin wrappers or identity abstractions.
- Unnecessary casts, raw types, `Object`, optional params that muddy the real contract.
- Copy-pasted logic instead of an extracted helper.
- Narrow edge-case handling implemented in the middle of an already busy function.
- Refactors that pass tests but make the code less modular or less readable.
- "Temporary" branching that will become permanent debt.
- Bespoke helpers where the codebase already has a canonical utility.
- Logic in the wrong layer/package when there is a clear canonical home.
- Sequential async flow where independent work would be simpler in parallel.
- Partial-update logic that leaves state less atomic than necessary.

## Preferred remedies

Delete a layer of indirection rather than polishing it. Reframe the state model so conditionals disappear
instead of getting centralised. Change the ownership boundary so the feature becomes a natural extension of
an existing abstraction. Turn special cases into a simpler default flow. Extract a helper or pure function.
Split a large file into focused modules. Move feature-specific logic behind its own abstraction. Replace
condition chains with a typed model or explicit dispatcher. Separate orchestration from business logic.
Collapse duplicate branches. Delete wrappers that do not clarify. Reuse the canonical helper. Make type
boundaries explicit so control flow simplifies. Move logic to the module that already owns the concept.
Parallelise independent work when that also simplifies. Make related updates atomic.

Do not settle for "maybe rename this" when the real issue is structural. Do not settle for a cleaner
version of the same messy idea when a much simpler idea is plausible.

## Tone

Direct, serious, demanding. Not rude, but do not soften major maintainability issues into mild
suggestions. If the code makes the codebase messier, say so. If it missed a dramatic simplification, say so.
Phrases that fit: "this pushes the file past 1k lines - can we decompose this first?", "this adds another
special-case branch into an already busy flow - can we move it behind its own abstraction?", "this works,
but it makes the surrounding code more spaghetti - keep the behaviour, restructure the implementation",
"this abstraction seems unnecessary - can we keep the direct flow?", "why does this need a cast / optional
here? can we make the boundary explicit instead?", "i think there's a code-judo move here that makes this
much simpler".

## Output

Write the review as a single message the author can act on without the transcript:

1. **Verdict** first: `APPROVE`, `APPROVE WITH CHANGES`, or `BLOCK`, with one sentence of why.
2. **Findings**, ordered by this priority, a small number of high-conviction items rather than a long
   list of nits:
   1. structural code-quality regressions
   2. missed opportunities for dramatic simplification / code-judo restructuring
   3. spaghetti / branching complexity increases
   4. boundary / abstraction / type-contract problems
   5. file-size and decomposition concerns
   6. modularity and abstraction issues
   7. legibility and maintainability concerns
   Each finding: `file:line`, what is wrong in one sentence, why it matters, and the concrete remedy
   (sketch the restructured shape in a few lines of code when that is clearer than prose).
3. **File-size table** for any file within 200 lines of, or over, the 1000-line boundary after the change.
4. **What is good** - briefly, only what is genuinely worth keeping as a pattern.

Do not flood the review with low-value nits when larger structural issues exist. Do not apply fixes;
this skill reviews. If the user then asks to apply a finding, do it as a separate change.

## Approval bar

Do not approve merely because behaviour seems correct. Approve only when there is:

- no clear structural regression
- no obvious missed opportunity to make the implementation dramatically simpler when such a path is visible
- no unjustified file-size explosion
- no obvious spaghetti growth from special-case branching
- no hacky or magical abstraction that makes the code harder to reason about
- no unnecessary wrapper / cast / optionality churn obscuring the real design
- no clear architecture-boundary leak or avoidable canonical-helper duplication
- no missed obvious decomposition that would materially improve maintainability

Presumptive blockers unless the author justifies them clearly:

- a lot of incidental complexity preserved when a plausible code-judo move would delete it
- a file pushed from below 1000 lines to above 1000 lines
- ad-hoc branching that makes an existing flow more tangled
- a local problem solved by scattering feature checks across shared code
- an unnecessary abstraction, wrapper, or cast-heavy contract that makes the design more indirect
- a duplicated helper, or logic in the wrong layer when there is a clear canonical home

If those conditions are not met, leave explicit, actionable feedback and push for a cleaner decomposition.
