import asyncio

from remote_predicate_resource import RemotePredicateResource
from server import run_server


async def main():
    run_server()
    await RemotePredicateResource.from_env(5)

    while True:
        await asyncio.sleep(1)  # Sleep in small intervals to keep the loop running


asyncio.run(main())
