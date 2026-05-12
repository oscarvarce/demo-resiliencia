# Technical Assessment: Global Direct Digital Channel Architecture

**Candidate:** Oscar Mauricio Vargas Arce  
**Date:** May 2026

## **Personal Introduction:**

I am now at an inflection point in my career. I have built and optimized systems, led technical teams, mentored 500+ developers, and acted as the bridge between business and engineering. What I want now is to scale my impact: to design the systems before they are built, to make the architectural decisions that prevent million-user outages, and to create platforms that teams can build upon with confidence.  
This assessment is my deliberate step into that space. I approached it not as an expert architect — I am honest about that — but as a seasoned engineer applying his existing skills to new challenges. Where I encountered concepts I had not yet implemented in production (global multi-region active-active, event-driven sagas, chaos engineering), I researched them deeply, implemented them in code, and documented my thought process.

What you will see in this document is:

* **Real experience** applied to architectural problems (scalability, integration, data residency)  
* **Intellectual honesty** about the gap between "I have processed 1M records/day" and "I have designed a global digital channel"  
* **Proof of execution** — working code, not just diagrams  
* **A clear growth trajectory** — I know what I bring and what I need to master next

## **Section A — Architecture & Roadmap: Scaling What I Have Built**

### **A.1 Target Architecture:**

I have operated systems at scale. At Claro Colombia, I optimized a CDR processing engine for \+1 million XML records daily. At Universidad del Norte, I designed ETL pipelines and Power BI dashboards serving 10+ departments. At Movilplata, I worked on microservices deployed in GCP. These experiences taught me that scale is not just about throughput — it is about resilience, observability, and the ability to recover when things break.  
This target architecture for a multi-country Direct Digital Channel extends those lessons to a global, multi-region context.

**Note on Technology Stack:** The architecture diagram below represents a technology-agnostic blueprint. While the specific stack (Salesforce, Azure, or other enterprise platforms) would be determined by the organization's existing investments, the resilience patterns (circuit breakers, idempotency, async messaging) and integration framework apply universally. I have not yet worked directly with Salesforce or Azure Analytics at production scale, but I understand that the integration framework I designed in Section B is stack-agnostic by design — it connects to any upstream via REST/SOAP APIs, handles rate limits through circuit breakers and bulkheads, and ensures idempotency for critical customer operations. 

#### **Architecture Layers (Built on My Experience)**

| Layer | Components | What I Have Done | What I Am Learning |
| ----- | ----- | ----- | ----- |
| Edge | Global DNS, CDN/WAF, Regional API Gateways | Used Cloudflare and AWS Route 53 for basic routing. | Geo-routing, health-check-based failover, edge caching for sub-50ms global latency. |
| Application | Kubernetes, Service Mesh, BFF, Domain Microservices | Microservices on GCP (Movilplata). Docker, containerization. | Service mesh (Istio), HPA tuning, multi-cluster federation. |
| Integration | Kafka/EventBridge, Integration Framework, GraphQL Federation | ETL pipelines (SSIS), XML/CDR processing, data integration across systems. | Event-driven architecture at global scale, Kafka partitioning, saga orchestration, SOAP→REST protocol adaptation. |
| Data | PostgreSQL read replicas, Redis, Kafka, S3 | PostgreSQL optimization (Claro), MongoDB (Movilplata), data modeling for BI. | Multi-region replication, CRDTs, conflict resolution in active-active setups, GDPR/LGPD data residency controls. |
| Observability | Prometheus, Grafana, ELK, Jaeger, OpenTelemetry | Power BI dashboards, SSIS monitoring, basic logging. | Distributed tracing, SLO/SLI definition, three-pillar observability model (metrics, logs, traces). |
| Security | Zero Trust, Vault, mTLS, Data Residency | TLS and basic IAM. | SPIFFE/SPIRE, HashiCorp Vault, GDPR/LGPD compliance architecture across regions. |

#### 

#### 

#### **My Architectural Decisions (Grounded in Experience)**

1. Multi-Region Active-Active: At Claro, a single processing node failure would back up the CDR queue. I learned that single points of failure are unacceptable at scale. For a global digital channel, active-active is the only pattern that provides true resilience. I have not yet operated a multi-region active-active database, but I understand the trade-offs (conflict resolution, CAP theorem implications) and have researched CRDTs and vector clocks as potential solutions.   
2. Event-Driven Core for Critical Flows: My ETL experience taught me that batch processing creates bottlenecks and blind spots. Event streaming (Kafka) provides real-time visibility, replay capability, and natural audit trails — critical for financial flows like payments and account opening. I have used message queues conceptually; I am now deepening my knowledge of Kafka Streams, exactly-once semantics, and the Saga pattern for distributed transactions.   
3. Database-per-Service with CQRS: At Movilplata, I saw how shared databases create coupling that slows teams down. Database-per-service is non-negotiable for independent deployment. However, I acknowledge that CQRS and event sourcing are patterns I have read about extensively but not yet implemented in production. I understand the theory; I need the battle-tested experience. 

### **A.2 Integration Patterns: From ETL Pipelines to Resilient Service Mesh**

My background in ETL, XML processing, and data integration gives me a solid foundation for understanding integration patterns. I have spent years ensuring data flows correctly between systems; now I am extending that to ensuring service calls succeed, fail gracefully, and recover automatically. 

| Pattern | My Previous Experience  | My New Learning  |
| ----- | ----- | ----- |
| Retries \+ Backoff \+ Jitter | Retry logic in ETL pipelines when external APIs failed. | Full jitter prevents thundering herds. Implemented in the framework (Section B) using randomization over exponential delay. |
| Circuit Breaker | Basic Hystrix usage in Spring Boot. | HALF\_OPEN state is critical to prevent flapping. Built a custom implementation to understand the state machine deeply. |
| Idempotency | Deduplication in CDR processing (avoiding duplicate billing records). | UUIDv4 idempotency keys with Redis-backed TTL storage. Implemented a simulation in Python. |
| Bulkheads | Resource isolation in GCP (separate services, quotas). | Thread-pool-level and K8s-namespace-level bulkheads. Implemented a semaphore-based bulkhead in the framework. |
| Async Messaging | Batch ETL jobs (SSIS). | Real-time event streaming with Kafka, consumer groups, partition rebalancing, dead letter queues. My biggest growth area. |
| Caching | Query optimization and materialized views in PostgreSQL. | Redis Cluster, cache-aside vs write-through, cache warming, stampede prevention. |

**A.3 12-Week Roadmap: A Realistic Plan from Someone Who Has Delivered Before**

I have led sprints, managed backlogs, and delivered production systems. This roadmap reflects what I know about execution combined with what I need to learn about architecture at scale. 

#### Workstream 1: Reliability (Weeks 1–4) 

| Week | Deliverable | My Angle / Experience Applied |
| ----- | ----- | ----- |
| W1 | Resilience Framework MVP (retries, circuit breaker, timeout) | I have written retry logic and timeout handling in production ETL pipelines. Now I am packaging it into a reusable, configurable framework. |
| W2 | Bulkhead Implementation (K8s namespaces, thread pools, resource quotas) | Applying resource quota patterns I used in GCP (Movilplata) to Kubernetes namespaces and thread-level isolation. |
| W3 | Chaos Engineering Setup (Litmus/Gremlin) | New for me. I have read about Chaos Monkey and Gremlin. I want to run my first controlled failure injection — starting with pod kills and network latency. |
| W4 | DR & Failover Automation | At Claro, failover was manual. I want to automate regional failover with RTO \< 15 min. This requires hands-on mentorship. |

## Workstream 2: Integration Modernization (Weeks 5–8)

| Week | Deliverable | My Angle / Experience Applied |
| ----- | ----- | ----- |
| W5 | Async Messaging Platform (Kafka cluster, schema registry) | My biggest learning opportunity. I know batch ETL (SSIS). I need to master Kafka: brokers, partitions, schema registry, and the shift from "pull" to "push" architecture. |
| W6 | Idempotency & Deduplication (Redis-backed keys) | Directly applicable to my CDR experience at Claro. I know deduplication; now I am applying it to HTTP APIs with Redis and TTL management. |
| W7 | API Gateway & GraphQL Federation (BFF services) | New for me. I have used REST extensively. GraphQL federation and Backend-for-Frontend patterns are concepts I have studied but not yet operated in production. |
| W8 | Legacy Integration Abstraction (SOAP/mainframe adapters) | At Walmart, I coordinated between modern web apps and legacy core systems. I understand the friction. I want to build adapter patterns that reduce it. |

## Workstream 3: Observability & Operations (Weeks 9–12)

| Week | Deliverable | My Angle / Experience Applied |
| ----- | ----- | ----- |
| W9 | Distributed Tracing (OpenTelemetry, Jaeger) | I have built Power BI dashboards and SSIS monitoring. Distributed tracing is the next evolution — understanding a single user request across 20+ services. |
| W10 | Metrics & Alerting (Prometheus, Grafana, SLOs/SLIs) | I understand SLA vs SLO vs SLI conceptually. I need to operationalize them: define error budgets, set up Prometheus alerts, and create actionable runbooks. |
| W11 | Centralized Logging (ELK/Loki stack) | I know structured logging. I need to scale it: ELK/Loki, trace ID correlation across services, and log-based metrics. |
| W12 | SRE Runbooks & Onboarding | At Claro and Walmart, I wrote technical documentation. SRE runbooks are that discipline applied to incident response. I want to learn from experienced SREs. |

#### 

#### **A.4 Architecture Diagram: What I Would Draw**

I would create the diagram in Draw.io with three zoom levels, using conventions I learned from technical documentation standards:

* **Level 1 (System Context)**: Users, Digital Channel, external systems — the "big picture" I would present to business stakeholders (leveraging my Business Analyst experience at Walmart).  
* **Level 2 (Container)**: K8s clusters, Kafka, databases, API gateways per region — the technical view for engineering leads.  
* **Level 3 (Component)**: Detailed Integration Framework view — circuit breaker boundaries, retry flows, cache layers — for the implementation team.

Color coding: Blue (Customer), Green (Payments), Orange (Product), Purple (Observability), Red (Security). Line styles: Green solid (async), Blue solid (sync), Red dotted (circuit boundaries).  
**Technology Note:** The diagram uses cloud-native components (Kubernetes, Kafka, PostgreSQL) as reference architecture. In practice, the actual stack would align with the organization's existing investments (e.g., Azure, Salesforce, or other enterprise platforms). The resilience patterns and integration framework are **stack-agnostic** and would be adapted to the specific APIs, rate limits, and protocols of the chosen platform. 

## **Section B — Reusable Integration Framework: From Theory to Code**

### **B.1 Why I Built This (And What It Represents)**

I built this framework to prove that I can translate architectural patterns into working code. I have spent years writing production Java (Spring Boot) and Python. This framework is my deliberate practice in a new domain: resilience engineering.  
I chose Python for this assessment because it is readable and allows the reviewer to focus on the patterns, not language syntax. In production, I would implement this in Java with Spring Cloud Circuit Breaker, Resilience4j, or as a service mesh sidecar — but the principles are identical.

### **B.2 What the Framework Includes (And What I Knew vs. Learned)**

| Component | What I Knew Before | What I Learned for This Assessment |
| ----- | ----- | ----- |
| ResilienceConfig | Configuration management in Spring Boot (application.yml) | Centralizing resilience parameters (timeouts, retries, circuit thresholds) in a single tunable dataclass. |
| CircuitBreaker | Basic Hystrix usage in Java | Deep understanding of the state machine: CLOSED → OPEN → HALF\_OPEN. Why HALF\_OPEN prevents flapping. Thread-safe implementation with threading.Lock. |
| Bulkhead | Resource quotas in GCP | Semaphore-based concurrency limiting. Why per-dependency bulkheads prevent cascade failures. |
| IdempotencyStore | Deduplication in CDR processing | Redis-backed idempotency with TTL. Composite key (idempotency\_key \+ payload\_hash). Why TTL prevents unbounded growth. |
| RetryPolicy | Basic retry loops | Exponential backoff with full jitter. The AWS Architecture Blog insight: random(0, delay) prevents synchronized retries after recovery. |
| IntegrationContext | HTTP headers, request context | W3C Trace Context, OpenTelemetry propagation. Why trace IDs must flow through every layer for observability. |
| IntegrationClient | Service clients in Spring | Orchestrating the full pipeline: idempotency → circuit breaker → bulkhead → retry → cache. Why order matters. |

### **B.3 Design Decisions (With Honest Self-Assessment)**

| Decision | Why I Made It | Production Gap I Acknowledge |
| ----- | ----- | ----- |
| In-memory idempotency store | Demo necessity. Easy to understand. | Production needs Redis Cluster or DynamoDB with cross-region replication. I have not operated Redis Cluster in production. |
| Simple threading.Lock | Python GIL makes this acceptable for demo. | High-throughput systems need asyncio, reactive streams (Project Reactor), or lock-free data structures. I need hands-on experience here. |
| Full jitter | Research-backed (AWS, Google SRE). | I have not benchmarked equal jitter vs full jitter myself. I am trusting authority but want to validate with profiling. |
| Per-destination circuit breaker | Prevents one bad service from affecting others. | Memory footprint at 100+ destinations needs validation. I have not profiled this. |

### **B.4 What I Would Add With Mentorship**

* Adaptive timeouts based on historical p99 latency (not static values)

* Prometheus metrics for circuit breaker state changes, retry histograms, bulkhead utilization

* Reactive programming (Project Reactor / RxJava) for non-blocking I/O

* Request hedging for ultra-latency-sensitive operations

* Integration with Istio circuit breakers at the network level — ¿how do app-level and mesh-level breakers compose?

## **Section C — Demo Service & Reliability Test: Proving It Works**

### **C.1 What I Built**

An OrderService that calls an unstable payment gateway. The upstream simulates:

* 60% server errors (500, 502, 503, 504\)  
* 20% timeouts (hangs beyond threshold)  
* 20% slow successes

This is intentionally harsher than most real services to stress-test the framework.

### **C.2 How to Run**

\# 1\. Place both files in the same directory:  
\#    \- integration\_framework.py  
\#    \- demo\_service.py

\# 2\. Run the demo  
python demo\_service.py

\# 3\. Observe:  
\#    \- Structured JSON logs with trace IDs  
\#    \- Circuit breaker state transitions (CLOSED → OPEN → HALF\_OPEN → CLOSED)  
\#    \- Retry attempts with calculated backoff delays  
\#    \- Idempotency cache hits (duplicate orders)  
\#    \- Bulkhead rejections under concurrent load

### **C.3 Test Results and What They Prove**

| Test | What Happens | What It Validates |
| ----- | ----- | ----- |
| T1: Sequential Calls | 8 calls. Some succeed via retries. | Retries recover transient failures. I have seen this pattern in ETL retry logic. |
| T2: Circuit Breaker Opening | Opens after 3 failures. | Prevents cascade. I implemented the state machine correctly. |
| T3: Fast-Fail | \< 0.1s rejection when OPEN. | Protects upstream from overload. Critical insight: fast-fail is as important as retry. |
| T4: Recovery | HALF\_OPEN → CLOSED after success. | Gradual recovery prevents flapping. This was new to me; I validated it works. |
| T5: Idempotency | Duplicate order returns cached response. | Prevents double-charging. Directly applicable to my CDR deduplication experience. |
| T6: Bulkhead | 10 concurrent requests. 3+1 processed. 6 rejected. | Early rejection is better than crash. Counterintuitive but correct. |

### **C.4 Honest Reflection**

* **What worked**: All patterns behaved as researched. The circuit breaker opened, retries backed off, idempotency prevented duplicates.  
* **What is simplified**: No real HTTP calls, no network partitions, no TLS failures. My next step is testing against real infrastructure.  
* **What I want to learn**: How does this compose with **Istio circuit breakers**? What happens when app-level and network-level breakers disagree?

## **Section D — Technical Decision Record: My Thought Process**

### **D.1 ADR-001: Centralized vs. Decentralized Integrations**

#### **Context**

40+ upstream integrations (core banking, payments, KYC, notifications) in a multi-team environment. 

#### **My Experience**

At Walmart CAM, I coordinated three teams (Web, Core, App) for the WM Pass launch. I experienced firsthand how centralized coordination can become a bottleneck and how decentralized teams can diverge in their approaches. At Claro, I worked within a larger integration ecosystem where consistency was enforced top-down, sometimes slowing innovation. 

#### **Options Analysis**

| Approach | Pros | Cons | My Experience With This |
| :---- | :---- | :---- | :---- |
| Centralized Platform | Consistent security, monitoring, shared expertise | Bottleneck, single point of failure, tight coupling | Similar to Claro's top-down data integration. Consistent but slow to adapt. |
| Decentralized | Team autonomy, faster delivery | Inconsistent resilience, duplicated effort, operational sprawl | Similar to Walmart's cross-team coordination challenge. Fast but risky without guardrails. |

#### **My Decision (Tentative): Hybrid "Federated Integration with Guardrails"**

1. **Mandated Reusable Framework**: All teams MUST use the certified framework (Section B) for sync calls. Ensures consistent retries, circuit breakers, timeouts, and observability.  
2. **Centralized Async Infrastructure**: Kafka/EventBridge managed by platform SREs. Topics, schemas, ACLs governed centrally.  
3. **Shared Adapter Library**: Common protocol adapters (SOAP, ISO 8583\) maintained centrally, consumed as dependencies.  
4. **Domain Autonomy**: Teams own their integration orchestration and business logic.

**Why tentative**: I have coordinated teams but have not architected a 40-integration platform. I need mentorship on governance mechanisms (RFC process, architecture review board) that prevent chaos while preserving speed. 

### **D.2 ADR-002: Event-Driven vs. Synchronous for Critical Flows**

#### **Context**

Payments, account opening, loans — must be reliable, auditable, recoverable. 

#### **My Experience**

At Claro, CDR processing was batch-oriented (ETL). It worked but created blind spots — we knew about failures hours after they happened. At Universidad del Norte, real-time Power BI dashboards were impossible with batch delays. I learned that latency in data flows directly impacts decision-making. 

#### **Options Analysis**

| Approach | Best For | My Concern |
| ----- | ----- | ----- |
| Event-Driven | Durability, auditability, replay, decoupling | Complexity. Eventual consistency is hard to reason about. Debugging across events is harder than tracing a single HTTP call. |
| Synchronous | Immediate feedback, simplicity, low latency | Tight coupling. No natural buffer. Cascading failures. |

#### **My Decision (Tentative): CQRS \+ Saga Hybrid**

* **Commands (writes)**: Event-driven. Payments, account openings emit events. Event log \= source of truth. Provides audit trail and recovery.  
* **Queries (reads)**: Synchronous. Users checking balance expect immediate answers.  
* **Saga Orchestration**: Central coordinator for distributed transactions with compensation logic.

**Why tentative**: I understand saga theory but have not implemented one in production. I am particularly unsure about:

* Handling "orphan" events when compensation partially succeeds  
* Schema evolution without breaking consumers  
* Monitoring consumer lag to prevent read model staleness

**What I need**: Hands-on mentorship with Kafka Streams, exactly-once semantics, and production saga patterns.

## **Reflection: My Trajectory and Why This Role**

### **What I Bring (Proven)**

* **9+ years building production systems** in Java, Python, and JavaScript  
* **Scale experience**: \+1M records/day processing, ETL optimization, microservices on GCP  
* **Leadership**: Tech Lead coordinating sprints, Business Analyst bridging business and engineering, mentor to 500+ developers  
* **Cross-functional coordination**: Walmart CAM (Web \+ Core \+ App), Colpensiones (vendor coordination)  
* **Data integrity**: CDR deduplication, ETL pipeline design, BI dashboard accuracy

### **What I Am Learning (In Progress)**

* **Global multi-region architecture**: I have optimized single-region systems. I am now learning active-active, conflict resolution, and data residency.  
* **Event-driven architecture at scale**: I know batch ETL. I am mastering Kafka, stream processing, and sagas.  
* **Observability engineering**: I have built dashboards. I am learning distributed tracing, SLOs, and chaos engineering.  
* **Service mesh and zero trust**: I know Docker and basic K8s. I am studying Istio, mTLS, and SPIFFE.

### **What I Need (Honest Ask)**

* **Mentorship from experienced architects** who have designed global digital channels  
* **Hands-on exposure** to multi-region deployments, Kafka operations, and chaos engineering  
* **Architectural decision-making practice** — moving from "implement what was designed" to "design what will be implemented"

### **Why This Opportunity**

I am not a blank slate. I am an **experienced engineer making a deliberate career transition**. I bring:

* Technical depth (Java, Python, microservices, data at scale)  
* Leadership experience (Tech Lead, BA, mentor)  
* Proven execution (production systems, cross-team delivery)  
* Intellectual humility (I know what I don't know and I learn fast)

What I need is the **platform to scale my impact**. I want to design systems that serve millions, not just optimize the ones that do. I want to prevent outages before they happen, not just respond to them. I want to create architectures that teams can build upon with confidence.  
This assessment is my proof that I can **research, synthesize, implement, and honestly evaluate** complex architectural problems. I am ready to learn, ready to lead, and ready to grow into the tech lead this organization needs.

**Thank you for reviewing my assessment.**  
*Oscar Mauricio Vargas Arce*  
*Tech Lead | Business Analyst | Architect-in-Training* 

