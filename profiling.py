import timeit

from modules.file_manager import get_daily_log_path
from modules_optimized.file_manager_optimized import get_daily_log_path_optimized

# Measure execution time
time_original = timeit.timeit(
    "get_daily_log_path()",
    setup="from modules.file_manager import get_daily_log_path",
    number=1000
)
time_optimized = timeit.timeit(
    "get_daily_log_path_optimized()",
    setup="from modules_optimized.file_manager_optimized import get_daily_log_path_optimized",
    number=1000
)
print(f"Original function time for 1000 calls: {time_original:.6f} seconds")
print(f"Optimized function time for 1000 calls: {time_optimized:.6f} seconds")