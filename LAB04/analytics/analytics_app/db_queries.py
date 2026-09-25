import concurrent.futures
from django.db import connection

def execute_db_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def run_parallel_queries(num_threads, query):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(execute_db_query, query) for _ in range(num_threads)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results

