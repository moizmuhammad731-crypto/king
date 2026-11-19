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
    IF current.available AND current.id ∉ excluded THEN
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
  IF ride.status ∈ {COMPLETED, CANCELLED, NO_DRIVERS_AVAILABLE} THEN
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
  IF ride_id ∉ H_registry THEN
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
  IF ride.status ∈ {CANCELLED, COMPLETED} THEN
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
