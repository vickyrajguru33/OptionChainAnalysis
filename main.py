print('Hello from Python Project')

from db_handler import init_db
from scheduler import start_scheduler

if __name__ == "__main__":
    init_db()
    start_scheduler()

