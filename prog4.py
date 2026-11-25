import threading
import time

BUFFER_SIZE = 5
ITEMS = 10

buffer = [0] * BUFFER_SIZE
in_idx = 0
out_idx = 0

empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)

def producer():
    global in_idx
    for i in range(1, ITEMS + 1):
        empty.acquire()
        mutex.acquire()

        buffer[in_idx] = i
        print(f"Producer produced item {i} at slot {in_idx}")
        in_idx = (in_idx + 1) % BUFFER_SIZE

        mutex.release()
        full.release()
        time.sleep(0.1)

def consumer():
    global out_idx
    for _ in range(1, ITEMS + 1):
        full.acquire()
        mutex.acquire()

        item = buffer[out_idx]
        print(f"\t\tConsumer consumed item {item} from slot {out_idx}")
        out_idx = (out_idx + 1) % BUFFER_SIZE

        mutex.release()
        empty.release()
        time.sleep(0.15)

def main():
    prod = threading.Thread(target=producer)
    cons = threading.Thread(target=consumer)

    prod.start()
    cons.start()

    prod.join()
    cons.join()

    print("All items produced and consumed.")

if __name__ == "__main__":
    main()