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
