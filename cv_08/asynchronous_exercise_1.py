# Written by Anton Caceres
# https://github.com/MA3STR0/PythonAsyncWorkshop
import time
import asyncio
import aiohttp


async def request_greetings(name, work_queue):
    responses = []
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            async with session.get(url) as response:
                res = await response.text()
            responses.append(res)
        texts = '\n'.join(responses)
        return texts


async def main():
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for url in [
        'http://dsl.sk',
        'http://stuba.sk',
        'http://shmu.sk',
        'http://root.cz',
    ]:
        await work_queue.put(url)

    # Run tasks
    t1 = time.time()
    greetings = await asyncio.gather(request_greetings("One", work_queue), request_greetings("Two", work_queue))
    print(time.time() - t1, "seconds passed")
    print(greetings)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


