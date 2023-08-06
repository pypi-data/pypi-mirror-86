#! -*- coding: utf8 -*-
import itertools

from termcolor import colored, cprint
from tabulate import tabulate

from .main import GetMovies
from .const import WEEK

def transferWeekDay(d):
    return d[:-2] + WEEK.get(d[-2], '') + d[-1:]

def generateTime(date, time):
    time = list(map(lambda x: ['', x], time))
    time[0][0] = transferWeekDay(date)
    return list(time)


def main():
    movies = GetMovies()
    for m in movies:
        cprint(m.get('title'), 'red', 'on_cyan')
        t = list(map(
            lambda v: generateTime(*v),
            m.get('time', dict()).items()
        ))
        print(
            tabulate(
                list(itertools.chain.from_iterable(t)),
                headers=['date', 'time'],
                tablefmt='fancy_grid',
                colalign=('right','right')
            )
        )

if __name__ == '__main__':
    main()
