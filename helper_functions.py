import os

from data_structures import FenwickTree

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
