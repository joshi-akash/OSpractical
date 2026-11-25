class Process:
    def __init__(self, pid, at, bt, pr):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.pr = pr
        self.ct = 0
        self.tat = 0
        self.wt = 0
        self.rem = bt

def print_result(processes):
    total_wt = 0
    total_tat = 0
    print("\nPID\tAT\tBT\tCT\tTAT\tWT")
    for p in processes:
        print(f"{p.pid}\t{p.at}\t{p.bt}\t{p.ct}\t{p.tat}\t{p.wt}")
        total_wt += p.wt
        total_tat += p.tat
    n = len(processes)
    print(f"Average Waiting Time    = {total_wt / n:.2f}")
    print(f"Average Turnaround Time = {total_tat / n:.2f}")

def fcfs(processes):
    time = 0
    for p in processes:
        if time < p.at:
            time = p.at
        time += p.bt
        p.ct = time
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt
    print_result(processes)

def sjf(processes):
    n = len(processes)
    completed = 0
    time = 0
    done = [False] * n

    while completed < n:
        idx = -1
        min_bt = float("inf")
        for i in range(n):
            if not done[i] and processes[i].at <= time and processes[i].bt < min_bt:
                min_bt = processes[i].bt
                idx = i
        if idx == -1:
            time += 1
            continue
        time += processes[idx].bt
        processes[idx].ct = time
        processes[idx].tat = processes[idx].ct - processes[idx].at
        processes[idx].wt = processes[idx].tat - processes[idx].bt
        done[idx] = True
        completed += 1
    print_result(processes)

def priority_scheduling(processes):
    n = len(processes)
    completed = 0
    time = 0
    done = [False] * n

    while completed < n:
        idx = -1
        best = float("inf")
        for i in range(n):
            if not done[i] and processes[i].at <= time and processes[i].pr < best:
                best = processes[i].pr
                idx = i
        if idx == -1:
            time += 1
            continue
        time += processes[idx].bt
        processes[idx].ct = time
        processes[idx].tat = processes[idx].ct - processes[idx].at
        processes[idx].wt = processes[idx].tat - processes[idx].bt
        done[idx] = True
        completed += 1
    print_result(processes)

def round_robin(processes, quantum):
    n = len(processes)
    time = 0
    completed = 0
    for p in processes:
        p.rem = p.bt

    queue = []
    in_queue = [False] * n

    # Start with process(es) arriving at time 0, in PID order
    for i in range(n):
        if processes[i].at <= time:
            queue.append(i)
            in_queue[i] = True

    while completed < n:
        if not queue:
            time += 1
            for i in range(n):
                if not in_queue[i] and processes[i].rem > 0 and processes[i].at <= time:
                    queue.append(i)
                    in_queue[i] = True
            continue

        idx = queue.pop(0)
        slice_time = min(processes[idx].rem, quantum)
        time += slice_time
        processes[idx].rem -= slice_time

        for i in range(n):
            if not in_queue[i] and processes[i].rem > 0 and processes[i].at <= time and i != idx:
                queue.append(i)
                in_queue[i] = True

        if processes[idx].rem > 0:
            queue.append(idx)
        else:
            processes[idx].ct = time
            processes[idx].tat = processes[idx].ct - processes[idx].at
            processes[idx].wt = processes[idx].tat - processes[idx].bt
            completed += 1
            in_queue[idx] = False

    print_result(processes)

def main():
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        at, bt, pr = map(int, input(f"Process {i + 1} - Arrival Time, Burst Time, Priority: ").split())
        processes.append(Process(i + 1, at, bt, pr))

    print("\nMenu:\n1. FCFS\n2. SJF (Non-preemptive)")
    print("3. Priority (Non-preemptive)\n4. Round Robin")
    choice = int(input("Enter choice: "))

    if choice == 1:
        fcfs(processes)
    elif choice == 2:
        sjf(processes)
    elif choice == 3:
        priority_scheduling(processes)
    elif choice == 4:
        quantum = int(input("Enter time quantum: "))
        round_robin(processes, quantum)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()