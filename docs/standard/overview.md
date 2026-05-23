# Archeia Overview

Archeia gives software projects a shared knowledge layer inside the repo.

The goal is simple: humans and agents should not have to reconstruct project truth from scattered chats, tickets, docs, and guesses. Important context should live in predictable files, with clear ownership and validation.

## The Problem

AI coding agents are often smart enough to do the work, but they lack stable context. They lose decisions between sessions. They cannot always see product direction, architecture evidence, operating constraints, or current work state.

Human-agent collaboration has the same problem. A chat window can hold a conversation, but it is a weak place to keep durable project state.

## The Claim

The repo can be the shared surface.

Directories give structure. Files hold knowledge. Frontmatter carries schema. Git gives history, review, and recovery. Archeia adds the missing convention: where each kind of project knowledge belongs, how it changes, and who may write it.

## What Archeia Adds

Archeia defines four canonical domains:

- `strategy/`: direction, values, landscape, and roadmap.
- `operations/`: support, execution, process, people, finance, and compliance.
- `product/`: product strategy, design, technical context, and delivery.
- `growth/`: adoption, marketing, sales, success, and rollout.

It also defines three artifact shapes:

- **Living**: edited in place; git holds history.
- **Accumulating**: append-only records; never pruned.
- **Transient**: work-state artifacts; pruned after a retention window.

## Principles

1. Context is the bottleneck. Structure helps agents more than another memory silo.
2. The filesystem is both database and collaboration surface.
3. Ownership is the concurrency model. One top-level domain owns each write surface.
4. Files compose better than hidden APIs. Agents can read and write the same substrate.
5. Deterministic checks belong in tools. Judgment belongs in skills and humans.

## What Archeia Is Not

Archeia is not a hosted service, ticket system, wiki, vector database, or agent framework. Those tools can sit around it. Archeia is the project knowledge contract that those tools can read from and write to.

## When To Use It

Use Archeia when a software project needs durable context that agents and humans can both inspect. It is especially useful when product, technical, operational, and growth context need to stay connected without depending on one private tool.
