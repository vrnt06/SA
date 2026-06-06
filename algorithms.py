# algorithms.py
from collections import deque


def first_come_first_served(processes):
    sorted_proc = sorted(processes, key=lambda x: x["at"])
    time = 0
    results, gantt = [], []
    for p in sorted_proc:
        if time < p["at"]:
            time = p["at"]
        start = time
        time += p["bt"]
        ct = time
        tat = ct - p["at"]
        wt = tat - p["bt"]
        results.append(
            {
                "pid": p["pid"],
                "at": p["at"],
                "bt": p["bt"],
                "ct": ct,
                "tat": tat,
                "wt": wt,
            }
        )
        gantt.append({"pid": p["pid"], "start": start, "end": time})
    return results, gantt


def shortest_job_first(processes):
    n = len(processes)
    time = 0
    completed = 0
    visited = [False] * n
    results, gantt = [], []

    while completed < n:
        idx = -1
        min_bt = float("inf")
        for i in range(n):
            if (
                processes[i]["at"] <= time
                and not visited[i]
                and processes[i]["bt"] < min_bt
            ):
                min_bt = processes[i]["bt"]
                idx = i

        if idx != -1:
            p = processes[idx]
            start = time
            time += p["bt"]
            ct = time
            tat = ct - p["at"]
            wt = tat - p["bt"]
            results.append(
                {
                    "pid": p["pid"],
                    "at": p["at"],
                    "bt": p["bt"],
                    "ct": ct,
                    "tat": tat,
                    "wt": wt,
                }
            )
            gantt.append({"pid": p["pid"], "start": start, "end": time})
            visited[idx] = True
            completed += 1
        else:
            unvisited_at = [
                p["at"] for i, p in enumerate(processes) if not visited[i]
            ]
            time = min(unvisited_at) if unvisited_at else time + 1
    return results, gantt


def round_robin(processes, quantum):
    """Calculates Round Robin scheduling metrics."""
    sorted_proc = sorted(processes, key=lambda x: x["at"])
    queue = deque()
    time = 0
    i = 0
    n = len(sorted_proc)

    remaining = {p["pid"]: p["bt"] for p in sorted_proc}
    at_map = {p["pid"]: p["at"] for p in sorted_proc}
    bt_map = {p["pid"]: p["bt"] for p in sorted_proc}
    ct_map = {}
    gantt = []

    while i < n or queue:
        while i < n and sorted_proc[i]["at"] <= time:
            queue.append(sorted_proc[i]["pid"])
            i += 1

        if queue:
            pid = queue.popleft()
            start = time
            exec_time = min(quantum, remaining[pid])
            time += exec_time
            remaining[pid] -= exec_time
            gantt.append({"pid": pid, "start": start, "end": time})

            while i < n and sorted_proc[i]["at"] <= time:
                queue.append(sorted_proc[i]["pid"])
                i += 1

            if remaining[pid] > 0:
                queue.append(pid)
            else:
                ct_map[pid] = time
        else:
            if i < n:
                time = sorted_proc[i]["at"]
            else:
                time += 1

    results = []
    for p in sorted_proc:
        pid = p["pid"]
        if pid in ct_map:
            at = at_map[pid]
            bt = bt_map[pid]
            tat = ct_map[pid] - at
            wt = tat - bt
            results.append(
                {
                    "pid": pid,
                    "at": at,
                    "bt": bt,
                    "ct": ct_map[pid],
                    "tat": tat,
                    "wt": wt,
                }
            )
    return results, gantt
