import multiprocessing
import time
import pathlib
import hashlib

# print(f"Number of Cores: {multiprocessing.cpu_count()}")

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def parallel_fib(n):
    with multiprocessing.Pool() as pool:                # Wrapper function to distribute tasks and collect results
        results = pool.map(fibonacci, range(n))         # Split the calculation of the Fibonacci sequence
    return results

if __name__ == "__main__":
    n = 41
    fib_resultts = parallel_fib(n)      # Collect the results
    print(fib_resultts)
