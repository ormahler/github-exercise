from dal.github.github_seach_client import GithubSearchClient
import json
from multiprocessing.pool import ThreadPool
from functools import partial, reduce
import time
from datetime import datetime
import math


def main():
    git_hub_client = GithubSearchClient()
    handle_one_with_client = partial(handle_one, git_hub_client)
    total_count = 0
    final_res = []

    with open("queries.txt", "r") as q:
        queries = q.readlines()

        partition_queries = partition(queries, 10)
        with ThreadPool(10) as tp:
            for part in partition_queries:
                res = tp.map(handle_one_with_client, part)
                total_count = total_count + sum([r[0] for r in res])                     # overtime
                final_res = final_res + reduce(lambda a, b: a + b, [r[1] for r in res])  # overtime

                rate_limit_response = git_hub_client.get_rate_limit()
                sleep_time = rate_limit_response['resources']['search']['reset'] - math.floor(datetime.now().timestamp())
                if sleep_time > 0:
                    time.sleep(sleep_time)

    print(f"total_count: {total_count}")
    print(json.dumps(final_res, indent=2))


def handle_one(git_hub_client, query: str):
    total_count = 0
    items = []
    retry_query = None

    if query.startswith(GithubSearchClient.GITHUB_SEARCH_PREFIX):
        try:
            query_res: dict = git_hub_client.execute_search_query(query.strip())
            total_count = query_res['total_count']
            items = query_res['items']
        except Exception as e:
            print("failed to run query")
            retry_query = query

    return total_count, items, retry_query


def partition(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i: i+size]


if __name__ == '__main__':
    main()


