# Copyright (c) 2016 Erik Johansson <erik@ejohansson.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from . import requests

import http.client as http
import logging
import ssl
import urllib.parse


class Client(object):
    def __init__(self, username, password, server='com.sunny-portal.de',
                 port=http.HTTPS_PORT):
        super().__init__()
        self.log = logging.getLogger(__name__)
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.token = None

    def create_ssl_context(self):
        context = ssl.create_default_context()
        context.check_hostname = True
        return context

    def do_request(self, request):
        conn = http.HTTPSConnection(
            self.server, self.port, context=self.create_ssl_context())
        request.perform(conn)

    def get_token(self):
        if self.token is None:
            req = requests.AuthenticationRequest(self.username, self.password)
            self.do_request(req)
            self.token = req.get_token()
        return self.token

    def logout(self):
        if self.token is None:
            return
        req = requests.LogoutRequest(self.get_token())
        self.do_request(req)
        self.token = None

    def get_plants(self):
        req = requests.PlantListRequest(self.get_token())
        self.do_request(req)
