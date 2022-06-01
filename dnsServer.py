import asyncio
import signal
from aiodnsresolver import Resolver
from dnsResolver import isFiltred
from dnsrewriteproxy import (
    DnsProxy,
)
def get_resolver():
    async def get_nameservers(_, __):
        for _ in range(0, 5):
            yield (0.5, ('8.8.8.8', 53))
    return Resolver(get_nameservers=get_nameservers)

def get_resolver_proxy():
    async def get_nameservers(_, __):
        for _ in range(0, 5):
            yield (0.5, ('1.1.1.1', 53))
    return Resolver(get_nameservers=get_nameservers)


async def async_main():
    start = DnsProxy(get_resolver=get_resolver,rules=((r'(^.*$)', r'\1'),))
    proxy_task = await start()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, proxy_task.cancel)
    loop.add_signal_handler(signal.SIGTERM, proxy_task.cancel)

    try:
        await proxy_task
    except asyncio.CancelledError:
        pass

asyncio.run(async_main())
print('End of program')