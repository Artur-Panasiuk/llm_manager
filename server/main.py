from threading import Thread
from queue_manager import queue_handler
from api import start_server
import time

if __name__ == '__main__':
    Thread(target=start_server, daemon=True).start()
    Thread(target=queue_handler, daemon=True).start()

    while True:
        time.sleep(1)
