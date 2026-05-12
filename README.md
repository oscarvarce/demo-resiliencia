# demo-resiliencia
# Technical Assessment: Global Direct Digital Channel Architecture

**Candidate:** Oscar Mauricio Vargas Arce  
**Role:** Tech Lead  
**Date:** May 2026  

---

## Overview

This repository contains my technical assessment for a Tech Lead position focused on designing and coordinating resilient distributed systems for a multi-country Direct Digital Channel.

The assessment covers four sections:
- **Section A:** Target Architecture & 12-Week Roadmap
- **Section B:** Reusable Integration Framework (Python)
- **Section C:** Demo Service & Reliability Tests
- **Section D:** Technical Decision Records (ADRs)

---

## Repository Structure

```
demo-resiliencia/
├── integration_framework.py      # Reusable resilience framework (Section B)
├── demo_service.py               # Demo service with 6 reliability tests (Section C)
├── docs/
│   └── architecture-diagram.png  # Target architecture visualization (Section A)
├── PROMPTS.md                    # AI prompts used (transparency)
├── assessment-document.md        # Full assessment document (Sections A-D)
└── README.md                     # This file
```

---

## Quick Start: Run the Demo

### Prerequisites
- Python 3.8 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/oscarvarce/demo-resiliencia.git
cd demo-resiliencia

# No additional dependencies required — uses Python standard library only
```

### Run the Reliability Test

```bash
python demo_service.py
```

### Expected Output

The demo executes 6 tests demonstrating resilience patterns:

| Test | What It Proves |
|------|---------------|
| **T1: Sequential Calls** | Retry with exponential backoff + jitter |
| **T2: Circuit Breaker Opening** | State transition: CLOSED → OPEN |
| **T3: Fast-Fail** | Immediate rejection when circuit is OPEN (< 0.1s) |
| **T4: Recovery** | State transition: HALF_OPEN → CLOSED |
| **T5: Idempotency** | Duplicate requests return cached response |
| **T6: Bulkhead** | Concurrent execution limiting |

**Runtime:** ~45 seconds  
**Success rate:** Depends on random failure simulation (typically 30-50%)

---

## Architecture

![Target Architecture](docs/architecture-diagram.png)

The target architecture is a **multi-region, active-active** platform with six layers:

| Layer | Purpose | Key Components |
|-------|---------|---------------|
| **Edge** | Global traffic management | DNS geo-routing, CDN, API Gateway |
| **Application** | Microservices execution | Kubernetes, Service Mesh, BFF |
| **Integration** | Service communication | Kafka, Integration Framework, GraphQL |
| **Data** | Persistence & caching | PostgreSQL, Redis, S3, MongoDB |
| **Observability** | Monitoring & alerting | Prometheus, Grafana, ELK, Jaeger |
| **Security** | Zero trust & compliance | Vault, mTLS, data residency |

See `assessment-document.md` for full architectural decisions and trade-offs.

---

## Framework Components

The `integration_framework.py` implements six resilience patterns:

| Pattern | Class | Description |
|---------|-------|-------------|
| **Retry + Backoff + Jitter** | `RetryPolicy` | Exponential backoff with full jitter to prevent thundering herd |
| **Circuit Breaker** | `CircuitBreaker` | CLOSED → OPEN → HALF_OPEN state machine |
| **Bulkhead** | `Bulkhead` | Concurrency limiting with queue |
| **Idempotency** | `IdempotencyStore` | TTL-based deduplication storage |
| **Trace Propagation** | `IntegrationContext` | W3C Trace Context compliant headers |
| **Structured Logging** | `TraceLogger` | JSON logs with trace ID correlation |

---

## AI Usage Transparency

I used multiple AI tools (Kimi, Deepseek, Claude) as **sparring partners** to accelerate research and validate implementations. All prompts, iterations, and manual validations are documented in [PROMPTS.md](./PROMPTS.md).

**What AI did:**
- Accelerate research on resilience patterns
- Structure architectural arguments (ADRs, trade-offs)
- Generate code scaffolding for the framework

**What AI did NOT do:**
- Replace my technical judgment
- Invent experiences I do not have
- Run or test the code — execution was entirely manual

---

## About Me

- **9+ years** in software engineering (Java, Python, JavaScript)
- **Scale experience:** +1M records/day CDR processing (Claro Colombia)
- **Cross-team coordination:** Walmart CAM (Web + Core + App cells)
- **Mentorship:** 500+ developers trained in MinTIC/SENA bootcamps
- **Current role:** Senior Java Developer / Tech Lead at Hitss

---

**Oscar Mauricio Vargas Arce**  
Tech Lead | Business Analyst | Architect-in-Training
