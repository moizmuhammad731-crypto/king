# NED University of Engineering & Technology

## Department of Software Engineering

### SE-213: Data Structures and Algorithms

# PINK WHEELS

## A Women-Focused Ride-Hailing Platform for Karachi with DSA-Based Matchmaking

### Complex Engineering Problem (CEP) Report

**CLO 2 — Problem Analysis | CLO 3 — Individual and Teamwork**

| Group Member | Seat Number | Primary Contribution |
|---|---|---|
| [Member 1 Full Name] | [SE-XX-XXX] | Linked list and priority-queue design; Chapters 1–2 |
| [Member 2 Full Name] | [SE-XX-XXX] | Matchmaking workflows, complexity analysis; Chapters 4–5 |
| [Member 3 Full Name] | [SE-XX-XXX] | Frontend integration, testing, walkthrough; Chapters 3 and 6 |

**Semester:** Fall 2026  **Section:** [Section]  **Date:** 19 November 2026

**Course Instructor:** [Instructor Name]

**Submitted in partial fulfilment of the Complex Engineering Problem requirement for SE-213.**

---

## Abstract

Ride-hailing in Karachi is constrained less by the number of vehicles than by how quickly and fairly an available driver can be matched to a passenger. Informal practices—street hailing, phone calls, and coordinator-managed WhatsApp groups—provide no reliable view of driver availability, no deterministic nearest-driver selection, no auditable record of what happened to a request, and no transparent fare. Pink Wheels is a women-focused ride-hailing demonstration platform that addresses these gaps with a FastAPI backend, a Vue 3 single-page frontend, and a deliberately implemented Data Structures and Algorithms layer rather than library shortcuts.

The system maintains registered drivers in a custom singly linked list, ranks eligible drivers in a custom binary min-heap priority queue keyed primarily on estimated time of arrival (ETA), secondarily on distance, and finally on driver identifier for deterministic tie-breaking, records every lifecycle event in a custom LIFO activity stack, and demonstrates FIFO intake through a custom ride-request queue. Geographic distance is computed with the Haversine formula, ETA is derived from a constant average city speed with a two-minute floor, and fares follow three explicit vehicle categories. The complete ride lifecycle—request, offer, rejection and reassignment cascade, acceptance, completion, and cancellation—is coordinated in a single service module and persisted to SQLite (with automatic PostgreSQL fallback).

The engineering analysis shows that building the candidate heap costs $O(n + a\log a)$ for $n$ registered and $a$ eligible drivers, that a rejection step costs $O(\log a)$ while the heap is alive, and that every operation is deterministic under equal ETAs because of the three-level priority key. A concrete walkthrough on the seeded Karachi dataset reproduces the live application exactly: 13 registered drivers, 11 eligible candidates, a heap root of Hina Tariq at 2.0 minutes, and a full ranking from 2.0 to 27.3 minutes. The report also evaluates Bubble Sort with early exit and Quick Sort as design-level alternatives, and explains why incremental heap extraction, not whole-collection sorting, fits the dispatch workload. Verification covers 48 automated tests, a complete OFFERED → ACCEPTED → COMPLETED lifecycle, and frame-time measurements in which every page holds a 99th-percentile frame time below 2.1 ms unthrottled and below 6.6 ms under four-times CPU throttling, inside the 8.33 ms budget of a 120 Hz display. The work demonstrates problem analysis (CLO 2) through requirement decomposition, structure selection, and complexity reasoning, and teamwork (CLO 3) through clean module boundaries, shared API contracts, and integrated end-to-end verification.

---

## Acknowledgement

We express our sincere gratitude to our course instructor for SE-213: Data Structures and Algorithms for guidance that kept the project anchored in algorithmic reasoning rather than surface-level application development. The Department of Software Engineering at NED University of Engineering & Technology provided the academic environment and laboratory resources that made the implementation and testing possible. We also thank our peers who reviewed the demonstration dashboard and tested the ride lifecycle from the passenger and driver perspectives. Finally, we acknowledge the open-source communities behind FastAPI, Vue.js, Leaflet, SQLite, and OpenStreetMap/OSRM, whose documentation and tooling supported the engineering work described in this report.

---

## Contents

1. Chapter 1 — Introduction and Problem Understanding
2. Chapter 2 — Requirement Identification and System Analysis
3. Chapter 3 — System Design and Architecture
4. Chapter 4 — Algorithm Design Document
5. Chapter 5 — Time and Space Complexity Analysis
6. Chapter 6 — Algorithm Demonstration and Walkthrough
7. Chapter 7 — Conclusion, Future Scope, and Source Code Listings

---

## List of Figures

- Figure 1.1 — Passenger ride-booking interface with Karachi map and fare estimate
- Figure 1.2 — Driver console with availability control and active ride
- Figure 3.1 — DSA Demonstration Dashboard overview
- Figure 6.1 — Linked list visualization of the 13 registered drivers
- Figure 6.2 — Linked list registration and node-management controls
- Figure 6.3 — Priority-queue tab ranked from a reference pickup point
- Figure 6.4 — Min-heap ranking of all 11 eligible drivers
- Figure 6.5 — Five-step matchmaking simulation in the DSA dashboard
- Figure 6.6 — Fare breakdown for the Saddar-to-Clifton trip
- Figure 6.7 — LIFO activity stack after the Ride #23 lifecycle

## List of Tables

- Table 1.1 — User roles and responsibilities
- Table 1.2 — CLO 2 and CLO 3 mapping
- Table 2.1 — Functional requirements and implementation mapping
- Table 2.2 — Non-functional requirements and verification evidence
- Table 2.3 — Hardware and software stack
- Table 2.4 — Data structure inventory and module mapping
- Table 2.5 — Algorithm inventory and module mapping
- Table 2.6 — REST API surface
- Table 3.1 — Layer responsibilities
- Table 3.2 — The `passengers` table
- Table 3.3 — The `rides` table
- Table 3.4 — State ownership and lifetime
- Table 3.5 — Ride state transitions and guards
- Table 4.1 — Edge cases and tie-breakers
- Table 4.2 — Structural invariants
- Table 5.1 — Complexity notation and variables
- Table 5.2 — Per-operation time complexity
- Table 5.3 — Composite workflow complexity
- Table 5.4 — Space complexity
- Table 5.5 — Comparative asymptotic summary
- Table 5.6 — Bubble Sort versus Quick Sort
- Table 5.7 — Empirical microbenchmarks
- Table 6.1 — Seeded driver dataset with distance and ETA to Saddar
- Table 6.2 — Heap array after each insertion
- Table 6.3 — Priority-queue extraction order
- Table 6.4 — Ride #23 event timeline
- Table 6.5 — Activity stack contents
- Table 6.6 — Rejection cascade for a fresh 11-driver heap
- Table 6.7 — Sorting comparison run on 11 ETA values
- Table 6.8 — Edge-case verification results
- Table 6.9 — Frame-time measurements
- Table 7.1 — Limitations, impact, and remediation priority

---

# Chapter 1 — Introduction and Problem Understanding

## 1.1 Background and Domain Context

Karachi is a dense, polycentric city in which mobility is shaped by distance, traffic volatility, and personal safety concerns. For women passengers, these concerns are compounded: the choice of driver, the predictability of pickup, and the existence of a traceable record of the trip often matter as much as price. Ride-hailing applications address part of this problem by digitizing the request, but the quality of a ride-hailing platform is determined by the dispatch decision underneath the interface—how quickly an available driver is found, whether the nearest driver is actually selected, what happens when a driver declines, and whether the platform can explain each of those decisions afterwards.

Pink Wheels is an academic, women-focused ride-hailing platform built for this setting. It is a complete demonstration system rather than a commercial dispatch service: a passenger selects a pickup and destination from well-known Karachi locations or by clicking a live map, receives a transparent fare estimate, and submits a request; the backend then ranks eligible women drivers by estimated arrival time and offers the ride to the best candidate; the driver can accept, reject (which triggers a reassignment cascade), or complete the trip; and every event is written into an auditable activity trail. The central engineering claim of the project is that these behaviours are produced by explicitly implemented data structures and algorithms, not by framework utilities or database shortcuts.

The platform deliberately separates *state that must survive a restart* from *state that is naturally in-memory*. Completed and in-progress rides, fares, and passenger records live in a relational database. The driver registry, candidate priority queues, the live request queue, and the activity stack are implemented as custom data structures in the backend process. This separation is itself a design decision that the report evaluates: it keeps the algorithmic behaviour visible and testable, while making the durability boundary explicit.

## 1.2 Existing Practices and Operational Challenges

Before analysing the proposed system, it is useful to state the operational practices it replaces or improves upon.

**Street hailing and informal pickup points.** A passenger negotiates directly with a driver. There is no availability model, no fare transparency, and no record of the trip. Selection is opportunistic and often biased toward whoever is physically closest to the passenger's line of sight, not necessarily the best match.

**Phone-based dispatch.** A call centre or coordinator receives a request and contacts drivers one by one. The coordinator must remember who is free, estimate travel time mentally, and handle declines sequentially. As the active driver pool grows, the coordinator's working memory becomes the bottleneck, and the process is difficult to audit.

**WhatsApp and social-media coordination groups.** Requests are broadcast to a group. Drivers self-select, which frequently produces duplicate claims, slow responses, and no reliable ordering. There is no deterministic rule for who receives the ride, and no structured history afterwards.

**Spreadsheet-based driver lists.** Some small operators track drivers in spreadsheets. A spreadsheet can list availability, but it cannot rank candidates by distance and ETA in real time, cannot update automatically when a driver declines, and cannot guarantee a consistent tie-breaking rule.

These practices share four weaknesses that map directly onto data-structure and algorithm requirements:

1. **Availability is not represented as a traversable structure**, so finding eligible drivers is a manual scan.
2. **Candidate selection is not algorithmic**, so "nearest" is an estimate rather than a computed Haversine distance and ETA.
3. **Declines are not modelled as a cascade**, so a single rejection often restarts the whole process manually or loses the request.
4. **Events are not recorded in an ordered, retrievable trail**, so disputes and operational reviews depend on memory.

## 1.3 Problem Statement

The problem addressed by Pink Wheels can be stated precisely:

> Design and implement a ride-hailing platform for Karachi in which a passenger request is matched to the eligible driver with the lowest estimated time of arrival, where eligibility and availability are maintained in an explicit data structure, where a rejection automatically advances to the next-best candidate without recomputing the entire candidate set, and where every request, offer, acceptance, rejection, completion, and cancellation is recorded in an ordered audit trail—while keeping the user interface responsive at modern display refresh rates.

The problem is algorithmic before it is visual. The interface must show a ranking, but the ranking must be produced by a defensible structure with predictable complexity. The lifecycle must feel instantaneous, but the backend must enforce state transitions and persist outcomes.

## 1.4 Proposed System Overview

Pink Wheels implements the following end-to-end flow:

1. **Booking.** The passenger selects a pickup and destination from 23 famous Karachi locations (for example, Saddar Empress Market, Clifton Beach, Mazar-e-Quaid, Dolmen Mall Clifton, Jinnah International Airport) or clicks two points on a Leaflet map. The frontend calls the fare-estimation endpoint, which computes Haversine distance and a category-specific fare.
2. **Request intake.** On submission, the backend computes the trip distance and fare, enqueues the request in the custom FIFO queue, persists a ride row, dequeues the request for immediate processing, and logs a `RIDE_REQUESTED` event.
3. **Candidate construction.** The matchmaking service traverses the driver linked list, filters drivers whose `is_available` flag is true, computes Haversine distance and ETA from each driver to the pickup, and pushes each candidate into a custom binary min-heap priority queue keyed by `(eta_minutes, distance_km, driver_id)`.
4. **Offer.** The root of the heap is popped and offered the ride. The ride row changes to `OFFERED`, and a `DRIVER_OFFERED` event is pushed onto the activity stack.
5. **Driver response.** The selected driver accepts—marking themselves busy in the linked list and moving the ride to `ACCEPTED`—or rejects. A rejection pops the next-best candidate from the same heap, logs `RIDE_REJECTED` and `DRIVER_REASSIGNED`, and re-offers the ride. If the heap empties, the ride becomes `NO_DRIVERS_AVAILABLE` and a `MATCHMAKING_EXHAUSTED` event is recorded.
6. **Completion or cancellation.** Completion is permitted only from `ACCEPTED`; it frees the driver, sets the ride to `COMPLETED`, and logs the event. Cancellation is permitted from any non-terminal state, frees the driver if the ride had been accepted, and logs `RIDE_CANCELLED`.

![Passenger ride-booking interface](images/fig02-passenger-booking.png)

*Figure 1.1 — Passenger ride-booking interface. The 23-location Karachi dataset feeds both the pickup and destination selects; the right panel shows the live map, driver positions, and the OSRM road-network route.*

The driver console presents the same lifecycle from the supply side. A driver is selected from the linked list, availability can be toggled, incoming offers are listed, and accepted rides expose a completion action. The console is intentionally a *role simulation*: because the project does not implement authentication, the driver selector identifies which registered driver the operator is acting as.

![Driver dashboard](images/fig04-driver-dashboard.png)

*Figure 1.2 — Driver console showing the active driver, linked-list availability status, pending offers, and one in-progress ride.*

The DSA Demonstration Dashboard exposes the internal structures directly. It visualizes the linked list as a pointer chain, ranks drivers by min-heap priority, shows the activity stack top-down, and replays the five-step matchmaking algorithm. This dashboard is not a decorative extra; it is the primary evidence that the structures described in this report are the structures actually driving the application.

## 1.5 User Roles and Workflows

*Table 1.1 — User roles and responsibilities*

| Role | Interface | Responsibilities | Backend interactions |
|---|---|---|---|
| Passenger | Passenger Home, Ride Status, Ride History | Choose pickup/destination and category, estimate fare, request ride, track status, cancel, review history | `POST /api/rides/estimate-fare`, `POST /api/rides/request`, `GET /api/rides/{id}`, `POST /api/rides/{id}/cancel`, `GET /api/rides` |
| Driver | Driver Console | Choose active driver identity, toggle availability, view offers, accept or reject, complete active ride | `GET /api/drivers`, `PATCH /api/drivers/{id}/availability`, `POST /api/rides/{id}/accept`, `POST /api/rides/{id}/reject`, `POST /api/rides/{id}/complete` |
| DSA administrator / demonstrator | DSA Dashboard | Inspect linked list, heap, stack, and queue; register or delete drivers; change availability; simulate matchmaking | `GET/POST/DELETE /api/drivers`, all `/api/dsa/*` inspection endpoints |

The passenger workflow is deliberately linear, the driver workflow is event-driven (offers arrive from matchmaking), and the administrator workflow is observational. Because the three roles share one backend, the demonstration can show a single ride crossing all three interfaces without any simulated data.

## 1.6 Objectives

The project pursues the following objectives:

1. Represent driver registration and availability with a custom singly linked list that supports insertion, deletion, search, traversal, and status updates.
2. Rank eligible drivers with a custom binary min-heap that exposes `push`, `pop`, `peek`, `heapify`, and priority updates, and that guarantees deterministic ordering under equal ETAs.
3. Implement a rejection cascade in which a declined offer advances to the next-best candidate in $O(\log a)$ while the heap is alive, instead of rebuilding or re-sorting the candidate set.
4. Record every lifecycle event in a custom LIFO stack that returns the most recent event first.
5. Demonstrate FIFO intake with a custom queue, while documenting the difference between the queue's transient role and a persistent backlog.
6. Compute distance, ETA, and fare transparently and consistently across backend and UI.
7. Persist ride and passenger records with parameterized SQL and a SQLite fallback for offline demonstrations.
8. Validate correctness with unit and integration tests and validate the user experience with an end-to-end ride lifecycle and frame-time measurements.
9. Present the internal structures in a live dashboard so that algorithmic behaviour can be inspected rather than inferred.

## 1.7 Scope, Assumptions, and Limitations

**In scope.** Driver registration and availability; 23-location Karachi booking; map-based pickup/destination selection; Haversine distance; ETA with a fixed average speed; three fare categories; min-heap matchmaking; rejection cascade; acceptance, completion, and cancellation; activity audit trail; ride history; DSA visualization; responsive pink-themed UI.

**Out of scope or simplified.** The following limitations are stated explicitly so that the report does not claim behaviour the code does not provide:

- **No authentication or authorization.** There are no user accounts, tokens, or sessions. The driver console selects an identity from a dropdown. Any caller can invoke any endpoint. This is acceptable for a course demonstration but not for production.
- **Driver state is in-memory and reseeded on restart.** The 13 women drivers are loaded from `backend/dsa/sample_drivers.py` when the service module is imported. Registrations and availability changes are lost when the backend restarts, while ride rows remain in SQLite.
- **The activity stack is in-memory and unbounded.** Events are lost on restart, and the stack has no maximum depth or persistence.
- **The FIFO queue is transient, not a backlog.** `request_ride()` enqueues and immediately dequeues within the same call so that FIFO ordering is exercised and visible. There is no worker that drains a backlog, and the dashboard panel for the queue was removed from the UI; the backend queue and its inspection endpoint remain.
- **The chained hash table is implemented but not wired.** `backend/dsa/hash_table.py` provides a custom hash table with chaining, but no route or service imports it; driver lookup still uses the linked list's $O(n)$ search. The report treats it as an implemented-but-unused structure, not as part of the live request path.
- **ETA uses a constant speed.** The service assumes 25 km/h and a two-minute floor; it does not use live traffic, road geometry, or time-of-day models.
- **Distance is great-circle, not road distance.** Haversine gives straight-line kilometres. The frontend draws an OSRM road route for visualization, but matchmaking ranks by Haversine distance, so the displayed road route and the ranking distance are not identical.
- **Single-process concurrency.** The in-memory structures are not protected by locks, and running multiple Uvicorn workers would give each worker a different driver list. The demonstration runs one backend process.
- **No payments, live GPS, or push notifications.** Polling and manual refresh drive the UI updates.
- **PostgreSQL is optional.** The code attempts PostgreSQL when configured and falls back to SQLite after a failed connection, with the fallback cached for the process lifetime.

These limitations do not invalidate the algorithmic claims, because the structures and workflows described in Chapters 4–6 are the ones executed by the live system. They do, however, define the boundary between the academic implementation and a production dispatch platform.

## 1.8 Why Efficient Data Structures and Algorithms Matter Under Load

A ride-hailing dispatch loop is latency-sensitive and request-dense. The relevant load variables are the number of registered drivers $n$, the number of eligible drivers $a \le n$, the number of offer rounds $k$ caused by rejections, and the number of ride records $r$. The cost of a naive implementation grows in ways that are invisible at 13 drivers but become operationally significant at city scale:

- **Linear rescanning per offer.** Recomputing the candidate set for every rejection costs $O(k \cdot n \log n)$ when a heap rebuild is repeated. Keeping the heap alive between offers reduces the cascade to $k \cdot O(\log a)$.
- **Whole-collection sorting for a single winner.** Sorting all candidates to find one best driver costs $\Theta(a \log a)$ even when only the minimum is needed. A heap build plus one extraction costs $O(a)$ if built with heapify (or $O(a \log a)$ with sequential pushes, as the current implementation does) plus $O(\log a)$ for the extraction; subsequent extractions are $O(\log a)$ each.
- **Quadratic list maintenance.** Appending to a singly linked list without a tail pointer requires a full traversal, so $n$ registrations cost $O(n^2)$. The microbenchmark in Chapter 5 shows this concretely: 1,000 appends take about 17 ms, 2,000 take about 65 ms, and 5,000 take about 362 ms. A tail pointer would make append $O(1)$.
- **Audit-trail growth.** A LIFO stack gives $O(1)$ event insertion and $O(1)$ access to the most recent event, which is exactly what an operator needs during an active ride. A database write per event would add I/O latency to every state transition.
- **UI frame budget.** The frontend must not perform heavy synchronous work during scrolling or hover. The measured budget for 120 Hz is 8.33 ms per frame; the implemented pages stay well inside it by using transform/opacity-only transitions, one-shot reveal observers, and diffs in polling responses.

The project therefore treats complexity as an operational property, not only an exam topic. Chapter 5 quantifies every operation; Chapter 6 connects the numbers to the live dataset.

## 1.9 CLO 2 and CLO 3 Alignment

*Table 1.2 — CLO 2 and CLO 3 mapping*

| CLO | Expected behaviour | How this project demonstrates it | Evidence |
|---|---|---|---|
| CLO 2 — Problem Analysis | Analyse a complex engineering problem, decompose requirements, select appropriate techniques, and justify choices with complexity and trade-off reasoning | Formulated the dispatch problem in terms of availability, ranking, cascading rejection, and auditability; mapped each requirement to a structure; derived best/average/worst cases; compared heap extraction with Bubble and Quick Sort; evaluated memory and concurrency limitations | Chapters 1, 2, 5; Tables 2.4–2.5, 5.2–5.6 |
| CLO 3 — Individual and Teamwork | Work effectively in a team, define interfaces, integrate components, and verify the integrated result | Separated the DSA layer, service layer, API layer, persistence layer, and Vue presentation layer; agreed on a single service API used by all routes; divided design, implementation, verification, and documentation; validated with 48 tests and an end-to-end lifecycle walkthrough | Chapters 3, 6; Tables 2.1, 2.6, 6.4, 6.8; Section 6.10 |

The CLO mapping is not retrospective labelling: each chapter produces an artifact that a reviewer can inspect. The requirement matrix in Chapter 2 is the analysis artifact, the API contract and layer diagram in Chapter 3 are the teamwork artifacts, and the traces and measurements in Chapter 6 are the verification artifacts.

---

# Chapter 2 — Requirement Identification and System Analysis

## 2.1 Functional Requirements

Functional requirements were derived from the three user roles and from the algorithmic behaviours the project must demonstrate. Each requirement is mapped to the module that satisfies it and to the interface through which a reviewer can observe it.

*Table 2.1 — Functional requirements and implementation mapping*

| ID | Requirement | Implementation | Observable through |
|---|---|---|---|
| FR-01 | Register a driver in a singly linked list | `DriverLinkedList.append()` in `dsa/linked_list.py`; `POST /api/drivers/register` | DSA linked-list tab; `GET /api/drivers` |
| FR-02 | Insert a driver at a specific index | `DriverLinkedList.insert()` | Unit tests; service availability |
| FR-03 | Delete a driver by identifier | `DriverLinkedList.delete()`; `DELETE /api/drivers/{id}` | Node-management table |
| FR-04 | Search a driver by identifier | `DriverLinkedList.search()`; `GET /api/drivers/{id}` | Search box in linked-list tab |
| FR-05 | Toggle driver availability | `DriverLinkedList.update_availability()`; `PATCH /api/drivers/{id}/availability` | Driver console; linked-list status chips |
| FR-06 | Estimate trip distance and fare without booking | `haversine_distance()`, `calculate_fare()`; `POST /api/rides/estimate-fare` | Passenger fare card |
| FR-07 | Submit a ride request and run matchmaking | `request_ride()`; `POST /api/rides/request` | Booking flow; Ride Status page |
| FR-08 | Rank eligible drivers by ETA and distance | `DriverPriorityQueue`; `GET /api/dsa/priority-queue` | Priority-queue tab |
| FR-09 | Offer the ride to the best driver | Root extraction in `request_ride()` | Driver console offer list |
| FR-10 | Accept an offer and mark driver busy | `accept_ride()` | Ride Status; driver active rides |
| FR-11 | Reject an offer and reassign to the next candidate | `reject_ride()` | Cascade walkthrough; activity stack |
| FR-12 | Mark an accepted ride complete and free the driver | `complete_ride()` | Driver console; passenger history |
| FR-13 | Cancel a pending, offered, or accepted ride | `cancel_ride()` | Ride Status page |
| FR-14 | Record lifecycle events in LIFO order | `ActivityStack.push()`; `GET /api/dsa/stack` | LIFO tab |
| FR-15 | Demonstrate FIFO request intake | `RideQueue.enqueue()/dequeue()`; `GET /api/dsa/queue` | API inspection |
| FR-16 | Simulate the five-step matchmaking algorithm | `POST /api/dsa/matchmaking` | Matchmaking-flow tab |
| FR-17 | List rides and enrich them with driver details | `GET /api/rides`, `GET /api/rides/{id}` | History table; status page |
| FR-18 | Manage passenger records | `GET/POST /api/passengers` | API |
| FR-19 | Report service and database health | `GET /api/health` | Navbar/footer health indicator |
| FR-20 | Provide a responsive booking UI with 23 Karachi locations and map selection | `Home.vue`, `RideMap.vue`, `PRESET_LOCATIONS` | Passenger interface |
| FR-21 | Display ride status and history with category-specific fares | `RideStatus.vue`, `RideHistory.vue` | Passenger pages |

Two implementation details deserve emphasis because they affect requirement interpretation. First, FR-10 and FR-11 are guarded by the ride state and by the offered driver's identity: a driver who was not the current offeree cannot accept or reject, and a ride in a terminal state cannot be acted on again. Second, FR-07 persists the ride *before* matchmaking selects a driver, so a ride row can exist without a driver identifier; this is what makes the rejection and cancellation flows auditable.

## 2.2 Non-Functional Requirements

*Table 2.2 — Non-functional requirements and verification evidence*

| ID | Quality attribute | Requirement | Evidence |
|---|---|---|---|
| NFR-01 | Performance (backend) | Candidate ranking for 11 drivers should complete in single-digit milliseconds on a laptop-class machine | `POST /api/dsa/matchmaking` measured at 3.77–4.44 ms over five runs |
| NFR-02 | Performance (frontend) | Every page should stay inside the 8.33 ms frame budget of a 120 Hz display in steady state | p99 frame time 0.8–2.1 ms unthrottled; 5.1–6.6 ms at 4× CPU throttle; 0 frames over budget in confirmation runs |
| NFR-03 | Smoothness | Interactions must not trigger layout thrash or long main-thread tasks during scroll/hover | 0–1 layouts per benchmark segment; hover paint 1.8 ms; animations limited to transform/opacity |
| NFR-04 | Reliability | The service must start without an external database server and must not corrupt state on invalid actions | SQLite fallback; parameterized SQL; HTTP 404/409 state guards; 48 tests |
| NFR-05 | Security | All SQL must be parameterized; input must be schema-validated; the demo must not claim credential security it does not provide | `%s`/`?` placeholders; Pydantic models; CORS with credentials disabled; explicit no-auth limitation |
| NFR-06 | Usability | The interface must be readable, responsive, and operable at mobile width | Light-pink theme; 390 px viewport with zero horizontal overflow; labelled controls; visible status chips |
| NFR-07 | Maintainability | Structures, services, routes, and persistence must be separated and documented | `dsa/`, `services/`, `routes/`, `database.py`; docstrings; single-responsibility modules |
| NFR-08 | Scalability | Dispatch cost should grow near-linearly in the driver count, not quadratically | $O(n + a \log a)$ request path; heap cascade $O(\log a)$; microbenchmarks in Section 5.8 |
| NFR-09 | Portability | The system should run on Windows and Linux with standard Python and Node toolchains | Python 3.14.7, Node 24.18.0, SQLite; no native services required |
| NFR-10 | Observability | The system should expose liveness, database engine, ranking, and audit state | `/api/health`, `/api/dsa/priority-queue`, `/api/dsa/stack` |

NFR-02 deserves a note on interpretation. A browser presents frames at the display's refresh rate; a 60 Hz panel shows at most 60 frames per second regardless of application headroom. The measurements in this report use an uncapped headless Chrome to quantify *available headroom* against the 8.33 ms budget that a 120 Hz display would impose. No synthetic or cosmetic FPS counter was added to the UI.

## 2.3 Hardware and Software Stack

*Table 2.3 — Hardware and software stack*

| Layer | Technology | Version / detail |
|---|---|---|
| Backend language | Python | 3.14.7 (virtual environment) |
| API framework | FastAPI | ≥ 0.115 |
| ASGI server | Uvicorn | ≥ 0.34 |
| Validation | Pydantic | ≥ 2.10 |
| Database driver | psycopg | ≥ 3.2 (optional PostgreSQL) |
| Default database | SQLite | file `backend/pink_wheels_dsa.db` |
| Config | python-dotenv | `.env` / `DATABASE_URL` |
| Backend tests | pytest, httpx | 48 test cases across 7 modules |
| Frontend framework | Vue | 3.5.44 |
| Build tool | Vite | 8.3.6 |
| Styling | Tailwind CSS | 4.3.4 via `@tailwindcss/vite` |
| State management | Pinia | 4.1 |
| Routing | Vue Router | 5.4 |
| HTTP client | Axios | 1.21 |
| Maps | Leaflet | 1.9.4 with Esri World Light Gray tiles |
| Routing service | OSRM public demo | fallback to straight line |
| Icons | lucide-vue-next | 1.0 |
| Test host | AMD Ryzen 7 7445HS, 15.2 GB RAM, RTX 4050 Laptop GPU | Windows 11 build 26200, x64 |
| Verification browser | Headless Chrome via CDP | uncapped rAF for headroom measurement |

## 2.4 Data Structure and Algorithm Inventory

This section is the core of the requirement analysis: it maps every structure and algorithm to its file, its operations, its role, and its actual status in the running system. The distinction between *active*, *implemented but not wired*, and *design-level* is essential; the report does not present an implemented-but-unused structure as a live feature.

*Table 2.4 — Data structure inventory and module mapping*

| Structure | File and class | Operations implemented | Live request path? | Role in the system |
|---|---|---|---|---|
| Singly linked list | `backend/dsa/linked_list.py` — `DriverNode`, `DriverLinkedList` | `append`, `insert(index)`, `delete`, `search`, `traverse`, `display`, `size`, `update_availability`, `get_available_drivers` | Yes | Driver registry, availability state, candidate source, driver-name enrichment for ride rows |
| Binary min-heap priority queue | `backend/dsa/priority_queue.py` — `DriverPriorityQueue` | `_parent`, `_left_child`, `_right_child`, `_is_higher_priority`, `_sift_up`, `_sift_down`, `push`, `pop`, `peek`, `is_empty`, `size`, `heapify`, `update_priority`, `display` | Yes (`push`, `pop`, `peek`, `display`; `heapify` and `update_priority` are currently unused by the service) | Ranking eligible drivers, selecting the best candidate, driving the rejection cascade |
| LIFO stack | `backend/dsa/stack.py` — `StackNode`, `ActivityStack` | `push`, `pop`, `peek`, `is_empty`, `size`, `display` | Yes (`push`, `display`, `peek`; `pop` is not called by any route) | Activity history and audit trail, most-recent-first |
| FIFO queue | `backend/dsa/queue.py` — `QueueNode`, `RideQueue` | `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `display` | Yes (enqueue and immediate dequeue in `request_ride`; display via inspection API) | Demonstrates FIFO intake; holds a request only for the duration of the request transaction |
| Chained hash table | `backend/dsa/hash_table.py` — `HashNode`, `DriverHashTable` | `_hash`, `put`, `get`, `delete`, `size`, `display_buckets` | No | Implemented academic alternative for $O(1)$ average driver lookup; not imported by any route or service |
| Dictionary (language container) | `services/matchmaking.py` — `active_ride_pqs` | Insert, lookup, remove keyed by ride id | Yes | Maps each active ride to its live candidate heap |
| Set (language container) | `services/matchmaking.py` — `excluded_driver_ids` | Membership, insertion | Yes | Excludes the rejecting driver when a heap is rebuilt after a restart |

*Table 2.5 — Algorithm inventory and module mapping*

| Algorithm / calculation | Location | Inputs → Outputs | Used by |
|---|---|---|---|
| Haversine distance | `services/matchmaking.py` — `haversine_distance()` | `(lat1, lon1, lat2, lon2)` → kilometres, rounded to 2 dp | Fare estimation, candidate ETA, trip distance |
| ETA estimation | `calculate_eta()` | distance km, speed (default 25 km/h) → minutes, minimum 2.0, 1 dp | Candidate ranking, offer description |
| Fare calculation | `calculate_fare()` | distance km, vehicle type → base fare, rate, distance charge, total | Fare estimate, ride record |
| Candidate construction | `build_priority_queue_for_ride()` | pickup coordinates, excluded set → heap of eligible drivers | Request flow, rejection rebuild, DSA ranking |
| Best-driver selection | `request_ride()` | heap → root candidate | Offer creation |
| Rejection cascade | `reject_ride()` | ride id, driver id → next offer or exhaustion | Driver decline handling |
| Acceptance transition | `accept_ride()` | ride id, driver id → `ACCEPTED` state | Driver acceptance |
| Completion transition | `complete_ride()` | ride id → `COMPLETED` state and freed driver | Trip completion |
| Cancellation transition | `cancel_ride()` | ride id → `CANCELLED` state | Passenger cancellation |
| Activity logging | `ActivityStack.push()` calls throughout the service | event dict → LIFO top | Audit trail |
| State validation and error mapping | `accept_ride`, `reject_ride`, `complete_ride`, `cancel_ride`; `routes/rides.py` | invalid state → `RideStateError` → HTTP 409; missing ride → 404 | All lifecycle endpoints |
| Bubble Sort (early exit) | Design-level only; not in the repository | list of candidates → sorted list | Comparison in Chapter 5 |
| Quick Sort (Lomuto partition) | Design-level only; not in the repository | list of candidates → sorted list | Comparison in Chapter 5 |

## 2.5 Implemented Versus Design-Level Scope

The CEP brief expects a clear separation between what the system executes and what the team evaluated as an alternative. Pink Wheels makes the following distinctions:

**Implemented and active.** Singly linked list, binary min-heap priority queue, LIFO stack, FIFO queue intake, Haversine distance, ETA, fare calculation, matchmaking, rejection cascade, acceptance, completion, cancellation, state validation, SQLite persistence with PostgreSQL fallback, activity logging, and the DSA inspection API.

**Implemented but not wired.** The chained hash table is complete and documented, but no module imports it. Its purpose is to demonstrate an $O(1)$ average lookup alternative to the linked list's $O(n)$ search. The report recommends wiring it in Chapter 7; it does not claim that the live lookup is constant-time.

**Implemented but not exercised by the service.** `DriverPriorityQueue.heapify()` and `update_priority()` are implemented and unit-tested, but `build_priority_queue_for_ride()` builds the heap with repeated `push()` calls, and no workflow updates a candidate's priority in place. The report therefore analyses the build path as $O(a \log a)$, not $O(a)$, while noting that switching to `heapify()` would improve the constant and the asymptotic build term.

**Design-level only.** Bubble Sort with early exit and Quick Sort are written as complete pseudocode for comparison. Neither is called by the application. The system does not need a general-purpose sort for dispatch: it needs repeated minimum extraction, which is exactly what the heap provides.

**CEP DSA categories not used, and why.** The system does not implement binary search trees, AVL/red-black trees, graphs, Dijkstra/A*, dynamic programming, or tries. There is no graph structure in the backend; the frontend requests a road route from OSRM for display, but that route is an external service call, not a student-implemented shortest-path algorithm. A balanced tree could replace the linked list for lookup, and a spatial index (k-d tree or geohash) could accelerate nearest-driver search at scale; both are discussed as future work rather than falsely presented as implemented. The absence of these categories is a scope decision, not an oversight: the project's algorithmic thesis is the linked-list-to-heap pipeline and its cascade behaviour.

## 2.6 API Surface

*Table 2.6 — REST API surface*

| Method | Endpoint | Purpose | Primary module |
|---|---|---|---|
| GET | `/` | Project metadata and endpoint list | `main.py` |
| GET | `/api/health` | Liveness and active database engine | `main.py`, `database.py` |
| GET | `/api/drivers` | Traverse the driver linked list | `routes/drivers.py` |
| POST | `/api/drivers/register` | Append a driver; auto-assign max ID + 1 if omitted; reject duplicate explicit ID | `routes/drivers.py` |
| GET | `/api/drivers/{id}` | Search the linked list | `routes/drivers.py` |
| DELETE | `/api/drivers/{id}` | Delete a driver node | `routes/drivers.py` |
| PATCH | `/api/drivers/{id}/availability` | Set `is_available` | `routes/drivers.py` |
| GET | `/api/passengers` | List passengers | `routes/passengers.py` |
| POST | `/api/passengers` | Create a passenger | `routes/passengers.py` |
| POST | `/api/rides/estimate-fare` | Haversine distance and fare without booking | `routes/rides.py` |
| POST | `/api/rides/request` | Persist, enqueue/dequeue, match, and offer | `routes/rides.py` |
| GET | `/api/rides` | List rides, optionally filtered by status | `routes/rides.py` |
| GET | `/api/rides/{id}` | Ride detail with driver enrichment | `routes/rides.py` |
| POST | `/api/rides/{id}/accept` | Driver acceptance | `routes/rides.py` |
| POST | `/api/rides/{id}/reject` | Rejection and cascade | `routes/rides.py` |
| POST | `/api/rides/{id}/complete` | Completion and driver release | `routes/rides.py` |
| POST | `/api/rides/{id}/cancel` | Cancellation and driver release | `routes/rides.py` |
| GET | `/api/dsa/linked-list` | Linked-list inspection | `routes/dsa.py` |
| GET | `/api/dsa/queue` | FIFO queue inspection | `routes/dsa.py` |
| GET | `/api/dsa/priority-queue?lat=&lon=` | Heap array and sorted priority order for a coordinate | `routes/dsa.py` |
| GET | `/api/dsa/stack` | Stack depth, top, and top-down items | `routes/dsa.py` |
| POST | `/api/dsa/matchmaking` | Five-step algorithm simulation | `routes/dsa.py` |

All write endpoints validate their payloads with Pydantic models. The service layer raises `RideNotFoundError` for missing rides and `RideStateError` for invalid transitions; the ride router converts these into HTTP 404 and 409 respectively. This separation keeps HTTP concerns out of the algorithms and makes the service directly testable.

---

# Chapter 3 — System Design and Architecture

## 3.1 Architectural Style and Layers

Pink Wheels uses a layered client–server architecture with a deliberately thin presentation layer and a deliberately explicit algorithm layer. The backend is stateless with respect to HTTP: every route delegates to a service function, and the service owns the in-memory data structures and the database calls. This keeps the algorithms independent of FastAPI, which is why the same functions can be exercised directly by the test suite and by the DSA simulation endpoint.

```
+--------------------------------------------------------------------------+
| PRESENTATION LAYER — Vue 3 SPA (Vite, Tailwind CSS, Leaflet)             |
| Landing | Passenger Home | Ride Status | History | Driver | DSA Dashboard|
+------------------------------------+-------------------------------------+
                                     | Axios JSON over HTTP
                                     v
+--------------------------------------------------------------------------+
| API LAYER — FastAPI routers with Pydantic validation                     |
| /api/drivers | /api/passengers | /api/rides | /api/dsa | /api/health     |
| 400 validation, 404 missing ride, 409 invalid state                      |
+------------------------------------+-------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
| SERVICE / ALGORITHM LAYER — services/matchmaking.py                      |
| Haversine -> ETA -> Fare -> Request -> Candidate heap -> Offer ->        |
| Accept / Reject cascade / Complete / Cancel -> Activity log              |
+-------------------+----------------------------------+-------------------+
                    |                                  |
                    v                                  v
+-----------------------------------+   +----------------------------------+
| DSA LAYER — backend/dsa           |   | PERSISTENCE — database.py        |
| DriverLinkedList   (registry)     |   | SQLite (default) / PostgreSQL    |
| DriverPriorityQueue(min-heap)     |   | passengers, rides                |
| ActivityStack      (LIFO audit)   |   | parameterized SQL, auto-fallback |
| RideQueue          (FIFO intake)  |   +----------------------------------+
| DriverHashTable    (not wired)    |
+-----------------------------------+
```

*Table 3.1 — Layer responsibilities*

| Layer | Owns | Must not own | Key files |
|---|---|---|---|
| Presentation | Rendering, user input, map interaction, polling, client-side routing | Business rules, ranking, persistence | `frontend/src/pages`, `components/common`, `services/api.js`, `router/index.js` |
| API | HTTP verbs, paths, request/response schemas, status-code mapping | Algorithm logic, SQL | `backend/routes/*.py`, `backend/main.py` |
| Service / algorithm | Matchmaking, lifecycle rules, distance/ETA/fare, logging, coordination | HTTP concerns, DOM concerns | `backend/services/matchmaking.py` |
| DSA | Structure invariants and operations | Database schema, HTTP | `backend/dsa/*.py` |
| Persistence | Connection management, SQL execution, schema initialization, fallback | Business state machines | `backend/database.py` |

![DSA demonstration dashboard](images/fig05-dsa-dashboard.png)

*Figure 3.1 — DSA Demonstration Dashboard. The four tabs expose the linked list, the priority queue, the LIFO stack, and the matchmaking replay; the linked-list tab is shown with all 13 registered nodes.*

## 3.2 Component Responsibilities

**Frontend application shell.** `App.vue` provides the navbar, footer, background, and route-reveal behaviour. `main.js` installs Pinia and Vue Router and imports Leaflet styles. `services/api.js` centralizes every backend call, so endpoint changes are made in one file. `stores/health.js` wraps the health check used by the shell.

**Passenger pages.** `Home.vue` owns the 23-location dataset, pickup/destination selection, category selection, fare estimation, route drawing, and ride submission. `RideStatus.vue` polls the ride record and renders the current status with a category-specific banner; it also exposes cancellation. `RideHistory.vue` lists persisted rides with driver and fare details.

**Driver page.** `DriverDashboard.vue` reads the linked list to populate the identity selector, toggles availability, lists offered rides, and completes accepted rides. Its polling compares the new list with the previous one before updating reactive state, and skips work when the document is hidden.

**DSA dashboard.** `DsaDashboard.vue` is an administrative inspection surface with four tabs: linked list (visual pointer chain, registration form, search/delete/toggle table), priority queue (reference pickup, heap ranking, heap array), LIFO stack (top-down event audit), and matchmaking flow (five-step replay with the selected winner).

**Backend routers.** The driver router mutates the linked list; the ride router maps service exceptions to HTTP status codes; the DSA router exposes read-only inspections and a matchmaking simulation; the health route reports the active database engine.

**Service layer.** `services/matchmaking.py` is the single authority for ride lifecycle. It constructs the global singletons at import time, defines the geographic and fare utilities, builds candidate heaps, and implements the request/accept/reject/complete/cancel workflows. It raises typed errors so that callers do not need to inspect strings.

**Persistence layer.** `database.py` hides the difference between SQLite and PostgreSQL behind `execute_query()` and `execute_commit()`, translates `%s` placeholders to `?` for SQLite, initializes both schemas, seeds three demo passengers, and caches the PostgreSQL fallback decision.

## 3.3 Data Model and Relationships

The durable model has two tables. The in-memory model has four custom structures plus a dictionary of active heaps.

*Table 3.2 — `passengers` table*

| Column | Type (SQLite) | Constraints | Meaning |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Passenger identifier |
| `name` | TEXT | NOT NULL | Display name |
| `phone` | TEXT | NOT NULL | Contact number (not used for authentication) |

*Table 3.3 — `rides` table*

| Column | Type (SQLite) | Constraints | Meaning |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Ride identifier used by lifecycle endpoints |
| `passenger_id` | INTEGER | nullable | Passenger who requested the ride |
| `driver_id` | INTEGER | nullable | Current or assigned driver |
| `pickup_location` | TEXT | NOT NULL | Human-readable pickup label |
| `destination` | TEXT | NOT NULL | Human-readable destination label |
| `pickup_latitude` | REAL | NOT NULL | Pickup coordinate |
| `pickup_longitude` | REAL | NOT NULL | Pickup coordinate |
| `destination_latitude` | REAL | NOT NULL | Destination coordinate |
| `destination_longitude` | REAL | NOT NULL | Destination coordinate |
| `distance_km` | REAL | default 0.0 | Haversine trip distance |
| `fare` | REAL | default 0.0 | Computed total fare in PKR |
| `vehicle_type` | TEXT | default `'Bike'` | Category passed to fare calculation |
| `status` | TEXT | NOT NULL default `'PENDING'` | Lifecycle state |
| `created_at` | TEXT | default CURRENT_TIMESTAMP | Row creation timestamp |

The two tables have no declared foreign-key constraints and no secondary indexes beyond the primary keys. The relationship is logical rather than enforced: `rides.passenger_id` references `passengers.id`, and `rides.driver_id` references an in-memory linked-list node. This asymmetry is intentional for the demonstration but is a documented limitation: deleting a driver from the linked list does not update historical ride rows, which then display a fallback label such as `Driver #113`.

The in-memory state is owned by the service module:

- `driver_list` — a `DriverLinkedList` seeded with 13 drivers at import time.
- `ride_queue` — a `RideQueue` used for transient FIFO intake.
- `activity_stack` — an `ActivityStack` seeded with a `SYSTEM_STARTUP` event.
- `active_ride_pqs` — a Python dictionary mapping `ride_id` to the heap that was built for that ride.

*Table 3.4 — State ownership and lifetime*

| State | Structure | Lifetime | Survives restart? | Consistency mechanism |
|---|---|---|---|---|
| Driver registry and availability | Singly linked list | Process | No (reseeded) | Mutated only through service functions |
| Ride request intake | FIFO queue | Per request | No | Enqueue followed by dequeue in the same call |
| Candidate ranking | Min-heap per active ride | Request until accept/complete/cancel | No | Stored in `active_ride_pqs` |
| Activity trail | LIFO stack | Process | No | Every lifecycle function pushes exactly one or more events |
| Ride and passenger records | SQLite/PostgreSQL | Durable | Yes | Parameterized SQL |
| Excluded-driver set for rebuild | Python set | Per reject rebuild | No | Constructed from the rejecting driver only |

## 3.4 Ride State Machine

A ride is created in `PENDING` and normally transitions to `OFFERED` within the same request call. The states and guards are:

*Table 3.5 — Ride state transitions and guards*

| From | Event | To | Guard / precondition | Side effects |
|---|---|---|---|---|
| — | Request inserted | `PENDING` | Valid coordinates and vehicle type | Row inserted, request enqueued/dequeued, `RIDE_REQUESTED` logged |
| `PENDING` | Best driver found | `OFFERED` | Heap non-empty | Driver stored, `DRIVER_OFFERED` logged |
| `PENDING` | No driver found | (row remains `PENDING`; response says `NO_DRIVERS_AVAILABLE`) | Heap empty | No row update; documented inconsistency |
| `OFFERED` | Driver rejects | `OFFERED` (new driver) | Rejecting driver is the current offeree | Heap pop, driver updated, `RIDE_REJECTED` and `DRIVER_REASSIGNED` logged |
| `OFFERED` | Last candidate rejects | `NO_DRIVERS_AVAILABLE` | Heap empty | `MATCHMAKING_EXHAUSTED` logged |
| `OFFERED`/`PENDING` | Driver accepts | `ACCEPTED` | Driver registered; offered driver matches if set | Driver marked busy, `RIDE_ACCEPTED` logged, heap removed |
| `ACCEPTED` | Driver completes | `COMPLETED` | Status is exactly `ACCEPTED` (repeat completion is idempotent) | Driver marked available, `RIDE_COMPLETED` logged, heap removed |
| Any non-terminal | Cancel | `CANCELLED` | Status is not already `CANCELLED` or `COMPLETED` | Driver freed only if status was `ACCEPTED`, `RIDE_CANCELLED` logged |

The state machine is enforced in the service layer rather than in the database. This gives precise error messages and keeps the logic testable, but it also means the database alone cannot reject an invalid transition if a future caller bypasses the service. The most important gap is that `accept_ride()` does not explicitly require `OFFERED`; it rejects terminal and already-accepted states and then checks the driver, so a `PENDING` ride with no assigned driver could be accepted by any registered driver. In practice `PENDING` is transient, but the report records the gap in Section 4.11 and Chapter 7 rather than presenting the guard as complete.

```
                      reject + next candidate
                 +----------------------------+
                 |                            v
[PENDING] ---> [OFFERED] ----------------> [OFFERED]
    |              |  |                          |
    | accept       |  | reject + empty heap      |
    v              |  +--> [NO_DRIVERS_AVAILABLE]|
[ACCEPTED] <-------+                             |
    |                                            |
    | complete                                   |
    v                                            |
[COMPLETED]                                      |
                                                 |
 any non-terminal + cancel --> [CANCELLED] <-----+
```

## 3.5 Authentication, Roles, and Authorization

The system has no authentication layer. The frontend exposes three navigation targets—Passenger, Driver, and DSA Dashboard—and the backend trusts the payload. The driver console's dropdown is the identity mechanism: selecting Hina Tariq sends `driver_id: 102` when accepting or rejecting. Consequently:

- There is no protection against a passenger calling a driver endpoint or a driver viewing the DSA dashboard.
- There is no token, password, session, or role claim to validate.
- CORS is configured with `allow_origins=["*"]` and `allow_credentials=False`, which is appropriate for a local demonstration and explicitly not suitable for production.

The report treats this as an accepted academic limitation. It does not claim that role separation is enforced. The role model still matters for teamwork and usability: it defines which interface exercises which lifecycle endpoint, and it makes the demonstration legible.

## 3.6 Data Flow Diagrams

**Context diagram (Level 0).**

```
 Passenger                  +-----------------------------+
   |  pickup, destination   |                             |
   |  category, request     |      PINK WHEELS SYSTEM     |----> Fare, status,
   +----------------------->|   booking + matchmaking     |      offer result
                            |   + ride lifecycle          |
 Driver                    |   + activity audit          |----> Offer, reassignment,
   |  accept / reject /     |                             |      completion result
   |  complete              |                             |
   +----------------------->|                             |
                            +--------------+--------------+
                                           |
 DSA administrator                         | rides, passengers
   |  inspect / simulate                    v
   +----------------------------------> [SQLite / PostgreSQL]
```

**Level 1 — booking and matchmaking.**

```
 Passenger --(pickup, destination, category)--> 1.0 Estimate Fare
                                                    |
                                                    v
                                            distance, fare --> Passenger
 Passenger --(request)--> 2.0 Request Intake --> D1 rides (INSERT PENDING)
                              |  |  |
                              |  |  +--> 2.1 FIFO Queue (enqueue/dequeue)
                              |  |
                              |  +-----> 2.2 Activity Stack (RIDE_REQUESTED)
                              |
                              +--------> 3.0 Candidate Construction
                                           | traverse D2 Driver Linked List
                                           | filter available
                                           | Haversine + ETA
                                           v
                                         D3 Min-Heap (push candidates)
                                           |
                                           v
                                         4.0 Offer Selection (pop root)
                                           |
                                           +--> D1 rides (UPDATE OFFERED)
                                           +--> D2 driver stays available until accept
                                           +--> D4 Activity Stack (DRIVER_OFFERED)
```

**Level 1 — driver response.**

```
 Driver --(accept)--> 5.0 Acceptance --> validate state and identity
                                        --> D2: mark driver busy
                                        --> D1: UPDATE ACCEPTED
                                        --> D4: RIDE_ACCEPTED

 Driver --(reject)--> 6.0 Rejection --> D4: RIDE_REJECTED
                                        --> pop next from D3
                                        --> if candidate: D1 UPDATE OFFERED, D4 REASSIGNED
                                        --> if empty: D1 NO_DRIVERS_AVAILABLE, D4 EXHAUSTED

 Driver --(complete)--> 7.0 Completion --> D2: mark driver available
                                         --> D1: UPDATE COMPLETED
                                         --> D4: RIDE_COMPLETED
```

## 3.7 Request and Match Sequence

The following sequence summarizes the exact order of operations in `request_ride()`. The order matters for auditability: the ride row exists before the offer, and the request is logged before matchmaking runs.

```
Passenger UI      Ride API           Service                 DSA / Database
     |               |                  |                         |
     | POST /request |                  |                         |
     |-------------->| request_ride()   |                         |
     |               |----------------->| trip = Haversine(...)   |
     |               |                  | fare = calculate_fare() |
     |               |                  | RideQueue.enqueue()     |
     |               |                  |------------------------>| FIFO queue
     |               |                  | INSERT ride PENDING     |
     |               |                  |------------------------>| rides
     |               |                  | RideQueue.dequeue()     |
     |               |                  |------------------------>| FIFO queue
     |               |                  | ActivityStack.push()    |
     |               |                  |------------------------>| RIDE_REQUESTED
     |               |                  | build_pq(pickup)        |
     |               |                  |-- traverse driver list ->|
     |               |                  |   Haversine + ETA       |
     |               |                  |   heap.push(candidate)  |
     |               |                  | best = heap.pop()       |
     |               |                  | UPDATE ride OFFERED     |
     |               |                  |------------------------>| rides
     |               |                  | ActivityStack.push()    |
     |               |                  |------------------------>| DRIVER_OFFERED
     |               |<-----------------| result + remaining size |
     |<--------------|                  |                         |
```

## 3.8 Key Algorithm Flowchart — Candidate Construction and Offer

The matchmaking pipeline is the central algorithm of the system. Chapter 4 provides the full pseudocode; this section fixes the control flow and every branch.

```
START
  |
  v
INPUT pickup latitude, pickup longitude, excluded driver set
  |
  v
pq <- empty min-heap; current <- driver_list.head
  |
  v
+-----------------------+
| current != NULL ?     |---- NO ---> RETURN pq
+-----------------------+
  | YES
  v
+------------------------------------------+
| current.is_available AND                 |---- NO ---> current <- current.next
| current.id NOT IN excluded ?             |             (loop)
+------------------------------------------+
  | YES
  v
d <- HAVERSINE(current position, pickup)
eta <- ETA(d)
candidate <- {id, name, phone, vehicle, lat, lon, d, eta}
  |
  v
pq.push(candidate)          // O(log a)
  |
  v
current <- current.next
  |
  +-----------------------> back to loop test
```

After the heap is built, `request_ride()` performs `best <- pq.pop()`. If `best` is `NULL`, no offer is made; if it is a candidate, the ride row is updated to `OFFERED` with the candidate's identifier and a `DRIVER_OFFERED` event is logged. The remaining heap stays in `active_ride_pqs[ride_id]` so that a rejection can continue from the next-best candidate without rebuilding.

## 3.9 Presentation Architecture and Performance Design

The frontend is a single-page application with six routes (four primary pages plus redirects). It deliberately avoids heavy rendering patterns that would undermine the 120 Hz objective:

- **Compositor-friendly motion.** Interactive transitions are limited to `transform` and `opacity`. Decorative glows are static CSS gradients, and backdrop blur is not used.
- **One-shot reveal observers.** Sections reveal with an `IntersectionObserver` that adds a class once and stops observing; scrolling does not trigger per-frame JavaScript.
- **CSS scroll progress.** The top progress bar uses `animation-timeline: scroll(root block)`, so its progress is computed by the compositor rather than by a scroll listener.
- **Diffed polling.** Driver and ride polling compare the incoming payload with the previous state and skip reactive writes when nothing changed; polling is suspended while `document.hidden` is true.
- **Paint containment.** The decorative aurora layer uses `contain: paint style` so its large radial gradients cannot invalidate paint outside their box.
- **Map discipline.** Leaflet tiles are loaded from Esri's light-gray base and reference layers; markers are custom `divIcon`s; the route is a polyline from the OSRM demo service with a straight-line fallback. Map work is isolated to the map component.

These choices are architecture, not polish. They determine whether the measured frame times in Chapter 6 are achievable, and they explain why the UI can be visually rich without a rendering penalty.

---

# Chapter 4 — Algorithm Design Document

## 4.1 Purpose and Coverage

This chapter specifies every algorithm and data-structure operation that the Pink Wheels backend executes, plus the two design-level sorting algorithms used for comparison. The specification is written so that a reader can reproduce the implementation without reading Python: each routine states its input, output, numbered steps, boundary conditions, and source location. Composite workflows are then specified in terms of the primitive operations, which mirrors the actual call graph in `services/matchmaking.py`.

The chapter covers:

1. Singly linked list operations used for driver registration and availability.
2. Binary min-heap operations used for candidate ranking and cascading extraction.
3. LIFO stack operations used for the activity trail.
4. FIFO queue operations used for request intake.
5. Chained hash table operations, clearly marked as implemented but not wired.
6. Haversine distance, ETA, and fare calculations.
7. The request, offer, acceptance, rejection, completion, and cancellation workflows.
8. Bubble Sort with early exit and Quick Sort (Lomuto), as design-level comparisons.
9. Edge cases, tie-breakers, and structural invariants.
10. Flowcharts for the heap operations, the rejection cascade, and the ride lifecycle.

## 4.2 Pseudocode Conventions

The following conventions are used consistently:

- `←` denotes assignment; `=` appears only in comparisons or mathematical identities.
- `//` begins an inline comment.
- Every routine declares `INPUT` and `OUTPUT` explicitly.
- Indexing is zero-based for arrays and heap positions, matching the Python implementation.
- `NULL` denotes the absent `next`/`top`/`front` pointer; `None` in the source.
- `A[i].key` denotes the tuple `(eta_minutes, distance_km, driver_id)` compared lexicographically.
- Source references use repository-relative paths and routine names, for example `backend/dsa/priority_queue.py :: DriverPriorityQueue.push`.
- Error paths are part of the specification, not an afterthought: `RETURN FALSE`, `RETURN NULL`, or `RAISE` is stated wherever the implementation has a boundary.

## 4.3 Singly Linked List Operations

The linked list is the authoritative registry of drivers. Each node stores identity, contact, vehicle, current coordinates, availability, and a `next` pointer. The list maintains a `_count` that is incremented on insertion and decremented on deletion. It does not maintain a tail pointer, which is why append is linear.

### 4.3.1 APPEND — `append(driver_data)`

```
INPUT : driver_data containing driver_id, driver_name, phone_number,
        vehicle_number, current_latitude, current_longitude, is_available
OUTPUT: the newly created DriverNode

1.  node ← NEW DriverNode(
        driver_id        ← driver_data.driver_id,
        driver_name      ← driver_data.driver_name,
        phone_number     ← driver_data.phone_number or "",
        vehicle_number   ← driver_data.vehicle_number or "",
        latitude         ← FLOAT(driver_data.current_latitude or 24.8607),
        longitude        ← FLOAT(driver_data.current_longitude or 67.0011),
        is_available     ← driver_data.is_available or TRUE,
        next             ← NULL)
2.  IF head = NULL THEN
3.      head ← node                         // first node in the list
4.  ELSE
5.      current ← head
6.      WHILE current.next != NULL DO       // walk to the last node
7.          current ← current.next
8.      END WHILE
9.      current.next ← node                 // link the new node at the tail
10. END IF
11. _count ← _count + 1
12. RETURN node

Complexity: Θ(n) worst case for the tail walk; Θ(1) when the list is empty.
Boundary: duplicate identifiers are not checked here; the registration route
performs the duplicate check before calling append.
```

### 4.3.2 INSERT AT INDEX — `insert(index, driver_data)`

```
INPUT : index in [0, _count], driver_data
OUTPUT: the newly created DriverNode

1.  IF index < 0 OR index > _count THEN
2.      RAISE IndexError("Index out of bounds")
3.  END IF
4.  node ← NEW DriverNode(... fields as in APPEND ...)
5.  IF index = 0 THEN
6.      node.next ← head
7.      head ← node
8.  ELSE
9.      current ← head
10.     FOR step ← 1 TO index - 1 DO
11.         IF current != NULL THEN current ← current.next
12.     END FOR
13.     IF current != NULL THEN
14.         node.next ← current.next
15.         current.next ← node
16.     END IF
17. END IF
18. _count ← _count + 1
19. RETURN node

Complexity: Θ(index) time for the walk, Θ(1) extra space.
Boundary: the index is validated against the current count before any mutation.
```

### 4.3.3 DELETE BY IDENTIFIER — `delete(driver_id)`

```
INPUT : driver_id
OUTPUT: TRUE if a node was removed, FALSE otherwise

1.  IF head = NULL THEN RETURN FALSE          // empty list
2.  IF head.driver_id = driver_id THEN
3.      head ← head.next                     // remove the first node
4.      _count ← _count - 1
5.      RETURN TRUE
6.  END IF
7.  current ← head
8.  WHILE current.next != NULL DO
9.      IF current.next.driver_id = driver_id THEN
10.         current.next ← current.next.next // bypass the target node
11.         _count ← _count - 1
12.         RETURN TRUE
13.     END IF
14.     current ← current.next
15. END WHILE
16. RETURN FALSE                              // identifier not present

Complexity: Θ(n) worst case, Θ(1) best case when the head is deleted.
```

### 4.3.4 SEARCH — `search(driver_id)`

```
INPUT : driver_id
OUTPUT: DriverNode if found, otherwise NULL

1.  current ← head
2.  WHILE current != NULL DO
3.      IF current.driver_id = driver_id THEN RETURN current
4.      current ← current.next
5.  END WHILE
6.  RETURN NULL

Complexity: Θ(n) worst case; Θ(1) best case.
```

### 4.3.5 TRAVERSE — `traverse()`

```
INPUT : none
OUTPUT: ordered list of driver dictionaries from head to tail

1.  result ← empty list
2.  current ← head
3.  WHILE current != NULL DO
4.      APPEND current.to_dict() TO result
5.      current ← current.next
6.  END WHILE
7.  RETURN result

Complexity: Θ(n) time, Θ(n) space for the result.
```

### 4.3.6 UPDATE AVAILABILITY — `update_availability(driver_id, flag)`

```
INPUT : driver_id, is_available flag
OUTPUT: TRUE if the driver exists and was updated, FALSE otherwise

1.  node ← SEARCH(driver_id)
2.  IF node = NULL THEN RETURN FALSE
3.  node.is_available ← flag
4.  RETURN TRUE

Complexity: Θ(n) because SEARCH is linear.
```

### 4.3.7 GET AVAILABLE DRIVERS — `get_available_drivers()`

```
INPUT : none
OUTPUT: list of DriverNode references whose is_available is TRUE

1.  available ← empty list
2.  current ← head
3.  WHILE current != NULL DO
4.      IF current.is_available = TRUE THEN
5.          APPEND current TO available
6.      END IF
7.      current ← current.next
8.  END WHILE
9.  RETURN available

Complexity: Θ(n) time, Θ(a) space where a is the number of available drivers.
Note: the production matchmaking path performs the filter inline inside
build_priority_queue_for_ride(); this helper is used by the simulation endpoint.
```

## 4.4 Binary Min-Heap Priority Queue Operations

The heap is stored in a Python list. The priority order is lexicographic on `(eta_minutes, distance_km, driver_id)`: the smallest ETA wins; equal ETAs are broken by the smaller distance; equal distances are broken by the smaller driver identifier. The third key guarantees deterministic output for otherwise identical candidates.

### 4.4.1 PRIORITY COMPARISON — `_is_higher_priority(a, b)`

```
INPUT : candidate dictionaries a and b
OUTPUT: TRUE if a must be extracted before b

1.  IF a.eta_minutes != b.eta_minutes THEN
2.      RETURN a.eta_minutes < b.eta_minutes
3.  END IF
4.  IF a.distance_km != b.distance_km THEN
5.      RETURN a.distance_km < b.distance_km
6.  END IF
7.  RETURN a.driver_id < b.driver_id

Complexity: Θ(1).
```

### 4.4.2 SIFT UP — `_sift_up(index)`

```
INPUT : index of a newly inserted or improved element
OUTPUT: none; the heap invariant is restored

1.  current ← index
2.  WHILE current > 0 DO
3.      parent ← (current - 1) DIV 2
4.      IF HIGHER-PRIORITY(heap[current], heap[parent]) THEN
5.          SWAP(heap[current], heap[parent])
6.          current ← parent
7.      ELSE
8.          BREAK                         // parent is already better
9.      END IF
10. END WHILE

Complexity: O(log a); Θ(1) when the element already has lower priority than
its parent (no swaps).
```

### 4.4.3 SIFT DOWN — `_sift_down(index)`

```
INPUT : index of an element that may violate the min-heap property
OUTPUT: none; the heap invariant is restored

1.  smallest ← index
2.  size ← heap.size
3.  LOOP FOREVER
4.      left ← 2 * smallest + 1
5.      right ← 2 * smallest + 2
6.      candidate ← smallest
7.      IF left < size AND HIGHER-PRIORITY(heap[left], heap[candidate]) THEN
8.          candidate ← left
9.      END IF
10.     IF right < size AND HIGHER-PRIORITY(heap[right], heap[candidate]) THEN
11.         candidate ← right
12.     END IF
13.     IF candidate = smallest THEN
14.         BREAK                          // both children are lower priority
15.     END IF
16.     SWAP(heap[smallest], heap[candidate])
17.     smallest ← candidate
18. END LOOP

Complexity: O(log a).
```

### 4.4.4 PUSH — `push(item)`

```
INPUT : candidate dictionary
OUTPUT: none

1.  APPEND item TO heap
2.  SIFT-UP(heap.size - 1)

Complexity: O(log a) time, O(1) extra space (amortized array growth is O(1)).
Boundary: pushing into an empty heap places the item at index 0 and sift-up
performs no work.
```

### 4.4.5 POP — `pop()`

```
INPUT : none
OUTPUT: the minimum-priority candidate, or NULL if the heap is empty

1.  IF heap.size = 0 THEN RETURN NULL
2.  IF heap.size = 1 THEN RETURN heap.pop()
3.  root ← heap[0]
4.  heap[0] ← heap.pop()                 // move the last element to the root
5.  SIFT-DOWN(0)
6.  RETURN root

Complexity: O(log a) time, O(1) extra space.
Boundary: the single-element case avoids an unnecessary sift-down.
```

### 4.4.6 PEEK — `peek()`

```
INPUT : none
OUTPUT: heap[0] or NULL

1.  IF heap.size = 0 THEN RETURN NULL
2.  RETURN heap[0]

Complexity: Θ(1).
```

### 4.4.7 HEAPIFY — `heapify(items)`

```
INPUT : arbitrary list of candidate dictionaries
OUTPUT: none; heap is rebuilt in place from the list

1.  heap ← deep copy of items
2.  IF heap.size <= 1 THEN RETURN
3.  start ← (heap.size - 2) DIV 2       // last internal node
4.  FOR i ← start DOWN TO 0 DO
5.      SIFT-DOWN(i)
6.  END FOR

Complexity: O(a) time by the standard heapify bound, O(a) space for the copy.
Status: implemented and unit-tested, but not used by the request path; the
service builds heaps with repeated PUSH calls.
```

### 4.4.8 UPDATE PRIORITY — `update_priority(id, eta, distance)`

```
INPUT : driver_id, new ETA, new distance
OUTPUT: TRUE if the driver was found and updated, FALSE otherwise

1.  FOR i ← 0 TO heap.size - 1 DO
2.      IF heap[i].driver_id = driver_id THEN
3.          heap[i].eta_minutes ← new_eta
4.          heap[i].distance_km ← new_distance
5.          SIFT-UP(i)                  // handles a decrease in key
6.          SIFT-DOWN(i)                // handles an increase in key
7.          RETURN TRUE
8.      END IF
9.  END FOR
10. RETURN FALSE

Complexity: O(a) for the linear search plus O(log a) for the two sifts.
Status: implemented and tested; not called by any workflow, because driver
positions are static in the demonstration and a ride's candidates are not
re-ranked mid-cascade.
```

### 4.4.9 DISPLAY — `display()`

```
INPUT : none
OUTPUT: candidates in ascending priority order; heap is unchanged

1.  backup ← deep copy of heap
2.  temp ← new empty DriverPriorityQueue
3.  temp.heap ← deep copy of heap
4.  ordered ← empty list
5.  WHILE temp is not empty DO
6.      APPEND temp.pop() TO ordered
7.  END WHILE
8.  heap ← backup                         // restore the original structure
9.  RETURN ordered

Complexity: Θ(a log a) time, Θ(a) space. The method is non-destructive and is
used by the ranking endpoint and the DSA dashboard.
```

## 4.5 LIFO Stack Operations

The stack records lifecycle events. Each node stores an event dictionary and a `next` pointer to the previous top. The stack also maintains a `_count`.

### 4.5.1 PUSH — `push(activity)`

```
INPUT : activity dictionary
OUTPUT: none

1.  IF activity has no timestamp THEN
2.      activity.timestamp ← CURRENT DATE AND TIME formatted "%Y-%m-%d %H:%M:%S"
3.  END IF
4.  node ← NEW StackNode(data ← activity, next ← top)
5.  top ← node
6.  _count ← _count + 1

Complexity: Θ(1) time, Θ(1) space.
```

### 4.5.2 POP — `pop()`

```
INPUT : none
OUTPUT: the most recent event dictionary, or NULL if the stack is empty

1.  IF top = NULL THEN RETURN NULL
2.  target ← top
3.  top ← top.next
4.  _count ← _count - 1
5.  RETURN target.data

Complexity: Θ(1).
Status: implemented and unit-tested; no route currently pops the audit trail,
because the application only appends and displays events.
```

### 4.5.3 PEEK AND DISPLAY

```
PEEK:
1.  IF top = NULL THEN RETURN NULL
2.  RETURN top.data

DISPLAY:
1.  result ← empty list
2.  current ← top
3.  WHILE current != NULL DO
4.      APPEND current.data TO result
5.      current ← current.next
6.  END WHILE
7.  RETURN result                        // most recent first

Complexity: PEEK Θ(1); DISPLAY Θ(s) time and Θ(s) space.
```

## 4.6 FIFO Queue Operations

The queue holds a request only for the duration of `request_ride()`. Its value is the demonstrated FIFO discipline and the inspection endpoint, not a persistent backlog.

### 4.6.1 ENQUEUE — `enqueue(item)`

```
INPUT : request dictionary
OUTPUT: none

1.  node ← NEW QueueNode(data ← item)
2.  IF rear = NULL THEN
3.      front ← node
4.      rear ← node
5.  ELSE
6.      rear.next ← node
7.      rear ← node
8.  END IF
9.  _count ← _count + 1

Complexity: Θ(1).
```

### 4.6.2 DEQUEUE — `dequeue()`

```
INPUT : none
OUTPUT: the oldest request, or NULL if the queue is empty

1.  IF front = NULL THEN RETURN NULL
2.  target ← front
3.  front ← front.next
4.  IF front = NULL THEN rear ← NULL    // queue became empty
5.  _count ← _count - 1
6.  RETURN target.data

Complexity: Θ(1).
Boundary: the rear reset is essential; without it, a later enqueue would link
to a removed node and corrupt the queue.
```

### 4.6.3 PEEK AND DISPLAY

```
PEEK:
1.  IF front = NULL THEN RETURN NULL
2.  RETURN front.data

DISPLAY:
1.  result ← empty list; current ← front
2.  WHILE current != NULL DO
3.      APPEND current.data TO result
4.      current ← current.next
5.  END WHILE
6.  RETURN result                        // front to rear

Complexity: PEEK Θ(1); DISPLAY Θ(size).
```

## 4.7 Chained Hash Table Operations (Implemented, Not Wired)

The hash table uses an array of buckets of fixed capacity 10. Each bucket is a singly linked chain of key–value nodes. The hash function is `abs(hash(key)) % capacity`; because Python's `hash()` of an integer is the integer itself for the practical identifier range used here, the effective bucket is `driver_id % 10`.

### 4.7.1 HASH

```
INPUT : integer key
OUTPUT: bucket index in [0, capacity - 1]

1.  RETURN ABS(HASH(key)) MOD capacity

Complexity: Θ(1). No resizing or load-factor management is implemented.
```

### 4.7.2 PUT

```
INPUT : key, value dictionary
OUTPUT: none

1.  index ← HASH(key)
2.  current ← buckets[index]
3.  WHILE current != NULL DO
4.      IF current.key = key THEN
5.          current.value ← value      // update in place
6.          RETURN
7.      END IF
8.      current ← current.next
9.  END WHILE
10. newNode ← NEW HashNode(key, value, next ← buckets[index])
11. buckets[index] ← newNode            // head insertion
12. _count ← _count + 1

Complexity: O(1 + alpha) average, where alpha = _count / capacity; O(capacity)
worst case if every key collides. Head insertion makes the insert itself O(1)
after the duplicate check.
```

### 4.7.3 GET

```
INPUT : key
OUTPUT: value dictionary or NULL

1.  index ← HASH(key)
2.  current ← buckets[index]
3.  WHILE current != NULL DO
4.      IF current.key = key THEN RETURN current.value
5.      current ← current.next
6.  END WHILE
7.  RETURN NULL

Complexity: O(1 + alpha) average; O(capacity) worst case.
```

### 4.7.4 DELETE

```
INPUT : key
OUTPUT: TRUE if removed, FALSE if absent

1.  index ← HASH(key)
2.  current ← buckets[index]
3.  previous ← NULL
4.  WHILE current != NULL DO
5.      IF current.key = key THEN
6.          IF previous = NULL THEN
7.              buckets[index] ← current.next
8.          ELSE
9.              previous.next ← current.next
10.         END IF
11.         _count ← _count - 1
12.         RETURN TRUE
13.     END IF
14.     previous ← current
15.     current ← current.next
16. END WHILE
17. RETURN FALSE

Complexity: O(1 + alpha) average; O(capacity) worst case.
Integration status: no route or service imports DriverHashTable. The live
driver lookup remains the linked-list SEARCH, O(n). The table is retained as
the tested academic alternative and as the first recommendation in Chapter 7.
```

## 4.8 Geographic, ETA, and Fare Calculations

### 4.8.1 HAVERSINE DISTANCE

The great-circle distance between two latitude–longitude pairs is computed with the Haversine formula [3]. For latitudes and longitudes in degrees:

$$\phi_1 = \frac{\pi}{180}\,lat_1,\qquad \phi_2 = \frac{\pi}{180}\,lat_2$$

$$\Delta\phi = \frac{\pi}{180}(lat_2-lat_1),\qquad \Delta\lambda = \frac{\pi}{180}(lon_2-lon_1)$$

$$a = \sin^2\!\left(\frac{\Delta\phi}{2}\right) + \cos\phi_1\cos\phi_2\sin^2\!\left(\frac{\Delta\lambda}{2}\right)$$

$$c = 2\arctan2\!\left(\sqrt{a},\sqrt{1-a}\right),\qquad d = 6371.0 \times c$$

```
INPUT : lat1, lon1, lat2, lon2 in decimal degrees
OUTPUT: distance in kilometres, rounded to two decimal places

1.  R ← 6371.0                          // mean Earth radius in km
2.  phi1 ← RADIANS(lat1)
3.  phi2 ← RADIANS(lat2)
4.  dphi ← RADIANS(lat2 - lat1)
5.  dlambda ← RADIANS(lon2 - lon1)
6.  a ← SIN(dphi / 2)^2
        + COS(phi1) * COS(phi2) * SIN(dlambda / 2)^2
7.  c ← 2 * ATAN2(SQRT(a), SQRT(1 - a))
8.  d ← R * c
9.  RETURN ROUND(d, 2)

Complexity: Θ(1) time and space.
Boundary: identical coordinates give a = 0, c = 0, and d = 0.0.
```

### 4.8.2 ETA ESTIMATION

```
INPUT : distance_km, speed_kmh (default 25.0)
OUTPUT: ETA in minutes, rounded to one decimal place, minimum 2.0

1.  IF distance_km <= 0 THEN RETURN 2.0
2.  minutes ← (distance_km / speed_kmh) * 60.0
3.  RETURN ROUND(MAX(2.0, minutes), 1)

Complexity: Θ(1).
Rationale: 25 km/h approximates dense Karachi traffic for the demonstration;
the two-minute floor prevents an implausibly small ETA for a driver at the
pickup point. The ETA is a ranking signal, not a traffic prediction.
```

### 4.8.3 FARE CALCULATION

```
INPUT : distance_km, vehicle_type (case-insensitive)
OUTPUT: dictionary with label, base fare, rate, distance charge, total, currency

1.  v ← LOWERCASE(vehicle_type)
2.  IF "bike" IN v THEN
3.      base ← 50.0;  rate ← 15.0;  label ← "Bike (Pink Wheels)"
4.  ELSE IF "premium" IN v OR "good" IN v THEN
5.      base ← 150.0; rate ← 22.0;  label ← "Good Car (Premium)"
6.  ELSE
7.      base ← 100.0; rate ← 18.0;  label ← "Car (Standard)"
8.  END IF
9.  charge ← ROUND(distance_km * rate, 2)
10. total ← ROUND(base + charge, 2)
11. RETURN {label, base, rate, distance_km, charge, total, currency = "PKR"}

Complexity: Θ(1).
Boundary: an unknown category falls through to the standard car rather than
raising an error; category matching is substring-based and case-insensitive.
```

For the canonical Saddar-to-Clifton trip used in Chapter 6, $d = 5.68$ km, so the bike fare is $50 + 5.68 \times 15 = 135.20$ PKR, the standard car fare is $100 + 5.68 \times 18 = 202.24$ PKR, and the premium fare is $150 + 5.68 \times 22 = 274.96$ PKR.

## 4.9 Composite Workflows

### 4.9.1 BUILD CANDIDATE HEAP — `build_priority_queue_for_ride`

```
INPUT : pickup_latitude, pickup_longitude, excluded_driver_ids (optional set)
OUTPUT: DriverPriorityQueue containing every eligible candidate

1.  IF excluded_driver_ids = NULL THEN excluded_driver_ids ← empty set
2.  pq ← NEW DriverPriorityQueue
3.  current ← driver_list.head
4.  WHILE current != NULL DO
5.      IF current.is_available = TRUE
            AND current.driver_id NOT IN excluded_driver_ids THEN
6.          d ← HAVERSINE(current.lat, current.lon, pickup_lat, pickup_lon)
7.          eta ← CALCULATE-ETA(d)
8.          candidate ← {
                driver_id, driver_name, phone_number, vehicle_number,
                current_latitude, current_longitude,
                distance_km ← d, eta_minutes ← eta }
9.          pq.PUSH(candidate)
10.     END IF
11.     current ← current.next
12. END WHILE
13. RETURN pq

Complexity: n scans, a Haversine evaluations, and a pushes each O(log a):
O(n + a log a) time, O(a) space.
```

### 4.9.2 REQUEST RIDE — `request_ride`

```
INPUT : passenger_id, pickup_location, destination,
        pickup_lat, pickup_lon, dest_lat, dest_lon, vehicle_type
OUTPUT: result dictionary (ride id, status, assigned driver, fare, remaining count)

1.  trip ← HAVERSINE(pickup_lat, pickup_lon, dest_lat, dest_lon)
2.  fare ← CALCULATE-FARE(trip, vehicle_type)
3.  request ← {passenger_id, pickup_location, destination,
                 pickup_lat, pickup_lon, dest_lat, dest_lon,
                 distance_km ← trip, fare ← fare.total,
                 vehicle_type, requested_at ← now}
4.  ride_queue.ENQUEUE(request)
5.  ride_id ← INSERT INTO rides
        (passenger_id, driver_id = NULL, locations, coordinates,
         distance_km, fare, vehicle_type, status = 'PENDING')
6.  ride_queue.DEQUEUE()                  // request admitted to processing
7.  activity_stack.PUSH({
        ride_id, passenger_id, event = 'RIDE_REQUESTED',
        description = "<passenger> requested <category> from <pickup> to <destination>",
        timestamp = now })
8.  pq ← BUILD-CANDIDATE-HEAP(pickup_lat, pickup_lon)
9.  active_ride_pqs[ride_id] ← pq
10. best ← pq.POP()
11. IF best != NULL THEN
12.     UPDATE rides SET driver_id = best.driver_id, status = 'OFFERED'
            WHERE id = ride_id
13.     activity_stack.PUSH({
            ride_id, driver_id = best.driver_id, event = 'DRIVER_OFFERED',
            description = "<name>, ETA, distance", timestamp = now })
14. END IF
15. RETURN {
        ride_id,
        status ← IF best = NULL THEN 'NO_DRIVERS_AVAILABLE' ELSE 'OFFERED',
        assigned_driver ← best,
        fare_info ← fare,
        trip_distance_km ← trip,
        remaining_candidates_count ← pq.SIZE() }

Complexity: Θ(1) for the queue, O(1) for each database operation, O(n + a log a)
for candidate construction, O(log a) for the extraction: O(n + a log a) overall.
Boundary: when best = NULL, the response says NO_DRIVERS_AVAILABLE but the
database row is not updated from PENDING. This divergence is documented in
Section 4.11 and Chapter 7; it is the most significant state-consistency gap
found during the analysis.
```

### 4.9.3 ACCEPT RIDE — `accept_ride`

```
INPUT : ride_id, driver_id
OUTPUT: acceptance result

1.  ride ← SELECT * FROM rides WHERE id = ride_id
2.  IF ride = NULL THEN RAISE RideNotFoundError
3.  IF ride.status IN ('COMPLETED', 'CANCELLED', 'NO_DRIVERS_AVAILABLE') THEN
4.      RAISE RideStateError("no longer available")
5.  END IF
6.  IF ride.status = 'ACCEPTED' THEN
7.      RAISE RideStateError("already accepted")
8.  END IF
9.  driver ← driver_list.SEARCH(driver_id)
10. IF driver = NULL THEN RAISE RideStateError("not registered")
11. IF ride.driver_id != NULL AND ride.driver_id != driver_id THEN
12.     RAISE RideStateError("offered to another driver")
13. END IF
14. driver_list.UPDATE-AVAILABILITY(driver_id, FALSE)
15. UPDATE rides SET status = 'ACCEPTED', driver_id = driver_id WHERE id = ride_id
16. activity_stack.PUSH({event = 'RIDE_ACCEPTED', driver_id, ride_id,
        description = "driver marked BUSY in Linked List"})
17. active_ride_pqs.REMOVE(ride_id)
18. RETURN {status = 'ACCEPTED', driver_id, driver_name, message}

Complexity: O(n) for the list search and the availability update (the update
searches again), plus O(1) database and stack work: O(n) overall.
Boundary: the guard does not require status = 'OFFERED' before acceptance; see
Section 4.11 for the PENDING-acceptance gap.
```

### 4.9.4 REJECT RIDE AND CASCADE — `reject_ride`

```
INPUT : ride_id, driver_id
OUTPUT: reassignment result or exhaustion result

1.  ride ← SELECT * FROM rides WHERE id = ride_id
2.  IF ride = NULL THEN RAISE RideNotFoundError
3.  IF ride.status != 'OFFERED' THEN RAISE RideStateError("no open offer")
4.  IF ride.driver_id != NULL AND ride.driver_id != driver_id THEN
5.      RAISE RideStateError("not offered to this driver")
6.  END IF
7.  driver ← driver_list.SEARCH(driver_id)
8.  name ← IF driver != NULL THEN driver.driver_name ELSE "Driver #<id>"
9.  activity_stack.PUSH({event = 'RIDE_REJECTED', description = "<name> rejected"})
10. IF active_ride_pqs does NOT contain ride_id THEN
11.     pq ← BUILD-CANDIDATE-HEAP(ride.pickup_lat, ride.pickup_lon,
                                   excluded_driver_ids = {driver_id})
12.     active_ride_pqs[ride_id] ← pq
13. END IF
14. pq ← active_ride_pqs[ride_id]
15. next ← IF pq is not empty THEN pq.POP() ELSE NULL
16. IF next != NULL THEN
17.     UPDATE rides SET driver_id = next.driver_id, status = 'OFFERED'
18.     activity_stack.PUSH({event = 'DRIVER_REASSIGNED',
            description = "re-offered to <name>, ETA <eta>"})
19.     RETURN {status = 'OFFERED', assigned_driver = next,
                message = "reassigned to next candidate"}
20. ELSE
21.     UPDATE rides SET status = 'NO_DRIVERS_AVAILABLE'
22.     activity_stack.PUSH({event = 'MATCHMAKING_EXHAUSTED',
            description = "no further available drivers"})
23.     RETURN {status = 'NO_DRIVERS_AVAILABLE', assigned_driver = NULL,
                message = "all eligible drivers rejected"}
24. END IF

Complexity: O(1) database reads/writes; O(log a) when the heap is alive;
O(n + a log a) only on the rebuild branch after a process restart.
Boundary: the exhausted heap remains in active_ride_pqs because the function
does not remove the entry on the exhaustion branch; see Chapter 7.
```

### 4.9.5 COMPLETE RIDE — `complete_ride`

```
INPUT : ride_id
OUTPUT: completion result

1.  ride ← SELECT * FROM rides WHERE id = ride_id
2.  IF ride = NULL THEN RAISE RideNotFoundError
3.  IF ride.status = 'COMPLETED' THEN RETURN idempotent success
4.  IF ride.status != 'ACCEPTED' THEN RAISE RideStateError("cannot complete")
5.  driver_id ← ride.driver_id
6.  IF driver_id != NULL THEN driver_list.UPDATE-AVAILABILITY(driver_id, TRUE)
7.  UPDATE rides SET status = 'COMPLETED' WHERE id = ride_id
8.  driver ← IF driver_id != NULL THEN driver_list.SEARCH(driver_id) ELSE NULL
9.  name ← IF driver != NULL THEN driver.driver_name ELSE "Assigned Driver"
10. activity_stack.PUSH({event = 'RIDE_COMPLETED',
        description = "ride completed; driver available again"})
11. active_ride_pqs.REMOVE(ride_id)
12. RETURN {status = 'COMPLETED', message}

Complexity: O(n) due to the availability update and the name lookup; O(1)
database and stack work.
Boundary: repeated completion is idempotent rather than an error, which makes
the driver console tolerant of double clicks.
```

### 4.9.6 CANCEL RIDE — `cancel_ride`

```
INPUT : ride_id
OUTPUT: cancellation result

1.  ride ← SELECT * FROM rides WHERE id = ride_id
2.  IF ride = NULL THEN RAISE RideNotFoundError
3.  IF ride.status IN ('CANCELLED', 'COMPLETED') THEN
4.      RETURN idempotent result with the existing status
5.  END IF
6.  IF ride.driver_id != NULL AND ride.status = 'ACCEPTED' THEN
7.      driver_list.UPDATE-AVAILABILITY(ride.driver_id, TRUE)
8.  END IF
9.  UPDATE rides SET status = 'CANCELLED' WHERE id = ride_id
10. activity_stack.PUSH({event = 'RIDE_CANCELLED',
        description = "ride was cancelled"})
11. active_ride_pqs.REMOVE(ride_id)
12. RETURN {status = 'CANCELLED', message}

Complexity: O(1) plus O(n) if an accepted driver must be freed.
Boundary: an offered driver is not marked busy, so cancellation from OFFERED
does not need to free anyone; the guard checks the status before updating.
```

### 4.9.7 RIDE LISTING WITH DRIVER ENRICHMENT — `GET /api/rides`

```
INPUT : optional status filter
OUTPUT: rides with driver_name, driver_phone, vehicle_number

1.  IF status provided THEN rows ← SELECT * FROM rides WHERE status = ?
        ORDER BY id DESC
    ELSE rows ← SELECT * FROM rides ORDER BY id DESC
2.  FOR EACH row IN rows DO
3.      IF row.driver_id != NULL THEN
4.          node ← driver_list.SEARCH(row.driver_id)
5.          row.driver_name ← node.driver_name IF node ELSE "Driver #<id>"
6.          row.driver_phone ← node.phone_number IF node ELSE ""
7.          row.vehicle_number ← node.vehicle_number IF node ELSE ""
8.      ELSE
9.          row.driver_name ← NULL
10.     END IF
11. END FOR
12. RETURN {rides: rows}

Complexity: O(r) database rows plus O(n) per row with a driver:
O(r * n) worst case. This is a concrete candidate for the unwired hash table.
```

## 4.10 Design-Level Comparison Algorithms

Neither Bubble Sort nor Quick Sort is called by Pink Wheels. They are specified here in full because the CEP requires a comparison of sorting strategies and because the comparison clarifies why the heap is the appropriate structure for dispatch. Both routines sort candidate records by the same three-level key used by the heap: ETA, then distance, then driver identifier.

### 4.10.1 BUBBLE SORT WITH EARLY EXIT

```
INPUT : array A of candidate records, comparator KEY
OUTPUT: A sorted in non-decreasing key order (in place)

1.  n ← A.length
2.  IF n <= 1 THEN RETURN A
3.  FOR i ← 0 TO n - 2 DO
4.      swapped ← FALSE
5.      FOR j ← 0 TO n - 2 - i DO
6.          IF KEY(A[j]) > KEY(A[j + 1]) THEN
7.              SWAP(A[j], A[j + 1])
8.              swapped ← TRUE
9.          END IF
10.     END FOR
11.     IF swapped = FALSE THEN
12.         BREAK                       // no inversions remain: array is sorted
13.     END IF
14. END FOR
15. RETURN A

Termination: the outer loop runs at most n - 1 times and the inner loop
strictly decreases, so the algorithm always terminates.
Best case: already-sorted input performs one pass, n - 1 comparisons, zero
swaps: Θ(n).
Average and worst case: Θ(n^2) comparisons and swaps.
Space: Θ(1) auxiliary. Stable: equal keys are never swapped because the
comparison is strict (>).
```

### 4.10.2 QUICK SORT WITH LOMUTO PARTITION

```
QUICKSORT(A, lo, hi):
INPUT : array A, inclusive bounds lo and hi
OUTPUT: the subarray A[lo..hi] sorted in place

1.  IF lo >= hi THEN RETURN             // base case: zero or one element
2.  p ← PARTITION(A, lo, hi)
3.  QUICKSORT(A, lo, p - 1)            // strictly smaller keys
4.  QUICKSORT(A, p + 1, hi)            // strictly larger keys
5.  RETURN

PARTITION(A, lo, hi):
INPUT : array A, inclusive bounds with at least two elements
OUTPUT: final pivot index

1.  pivot ← KEY(A[hi])                  // last element as pivot
2.  i ← lo - 1
3.  FOR j ← lo TO hi - 1 DO
4.      IF KEY(A[j]) <= pivot THEN
5.          i ← i + 1
6.          SWAP(A[i], A[j])
7.      END IF
8.  END FOR
9.  SWAP(A[i + 1], A[hi])               // place the pivot after the <= region
10. RETURN i + 1

Termination: each recursive call receives a strictly smaller range because the
pivot is excluded; the base case handles ranges of size 0 or 1.
Best and average case: Θ(n log n) comparisons.
Worst case: Θ(n^2) when the pivot is consistently the smallest or largest
element, which occurs for already-sorted input with a last-element pivot.
Space: O(log n) average recursion depth, O(n) worst case. Not stable.
```

The key insight for Pink Wheels is that neither sort is the right primitive. A request needs the *single* best driver, not a total order. A heap build plus one extraction gives that result without sorting the rest of the array; a rejection needs the *next* best driver, which a heap provides in $O(\log a)$ without touching the other candidates. Sorting all candidates once would cost $\Theta(a \log a)$ regardless of how many offers are actually made, and re-sorting after each rejection would multiply that cost by the number of rejections.

## 4.11 Edge Cases, Tie-Breakers, and Invariants

*Table 4.1 — Edge cases and tie-breakers*

| Situation | Behaviour | Source |
|---|---|---|
| Pop from empty heap | Returns `None`; no exception | `priority_queue.py :: pop` |
| Peek empty heap | Returns `None` | `priority_queue.py :: peek` |
| Pop the only element | Returns it directly; no sift-down | `priority_queue.py :: pop` |
| Heapify zero or one element | Returns immediately | `priority_queue.py :: heapify` |
| Update a missing driver priority | Returns `False` without mutation | `priority_queue.py :: update_priority` |
| Equal ETA, different distance | Smaller distance wins | `_is_higher_priority` |
| Equal ETA and distance | Smaller `driver_id` wins | `_is_higher_priority` |
| Delete head of linked list | Head advances; count decremented | `linked_list.py :: delete` |
| Delete missing identifier | Returns `False`; count unchanged | `linked_list.py :: delete` |
| Insert out of bounds | Raises `IndexError` before mutation | `linked_list.py :: insert` |
| Register duplicate explicit ID | HTTP 400 from the route check | `routes/drivers.py` |
| Register without ID | ID becomes current maximum + 1 | `routes/drivers.py` |
| Delete from empty list | Returns `False` | `linked_list.py :: delete` |
| Dequeue last queue element | `front` and `rear` both become `NULL` | `queue.py :: dequeue` |
| Pop empty stack | Returns `None` | `stack.py :: pop` |
| Identical pickup and driver coordinates | Haversine 0.0; ETA floor 2.0 | `matchmaking.py` |
| Zero or negative distance for fare | Base fare only | `calculate_fare` |
| Unknown vehicle category | Falls back to standard car | `calculate_fare` |
| Accept a completed or cancelled ride | HTTP 409 | `accept_ride` |
| Accept a ride offered to another driver | HTTP 409 | `accept_ride` |
| Accept a `PENDING` ride with no driver | **Permitted by the current guard** (gap) | `accept_ride` |
| Reject a ride that is not `OFFERED` | HTTP 409 | `reject_ride` |
| Reject as a non-offered driver | HTTP 409 | `reject_ride` |
| Complete a non-`ACCEPTED` ride | HTTP 409 | `complete_ride` |
| Complete an already completed ride | Idempotent success | `complete_ride` |
| Cancel a completed or cancelled ride | Idempotent result | `cancel_ride` |
| No eligible drivers at request time | Response `NO_DRIVERS_AVAILABLE`, row remains `PENDING` (gap) | `request_ride` |
| Hash collision | Chain traversal within the bucket | `hash_table.py` |
| Hash update of an existing key | Value replaced; count unchanged | `hash_table.py :: put` |

*Table 4.2 — Structural invariants*

| Invariant | Statement | Enforcement |
|---|---|---|
| Min-heap order | For every index $i>0$, the key at $i$ is not smaller than the key at $\lfloor (i-1)/2 \rfloor$ | `_sift_up` after push, `_sift_down` after pop/heapify |
| Heap completeness | The array has no gaps and children of $i$ are $2i+1$ and $2i+2$ | Array append/remove only |
| List count | `_count` equals the number of reachable nodes from `head` | Increment on append/insert, decrement on delete |
| List acyclicity | `next` pointers form a finite chain ending in `NULL` | Nodes are only created and linked; no node is re-linked into an earlier position |
| Stack top | `top` references the most recently pushed node | Push replaces `top`; pop advances to `top.next` |
| Queue endpoints | If the queue is non-empty, `front` is the oldest node and `rear` is the newest; if empty, both are `NULL` | Enqueue/dequeue update both endpoints, including the last-element reset |
| Active heap keyed by ride | `active_ride_pqs[ride_id]` corresponds to that ride's candidate set | Set in `request_ride`; removed on accept/complete/cancel |
| Logged transitions | Every successful lifecycle mutation pushes at least one audit event | Service functions call `activity_stack.push` after each mutation |
| Percentage/rounding | Distances and charges are rounded to 2 dp; ETAs to 1 dp | Utility functions apply `round` at the boundary |

The two gaps marked in Table 4.1—acceptance from `PENDING` and the un-updated row when no driver is available—are included deliberately. A CEP report that claimed a perfect state machine would misrepresent the code. Both have straightforward fixes (require `OFFERED` in `accept_ride`, and update the row to `NO_DRIVERS_AVAILABLE` in the no-driver branch of `request_ride`), which are listed in Chapter 7.

## 4.12 Algorithm Flowcharts

**Heap insertion (`push`) and extraction (`pop`).**

```
PUSH(item)                              POP()
  |                                       |
  v                                       v
append item to heap                  +-------------+
  |                                  | size = 0 ?  |--YES--> return NULL
  v                                  +-------------+
i <- size - 1                             | NO
  |                                       v
  v                                  +-------------+
+-------------+                      | size = 1 ?  |--YES--> return heap.pop()
| i > 0 ?     |--NO--> DONE         +-------------+
+-------------+                           | NO
  | YES                                   v
  v                                  root <- heap[0]
parent <- (i - 1) / 2                heap[0] <- heap.pop()
  |                                       |
  v                                       v
+----------------------------+       SIFT-DOWN(0)
| heap[i] < heap[parent] ?   |--NO--> DONE   |
+----------------------------+              v
  | YES                                  return root
  v
swap heap[i], heap[parent]
i <- parent
  |
  +--> loop back to i > 0
```

**Rejection cascade.**

```
START reject_ride(ride_id, driver_id)
  |
  v
fetch ride; if missing -> 404
  |
  v
+---------------------------+
| status = OFFERED ?        |--NO--> 409
+---------------------------+
  | YES
  v
+---------------------------+
| offered driver = caller ? |--NO--> 409
+---------------------------+
  | YES (or no driver set)
  v
push RIDE_REJECTED
  |
  v
+----------------------------+
| active heap exists ?       |--NO--> rebuild heap excluding rejecter
+----------------------------+        (O(n + a log a))
  | YES                              |
  +---------------+------------------+
                  v
        next <- pq.pop()
                  |
          +-------+--------+
          |                |
     next != NULL      next = NULL
          |                |
          v                v
  UPDATE OFFERED      UPDATE NO_DRIVERS_AVAILABLE
  push DRIVER_        push MATCHMAKING_
    REASSIGNED           EXHAUSTED
          |                |
          v                v
     return offer      return exhaustion
```

**Request and offer.**

```
START request_ride
  |
  v
trip <- Haversine; fare <- calculate_fare
  |
  v
enqueue request; INSERT row PENDING; dequeue request
  |
  v
push RIDE_REQUESTED
  |
  v
pq <- build candidate heap (available drivers only)
  |
  v
active_ride_pqs[ride_id] <- pq
  |
  v
best <- pq.pop()
  |
  v
+----------------+        +-------------------------------------------+
| best != NULL ? |--NO--->| return NO_DRIVERS_AVAILABLE (row stays   |
+----------------+         | PENDING; documented consistency gap)     |
  | YES                    +-------------------------------------------+
  v
UPDATE row to OFFERED with best.driver_id
  |
  v
push DRIVER_OFFERED
  |
  v
return OFFERED, driver, fare, remaining heap size
```

---

# Chapter 5 — Time and Space Complexity Analysis

## 5.1 Variables and Conventions

*Table 5.1 — Complexity notation and variables*

| Symbol | Meaning | Typical value in the demonstration |
|---|---|---|
| $n$ | Number of drivers registered in the linked list | 13 |
| $a$ | Number of eligible (available, not excluded) drivers | 11 |
| $k$ | Number of offers consumed in a rejection cascade | 1–11 |
| $s$ | Number of events in the activity stack | 9 at the captured state |
| $q$ | Number of requests in the FIFO queue | 0 or 1 (transient) |
| $r$ | Number of ride rows returned by a listing | 23 at the captured demonstration state |
| $c$ | Hash-table bucket capacity | 10 |
| $\alpha$ | Hash-table load factor, $\alpha = m/c$ | 1.3 for 13 drivers |
| $m$ | Number of keys stored in the hash table | 13 if wired |
| $R$ | Earth radius, 6371 km | constant |
| $h$ | Heap height, $\lfloor \log_2 a \rfloor$ | 3 for 11 candidates |

All bounds are stated for the comparison-based operations actually implemented. Arithmetic operations on floating-point coordinates are treated as $\Theta(1)$. Database operations are treated as $\Theta(1)$ for a primary-key lookup and insert/update on the demonstration dataset; no query planner analysis is claimed.

## 5.2 Per-Operation Time Complexity

*Table 5.2 — Per-operation time complexity*

| Structure | Operation | Best case | Average case | Worst case | Auxiliary space |
|---|---|---|---|---|---|
| Linked list | `append` | $\Theta(1)$ (empty) | $\Theta(n)$ | $\Theta(n)$ | $\Theta(1)$ |
| Linked list | `insert(index)` | $\Theta(1)$ (head) | $\Theta(i)$ | $\Theta(n)$ | $\Theta(1)$ |
| Linked list | `delete(id)` | $\Theta(1)$ (head) | $\Theta(n)$ | $\Theta(n)$ | $\Theta(1)$ |
| Linked list | `search(id)` | $\Theta(1)$ (head) | $\Theta(n)$ | $\Theta(n)$ | $\Theta(1)$ |
| Linked list | `update_availability` | $\Theta(1)$ (head) | $\Theta(n)$ | $\Theta(n)$ | $\Theta(1)$ |
| Linked list | `get_available_drivers` | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ | $\Theta(a)$ |
| Linked list | `traverse` | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ |
| Min-heap | `push` | $\Theta(1)$ (no swap) | $O(\log a)$ | $O(\log a)$ | $\Theta(1)$ |
| Min-heap | `pop` | $\Theta(1)$ (size 1) | $O(\log a)$ | $O(\log a)$ | $\Theta(1)$ |
| Min-heap | `peek` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| Min-heap | `heapify` | $O(a)$ | $O(a)$ | $O(a)$ | $\Theta(a)$ |
| Min-heap | `update_priority` | $O(\log a)$ (first element) | $O(a)$ | $O(a)$ | $\Theta(1)$ |
| Min-heap | `display` | $\Theta(a \log a)$ | $\Theta(a \log a)$ | $\Theta(a \log a)$ | $\Theta(a)$ |
| LIFO stack | `push` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| LIFO stack | `pop` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| LIFO stack | `peek` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| LIFO stack | `display` | $\Theta(s)$ | $\Theta(s)$ | $\Theta(s)$ | $\Theta(s)$ |
| FIFO queue | `enqueue` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| FIFO queue | `dequeue` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| FIFO queue | `peek` | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| Hash table | `get` | $\Theta(1)$ | $O(1+\alpha)$ | $O(c)$ | $\Theta(1)$ |
| Hash table | `put` | $\Theta(1)$ | $O(1+\alpha)$ | $O(c)$ | $\Theta(1)$ |
| Hash table | `delete` | $\Theta(1)$ | $O(1+\alpha)$ | $O(c)$ | $\Theta(1)$ |
| Calculation | Haversine | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| Calculation | ETA | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |
| Calculation | Fare | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ |

Two entries require explanation. First, `update_priority` is listed as $O(a)$ rather than $O(\log a)$ because the implementation finds the driver by scanning the heap array; the sift operations themselves are logarithmic. A position map from `driver_id` to heap index would reduce the search to expected $O(1)$ and the update to $O(\log a)$, but no such map is maintained. Second, `display` is not a pure traversal: it copies the heap and performs $a$ extractions, so it is $\Theta(a \log a)$ and uses $\Theta(a)$ auxiliary space. This is acceptable for the dashboard, which displays at most a few dozen candidates, but it would be wasteful for a hot path.

## 5.3 Composite Workflow Complexity

*Table 5.3 — Composite workflow complexity*

| Workflow | Dominant operations | Time complexity | Space complexity |
|---|---|---|---|
| Build candidate heap | Scan $n$ nodes, $a$ Haversine calculations, $a$ pushes | $O(n + a\log a)$ | $O(a)$ |
| Request ride | Build heap + one pop + constant queue/DB/log work | $O(n + a\log a)$ | $O(a)$ per active ride |
| Accept ride | One ride lookup, two linear list searches/updates | $O(n)$ | $\Theta(1)$ |
| Reject with live heap | Constant DB work + one pop | $O(\log a)$ | $\Theta(1)$ |
| Reject after restart (rebuild) | Scan $n$, compute $a$ ETAs, push $a$ candidates, pop one | $O(n + a\log a)$ | $O(a)$ |
| Exhaust a cascade of $k$ offers | $k$ pops | $O(a\log a + k\log a)$ including the initial build | $O(a)$ |
| Complete ride | Ride lookup + availability update $O(n)$ + name lookup $O(n)$ | $O(n)$ | $\Theta(1)$ |
| Cancel ride | Ride lookup + optional availability update $O(n)$ | $O(n)$ | $\Theta(1)$ |
| List rides | $r$ rows, linear driver lookup per row | $O(rn)$ | $O(r + n)$ |
| DSA ranking endpoint | Build heap + non-destructive full display | $O(n + a\log a)$ | $O(a)$ |
| Matchmaking simulation | Candidate calculations + second heap build + display | $O(n + a\log a)$ | $O(a)$ |

The request path is the one that matters under load. Its asymptotic cost is dominated by the scan of the registry, not by the heap: for $a \le n$, $O(n + a\log a)$ is $O(n\log n)$ in the worst case but is effectively $O(n)$ when $a$ is small. The rejection path is the design win: once the heap exists, each decline costs one logarithmic extraction, so a cascade of $k$ declines costs $O(a\log a + k\log a)$ for the whole request rather than $O(k(n + a\log a))$ for repeated rebuilds.

The listing workflow is the weakest asymptotic path: for each of $r$ rides with a driver, it performs a linear search of $n$ nodes, giving $O(rn)$. With 23 rides and 13 drivers this is trivial, but it is exactly the workload that the unwired hash table was designed to address. Wiring the table would reduce the driver enrichment step to expected $O(r)$.

## 5.4 Space Complexity

*Table 5.4 — Space complexity*

| Component | Space | Notes |
|---|---|---|
| Driver linked list | $\Theta(n)$ | One node and one dictionary per driver |
| Candidate heap | $\Theta(a)$ per active ride | Candidate dictionaries duplicate several driver fields |
| Active heap dictionary | $O(A)$ where $A$ is the number of active ride heaps | Entries removed on accept, complete, and cancel; **not** removed on exhaustion |
| Activity stack | $\Theta(s)$ and unbounded | Grows with every event for the process lifetime |
| FIFO queue | $\Theta(q)$, effectively 0–1 | Enqueue and dequeue occur in the same request |
| Hash table (if wired) | $\Theta(c + m)$ | Fixed 10 buckets plus chain nodes; no resizing |
| Ride and passenger tables | $\Theta(r)$ on disk | SQLite file; independent of process memory |
| Request/response payloads | $O(a)$ | Ranking payload includes every candidate |

The memory profile is modest at the demonstration scale but has two unbounded components: the activity stack and the number of retained ride heaps. Neither is a problem for a course demo; both are production concerns addressed in Chapter 7. The candidate heap also duplicates driver fields (name, phone, vehicle, coordinates) in each candidate dictionary, which is a deliberate trade-off: the heap must be independent of later mutations to the linked-list node, so copying is safer than storing node references.

## 5.5 Comparative Asymptotic Summary

*Table 5.5 — Comparative asymptotic summary*

| Design question | Chosen approach | Alternative | Chosen cost | Alternative cost | Decision |
|---|---|---|---|---|---|
| Look up a driver by ID | Linked-list search | Chained hash table | $O(n)$ | $O(1+\alpha)$ average | Chosen for simplicity; hash is implemented but unwired; wiring recommended |
| Append a driver | Singly linked list without tail | List with tail pointer | $O(n)$ | $O(1)$ | Chosen for academic linked-list demonstration; tail pointer is the obvious optimization |
| Select the best driver | Min-heap pop | Sort all candidates | $O(\log a)$ after build | $\Theta(a\log a)$ per selection | Heap wins for a single winner |
| Handle $k$ rejections | Pop from the live heap | Rebuild or re-sort per rejection | $O(a\log a + k\log a)$ | $O(k(n + a\log a))$ | Heap wins decisively as $k$ grows |
| Produce the full ranking | Non-destructive heap display | Sort the candidate array | $\Theta(a\log a)$ | $\Theta(a\log a)$ | Equivalent asymptotically; heap display reuses the invariant and avoids a separate sort |
| Most recent audit event | LIFO stack top | Database query ordered by time | $\Theta(1)$ | $O(\log r)$ with an index, plus I/O | Stack wins for the live operator view |
| Request intake ordering | FIFO queue | Immediate processing | $\Theta(1)$ | $\Theta(1)$ | Queue demonstrates FIFO discipline; no backlog is retained |
| Nearest-driver search | Haversine scan of all drivers | Spatial index (k-d tree, geohash) | $O(n)$ per build | $O(\log n)$ average (k-d tree) | Scan is adequate at 13–100 drivers; spatial index is future work |
| Road-network ETA | Haversine + constant speed | Graph shortest path (Dijkstra/A*) on OSM | $\Theta(1)$ per candidate | $O((V+E)\log V)$ per query | Straight-line ranking is adequate for a demo; OSRM is used only for the displayed polyline |

## 5.6 Bubble Sort Versus Quick Sort

*Table 5.6 — Bubble Sort versus Quick Sort*

| Property | Bubble Sort with early exit | Quick Sort (Lomuto, last pivot) |
|---|---|---|
| Best-case time | $\Theta(n)$ — one pass, no swaps | $\Theta(n\log n)$ — balanced partitions |
| Average-case time | $\Theta(n^2)$ | $\Theta(n\log n)$ |
| Worst-case time | $\Theta(n^2)$ | $\Theta(n^2)$ — already-sorted input with last-element pivot |
| Auxiliary space | $\Theta(1)$ | $O(\log n)$ average recursion, $O(n)$ worst |
| Stable | Yes | No |
| Adaptive | Yes — stops when a pass makes no swaps | No, not in this implementation |
| Behaviour on sorted input | One pass, $n-1$ comparisons, 0 swaps | Degenerate partitions, $\Theta(n^2)$ |
| Behaviour on reversed input | Maximum swaps, $\Theta(n^2)$ | Often balanced, $\Theta(n\log n)$ |
| Suitability for dispatch | Poor for large $a$; useful only as a teaching baseline | Good general-purpose sort, but unnecessary for selecting one winner |

On the 11 ETA values used in the Chapter 6 dataset (insertion order 13.6, 2.0, 25.9, 13.0, 12.3, 15.6, 19.9, 26.4, 18.5, 27.3, 9.3), Bubble Sort with early exit required 10 passes, 55 comparisons, and 20 swaps. Quick Sort with a last-element pivot required 27 comparisons and 13 swaps. On already-sorted input, Bubble Sort required one pass and 10 comparisons, while the same Quick Sort implementation required 55 comparisons and degenerated to its worst-case recursion pattern. This is the classic inversion: the "slow" algorithm is better on nearly sorted data, while the "fast" algorithm is better on random data.

Neither algorithm is used by Pink Wheels. The system's requirement is not a total order; it is repeated minimum extraction with deterministic tie-breaking. A heap provides that in $O(\log a)$ per extraction while preserving the remaining candidates for the next offer. Sorting the candidates would produce the same first element at a higher cost and would still need to be repeated or maintained if the candidate set changed.

## 5.7 Why the Chosen Structures Fit the Workload

**Linked list for the registry.** Driver registration is append-heavy, deletions are rare, and the registry must preserve a visible insertion order for the dashboard. A linked list makes the pointer structure explicit and gives $O(1)$ insertion at the head. The missing tail pointer is a performance weakness ($O(n)$ append), but it is also an honest teaching point: the microbenchmark shows the quadratic cost of repeated appends, and the report recommends a tail pointer as a one-line improvement.

**Min-heap for dispatch.** The dispatch question is "who is first?" followed by "who is next?" A heap answers both in logarithmic time and supports the rejection cascade without recomputation. The three-level comparator makes the answer deterministic and reproducible, which matters for a demonstration and for auditing.

**LIFO stack for audit.** An operator watching a ride needs the latest event first. A stack gives that in constant time and preserves chronological order underneath. It also models the "undo-like" nature of an active lifecycle: the top of the stack is the current state of play.

**FIFO queue for intake.** The queue demonstrates fairness of arrival order. In the current implementation the request is dequeued immediately, so the queue is a transient pipeline rather than a backlog. This is a scope decision: implementing a background worker that drains a queue would introduce concurrency, persistence, and failure-handling requirements that are outside the course's algorithmic focus.

**Hash table as the prepared alternative.** The table is the right answer to the $O(n)$ lookup weakness, but wiring it would change the registry's primary representation and require synchronization with the linked list. Keeping it implemented and testing it demonstrates the trade-off without destabilizing the working pipeline.

**Heapify versus repeated push.** The build path uses $a$ pushes, each $O(\log a)$, for $O(a\log a)$. The `heapify` method achieves $O(a)$ by sifting down from the last internal node. Switching the build to `heapify` would improve the asymptotic build term and is the second concrete optimization recommended in Chapter 7. The current choice is defensible for $a=11$ (the measured build path is a few milliseconds), but the report does not hide the better option.

## 5.8 Empirical Microbenchmarks

The following measurements were taken on the test host (AMD Ryzen 7 7445HS, 15.2 GB RAM, Python 3.14.7) using `time.perf_counter()` around the actual custom implementations. They are indicative, not a formal benchmark: Python object overhead and the interpreter's allocator affect constants, and the dataset is synthetic.

*Table 5.7 — Empirical microbenchmarks*

| Experiment | Size | Measured time | Interpretation |
|---|---|---|---|
| Heap push all candidates | $a = 1{,}000$ | 1.4 ms | $O(a\log a)$ with small constants |
| Heap push all candidates | $a = 10{,}000$ | 10.3 ms | Roughly 7.4× for 10× elements |
| Heap pop all candidates | $a = 1{,}000$ | 5.9 ms | Extraction includes sift-down |
| Heap pop all candidates | $a = 10{,}000$ | 108.0 ms | About 18× for 10× elements, consistent with $n\log n$ plus cache effects |
| Linked-list append all | $n = 1{,}000$ | 17.0 ms | Tail walk dominates |
| Linked-list append all | $n = 2{,}000$ | 65.1 ms | 3.8× for 2× elements — quadratic growth |
| Linked-list append all | $n = 5{,}000$ | 362.2 ms | 5.6× for 2.5× elements — clearly $O(n^2)$ |
| Linked-list search for last node | $n = 5{,}000$ | 0.303 ms | Linear but with a small constant |
| Matching simulation endpoint | $a = 11$ | 3.77–4.44 ms over five runs | Includes JSON serialization and full ranking display |

The append experiment is the clearest evidence that the missing tail pointer matters: doubling the list size roughly quadruples the total append time. It also shows why the demonstration is still responsive at 13 drivers—the quadratic term is invisible at that scale—and why the report distinguishes "adequate for the demo" from "adequate for production."

---

# Chapter 6 — Algorithm Demonstration and Walkthrough

## 6.1 Environment and Dataset

The walkthrough uses the live application running locally: FastAPI on `127.0.0.1:8000`, Vite on `localhost:5173`, and SQLite as the active backend. The driver registry is seeded from `backend/dsa/sample_drivers.py` with 13 verified women drivers. Eleven are available; Samina Sheikh (#104) is busy by seed, and Zubeda Bibi (#110) is offline by seed. The captured demonstration database contained 23 ride records, including the completed Ride #22 (Hina Tariq) and Ride #23 (Kinza Shah). The automated test suite adds temporary lifecycle rows when it runs, so the 23-row state is the state at capture time.

*Table 6.1 — Seeded driver dataset with distance and ETA to Saddar Empress Market (24.8615, 67.0099)*

| ID | Driver | Seed area | Latitude | Longitude | Status | Distance (km) | ETA (min) |
|---|---|---|---|---|---|---|---|
| 101 | Sobia Parveen | Clifton Block 2 | 24.8138 | 67.0300 | Available | 5.68 | 13.6 |
| 102 | Hina Tariq | Saddar Empress Market | 24.8615 | 67.0099 | Available | 0.00 | 2.0 |
| 103 | Mariam Siddiqui | Gulshan-e-Iqbal Block 6 | 24.9180 | 67.0971 | Available | 10.81 | 25.9 |
| 104 | Samina Sheikh | DHA Phase 5 | 24.8256 | 67.0652 | Busy (seed) | 6.86 | 16.5 |
| 105 | Nida Rehman | PECHS Block 2 | 24.8732 | 67.0621 | Available | 5.42 | 13.0 |
| 106 | Areeba Jamil | Tariq Road | 24.8719 | 67.0594 | Available | 5.13 | 12.3 |
| 107 | Khadija Farooq | Bahadurabad Chowrangi | 24.8821 | 67.0700 | Available | 6.48 | 15.6 |
| 108 | Faiza Anwar | North Nazimabad Block H | 24.9298 | 67.0425 | Available | 8.28 | 19.9 |
| 109 | Bushra Rasheed | Federal B Area | 24.9385 | 67.0782 | Available | 10.99 | 26.4 |
| 110 | Zubeda Bibi | I.I. Chundrigar Road | 24.8530 | 67.0162 | Offline (seed) | 1.14 | 2.7 |
| 111 | Rabia Mumtaz | Defence Phase 2 Ext | 24.8390 | 67.0820 | Available | 7.69 | 18.5 |
| 112 | Sidra Batool | Gulistan-e-Johar Block 12 | 24.8964 | 67.1158 | Available | 11.37 | 27.3 |
| 113 | Kinza Shah | Cantt Station | 24.8472 | 67.0450 | Available | 3.88 | 9.3 |

The table illustrates an important property of the algorithm: Zubeda Bibi is only 1.14 km from the pickup, yet she is not a candidate because her availability flag is false. Availability is a hard filter applied before ranking; it is not a soft penalty. This is the correct behaviour for a dispatch system—offering a ride to an offline driver would create a worse experience than choosing a slightly farther available driver.

## 6.2 Linked List State

![Linked list visualization](images/fig01-dsa-linked-list-overview.png)

*Figure 6.1 — Linked-list visualization. The dashboard reports 13 total nodes and renders the pointer chain from HEAD; each card shows the node identifier, name, vehicle, availability chip, and the `next` pointer.*

The list is ordered by registration: 101 → 102 → 103 → 104 → 105 → 106 → 107 → 108 → 109 → 110 → 111 → 112 → 113 → NULL. The displayed cards confirm that node 104 is marked Busy and the remaining visible nodes are Available. The `next` values are explicit: node 101 points to 102, node 102 points to 103, and so on. This is the structure that matchmaking traverses; the screenshot is not a mock-up of a list, it is a rendering of `DriverLinkedList.traverse()`.

![Linked list management](images/fig06-linked-list-management.png)

*Figure 6.2 — Registration, search, and node management. Registering appends a node; the table supports toggling availability and deleting a node; the search box resolves an identifier through `DriverLinkedList.search()`.*

The management panel exercises the linked-list operations described in Section 4.3. The registration form builds a `driver_data` dictionary from the name, phone, vehicle, latitude, and longitude fields; the route appends it and returns the new node. When no identifier is supplied, the route scans the list for the current maximum and assigns `maximum + 1`; with the seeded list at 113, the next automatic identifier is 114. Supplying an existing identifier is rejected with HTTP 400 before any mutation, which is why the append operation does not need its own duplicate check.

## 6.3 Heap Construction Trace

![Priority queue dashboard](images/fig07-priority-queue.png)

*Figure 6.3 — Priority-queue tab for the Saddar reference point. The heap contains 11 eligible drivers; the root card marks Hina Tariq as first priority at 2.0 minutes.*

The build scans the linked list in registration order and pushes each eligible driver. The order of insertion is therefore 101, 102, 103, 105, 106, 107, 108, 109, 111, 112, 113, skipping the busy and offline drivers. Table 6.2 records the internal array after each push, using the compact notation `id:eta`.

*Table 6.2 — Heap array after each insertion*

| Push | Inserted | Heap array after sift-up |
|---|---|---|
| 1 | 101 (13.6) | `[101:13.6]` |
| 2 | 102 (2.0) | `[102:2.0, 101:13.6]` |
| 3 | 103 (25.9) | `[102:2.0, 101:13.6, 103:25.9]` |
| 4 | 105 (13.0) | `[102:2.0, 105:13.0, 103:25.9, 101:13.6]` |
| 5 | 106 (12.3) | `[102:2.0, 106:12.3, 103:25.9, 101:13.6, 105:13.0]` |
| 6 | 107 (15.6) | `[102:2.0, 106:12.3, 107:15.6, 101:13.6, 105:13.0, 103:25.9]` |
| 7 | 108 (19.9) | `[102:2.0, 106:12.3, 107:15.6, 101:13.6, 105:13.0, 103:25.9, 108:19.9]` |
| 8 | 109 (26.4) | `[102:2.0, 106:12.3, 107:15.6, 101:13.6, 105:13.0, 103:25.9, 108:19.9, 109:26.4]` |
| 9 | 111 (18.5) | `[102:2.0, 106:12.3, 107:15.6, 101:13.6, 105:13.0, 103:25.9, 108:19.9, 109:26.4, 111:18.5]` |
| 10 | 112 (27.3) | `[102:2.0, 106:12.3, 107:15.6, 101:13.6, 105:13.0, 103:25.9, 108:19.9, 109:26.4, 111:18.5, 112:27.3]` |
| 11 | 113 (9.3) | `[102:2.0, 113:9.3, 107:15.6, 101:13.6, 106:12.3, 103:25.9, 108:19.9, 109:26.4, 111:18.5, 112:27.3, 105:13.0]` |

Three insertions deserve a closer look.

**Push 4 (#105, ETA 13.0).** The new element is appended at index 3. Its parent is index 1 (#101, ETA 13.6). Since 13.0 < 13.6, the two swap; #105 moves to index 1 and #101 moves to index 3. The new parent is index 0 (#102, ETA 2.0), which is better, so sift-up stops. The array after the insertion reflects this single swap.

**Push 11 (#113, ETA 9.3).** The element is appended at index 10. Its parent is index 4 (#105, ETA 13.0), so they swap. At index 4, the parent is index 1 (#106, ETA 12.3), so they swap again. At index 1, the parent is index 0 (#102, ETA 2.0), which is better, so sift-up stops. #113 ends at index 1, #106 moves to index 4, and #105 drops to index 10. This is the most expensive insertion in the trace—three comparisons and two swaps—and it is still bounded by the heap height of 3.

**The final array is a valid heap but not a sorted array.** Index 0 is the minimum, but index 1 (9.3) is smaller than index 2 (15.6), and index 4 (12.3) is smaller than index 3 (13.6). This is expected: the heap invariant relates each node only to its parent, not to its siblings. Sorted order is produced by extraction, not by reading the array.

## 6.4 Extraction and Ranking

![Heap ranking](images/fig08-heap-ranking.png)

*Figure 6.4 — The dashboard's ranked view of all 11 candidates. Rank #1 is the heap root; the remaining cards follow extraction order, not array order.*

*Table 6.3 — Priority-queue extraction order*

| Pop | Driver | ID | ETA (min) | Distance (km) | Remaining after pop |
|---|---|---|---|---|---|
| 1 | Hina Tariq | 102 | 2.0 | 0.00 | 10 |
| 2 | Kinza Shah | 113 | 9.3 | 3.88 | 9 |
| 3 | Areeba Jamil | 106 | 12.3 | 5.13 | 8 |
| 4 | Nida Rehman | 105 | 13.0 | 5.42 | 7 |
| 5 | Sobia Parveen | 101 | 13.6 | 5.68 | 6 |
| 6 | Khadija Farooq | 107 | 15.6 | 6.48 | 5 |
| 7 | Rabia Mumtaz | 111 | 18.5 | 7.69 | 4 |
| 8 | Faiza Anwar | 108 | 19.9 | 8.28 | 3 |
| 9 | Mariam Siddiqui | 103 | 25.9 | 10.81 | 2 |
| 10 | Bushra Rasheed | 109 | 26.4 | 10.99 | 1 |
| 11 | Sidra Batool | 112 | 27.3 | 11.37 | 0 |

The first extraction is the most instructive. The root (#102) is saved, the last element (#105) is moved to index 0, and sift-down proceeds: compare the children #113 (9.3) and #107 (15.6), choose #113, and swap; at index 1 compare the children #101 (13.6) and #106 (12.3), choose #106, and swap; at index 4 the only child is #112 (27.3), which is worse than #105 (13.0), so the sift stops. The new root is #113. The second extraction repeats the process and places #106 at the root. The resulting order matches the dashboard exactly, which is the strongest available evidence that the visualization is bound to the heap rather than to a separately sorted list.

Note that Nida (#105, 13.0) ranks ahead of Sobia (#101, 13.6) despite being inserted later, and that the ranking is not the insertion order. The comparator is doing its job: it orders by ETA first, and only then by distance and identifier.

## 6.5 Matchmaking Flow

![Matchmaking simulation](images/fig10-matchmaking-flow.png)

*Figure 6.5 — The five-step matchmaking replay. Step 1 scans 13 nodes, step 2 filters to 11 available drivers, step 3 computes Haversine distance and ETA, step 4 builds the min-heap, and step 5 selects the root.*

The simulation endpoint performs the same conceptual pipeline as `request_ride()` but does not write a ride row. It is useful for demonstration because it makes each stage explicit:

1. **Traverse.** 13 registered nodes are scanned.
2. **Filter.** 11 nodes have `is_available = true`.
3. **Calculate.** 11 Haversine distances and 11 ETAs are computed.
4. **Build.** 11 candidates are pushed into the heap; the root has the lowest ETA.
5. **Select.** Hina Tariq (#102) wins with ETA 2.0 minutes and distance 0.0 km.

The endpoint measured 3.77–4.44 ms per call over five runs on the test host, including JSON serialization and the non-destructive ranking display. That is the candidate-ranking cost for the full dataset; the database writes in `request_ride()` add a small constant amount of work.

## 6.6 Ride #23 Lifecycle Trace

Ride #23 is the most complete lifecycle captured in the demonstration database. The passenger is Fatima Noor (#1); the pickup is Saddar Empress Market (24.8615, 67.0099); the destination is Clifton Beach / Seaview (24.8138, 67.0300); the category is Bike. The Haversine trip distance is 5.68 km and the fare is 135.20 PKR.

The timing is important. Ride #22 was accepted by Hina Tariq (#102) and was still in progress when Ride #23 was requested. Hina was therefore marked busy and excluded from the candidate set for #23. Ride #22 completed 14 seconds after #23 was requested, which made Hina available again—but the heap for #23 had already been built and was not retroactively changed. Kinza Shah (#113), the best available candidate at request time, received the offer.

*Table 6.4 — Ride #23 event timeline (reconstructed from the stored ride row and activity stack)*

| Time | Event | Database / DSA effect | Stack event |
|---|---|---|---|
| 18:01:32 | Passenger requests Bike from Saddar to Clifton | Row inserted as `PENDING`; request enqueued/dequeued; heap built from 10 eligible drivers (Hina busy, Samina and Zubeda unavailable) | `RIDE_REQUESTED` |
| 18:01:32 | Kinza Shah is the heap root at 9.3 min / 3.88 km | Row updated to `OFFERED`, `driver_id = 113`; root popped | `DRIVER_OFFERED` |
| 18:01:46 | Ride #22 completes; Hina becomes available | Linked-list node 102 `is_available = true`; #22 row `COMPLETED`; #23 heap is unchanged | `RIDE_COMPLETED` (#22) |
| 18:02:09 | Kinza accepts #23 | Node 113 marked busy; #23 row `ACCEPTED`; heap removed from `active_ride_pqs` | `RIDE_ACCEPTED` |
| 18:02:18 | Kinza completes #23 | Node 113 marked available; #23 row `COMPLETED`; heap removal is idempotent | `RIDE_COMPLETED` |

The trace explains a subtle but important property of the design: a candidate heap is a **snapshot** taken at request time. Availability changes after the snapshot do not re-rank an existing offer. This is desirable for stability—the offered driver is not silently replaced by a driver who happens to become free a second later—but it also means that a newly freed driver is not considered until the next request. A production system could choose to refresh the heap on availability changes; the demonstration deliberately keeps the snapshot so that the cascade order is deterministic and explainable.

![Fare breakdown](images/fig03-passenger-fare-detail.png)

*Figure 6.6 — Fare breakdown for the Saddar-to-Clifton trip: 5.68 km, 50 PKR base, 85.2 PKR distance charge at 15 PKR/km, 135.2 PKR total. The card is computed by the same `haversine_distance` and `calculate_fare` functions used by the backend.*

## 6.7 Activity Stack After the Lifecycle

![Activity stack](images/fig09-activity-stack.png)

*Figure 6.7 — LIFO activity stack. The top event is the most recent action; the stack depth is 9, and the five visible entries trace Ride #23 and the completion of Ride #22.*

*Table 6.5 — Activity stack contents (top to bottom, visible entries)*

| Position | Event | Description | Timestamp |
|---|---|---|---|
| TOP | `RIDE_COMPLETED` | Ride #23 completed; Kinza Shah available again | 2026-11-19 18:02:18 |
| #2 | `RIDE_ACCEPTED` | Kinza Shah accepted Ride #23; marked BUSY in linked list | 2026-11-19 18:02:09 |
| #3 | `RIDE_COMPLETED` | Ride #22 completed; Hina Tariq available again | 2026-11-19 18:01:46 |
| #4 | `DRIVER_OFFERED` | Ride #23 offered to Kinza Shah (ETA 9.3 min, 3.88 km) | 2026-11-19 18:01:32 |
| #5 | `RIDE_REQUESTED` | Fatima Noor requested Bike from Saddar to Clifton (fare 135.2) | 2026-11-19 18:01:32 |

The five visible entries are exactly the sequence in Table 6.4 in reverse chronological order. The stack depth of 9 means that four earlier events—from preceding rides and the `SYSTEM_STARTUP` event—sit below the visible window. The ordering demonstrates the LIFO invariant: `push` always places the new event at the top, and `display` traverses from `top` through `next` pointers.

Why a stack rather than a list or a database table? For a live operator, the most recent event is the most relevant. A stack provides $O(1)$ insertion and $O(1)$ access to the latest event, and its top-down traversal naturally produces "latest first." The trade-off is that history is unbounded and in-memory; Chapter 7 recommends a persistent audit table alongside a bounded in-process stack.

## 6.8 Rejection Cascade Trace

To demonstrate the cascade cleanly, assume Ride #23 has completed and Hina Tariq is available again, so the heap contains all 11 eligible drivers. A new request at Saddar rebuilds the heap with Hina at the root. The driver rejects; the service pops the next candidate from the same heap and re-offers. The sequence is:

*Table 6.6 — Rejection cascade for a fresh 11-driver heap*

| Offer round | Offered driver | ETA (min) | Action | Resulting ride status |
|---|---|---|---|---|
| 1 | Hina Tariq (#102) | 2.0 | Reject | `OFFERED` → Kinza Shah |
| 2 | Kinza Shah (#113) | 9.3 | Reject | `OFFERED` → Areeba Jamil |
| 3 | Areeba Jamil (#106) | 12.3 | Reject | `OFFERED` → Nida Rehman |
| 4 | Nida Rehman (#105) | 13.0 | Reject | `OFFERED` → Sobia Parveen |
| 5 | Sobia Parveen (#101) | 13.6 | Reject | `OFFERED` → Khadija Farooq |
| 6 | Khadija Farooq (#107) | 15.6 | Reject | `OFFERED` → Rabia Mumtaz |
| 7 | Rabia Mumtaz (#111) | 18.5 | Reject | `OFFERED` → Faiza Anwar |
| 8 | Faiza Anwar (#108) | 19.9 | Reject | `OFFERED` → Mariam Siddiqui |
| 9 | Mariam Siddiqui (#103) | 25.9 | Reject | `OFFERED` → Bushra Rasheed |
| 10 | Bushra Rasheed (#109) | 26.4 | Reject | `OFFERED` → Sidra Batool |
| 11 | Sidra Batool (#112) | 27.3 | Reject | `NO_DRIVERS_AVAILABLE` |

Each rejection pushes two events: `RIDE_REJECTED` for the decline and either `DRIVER_REASSIGNED` for the next offer or `MATCHMAKING_EXHAUSTED` for the final decline. The database row's `driver_id` changes with each reassignment; the status remains `OFFERED` until exhaustion. The heap shrinks by one on each pop, so the eleventh decline finds it empty.

The complexity of the whole cascade is $O(a\log a + k\log a)$ with $a=11$ and $k=11$: one build plus eleven logarithmic extractions. A rebuild-per-rejection design would instead perform eleven scans of the linked list and eleven heap builds—roughly an order of magnitude more work even at this small scale, and a much larger gap at city scale.

Two operational details are worth recording. First, when a rejection arrives after a process restart, the heap may no longer be in `active_ride_pqs`; the service rebuilds it from the ride's stored pickup coordinates and excludes the rejecting driver. That rebuild is $O(n + a\log a)$ and may include drivers whose availability changed since the original offer. Second, when the heap is exhausted, the code does not remove the empty heap from `active_ride_pqs`; this is a small retained-memory leak that is harmless in a demo but should be fixed with a single `pop` on the exhaustion path.

## 6.9 Sorting Comparison Run

The same 11 ETA values, in linked-list insertion order, were run through the design-level algorithms:

*Table 6.7 — Sorting comparison run on 11 ETA values*

| Algorithm | Input order | Passes / recursion | Comparisons | Swaps | Output order |
|---|---|---|---|---|---|
| Bubble Sort with early exit | 13.6, 2.0, 25.9, 13.0, 12.3, 15.6, 19.9, 26.4, 18.5, 27.3, 9.3 | 10 passes | 55 | 20 | 2.0, 9.3, 12.3, 13.0, 13.6, 15.6, 18.5, 19.9, 25.9, 26.4, 27.3 |
| Quick Sort (Lomuto, last pivot) | same | Balanced/recursive | 27 | 13 | same |
| Bubble Sort on already-sorted input | ascending | 1 pass | 10 | 0 | unchanged |
| Quick Sort on already-sorted input | ascending | Degenerate partitions | 55 | — | unchanged |

The comparison confirms the textbook trade-off: Quick Sort is about twice as efficient on this random-ish input, but Bubble Sort's early exit makes it optimal on sorted input, while the last-element pivot drives Quick Sort to its worst case. Neither result changes the design decision, because the heap avoids sorting altogether for dispatch. The `display()` method produces the same sorted output in $\Theta(a\log a)$ by extracting from the heap, reusing the invariant that was already built for selection.

## 6.10 Edge-Case Verification

The following behaviours were verified against the running API or the automated test suite. They are recorded here because a complexity analysis is only credible if the boundary conditions are actually enforced.

*Table 6.8 — Edge-case verification results*

| Case | Expected | Observed |
|---|---|---|
| Register an existing explicit driver ID | HTTP 400, no mutation | 400 |
| Accept an already completed ride | HTTP 409 | 409 |
| Reject a ride that is not offered | HTTP 409 | 409 |
| Complete an already completed ride | Idempotent success | `status: COMPLETED`, "already completed" |
| Estimate fare with identical pickup and destination | 0 km, base fare only | 0.0 km, 50.0 PKR (Bike) |
| Estimate fare with an unknown category | Standard car fallback | `Car (Standard)`, 202.24 PKR for 5.68 km |
| Pop empty heap / peek empty heap | `None` | Passed unit tests |
| Single-element pop | Returns the element, no sift | Passed unit test |
| Equal ETA, smaller distance wins | Distance tie-breaker | Passed unit test |
| Equal ETA and distance, smaller ID wins | ID tie-breaker | Passed unit test |
| Heapify arbitrary list | Non-decreasing pops | Passed unit test |
| Update existing priority | Reorders the heap | Passed unit test |
| Update missing priority | Returns `False` | Passed unit test |
| Display is sorted and non-destructive | Order preserved, size unchanged | Passed unit test |
| Delete linked-list head / middle / missing | Correct count and `False` on miss | Passed unit tests |
| Dequeue last queue element | Front and rear reset | Passed unit tests |
| Stack pop on empty | `None` | Passed unit test |
| Haversine identical points | 0.0 km | Verified through fare endpoint |

The backend suite currently reports **48 passing test cases across 7 test modules** in 0.63 seconds (one third-party deprecation warning only). The suite covers the priority queue, linked list, history stack, matching and fare calculations, ride routes, the DSA workflow, and the full-system integration path.

## 6.11 End-to-End System Verification and UI Performance

**Ride lifecycle.** The end-to-end path was exercised in the browser: a passenger requested a Bike from Saddar to Clifton, the offer appeared in the selected driver's console, the driver accepted, and the ride was completed. The persisted row moved through `OFFERED` → `ACCEPTED` → `COMPLETED`, the driver's availability returned to true, and the stack recorded each transition. The screenshots in this chapter are from that running system, not from static mock data.

**Responsive layout.** At a 390 px mobile viewport, the passenger and DSA pages reported zero horizontal overflow. The DSA dashboard's four tabs, the 23-location selects, the map, and the ranking cards remained operable.

**Map.** The map loaded the Esri light-gray base and reference layers (24 tile requests observed for the initial view), rendered custom pink markers for pickup, destination, and drivers, and drew the OSRM route with a straight-line fallback. No console errors were observed on any page.

**Frame-time measurements.** The measurements use an uncapped headless Chrome so that the available headroom can be measured directly. The 120 Hz budget is 8.33 ms per frame; the 60 Hz budget is 16.67 ms. Each row summarizes thousands of animation-frame deltas during scrolling and interaction.

*Table 6.9 — Frame-time measurements (milliseconds)*

| Page / condition | p50 | p95 | p99 | Max | Frames over 8.33 ms |
|---|---|---|---|---|---|
| Passenger, desktop, unthrottled | 0.9 | 1.6 | 2.1 | 3.1 | 0 |
| Passenger history, desktop | 0.6 | 0.8 | 1.0 | 2.0 | 0 |
| Driver console, desktop | 0.4 | 0.6 | 0.8 | 3.0 | 0 |
| DSA dashboard, desktop | 0.5 | 0.8 | 1.0 | 1.8 | 0 |
| Passenger, desktop, 4× CPU throttle | 3.0 | 4.6 | 5.1 | 5.5 | 0 |
| DSA, desktop, 4× CPU throttle (first run) | 2.6 | 4.5 | 6.6 | 68.3 | 5 of ~1,800 |
| Passenger, mobile emulation | 0.7 | 1.3 | 1.7 | 5.8 | 0 |
| DSA, mobile emulation | 0.6 | 1.0 | 1.3 | 2.6 | 0 |

A 4×-throttled DSA run produced five over-budget frames out of roughly 1,800, dominated by a single 68.3 ms outlier consistent with a garbage-collection pause; the confirmation run produced none. The report presents both facts rather than claiming perfectly uniform frame times. Steady-state p99 is comfortably inside the 120 Hz budget, and the mobile runs show no over-budget frames.

The interaction profile is also compositor-friendly: tab switches incur a one-time paint of 17–36 ms while the new tab mounts, hover repaints cost about 1.8 ms, and scroll segments perform zero or one layout. These are one-time mount costs, not per-frame costs. No cosmetic FPS counter was added, and the browser still presents at the display's refresh rate; the measurements quantify headroom, not a manufactured number.

---

# Chapter 7 — Conclusion, Future Scope, and Source Code Listings

## 7.1 Key Engineering Takeaways

**The separation of registry and ranking is the central design idea.** The linked list answers "who is registered and available?" and the heap answers "who is best for this pickup?" Mixing the two would force either a linear scan on every offer or a sorted registry that is expensive to update. Keeping them separate means availability mutations touch only the list, while ranking is rebuilt as a cheap snapshot per request. The design is not the only possible one, but it is easy to explain, test, and visualize—properties that matter in an academic system and in an operational audit.

**The rejection cascade is where the data structure earns its place.** Selecting the best driver once could be done with a sort. The cascade is different: each decline needs the next-best candidate without recomputation. The live heap turns a decline into one $O(\log a)$ extraction, and the walkthrough in Section 6.8 shows eleven declines consuming a prebuilt heap in order. This is a concrete, measurable example of a structure fitting a workload rather than being chosen for its name.

**Determinism is a feature, not a detail.** Equal ETAs are common when drivers are clustered or when distances round to the same value. The comparator's second key (distance) and third key (driver identifier) guarantee that the same inputs always produce the same offer order. Without the third key, two identical candidates could be ordered arbitrarily, making demonstrations and audits irreproducible.

**Complexity analysis exposed both strengths and weaknesses.** The request path is $O(n + a\log a)$, the cascade is $O(\log a)$ per decline, and the stack is $O(1)$ per event. But the analysis also exposed an $O(n^2)$ registration pattern caused by the missing tail pointer, an $O(rn)$ ride-listing path caused by linear driver lookup, and an unused $O(a)$ heapify that could improve the build. A report that only listed the good bounds would be incomplete; the weaknesses are part of the engineering result.

**Tests and traces are the evidence base.** The 48 passing tests cover the heap invariants, tie-breakers, linked-list deletions, queue endpoint reset, fare and matching utilities, route behaviour, and the full-system path. The walkthrough adds evidence the tests cannot: the live ranking, the ride #23 timeline, and the activity stack. Together they support the claim that the described algorithms are the ones the application runs.

**The UI performance work is architectural.** The measured p99 frame times (0.8–2.1 ms unthrottled, 5.1–6.6 ms at 4× CPU throttle) are the result of compositor-only motion, one-shot reveal observers, diffed polling, paint containment, and a map isolated in its own component. None of these is a cosmetic trick, and none requires a fake FPS counter. The system meets the 120 Hz budget in steady state while remaining honest about one-off mount costs and an isolated garbage-collection outlier.

**Teamwork produced a maintainable boundary.** The DSA layer has no knowledge of HTTP, the routes have no knowledge of heap internals, and the frontend consumes a single API module. That separation is what allowed the project to change the visual theme, add 23 locations, remove the FIFO panel, and optimize rendering without rewriting the algorithms. It is also what makes the report's module mapping possible: each claim points to a file and a routine.

## 7.2 Limitations and Bottlenecks

*Table 7.1 — Limitations, impact, and remediation priority*

| # | Limitation | Impact | Remediation | Priority |
|---|---|---|---|---|
| 1 | Driver registry is in-memory and reseeded on restart | Registrations and availability changes are lost | Persist drivers in a `drivers` table and rebuild the list at startup | High |
| 2 | Activity stack is in-memory and unbounded | Audit trail is lost on restart; memory grows without limit | Write events to an `activities` table; keep a bounded in-process stack | High |
| 3 | `accept_ride` does not require `OFFERED` | A transient `PENDING` ride could be accepted by any registered driver | Add `status == 'OFFERED'` to the guard | High |
| 4 | No-driver request leaves the row `PENDING` | Response and database disagree on status | Update the row to `NO_DRIVERS_AVAILABLE` in the no-driver branch | High |
| 5 | Exhausted heap is not removed from `active_ride_pqs` | Small retained-memory growth per exhausted ride | Remove the entry on the exhaustion branch | Medium |
| 6 | Hash table is implemented but unwired | Driver lookup and ride enrichment remain $O(n)$ | Maintain a hash index alongside the list, or replace the list with the table | Medium |
| 7 | Linked list has no tail pointer | Append is $O(n)$; bulk registration is $O(n^2)$ | Add a `tail` reference and update it on append/delete | Medium |
| 8 | Build uses repeated `push` instead of `heapify` | Build is $O(a\log a)$ instead of $O(a)$ | Call `heapify` with the gathered candidates | Medium |
| 9 | `update_priority` scans the heap | Update is $O(a)$, not $O(\log a)$ | Maintain an index map from driver id to heap position | Low |
| 10 | No concurrency control | Multiple workers would diverge; simultaneous accepts are not serialized | Use a single worker for the demo; adopt Redis/DB-backed state with locks for scale | High (production) |
| 11 | No authentication or authorization | Any caller can act as any role | Add JWT/session auth and role checks; scope driver actions to the authenticated driver | High (production) |
| 12 | ETA uses a constant 25 km/h and Haversine distance | Ranking ignores traffic and road geometry | Use OSRM/Valhalla travel times or a learned ETA model | Medium |
| 13 | No spatial index for nearest-driver search | Candidate construction scans all drivers | Add a k-d tree or geohash index when $n$ grows | Low |
| 14 | No database foreign keys or secondary indexes | Driver deletion leaves stale references; listings scan | Add FKs and indexes on `status`, `driver_id`, `created_at` | Low |
| 15 | Driver deletion does not update historical rides | History shows `Driver #<id>` fallback names | Retain a driver snapshot on the ride row | Low |
| 16 | OSRM route is an external dependency | Map route may fail offline | Straight-line fallback is implemented; self-host OSRM for production | Low |
| 17 | No rate limiting or coordinate validation | Out-of-range inputs are accepted as floats | Add geographic bounds and request throttling | Low |

The two most urgent correctness items are 3 and 4. They are small code changes with disproportionate value: they make the state machine honest and keep the response and database consistent. The two most urgent scalability items are 1 and 2, because they define what survives a restart.

## 7.3 Future Scope

The following enhancements are ordered by the engineering value they add, not by implementation convenience:

1. **Persist drivers and audit events.** Create `drivers` and `activities` tables, load the linked list at startup, and append events to the table while keeping a bounded in-process stack for the dashboard. This closes the durability gap without changing the algorithmic core.
2. **Harden the ride state machine.** Require `OFFERED` for acceptance, set `NO_DRIVERS_AVAILABLE` on exhaustion at request time, remove exhausted heaps, and add explicit tests for each invalid transition.
3. **Wire the hash table.** Maintain `driver_id → node` in `DriverHashTable` so that `search`, `update_availability`, and ride enrichment become expected $O(1)$. This is the highest-leverage algorithmic improvement because it affects every lifecycle action.
4. **Add a tail pointer and use heapify.** These are small changes that remove the quadratic registration pattern and improve the candidate build from $O(a\log a)$ to $O(a)$.
5. **Introduce spatial indexing.** A k-d tree or geohash index would reduce nearest-driver candidate generation from $O(n)$ to approximately $O(\log n)$ in dense areas, at the cost of more complex updates when a driver moves.
6. **Adopt traffic-aware ETA.** Replace the constant-speed model with OSRM or Valhalla travel times, or a time-of-day model, and keep Haversine as a fast pre-filter. This changes the priority key from straight-line ETA to road ETA and may require a re-ranking step when traffic updates arrive.
7. **Add authentication and role scoping.** Issue tokens to passengers and drivers, bind driver actions to the authenticated identity, and protect the DSA dashboard with an administrator role.
8. **Move to an event-driven architecture.** Replace immediate dequeue with a persistent queue and a worker, publish ride events over WebSockets, and use Redis or a database with row locks to coordinate concurrent accepts.
9. **Add payments and receipts.** Integrate a payment gateway and generate a receipt from the persisted fare breakdown.
10. **Support a larger Karachi graph.** Add more locations, route caching, and offline tile fallback to make the demonstration robust without a network connection.

## 7.4 Source Code Listings

The following excerpts are verbatim from the repository and are included so that the pseudocode in Chapter 4 can be checked against the implementation. Ellipses mark omitted lines that are not part of the routine being illustrated.

**Listing 7.1 — Geographic and fare utilities** (`backend/services/matchmaking.py`, lines 69–124)

```python
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates geographic distance between two coordinates in kilometers
    using the Haversine formula."""
    R = 6371.0  # Earth's radius in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(R * c, 2)


def calculate_eta(distance_km: float, speed_kmh: float = 25.0) -> float:
    """Estimates travel time in minutes based on distance and average city speed."""
    if distance_km <= 0.0:
        return 2.0  # Minimum ETA
    minutes = (distance_km / speed_kmh) * 60.0
    return round(max(2.0, minutes), 1)


def calculate_fare(distance_km: float, vehicle_type: str = "Bike") -> Dict[str, Any]:
    """Fare calculation according to project rates (no waiting fees):
    - Bike: Rs. 50 base + Rs. 15/km
    - Car (Standard): Rs. 100 base + Rs. 18/km
    - Good Car (Premium): Rs. 150 base + Rs. 22/km
    """
    v_type = vehicle_type.lower()
    if "bike" in v_type:
        base_fare = 50.0
        rate_per_km = 15.0
        label = "Bike (Pink Wheels)"
    elif "premium" in v_type or "good" in v_type:
        base_fare = 150.0
        rate_per_km = 22.0
        label = "Good Car (Premium)"
    else:
        base_fare = 100.0
        rate_per_km = 18.0
        label = "Car (Standard)"

    distance_charge = round(distance_km * rate_per_km, 2)
    total_fare = round(base_fare + distance_charge, 2)

    return {
        "vehicle_type": label,
        "base_fare": base_fare,
        "rate_per_km": rate_per_km,
        "distance_km": round(distance_km, 2),
        "distance_charge": distance_charge,
        "total_fare": total_fare,
        "currency": "PKR"
    }
```

**Listing 7.2 — Heap comparator, sift operations, push and pop** (`backend/dsa/priority_queue.py`, lines 27–94)

```python
def _is_higher_priority(self, a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """Determines if driver 'a' has higher priority (smaller ETA, then smaller distance)."""
    # Primary key: ETA (minutes)
    eta_a = a.get("eta_minutes", 0.0)
    eta_b = b.get("eta_minutes", 0.0)
    if eta_a != eta_b:
        return eta_a < eta_b

    # Secondary tie-breaker: Distance (km)
    dist_a = a.get("distance_km", 0.0)
    dist_b = b.get("distance_km", 0.0)
    if dist_a != dist_b:
        return dist_a < dist_b

    # Tertiary tie-breaker: driver_id for deterministic ordering
    return a.get("driver_id", 0) < b.get("driver_id", 0)

def _sift_up(self, index: int) -> None:
    """Move element at index up until min-heap property is satisfied."""
    current = index
    while current > 0:
        parent_idx = self._parent(current)
        if self._is_higher_priority(self.heap[current], self.heap[parent_idx]):
            # Swap current with parent
            self.heap[current], self.heap[parent_idx] = self.heap[parent_idx], self.heap[current]
            current = parent_idx
        else:
            break

def _sift_down(self, index: int) -> None:
    """Move element at index down until min-heap property is satisfied."""
    smallest = index
    size = len(self.heap)

    while True:
        left = self._left_child(smallest)
        right = self._right_child(smallest)
        candidate = smallest

        if left < size and self._is_higher_priority(self.heap[left], self.heap[candidate]):
            candidate = left

        if right < size and self._is_higher_priority(self.heap[right], self.heap[candidate]):
            candidate = right

        if candidate != smallest:
            self.heap[smallest], self.heap[candidate] = self.heap[candidate], self.heap[smallest]
            smallest = candidate
        else:
            break

def push(self, item: Dict[str, Any]) -> None:
    """Inserts a new driver candidate into the min-heap."""
    self.heap.append(item)
    self._sift_up(len(self.heap) - 1)

def pop(self) -> Optional[Dict[str, Any]]:
    """Removes and returns the highest priority driver (lowest ETA)."""
    if self.is_empty():
        return None
    if len(self.heap) == 1:
        return self.heap.pop()

    root = self.heap[0]
    # Move last element to root and sift down
    self.heap[0] = self.heap.pop()
    self._sift_down(0)
    return root
```

**Listing 7.3 — Candidate heap construction and best-driver offer** (`backend/services/matchmaking.py`, lines 131–169 and 235–254)

```python
def build_priority_queue_for_ride(
    pickup_lat: float,
    pickup_lon: float,
    excluded_driver_ids: Optional[set] = None,
) -> DriverPriorityQueue:
    """Step 4 to 8:
    Retrieves registered drivers from Linked List, filters available drivers,
    computes distance and ETA to pickup, and inserts eligible candidates
    into the Binary Min-Heap Priority Queue.
    """
    if excluded_driver_ids is None:
        excluded_driver_ids = set()

    pq = DriverPriorityQueue()
    current = driver_list.head

    while current is not None:
        # Check if driver is registered, available, and not excluded
        if current.is_available and current.driver_id not in excluded_driver_ids:
            dist = haversine_distance(
                current.current_latitude,
                current.current_longitude,
                pickup_lat,
                pickup_lon
            )
            eta = calculate_eta(dist)

            candidate = {
                "driver_id": current.driver_id,
                "driver_name": current.driver_name,
                "phone_number": current.phone_number,
                "vehicle_number": current.vehicle_number,
                "current_latitude": current.current_latitude,
                "current_longitude": current.current_longitude,
                "distance_km": dist,
                "eta_minutes": eta,
            }
            # Step 8: Push into custom Priority Queue (Min-Heap)
            pq.push(candidate)

        current = current.next

    return pq

# ... inside request_ride() ...

    # 4. Build custom Priority Queue from available drivers in the Linked List
    pq = build_priority_queue_for_ride(pickup_lat, pickup_lon)
    active_ride_pqs[ride_id] = pq

    # 5. Select the best driver (lowest ETA) from Priority Queue
    best_driver = pq.pop()

    if best_driver:
        # Update ride in database to OFFERED
        execute_commit(
            "UPDATE rides SET driver_id = %s, status = %s WHERE id = %s",
            (best_driver["driver_id"], "OFFERED", ride_id)
        )
        activity_stack.push({
            "ride_id": ride_id,
            "driver_id": best_driver["driver_id"],
            "event": "DRIVER_OFFERED",
            "description": (
                f"Ride #{ride_id} offered to Driver {best_driver['driver_name']} "
                f"(ETA: {best_driver['eta_minutes']} min, "
                f"{best_driver['distance_km']} km away)."
            ),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
```

**Listing 7.4 — Rejection cascade core** (`backend/services/matchmaking.py`, lines 344–389)

```python
    # Rebuild the heap if this process restarted after the ride was created.
    if ride_id not in active_ride_pqs:
        active_ride_pqs[ride_id] = build_priority_queue_for_ride(
            ride["pickup_latitude"],
            ride["pickup_longitude"],
            excluded_driver_ids={driver_id},
        )

    pq = active_ride_pqs[ride_id]
    next_driver = pq.pop() if not pq.is_empty() else None

    if next_driver:
        execute_commit(
            "UPDATE rides SET driver_id = %s, status = %s WHERE id = %s",
            (next_driver["driver_id"], "OFFERED", ride_id)
        )
        activity_stack.push({
            "ride_id": ride_id,
            "driver_id": next_driver["driver_id"],
            "event": "DRIVER_REASSIGNED",
            "description": (
                f"Ride #{ride_id} re-offered to next priority driver "
                f"{next_driver['driver_name']} "
                f"(ETA: {next_driver['eta_minutes']} min)."
            ),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return {
            "ride_id": ride_id,
            "status": "OFFERED",
            "assigned_driver": next_driver,
            "message": f"Ride reassigned to next candidate: {next_driver['driver_name']}."
        }
    else:
        execute_commit(
            "UPDATE rides SET status = %s WHERE id = %s",
            ("NO_DRIVERS_AVAILABLE", ride_id)
        )
        activity_stack.push({
            "ride_id": ride_id,
            "event": "MATCHMAKING_EXHAUSTED",
            "description": f"No further available drivers in Priority Queue for Ride #{ride_id}.",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return {
            "ride_id": ride_id,
            "status": "NO_DRIVERS_AVAILABLE",
            "assigned_driver": None,
            "message": "All eligible drivers rejected or none available in priority queue."
        }
```

**Listing 7.5 — Linked-list append, delete and search** (`backend/dsa/linked_list.py`, lines 53–74, 106–134)

```python
def append(self, driver_data: Dict[str, Any]) -> DriverNode:
    """Appends a new driver node to the end of the linked list."""
    new_node = DriverNode(
        driver_id=driver_data["driver_id"],
        driver_name=driver_data["driver_name"],
        phone_number=driver_data.get("phone_number", ""),
        vehicle_number=driver_data.get("vehicle_number", ""),
        current_latitude=float(driver_data.get("current_latitude", 24.8607)),
        current_longitude=float(driver_data.get("current_longitude", 67.0011)),
        is_available=driver_data.get("is_available", True),
    )

    if self.head is None:
        self.head = new_node
    else:
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    self._count += 1
    return new_node

def delete(self, driver_id: int) -> bool:
    """Deletes a driver node by driver_id. Returns True if deleted, False otherwise."""
    if self.head is None:
        return False

    # If head is the target
    if self.head.driver_id == driver_id:
        self.head = self.head.next
        self._count -= 1
        return True

    current = self.head
    while current.next is not None:
        if current.next.driver_id == driver_id:
            current.next = current.next.next
            self._count -= 1
            return True
        current = current.next

    return False

def search(self, driver_id: int) -> Optional[DriverNode]:
    """Searches for a driver node by driver_id. Returns node or None."""
    current = self.head
    while current is not None:
        if current.driver_id == driver_id:
            return current
        current = current.next
    return None
```

**Listing 7.6 — Stack, queue and hash-table primitives** (`backend/dsa/stack.py`, `queue.py`, `hash_table.py`)

```python
# ActivityStack.push — LIFO insertion
def push(self, activity: Dict[str, Any]) -> None:
    """Pushes a new ride activity onto the top of the stack."""
    # Ensure timestamp is recorded
    if "timestamp" not in activity:
        activity["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_node = StackNode(data=activity, next_node=self.top)
    self.top = new_node
    self._count += 1

# RideQueue.enqueue — FIFO insertion
def enqueue(self, item: Dict[str, Any]) -> None:
    """Adds a ride request to the back (rear) of the queue."""
    new_node = QueueNode(data=item)
    if self.rear is None:
        self.front = new_node
        self.rear = new_node
    else:
        self.rear.next = new_node
        self.rear = new_node
    self._count += 1

# RideQueue.dequeue — FIFO removal with empty-queue reset
def dequeue(self) -> Optional[Dict[str, Any]]:
    """Removes and returns the oldest ride request from the front of the queue."""
    if self.is_empty():
        return None

    target = self.front
    self.front = self.front.next
    if self.front is None:
        self.rear = None
    self._count -= 1
    return target.data

# DriverHashTable.put — chained insertion with update
def put(self, key: int, value: Dict[str, Any]) -> None:
    """Inserts or updates a key-value pair in O(1) average time."""
    index = self._hash(key)
    head = self.buckets[index]

    # Check if key already exists in this bucket chain; update if found
    current = head
    while current is not None:
        if current.key == key:
            current.value = value
            return
        current = current.next

    # Key not found; insert new node at the head of the chain (O(1) insertion)
    new_node = HashNode(key=key, value=value, next_node=head)
    self.buckets[index] = new_node
    self._count += 1

# DriverHashTable.get — chained lookup
def get(self, key: int) -> Optional[Dict[str, Any]]:
    """Retrieves a driver by key (driver_id) in O(1) average time."""
    index = self._hash(key)
    current = self.buckets[index]

    while current is not None:
        if current.key == key:
            return current.value
        current = current.next

    return None
```

**Source map.** The complete implementation is organized as follows:

| File | Contents |
|---|---|
| `backend/dsa/linked_list.py` | `DriverNode`, `DriverLinkedList` (append, insert, delete, search, traverse, display, size, update availability, available-driver filter) |
| `backend/dsa/priority_queue.py` | `DriverPriorityQueue` (comparator, sift-up, sift-down, push, pop, peek, heapify, update priority, non-destructive display) |
| `backend/dsa/stack.py` | `StackNode`, `ActivityStack` (push, pop, peek, display) |
| `backend/dsa/queue.py` | `QueueNode`, `RideQueue` (enqueue, dequeue, peek, display) |
| `backend/dsa/hash_table.py` | `HashNode`, `DriverHashTable` (hash, put, get, delete, bucket display) |
| `backend/dsa/sample_drivers.py` | 13 seeded driver records |
| `backend/services/matchmaking.py` | Geographic/fare utilities, global structures, matchmaking and lifecycle workflows |
| `backend/routes/*.py` | HTTP endpoints and exception-to-status mapping |
| `backend/database.py` | SQLite/PostgreSQL abstraction, schema initialization, seeding |
| `frontend/src/services/api.js` | Centralized API client |
| `frontend/src/pages/*` | Passenger, driver, and DSA dashboard interfaces |

## 7.5 References

[1] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed. Cambridge, MA, USA: MIT Press, 2022.

[2] M. T. Goodrich, R. Tamassia, and M. H. Goldwasser, *Data Structures and Algorithms in Python*. Hoboken, NJ, USA: Wiley, 2013.

[3] C. Veness, "Calculate distance, bearing and more between Latitude/Longitude points," Movable Type Scripts. [Online]. Available: https://www.movable-type.co.uk/scripts/latlong.html. [Accessed: 19-Nov-2026].

[4] FastAPI, "FastAPI documentation." [Online]. Available: https://fastapi.tiangolo.com/. [Accessed: 19-Nov-2026].

[5] Vue.js, "Vue.js documentation." [Online]. Available: https://vuejs.org/guide/. [Accessed: 19-Nov-2026].

[6] Leaflet, "Leaflet documentation." [Online]. Available: https://leafletjs.com/reference.html. [Accessed: 19-Nov-2026].

[7] Project OSRM, "Open Source Routing Machine." [Online]. Available: https://project-osrm.org/. [Accessed: 19-Nov-2026].

[8] Python Software Foundation, "Python 3 documentation." [Online]. Available: https://docs.python.org/3/. [Accessed: 19-Nov-2026].

[9] SQLite, "SQLite documentation." [Online]. Available: https://www.sqlite.org/docs.html. [Accessed: 19-Nov-2026].

[10] PostgreSQL Global Development Group, "PostgreSQL documentation." [Online]. Available: https://www.postgresql.org/docs/. [Accessed: 19-Nov-2026].

