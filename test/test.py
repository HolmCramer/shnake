from threading import Thread
from time import sleep

def waiter() -> None:
    sleep(1)

def thread_builder() -> Thread:
    thread = Thread(target=waiter, args=())
    return thread

def main():
    while True:
        thread = thread_builder()
        thread.start()
        thread.join()
        print("finished")

main()