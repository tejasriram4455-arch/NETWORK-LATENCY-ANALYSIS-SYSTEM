import os
import random

# ==========================================
# SKIP LIST ADT
# ==========================================
class SkipList:

    MAX_LEVEL = 8

    class Node:
        def __init__(self, timestamp, latency, level):
            self.timestamp = timestamp
            self.latency = latency
            self.next = [None] * (level + 1)

    def __init__(self):
        self.head = self.Node(-(2**63), 0, self.MAX_LEVEL)
        self.currentLevel = 0
        self.size_count = 0
        self.random = random.Random(7)

    # Generate a random level for a new node.
    def randomLevel(self):
        result = 0
        while result < self.MAX_LEVEL and self.random.getrandbits(1) == 1:
            result += 1
        return result

    # ADT: Insert / Put
    # If timestamp already exists, update its latency.
    def insert(self, timestamp, latency):
        if latency < 0 or latency > 2147483647:
            raise ValueError("Latency must be a valid nonnegative integer")

        update = [None] * (self.MAX_LEVEL + 1)
        current = self.head

        for i in range(self.currentLevel, -1, -1):
            while (current.next[i] is not None
                and current.next[i].timestamp < timestamp):
                current = current.next[i]
            update[i] = current

        current = current.next[0]

        # If timestamp exists, update its latency.
        if current is not None and current.timestamp == timestamp:
            current.latency = latency
            return

        newLevel = self.randomLevel()

        if newLevel > self.currentLevel:
            for i in range(self.currentLevel + 1, newLevel + 1):
                update[i] = self.head
            self.currentLevel = newLevel

        newNode = self.Node(timestamp, latency, newLevel)

        for i in range(newLevel + 1):
            newNode.next[i] = update[i].next[i]
            update[i].next[i] = newNode

        self.size_count += 1

    # ADT: Search / Get
    def search(self, timestamp):
        current = self.head

        for i in range(self.currentLevel, -1, -1):
            while (current.next[i] is not None
                and current.next[i].timestamp < timestamp):
                current = current.next[i]

        current = current.next[0]

        if current is not None and current.timestamp == timestamp:
            return current

        return None

    # ADT: Update latency.
    def updateLatency(self, timestamp, newLatency):
        if newLatency < 0 or newLatency > 2147483647:
            return False

        found = self.search(timestamp)
        if found is None:
            return False

        found.latency = newLatency
        return True

    # ADT: Delete
    def delete(self, timestamp):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.head

        for i in range(self.currentLevel, -1, -1):
            while (current.next[i] is not None
                and current.next[i].timestamp < timestamp):
                current = current.next[i]
            update[i] = current

        current = current.next[0]

        if current is None or current.timestamp != timestamp:
            return False

        for i in range(self.currentLevel + 1):
            if update[i].next[i] is current:
                update[i].next[i] = current.next[i]

        while (self.currentLevel > 0
            and self.head.next[self.currentLevel] is None):
            self.currentLevel -= 1

        self.size_count -= 1
        return True

    # ADT: Range Query
    def rangeQuery(self, startTime, endTime):
        result = []
        if startTime > endTime:
            return result

        current = self.head

        for i in range(self.currentLevel, -1, -1):
            while (current.next[i] is not None
                and current.next[i].timestamp < startTime):
                current = current.next[i]

        current = current.next[0]

        while current is not None and current.timestamp <= endTime:
            result.append(current)
            current = current.next[0]

        return result

    # ADT: Predecessor
    def predecessor(self, timestamp):
        current = self.head
        candidate = None

        for i in range(self.currentLevel, -1, -1):
            while (current.next[i] is not None
                and current.next[i].timestamp < timestamp):
                current = current.next[i]
                candidate = current

        return candidate

    # ADT: Successor
    def successor(self, timestamp):
        current = self.head

        for i in range(self.currentLevel, -1, -1):
            while (current.next[i] is not None
                and current.next[i].timestamp <= timestamp):
                current = current.next[i]

        return current.next[0]

    # ADT: Earliest record
    def earliest(self):
        return self.head.next[0]

    # ADT: Latest record
    def latest(self):
        current = self.head
        for i in range(self.currentLevel, -1, -1):
            while current.next[i] is not None:
                current = current.next[i]
        return None if current is self.head else current

    # ADT: Size
    def size(self):
        return self.size_count

    # ADT: Check whether empty
    def isEmpty(self):
        return self.size_count == 0

    # ADT: Clear all records
    def clear(self):
        for i in range(self.MAX_LEVEL + 1):
            self.head.next[i] = None
        self.currentLevel = 0
        self.size_count = 0

    # ADT: Display records in timestamp order
    def display(self):
        if self.isEmpty():
            print("Skip List is empty.")
            return
        print("-" * 35)
        print("Timestamp\t\tLatency (ms)")
        print("-" * 35)
        current = self.head.next[0]
        while current is not None:
            print(f"{current.timestamp}\t\t{current.latency}")
            current = current.next[0]
        print("-" * 35)


# ==========================================
# FENWICK TREE ADT
# ==========================================
class FenwickTree:

    def __init__(self, n):
        if n < 0:
            raise ValueError("Size cannot be negative")
        self.n = n
        self.bit = [0] * (n + 1)
        self.values = [0] * (n + 1)

    def checkIndex(self, index):
        if index < 1 or index > self.n:
            raise ValueError(f"Index {index} out of range (1 to {self.n})")

    def set(self, index, newValue):
        self.checkIndex(index)
        if newValue < 0 or newValue > 2147483647:
            raise ValueError("Latency must be a valid nonnegative integer")
        change = newValue - self.values[index]
        self.values[index] = newValue
        self.addDelta(index, change)

    def addDelta(self, index, change):
        while index <= self.n:
            self.bit[index] += change
            index += index & -index

    def prefixSum(self, index):
        if index < 0 or index > self.n:
            raise ValueError("Index out of range")
        total = 0
        while index > 0:
            total += self.bit[index]
            index -= index & -index
        return total

    def rangeSum(self, left, right):
        if left < 1 or right > self.n or left > right:
            raise ValueError("Invalid range indices")
        return self.prefixSum(right) - self.prefixSum(left - 1)

    def rangeAverage(self, left, right):
        total = self.rangeSum(left, right)
        return total / (right - left + 1)

    def totalSum(self):
        return self.prefixSum(self.n)

    def findKth(self, k):
        total = self.totalSum()
        if k < 1 or k > total:
            raise ValueError("k must be between 1 and the total sum")

        index = 0
        step = 1 << (self.n.bit_length() - 1) if self.n > 0 else 0
        remaining = k

        while step > 0:
            nextIndex = index + step
            if nextIndex <= self.n and self.bit[nextIndex] < remaining:
                remaining -= self.bit[nextIndex]
                index = nextIndex
            step >>= 1

        return index + 1

    def getValue(self, index):
        self.checkIndex(index)
        return self.values[index]

    def size(self):
        return self.n

    def clear(self):
        self.bit = [0] * (self.n + 1)
        self.values = [0] * (self.n + 1)

    def display(self, timestamps):
        if self.n == 0:
            print("Fenwick Tree is empty.")
            return
        print("-" * 45)
        print("Index\tTimestamp\t\tLatency (ms)")
        print("-" * 45)
        for i in range(1, self.n + 1):
            print(f"{i}\t{timestamps[i]}\t\t{self.values[i]}")
        print("-" * 45)


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def findTimestampIndex(timestamps, timestamp):
    left = 1
    right = len(timestamps) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if timestamps[mid] == timestamp:
            return mid
        elif timestamps[mid] < timestamp:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def rebuildFenwickAndTimestamps(records):
    size = records.size()
    fenwick = FenwickTree(size)
    timestamps = [0] * (size + 1)
    node = records.earliest()
    index = 1
    while node is not None:
        timestamps[index] = node.timestamp
        fenwick.set(index, node.latency)
        node = node.next[0]
        index += 1
    return fenwick, timestamps


def loadCsv(path, records):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found at: {path}")

    with open(path, "r", encoding="utf-8-sig") as file:
        lineNumber = 0
        firstContentLine = True

        for line in file:
            lineNumber += 1
            line = line.strip()
            if not line:
                continue

            if firstContentLine and line.lower().startswith("timestamp"):
                firstContentLine = False
                continue

            firstContentLine = False
            parts = line.split(",")
            if len(parts) != 2:
                raise ValueError(f"Expected timestamp,latency_ms at line {lineNumber}: {line}")

            try:
                timestamp = int(parts[0].strip())
                latency = int(parts[1].strip())
            except ValueError as error:
                raise ValueError(f"Invalid integer at line {lineNumber}: {line}") from error

            if latency < 0 or latency > 2147483647:
                raise ValueError(f"Invalid latency range at line {lineNumber}")

            records.insert(timestamp, latency)


# ==========================================
# MAIN INTERACTIVE PROGRAM
# ==========================================
def main():
    records = SkipList()
    fenwick = FenwickTree(0)
    timestamps = [0]

    # Automatically try loading the default CSV on startup if it exists
    default_path = r"C:\Users\Haasini seema\OneDrive\Desktop\DSA\network_data.csv"
    if os.path.isfile(default_path):
        try:
            loadCsv(default_path, records)
            fenwick, timestamps = rebuildFenwickAndTimestamps(records)
            print(f"[Auto-loaded {records.size()} records from default path: {default_path}]")
        except Exception as e:
            print(f"[Could not auto-load default CSV: {e}]")

    while True:
        print("\n========================================")
        print("     NETWORK LATENCY MANAGEMENT CLI")
        print("========================================")
        print(f"Current Records Loaded: {records.size()}")
        print("1. Load records from CSV file")
        print("2. Insert or Update a record (Timestamp & Latency)")
        print("3. Search for a record by timestamp")
        print("4. Delete a record by timestamp")
        print("5. Perform Range Query (Start Timestamp to End Timestamp)")
        print("6. Find Predecessor and Successor of a timestamp")
        print("7. View Earliest and Latest records")
        print("8. Fenwick Tree Analytics & Status Analysis")
        print("9. Display all records")
        print("10. Exit")
        print("----------------------------------------")

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            csvPath = r"C:\Users\tejas\OneDrive\Desktop\All Subjects\DSA\case study\network_data.csv"
            try:
                records.clear()
                loadCsv(csvPath, records)
                fenwick, timestamps = rebuildFenwickAndTimestamps(records)
                print(f"\nSuccessfully loaded {records.size()} records from:\n{csvPath}")
                print("\n--- Loaded Records ---")
                records.display()
            except Exception as e:
                print(f"\nError loading CSV: {e}")

        elif choice == "2":
            try:
                ts = int(input("Enter timestamp (integer): "))
                lat = int(input("Enter latency (ms, 0-2147483647): "))
                records.insert(ts, lat)
                fenwick, timestamps = rebuildFenwickAndTimestamps(records)
                print(f"\nSuccessfully inserted/updated record [Timestamp: {ts}, Latency: {lat} ms]")
            except ValueError as e:
                print(f"\nInvalid input: {e}")

        elif choice == "3":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            try:
                ts = int(input("Enter timestamp to search: "))
                node = records.search(ts)
                if node:
                    print(f"\nFound Record -> Timestamp: {node.timestamp} | Latency: {node.latency} ms")
                else:
                    print(f"\nRecord with timestamp {ts} not found.")
            except ValueError:
                print("\nPlease enter a valid integer timestamp.")

        elif choice == "4":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            try:
                ts = int(input("Enter timestamp to delete: "))
                success = records.delete(ts)
                if success:
                    fenwick, timestamps = rebuildFenwickAndTimestamps(records)
                    print(f"\nSuccessfully deleted record with timestamp {ts}.")
                else:
                    print(f"\nRecord with timestamp {ts} not found.")
            except ValueError:
                print("\nPlease enter a valid integer timestamp.")

        elif choice == "5":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            try:
                start = int(input("Enter start timestamp: "))
                end = int(input("Enter end timestamp: "))
                results = records.rangeQuery(start, end)
                if results:
                    print(f"\n--- Range Query Results ({start} to {end}) ---")
                    for r in results:
                        print(f"Timestamp: {r.timestamp} | Latency: {r.latency} ms")
                else:
                    print(f"\nNo records found in range {start} to {end}.")
            except ValueError:
                print("\nPlease enter valid integer timestamps.")

        elif choice == "6":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            try:
                ts = int(input("Enter timestamp: "))
                pred = records.predecessor(ts)
                succ = records.successor(ts)
                print(f"\nPredecessor: {pred.timestamp if pred else 'None'}")
                print(f"Successor: {succ.timestamp if succ else 'None'}")
            except ValueError:
                print("\nPlease enter a valid integer timestamp.")

        elif choice == "7":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            earliest = records.earliest()
            latest = records.latest()
            print(f"\nEarliest Record -> Timestamp: {earliest.timestamp} | Latency: {earliest.latency} ms")
            print(f"Latest Record   -> Timestamp: {latest.timestamp} | Latency: {latest.latency} ms")

        elif choice == "8":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            print("\n--- Fenwick Tree Analytics & Status ---")
            print(f"Total Cumulative Latency: {fenwick.totalSum()} ms")
            print(f"Overall Average Latency: {fenwick.rangeAverage(1, fenwick.size()):.2f} ms")

            warningThreshold = 100
            criticalThreshold = 180

            print("\nPer-Record Status Analysis:")
            for i in range(1, fenwick.size() + 1):
                lat = fenwick.getValue(i)
                status = "CRITICAL" if lat >= criticalThreshold else ("WARNING" if lat >= warningThreshold else "NORMAL")
                print(f"Timestamp: {timestamps[i]} | Latency: {lat} ms | Status: {status}")

        elif choice == "9":
            if records.isEmpty():
                print("\nNo records available.")
                continue
            print("\n--- Skip List Display ---")
            records.display()
            print("\n--- Fenwick Tree Display ---")
            fenwick.display(timestamps)

        elif choice == "10":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()