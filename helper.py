#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on 11:31 am 30.03.20, by Yi Zhang

' a ... module of project '

__author__ = 'Yi Zhang'

import datetime as dt
import functools

def timer(func):
    '''Print the runtime of the decorated function'''
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        # Before performing func
        start_time = dt.datetime.now()
        val = func(*args, **kwargs)

        # after performing func
        end_time = dt.datetime.now()
        run_time = end_time - start_time
        days, mins, secs = str(run_time).split(':')
        print(f'Finished {func.__str__:s} in {int(days):d} days, {int(mins):d} minutes and {float(secs):.3f} seconds')
        return val
    return wrapper_timer

def description(newname):
    def wrapper_rename(func):
        func.__str__=newname
        return func
    return wrapper_rename

'''
@timer
@description('a new name')
def test_timer(i):
    return [x for x in range(i)]

test = test_timer(100000)
'''
