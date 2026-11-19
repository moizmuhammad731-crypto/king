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
    IF current.available AND current.id ∉ excluded THEN
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
  IF ride_id ∉ H_registry THEN
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
