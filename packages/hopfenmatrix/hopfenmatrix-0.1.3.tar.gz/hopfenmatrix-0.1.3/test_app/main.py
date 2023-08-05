import asyncio

import hopfenmatrix.run
import hopfenmatrix.config
import hopfenmatrix.callbacks
import hopfenmatrix.api_wrapper


async def test_send(api):
    await api.send_message("test", "!RyLzgPLXqKckiBeGKc:matrix.hopfenspace.org")
    await asyncio.sleep(0.1)


def command_y():
    async def send_response(api, room, event):
        await api.send_message("Received ping - PONG", "!RyLzgPLXqKckiBeGKc:matrix.hopfenspace.org")
    return send_response


def command_x():
    async def send_response_2(api, room, event):
        await api.send_message("DINGE !", room.room_id)
    return send_response_2


async def main():
    matrix = hopfenmatrix.api_wrapper.ApiWrapper()
    matrix.set_auto_join(allowed_users=["@izomikron:matrix.hopfenspace.org"])
    matrix.add_coroutine_callback(test_send(matrix))
    matrix.register_command(command_y(), ["ping", "p"])
    matrix.register_command(command_x(), ["pong", "p"])
    await matrix.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
