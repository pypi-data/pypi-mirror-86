import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ProgressText:
    
    def __init__(self, iterable=None, every_percent=10, task_name="unnamed"):
        assert iterable is not None
        assert every_percent > 0 and every_percent < 100
        self.iterable = iterable
        self.every_percent = every_percent
        self.task_name = task_name
        self.progress_printed = [False for _ in range(int(100 / every_percent))]
        self.update_every_iter = int(len(iterable) * every_percent / 100) + 1
        self.now_iter = -1
        self.max_iter = len(iterable)
        self.iterator = None
        self.time_start = None
    
    def __iter__(self):
        self.now_iter = 0
        self.iterator = iter(self.iterable)
        self.time_start = time.time()
        return self

    def __next__(self):
        if self.now_iter < len(self.iterable):
            for i in range(len(self.progress_printed)):
                if self.now_iter >= self.max_iter * i * self.every_percent / 100:
                    continue
                current_offset = i - 1
                if not self.progress_printed[current_offset]:
                    self.progress_printed[current_offset] = True
                    time_elapsed = time.time() - self.time_start
                    logger.info("Task [{}] {}% ({}/{}) finished.\n"
                                "\t Elapsed time [{}]. Estimated time to finish [{}]."\
                                    .format(self.task_name, current_offset * self.every_percent,
                                            self.now_iter, len(self.iterable),
                                            time.strftime("%H:%M:%S", time.gmtime(time_elapsed)),
                                            "inf" if self.now_iter == 0 else time.strftime("%H:%M:%S", time.gmtime(time_elapsed * (self.max_iter - self.now_iter) / self.now_iter))))
                break
            self.now_iter += 1
            return next(self.iterator)
        else:
            time_elapsed = time.time() - self.time_start
            logger.info("Task [{}] 100% ({}/{}) finished.\n"
                        "\t Elapsed time [{}]."\
                            .format(self.task_name, self.now_iter, len(self.iterable),
                                    time.strftime("%H:%M:%S", time.gmtime(time_elapsed))))
            raise StopIteration
