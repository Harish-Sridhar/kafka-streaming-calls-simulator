import threading
import queue
from modules import generate_messages
from modules import produce_messages

if __name__== "__main__":
    q = queue.Queue(3000)
    threads = list()
    threads.append(threading.Thread(target=generate_messages, kwargs={'queue': q}))
    threads.append(threading.Thread(target=produce_messages, kwargs={'queue': q}))

    for t in threads:
        t.start()

    for t in threads:
        t.join()