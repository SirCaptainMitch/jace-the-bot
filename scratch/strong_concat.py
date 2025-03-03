from functools import reduce
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # record start time
        result = func(*args, **kwargs)  # call the original function
        end_time = time.time()  # record end time
        print(f"{func.__name__} took {end_time - start_time:.10f} seconds")
        return result
    return wrapper



city = range(0, 10000)

@timer
def city_to_string_reduce(values):
    city_to_str = reduce(lambda x, y: str(x) + str(y), values)
    return city_to_str

@timer
def city_to_string_join(values):
    city_to_str = "".join([str(_) for _ in values])
    return city_to_str


print(city_to_string_reduce(city), 'city_to_string_reduce')
print(city_to_string_join(city), 'city_to_string_join')





