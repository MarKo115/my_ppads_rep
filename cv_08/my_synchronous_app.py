import requests
import time
import json
from requests.exceptions import HTTPError


def prepare_input():
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    list_isbn = ['9780002005883', '978000123456', '9780006178736', '9780006353287']
    urls_array = []
    for isbn in list_isbn:
        string = api + isbn
        urls_array.append(string)
    return urls_array


def prepare_output(resp):
    volume_info = resp.get("volumeInfo", {})
    title = volume_info.get("title", None)
    subtitle = volume_info.get("authors", None)
    published_date = volume_info.get("publishedDate", None)
    return title, subtitle, published_date


def request_book(url, sess):
    resp = None
    try:
        resp = sess.get(url)
        resp.raise_for_status()
        print(f"Response status ({url}): {resp.status_code}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    response_json = resp.json()
    items = response_json.get("items", [{}])[0]
    return items


if __name__ == "__main__":
    t1 = time.time()
    arr = prepare_input()
    with requests.Session() as session:
        for u in arr:
            response = request_book(u, session)
            parsed_response = prepare_output(response)
            print(f"Book: {json.dumps(parsed_response)}")

    print(time.time() - t1, "seconds passed")


