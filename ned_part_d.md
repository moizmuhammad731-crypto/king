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
