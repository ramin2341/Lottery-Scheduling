
# Fair-Share Scheduling Algorithm

groups = {
    "Group A": {
        "weight": 1,
        "processes": [
            {"name": "P1", "burst": 5},
            {"name": "P2", "burst": 3}
        ]
    },
    "Group B": {
        "weight": 1,
        "processes": [
            {"name": "P3", "burst": 4},
            {"name": "P4", "burst": 2}
        ]
    }
}

time = 0
timeline = []
completion = {}
waiting = {}

group_cpu = {name: 0 for name in groups}

for group in groups.values():
    for p in group["processes"]:
        p["remaining"] = p["burst"]

print("FAIR-SHARE CPU SCHEDULING")
print("-" * 55)

while any(
    p["remaining"] > 0
    for group in groups.values()
    for p in group["processes"]
):
    active_groups = [
        name for name, group in groups.items()
        if any(p["remaining"] > 0
               for p in group["processes"])
    ]

    # Select the group with the lowest normalized CPU usage
    selected_group = min(
        active_groups,
        key=lambda name:
            group_cpu[name] / groups[name]["weight"]
    )

    group = groups[selected_group]

    # Round Robin within the selected group
    active_processes = [
        p for p in group["processes"]
        if p["remaining"] > 0
    ]

    process = min(
        active_processes,
        key=lambda p: p.get("last_run", -1)
    )

    process["remaining"] -= 1
    process["last_run"] = time
    group_cpu[selected_group] += 1

    timeline.append((process["name"], time, time + 1))
    time += 1

    if process["remaining"] == 0:
        completion[process["name"]] = time

print("\nGantt Chart:")
for name, start, end in timeline:
    print(f"| {name} ({start}-{end}) ", end="")
print("|")

print("\nProcess  Group    Burst  Waiting  Turnaround")

total_waiting = 0
total_turnaround = 0
process_count = 0

for group_name, group in groups.items():
    for p in group["processes"]:
        turnaround = completion[p["name"]]
        wait = turnaround - p["burst"]

        total_waiting += wait
        total_turnaround += turnaround
        process_count += 1

        print(
            f'{p["name"]:<9}'
            f'{group_name:<9}'
            f'{p["burst"]:<7}'
            f'{wait:<9}'
            f'{turnaround}'
        )

print("-" * 55)
print("Average Waiting Time:",
      round(total_waiting / process_count, 2))
print("Average Turnaround Time:",
      round(total_turnaround / process_count, 2))

print("\nCPU Usage by Group:")
for name in groups:
    print(f"{name}: {group_cpu[name]} time units")