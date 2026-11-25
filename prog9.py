def fifo(ref, nf):
    frames = [-1] * nf
    front = 0
    faults = 0

    for page in ref:
        if page not in frames:
            frames[front] = page
            front = (front + 1) % nf
            faults += 1

    print(f"FIFO Page Faults  = {faults}")

def lru(ref, nf):
    frames = [-1] * nf
    last_used = [0] * nf
    filled = 0
    faults = 0

    for i, page in enumerate(ref):
        if page in frames:
            pos = frames.index(page)
            last_used[pos] = i
        else:
            faults += 1
            if filled < nf:
                frames[filled] = page
                last_used[filled] = i
                filled += 1
            else:
                # Find least recently used frame
                lru_idx = min(range(nf), key=lambda j: last_used[j])
                frames[lru_idx] = page
                last_used[lru_idx] = i

    print(f"LRU Page Faults   = {faults}")

def optimal(ref, nf):
    n = len(ref)
    frames = [-1] * nf
    filled = 0
    faults = 0

    for i, page in enumerate(ref):
        if page in frames[:filled]:
            continue

        faults += 1
        if filled < nf:
            frames[filled] = page
            filled += 1
            continue

        # Find the frame whose page is used farthest in future (or never)
        replace_idx = -1
        farthest = -1
        for j in range(nf):
            try:
                next_use = ref.index(frames[j], i + 1)
            except ValueError:
                replace_idx = j  # Never used again
                break
            if next_use > farthest:
                farthest = next_use
                replace_idx = j

        frames[replace_idx] = page

    print(f"Optimal Page Faults = {faults}")

def main():
    n = int(input("Enter number of pages in reference string: "))
    ref = list(map(int, input("Enter the reference string: ").split()))[:n]
    nf = int(input("Enter number of frames: "))

    fifo(ref, nf)
    lru(ref, nf)
    optimal(ref, nf)

if __name__ == "__main__":
    main()