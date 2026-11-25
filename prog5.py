import threading
import time

mutex = threading.Semaphore(1)
wrt = threading.Semaphore(1)
read_count = 0
shared_data = 0

def reader(reader_id):
    global read_count

    mutex.acquire()
    read_count += 1
    if read_count == 1:
        wrt.acquire()  # First reader locks the resource
    mutex.release()

    print(f"Reader {reader_id}: read shared_data = {shared_data}")
    time.sleep(0.2)

    mutex.acquire()
    read_count -= 1
    if read_count == 0:
        wrt.release()  # Last reader unlocks the resource
    mutex.release()

def writer(writer_id):
    global shared_data

    wrt.acquire()
    shared_data += 1
    print(f"Writer {writer_id}: wrote shared_data = {shared_data}")
    time.sleep(0.3)
    wrt.release()

def main():
    w = [
        threading.Thread(target=writer, args=(1,)),
        threading.Thread(target=writer, args=(2,))
    ]
    r = [threading.Thread(target=reader, args=(i + 1,)) for i in range(5)]

    w[0].start()
    for t in r:
        t.start()
    w[1].start()

    for t in r:
        t.join()
    w[0].join()
    w[1].join()

if __name__ == "__main__":
    main()