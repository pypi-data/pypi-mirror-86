# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
import socket

from .. import server


def test_exceptions():
    storages = dict(default='/some/path')

    # unterminated IPv6 address, one of the very few cases of unparseable URL
    url = 'tcp://[::'
    with pytest.raises(server.InvalidUrl) as exc_info:
        server.init([url], storages)
    assert exc_info.value.args == (url, 'Invalid IPv6 URL')

    # unsupported scheme
    url = 'exotic://localhost:1234'
    with pytest.raises(server.UnsupportedUrlScheme) as exc_info:
        server.init([url], storages)
    assert exc_info.value.args == ('exotic', )

    # bind error
    url = 'tcp://unresolvable-or-youre-kidding-me:0'
    with pytest.raises(server.BindError) as exc_info:
        server.init([url], storages)
    assert exc_info.value.args == (url, )

    # bind error with fixed port
    url = 'tcp://unresolvable-or-youre-kidding-me:1234'
    with pytest.raises(server.BindError) as exc_info:
        server.init([url], storages)
    assert exc_info.value.args == (url, )

    # bind error for non available port
    sock = None
    try:
        sock = socket.socket(socket.AF_INET)
        sock.bind(('127.0.0.1', 0))
        url = 'tcp://%s:%d' % sock.getsockname()
        with pytest.raises(server.BindError) as exc_info:
            server.init([url], storages)
    finally:
        assert sock is not None
        sock.close()
    assert exc_info.value.args == (url, )


def test_init_tcp():
    storages = dict(default='/some/path')
    server_instance = server.init(['tcp://localhost:0'], storages)
    try:
        server_instance.start()
    finally:
        server_instance.stop(None)
        server_instance.wait_for_termination()


def test_init_unix(tmpdir):
    storages = dict(default='/some/path')
    # 'unix://PATH' requires PATH to be absolute, whereas 'unix:PATH' does not.
    # currently, str(tmpdir) seems to be always absolute, but let's not depend
    # on that.
    url = 'unix:%s' % tmpdir.join('hgitaly.socket')
    server_instance = server.init([url], storages)
    try:
        server_instance.start()
    finally:
        server_instance.stop(None)
        server_instance.wait_for_termination()
