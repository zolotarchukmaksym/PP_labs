from .db_queries import run_parallel_queries
import time

def run_experiment():
    results = []
    thread_counts = [2, 4, 8, 16, 32, 64]
    query = """
        SELECT technician_id, COUNT(*) AS repair_count 
        FROM repair 
        WHERE repair_date BETWEEN '2024-01-01' AND '2024-12-31' 
        GROUP BY technician_id 
        ORDER BY repair_count DESC;
    """

    for num_threads in thread_counts:
        start_time = time.time()
        result = run_parallel_queries(num_threads, query)
        end_time = time.time()

        execution_time = end_time - start_time
        results.append({
            'num_threads': num_threads,
            'execution_time': execution_time,
            'result': result
        })

    return results