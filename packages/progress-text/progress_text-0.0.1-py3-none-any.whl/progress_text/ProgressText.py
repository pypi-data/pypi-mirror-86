import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ProgressText:
    
    def __init__(self, iterable=None, every_percent=10):
        assert iterable is not None
        assert every_percent > 0 and every_percent < 100
        self.iterable = iterable
        self.every_percent = every_percent
        self.progress_printed = [False for _ in range(int(100 / every_percent))]
        self.update_every_iter = int(len(iterable) * every_percent / 100) + 1
        self.now_iter = -1
        self.max_iter = len(iterable)
        self.iterator = None
    
    def __iter__(self):
        self.now_iter = 0
        self.iterator = iter(self.iterable)
        return self

    def __next__(self):
        if self.now_iter < len(self.iterable):
            for i in range(len(self.progress_printed)):
                if self.now_iter >= self.max_iter * i * self.every_percent / 100:
                    continue
                current_offset = i - 1
                if not self.progress_printed[current_offset]:
                    self.progress_printed[current_offset] = True
                    logger.info("{}% ({}/{}) finished.".format(current_offset * self.every_percent, self.now_iter, len(self.iterable)))
                break
            self.now_iter += 1
            return next(self.iterator)
        else:
            logger.info("100% ({}/{}) finished.".format(self.now_iter, len(self.iterable)))
            raise StopIteration
