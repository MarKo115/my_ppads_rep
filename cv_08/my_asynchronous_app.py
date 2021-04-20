import aiohttp
import asyncio
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


async def request_book(url, sess):
    resp = None
    try:
        resp = await sess.get(url)
        resp.raise_for_status()
        print(f"Response status ({url}): {resp.status}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    response_json = await resp.json()
    items = response_json.get("items", [{}])[0]
    return items


async def find_book(isbn, sess):
    response = await request_book(isbn, sess)
    parsed_response = prepare_output(response)
    print(f"Response: {json.dumps(parsed_response)}")


async def main():
    t1 = time.time()
    arr = prepare_input()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[find_book(u, session) for u in arr])

    print(time.time() - t1, "seconds passed")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


