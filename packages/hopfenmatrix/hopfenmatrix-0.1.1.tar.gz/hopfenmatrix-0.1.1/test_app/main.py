import asyncio

from nio import InviteMemberEvent

import hopfenmatrix.run
import hopfenmatrix.config
import hopfenmatrix.callbacks
import hopfenmatrix.api_wrapper


async def test_send(api):
    while True:
        await asyncio.sleep(1)
        await api.send_message("test", "!RyLzgPLXqKckiBeGKc:matrix.hopfenspace.org")


async def main():
    """
    config = hopfenmatrix.config.Config().from_json("config.json")

    client = hopfenmatrix.client.new_async_client(config)
    client.add_event_callback(
        hopfenmatrix.callbacks.apply_filter(
            hopfenmatrix.callbacks.auto_join(client),
            hopfenmatrix.callbacks.allowed_users([])),
        InviteMemberEvent)

    api = hopfenmatrix.api_wrapper.ApiWrapper(client, config)
    callbacks = [test_send(client, config)]

    await hopfenmatrix.run.start_bot(client, config, callbacks)
    """
    matrix = hopfenmatrix.api_wrapper.ApiWrapper()
    matrix.set_auto_join(allowed_users=["@izomikron:matrix.hopfenspace.org"])
    matrix.add_coroutine_callback(test_send(matrix))
    await matrix.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
