import asipio
import pytest
import asyncio
import itertools

pytest_plugins = ['asipio.pytest_plugin']


class TestServer:
    def __init__(self, app, *, loop=None, host='127.0.0.1'):
        self.loop = loop
        self.host = host
        self.app = app
        self._loop = loop

    async def start_server(self, protocol, *, loop=None):
        self.handler = self.app.run(
            protocol=protocol,
            local_addr=(self.sip_config['server_host'], self.sip_config['server_port'])
        )
        return await self.handler

    async def close(self):
        pass

    @property
    def sip_config(self):
        return {
            'client_host': self.host,
            'client_port': 7000,
            'server_host': self.host,
            'server_port': 6000,
            'user': 'pytest',
            'realm': 'example.com'
        }


class TestProxy(TestServer):
    @property
    def sip_config(self):
        return {
            'server_host': self.host,
            'server_port': 8000,
        }


@pytest.fixture(params=['udp', 'tcp'])
def protocol(request):
    if request.param == 'udp':
        return asipio.UDP
    elif request.param == 'tcp':
        return asipio.TCP
    pytest.fail('Test requested unknown protocol: {}'.format(request.param))


@pytest.fixture
def test_server(protocol, loop):
    servers = []

    async def go(handler, **kwargs):
        server = TestServer(handler)
        await server.start_server(protocol, loop=loop, **kwargs)
        servers.append(server)
        return server

    yield go

    async def finalize():
        while servers:
            await servers.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture
def test_proxy(protocol, loop):
    servers = []

    async def go(handler, **kwargs):
        server = TestProxy(handler)
        await server.start_server(protocol, loop=loop, **kwargs)
        servers.append(server)
        return server

    yield go

    async def finalize():
        while servers:
            await servers.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture
def from_details(request):
    return 'sip:{user}@{host}:{port}'.format(
        user='pytest',
        host='127.0.0.1',
        port=7000
    )


@pytest.fixture
def to_details(request):
    return 'sip:{user}@{host}:{port}'.format(
        user='666',
        host='127.0.0.1',
        port=6000
    )


@pytest.fixture
def loop(event_loop):
    return event_loop


@pytest.fixture(params=itertools.permutations(('client', 'server')))
def close_order(request):
    return request.param
