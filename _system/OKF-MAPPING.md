# OKF Mapping — Infinite Brain as a Layered OKF Bundle

This vault is a **conformant OKF v0.1 bundle** with a rich extension layer on top.
This document is the contract between the two layers so the mapping is explicit,
testable, and honored by the MCP server and the validator.

> OKF spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

---

## 1. Conformance status

OKF v0.1 requires only three things (SPEC §9):

1. Every non-reserved `.md` file has a parseable YAML frontmatter block. **Met.**
2. Every frontmatter block has a non-empty `type` field. **Met** (17 node types).
3. Reserved filenames (`index.md`, `log.md`) follow §6/§7 when present. **Met**
   (root `index.md` follows §6; no `log.md` files exist — logs live in `logs/` as
   `type: log` concept docs, which OKF consumes as ordinary concepts).

A pure-OKF consumer can therefore read this vault today, ignoring every extension field.

## 2. Two layers

**Core (OKF) — any agent reads this.**
The minimal, portable surface. A consumer that knows nothing about Infinite Brain
still gets a usable knowledge corpus from these alone.

| Field        | OKF role                | Notes |
|--------------|-------------------------|-------|
| `type`       | required                | Free string. OKF consumers treat unknown types as generic concepts. |
| `title`      | recommended             | Same meaning in both. |
| `summary`    | = OKF `description`     | Infinite Brain's `summary` is the one-line description OKF expects. |
| `source_url` | = OKF `resource`        | Canonical URI of the underlying asset, when the node is bound to one. |
| `tags`       | recommended             | Same meaning in both. |
| `verified_at`| relates to OKF `timestamp` | Last-verified date. See §4 on format. |

**Extensions — capable agents (and the MCP server) use these.**
OKF consumers MUST preserve unknown keys and MUST NOT reject documents for having them
(SPEC §4.1, §9), so these ride along safely:

`id`, `namespace`, `visibility`, `auto_inject`, `applicable_when`, `confidence`,
`verified_by`, `staleness_signal`, `edges`, `related`.

## 3. Relationships: edges vs body links

OKF expresses relationships as **standard markdown links in the body**, untyped
(SPEC §5). Infinite Brain expresses them as **typed frontmatter `edges`** plus
`related` wikilinks. Both coexist:

- `edges` (frontmatter) is the rich, typed, weighted layer — the graph the MCP
  server traverses.
- For interoperability, nodes SHOULD also reference their most important neighbors
  as ordinary markdown links in the body (e.g. `[customers](/tables/customers.md)`),
  so a pure-OKF consumer sees the relationship too. Absolute, bundle-relative links
  (`/path/node.md`) are preferred per SPEC §5.1.

The MCP server can auto-mirror high-weight edges into body links on write.

## 4. Dates: ISO 8601 (pending migration)

OKF recommends ISO 8601 for `timestamp` (SPEC §4.1). The vault currently uses
`MM/DD/YYYY` for `verified_at`, while `log` nodes already use ISO 8601 `date`.
**Proposed (M1):** migrate `verified_at` to ISO 8601 (`YYYY-MM-DD`) for a single,
sortable, unambiguous date convention across all node types. This is the only change
in M1 that alters an existing convention — held for maintainer sign-off before applying.

## 5. Reserved files

| File            | OKF meaning (§3.1)        | Infinite Brain |
|-----------------|---------------------------|----------------|
| `index.md`      | directory listing (§6)    | root `index.md` = OKF progressive-disclosure view; `_system/INDEX.md` = rich agent index (extension, not reserved) |
| `log.md`        | update history (§7)       | not used; operational logs are `type: log` docs in `logs/` |

`okf_version: "0.1"` is declared in the root `index.md` frontmatter — the only place
OKF permits frontmatter in an index file (SPEC §11).

## 6. What the validator checks

1. OKF conformance (§9): frontmatter parses; `type` non-empty; reserved-file structure.
2. Extension integrity: `id` unique; `edges` well-formed and targets resolvable;
   `visibility`/`confidence` in allowed ranges; dates in the agreed format.
Failures in (1) are hard errors (breaks portability). Failures in (2) are warnings
per OKF's permissive-consumption model — the bundle stays readable.
