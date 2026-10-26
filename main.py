import os

from data_structures import SkipList, FenwickTree
from helper_functions import loadCsv, rebuildFenwickAndTimestamps

# ==========================================
# MAIN INTERACTIVE PROGRAM
# ==========================================
def main():
    records = SkipList()
    fenwick = FenwickTree(0)
    timestamps = [0]

    # Automatically try loading the default CSV on startup if it exists
    default_path = r"/Users/saisuhamorri/Desktop/DSA/network_data.csv"
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
            csvPath = r"/Users/saisuhamorri/Desktop/DSA/network_data.csv"
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

# ============================================================
# OVERALL TIME COMPLEXITY
# CSV loading: O(n log n) expected
# Insert/Update: O(n log n) due to Fenwick Tree rebuilding
# Delete: O(n log n) due to Fenwick Tree rebuilding
# Search: O(log n) expected
# Range Query: O(log n + k) expected
# Predecessor/Successor: O(log n) expected
# Fenwick Tree sum/update operations: O(log n)
# Analytics/Status: O(n)
# Display All Records: O(n)
# Overall worst menu-operation complexity: O(n log n) expected
# ============================================================
