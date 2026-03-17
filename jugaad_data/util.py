"""Shared utility functions for caching, threading, and data conversion.

This module provides decorators for disk-based and time-based caching,
a thread pool helper, date range splitting, and optional numpy type
converters.
"""
import os
import collections
import json
import pickle
import time
import functools
from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor
import click
from appdirs import user_cache_dir

import calendar

import math

try:
    import numpy as np
except:
    np = None

def np_exception(function):
    """Decorator that raises :class:`ModuleNotFoundError` when numpy is unavailable."""
    def wrapper(*args, **kwargs):
        if not np:
            raise ModuleNotFoundError("Please install pandas and numpy using \n pip install pandas")
        return function(*args, **kwargs)

    return wrapper

@np_exception
def np_float(num):
    """Convert *num* to :class:`numpy.float64`, returning ``NaN`` on failure."""
    try:
        return np.float64(num)
    except:
        return np.nan

@np_exception
def np_date(dt):
    """Convert *dt* to :class:`numpy.datetime64`.

    Accepts ISO strings (``"2020-01-01"``), ``"%d-%b-%Y"`` (``"01-Jan-2020"``),
    and ``"%d %b %Y"`` (``"01 Jan 2020"``).  Returns ``NaT`` on failure.
    """
    try:
        return np.datetime64(dt)
    except:
        pass

    try:
        dt = datetime.strptime(dt, "%d-%b-%Y").date()
        return np.datetime64(dt)
    except:
        pass

    try:
        dt = datetime.strptime(dt, "%d %b %Y").date()
        return np.datetime64(dt)
    except:
        pass



    return np.datetime64('nat') 

    
@np_exception
def np_int(num):
    """Convert *num* to :class:`numpy.int64`, returning ``0`` on failure."""
    try:
        return np.int64(num)
    except:
        return 0

def break_dates(from_date, to_date):
    """Split a date range into per-month chunks.

    Args:
        from_date (datetime.date): Start date.
        to_date (datetime.date): End date.

    Returns:
        list[tuple]: List of ``(month_start, month_end)`` pairs that
        together cover the full range.
    """
    if from_date.replace(day=1) == to_date.replace(day=1):
        return [(from_date, to_date)]
    date_ranges = []
    month_start = from_date
    month_end = month_start.replace(day=calendar.monthrange(month_start.year, from_date.month)[1])
    while(month_end < to_date):
        date_ranges.append((month_start, month_end))
        month_start = month_end + timedelta(days=1)
        month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
        if month_end >= to_date:
            date_ranges.append((month_start, to_date))
    return date_ranges


def kw_to_fname(**kw):
    """Build a deterministic file name from keyword arguments.

    Joins the sorted keyword values with ``"-"``, skipping ``self``.
    Used by :func:`cached` to create unique cache file names.
    """
    name = "-".join([str(kw[k]) for k in sorted(kw) if k != "self"])
    return name



def cached(app_name):
    """
        Note to self:
            This is a russian doll
            wrapper - actual caching mechanism
            _cached - actual decorator
            cached - wrapper around decorator to make 'app_name' dynamic
    """
    def _cached(function):
        def wrapper(*args, **kw):
            kw.update(zip(function.__code__.co_varnames, args))
            env_dir = os.environ.get("J_CACHE_DIR")
            if not env_dir:
                cache_dir = user_cache_dir(app_name, app_name)
            else:
                cache_dir = os.path.join(env_dir, app_name)

            file_name = kw_to_fname(**kw)
            path = os.path.join(cache_dir, file_name)
            if not os.path.isfile(path):    
                if not os.path.exists(cache_dir):
                    os.makedirs(cache_dir)
                j = function(**kw)
                with open(path, 'wb') as fp:
                    pickle.dump(j, fp)        
            else:
                with open(path, 'rb') as fp:
                    j = pickle.load(fp)
            return j
        return wrapper
    return _cached


def pool(function, params, use_threads=True, max_workers=2):
    """Run *function* over *params* using a thread pool or sequentially.

    Args:
        function: Callable accepting positional args.
        params: Iterable of tuples, each unpacked as ``function(*p)``.
        use_threads: Use :class:`~concurrent.futures.ThreadPoolExecutor`
            when ``True`` (default), else run sequentially.
        max_workers: Maximum threads (default ``2``).

    Returns:
        Iterable of results, one per param tuple.
    """
    if use_threads:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            dfs = ex.map(function, *zip(*params))
    else:
        dfs = []
        for param in params:
            try:
                r = function(*param)
            except:
                raise 
            dfs.append(r)
    return dfs

def live_cache(app_name):
    """Time-based in-memory cache decorator for live data methods.

    Prevents hitting live-quote endpoints too frequently.  The first
    call fetches the result normally; subsequent calls within
    ``self.time_out`` seconds return the cached value.

    The decorated method's ``self`` object must have a ``time_out``
    attribute (seconds) and will gain a ``_cache`` dict attribute.
    """
    @functools.wraps(app_name)
    def wrapper(self, *args, **kwargs):
        # Get key by just concating the list of args and kwargs values and hope
        # that it does not break the code :P 
        inputs =  [str(a) for a in args] + [str(kwargs[k]) for k in kwargs]
        key = app_name.__name__ + '-'.join(inputs)
        now = datetime.now()
        time_out = self.time_out
        try:
            cache_obj = self._cache[key]
            if now - cache_obj['timestamp'] < timedelta(seconds=time_out):
                return cache_obj['value']
        except:
            self._cache = {}
        value = app_name(self, *args, **kwargs)
        self._cache[key] = {'value': value, 'timestamp': now}
        return value

    return wrapper 

