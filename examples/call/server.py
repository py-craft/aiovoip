import argparse
import asyncio
import aiovoip
import logging

sip_config = {
    'srv_host': 'xxxxxx',
    'srv_port': '7000',
    'realm': 'XXXXXX',
    'user': 'YYYYYY',
    'pwd': 'ZZZZZZ',
    'local_ip': '127.0.0.1',
    'local_port': 6000
}


async def on_invite(request, message):
    print('Call ringing!')
    dialog = await request.prepare(status_code=100)
    await dialog.reply(message, status_code=180)

    await dialog.reply(message, status_code=200)
    
    async for msg in dialog:
        if msg.method == 'BYE':
            await dialog.reply(msg, 200)
            break

    await dialog.close()

class Dialplan(aiovoip.BaseDialplan):

    async def resolve(self, *args, **kwargs):
        await super().resolve(*args, **kwargs)

        if kwargs['method'] == 'INVITE':
            return on_invite


def start(app, protocol):
    app.loop.run_until_complete(
        app.run(
            protocol=protocol,
            local_addr=(sip_config['local_ip'], sip_config['local_port'])))

    print('Serving on {} {}'.format(
        (sip_config['local_ip'], sip_config['local_port']), protocol))

    try:
        app.loop.run_forever()
    except KeyboardInterrupt:
        pass

    print('Closing')
    app.loop.run_until_complete(app.close())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--protocol', default='udp')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    app = aiovoip.Application(loop=loop, dialplan=Dialplan())

    if args.protocol == 'udp':
        start(app, aiovoip.UDP)
    elif args.protocol == 'tcp':
        start(app, aiovoip.TCP)
    elif args.protocol == 'ws':
        start(app, aiovoip.WS)
    else:
        raise RuntimeError("Unsupported protocol: {}".format(args.protocol))

    loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
