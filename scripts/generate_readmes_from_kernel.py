#!/usr/bin/env python3
"""Generate canonical README instructions from KERNEL.md meanings."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTANCE = ROOT / "examples" / ".archeia"


def load_kernel() -> str:
    cached = Path("/tmp/KERNEL.md")
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    result = subprocess.run(
        ["git", "show", "0cc4585^:KERNEL.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_domains(kernel: str) -> dict[str, dict]:
    domains: dict[str, dict] = {}
    chunks = re.split(r"\n### 4\.\d+ ", kernel)
    for chunk in chunks[1:]:
        header, _, body = chunk.partition("\n\n")
        domain_m = re.match(r"`(strategy|operations|product|growth)/`", header.strip())
        if not domain_m:
            continue
        domain = domain_m.group(1)
        canonical_m = re.search(r"\*\*Canonical meaning\.\*\* (.+)", body)
        broad_m = re.search(r"\*\*Broader semantic envelope\.\*\* (.+)", body)
        belongs_m = re.search(
            r"\*\*What belongs here\.\*\*\n\n((?:- .+\n)+)", body
        )
        not_m = re.search(
            r"\*\*What does not belong here\.\*\*\n\n((?:- .+\n)+)", body
        )
        if not all([canonical_m, broad_m, belongs_m, not_m]):
            continue
        domains[domain] = {
            "canonical": canonical_m.group(1).strip(),
            "broad": broad_m.group(1).strip(),
            "belongs": [line[2:].strip() for line in belongs_m.group(1).strip().splitlines()],
            "not_belongs": [line[2:].strip() for line in not_m.group(1).strip().splitlines()],
        }
    return domains


def parse_section6(kernel: str) -> dict[str, dict]:
    meanings: dict[str, dict] = {}
    chunks = re.split(r"\n### 6\.\d+ ", kernel)
    for chunk in chunks[1:]:
        header, _, body = chunk.partition("\n\n")
        path_raw = header.strip().strip("`")
        path_raw = path_raw.replace("Universal `", "").replace("`", "").strip("/")
        canonical_m = re.search(r"\*\*Canonical meaning\.\*\* (.+)", body)
        broad_m = re.search(r"\*\*Broad interpretation\.\*\* (.+)", body)
        if not canonical_m or not broad_m:
            continue
        meanings[path_raw] = {
            "canonical": canonical_m.group(1).strip(),
            "broad": broad_m.group(1).strip(),
            "universal": path_raw in {"decisions", "conventions", "learnings"},
        }
    return meanings


SUPPLEMENTARY: dict[str, dict[str, str]] = {
    "strategy/landscape": {
        "canonical": "External landscape evidence: competition, industry, and market context for strategic direction.",
        "broad": "Can include competitor snapshots, industry trend notes, market sizing, or other accumulating landscape intelligence that informs direction without being product-local.",
    },
    "strategy/landscape/competition": {
        "canonical": "Competitive landscape evidence for strategic direction.",
        "broad": "Can include competitor profiles, feature comparisons, positioning notes, and other accumulating competitive intelligence.",
    },
    "strategy/landscape/industry": {
        "canonical": "Industry landscape evidence for strategic direction.",
        "broad": "Can include industry trends, regulatory context, technology shifts, and other accumulating industry intelligence.",
    },
    "strategy/landscape/market": {
        "canonical": "Market landscape evidence for strategic direction.",
        "broad": "Can include market sizing, segment analysis, demand signals, and other accumulating market intelligence.",
    },
    "product/strategy": {
        "canonical": "Product strategy: how the product is positioned, sequenced, and measured.",
        "broad": "Can include product roadmap, user understanding, market positioning, and product-level metrics that shape what gets built.",
    },
    "product/strategy/roadmap": {
        "canonical": "Product roadmap sequencing and delivery contract surface.",
        "broad": "Can represent feature sequencing, release planning, or product initiative ordering that execution surfaces rely on.",
    },
    "product/strategy/users": {
        "canonical": "User and audience understanding for product decisions.",
        "broad": "Can include personas, user research summaries, jobs-to-be-done, and accumulating evidence about who the product serves.",
    },
    "product/strategy/metrics": {
        "canonical": "Product success metrics and measurement posture.",
        "broad": "Can include north-star metrics, KPI definitions, instrumentation plans, and how product success is evaluated.",
    },
    "product/design": {
        "canonical": "Design surface: interaction, visual, and experience contracts.",
        "broad": "Can include flows, prototypes, feedback, and assets that shape how the product is experienced.",
    },
    "product/design/flows": {
        "canonical": "User flows and interaction sequences.",
        "broad": "Can include journey maps, flow diagrams, state transitions, and durable interaction contracts.",
    },
    "product/design/feedback": {
        "canonical": "Accumulating design feedback and review records.",
        "broad": "Can include critique notes, usability findings, stakeholder feedback, and design review outcomes.",
    },
    "product/design/assets": {
        "canonical": "Durable design assets and references.",
        "broad": "Can include icons, illustrations, brand elements, and binary design files with descriptive sidecars.",
    },
    "product/technical": {
        "canonical": "Technical context: specs, architecture evidence, studies, and developer-facing truth.",
        "broad": "Can include executable specs, C4 models, architecture views, technical studies, and dev environment notes.",
    },
    "product/technical/architecture": {
        "canonical": "Architecture evidence and analysis for the product.",
        "broad": "Can include C4 models, rendered views, repository analysis, and other machine- or human-readable architecture truth.",
    },
    "product/technical/architecture/c4": {
        "canonical": "Machine-readable C4 architecture evidence (contract surface).",
        "broad": "JSON C4 elements with file-path evidence pointing to real source files. Used for product feasibility review and operations scoping.",
    },
    "product/technical/architecture/analysis": {
        "canonical": "Architecture analysis and repository intelligence.",
        "broad": "Can include dependency analysis, history scans, codebase models, and consolidated technical assessments.",
    },
    "product/technical/architecture/views": {
        "canonical": "Rendered architecture views derived from evidence.",
        "broad": "Can include Mermaid diagrams, C4 renders, and other human-readable views of the architecture model.",
    },
    "product/technical/studies": {
        "canonical": "Accumulating technical studies and research.",
        "broad": "Can include spikes, feasibility studies, performance investigations, and technical exploration records.",
    },
    "product/technical/devs": {
        "canonical": "Developer environment and workflow context.",
        "broad": "Can include local setup guides, dev tooling conventions, environment notes, and developer onboarding context.",
    },
    "product/execution": {
        "canonical": "Product-owned execution surface.",
        "broad": "Can include PRDs, execution plans, logs, retros, roles, and archived product delivery artifacts.",
    },
    "product/execution/prds": {
        "canonical": "Integrated buildable product missions (contract surface).",
        "broad": "Can include PRDs, build briefs, and integrated product missions that execution surfaces scope and deliver against.",
    },
    "product/execution/plans": {
        "canonical": "Transient product execution plans.",
        "broad": "Can include sprint plans, release plans, and active delivery plans with lifecycle status.",
    },
    "product/execution/retros": {
        "canonical": "Accumulating product execution retrospectives.",
        "broad": "Can include sprint retros, release retros, and delivery reflection records.",
    },
    "product/execution/logs": {
        "canonical": "Accumulating product execution logs.",
        "broad": "Can include delivery journals, standup notes, and chronological execution records.",
    },
    "product/execution/roles": {
        "canonical": "Product delivery roles and responsibilities.",
        "broad": "Can include RACI definitions, agent role boundaries, and who owns what in product delivery.",
    },
    "product/execution/archive": {
        "canonical": "Archived product execution artifacts.",
        "broad": "Can include completed PRDs, shipped plans, and retired delivery records kept for reference.",
    },
    "operations/execution/tasks": {
        "canonical": "Transient operations-owned tasks.",
        "broad": "Can include support tickets, operational to-dos, and active operations work items with lifecycle status.",
    },
    "operations/execution/projects": {
        "canonical": "Transient operations-owned projects.",
        "broad": "Can include internal improvement projects, support initiatives, and bounded operations efforts.",
    },
    "operations/execution/plans": {
        "canonical": "Transient operations execution plans.",
        "broad": "Can include operational sprint plans, rollout plans, and active operations scheduling artifacts.",
    },
    "operations/execution/retros": {
        "canonical": "Accumulating operations execution retrospectives.",
        "broad": "Can include operations retros, post-incident reviews, and reflection on operational delivery.",
    },
    "growth/strategy": {
        "canonical": "Growth strategy: positioning, segments, channels, and metrics.",
        "broad": "Can include growth roadmap, segment definitions, channel mix, pricing strategy, and adoption metrics.",
    },
    "growth/strategy/roadmap": {
        "canonical": "Growth initiative sequencing.",
        "broad": "Can represent GTM sequencing, campaign calendars, or adoption rollout ordering.",
    },
    "growth/strategy/segments": {
        "canonical": "Audience and market segment definitions.",
        "broad": "Can include ICP definitions, segment prioritization, and targeting criteria.",
    },
    "growth/strategy/positioning": {
        "canonical": "Market positioning and differentiation.",
        "broad": "Can include positioning statements, competitive framing, and value proposition articulation.",
    },
    "growth/strategy/metrics": {
        "canonical": "Growth and adoption metrics.",
        "broad": "Can include funnel metrics, acquisition KPIs, retention targets, and growth measurement posture.",
    },
    "growth/strategy/channel-mix": {
        "canonical": "Channel strategy and mix decisions.",
        "broad": "Can include channel prioritization, budget allocation across channels, and channel experiment results.",
    },
    "growth/strategy/pricing": {
        "canonical": "Pricing and packaging strategy.",
        "broad": "Can include pricing models, packaging tiers, and monetization strategy.",
    },
    "growth/marketing": {
        "canonical": "Marketing systems and programs.",
        "broad": "Can include brand, messaging, campaigns, content, web, inbound/outbound, community, and events.",
    },
    "growth/marketing/brand": {
        "canonical": "Brand identity and guidelines.",
        "broad": "Can include brand voice, visual identity, and brand governance.",
    },
    "growth/marketing/messaging": {
        "canonical": "Messaging frameworks and copy guidance.",
        "broad": "Can include taglines, value props, messaging hierarchies, and copy standards.",
    },
    "growth/marketing/assets": {
        "canonical": "Marketing assets and collateral.",
        "broad": "Can include images, videos, decks, and reusable marketing materials.",
    },
    "growth/marketing/style": {
        "canonical": "Marketing style and design standards.",
        "broad": "Can include typography, color usage, layout rules, and visual style guides.",
    },
    "growth/marketing/campaigns": {
        "canonical": "Campaign definitions and plans.",
        "broad": "Can include campaign briefs, timelines, and channel-specific campaign plans.",
    },
    "growth/marketing/content": {
        "canonical": "Content strategy and editorial plans.",
        "broad": "Can include content calendars, editorial guidelines, and content pillar definitions.",
    },
    "growth/marketing/web": {
        "canonical": "Web presence and digital marketing surface.",
        "broad": "Can include landing page specs, SEO posture, and web conversion strategy.",
    },
    "growth/marketing/inbound": {
        "canonical": "Inbound marketing programs.",
        "broad": "Can include SEO, content marketing, lead magnets, and organic acquisition programs.",
    },
    "growth/marketing/outbound": {
        "canonical": "Outbound marketing programs.",
        "broad": "Can include paid ads, outreach campaigns, and proactive demand generation.",
    },
    "growth/marketing/community": {
        "canonical": "Community building and engagement.",
        "broad": "Can include community platforms, engagement programs, and ambassador initiatives.",
    },
    "growth/marketing/events": {
        "canonical": "Events and experiential marketing.",
        "broad": "Can include conferences, webinars, meetups, and event playbooks.",
    },
    "growth/sales": {
        "canonical": "Sales motions and pipeline systems.",
        "broad": "Can include outbound, pipeline management, accounts, enablement, objections, pricing, and win-loss records.",
    },
    "growth/sales/outbound": {
        "canonical": "Outbound sales motions and sequences.",
        "broad": "Can include prospecting playbooks, outreach templates, and outbound cadences.",
    },
    "growth/sales/pipeline": {
        "canonical": "Sales pipeline management.",
        "broad": "Can include pipeline stages, forecasting, and deal progression rules.",
    },
    "growth/sales/accounts": {
        "canonical": "Account management and relationships.",
        "broad": "Can include account plans, relationship maps, and key account strategies.",
    },
    "growth/sales/enablement": {
        "canonical": "Sales enablement materials and training.",
        "broad": "Can include pitch decks, battle cards, training guides, and sales tooling.",
    },
    "growth/sales/objections": {
        "canonical": "Objection handling and competitive responses.",
        "broad": "Can include objection libraries, response scripts, and competitive counter-positioning.",
    },
    "growth/sales/pricing": {
        "canonical": "Sales-side pricing and deal structures.",
        "broad": "Can include discount rules, deal templates, and pricing negotiation guidance.",
    },
    "growth/sales/win-loss": {
        "canonical": "Accumulating win-loss analysis records.",
        "broad": "Can include deal postmortems, competitive loss analysis, and win pattern documentation.",
    },
    "growth/success": {
        "canonical": "Customer success, support, and adoption systems.",
        "broad": "Can include onboarding, activation, adoption, retention, expansion, enablement, and support surfaces.",
    },
    "growth/success/onboarding": {
        "canonical": "Customer onboarding programs.",
        "broad": "Can include onboarding flows, checklists, and first-value delivery plans.",
    },
    "growth/success/activation": {
        "canonical": "User activation and time-to-value.",
        "broad": "Can include activation metrics, aha-moment definitions, and activation improvement programs.",
    },
    "growth/success/adoption": {
        "canonical": "Feature and product adoption programs.",
        "broad": "Can include adoption campaigns, feature rollout plans, and usage improvement initiatives.",
    },
    "growth/success/retention": {
        "canonical": "Retention and churn prevention.",
        "broad": "Can include retention programs, churn analysis, and re-engagement strategies.",
    },
    "growth/success/expansion": {
        "canonical": "Expansion and upsell programs.",
        "broad": "Can include expansion plays, upsell triggers, and account growth strategies.",
    },
    "growth/success/enablement": {
        "canonical": "Customer enablement and education.",
        "broad": "Can include help docs, tutorials, training programs, and self-service resources.",
    },
    "growth/success/support": {
        "canonical": "Customer support systems and posture.",
        "broad": "Can include support tiers, SLA definitions, escalation paths, and support tooling.",
    },
    "growth/execution": {
        "canonical": "Growth-owned execution surface.",
        "broad": "Can include growth plans, programs, experiments, dashboards, logs, and retros.",
    },
    "growth/execution/plans": {
        "canonical": "Transient growth execution plans.",
        "broad": "Can include campaign execution plans, launch plans, and active GTM scheduling artifacts.",
    },
    "growth/execution/programs": {
        "canonical": "Transient growth programs.",
        "broad": "Can include multi-channel programs, launch programs, and bounded GTM initiatives with lifecycle status.",
    },
    "growth/execution/experiments": {
        "canonical": "Growth experiment programs.",
        "broad": "Can include experiment design, running experiments, and experiment learnings.",
    },
    "growth/execution/experiments/running": {
        "canonical": "Currently running growth experiments (transient).",
        "broad": "Can include active A/B tests, channel experiments, and in-flight growth hypotheses with lifecycle status.",
    },
    "growth/execution/experiments/learnings": {
        "canonical": "Accumulating growth experiment learnings.",
        "broad": "Can include experiment results, postmortems, and reusable growth insights.",
    },
    "growth/execution/dashboards": {
        "canonical": "Growth execution dashboards and reporting.",
        "broad": "Can include funnel dashboards, campaign performance views, and adoption reporting.",
    },
    "growth/execution/logs": {
        "canonical": "Accumulating growth execution logs.",
        "broad": "Can include campaign journals, launch logs, and chronological GTM records.",
    },
    "growth/execution/retros": {
        "canonical": "Accumulating growth execution retrospectives.",
        "broad": "Can include campaign retros, launch retros, and GTM reflection records.",
    },
    ".system": {
        "canonical": "System metadata: version, manifest, and installed contract schemas.",
        "broad": "Tools read this directory. Humans and agents typically do not store project knowledge here.",
    },
}

TITLE_OVERRIDES = {
    "c4": "C4 Architecture",
    "prds": "PRDs",
    "devs": "Developer Context",
    "channel-mix": "Channel Mix",
    "data-security": "Data Security",
    "win-loss": "Win-Loss Analysis",
}


def title_for(rel_path: str) -> str:
    rel = rel_path.replace("/README.md", "").strip("/")
    if not rel:
        return "Archeia Instance"
    last = rel.split("/")[-1]
    return TITLE_OVERRIDES.get(last, last.replace("-", " ").replace("_", " ").title())


def lookup_meaning(rel_path: str, meanings: dict[str, dict], domains: dict[str, dict]) -> dict:
    rel = rel_path.replace("/README.md", "").strip("/")
    parts = rel.split("/")

    if parts[-1] in {"decisions", "conventions", "learnings"}:
        uni = meanings[parts[-1]]
        parent = "/".join(parts[:-1])
        broad = uni["broad"]
        if parent:
            broad += f" Scoped to the `{parent}` subtree."
        return {"canonical": uni["canonical"], "broad": broad, "universal": True}

    candidate = rel
    while True:
        if candidate in meanings:
            info = meanings[candidate]
            return {
                "canonical": info["canonical"],
                "broad": info["broad"],
                "universal": info.get("universal", False),
            }
        if "/" not in candidate:
            break
        candidate = candidate.rsplit("/", 1)[0]

    top = parts[0]
    if top in domains:
        return {
            "canonical": domains[top]["canonical"],
            "broad": domains[top]["broad"],
            "universal": False,
        }

    return {
        "canonical": "Canonical Archeia knowledge for this path.",
        "broad": "Use according to the path name and owning domain.",
        "universal": False,
    }


def questions_for(rel_path: str) -> list[str]:
    rel = rel_path.replace("/README.md", "").strip("/")
    last = rel.split("/")[-1] if rel else "project"

    if last == "decisions":
        return [
            "What choices or tradeoffs belong in this local decisions record?",
            "What context would a future agent need to understand why this decision was made?",
        ]
    if last == "conventions":
        return [
            "What local defaults or ways of working apply here?",
            "What would we want every contributor to do the same way in this subtree?",
        ]
    if last == "learnings":
        return [
            "What lessons, mistakes, or discoveries should be preserved here?",
            "What should future work avoid or repeat based on experience here?",
        ]

    templates = {
        "vision": [
            "What is the long-horizon purpose or mission for this project?",
            "What would we refuse to pursue?",
        ],
        "values": [
            "What principles or non-negotiables constrain this project?",
            "What trust, safety, or ethics postures apply?",
        ],
        "ethics": [
            "What is our minimum ethics posture for this project?",
            "What would we refuse to build or ship?",
        ],
        "specs": [
            "What executable requirements or specs define current product truth?",
            "What is out of scope or not yet specified?",
        ],
        "processes": [
            "What repeatable process, SOP, or runbook belongs here?",
            "When is this process used and who owns it?",
        ],
        "tasks": [
            "What operations tasks are currently active or queued?",
            'Or: N/A — no operations task tracking yet.',
        ],
        "c4": [
            "What architecture elements exist and what source files evidence them?",
            "Or: N/A — architecture model not started.",
        ],
        "prds": [
            "What integrated product mission or PRD defines current buildable work?",
            "Or: N/A — no active PRD yet.",
        ],
    }
    if last in templates:
        return templates[last]

    title = title_for(rel_path).lower()
    return [
        f"What should be written at `{rel or '.archeia'}` for this project?",
        f'Or: N/A / not applicable yet for {title}.',
    ]


def belongs_lines(rel_path: str, info: dict, domains: dict[str, dict]) -> list[str]:
    rel = rel_path.replace("/README.md", "").strip("/")
    top = rel.split("/")[0] if rel else ""
    if rel == top and top in domains:
        return domains[top]["belongs"]
    if info.get("universal"):
        return [f"Local {rel.split('/')[-1]} records scoped to this subtree."]
    return ["Artifacts that match this path's canonical meaning and owning domain."]


def not_belongs_lines(rel_path: str, domains: dict[str, dict]) -> list[str]:
    rel = rel_path.replace("/README.md", "").strip("/")
    top = rel.split("/")[0] if rel else ""
    if rel == top and top in domains:
        return domains[top]["not_belongs"]
    return [
        "Unrelated project knowledge, hidden wrapper folders, or content owned by another top-level domain."
    ]


def render_readme(rel_path: str, meanings: dict[str, dict], domains: dict[str, dict]) -> str:
    rel = rel_path.replace("/README.md", "").strip("/")

    if rel == ".system":
        info = meanings[".system"]
        return "\n".join(
            [
                "# System Metadata",
                "",
                f"**Canonical meaning.** {info['canonical']}",
                "",
                f"**Broad interpretation.** {info['broad']}",
                "",
                "**What belongs here:** `VERSION`, `spec.yaml`, and installed contract schemas only.",
                "",
                "**What does not belong here:** Project knowledge artifacts, domain content, or secrets.",
                "",
            ]
        )

    info = lookup_meaning(rel_path, meanings, domains)
    title = title_for(rel_path)
    lines = [
        f"# {title}",
        "",
        f"**Canonical meaning.** {info['canonical']}",
        "",
        f"**Broad interpretation.** {info['broad']}",
        "",
        'Answer here (even "N/A" or "not applicable yet"):',
        "",
    ]
    lines.extend(f"- {q}" for q in questions_for(rel_path))
    lines.extend(["", "**What belongs here:**"])
    lines.extend(f"- {b}" for b in belongs_lines(rel_path, info, domains))
    lines.extend(["", "**What does not belong here:**"])
    lines.extend(f"- {nb}" for nb in not_belongs_lines(rel_path, domains))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    kernel = load_kernel()
    domains = parse_domains(kernel)
    meanings = parse_section6(kernel)
    for path, info in SUPPLEMENTARY.items():
        meanings[path] = {**info, "universal": False}

    updated = 0
    for readme in sorted(INSTANCE.rglob("README.md")):
        rel = str(readme.relative_to(INSTANCE))
        if rel == "README.md":
            continue
        readme.write_text(render_readme(rel, meanings, domains), encoding="utf-8")
        updated += 1

    print(f"Updated {updated} README instruction files from KERNEL.md")
    print(f"KERNEL section 6 entries: {len(parse_section6(kernel))}")
    print(f"Supplementary paths added: {len(SUPPLEMENTARY)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
