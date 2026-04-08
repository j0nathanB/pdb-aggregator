Implementation

Here's everything Claude Code needs, in loading order:

**Architecture (read first):**

1. `mpm_unified_architecture_v4.1.md`
2. `extraction_architecture.md`
3. `gov_source_agent_design.md`

**Handoff briefs (read second):** 4. `claude_code_handoff_steps_1_5.md` (already delivered) 5. `claude_code_handoff_steps_6_plus.md` (new)

**Agent prompts (reference during implementation):** 6. `gov_source_agent.md` 7. `triage_agent_v4.1.md` 8. `country_agent_deep_dive_v4.1.md` 9. `devils_advocate_v4.1.md` 10. `regional_synthesis.md` 11. `executive_agent.md`

**Supporting inputs (reference as needed):** 12. `regional_frameworks.md` 13. `newsletter_assembly_spec.md` 14. `information_culture_classifications.md` 15. Both `REPORT.md` files (media + government extraction data → routing table)

That's 15 documents. The handoff brief tells Claude Code what to build, in what order, and where to find the specs for each component. The architecture doc is the single source of truth when anything conflicts.

revision:

**Read in this order:**

1. `mpm_unified_architecture_v4.1.md` — the single source of truth
2. `claude_code_handoff_steps_1_5.md` + `claude_code_steps_1_5_revision.md` — infrastructure
3. `claude_code_handoff_steps_6_plus.md` — pipeline implementation
4. `extraction_architecture.md` — routing table and pool dispatch
5. `guardian_api_implementation.md` — Publisher API spec
6. `gov_source_agent_design.md` — two-layer integration notes

**Agent prompts** (loaded as templates, not hardcoded): 7. All six prompt files in `prompts/`

**Supporting inputs** (reference as needed): 8. `regional_frameworks.md` 9. `newsletter_assembly_spec.md` 10. `information_culture_classifications.md` 11. Both REPORT.md files (extraction test data → routing table)