---
id: pillar-example-philosophy
title: Decisions Should Be Deliberate and Recorded
type: pillar
namespace: default
visibility: public
summary: The founding principle that deliberate, recorded decisions outperform ad-hoc reactions over time, especially as organizations scale and context fragments.
auto_inject: false
applicable_when: "Empty"
confidence: 1.0
verified_at: 05/11/2026
verified_by: System Bootstrap
staleness_signal: If the organization dissolves or this vault is archived, mark as historical
tags: ["core-philosophy", "decision-making", "institutional-memory", "knowledge-management"]
edges: [
  {"target": "decision-example-action", "type": "supports", "weight": 0.9, "note": "The decision exemplifies the principle of deliberate action recorded in writing"}
]
related: ["[[decision-example-action]]"]
source_url: "Empty"
---

# Decisions Should Be Deliberate and Recorded

## Why This Pillar Exists

In fast-moving organizations, the default mode is reaction. Someone asks a question, a meeting produces an answer, and within a week nobody can remember why a particular choice was made. Context decays. New team members inherit contradictory precedents. The same debates repeat themselves endlessly.

This pillar asserts that **time spent recording the reasoning behind a decision is not overhead — it is leverage**. The marginal cost of writing a decision record is small; the cost of not having it when context is needed is large and often paid by someone else.

## What "Deliberate" Means

A deliberate decision is one where the following are explicit:

- **The problem being solved.** Not just the symptom or the surface request, but the underlying need.
- **Alternatives considered.** At minimum, what else was on the table and why it was rejected.
- **The criteria for choice.** What inputs, values, or constraints drove the selection.
- **The expected outcome.** Not a guarantee, but the hypothesis being acted on.
- **Conditions for reversal.** What would cause this decision to be revisited.

Deliberate does not mean slow. A five-minute writeup in a decision node is enough for most operational choices. The point is not formality — it is traceability.

## What "Recorded" Means

Recording means placing the decision in the vault with a structured frontmatter and a body that explains the reasoning. It does not mean a lengthy document. The ideal decision node:

- Can be read in under two minutes.
- Captures enough context for someone who was not in the room.
- Links to supporting evidence (facts, sources, hypotheses).
- Names the decision-maker or team for accountability.

Recording also means making the decision retrievable — stored with an appropriate `namespace`, tagged for topical access, and wired to related nodes via edges.

## Relationship to Other Nodes

This pillar is the root of a knowledge subgraph. It is supported by:

- **Decision nodes** that embody the principle in practice.
- **Pattern nodes** that describe recurring decision shapes.
- **Fact nodes** that provide evidential grounding for decisions.
- **Playbook nodes** that operationalize decision outcomes.

The pillar itself does not change often. When it does, the ripple effect touches every downstream node. Treat it as load-bearing.

## Implications for Vault Behavior

Every agent and human operating within this vault should:

1. Default to creating a decision node before taking significant action.
2. Fill in all required frontmatter fields — especially `staleness_signal`.
3. Wire decisions to pillars that justify them, using the `supports` edge type.
4. Revisit decision nodes when their staleness signal is triggered.

---

*This pillar was bootstrapped as part of the initial vault scaffolding on 05/11/2026.*
