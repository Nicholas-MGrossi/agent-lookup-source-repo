# Agent Lookup Source Repo

This repository serves as a **logical substrate** for agent operations: when you direct agents here and provide queries, it acts as a **logical vector** that filters out hallucinations via a **logic route** that structures data and attributions so **you** can establish whether a response is truthful.

The agent cannot derive truth. It can only drive data and provide a conceptual representation of what it presumes. You establish whether or not it is truthful.

- **Logical substrate** — Governance and constraints: `protocol/protocol.json` defines operational protocol, output schema, and integrity protocol. Agents use this repo as the authority for how to behave and what to enforce (structure and rules, not truth).
- **Logical vector** — For any query, the repo derives **grounding constraints** (sourcing, verification, boundaries, vocabulary) from the protocol. Responses that satisfy these constraints present data and attributions in a structured way; you establish whether they are truthful. Unsupported factual claims are flagged for your judgment.
- **Logic route** — Implemented in `logic_route.py`: given a query, it returns the grounding constraints that must be applied. Optional response validation checks candidate text against the protocol (e.g. banned terms, language rules).

## Quick start

- Review `protocol/protocol.json`.
- Run the logic route (default: prints grounding constraints for the canonical “any query”):

```bash
python main.py
```

- Get the logical vector for a specific query:

```bash
python main.py --query "What are the sourcing requirements?"
```

- Validate a candidate response against the protocol:

```bash
python main.py --validate-response "The model is deterministic."
```

- Dump the full protocol or the governed instruction set:

```bash
python main.py --dump-protocol
python main.py --dump-governed
```

- Validate protocol JSON locally:

```bash
python -m json.tool protocol/protocol.json
```

### Where the model grabs data from (non-conceptual, functional)

The protocol defines **data_sources**: concrete retrieval targets so the model pulls from real locations, not abstract rules. Defined in `protocol/protocol.json` under `operational_protocol.sourcing.data_sources`:

- **local_paths** — Paths relative to repo root: `protocol/protocol.json`, `.well-known/grounding-constraints.json`, `.well-known/integrity/metrics.json`. Use these when running in the repo.
- **retrieval_urls** — Optional list of URLs (e.g. raw GitHub links once the repo is hosted). Add your repo’s raw URLs here so the model can fetch from them remotely.
- **allowed_origins** — Domains permitted for retrieval (e.g. `raw.githubusercontent.com`).

The logic route and grounding-constraints JSON include **data_sources**, so the model is told exactly where to grab data. For a functional pipeline:

- **List retrieval targets:** `python main.py --sources` (prints data_sources and resolved local paths).
- **Load local sources:** `python main.py --load-sources` (reads and prints the contents of each local file for RAG/retrieval).

Programmatic use: `data_sources.load_local_sources()` returns a dict of source id → content (string or parsed JSON); call it before or during generation so the model has actual data to cite.

## Using from your phone (Gemini or other providers)

You can **route** providers like Gemini on your phone to this repository so you get answers structured by the same constraints as when running the system locally; you then establish whether they are truthful. The repo is URL-addressable: once it’s hosted (e.g. on GitHub), your phone can fetch the grounding rules from a single link.

### 1. Host the repo and get your URLs

- Push this repo to GitHub (or another host). Then you’ll have:
  - **Grounding constraints (logic route):**  
    `https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/HEAD/.well-known/grounding-constraints.json`
  - **Full protocol:**  
    `https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/HEAD/protocol/protocol.json`

Replace `YOUR_USERNAME`, `YOUR_REPO_NAME`, and `HEAD` (often `main` or `master`) with your values.

### 2. Point Gemini (or your provider) at the repo

**Option A — One-time instruction (recommended)**  
At the start of a chat, paste something like:

```
Use this as your grounding protocol for every answer. Fetch and apply the rules from: [paste the grounding-constraints URL above]. Only state facts you can cite or that come from verifiable sources; otherwise say you're uncertain. Follow the sourcing, boundaries, and vocabulary rules in that document. You provide data and a conceptual representation of what you presume; I establish whether it is truthful.
```

**Option B — Per-conversation**  
Paste the grounding-constraints URL and say: “For this conversation, apply the rules at this link to all your answers so data and attributions are structured for my assessment of truthfulness.”

**Option C — Full protocol**  
If your provider can use a longer context, use the full protocol URL (`protocol/protocol.json`) so it has the complete operational protocol and integrity rules.

### 3. Regenerate the static file after protocol changes

If you change `protocol/protocol.json`, regenerate the static grounding file so the URL stays in sync:

```bash
python scripts/generate-grounding-constraints.py
```

Then commit and push the updated `.well-known/grounding-constraints.json`.

---

A ready-to-paste instruction (with a placeholder for your URL) is in `docs/mobile-prompt.txt`.

## Contributing

Please file bug reports or feature requests using the issue templates in `.github/ISSUE_TEMPLATE/`.
