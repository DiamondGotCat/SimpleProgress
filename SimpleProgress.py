import time
import sys
import threading


class SimpleProgress:

    def __init__(self, tasks=[]):
        self.tasks = tasks

    @staticmethod
    def move_cursor(row, col):
        sys.stdout.write(f'\033[{row};{col}H')

    @staticmethod
    def print_progress_bar(task_id, progress, total, length=30):
        percent = ("{0:.1f}").format(100 * (progress / float(total)))
        filled_length = int(length * progress // total)
        bar = '\033[92m' + '-' * filled_length + '\033[91m' + '-' * (length - filled_length) + '\033[0m'
        return f'{task_id}: ({bar}) {percent}%'

    def task_wrapper(self, task_func, task_id, row, *args, **kwargs):
        total = 100
        for i in range(total):
            task_func(*args, **kwargs)
            self.move_cursor(row, 0)
            sys.stdout.write(self.print_progress_bar(task_id, i + 1, total))
            sys.stdout.flush()
        self.move_cursor(row, 0)
        sys.stdout.write(self.print_progress_bar(task_id, total, total) + '\n')
        sys.stdout.flush()

    def run_tasks(self, task_func, *args, **kwargs):
        sys.stdout.write('\033[2J')
        sys.stdout.flush()

        threads = []
        for i, task_id in enumerate(self.tasks):
            thread = threading.Thread(target=self.task_wrapper, args=(task_func, task_id, i + 1) + args, kwargs=kwargs)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.move_cursor(len(self.tasks) + 1, 0)
        print("All tasks completed!")


if __name__ == "__main__":

    def example_task():
        time.sleep(0.01)

    tasks = [
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4"
    ]

    progress = SimpleProgress(tasks=tasks)
    progress.run_tasks(example_task)
