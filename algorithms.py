# algorithms.py


def first_come_first_served(processes):
    """Calculates FCFS scheduling metrics.

    Input format: [{'pid': str, 'at': int, 'bt': int}]
    """
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
    """Calculates Non-preemptive SJF scheduling metrics."""
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