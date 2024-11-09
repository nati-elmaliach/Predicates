import asyncio

from remote_predicate_resource import RemotePredicateResource
from server import run_server


async def main():
    run_server()  # Runs on a different Therad
    await RemotePredicateResource.from_env(5)  # We can assign it to a variable and use it if we want

    try:
        # Keep the main coroutine running, This will never complete
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Task Cancel")


asyncio.run(main())
