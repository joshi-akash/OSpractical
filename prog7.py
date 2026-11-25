P = 5  # Number of processes
R = 3  # Number of resource types

def calculate_need(maximum, allocation):
    return [[maximum[i][j] - allocation[i][j] for j in range(R)] for i in range(P)]

def is_safe(available, allocation, need):
    work = available[:]
    finish = [False] * P
    safe_seq = []

    while len(safe_seq) < P:
        found = False
        for i in range(P):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(R)):
                for k in range(R):
                    work[k] += allocation[i][k]
                safe_seq.append(i)
                finish[i] = True
                found = True
        if not found:
            return False, []  # No process could proceed: unsafe
    return True, safe_seq

def request_resources(pid, request, available, allocation, need):
    for j in range(R):
        if request[j] > need[pid][j]:
            print("Error: process has exceeded its maximum claim.")
            return False
        if request[j] > available[j]:
            print("Request denied: not enough resources available.")
            return False

    # Tentatively allocate
    for j in range(R):
        available[j] -= request[j]
        allocation[pid][j] += request[j]
        need[pid][j] -= request[j]

    safe, _ = is_safe(available, allocation, need)
    if safe:
        print("Request can be granted safely.")
        return True
    else:
        # Rollback
        for j in range(R):
            available[j] += request[j]
            allocation[pid][j] -= request[j]
            need[pid][j] += request[j]
        print("Request denied: would lead to an unsafe state.")
        return False

def main():
    available = list(map(int, input(f"Enter available resources of each type ({R} types): ").split()))

    print(f"Enter Maximum matrix ({P} processes x {R} resources):")
    maximum = [list(map(int, input().split())) for _ in range(P)]

    print("Enter Allocation matrix:")
    allocation = [list(map(int, input().split())) for _ in range(P)]

    need = calculate_need(maximum, allocation)

    safe, safe_seq = is_safe(available, allocation, need)
    if safe:
        print("System is in a SAFE state.")
        print("Safe sequence:", " ".join(f"P{p}" for p in safe_seq))
    else:
        print("System is in an UNSAFE state.")

    pid = int(input("\nEnter process number requesting resources: "))
    request = list(map(int, input(f"Enter request vector ({R} values): ").split()))

    request_resources(pid, request, available, allocation, need)

if __name__ == "__main__":
    main()