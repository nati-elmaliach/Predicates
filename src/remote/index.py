import asyncio

from remote_predicate_resource import RemotePredicateResource
from server import run_server


async def main():
    run_server() # Runs on a different Therad
    predicate_resource = await RemotePredicateResource.from_env(5)

    try:
        # Keep the main coroutine running, This will never complete
        await asyncio.Future() 
    except asyncio.CancelledError:
        print('Task Cancel')

asyncio.run(main())
