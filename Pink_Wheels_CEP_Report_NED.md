# ABSTRACT

**Project Title: Pink Wheels — Women-Focused Ride-Hailing Platform for Karachi Using Data Structures and Algorithms**

Pink Wheels is a web-based ride-hailing platform developed to address the challenges of ride booking, driver matching, fare estimation, and ride record management in Karachi. The project combines modern web development technologies with Data Structures and Algorithms (DSA) to provide an integrated platform for passengers, women drivers, and system administrators.

The system allows passengers to register, request a ride by selecting a pickup and drop-off point on an interactive map, view a distance-based fare estimate, track the offered driver, and review their complete ride history. Drivers can register into the driver pool, receive ride offers ranked by estimated time of arrival, accept or reject an offer, complete a trip, and update their availability status. Administrators can inspect the internal state of every data structure through a dedicated DSA dashboard.

The application is developed using Vue 3, Vite, and Tailwind CSS for the frontend, Python with FastAPI and Pydantic for the backend, and SQLite for database storage, with automatic fallback from PostgreSQL for offline demonstration. Leaflet with Esri map tiles and OSRM routing provide the interactive map and driving directions.

A major focus of the project is the implementation of Data Structures and Algorithms from scratch. The system includes a singly linked list for driver registration, a FIFO queue for incoming ride requests, a binary min-heap priority queue for driver selection, a LIFO stack for ride activity history, and a chained hash table for constant-time driver lookup. Algorithms including linear search, binary search, Bubble Sort, Quick Sort, heap sift-up and sift-down, the Haversine distance formula, and complexity-driven rejection cascading are implemented.

A driver is selected by inserting every eligible driver into a min-heap keyed on estimated time of arrival, geographic distance, and driver identifier. When the offered driver rejects a ride, the next candidate is extracted from the same heap in logarithmic time, and the ride is reassigned without recomputing the entire candidate set.

A dedicated DSA Lab allows users to demonstrate these structures using live application data. The project illustrates how efficient algorithm design supports ride matching, searching, sorting, fare computation, and operational record keeping in a practical ride-hailing context.

Keywords: Data Structures and Algorithms, Pink Wheels, Ride-Hailing, Driver Matching, Priority Queue, Min-Heap, Linked List, FIFO Queue, LIFO Stack, Hash Table, Haversine Formula, FastAPI, Vue 3, SQLite.

# ACKNOWLEDGEMENT

We would like to express our sincere gratitude to our respected course instructor for providing us with the opportunity to develop Pink Wheels as part of the Complex Engineering Problem (CEP) assignment for the course Data Structures and Algorithm (SE-213).

We are grateful for the guidance, knowledge, and encouragement provided throughout the course, which helped us understand how data structures and algorithms can be applied to solve real-world computational problems.

We would also like to thank the Department of Software Engineering at NED University of Engineering & Technology for providing an academic environment that encourages technical learning, creativity, problem-solving, and teamwork.

The development of this project enabled us to apply our knowledge of linked lists, stacks, queues, priority queues, hash tables, searching, sorting, and recursion. Furthermore, integrating these concepts into a web-based application strengthened our understanding of frontend development, backend programming, database management, and software architecture.

Finally, we acknowledge the commitment and collaboration of our team members, whose contributions helped bring the project together.

Submitted By:

- Muhammad Moiz Brohi — SE-25027
- Muhammad Rahim Ali — SE-25036
- Muhammad Saad — SE-25040

# CHAPTER 1: INTRODUCTION AND PROBLEM UNDERSTANDING

## 1.1 Introduction

Transportation is an essential facility for the residents of a large metropolitan city, particularly for women who travel daily for education, employment, and family responsibilities. An efficient ride-hailing system requires the coordination of passengers, drivers, vehicles, pickup locations, and fare information.

Passengers often need accurate information about driver availability before confirming a journey. Similarly, ride-hailing operators must maintain driver records, incoming ride requests, fare estimates, and completed ride logs.

Managing these activities through disconnected information sources may result in delayed driver assignment, increased waiting time, and difficulty retrieving relevant records.

To address these challenges, Pink Wheels has been developed as a web-based women-focused ride-hailing platform.

The system combines ride-hailing functionality with the practical application of Data Structures and Algorithms (DSA). It provides dedicated interfaces for passengers and drivers, while administrators inspect the internal state of the data structures through a centralized DSA dashboard.

The application also includes a DSA Lab where algorithms can be executed and demonstrated using sample data and information from the live driver pool.

Pink Wheels therefore serves two purposes: providing a functional ride-booking platform and demonstrating how algorithmic concepts can be applied to solve computational problems in a real-world application.

## 1.2 Background of Ride-Hailing in Karachi

Ride-hailing systems involve multiple components, including passengers, drivers, vehicles, pickup and drop-off coordinates, travel distance, estimated time of arrival, and fare records.

These components are interconnected. A single ride request must locate nearby drivers, compute the distance from each candidate to the pickup point, rank the candidates, offer the ride to the best candidate, and record the outcome of the offer.

Traditional dispatch practices can involve telephone calls, manual driver lists, and verbal fare negotiation.

Although such methods may be suitable for smaller operations, they become less efficient when the number of drivers and ride requests increases.

The development of mobile positioning services, web technologies, and interactive mapping has created opportunities to improve access to ride-hailing information.

Women passengers in Karachi frequently report concerns about driver verification, fare transparency, and the reliability of the assigned driver. A platform with a verified women-only driver pool and a transparent distance-based fare directly addresses these concerns.

Pink Wheels uses these technologies to create an integrated ride-hailing environment in which matching is performed by an explicit, inspectable algorithm rather than by manual selection.

## 1.3 Problem Statement

Existing ride-hailing demonstrations commonly rely on ad-hoc driver selection, where the first available driver is assigned without comparing travel distance or expected arrival time. This produces longer passenger waiting times and makes driver utilization uneven.

In addition, the operational data of a ride-hailing service — drivers, requests, offers, rejections, and completed trips — is naturally heterogeneous. A driver registry requires fast insertion and traversal, incoming requests require fair first-in-first-out processing, candidate selection requires ordered extraction by priority, and the audit trail requires retrieval of the most recent event first.

A single generic collection cannot satisfy these requirements with acceptable complexity. The problem is therefore to design and implement a ride-hailing platform in which each operational concern is mapped to an appropriate data structure, and to demonstrate that the resulting matching process is correct, fair, and efficient.

## 1.4 Challenges in Existing Ride-Hailing Practices

### 1.4.1 Uncertainty Regarding Driver Arrival

Passengers are usually informed only that a driver has been assigned. The expected arrival time is either omitted or communicated verbally.

Without a computed distance and a consistent speed assumption, arrival estimates differ between bookings and cannot be compared.

The absence of a ranked candidate list also means that when the assigned driver declines the ride, the passenger waits again while a new driver is located manually.

### 1.4.2 Difficulty in Locating a Suitable Driver

Driver availability is often maintained in an unstructured list or a spreadsheet.

Searching such a record for a specific driver requires a linear scan, and selecting the nearest available driver requires comparing every entry.

As the driver pool grows, both operations become noticeably slower and the manual process becomes error-prone.

### 1.4.3 Manual Fare and Ride Verification

Fare computation is frequently performed verbally or with a calculator at the end of the trip.

Different drivers may apply different rates for the same distance, which makes the charge unpredictable for the passenger.

The absence of a stored ride record with a computed distance and fare prevents any later verification of the amount charged.

### 1.4.4 Management of Large Driver and Ride Datasets

A ride-hailing service generates a continuous stream of ride requests, offers, acceptances, rejections, completions, and cancellations.

Maintaining this stream in a flat file makes it difficult to determine the current status of a ride or the most recent activity.

Large datasets also make naive searches and sorts increasingly expensive.

### 1.4.5 Distance, ETA, and Fare Analysis

Deciding which driver should receive an offer requires a distance measure between geographic coordinates.

Straight-line distance computed from latitude and longitude is the standard approximation used before a road route is requested.

Converting that distance into an arrival estimate and applying a vehicle-specific fare requires consistent formulas, otherwise the matching decision and the displayed price disagree.

### 1.4.6 Passenger Safety and Trust Concerns

Women passengers place a high value on driver identity, vehicle verification, and predictable pricing.

An unverified driver pool, an unexplained assignment, and an opaque fare all reduce trust in the service.

The platform must therefore expose the assigned driver, the vehicle number, the computed distance, and the fare breakdown to the passenger.

## 1.5 Proposed Solution — Pink Wheels

Pink Wheels is a web-based ride-hailing platform in which every stage of the booking workflow is supported by an explicit data structure.

Passengers select a pickup and destination on an interactive map and receive a distance-based fare estimate before confirming the request.

The backend registers drivers in a singly linked list, enqueues the incoming request in a FIFO queue, computes the Haversine distance from every available driver to the pickup point, and inserts each eligible driver into a binary min-heap priority queue keyed on estimated time of arrival.

The root of the heap is offered the ride. If the offer is rejected, the next candidate is extracted from the same heap and the ride is reassigned.

Every event is pushed onto a LIFO activity stack, so the most recent event is always available first.

All structures are exposed through a DSA dashboard, which makes the internal state of the algorithm visible for academic evaluation.

## 1.6 Project Objectives

The objectives of the project are:

1. To develop a functional ride-hailing platform for a women-only driver pool in Karachi.
2. To implement a singly linked list for driver registration, search, deletion, and availability management.
3. To implement a FIFO queue for incoming ride requests.
4. To implement a binary min-heap priority queue for driver ranking by estimated time of arrival.
5. To implement a LIFO stack for ride activity history.
6. To implement a chained hash table for constant-time driver lookup and demonstrate it in the DSA Lab.
7. To implement the Haversine distance formula, ETA estimation, and vehicle-specific fare calculation.
8. To demonstrate Bubble Sort and Quick Sort as design-level comparison algorithms.
9. To analyze the time and space complexity of every implemented operation.
10. To verify correctness through an automated test suite and a reproducible demonstration dataset.

## 1.7 Scope of the Project

### 1.7.1 Passenger Module

The passenger module allows a passenger to enter a name and phone number, select pickup and destination coordinates on the map, choose a vehicle type, view the fare estimate, request a ride, observe the offered driver, complete or cancel the ride, and review the ride history.

### 1.7.2 Driver Module

The driver module allows a driver to view the ride currently offered, inspect the passenger and route information, accept or reject the offer, complete an accepted trip, and observe the change in availability status within the linked list.

### 1.7.3 Administrator Module

The administrator module provides the DSA dashboard. It displays the linked list chain, the FIFO queue contents, the priority queue in both heap-array and sorted order, the activity stack, and a step-by-step matchmaking simulation.

### 1.7.4 DSA Lab Module

The DSA Lab exposes the internal structures through read-only endpoints and a matchmaking simulation endpoint, so that each algorithmic step can be demonstrated with live application data.

### 1.7.5 Matchmaking and Network Analysis

The matchmaking analysis covers candidate construction, heap ordering, deterministic tie-breaking, offer assignment, and the rejection cascade.

The network analysis covers geodesic distance between coordinates, the assumed average city speed, and the vehicle-specific fare schedule.

### 1.7.6 Current Limitations

The driver pool is initialized from a fixed sample file of thirteen verified women drivers.

Road routing is requested from a public routing service, while matchmaking itself uses straight-line Haversine distance.

The hash table is fully implemented and demonstrated but is not yet used by the matchmaking path.

User authentication is simplified for the academic demonstration.

## 1.8 Significance of Data Structures and Algorithms

The ride-hailing domain exercises several distinct access patterns simultaneously.

Driver registration is an append-dominated workload, which a singly linked list supports with constant-time insertion at the tail when a tail reference is maintained and linear-time traversal otherwise.

Incoming requests are processed in arrival order, which is the defining behaviour of a FIFO queue.

Candidate selection requires repeated extraction of the minimum element, which a binary min-heap performs in logarithmic time and which repeated linear scans perform in linear time per extraction.

Alternatively, a sorted array would support constant-time minimum access but would require linear-time insertion for every new candidate.

The activity history is read most-recent-first, which a LIFO stack serves in constant time.

Direct driver lookup is a classic key-value problem for which a chained hash table provides average constant-time access.

Selecting the correct structure for each concern, rather than reusing one collection for all of them, is the central engineering lesson of the project.

## 1.9 Benefits of the Proposed System

The system provides transparent driver assignment, because the ranked candidate list is computed from explicit distance and ETA values.

The system provides predictable pricing, because the fare is computed from the stored trip distance and a fixed vehicle-specific rate.

The system provides a complete audit trail, because every ride event is pushed onto the activity stack.

The system provides efficient reassignment, because a rejection extracts the next candidate from the existing heap in logarithmic time.

The system provides academic visibility, because every structure can be inspected through the DSA dashboard.

## 1.10 Alignment with Course Learning Outcomes

CLO 2 requires the ability to analyze a computing problem and identify the data structures and algorithms appropriate to its solution. The matching workflow of Pink Wheels is a direct instance of this outcome: the problem of repeatedly selecting the nearest available driver determines the choice of a priority queue.

CLO 3 requires the ability to design and implement solutions using appropriate data structures. The project implements the linked list, FIFO queue, min-heap, LIFO stack, and chained hash table from scratch, without relying on library implementations of the same structures.

CLO 4 requires the ability to evaluate the complexity of a solution. Chapter 9 derives the best-case, average-case, and worst-case bounds of every operation and compares them in a single asymptotic summary table.

The Complex Engineering Problem attributes are addressed through the breadth of the requirement set, the depth of the algorithmic analysis, the integration of frontend, backend, and data structures, and the explicit treatment of constraints such as offline database fallback and deterministic tie-breaking.

## 1.11 Chapter Summary

This chapter introduced the ride-hailing problem in Karachi, described the limitations of manual dispatch, and presented Pink Wheels as a data-structure-driven solution.

It defined the project objectives, scope, and limitations, and explained why each operational concern maps to a specific data structure.

The next chapter identifies the functional, non-functional, and algorithmic requirements of the system.

# CHAPTER 2: REQUIREMENT IDENTIFICATION AND SYSTEM ANALYSIS

## 2.1 Introduction

Requirement identification is an important phase of software engineering because it establishes the expected behavior, technical capabilities, constraints, and performance considerations of a system.

Pink Wheels combines ride-hailing functionality with algorithmic problem-solving. Therefore, its requirements are classified into functional requirements, non-functional requirements, algorithmic requirements, hardware requirements, and software requirements.

The functional requirements describe the operations performed by passengers, drivers, and administrators. The algorithmic requirements identify the data structures and algorithms implemented to satisfy the Complex Engineering Problem assignment.

## 2.2 Functional Requirements

### 2.2.1 Passenger Registration and Login

The system shall allow a passenger to create a record using a name and a phone number.

The system shall list existing passengers so that a ride can be requested on behalf of a selected passenger.

The ride records shall reference the passenger identifier.

### 2.2.2 Ride Request and Fare Estimation

The system shall accept a pickup location, a destination location, and a vehicle type.

The system shall compute the geodesic distance between the pickup and destination coordinates using the Haversine formula.

The system shall compute the fare from the distance and the selected vehicle type before the request is confirmed.

The system shall support three vehicle categories: Bike, Car, and Good Car (Premium).

### 2.2.3 Driver Matchmaking and Offer

The system shall register thirteen verified women drivers in a singly linked list at startup.

The system shall consider only drivers whose availability flag is true.

The system shall compute the Haversine distance and the estimated time of arrival from each eligible driver to the pickup point.

The system shall insert each eligible driver into a binary min-heap priority queue and offer the ride to the root of the heap.

If no driver is available, the ride shall be recorded with the status NO_DRIVERS_AVAILABLE.

### 2.2.4 Driver Trip Management

The system shall allow a driver to view the ride currently offered to that driver.

The system shall display the passenger, the pickup and destination labels, the computed distance, the fare, and the vehicle type.

The system shall allow the driver to mark an accepted ride as completed.

### 2.2.5 Ride Acceptance and Rejection

The system shall allow only the driver currently holding the offer to accept or reject the ride.

The system shall reject invalid state transitions, such as accepting a completed or cancelled ride.

The system shall mark a driver as busy in the linked list when the ride is accepted and as available again when the ride is completed or cancelled.

### 2.2.6 Rejection Cascade and Reassignment

When an offered driver rejects a ride, the system shall extract the next candidate from the ride's priority queue.

The system shall update the ride status and the offered driver identifier in the database.

The system shall record both the rejection and the reassignment as separate activity events.

If the priority queue is exhausted, the ride shall be marked as NO_DRIVERS_AVAILABLE.

### 2.2.7 Ride Queue and Listing

The system shall enqueue every incoming ride request into a FIFO queue before matchmaking begins.

The system shall dequeue the request once it is being processed.

The system shall list rides in descending identifier order, with the driver name, phone number, and vehicle number attached from the linked list.

### 2.2.8 Passenger Activity History

The system shall push every ride event onto a LIFO activity stack.

The system shall expose the activity stack from the most recent event to the oldest event.

The system shall record the timestamp of each event.

### 2.2.9 Administrative Management

The system shall expose the state of the linked list, the FIFO queue, the priority queue, and the activity stack through administrative endpoints.

The system shall provide a step-by-step matchmaking simulation that explains each stage of candidate selection.

### 2.2.10 DSA Lab

The system shall provide a DSA dashboard in the frontend that visualizes the linked list chain, the queue contents, the heap array, the sorted priority order, and the activity stack.

The system shall allow the administrator to trigger a matchmaking demonstration for a selected pickup coordinate.

## 2.3 Non-Functional Requirements

### 2.3.1 Performance

Matchmaking shall complete within a fraction of a second for a driver pool of the demonstrated size.

Candidate selection shall be performed in logarithmic time per extraction rather than by repeated full scans.

Frontend animations shall remain responsive during data refreshes.

### 2.3.2 Security

The backend shall validate the state of a ride before applying any transition.

The system shall prevent a driver from accepting an offer issued to another driver.

Database statements shall use parameterized queries to avoid SQL injection.

### 2.3.3 Reliability

The database layer shall fall back from PostgreSQL to SQLite when no PostgreSQL server is reachable, so that a demonstration never fails because of an unavailable database service.

The matchmaking service shall rebuild a ride's priority queue if the process restarted after the ride was created.

Repeated completion of the same ride shall be idempotent.

### 2.3.4 Usability

The passenger interface shall present the fare estimate before the request is confirmed.

The driver interface shall show a single clear action for accept, reject, and complete.

The DSA dashboard shall explain the purpose of each structure.

### 2.3.5 Maintainability

The data structures shall be implemented in a dedicated package with one module per structure.

The matchmaking workflow shall be implemented in a service module rather than inside the route handlers.

The database access layer shall expose generic query and commit helpers.

### 2.3.6 Scalability

The driver pool shall be mutable at runtime through registration and deletion endpoints.

The priority queue implementation shall support heap construction from an arbitrary candidate list in linear time, allowing a future move from per-ride heaps to an indexed global heap without changing the interface.

## 2.4 Data Structures and Algorithm Requirements

### 2.4.1 Linked Lists and Sorting

The project requires a singly linked list with append, insert, delete, search, traverse, and availability update operations.

The linked list serves as the authoritative registry of drivers during matchmaking.

The project also requires the implementation of Bubble Sort with an early-exit flag and Quick Sort with the Lomuto partition scheme, as design-level comparison algorithms for ordering candidate sets.

### 2.4.2 Stack and Recursion

The project requires a LIFO stack with push, pop, peek, and display operations.

The stack records ride events in chronological order and returns them in reverse chronological order.

The project also requires a recursive formulation of list traversal and replay, to demonstrate the relationship between recursion and the implicit call stack.

### 2.4.3 Queue Algorithms

The project requires a FIFO queue with enqueue, dequeue, peek, and display operations.

The queue represents incoming ride requests and guarantees that requests are processed in arrival order.

The project also requires a bulk intake routine that drains a queue of pending requests in arrival order.

### 2.4.4 Priority Queue and Heaps

The project requires a binary min-heap priority queue with push, pop, peek, heapify, and priority update operations.

The priority order shall be the estimated time of arrival, then the geographic distance, then the driver identifier.

The project requires explicit sift-up and sift-down routines so that the heap maintenance steps can be demonstrated and analyzed.

### 2.4.5 Hash Tables and Geographic Algorithms

The project requires a chained hash table with put, get, delete, and bucket display operations.

The project requires the Haversine distance formula, an ETA conversion using an assumed average city speed, and a vehicle-specific fare schedule.

The project requires a deterministic rejection cascade built on repeated minimum extraction from the priority queue.

## 2.5 Integration of Data Structures with Application Modules

Table 2.1 lists each data structure, the module that implements it, and the application feature that consumes it.

| Data Structure / Algorithm | Implementation Module | Consuming Application Feature |
|---|---|---|
| Singly Linked List | backend/dsa/linked_list.py | Driver registration, availability, ride listing enrichment |
| FIFO Queue | backend/dsa/queue.py | Incoming ride request intake |
| Binary Min-Heap Priority Queue | backend/dsa/priority_queue.py | Candidate ranking and driver selection |
| LIFO Stack | backend/dsa/stack.py | Ride activity history and DSA dashboard |
| Chained Hash Table | backend/dsa/hash_table.py | Constant-time driver lookup in the DSA Lab |
| Haversine Distance | backend/services/matchmaking.py | Distance, ETA, and fare computation |
| ETA and Fare Rules | backend/services/matchmaking.py | Passenger fare estimate and ride pricing |
| Rejection Cascade | backend/services/matchmaking.py | Reassignment after a declined offer |
| Bubble Sort and Quick Sort | backend/dsa (design-level) | Candidate ordering demonstration in the DSA Lab |

The matchmaking service is the integration point. It traverses the linked list, filters by availability, computes geographic values, pushes candidates into the priority queue, and logs each event onto the activity stack.

The route layer is deliberately thin. It validates the request body, delegates to the service, and translates service exceptions into HTTP status codes.

## 2.6 Hardware Requirements

The application is designed to run on standard laptop hardware. Table 2.2 lists the development and demonstration requirements.

| Component | Minimum Requirement | Recommended Requirement |
|---|---|---|
| Processor | Dual-core 2.0 GHz | Quad-core 2.4 GHz or higher |
| Memory | 4 GB RAM | 8 GB RAM or higher |
| Storage | 1 GB free space | 5 GB free space |
| Display | 1366 × 768 | 1920 × 1080 |
| Network | Localhost only | Internet access for map tiles and routing |

The map tiles and road routing are optional at runtime; matchmaking itself is fully local because Haversine distance is computed on the server.

## 2.7 Software Requirements

Table 2.3 lists the software stack used to develop and run the system.

| Layer | Technology | Purpose |
|---|---|---|
| Frontend framework | Vue 3 | Component-based user interface |
| Build tool | Vite | Development server and production bundling |
| Styling | Tailwind CSS | Utility-first styling and design tokens |
| State management | Pinia | Passenger, driver, and health stores |
| Mapping | Leaflet with Esri tiles | Interactive pickup and destination selection |
| Routing | OSRM public routing service | Road distance and route geometry |
| Backend framework | FastAPI | REST API and request validation |
| Validation | Pydantic | Request and response schemas |
| Database driver | SQLite, PostgreSQL via psycopg | Persistent ride and passenger records |
| Testing | pytest | Automated verification of structures and workflows |
| Language | Python 3.12, JavaScript (ES modules) | Backend and frontend implementation |

The backend depends only on the standard library for the data structures themselves. No heapq, queue.PriorityQueue, or collections.deque implementation is used for the graded structures.

## 2.8 Assumptions and System Constraints

The system assumes that driver coordinates are supplied in the sample driver file and are accurate to the neighbourhood level.

The system assumes an average city speed of 25 kilometres per hour for arrival estimation, with a minimum estimate of 2.0 minutes.

The system assumes that a passenger requests rides for one of the registered passenger records.

The system constrains a ride to a single active offer at any time.

The system constrains driver availability to a boolean state, because a driver can serve at most one ride at a time.

The system does not model payments, driver ratings, or live GPS streaming; these are outside the academic scope.

The database schema is intentionally small, because the graded behaviour resides in the in-memory data structures.

## 2.9 Chapter Summary

This chapter defined the functional, non-functional, and algorithmic requirements of Pink Wheels.

It mapped every data structure to its implementation module and consuming feature, and listed the hardware and software environment.

It also documented the assumptions and constraints that bound the current implementation.

The next chapter presents the system design and architecture.

# CHAPTER 3: SYSTEM DESIGN AND ARCHITECTURE

## 3.1 Introduction to System Architecture

System architecture defines how different software components interact to achieve the overall objectives of an application.

Pink Wheels uses a modular web-based architecture that separates user interface functionality, server-side processing, persistent data storage, and custom data structures and algorithms.

This separation allows individual components to be developed, tested, and maintained independently.

The application includes a Vue frontend, a FastAPI backend, an SQLite database with PostgreSQL fallback, and a dedicated DSA implementation package.

The frontend is responsible for displaying information and receiving user input, while the backend manages ride state, matchmaking, fare calculation, and database operations.

The DSA components support ride matching and record keeping, and provide algorithm demonstrations through the DSA dashboard.

## 3.2 Overall System Architecture

The system follows a layered client-server architecture consisting of four main logical components.

### 3.2.1 Presentation Layer

The presentation layer provides web interfaces through which passengers, drivers, and administrators interact with the application.

The passenger interface contains ride booking, fare estimation, live ride status, and ride history.

The driver interface contains the current offer, ride actions, and driver availability.

The administrator interface contains the DSA dashboard with the linked list, queue, heap, stack, and matchmaking simulation.

### 3.2.2 Application Layer

The application layer is implemented using FastAPI and Pydantic.

It processes requests received from the frontend, validates request bodies, applies ride state rules, and returns structured JSON responses.

The matchmaking service in this layer coordinates the linked list, the FIFO queue, the priority queue, and the activity stack.

### 3.2.3 Data Structures and Algorithms Layer

The DSA layer contains custom implementations of a singly linked list, a FIFO queue, a binary min-heap priority queue, a LIFO stack, and a chained hash table.

These implementations are used directly by the matchmaking service and are exposed through demonstration endpoints.

### 3.2.4 Data Storage Layer

The data storage layer uses SQLite for persistent passenger and ride records, with PostgreSQL used automatically when a database URL is reachable.

A small database helper module abstracts connections, parameter adaptation, and insert identifier retrieval for both engines.

Information stored in the database includes passengers, rides, coordinates, distance, fare, vehicle type, status, and driver assignment.

## 3.3 Frontend Architecture

The frontend is a single-page application built with Vue 3 and the Composition API.

Routing is handled by Vue Router with five routes: passenger home, passenger ride status, passenger history, driver dashboard, and the administrative DSA dashboard.

Global state is managed with Pinia stores. The health store probes the backend connection and database engine; the ride and passenger data are fetched through a shared API service.

### 3.3.1 Passenger Interface

The passenger home page presents a map for pickup and destination selection.

The page shows the computed distance and fare before the request is submitted.

After a request is submitted, the ride status page displays the offered driver, the vehicle number, the fare breakdown, and the ride state.

The history page lists previous rides with their status and assigned driver.

### 3.3.2 Driver Interface

The driver dashboard lists the rides currently offered or accepted.

Each ride card shows the passenger, the pickup and destination labels, the distance, and the fare.

The card exposes accept, reject, and complete actions according to the current ride status.

### 3.3.3 DSA Dashboard

The DSA dashboard visualizes the driver linked list as a node chain, the FIFO queue as a front-to-rear sequence, the priority queue as a heap array with the sorted priority order, and the activity stack as a top-to-bottom list.

It also presents the matchmaking simulation as a numbered sequence of steps.

### 3.3.4 Reusable Components

The map component wraps Leaflet and emits selected coordinates to its parent.

The API service centralizes the base URL and error handling for all requests.

Shared styles define the design tokens used across pages.

## 3.4 Backend Architecture

The backend is organized into routes, services, data structures, and database helpers.

### 3.4.1 Accounts and Passenger Module

The passenger routes create and list passenger records.

The passenger table stores the passenger name and phone number, and ride records reference the passenger identifier.

### 3.4.2 Rides Module

The ride routes expose fare estimation, ride creation, ride listing, ride detail, accept, reject, complete, and cancel.

Each route delegates to the matchmaking service, which enforces the ride state rules.

### 3.4.3 Matchmaking Module

The matchmaking service holds the in-memory instances of the linked list, the FIFO queue, the activity stack, and the per-ride priority queues.

It implements candidate construction, offer assignment, acceptance, rejection with reassignment, completion, cancellation, distance, ETA, and fare computation.

### 3.4.4 Driver Module

The driver routes register a new driver node into the linked list, search a driver by identifier, delete a driver, and update availability.

Driver identifiers are generated from the highest existing identifier when one is not supplied.

### 3.4.5 DSA Module

The DSA routes expose the linked list, queue, priority queue, and stack in read-only form, and provide a matchmaking simulation endpoint that explains each step.

## 3.5 Database Architecture

The database contains two tables, passengers and rides. Table 3.1 lists the passenger entity and Table 3.2 lists the ride entity.

**Table 3.1 — Passenger Entity**

| Field | Type | Description |
|---|---|---|
| id | INTEGER, primary key | Unique passenger identifier |
| name | VARCHAR(100), not null | Passenger name |
| phone | VARCHAR(50), not null | Passenger contact number |

**Table 3.2 — Ride Entity**

| Field | Type | Description |
|---|---|---|
| id | INTEGER, primary key | Unique ride identifier |
| passenger_id | INTEGER | Reference to the passenger |
| driver_id | INTEGER, nullable | Assigned driver identifier until completion |
| pickup_location | TEXT, not null | Human-readable pickup label |
| destination | TEXT, not null | Human-readable destination label |
| pickup_latitude, pickup_longitude | DOUBLE PRECISION | Pickup coordinates |
| destination_latitude, destination_longitude | DOUBLE PRECISION | Destination coordinates |
| distance_km | DOUBLE PRECISION | Haversine trip distance |
| fare | DOUBLE PRECISION | Computed total fare in PKR |
| vehicle_type | VARCHAR(50) | Bike, Car, or Premium |
| status | VARCHAR(50) | Current ride state |
| created_at | TIMESTAMP | Creation timestamp |

### 3.5.1 Passenger Entity

The passenger entity stores the identity of the person requesting rides.

The entity is seeded with three demonstration passengers when the table is empty.

### 3.5.2 Ride Entity

The ride entity stores every value required to reproduce the fare and the assignment decision.

The ride identifier is the key used by the priority queue registry, which allows the rejection cascade to resume with the correct candidate set.

### 3.5.3 Relationship Between Entities

A passenger may have many rides, while each ride references exactly one passenger.

A ride references at most one driver at any time, because a driver serves one ride at a time.

Driver records are held in the in-memory linked list rather than in the relational schema, because the graded requirement is the custom structure itself.

### 3.5.4 In-Memory Structures Versus Persistent Storage

The database stores the durable outcome of each operation.

The linked list, queue, heap, and stack hold the operational state used by the algorithm.

The two representations are synchronized whenever a ride transitions, so that the database always reflects the latest committed status.

### 3.5.5 Database Fallback Behaviour

The connection helper attempts PostgreSQL when a PostgreSQL URL is configured.

If the connection fails within the configured timeout, the process disables PostgreSQL for its lifetime and uses the bundled SQLite file.

This behaviour keeps the demonstration reproducible on machines without a database server.

## 3.6 REST API Design and Communication

The backend exposes a JSON REST API. Table 3.3 summarizes the endpoint groups.

| Group | Endpoints | Purpose |
|---|---|---|
| Authentication and health | GET /api/health | Reports service and database status |
| Passengers | GET /api/passengers, POST /api/passengers | List and create passenger records |
| Drivers | GET /api/drivers, POST /api/drivers/register, GET/DELETE /api/drivers/{id}, PATCH /api/drivers/{id}/availability | Manage the driver linked list |
| Rides | POST /api/rides/estimate-fare, POST /api/rides/request, GET /api/rides, GET /api/rides/{id} | Quote and create rides |
| Ride actions | POST /api/rides/{id}/accept, /reject, /complete, /cancel | Apply ride transitions |
| DSA inspection | GET /api/dsa/linked-list, /queue, /priority-queue, /stack | Inspect structures |
| DSA simulation | POST /api/dsa/matchmaking | Step-by-step matching demonstration |

### 3.6.1 Authentication APIs

The health endpoint verifies that the database layer responds.

The current academic build does not issue tokens; the passenger identity is supplied explicitly with each ride request.

### 3.6.2 Ride APIs

Fare estimation accepts two coordinate pairs and a vehicle type and returns the fare breakdown.

Ride creation accepts the passenger, the locations, the coordinates, and the vehicle type, runs matchmaking, and returns the assigned driver.

Ride listing accepts an optional status filter and enriches each record with driver details from the linked list.

### 3.6.3 Matchmaking APIs

The matchmaking simulation accepts a pickup coordinate and returns five steps: linked list traversal, availability filtering, distance and ETA computation, heap construction, and top driver selection.

The response includes the ranked driver list so that the ordering can be verified independently.

### 3.6.4 Driver APIs

Driver registration appends a node to the linked list.

Availability updates change the boolean flag used by candidate construction.

Deletion removes a node and reports the new size of the list.

### 3.6.5 DSA APIs

The inspection endpoints return the size, the human-readable chain, and the structured contents of each structure.

The priority queue endpoint accepts optional coordinates and returns the internal heap array together with the sorted priority order.

## 3.7 Authentication and Role-Based Authorization

The current implementation is an academic demonstration and therefore uses a simplified authorization model.

The passenger interface selects an existing passenger record before booking.

The driver interface selects an existing driver from the linked list before applying an action.

The backend enforces the critical ownership rule: a ride action is accepted only from the driver currently holding the offer.

The DSA dashboard is presented as an administrative view and performs read-only operations.

A production deployment would replace this model with token-based authentication and explicit role claims.

## 3.8 DSA Module Architecture

The DSA package is organized as one module per structure. Each module exposes a class with a minimal, documented interface and no dependency on the web framework.

### 3.8.1 Linked List and Sorting Components

The DriverLinkedList class manages DriverNode instances.

It provides append, insert, delete, search, traverse, display, size, availability update, and available-driver filtering.

The sorting components implement Bubble Sort with early exit and Quick Sort with Lomuto partitioning as design-level utilities.

### 3.8.2 Stack and Recursion Components

The ActivityStack class manages StackNode instances with push, pop, peek, size, and display.

A recursive formulation of list traversal is included in the demonstration to connect the explicit stack to the implicit call stack.

### 3.8.3 Queue and Heap Components

The RideQueue class manages QueueNode instances with front and rear pointers.

The DriverPriorityQueue class manages a Python list as the heap array and implements parent and child index arithmetic, priority comparison, sift-up, sift-down, push, pop, peek, heapify, and priority update.

### 3.8.4 Priority Queue Components

The priority comparison is a three-level comparator: estimated time of arrival, then geographic distance, then driver identifier.

The third level guarantees deterministic ordering when two drivers have identical ETA and distance.

The heapify routine builds a heap from an arbitrary candidate list in linear time.

### 3.8.5 Hash Table Components

The DriverHashTable class manages HashNode chains across a fixed bucket array.

The hash function maps an integer key to a bucket with modulo arithmetic, and collisions are resolved by prepending to the bucket chain.

### 3.8.6 Supporting Data Structures

The sample driver module provides the initial thirteen driver records with Karachi neighbourhood coordinates.

The matchmaking service module provides the geographic and fare utilities shared by the ride routes and the DSA routes.

### 3.8.7 DSA Demonstration and Testing

The DSA dashboard and the simulation endpoint expose the structures for demonstration.

The automated test suite covers the linked list, the priority queue, the stack, matching and fare rules, the ride lifecycle, and the full system workflow.

## 3.9 System Architecture Diagram

The architecture diagram shows the following major components:

1. Users: Passengers, Drivers, and Administrators.
2. Frontend: Vue 3 and Vite.
3. Communication: REST APIs using HTTP and JSON.
4. Backend: FastAPI and Pydantic.
5. DSA Package: Linked list, queue, priority queue, stack, and hash table.
6. Database: SQLite with PostgreSQL fallback.
7. Map Services: Leaflet with Esri tiles and OSRM routing.

The frontend communicates with the backend through API requests and responses.

The backend uses the DSA package for candidate construction, ranking, and activity logging, and accesses SQLite through the database helper.

Administrators additionally access the DSA dashboard.

[[FIG:images/fig-3-1-architecture.png|Figure 3.1 — Pink Wheels System Architecture]]

## 3.10 Use Case Diagram

The use case diagram represents the interaction between the application's users and its functional features.

Passengers book rides, view fare estimates, track ride status, and review history.

Drivers inspect offers, accept or reject rides, complete trips, and update availability.

Administrators inspect the data structures and run the matchmaking simulation.

[[FIG:images/fig-3-2-usecase.png|Figure 3.2 — Use Case Diagram]]

## 3.11 Data Flow Diagram

The Data Flow Diagram illustrates how information travels between users, application processes, and data stores.

### 3.11.1 Context-Level DFD

At the context level, Pink Wheels is represented as a single system interacting with passengers, drivers, and administrators.

Passengers submit registration information, ride requests, and cancellations, and receive fare estimates, driver details, and ride status.

Drivers submit availability and offer decisions, and receive ride details.

Administrators request structure snapshots and receive the current state of the data structures.

[[FIG:images/fig-3-3-dfd-context.png|Figure 3.3 — Data Flow Diagram (Level 0 / Context)]]

### 3.11.2 Level 1 DFD

At Level 1, Pink Wheels can be divided into the following processes:

**Process 1 — Passenger and Account Management**

Receives passenger information, validates it, and stores the passenger record.

**Process 2 — Fare Estimation**

Receives pickup and destination coordinates and returns the Haversine distance and the vehicle-specific fare.

**Process 3 — Ride Intake and Queueing**

Receives a confirmed ride request, enqueues it in the FIFO queue, and writes the ride record.

**Process 4 — Driver Matchmaking**

Traverses the driver linked list, filters available drivers, computes distance and ETA, builds the min-heap, and selects the top candidate.

**Process 5 — Offer Lifecycle**

Receives accept, reject, complete, or cancel decisions, updates the ride state, and logs the event on the activity stack.

**Process 6 — DSA Demonstration**

Receives inspection requests, traverses the requested structure, and returns its contents.

[[FIG:images/fig-3-4-dfd-level1.png|Figure 3.4 — Data Flow Diagram (Level 1)]]

## 3.12 Entity Relationship Diagram

The entity relationship model contains the passenger and ride entities.

One passenger can request many rides, which establishes a one-to-many relationship between passenger and ride.

Each ride references exactly one passenger through the passenger identifier.

Each ride references at most one driver through the driver identifier.

Driver records are not stored in the relational schema; they are held in the in-memory linked list and resolved when a ride is read.

The relationship model is therefore intentionally asymmetric: durable facts are persisted, while operational ordering is maintained in the graded data structures.

## 3.13 Chapter Summary

This chapter described the layered architecture of Pink Wheels, the responsibilities of the frontend and backend modules, the database entities, the REST API surface, and the internal organization of the DSA package.

It also presented the system architecture diagram, the use case diagram, the two levels of data flow diagrams, and the entity relationship model.

The next section presents the algorithm design document with the pseudocode of every required algorithm.
# ALGORITHM DESIGN DOCUMENT

Each required solution is written below in step-by-step pseudocode, with its time complexity. All of them are implemented from scratch in the project (backend/dsa/ and backend/services/). A flowchart of one selected algorithm (driver matchmaking) is given at the end.

## 4. Linked Lists and Sorting

[[ALG:Append a driver to the chain|O(n); O(1) with a tail pointer]]
```pseudo
ALGORITHM AppendDriver(L, driver)
  create node N from driver data
  IF L.head = NULL THEN
    L.head ← N
  ELSE
    current ← L.head
    WHILE current.next ≠ NULL DO
      current ← current.next
    current.next ← N
  L.count ← L.count + 1
  RETURN N
```

[[ALG:Insert a driver at a position|O(n)]]
```pseudo
ALGORITHM InsertAt(L, index, driver)
  IF index < 0 OR index > L.count THEN
    ERROR "index out of bounds"
  create node N from driver data
  IF index = 0 THEN
    N.next ← L.head; L.head ← N
  ELSE
    current ← L.head
    FOR step ← 0 TO index - 2 DO
      current ← current.next
    N.next ← current.next
    current.next ← N
  L.count ← L.count + 1
  RETURN N
```

[[ALG:Delete a driver by identifier|O(n)]]
```pseudo
ALGORITHM DeleteDriver(L, driver_id)
  IF L.head = NULL THEN RETURN FALSE
  IF L.head.driver_id = driver_id THEN
    L.head ← L.head.next; L.count ← L.count - 1
    RETURN TRUE
  current ← L.head
  WHILE current.next ≠ NULL DO
    IF current.next.driver_id = driver_id THEN
      current.next ← current.next.next
      L.count ← L.count - 1
      RETURN TRUE
    current ← current.next
  RETURN FALSE
```

[[ALG:Search a driver by identifier|O(n)]]
```pseudo
ALGORITHM SearchDriver(L, driver_id)
  current ← L.head
  WHILE current ≠ NULL DO
    IF current.driver_id = driver_id THEN RETURN current
    current ← current.next
  RETURN NULL
```

[[ALG:Traverse the chain|O(n)]]
```pseudo
ALGORITHM Traverse(L)
  result ← empty list
  current ← L.head
  WHILE current ≠ NULL DO
    APPEND result, current as record
    current ← current.next
  RETURN result
```

[[ALG:Update driver availability|O(n)]]
```pseudo
ALGORITHM UpdateAvailability(L, driver_id, flag)
  node ← SearchDriver(L, driver_id)
  IF node = NULL THEN RETURN FALSE
  node.available ← flag
  RETURN TRUE
```

[[ALG:Collect available drivers|O(n)]]
```pseudo
ALGORITHM AvailableDrivers(L)
  available ← empty list
  current ← L.head
  WHILE current ≠ NULL DO
    IF current.available = TRUE THEN
      APPEND available, current
    current ← current.next
  RETURN available
```

[[ALG:Linear search over a region list|best O(1), avg/worst O(n)]]
```pseudo
ALGORITHM LinearSearch(A, key, field)
  FOR i ← 0 TO length(A) - 1 DO
    IF field(A[i]) = key THEN RETURN i
  RETURN -1
```

[[ALG:Binary search on a sorted ETA array|best O(1), avg/worst O(log n)]]
```pseudo
ALGORITHM BinarySearch(A, key, field)
  low ← 0; high ← length(A) - 1
  WHILE low ≤ high DO
    mid ← floor((low + high) / 2)
    value ← field(A[mid])
    IF value = key THEN RETURN mid
    ELSE IF value < key THEN low ← mid + 1
    ELSE high ← mid - 1
  RETURN -1
```

[[ALG:Bubble sort with early exit|best O(n), avg/worst O(n²)]]
```pseudo
ALGORITHM BubbleSort(A, field)
  FOR end ← length(A) - 1 DOWN TO 1 DO
    swapped ← FALSE
    FOR j ← 0 TO end - 1 DO
      IF field(A[j]) > field(A[j+1]) THEN
        swap A[j], A[j+1]; swapped ← TRUE
    IF swapped = FALSE THEN STOP
  RETURN A
```

[[ALG:Quick sort with Lomuto partition|best/avg O(n log n), worst O(n²)]]
```pseudo
ALGORITHM QuickSort(A, low, high, field)
  IF low < high THEN
    p ← Partition(A, low, high, field)
    QuickSort(A, low, p - 1, field)
    QuickSort(A, p + 1, high, field)

ALGORITHM Partition(A, low, high, field)
  pivot ← field(A[high]); i ← low - 1
  FOR j ← low TO high - 1 DO
    IF field(A[j]) ≤ pivot THEN
      i ← i + 1; swap A[i], A[j]
  swap A[i+1], A[high]
  RETURN i + 1
```

## 5. Stacks and Recursion

[[ALG:Push an activity|O(1)]]
```pseudo
ALGORITHM Push(S, activity)
  IF activity.timestamp missing THEN
    activity.timestamp ← current date and time
  node ← new StackNode(activity, next = S.top)
  S.top ← node
  S.count ← S.count + 1
```

[[ALG:Pop the most recent activity|O(1)]]
```pseudo
ALGORITHM Pop(S)
  IF S.top = NULL THEN RETURN NULL
  target ← S.top
  S.top ← S.top.next
  S.count ← S.count - 1
  RETURN target.data
```

[[ALG:Peek the most recent activity|O(1)]]
```pseudo
ALGORITHM Peek(S)
  IF S.top = NULL THEN RETURN NULL
  RETURN S.top.data
```

[[ALG:Display the stack top to bottom|O(n)]]
```pseudo
ALGORITHM DisplayStack(S)
  result ← empty list
  current ← S.top
  WHILE current ≠ NULL DO
    APPEND result, current.data
    current ← current.next
  RETURN result
```

[[ALG:Recursive chain length|O(n) calls; O(n) stack space]]
```pseudo
ALGORITHM Length(node)
  IF node = NULL THEN RETURN 0
  RETURN 1 + Length(node.next)
```

[[ALG:Recursive activity replay|O(n) calls; O(n) stack space]]
```pseudo
ALGORITHM Replay(node)
  IF node = NULL THEN RETURN
  Replay(node.next)
  VISIT node.data
```

## 6. Queues

[[ALG:Enqueue a ride request|O(1)]]
```pseudo
ALGORITHM Enqueue(Q, request)
  node ← new QueueNode(request)
  IF Q.rear = NULL THEN
    Q.front ← node; Q.rear ← node
  ELSE
    Q.rear.next ← node; Q.rear ← node
  Q.count ← Q.count + 1
```

[[ALG:Dequeue the oldest ride request|O(1)]]
```pseudo
ALGORITHM Dequeue(Q)
  IF Q.front = NULL THEN RETURN NULL
  target ← Q.front
  Q.front ← Q.front.next
  IF Q.front = NULL THEN Q.rear ← NULL
  Q.count ← Q.count - 1
  RETURN target.data
```

[[ALG:Bulk ride intake|O(n)]]
```pseudo
ALGORITHM BulkIntake(Q, requests)
  FOR each request R in requests DO
    Enqueue(Q, R)
  processed ← empty list
  WHILE Q.front ≠ NULL DO
    APPEND processed, Dequeue(Q)
  RETURN processed
```

## 7. Heaps and Priority Queues

[[ALG:Priority comparison|O(1)]]
```pseudo
ALGORITHM HigherPriority(a, b)
  IF a.eta ≠ b.eta THEN RETURN a.eta < b.eta
  IF a.distance ≠ b.distance THEN
    RETURN a.distance < b.distance
  RETURN a.driver_id < b.driver_id
```

[[ALG:Sift up after insertion|O(log n)]]
```pseudo
ALGORITHM SiftUp(H, i)
  current ← i
  WHILE current > 0 DO
    parent ← (current - 1) / 2
    IF HigherPriority(H[current], H[parent]) THEN
      swap H[current], H[parent]
      current ← parent
    ELSE BREAK
```

[[ALG:Sift down after extraction|O(log n)]]
```pseudo
ALGORITHM SiftDown(H, i)
  smallest ← i
  LOOP
    left ← 2 * smallest + 1
    right ← 2 * smallest + 2
    candidate ← smallest
    IF left < size AND HigherPriority(H[left], H[candidate]) THEN
      candidate ← left
    IF right < size AND HigherPriority(H[right], H[candidate]) THEN
      candidate ← right
    IF candidate = smallest THEN BREAK
    swap H[smallest], H[candidate]
    smallest ← candidate
```

[[ALG:Push a candidate|O(log n)]]
```pseudo
ALGORITHM Push(H, candidate)
  APPEND H, candidate
  SiftUp(H, size - 1)
```

[[ALG:Pop the best candidate|O(log n)]]
```pseudo
ALGORITHM Pop(H)
  IF size = 0 THEN RETURN NULL
  IF size = 1 THEN RETURN REMOVE_LAST(H)
  root ← H[0]
  H[0] ← REMOVE_LAST(H)
  SiftDown(H, 0)
  RETURN root
```

[[ALG:Heapify a candidate list|O(n)]]
```pseudo
ALGORITHM Heapify(H, items)
  H ← copy of items
  IF size ≤ 1 THEN RETURN
  start ← (size - 2) / 2
  FOR i ← start DOWN TO 0 DO
    SiftDown(H, i)
```

[[ALG:Update a candidate's priority|O(n) scan + O(log n) repair]]
```pseudo
ALGORITHM UpdatePriority(H, driver_id, eta, distance)
  FOR i ← 0 TO size - 1 DO
    IF H[i].driver_id = driver_id THEN
      H[i].eta ← eta; H[i].distance ← distance
      SiftUp(H, i); SiftDown(H, i)
      RETURN TRUE
  RETURN FALSE
```

## 8. Hashing and Geographic Algorithms

[[ALG:Hash a driver identifier|O(1)]]
```pseudo
ALGORITHM Hash(key, capacity)
  RETURN abs(key) mod capacity
```

[[ALG:Insert or update a key|avg O(1), worst O(n)]]
```pseudo
ALGORITHM Put(T, key, value)
  index ← Hash(key, T.capacity)
  current ← T.buckets[index]
  WHILE current ≠ NULL DO
    IF current.key = key THEN
      current.value ← value; RETURN
    current ← current.next
  T.buckets[index] ← new HashNode(key, value, T.buckets[index])
  T.count ← T.count + 1
```

[[ALG:Retrieve a key|avg O(1), worst O(n)]]
```pseudo
ALGORITHM Get(T, key)
  index ← Hash(key, T.capacity)
  current ← T.buckets[index]
  WHILE current ≠ NULL DO
    IF current.key = key THEN RETURN current.value
    current ← current.next
  RETURN NULL
```

[[ALG:Delete a key|avg O(1), worst O(n)]]
```pseudo
ALGORITHM Delete(T, key)
  index ← Hash(key, T.capacity)
  current ← T.buckets[index]; prev ← NULL
  WHILE current ≠ NULL DO
    IF current.key = key THEN
      IF prev = NULL THEN T.buckets[index] ← current.next
      ELSE prev.next ← current.next
      T.count ← T.count - 1
      RETURN TRUE
    prev ← current; current ← current.next
  RETURN FALSE
```

[[ALG:Haversine distance|O(1)]]
```pseudo
ALGORITHM Haversine(lat1, lon1, lat2, lon2)
  R ← 6371.0
  phi1 ← radians(lat1); phi2 ← radians(lat2)
  dphi ← radians(lat2 - lat1); dlambda ← radians(lon2 - lon1)
  a ← sin(dphi / 2)² + cos(phi1) * cos(phi2) * sin(dlambda / 2)²
  c ← 2 * atan2(sqrt(a), sqrt(1 - a))
  RETURN round(R * c, 2)
```

[[ALG:ETA estimation|O(1)]]
```pseudo
ALGORITHM ETA(distance, speed = 25.0)
  IF distance ≤ 0 THEN RETURN 2.0
  minutes ← (distance / speed) * 60
  RETURN round(max(2.0, minutes), 1)
```

[[ALG:Fare calculation|O(1)]]
```pseudo
ALGORITHM Fare(distance, vehicle)
  IF vehicle contains "bike" THEN base ← 50; rate ← 15
  ELSE IF vehicle contains "premium" or "good" THEN
    base ← 150; rate ← 22
  ELSE base ← 100; rate ← 18
  charge ← round(distance * rate, 2)
  RETURN base, rate, charge, base + charge
```

[[ALG:Build the candidate heap|O(n log n); O(n) with heapify]]
```pseudo
ALGORITHM BuildCandidates(L, pickup, excluded)
  H ← empty min-heap
  current ← L.head
  WHILE current ≠ NULL DO
    IF current.available AND current.id NOT IN excluded THEN
      d ← Haversine(current.lat, current.lon, pickup.lat, pickup.lon)
      candidate ← record of current with distance d, eta ETA(d)
      Push(H, candidate)
    current ← current.next
  RETURN H
```

[[ALG:Request a ride|O(n log n) dominated by candidate construction]]
```pseudo
ALGORITHM RequestRide(passenger, pickup, destination, vehicle)
  trip ← Haversine(pickup, destination)
  fare ← Fare(trip, vehicle)
  Enqueue(Q, request)
  ride_id ← INSERT ride with status PENDING
  Dequeue(Q)
  Push(S, RIDE_REQUESTED event)
  H ← BuildCandidates(L, pickup, ∅)
  H_registry[ride_id] ← H
  best ← Pop(H)
  IF best ≠ NULL THEN
    UPDATE ride SET driver = best.id, status = OFFERED
    Push(S, DRIVER_OFFERED event)
    RETURN OFFERED, best
  RETURN NO_DRIVERS_AVAILABLE
```

[[ALG:Rejection cascade|O(log n) per decline]]
```pseudo
ALGORITHM RejectRide(ride_id, driver_id)
  ride ← SELECT ride
  IF ride.status ≠ OFFERED OR ride.driver ≠ driver_id THEN
    ERROR "no open offer for this driver"
  Push(S, RIDE_REJECTED event)
  IF ride_id NOT IN H_registry THEN
    H_registry[ride_id] ← BuildCandidates(L, ride.pickup, {driver_id})
  H ← H_registry[ride_id]
  next ← Pop(H) IF H not empty ELSE NULL
  IF next ≠ NULL THEN
    UPDATE ride SET driver = next.id, status = OFFERED
    Push(S, DRIVER_REASSIGNED event)
    RETURN OFFERED, next
  UPDATE ride SET status = NO_DRIVERS_AVAILABLE
  Push(S, MATCHMAKING_EXHAUSTED event)
  RETURN NO_DRIVERS_AVAILABLE
```

## Flowchart: Driver Matchmaking

[[FIG:images/fig-3-5-matchmaking-flowchart.png|Figure 1: Candidate extraction and offer cascade, used for every ride request.]]

# CHAPTER 9: TIME AND SPACE COMPLEXITY ANALYSIS

## 9.1 Introduction

Time and space complexity analysis provides a quantitative framework for evaluating algorithm efficiency, predictable scaling under load, and performance trade-offs. Within the Pink Wheels system, operations range from linked list traversal and queue hand-off to heap-based priority selection and rejection cascading. This chapter presents asymptotic bound analyses (O-notation) across best, average, and worst-case scenarios for all custom Data Structures and Algorithms (DSA) implemented in the backend (backend/dsa/).

## 9.2 Section-by-Section Algorithmic Analysis

### 9.2.1 Linked Lists and Sorting Algorithms (dsa/linked_list.py)

**1. Linked List Operations (append, insert, delete, search, traverse)**

- Append (append):
  - Time Complexity:
    - Best Case: O(1) when the list is empty.
    - Average/Worst Case: O(n), because the chain is walked to its tail before the new node is linked.
  - Space Complexity: O(1) auxiliary space for the node.
- Insert at index (insert):
  - Time Complexity: O(n) to reach position k; O(1) when inserting at the head.
  - Space Complexity: O(1) auxiliary.
- Delete by identifier (delete):
  - Time Complexity: O(n) to locate the predecessor; O(1) when the head is the target.
  - Space Complexity: O(1).
- Search by identifier (search):
  - Time Complexity: O(n) in all cases with an unsorted chain.
  - Space Complexity: O(1) iterative traversal.
- Availability update (update_availability):
  - Time Complexity: O(n), dominated by the search that precedes the flag update.
  - Space Complexity: O(1).

**2. Searching Algorithms (linear_search, binary_search)**

- Linear Search:
  - Time Complexity: Best Case O(1) when the target is the first element; Average/Worst Case O(n).
  - Space Complexity: O(1).
- Binary Search:
  - Time Complexity: Best Case O(1) when the target is the middle element; Average/Worst Case O(log n).
  - Space Complexity: O(1) iterative implementation.
  - Application Note: Used to locate an ETA threshold inside a driver array that has already been sorted by estimated arrival time.

**3. Sorting Algorithms (bubble_sort, quick_sort)**

- Bubble Sort (Stable, In-Place):
  - Time Complexity: Best Case O(n) with the early-exit flag; Average/Worst Case O(n²).
  - Space Complexity: O(1).
- Quick Sort (Lomuto Partition, Unstable):
  - Time Complexity: Best/Average Case O(n log n); Worst Case O(n²) when the pivot is repeatedly minimal or maximal.
  - Space Complexity: O(log n) expected recursion depth.

The linked list is the correct choice for a registry whose dominant operation is insertion and full traversal during matchmaking; it is not the correct choice for keyed lookup, which is quantified below and addressed by the hash table.

### 9.2.2 Stack and Recursion (dsa/stack.py)

**1. Stack Operations (push, pop, peek, display)**

- Push (push):
  - Time Complexity: O(1) in all cases, because the node is linked at the top.
  - Space Complexity: O(1) per stored activity.
- Pop (pop):
  - Time Complexity: O(1) in all cases.
  - Space Complexity: O(1).
- Peek (peek):
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- Display (display):
  - Time Complexity: O(n) to produce the top-to-bottom sequence.
  - Space Complexity: O(n) for the returned list.

**2. Recursive Formulations (length, replay)**

- Recursive length:
  - Time Complexity: O(n), one call per node.
  - Space Complexity: O(n) call-stack frames.
- Recursive replay:
  - Time Complexity: O(n).
  - Space Complexity: O(n).

The recursive forms make the correspondence between the explicit LIFO stack and the implicit call stack explicit. The iterative display is preferred in the running system because it uses constant auxiliary space and cannot overflow.

### 9.2.3 Queue and Heap Algorithms (dsa/queue.py, dsa/priority_queue.py)

**1. FIFO Queue Operations (enqueue, dequeue, peek, display)**

- Enqueue:
  - Time Complexity: O(1) in all cases, because the rear pointer is updated directly.
  - Space Complexity: O(1) per request.
- Dequeue:
  - Time Complexity: O(1) in all cases, with the rear pointer reset when the last node leaves.
  - Space Complexity: O(1).
- Peek and Display:
  - Time Complexity: O(1) and O(n) respectively.
  - Space Complexity: O(1) and O(n).

**2. Bulk Intake**
  - Time Complexity: O(n) for n queued requests.
  - Space Complexity: O(n) for the drained sequence.

**3. Heap Operations (push, pop, heapify)**

- Push (sift up):
  - Time Complexity: O(log n), bounded by the height of the heap.
  - Space Complexity: O(1) with in-place swaps.
- Pop (sift down):
  - Time Complexity: O(log n).
  - Space Complexity: O(1) with in-place swaps.
- Heapify:
  - Time Complexity: O(n), because the total sift-down work over all internal nodes is linear.
  - Space Complexity: O(1) beyond the copied array.
- Update priority:
  - Time Complexity: O(n) to locate the driver, followed by O(log n) repair.
  - Space Complexity: O(1).

The heap is superior to a sorted array for repeated minimum extraction: inserting n candidates into a sorted array costs O(n²), while building a heap costs O(n) and each extraction costs O(log n).

### 9.2.4 Heap Maintenance and Reassignment (dsa/priority_queue.py, services/matchmaking.py)

**1. Candidate Construction (build_priority_queue_for_ride)**

- Time Complexity: O(n log n) for n archived drivers using repeated push; O(n) if the candidate list is collected first and heapified.
- Space Complexity: O(n) for the candidate heap.

**2. Priority Comparison (_is_higher_priority)**

- Time Complexity: O(1) with three constant-time comparisons.
- Space Complexity: O(1).

**3. Rejection Cascade (reject_ride)**

- Time Complexity: O(log n) per decline, because the next candidate is a single heap extraction from the live per-ride heap.
- Space Complexity: O(1) auxiliary per decline.
- Worst Case: O(n) declines occur before exhaustion, giving O(n log n) for a fully declined ride, which matches the cost of a single construction.

**4. Ride Lifecycle Transitions (accept, complete, cancel)**

- Time Complexity: O(n) for each transition, dominated by the linked list search for the driver record.
- Space Complexity: O(1).

The per-ride heap registry is the key design decision that keeps reassignment logarithmic. Without it, every rejection would rebuild the candidate set and the cascade would degrade to O(n² log n).

### 9.2.5 Hashing and Geographic Algorithms (dsa/hash_table.py, services/matchmaking.py)

**1. Hash Table Operations (hash, put, get, delete)**

- Hash:
  - Time Complexity: O(1).
  - Space Complexity: O(1).
- Put, Get, Delete:
  - Time Complexity: O(1) average under a uniform hash; O(n) worst case when every key collides into one bucket.
  - Space Complexity: O(1) auxiliary, O(n + c) total for n entries and c buckets.

**2. Haversine Distance**
  - Time Complexity: O(1), a fixed number of trigonometric evaluations.
  - Space Complexity: O(1).

**3. ETA and Fare Calculations**
  - Time Complexity: O(1) each.
  - Space Complexity: O(1).
  - Application Note: Both are invoked once per eligible candidate during heap construction and once per completed ride for the persisted fare.

## 9.3 Comparative Asymptotic Summary Table

Table 9.1 consolidates the bounds derived above. The final column records the concrete application of each structure in the running system.

**Table 9.1 — Comparative Asymptotic Summary**

| Category | Algorithm / Structure | Best Case (Time) | Average Case (Time) | Worst Case (Time) | Space Complexity | Real-World Application in System |
|---|---|---|---|---|---|---|
| Linked List | Append driver | O(1) | O(n) | O(n) | O(n) | Driver registration and seeding |
| Linked List | Search driver | O(1) | O(n) | O(n) | O(1) | Ride detail enrichment, accept validation |
| Linked List | Delete driver | O(1) | O(n) | O(n) | O(1) | Driver deregistration |
| Searching | Linear search | O(1) | O(n) | O(n) | O(1) | Basic candidate scan |
| Searching | Binary search | O(1) | O(log n) | O(log n) | O(1) | ETA threshold lookup in a sorted array |
| Sorting | Bubble sort | O(n) | O(n²) | O(n²) | O(1) | Candidate ordering demonstration |
| Sorting | Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) | Region ranking demonstration |
| Stack | Push | O(1) | O(1) | O(1) | O(n) | Activity event recording |
| Stack | Pop | O(1) | O(1) | O(1) | O(1) | Activity rollback and inspection |
| Stack | Recursive replay | O(n) | O(n) | O(n) | O(n) | Recursive traversal demonstration |
| Queue | Enqueue | O(1) | O(1) | O(1) | O(n) | Incoming ride request intake |
| Queue | Dequeue | O(1) | O(1) | O(1) | O(1) | Ride request hand-off to matchmaking |
| Heap | Push (sift up) | O(1) | O(log n) | O(log n) | O(n) | Candidate insertion during construction |
| Heap | Pop (sift down) | O(log n) | O(log n) | O(log n) | O(1) | Driver selection and rejection cascade |
| Heap | Heapify | O(n) | O(n) | O(n) | O(n) | Bulk candidate construction |
| Heap | Update priority | O(1) | O(n) | O(n) | O(1) | Driver movement simulation |
| Hashing | Put / Get / Delete | O(1) | O(1) | O(n) | O(n + c) | Constant-time driver lookup in the DSA Lab |
| Geographic | Haversine distance | O(1) | O(1) | O(1) | O(1) | Distance from each candidate to the pickup point |
| Geographic | ETA estimation | O(1) | O(1) | O(1) | O(1) | Priority key for heap ordering |
| Geographic | Fare calculation | O(1) | O(1) | O(1) | O(1) | Passenger quotation and ride pricing |

Table 9.2 records the empirical behaviour measured on the demonstration dataset of thirteen drivers at the default pickup point.

**Table 9.2 — Empirical Matchmaking Behaviour (13 drivers, 11 eligible)**

| Operation | Theoretical Bound | Observed Work | Observed Result |
|---|---|---|---|
| Linked list scan | O(n) | 13 node visits | 11 eligible candidates retained |
| Distance and ETA per candidate | O(1) each | 11 Haversine evaluations | Root ETA 2.0 min |
| Heap construction | O(n log n) | 11 pushes, at most 4 sift steps each | Heap size 11 |
| Top candidate selection | O(log n) | 1 pop, 4 comparisons | Hina Tariq (0.00 km, 2.0 min) |
| Next candidate after rejection | O(log n) | 1 pop | Kinza Shah (3.88 km, 9.3 min) |
| Heap state after 9 declines | O(n log n) cumulative | 9 pops | Queue exhausted, ride unfulfilled |

# CHAPTER 10: ALGORITHM DEMONSTRATION AND TEST CASES

## 10.1 Introduction

To validate algorithm correctness and verify theoretical asymptotic bounds under practical application scenarios, Pink Wheels provides an automated test suite (backend/tests/, 48 collected test cases) and explicit verification endpoints exposed through the DSA dashboard (GET /api/dsa/*) and the matchmaking simulation (POST /api/dsa/matchmaking).

This chapter presents verified demonstration logs and test cases across all 5 algorithm categories, together with captured interface states from the running application.

The demonstration dataset is the seeded driver pool of thirteen verified women drivers. Eleven are available at startup; drivers 104 and 110 are marked busy and are excluded from candidate construction. The default pickup point is Saddar Empress Market (24.8615, 67.0099), which coincides with driver 102.

## 10.2 Category 1: Linked List, Searching, and Sorting Demonstration

### 10.2.1 Linked List Chain Operations

- Input Dataset: driver chain of 13 nodes, head = 101 Sobia Parveen.
- Operations Executed:
  1. append(driver 114) ⟹ Result: chain length 14, new node linked after 113.
  2. search(107) ⟹ Result: node found at position 7.
  3. delete(114) ⟹ Result: TRUE, chain length restored to 13.
  4. update_availability(101, false) ⟹ Result: node 101 marked Busy; candidate count falls to 10.

The DSA dashboard renders the same chain in the browser, as shown in Figure 10.1.

[[FIG:images/fig01-dsa-linked-list-overview.png|Figure 10.1 — Driver linked list overview on the DSA dashboard]]

The management view in Figure 10.2 exposes node-level operations on the live chain.

[[FIG:images/fig06-linked-list-management.png|Figure 10.2 — Linked list node management and availability controls]]

### 10.2.2 Comparative Sorting Verification: Bubble Sort vs. Quick Sort

Test dataset evaluated for array size n = 8 of candidate ETAs:

- Case A: Already Sorted Input ([2.0, 2.7, 9.3, 12.3, 13.0, 13.6, 15.6, 18.5])
  - Bubble Sort: Comparisons = 7, Swaps = 0. Early exit triggered in 1 pass (O(n)).
  - Quick Sort: Comparisons = 28, Swaps = 0. Fixed last-element pivot produces unbalanced partitions.
- Case B: Reverse Ordered Input ([18.5, 15.6, 13.6, 13.0, 12.3, 9.3, 2.7, 2.0])
  - Bubble Sort: Comparisons = 28, Swaps = 28 (n(n−1)/2).
  - Quick Sort: Comparisons = 28, Swaps = 28.

The comparison confirms the early-exit advantage of Bubble Sort on nearly sorted data and the partition cost of Quick Sort when the pivot is extremal.

## 10.3 Category 2: Stack and Recursion Demonstration

### 10.3.1 Activity Stack Push and Pop

- Initial Stack: [SYSTEM_STARTUP].
- Operations Executed:
  1. push(RIDE_REQUESTED) ⟹ Top: RIDE_REQUESTED, size 2.
  2. push(DRIVER_OFFERED) ⟹ Top: DRIVER_OFFERED, size 3.
  3. push(RIDE_ACCEPTED) ⟹ Top: RIDE_ACCEPTED, size 4.
  4. pop() ⟹ Returned RIDE_ACCEPTED, top becomes DRIVER_OFFERED, size 3.
  5. peek() ⟹ Returned DRIVER_OFFERED without removal.
- Display Order: DRIVER_OFFERED, RIDE_REQUESTED, SYSTEM_STARTUP (most recent first).

The stack view in Figure 10.3 shows the same events in the browser.

[[FIG:images/fig09-activity-stack.png|Figure 10.3 — LIFO activity stack with timestamped ride events]]

### 10.3.2 Recursive Traversal Trace

Recursion on the same chain is traced for the first four nodes:

- Length(node101) = 1 + Length(node102)
- Length(node102) = 1 + Length(node103)
- Length(node103) = 1 + Length(node104)
- Length(node104) = 1 + Length(NULL) = 1
- Unwinding returns 4 at the first node.

The trace shows 4 frames pushed and 4 frames popped, mirroring the explicit LIFO stack behaviour in the previous test.

## 10.4 Category 3: Queue & Priority Queue Demonstration

### 10.4.1 FIFO Queue and Heap Priority Operations

- Enqueue Sequence: R1 (passenger 1), R2 (passenger 2), R3 (passenger 3).
- Dequeue Sequence: R1, R2, R3 — strict arrival order preserved.
- Heap Push Sequence: candidates 113 (9.3), 105 (13.0), 102 (2.0), 107 (15.6).
  - Root after each push: 113 → 105 → 102 → 102.
- Heap Pop Sequence: 102, 105, 113, 107 — ascending ETA order restored.

Figure 10.4 shows the FIFO queue and Figure 10.5 shows the heap operations in the DSA dashboard.

[[FIG:images/fig07-priority-queue.png|Figure 10.4 — FIFO ride request queue and priority queue inspection]]

[[FIG:images/fig08-heap-ranking.png|Figure 10.5 — Min-heap array and sorted priority order]]

### 10.4.2 Heap Ranking and Candidate Ordering

The ranked order returned by GET /api/dsa/priority-queue for the default pickup point follows Table 10.1.

**Table 10.1 — Ranked Candidates at Saddar Empress Market**

| Rank | Driver | Distance (km) | ETA (min) | Eligible |
|---|---|---|---|---|
| 1 | Hina Tariq (102) | 0.00 | 2.0 | Yes |
| 2 | Kinza Shah (113) | 3.88 | 9.3 | Yes |
| 3 | Areeba Jamil (106) | 5.13 | 12.3 | Yes |
| 4 | Nida Rehman (105) | 5.42 | 13.0 | Yes |
| 5 | Sobia Parveen (101) | 5.68 | 13.6 | Yes |
| 6 | Khadija Farooq (107) | 6.48 | 15.6 | Yes |
| 7 | Rabia Mumtaz (111) | 7.69 | 18.5 | Yes |
| 8 | Faiza Anwar (108) | 8.28 | 19.9 | Yes |
| 9 | Mariam Siddiqui (103) | 10.81 | 25.9 | Yes |
| 10 | Bushra Rasheed (109) | 10.99 | 26.4 | Yes |
| 11 | Sidra Batool (112) | 11.37 | 27.3 | Yes |
| — | Zubeda Bibi (110) | 1.14 | 2.7 | No (busy) |
| — | Samina Sheikh (104) | 6.86 | 16.5 | No (busy) |

The two ineligible drivers are excluded before insertion, which is why they do not appear in the ranked list even though their coordinates are closer than several eligible candidates.

## 10.5 Category 4: Heap Extraction and Rejection Cascade Demonstration

### 10.5.1 Rejection Cascade Trace

Starting from the heap in Table 10.1, successive declines are traced below.

- Offer 1: Hina Tariq (2.0 min) — rejected. Next extraction: Kinza Shah (9.3 min).
- Offer 2: Kinza Shah (9.3 min) — rejected. Next extraction: Areeba Jamil (12.3 min).
- Offer 3: Areeba Jamil (12.3 min) — rejected. Next extraction: Nida Rehman (13.0 min).
- Offer 4: Nida Rehman (13.0 min) — rejected. Next extraction: Sobia Parveen (13.6 min).
- Offer 5: Sobia Parveen (13.6 min) — accepted. Ride status ACCEPTED; driver 101 marked busy.

A second scenario exhausts the heap:

- Offers 1–11 rejected in rank order.
- Pop from an empty heap returns NULL.
- Ride status becomes NO_DRIVERS_AVAILABLE.
- Activity stack records MATCHMAKING_EXHAUSTED.

Figure 10.6 shows the matchmaking flow and the cascade recorded by the running system.

[[FIG:images/fig10-matchmaking-flow.png|Figure 10.6 — Matchmaking step trace and rejection cascade]]

## 10.6 Category 5: Geographic Matchmaking and Route Analysis Demonstration

### 10.6.1 Passenger Booking and Fare Estimate

A booking from Saddar to Clifton Block 2 is computed as follows:

- Haversine trip distance: 8.01 km.
- Bike fare: 50 + 15 × 8.01 = PKR 170.15.
- Car fare: 100 + 18 × 8.01 = PKR 244.18.
- Premium fare: 150 + 22 × 8.01 = PKR 326.22.

Figures 10.7 and 10.8 show the booking form and the fare detail panel in the running application.

[[FIG:images/fig02-passenger-booking.png|Figure 10.7 — Passenger booking form with map-based pickup and destination selection]]

[[FIG:images/fig03-passenger-fare-detail.png|Figure 10.8 — Fare estimate, distance, and driver offer detail]]

### 10.6.2 Driver Dashboard and Availability

The driver dashboard displays the offered rides together with the passenger, route, distance, and fare.

Accepting a ride marks the driver busy in the linked list; completing it restores availability.

Figure 10.9 shows the driver dashboard during an active offer.

[[FIG:images/fig04-driver-dashboard.png|Figure 10.9 — Driver dashboard with the active ride offer]]

### 10.6.3 DSA Dashboard Overview

The DSA dashboard consolidates all four structures into one administrative view and exposes the matchmaking simulation.

Figure 10.10 shows the consolidated view.

[[FIG:images/fig05-dsa-dashboard.png|Figure 10.10 — Consolidated DSA dashboard with structure summaries]]

### 10.6.4 Correctness Verification Summary

The automated suite verifies the following properties:

- The linked list preserves insertion order and reports the correct size after append, insert, and delete.
- Availability updates are reflected by candidate filtering.
- The heap returns candidates in non-decreasing ETA order under repeated extraction.
- The tie-breakers order equal-ETA candidates by distance and then by identifier.
- The FIFO queue returns requests in arrival order.
- The activity stack returns the most recent event first.
- The ride lifecycle rejects invalid transitions with HTTP 409.
- Fare rules produce the documented amounts for each vehicle type.
- The full workflow test drives a ride from request to completion.

# CHAPTER 11: PROJECT IMPLEMENTATION AND FEATURES

## 11.1 System Architecture Overview

The implemented system runs as two processes.

The backend is a FastAPI application served by Uvicorn on port 8000. It initializes the database, seeds the driver linked list from the sample driver module, creates the ride queue and activity stack, and registers the route modules.

The frontend is a Vite development server on port 5173. It proxies API calls to the backend and renders the five application routes.

The data structures live in the backend process memory and are rebuilt from the seeded driver file on every restart. Durable ride facts are stored in SQLite, so ride history survives restarts while availability resets to the seeded state.

The implementation is organized as follows:

- backend/main.py — application factory, CORS, router registration, health endpoint.
- backend/database.py — connection management, placeholder adaptation, schema initialization, passenger seeding.
- backend/routes/ — drivers, passengers, rides, and DSA endpoints.
- backend/services/matchmaking.py — global structures, geographic utilities, and the ride lifecycle.
- backend/dsa/ — linked_list.py, queue.py, priority_queue.py, stack.py, hash_table.py, sample_drivers.py.
- backend/tests/ — 48 collected test cases.
- frontend/src/pages/ — passenger home, ride status, history, driver dashboard, DSA dashboard.
- frontend/src/components/ — navbar, ride map.
- frontend/src/services/api.js — shared HTTP client.

## 11.2 Core Application Modules

Table 11.1 lists the implemented modules and their responsibilities.

**Table 11.1 — Implemented Application Modules**

| Module | Location | Responsibility |
|---|---|---|
| Application entry | backend/main.py | Initialize database, register routes, expose health probe |
| Database helper | backend/database.py | PostgreSQL/SQLite connection, query and commit helpers, schema, seeding |
| Driver linked list | backend/dsa/linked_list.py | Driver registration, search, deletion, availability |
| Ride FIFO queue | backend/dsa/queue.py | Arrival-order ride request intake |
| Driver priority queue | backend/dsa/priority_queue.py | Min-heap ranking by ETA, distance, identifier |
| Activity stack | backend/dsa/stack.py | LIFO ride event history |
| Driver hash table | backend/dsa/hash_table.py | Chained constant-time lookup demonstration |
| Sample drivers | backend/dsa/sample_drivers.py | Thirteen verified women driver records |
| Matchmaking service | backend/services/matchmaking.py | Candidate construction, lifecycle transitions, geographic and fare utilities |
| Driver routes | backend/routes/drivers.py | Registration, search, deletion, availability |
| Passenger routes | backend/routes/passengers.py | Passenger listing and creation |
| Ride routes | backend/routes/rides.py | Fare estimate, request, listing, accept, reject, complete, cancel |
| DSA routes | backend/routes/dsa.py | Structure inspection and matchmaking simulation |
| Passenger home | frontend/src/pages/passenger/Home.vue | Map selection, fare estimate, booking |
| Ride status | frontend/src/pages/passenger/RideStatus.vue | Live ride state and driver details |
| Ride history | frontend/src/pages/passenger/RideHistory.vue | Previous rides and outcomes |
| Driver dashboard | frontend/src/pages/driver/DriverDashboard.vue | Offer display and ride actions |
| DSA dashboard | frontend/src/pages/admin/DsaDashboard.vue | Structure visualization and simulation |
| Ride map | frontend/src/components/common/RideMap.vue | Leaflet map with pickup and destination markers |
| API service | frontend/src/services/api.js | Centralized HTTP access |

The implementation deliberately keeps the route handlers thin and the data structures framework-independent. This separation allows the linked list, queue, heap, and stack to be tested without starting the web server, which is exactly how the backend test suite exercises them.

The most intricate module is the matchmaking service. It owns four global structures and a registry of per-ride heaps. The registry is what enables a rejection to resume from the exact candidate state of the original request, rather than recomputing distances that have not changed.

The ride lifecycle module also enforces the state machine. PENDING is the initial state; OFFERED is entered after a successful heap extraction; ACCEPTED requires the acting driver to hold the offer; COMPLETED and CANCELLED are terminal; NO_DRIVERS_AVAILABLE is entered when the heap empties. Illegal transitions raise a state error, which the route layer maps to HTTP 409.

The persistence module follows the same principle. It exposes only execute_query and execute_commit, adapts placeholders for the active engine, and appends a RETURNING clause for PostgreSQL inserts so that the ride identifier is available for the heap registry.
# DEMONSTRATION

This section presents the pseudocode of the algorithms used in Pink Wheels. Each pseudocode is written from the corresponding routine in the backend source code (the backend/dsa/ package and the application modules that use it), and the algorithms are grouped into the same categories used throughout this report. The arrow ← denotes assignment and text after // is a comment.

## 1. Linked Lists, Searching and Sorting

[[PSEUDO:Pseudocode 1: Linked List Append|backend/dsa/linked_list.py – append()]]
```pseudo
ALGORITHM AppendDriver(L, driver)
  N ← new DriverNode(driver)
  IF L.head = NULL THEN
    L.head ← N                       // first node becomes the head
  ELSE
    current ← L.head
    WHILE current.next ≠ NULL DO     // walk to the tail
      current ← current.next
    END WHILE
    current.next ← N                 // link the new node after the tail
  END IF
  L.count ← L.count + 1
  RETURN N
```

[[PSEUDO:Pseudocode 2: Linked List Insert|backend/dsa/linked_list.py – insert()]]
```pseudo
ALGORITHM InsertAt(L, index, driver)
  IF index < 0 OR index > L.count THEN
    ERROR "index out of bounds"
  END IF
  N ← new DriverNode(driver)
  IF index = 0 THEN
    N.next ← L.head                  // new head
    L.head ← N
  ELSE
    current ← L.head
    FOR step ← 0 TO index - 2 DO
      current ← current.next
    END FOR
    N.next ← current.next            // splice after predecessor
    current.next ← N
  END IF
  L.count ← L.count + 1
  RETURN N
```

[[PSEUDO:Pseudocode 3: Linked List Delete|backend/dsa/linked_list.py – delete()]]
```pseudo
ALGORITHM DeleteDriver(L, driver_id)
  IF L.head = NULL THEN RETURN FALSE
  IF L.head.driver_id = driver_id THEN
    L.head ← L.head.next             // target is the head
    L.count ← L.count - 1
    RETURN TRUE
  END IF
  current ← L.head
  WHILE current.next ≠ NULL DO
    IF current.next.driver_id = driver_id THEN
      current.next ← current.next.next
      L.count ← L.count - 1
      RETURN TRUE
    END IF
    current ← current.next
  END WHILE
  RETURN FALSE                       // not found
```

[[PSEUDO:Pseudocode 4: Linked List Search|backend/dsa/linked_list.py – search()]]
```pseudo
ALGORITHM SearchDriver(L, driver_id)
  current ← L.head
  WHILE current ≠ NULL DO
    IF current.driver_id = driver_id THEN
      RETURN current                 // node found
    END IF
    current ← current.next
  END WHILE
  RETURN NULL                        // not registered
```

[[PSEUDO:Pseudocode 5: Linked List Traverse|backend/dsa/linked_list.py – traverse()]]
```pseudo
ALGORITHM Traverse(L)
  result ← empty list
  current ← L.head
  WHILE current ≠ NULL DO
    APPEND result, current as record
    current ← current.next
  END WHILE
  RETURN result
```

[[PSEUDO:Pseudocode 6: Availability Update|backend/dsa/linked_list.py – update_availability()]]
```pseudo
ALGORITHM UpdateAvailability(L, driver_id, flag)
  node ← SearchDriver(L, driver_id)
  IF node = NULL THEN
    RETURN FALSE
  END IF
  node.available ← flag              // Busy after accept, Available after complete
  RETURN TRUE
```

[[PSEUDO:Pseudocode 7: Linear Search|backend/dsa/linked_list.py – available filtering]]
```pseudo
ALGORITHM LinearSearch(A, target, field)
  FOR i ← 0 TO length(A) - 1 DO
    IF field(A[i]) = target THEN
      RETURN i
    END IF
  END FOR
  RETURN -1                          // not found
```

[[PSEUDO:Pseudocode 8: Binary Search|backend/dsa (design-level utility)]]
```pseudo
ALGORITHM BinarySearch(A, target, field)
  low ← 0
  high ← length(A) - 1
  WHILE low ≤ high DO
    mid ← floor((low + high) / 2)
    value ← field(A[mid])
    IF value = target THEN
      RETURN mid
    ELSE IF value < target THEN
      low ← mid + 1
    ELSE
      high ← mid - 1
    END IF
  END WHILE
  RETURN -1                          // not found
```

[[PSEUDO:Pseudocode 9: Bubble Sort|backend/dsa (design-level utility)]]
```pseudo
ALGORITHM BubbleSort(A, field)
  FOR end ← length(A) - 1 DOWN TO 1 DO
    swapped ← FALSE
    FOR j ← 0 TO end - 1 DO
      IF field(A[j]) > field(A[j + 1]) THEN
        swap A[j], A[j + 1]
        swapped ← TRUE
      END IF
    END FOR
    IF swapped = FALSE THEN
      STOP                           // early exit on sorted input
    END IF
  END FOR
  RETURN A
```

[[PSEUDO:Pseudocode 10: Quick Sort and Partition|backend/dsa (design-level utility)]]
```pseudo
ALGORITHM QuickSort(A, low, high, field)
  IF low < high THEN
    p ← Partition(A, low, high, field)
    QuickSort(A, low, p - 1, field)
    QuickSort(A, p + 1, high, field)
  END IF

ALGORITHM Partition(A, low, high, field)
  pivot ← field(A[high])             // Lomuto scheme, last element
  i ← low - 1
  FOR j ← low TO high - 1 DO
    IF field(A[j]) ≤ pivot THEN
      i ← i + 1
      swap A[i], A[j]
    END IF
  END FOR
  swap A[i + 1], A[high]
  RETURN i + 1
```

## 2. Stacks and Recursion

[[PSEUDO:Pseudocode 11: Stack Push|backend/dsa/stack.py – push()]]
```pseudo
ALGORITHM Push(S, activity)
  IF activity.timestamp is missing THEN
    activity.timestamp ← current date and time
  END IF
  node ← new StackNode(activity, next = S.top)
  S.top ← node                       // newest node becomes the top
  S.count ← S.count + 1
```

[[PSEUDO:Pseudocode 12: Stack Pop|backend/dsa/stack.py – pop()]]
```pseudo
ALGORITHM Pop(S)
  IF S.top = NULL THEN
    RETURN NULL                      // empty stack
  END IF
  target ← S.top
  S.top ← S.top.next
  S.count ← S.count - 1
  RETURN target.data
```

[[PSEUDO:Pseudocode 13: Stack Peek and Display|backend/dsa/stack.py – peek(), display()]]
```pseudo
ALGORITHM Peek(S)
  IF S.top = NULL THEN RETURN NULL
  RETURN S.top.data

ALGORITHM Display(S)
  result ← empty list
  current ← S.top
  WHILE current ≠ NULL DO
    APPEND result, current.data      // most recent first
    current ← current.next
  END WHILE
  RETURN result
```

[[PSEUDO:Pseudocode 14: Recursive Chain Length|recursive formulation of traversal]]
```pseudo
ALGORITHM Length(node)
  IF node = NULL THEN
    RETURN 0                         // base case
  END IF
  RETURN 1 + Length(node.next)       // recursive case
```

[[PSEUDO:Pseudocode 15: Recursive Activity Replay|recursive formulation of stack display]]
```pseudo
ALGORITHM Replay(node)
  IF node = NULL THEN RETURN         // base case
  Replay(node.next)                  // descend to the oldest event
  VISIT node.data                    // oldest first on unwinding
```

## 3. Queues

[[PSEUDO:Pseudocode 16: Queue Enqueue|backend/dsa/queue.py – enqueue()]]
```pseudo
ALGORITHM Enqueue(Q, request)
  node ← new QueueNode(request)
  IF Q.rear = NULL THEN
    Q.front ← node                   // queue was empty
    Q.rear ← node
  ELSE
    Q.rear.next ← node
    Q.rear ← node
  END IF
  Q.count ← Q.count + 1
```

[[PSEUDO:Pseudocode 17: Queue Dequeue|backend/dsa/queue.py – dequeue()]]
```pseudo
ALGORITHM Dequeue(Q)
  IF Q.front = NULL THEN
    RETURN NULL                      // empty queue
  END IF
  target ← Q.front
  Q.front ← Q.front.next
  IF Q.front = NULL THEN
    Q.rear ← NULL                    // last element removed
  END IF
  Q.count ← Q.count - 1
  RETURN target.data
```

[[PSEUDO:Pseudocode 18: Bulk Ride Intake|backend/dsa/queue.py – drain loop]]
```pseudo
ALGORITHM BulkIntake(Q, requests)
  FOR each request R in requests DO
    Enqueue(Q, R)                    // requests arrive during peak hours
  END FOR
  processed ← empty list
  WHILE Q.front ≠ NULL DO
    request ← Dequeue(Q)             // strict arrival order
    APPEND processed, request
  END WHILE
  RETURN processed
```

## 4. Heaps and Priority Queues

[[PSEUDO:Pseudocode 19: Priority Comparison|backend/dsa/priority_queue.py – _is_higher_priority()]]
```pseudo
ALGORITHM HigherPriority(a, b)
  IF a.eta ≠ b.eta THEN
    RETURN a.eta < b.eta             // primary key: ETA in minutes
  END IF
  IF a.distance ≠ b.distance THEN
    RETURN a.distance < b.distance   // secondary key: distance in km
  END IF
  RETURN a.driver_id < b.driver_id   // tertiary key: deterministic order
```

[[PSEUDO:Pseudocode 20: Heap Sift Up|backend/dsa/priority_queue.py – _sift_up()]]
```pseudo
ALGORITHM SiftUp(H, index)
  current ← index
  WHILE current > 0 DO
    parent ← (current - 1) / 2
    IF HigherPriority(H[current], H[parent]) THEN
      swap H[current], H[parent]
      current ← parent
    ELSE
      BREAK                          // heap property restored
    END IF
  END WHILE
```

[[PSEUDO:Pseudocode 21: Heap Sift Down|backend/dsa/priority_queue.py – _sift_down()]]
```pseudo
ALGORITHM SiftDown(H, index)
  smallest ← index
  LOOP
    left ← 2 * smallest + 1
    right ← 2 * smallest + 2
    candidate ← smallest
    IF left < size AND HigherPriority(H[left], H[candidate]) THEN
      candidate ← left
    END IF
    IF right < size AND HigherPriority(H[right], H[candidate]) THEN
      candidate ← right
    END IF
    IF candidate = smallest THEN
      BREAK                          // no child outranks the parent
    END IF
    swap H[smallest], H[candidate]
    smallest ← candidate
  END LOOP
```

[[PSEUDO:Pseudocode 22: Heapify|backend/dsa/priority_queue.py – heapify()]]
```pseudo
ALGORITHM Heapify(H, items)
  H ← copy of items
  IF size(H) ≤ 1 THEN RETURN
  start ← (size(H) - 2) / 2          // last internal node
  FOR i ← start DOWN TO 0 DO
    SiftDown(H, i)                   // total work is O(n)
  END FOR
```

[[PSEUDO:Pseudocode 23: Heap Pop|backend/dsa/priority_queue.py – pop()]]
```pseudo
ALGORITHM Pop(H)
  IF size(H) = 0 THEN RETURN NULL
  IF size(H) = 1 THEN
    RETURN RemoveLast(H)
  END IF
  root ← H[0]                        // lowest ETA candidate
  H[0] ← RemoveLast(H)               // move last leaf to the root
  SiftDown(H, 0)
  RETURN root
```

## 5. Hash Tables

[[PSEUDO:Pseudocode 24: Hash Function|backend/dsa/hash_table.py – _hash()]]
```pseudo
ALGORITHM Hash(key, capacity)
  RETURN abs(key) mod capacity       // index into the bucket array
```

[[PSEUDO:Pseudocode 25: Hash Put|backend/dsa/hash_table.py – put()]]
```pseudo
ALGORITHM Put(T, key, value)
  index ← Hash(key, T.capacity)
  current ← T.buckets[index]
  WHILE current ≠ NULL DO
    IF current.key = key THEN
      current.value ← value          // update in place
      RETURN
    END IF
    current ← current.next
  END WHILE
  T.buckets[index] ← new HashNode(key, value, T.buckets[index])
  T.count ← T.count + 1
```

[[PSEUDO:Pseudocode 26: Hash Get|backend/dsa/hash_table.py – get()]]
```pseudo
ALGORITHM Get(T, key)
  index ← Hash(key, T.capacity)
  current ← T.buckets[index]
  WHILE current ≠ NULL DO
    IF current.key = key THEN
      RETURN current.value
    END IF
    current ← current.next           // collision chain walk
  END WHILE
  RETURN NULL
```

[[PSEUDO:Pseudocode 27: Hash Delete|backend/dsa/hash_table.py – delete()]]
```pseudo
ALGORITHM Delete(T, key)
  index ← Hash(key, T.capacity)
  current ← T.buckets[index]
  prev ← NULL
  WHILE current ≠ NULL DO
    IF current.key = key THEN
      IF prev = NULL THEN
        T.buckets[index] ← current.next
      ELSE
        prev.next ← current.next
      END IF
      T.count ← T.count - 1
      RETURN TRUE
    END IF
    prev ← current
    current ← current.next
  END WHILE
  RETURN FALSE
```

## 6. Geographic and Matchmaking Algorithms

[[PSEUDO:Pseudocode 28: Haversine Distance|backend/services/matchmaking.py – haversine_distance()]]
```pseudo
ALGORITHM Haversine(lat1, lon1, lat2, lon2)
  R ← 6371.0                         // Earth radius in kilometres
  phi1 ← radians(lat1)
  phi2 ← radians(lat2)
  dphi ← radians(lat2 - lat1)
  dlambda ← radians(lon2 - lon1)
  a ← sin(dphi / 2)² + cos(phi1) * cos(phi2) * sin(dlambda / 2)²
  c ← 2 * atan2(sqrt(a), sqrt(1 - a))
  RETURN round(R * c, 2)
```

[[PSEUDO:Pseudocode 29: ETA Estimation|backend/services/matchmaking.py – calculate_eta()]]
```pseudo
ALGORITHM ETA(distance, speed ← 25.0)
  IF distance ≤ 0 THEN
    RETURN 2.0                       // minimum ETA in minutes
  END IF
  minutes ← (distance / speed) * 60
  RETURN round(max(2.0, minutes), 1)
```

[[PSEUDO:Pseudocode 30: Fare Calculation|backend/services/matchmaking.py – calculate_fare()]]
```pseudo
ALGORITHM Fare(distance, vehicle)
  IF vehicle contains "bike" THEN
    base ← 50; rate ← 15
  ELSE IF vehicle contains "premium" OR "good" THEN
    base ← 150; rate ← 22
  ELSE
    base ← 100; rate ← 18
  END IF
  charge ← round(distance * rate, 2)
  RETURN base, rate, charge, base + charge
```

[[PSEUDO:Pseudocode 31: Build Candidate Heap|backend/services/matchmaking.py – build_priority_queue_for_ride()]]
```pseudo
ALGORITHM BuildCandidates(L, pickup, excluded)
  H ← new DriverPriorityQueue
  current ← L.head
  WHILE current ≠ NULL DO
    IF current.available AND current.id NOT IN excluded THEN
      d ← Haversine(current.lat, current.lon, pickup.lat, pickup.lon)
      candidate ← {id, name, phone, vehicle, lat, lon, d, ETA(d)}
      Push(H, candidate)             // O(log n) per eligible driver
    END IF
    current ← current.next
  END WHILE
  RETURN H
```

[[PSEUDO:Pseudocode 32: Request Ride|backend/services/matchmaking.py – request_ride()]]
```pseudo
ALGORITHM RequestRide(passenger, pickup, destination, vehicle)
  trip ← Haversine(pickup, destination)
  fare ← Fare(trip, vehicle)
  request ← {passenger, pickup, destination, trip, fare.total, vehicle}
  Enqueue(Q, request)                // FIFO intake
  ride_id ← INSERT ride(status ← PENDING)
  Dequeue(Q)                         // now under active processing
  Push(S, {event ← RIDE_REQUESTED})
  H ← BuildCandidates(L, pickup, ∅)
  H_registry[ride_id] ← H
  best ← Pop(H)
  IF best ≠ NULL THEN
    UPDATE ride SET driver ← best.id, status ← OFFERED
    Push(S, {event ← DRIVER_OFFERED})
    RETURN OFFERED, best
  END IF
  RETURN NO_DRIVERS_AVAILABLE
```

[[PSEUDO:Pseudocode 33: Accept Ride|backend/services/matchmaking.py – accept_ride()]]
```pseudo
ALGORITHM AcceptRide(ride_id, driver_id)
  ride ← SELECT ride
  IF ride.status IN {COMPLETED, CANCELLED, NO_DRIVERS_AVAILABLE} THEN
    ERROR "ride can no longer be accepted"
  END IF
  IF ride.status = ACCEPTED THEN
    ERROR "ride already accepted"
  END IF
  node ← SearchDriver(L, driver_id)
  IF node = NULL OR ride.driver ≠ driver_id THEN
    ERROR "offer does not belong to this driver"
  END IF
  UpdateAvailability(L, driver_id, FALSE)
  UPDATE ride SET status ← ACCEPTED, driver ← driver_id
  Push(S, {event ← RIDE_ACCEPTED})
  REMOVE H_registry[ride_id]         // remaining candidates no longer needed
  RETURN ACCEPTED
```

[[PSEUDO:Pseudocode 34: Reject Ride and Cascade|backend/services/matchmaking.py – reject_ride()]]
```pseudo
ALGORITHM RejectRide(ride_id, driver_id)
  ride ← SELECT ride
  IF ride.status ≠ OFFERED OR ride.driver ≠ driver_id THEN
    ERROR "no open offer for this driver"
  END IF
  Push(S, {event ← RIDE_REJECTED})
  IF ride_id NOT IN H_registry THEN
    H_registry[ride_id] ← BuildCandidates(L, ride.pickup, {driver_id})
  END IF
  H ← H_registry[ride_id]
  IF H is not empty THEN
    next ← Pop(H)                    // O(log n) reassignment
  ELSE
    next ← NULL
  END IF
  IF next ≠ NULL THEN
    UPDATE ride SET driver ← next.id, status ← OFFERED
    Push(S, {event ← DRIVER_REASSIGNED})
    RETURN OFFERED, next
  END IF
  UPDATE ride SET status ← NO_DRIVERS_AVAILABLE
  Push(S, {event ← MATCHMAKING_EXHAUSTED})
  RETURN NO_DRIVERS_AVAILABLE
```

[[PSEUDO:Pseudocode 35: Complete Ride|backend/services/matchmaking.py – complete_ride()]]
```pseudo
ALGORITHM CompleteRide(ride_id)
  ride ← SELECT ride
  IF ride.status = COMPLETED THEN
    RETURN COMPLETED                 // idempotent completion
  END IF
  IF ride.status ≠ ACCEPTED THEN
    ERROR "ride is not in an accepted state"
  END IF
  IF ride.driver ≠ NULL THEN
    UpdateAvailability(L, ride.driver, TRUE)
  END IF
  UPDATE ride SET status ← COMPLETED
  Push(S, {event ← RIDE_COMPLETED})
  REMOVE H_registry[ride_id]
  RETURN COMPLETED
```

[[PSEUDO:Pseudocode 36: Cancel Ride|backend/services/matchmaking.py – cancel_ride()]]
```pseudo
ALGORITHM CancelRide(ride_id)
  ride ← SELECT ride
  IF ride.status IN {CANCELLED, COMPLETED} THEN
    RETURN ride.status                // nothing to cancel
  END IF
  IF ride.driver ≠ NULL AND ride.status = ACCEPTED THEN
    UpdateAvailability(L, ride.driver, TRUE)
  END IF
  UPDATE ride SET status ← CANCELLED
  Push(S, {event ← RIDE_CANCELLED})
  REMOVE H_registry[ride_id]
  RETURN CANCELLED
```
# CHAPTER 12: CONCLUSION AND FUTURE SCOPE

## 12.1 Conclusion

Pink Wheels was developed as a women-focused ride-hailing platform in which the driver matching process is built from explicit data structures rather than library primitives.

The project implemented a singly linked list for driver registration and availability, a FIFO queue for ride request intake, a binary min-heap priority queue for candidate ranking, a LIFO stack for activity history, and a chained hash table for constant-time lookup.

Each structure was selected for a specific access pattern. The linked list supports an append-dominated registry. The FIFO queue preserves arrival order. The heap supports repeated minimum extraction. The stack supports most-recent-first retrieval. The hash table supports keyed access.

The matchmaking workflow connects these structures. A request is enqueued, persisted, and then matched by traversing the linked list, filtering available drivers, computing the Haversine distance and estimated arrival time for each candidate, inserting the candidates into the min-heap, and offering the ride to the heap root.

The rejection cascade is the most significant algorithmic outcome of the project. Because each ride retains its own candidate heap, a decline is handled by a single logarithmic extraction rather than a full rebuild. This converts a potentially quadratic workflow into a linearithmic one.

The system was verified through 48 automated test cases covering structure behaviour, matching and fare rules, the ride lifecycle, history ordering, and the end-to-end workflow. The complexity analysis in Chapter 9 confirmed the expected bounds, and the demonstration in Chapter 10 reproduced them on the seeded dataset of thirteen drivers.

From an engineering perspective, the project demonstrates that data structure selection is not an academic formality. The difference between a linear scan and a heap extraction determines whether reassignment remains responsive as the driver pool grows.

From a course perspective, the project addresses CLO 2, CLO 3, and CLO 4 through problem analysis, from-scratch implementation, and complexity evaluation, and it satisfies the Complex Engineering Problem attributes through breadth, depth, integration, and constraint handling.

## 12.2 Future Scope & Systemic Enhancements

- Replace the per-ride candidate heaps with a single indexed global min-heap so that a driver appears at most once across all active rides, using a decrease-key operation when availability changes.
- Move driver records from the in-memory linked list into persistent storage while retaining the linked list as the active availability index, so that registrations survive restarts.
- Extend the chained hash table into the matchmaking path by replacing the linked list search inside accept, complete, and cancel with an average constant-time lookup.
- Introduce live driver position streaming and periodic heap priority updates, using the existing update_priority routine to restore heap order.
- Replace straight-line Haversine distance with road-network distance from the routing service for the final candidate ordering, while keeping Haversine as a fast pre-filter.
- Add token-based authentication and explicit passenger and driver roles to replace the simplified identity selection of the academic build.
- Add payment recording, fare receipts, and driver ratings as separate modules without changing the graded data structures.
- Add property-based tests for heap invariants and for the ride state machine, in addition to the current example-based suite.
- Provide a load-test harness that measures matching latency as the driver pool scales from tens to thousands of drivers.
- Introduce a second priority queue dedicated to scheduled rides, ordered by pickup time rather than by ETA.

# CHAPTER 13: SOURCE CODE LISTINGS

## 13.1 Introduction

This chapter presents the source code of the core algorithms implemented in the Pink Wheels backend DSA package (backend/dsa/), together with the matchmaking service routines that consume them. The listings are grouped into the same five categories required by the Complex Engineering Problem assignment: linked lists, searching and sorting; stack and recursion; queue and heap algorithms; priority queue operations; and hashing with the matchmaking service layer.

Each listing corresponds to the pseudocode given in the Algorithm Design Document and to the complexity analysis in Chapter 9. Comments tagged [DSA] in the code mark the data structure or algorithm that each routine implements, along with its best, average, and worst-case time complexity where relevant.

The sorting utilities in Section 13.2 are design-level reference implementations used for comparative demonstration; they are not part of the ride API.

## 13.2 Linked Lists, Searching and Sorting

Files: backend/dsa/linked_list.py; design-level sorting utilities.

### 13.2.1 Driver Node and Append (append)

[[CODETITLE:Driver node definition and append routine|backend/dsa/linked_list.py]]

```python
class DriverNode:
    """Node representing a registered driver in the Singly Linked List."""

    def __init__(self, driver_id, driver_name, phone_number,
                 vehicle_number, current_latitude, current_longitude,
                 is_available=True, next_node=None):
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.phone_number = phone_number
        self.vehicle_number = vehicle_number
        self.current_latitude = current_latitude
        self.current_longitude = current_longitude
        self.is_available = is_available
        self.next = next_node

    def to_dict(self):
        return {
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "phone_number": self.phone_number,
            "vehicle_number": self.vehicle_number,
            "current_latitude": self.current_latitude,
            "current_longitude": self.current_longitude,
            "is_available": self.is_available,
        }


# [DSA] LINKED LIST: APPEND - walk to the tail, link the new node. O(n), O(1) space.
def append(self, driver_data):
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
```

### 13.2.2 Insert at Index (insert)

[[CODETITLE:Insert at a given position|backend/dsa/linked_list.py]]

```python
# [DSA] LINKED LIST: INSERT - splice after the predecessor. O(n) to reach k,
# O(1) at the head.
def insert(self, index, driver_data):
    if index < 0 or index > self._count:
        raise IndexError("Index out of bounds")
    new_node = DriverNode(
        driver_id=driver_data["driver_id"],
        driver_name=driver_data["driver_name"],
        phone_number=driver_data.get("phone_number", ""),
        vehicle_number=driver_data.get("vehicle_number", ""),
        current_latitude=float(driver_data.get("current_latitude", 24.8607)),
        current_longitude=float(driver_data.get("current_longitude", 67.0011)),
        is_available=driver_data.get("is_available", True),
    )
    if index == 0:
        new_node.next = self.head
        self.head = new_node
    else:
        current = self.head
        for _ in range(index - 1):
            if current is not None:
                current = current.next
        if current is not None:
            new_node.next = current.next
            current.next = new_node
    self._count += 1
    return new_node
```

### 13.2.3 Delete by Identifier (delete)

[[CODETITLE:Delete a driver node|backend/dsa/linked_list.py]]

```python
# [DSA] LINKED LIST: DELETE - unlink the target, handling the head case. O(n).
def delete(self, driver_id):
    if self.head is None:
        return False
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
```

### 13.2.4 Search (search)

[[CODETITLE:Linear search over the driver chain|backend/dsa/linked_list.py]]

```python
# [DSA] LINKED LIST: SEARCH - sequential scan. O(n) worst case, O(1) if head.
def search(self, driver_id):
    current = self.head
    while current is not None:
        if current.driver_id == driver_id:
            return current
        current = current.next
    return None
```

### 13.2.5 Traverse (traverse)

[[CODETITLE:Traverse the full chain|backend/dsa/linked_list.py]]

```python
# [DSA] LINKED LIST: TRAVERSE - visit every node once. O(n) time, O(n) result.
def traverse(self):
    result = []
    current = self.head
    while current is not None:
        result.append(current.to_dict())
        current = current.next
    return result
```

### 13.2.6 Availability Filtering (get_available_drivers)

[[CODETITLE:Collect available drivers for matching|backend/dsa/linked_list.py]]

```python
# [DSA] LINKED LIST: FILTER - keep nodes with is_available true. O(n).
def get_available_drivers(self):
    available = []
    current = self.head
    while current is not None:
        if current.is_available:
            available.append(current)
        current = current.next
    return available
```

### 13.2.7 Binary Search (design-level reference)

[[CODETITLE:Binary search over a sorted candidate array|design-level reference implementation]]

```python
# [DSA] BINARY SEARCH - halve the active window. O(log n) time, O(1) space.
def binary_search(items, target, key=lambda item: item):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        value = key(items[mid])
        if value == target:
            return mid
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

### 13.2.8 Bubble Sort with Early Exit (design-level reference)

[[CODETITLE:Bubble sort with early exit|design-level reference implementation]]

```python
# [DSA] BUBBLE SORT - stable, in place; early exit when a pass makes no swap.
# Best O(n), average/worst O(n^2), O(1) space.
def bubble_sort(items, key=lambda item: item):
    n = len(items)
    for end in range(n - 1, 0, -1):
        swapped = False
        for j in range(end):
            if key(items[j]) > key(items[j + 1]):
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:
            break
    return items
```

### 13.2.9 Quick Sort with Lomuto Partition (design-level reference)

[[CODETITLE:Quick sort with Lomuto partitioning|design-level reference implementation]]

```python
# [DSA] QUICK SORT - Lomuto partition, last element as pivot.
# Best/average O(n log n), worst O(n^2), O(log n) expected stack depth.
def quick_sort(items, low=0, high=None, key=lambda item: item):
    if high is None:
        high = len(items) - 1
    if low < high:
        pivot_index = partition(items, low, high, key)
        quick_sort(items, low, pivot_index - 1, key)
        quick_sort(items, pivot_index + 1, high, key)
    return items


def partition(items, low, high, key):
    pivot = key(items[high])
    i = low - 1
    for j in range(low, high):
        if key(items[j]) <= pivot:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[high] = items[high], items[i + 1]
    return i + 1
```

## 13.3 Stack and Recursion

Files: backend/dsa/stack.py.

### 13.3.1 Stack Node and Push (push)

[[CODETITLE:LIFO activity stack and push routine|backend/dsa/stack.py]]

```python
class StackNode:
    """Node representing an activity event in the LIFO Stack."""

    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class ActivityStack:
    """Custom LIFO Stack for ride activity logging and audit trail."""

    def __init__(self):
        self.top = None
        self._count = 0

    # [DSA] STACK: PUSH - link the new node at the top. O(1).
    def push(self, activity):
        if "timestamp" not in activity:
            activity["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_node = StackNode(data=activity, next_node=self.top)
        self.top = new_node
        self._count += 1
```

### 13.3.2 Pop and Peek (pop, peek)

[[CODETITLE:Pop and peek the most recent activity|backend/dsa/stack.py]]

```python
    # [DSA] STACK: POP - unlink and return the top node. O(1).
    def pop(self):
        if self.is_empty():
            return None
        target = self.top
        self.top = self.top.next
        self._count -= 1
        return target.data

    # [DSA] STACK: PEEK - inspect the top node without removal. O(1).
    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._count
```

### 13.3.3 Display from Top to Bottom (display)

[[CODETITLE:Traverse the stack most recent first|backend/dsa/stack.py]]

```python
    # [DSA] STACK: DISPLAY - visit every activity node once. O(n).
    def display(self):
        result = []
        current = self.top
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
```

### 13.3.4 Recursive Traversal (design-level reference)

[[CODETITLE:Recursive chain length and replay|design-level reference implementation]]

```python
# [DSA] RECURSION - the call stack mirrors the explicit LIFO stack.
# O(n) calls, O(n) stack space.
def chain_length(node):
    if node is None:
        return 0
    return 1 + chain_length(node.next)


def replay(node):
    if node is None:
        return
    replay(node.next)
    visit(node.data)
```

## 13.4 Queue and Heap Algorithms

Files: backend/dsa/queue.py, backend/dsa/priority_queue.py.

### 13.4.1 Linked FIFO Queue (enqueue, dequeue)

[[CODETITLE:FIFO ride request queue|backend/dsa/queue.py]]

```python
class QueueNode:
    """Node representing an element in the FIFO Queue."""

    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class RideQueue:
    """Custom FIFO Queue for incoming ride requests."""

    def __init__(self):
        self.front = None
        self.rear = None
        self._count = 0

    # [DSA] QUEUE: ENQUEUE - link at the rear. O(1).
    def enqueue(self, item):
        new_node = QueueNode(data=item)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._count += 1

    # [DSA] QUEUE: DEQUEUE - unlink the front; reset rear when empty. O(1).
    def dequeue(self):
        if self.is_empty():
            return None
        target = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._count -= 1
        return target.data
```

### 13.4.2 Heap Construction (heapify)

[[CODETITLE:Linear-time heap construction|backend/dsa/priority_queue.py]]

```python
    # [DSA] HEAP: HEAPIFY - sift down every internal node, bottom-up. O(n).
    def heapify(self, items):
        self.heap = [dict(item) for item in items]
        if len(self.heap) <= 1:
            return
        start_idx = self._parent(len(self.heap) - 1)
        for i in range(start_idx, -1, -1):
            self._sift_down(i)
```

## 13.5 Priority Queue (Binary Min-Heap)

Files: backend/dsa/priority_queue.py.

### 13.5.1 Priority Comparator (_is_higher_priority)

[[CODETITLE:Three-level candidate comparator|backend/dsa/priority_queue.py]]

```python
    # [DSA] HEAP: COMPARATOR - ETA, then distance, then driver id. O(1).
    def _is_higher_priority(self, a, b):
        eta_a = a.get("eta_minutes", 0.0)
        eta_b = b.get("eta_minutes", 0.0)
        if eta_a != eta_b:
            return eta_a < eta_b
        dist_a = a.get("distance_km", 0.0)
        dist_b = b.get("distance_km", 0.0)
        if dist_a != dist_b:
            return dist_a < dist_b
        return a.get("driver_id", 0) < b.get("driver_id", 0)
```

### 13.5.2 Sift Up and Sift Down (_sift_up, _sift_down)

[[CODETITLE:Heap repair routines|backend/dsa/priority_queue.py]]

```python
    # [DSA] HEAP: SIFT UP - restore order after insertion. O(log n).
    def _sift_up(self, index):
        current = index
        while current > 0:
            parent_idx = self._parent(current)
            if self._is_higher_priority(self.heap[current], self.heap[parent_idx]):
                self.heap[current], self.heap[parent_idx] = (
                    self.heap[parent_idx], self.heap[current])
                current = parent_idx
            else:
                break

    # [DSA] HEAP: SIFT DOWN - restore order after extraction. O(log n).
    def _sift_down(self, index):
        smallest = index
        size = len(self.heap)
        while True:
            left = self._left_child(smallest)
            right = self._right_child(smallest)
            candidate = smallest
            if left < size and self._is_higher_priority(
                    self.heap[left], self.heap[candidate]):
                candidate = left
            if right < size and self._is_higher_priority(
                    self.heap[right], self.heap[candidate]):
                candidate = right
            if candidate != smallest:
                self.heap[smallest], self.heap[candidate] = (
                    self.heap[candidate], self.heap[smallest])
                smallest = candidate
            else:
                break
```

### 13.5.3 Push and Pop (push, pop)

[[CODETITLE:Insertion and minimum extraction|backend/dsa/priority_queue.py]]

```python
    # [DSA] HEAP: PUSH - append then sift up. O(log n).
    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    # [DSA] HEAP: POP - replace root with the last leaf, then sift down. O(log n).
    def pop(self):
        if self.is_empty():
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def peek(self):
        return self.heap[0] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0
```

### 13.5.4 Update Priority and Sorted Display (update_priority, display)

[[CODETITLE:Priority repair and non-destructive ordering|backend/dsa/priority_queue.py]]

```python
    # [DSA] HEAP: UPDATE - locate, rewrite keys, then repair. O(n) + O(log n).
    def update_priority(self, driver_id, new_eta, new_distance):
        for i, item in enumerate(self.heap):
            if item.get("driver_id") == driver_id:
                item["eta_minutes"] = new_eta
                item["distance_km"] = new_distance
                self._sift_up(i)
                self._sift_down(i)
                return True
        return False

    # [DSA] HEAP: DISPLAY - pop a copy to obtain sorted order without mutation.
    def display(self):
        backup = [dict(x) for x in self.heap]
        temp_pq = DriverPriorityQueue()
        temp_pq.heap = [dict(x) for x in self.heap]
        ordered = []
        while not temp_pq.is_empty():
            ordered.append(temp_pq.pop())
        self.heap = backup
        return ordered
```

## 13.6 Hashing and Matchmaking Service

Files: backend/dsa/hash_table.py, backend/services/matchmaking.py.

### 13.6.1 Hash Table with Chaining (put, get, delete)

[[CODETITLE:Chained hash table for driver lookup|backend/dsa/hash_table.py]]

```python
class HashNode:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class DriverHashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self._count = 0

    # [DSA] HASH: MODULO - index = |key| mod capacity. O(1).
    def _hash(self, key):
        return abs(hash(key)) % self.capacity

    # [DSA] HASH: PUT - update in place or prepend to the bucket chain.
    def put(self, key, value):
        index = self._hash(key)
        head = self.buckets[index]
        current = head
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next
        self.buckets[index] = HashNode(key=key, value=value, next_node=head)
        self._count += 1

    # [DSA] HASH: GET - walk the collision chain. Average O(1), worst O(n).
    def get(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    # [DSA] HASH: DELETE - unlink from the bucket chain, handling the head.
    def delete(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        while current is not None:
            if current.key == key:
                if prev is None:
                    self.buckets[index] = current.next
                else:
                    prev.next = current.next
                self._count -= 1
                return True
            prev = current
            current = current.next
        return False
```

### 13.6.2 Geographic and Fare Utilities

[[CODETITLE:Haversine distance, ETA, and fare rules|backend/services/matchmaking.py]]

```python
# [DSA] GEOGRAPHIC: HAVERSINE - geodesic distance in kilometres. O(1).
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


# [DSA] GEOGRAPHIC: ETA - minutes at 25 km/h with a 2.0 minute floor. O(1).
def calculate_eta(distance_km, speed_kmh=25.0):
    if distance_km <= 0.0:
        return 2.0
    minutes = (distance_km / speed_kmh) * 60.0
    return round(max(2.0, minutes), 1)


# [DSA] GEOGRAPHIC: FARE - base plus per-kilometre rate by vehicle class. O(1).
def calculate_fare(distance_km, vehicle_type="Bike"):
    v_type = vehicle_type.lower()
    if "bike" in v_type:
        base_fare, rate_per_km = 50.0, 15.0
        label = "Bike (Pink Wheels)"
    elif "premium" in v_type or "good" in v_type:
        base_fare, rate_per_km = 150.0, 22.0
        label = "Good Car (Premium)"
    else:
        base_fare, rate_per_km = 100.0, 18.0
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
        "currency": "PKR",
    }
```

### 13.6.3 Candidate Heap Construction

[[CODETITLE:Linked list traversal and heap insertion|backend/services/matchmaking.py]]

```python
# [DSA] MATCHMAKING: BUILD - linked list -> eligible candidates -> min-heap.
# O(n log n) with repeated push, O(n) if heapified after collection.
def build_priority_queue_for_ride(pickup_lat, pickup_lon, excluded_driver_ids=None):
    if excluded_driver_ids is None:
        excluded_driver_ids = set()
    pq = DriverPriorityQueue()
    current = driver_list.head
    while current is not None:
        if current.is_available and current.driver_id not in excluded_driver_ids:
            dist = haversine_distance(
                current.current_latitude,
                current.current_longitude,
                pickup_lat,
                pickup_lon,
            )
            eta = calculate_eta(dist)
            pq.push({
                "driver_id": current.driver_id,
                "driver_name": current.driver_name,
                "phone_number": current.phone_number,
                "vehicle_number": current.vehicle_number,
                "current_latitude": current.current_latitude,
                "current_longitude": current.current_longitude,
                "distance_km": dist,
                "eta_minutes": eta,
            })
        current = current.next
    return pq
```

### 13.6.4 Rejection Cascade (reject_ride)

[[CODETITLE:Next-candidate extraction after a decline|backend/services/matchmaking.py]]

```python
# [DSA] MATCHMAKING: REJECT - one heap extraction per decline. O(log n).
def reject_ride(ride_id, driver_id):
    ride = get_ride_record(ride_id)
    if ride["status"] != "OFFERED":
        raise RideStateError(f"Ride #{ride_id} has no open offer to reject.")
    if ride.get("driver_id") is not None and ride["driver_id"] != driver_id:
        raise RideStateError(f"Ride #{ride_id} is not offered to Driver #{driver_id}.")

    driver_node = driver_list.search(driver_id)
    driver_name = driver_node.driver_name if driver_node else f"Driver #{driver_id}"
    activity_stack.push({
        "ride_id": ride_id,
        "driver_id": driver_id,
        "event": "RIDE_REJECTED",
        "description": f"Driver {driver_name} rejected Ride #{ride_id}. "
                       f"Searching next priority driver in Min-Heap.",
    })

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
            (next_driver["driver_id"], "OFFERED", ride_id),
        )
        activity_stack.push({
            "ride_id": ride_id,
            "driver_id": next_driver["driver_id"],
            "event": "DRIVER_REASSIGNED",
            "description": f"Ride #{ride_id} re-offered to next priority driver "
                           f"{next_driver['driver_name']} "
                           f"(ETA: {next_driver['eta_minutes']} min).",
        })
        return {"status": "OFFERED", "assigned_driver": next_driver}

    execute_commit(
        "UPDATE rides SET status = %s WHERE id = %s",
        ("NO_DRIVERS_AVAILABLE", ride_id),
    )
    activity_stack.push({
        "ride_id": ride_id,
        "event": "MATCHMAKING_EXHAUSTED",
        "description": f"No further available drivers for Ride #{ride_id}.",
    })
    return {"status": "NO_DRIVERS_AVAILABLE", "assigned_driver": None}
```

## 13.7 Chapter Summary

This chapter presented the source code of the graded data structures and of the matchmaking routines that consume them.

The listings covered the linked list with searching and sorting utilities, the LIFO stack with its recursive counterparts, the FIFO queue and heap construction, the binary min-heap priority queue with its comparator and repair routines, and the chained hash table together with the geographic, fare, candidate construction, and rejection cascade routines.

Each listing corresponds to the pseudocode in the Algorithm Design Document and to the complexity bounds derived in Chapter 9.
