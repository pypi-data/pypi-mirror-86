
import inspect
import hashlib
import pickle
import os
import warnings
import functools
from typing import Callable, List, Tuple, Dict, Any, Optional


def cache_function(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        return cached(f, *args, **kwds)
    return wrapper
    

def cached(func: Callable[..., object], *args: object, **kwargs: object) -> Any:
    try:
        func_source = inspect.getsource(func)
    except (OSError, TypeError) as _e:
        warnings.warn(f"Could not cache '{func.__name__}' call because its source is not available")
        return func(*args, **kwargs)
    
    call_hash = _compute_hash_for_function_call(func_source, args, kwargs)

    if call_hash is None:
        warnings.warn(f"Could not cache '{func.__name__}' call because arguments are not picklable")
        return func(*args, **kwargs)

    cache_dir = "plotpage-cache"
    cache_path = os.path.join(cache_dir, func.__name__ + "-" + call_hash + ".pkl")

    try:
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    except:
        return_value = func(*args, **kwargs)

        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(return_value, f)
    
    return return_value

def _compute_hash_for_function_call(func_source: str, args: Tuple[object, ...], kwargs: Dict[str, object]) -> Optional[str]:
    # Construct the cache key as a hash based on the function, args and kwargs.
    # The purpose is to avoid false positives when retrieving cached results,
    # so if the function or arguments changes, the hash should change.
    # If the call is not hashable, return None, in which case caching will not happen.
    
    cache_parts: List[object] = []
    cache_parts.append(func_source)
    cache_parts.extend(("arg", arg) for arg in args)
    cache_parts.extend(("kwarg", kwarg) for kwarg in kwargs.items())
    
    cache_hash_key = hashlib.sha1()
    
    for cache_part in cache_parts:
        try:
            pickled_object = pickle.dumps(cache_part)
        except TypeError:
            return None
        
        cache_hash_key.update(pickled_object)
    
    return cache_hash_key.hexdigest()
