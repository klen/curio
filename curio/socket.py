# curio/socket.py
#
# Standin for the standard socket library.  The entire contents of stdlib socket are
# made available here.  However, the socket class is replaced by an async compatible version.
# Certain blocking operations are also replaced by versions safe to use in async.
#

import socket as _socket

__all__ = _socket.__all__  # type: ignore[attr-defined]

from socket import *
from functools import wraps, partial

from . import workers
from . import io


@wraps(_socket.socket)  # type: ignore[no-redef]
def socket(*args, **kwargs):
    return io.Socket(_socket.socket(*args, **kwargs))


@wraps(_socket.socketpair)  # type: ignore[no-redef]
def socketpair(*args, **kwargs):
    s1, s2 = _socket.socketpair(*args, **kwargs)
    return io.Socket(s1), io.Socket(s2)


@wraps(_socket.fromfd)  # type: ignore[no-redef]
def fromfd(*args, **kwargs):
    return io.Socket(_socket.fromfd(*args, **kwargs))


# Replacements for blocking functions related to domain names and DNS

# @wraps(_socket.create_connection)
# async def create_connection(*args, **kwargs):
#    sock = await workers.run_in_thread(partial(_socket.create_connection, *args, **kwargs))
#    return io.Socket(sock)


async def create_connection(address, timeout=None, source_address=None):  # type: ignore[no-redef]
    """
    Pure async implementation of the socket.create_connection function in standard library
    """
    host, port = address
    err = None
    for res in await getaddrinfo(host, port, 0, SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket(af, socktype, proto)
            if source_address:
                sock.bind(source_address)
            await sock.connect(sa)
            # Break explicitly a reference cycle
            err = None
            return sock

        except error as _:
            err = _
            if sock is not None:
                await sock.close()

    if err is not None:
        raise err
    else:
        raise OSError("getaddrinfo returns an empty list")


@wraps(_socket.getaddrinfo)  # type: ignore[no-redef]
async def getaddrinfo(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.getaddrinfo, *args, **kwargs))


@wraps(_socket.getfqdn)  # type: ignore[no-redef]
async def getfqdn(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.getfqdn, *args, **kwargs))


@wraps(_socket.gethostbyname)  # type: ignore[no-redef]
async def gethostbyname(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.gethostbyname, *args, **kwargs))


@wraps(_socket.gethostbyname_ex)  # type: ignore[no-redef]
async def gethostbyname_ex(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.gethostbyname_ex, *args, **kwargs))


@wraps(_socket.gethostname)  # type: ignore[no-redef]
async def gethostname(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.gethostname, *args, **kwargs))


@wraps(_socket.gethostbyaddr)  # type: ignore[no-redef]
async def gethostbyaddr(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.gethostbyaddr, *args, **kwargs))


@wraps(_socket.getnameinfo)  # type: ignore[no-redef]
async def getnameinfo(*args, **kwargs):
    return await workers.run_in_thread(partial(_socket.getnameinfo, *args, **kwargs))
