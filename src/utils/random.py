import time
import random

sample = set(range(0, 999))


def generate_timebased_id():
    now_as_miliseconds = str(int(time.time()))
    return int(
        "{}{:03d}".format(now_as_miliseconds, random.sample(sample, 1)[0])
    )
