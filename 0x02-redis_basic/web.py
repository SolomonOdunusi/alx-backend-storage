"""This module implements an
expiring web cache and tracker
"""
import redis
import requests


def get_page(url: str) -> str:
    """Obtains the html of a particular url"""
    r = redis.Redis()

    count_key = f"count:{url}"
    r.incr(count_key)

    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    content = response.text

    r.setex(url, 10, content)

    return content


"""Testcase for the get_page function
"""
if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/delay/1000/url/"
           "http://example.com")

    for i in range(3):
        page_content = get_page(url)
        print(f"Content fetched from {url}:\n{page_content}\n")

    r = redis.Redis()
    count_key = f"count:{url}"
    access_count = r.get(count_key)
    print(f"Access count for {url}: {int(access_count)}")
