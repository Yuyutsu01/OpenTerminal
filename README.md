# OpenTerminal – A Full‑Fledged Bloomberg Terminal Alternative

> **Disclaimer** – This project is a **conceptual blueprint** for educational purposes. Building a production‑grade Bloomberg Terminal requires billions in data licensing, regulatory compliance, and infrastructure. This README outlines a **minimal viable architecture** for an open‑source, single‑asset class, delayed‑data terminal.

## Table of Contents
- [Overview](#overview)
- [Project Scope & Constraints](#project-scope--constraints)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Roadmap](#roadmap)
- [Challenges & Trade‑offs](#challenges--trade-offs)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**OpenTerminal** is an attempt to build a **modular, extensible financial desktop application** that mimics the core user experience of a Bloomberg Terminal – real‑time market data, news aggregation, basic analytics, and a messaging layer – but within a realistic budget and legal framework for a research project or early‑stage fintech.

**Why?** To demystify the complexity of professional trading platforms and provide a learning sandbox for financial engineers, data scientists, and UI/UX designers.

---

## Project Scope & Constraints

To keep the project feasible, we **intentionally limit** the scope:

| Constraint | Decision |
|------------|----------|
| **Asset class** | US equities only (NASDAQ, NYSE) |
| **Data timeliness** | 15‑minute delayed (free from IEX Cloud / Polygon.io free tier) |
| **User count** | Single user / local deployment only |
| **Messaging** | Optional – WebSocket chat with no compliance auditing (for demo only) |
| **Real‑time infrastructure** | Single machine (no distributed streaming) |
| **Regulatory** | No real trading, no order execution – analytics only |

> 💡 A **production** terminal would require live data licensing (costing >$50M/year), colocation, 24/7 support, and regulatory approval.

---

## Features

### Core (MVP)
- [x] Live (delayed) price quotes for 10,000+ US stocks  
- [x] Interactive charts (candlestick, volume, indicators)  
- [x] News feed – aggregated from free RSS (Yahoo Finance, SEC EDGAR)  
- [x] Basic screeners (e.g., P/E ratio, 52‑week high)  
- [x] Excel add‑in – fetch stock prices via WebSocket  
- [x] Keyboard‑driven command palette (like Bloomberg’s `GO`)

### Advanced (Phase 2)
- [ ] Historical tick database (PostgreSQL + TimescaleDB)  
- [ ] Simple portfolio VaR (variance‑covariance method)  
- [ ] Earnings sentiment analysis (using Hugging Face transformers)  
- [ ] Web version (React + FastAPI)

### Stretch Goals
- [ ] Real‑time chat (no persistence)  
- [ ] Options pricing (Black‑Scholes calculator)  
- [ ] Dark mode

---

## System Architecture

