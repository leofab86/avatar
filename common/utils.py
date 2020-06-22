import asyncio


def run_async_coroutine(func):
    loop = asyncio.new_event_loop()

    async def async_handler():
        loop.run_in_executor(None, func)

    asyncio.run(async_handler())
    loop.close()
    # Closing the loop here causes an error when the async thread completes because it runs some code that checks
    # whether it is already closed. This error doesn't cause any problems because nothing is waiting on the loop.
    # So I prefer the error than potentially leaking resources from not closing the loop?
    # TODO: Figure out how to avoid this
