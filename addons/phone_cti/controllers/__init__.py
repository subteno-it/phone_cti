# -*- coding: utf-8 -*-
##############################################################################
#
#    phone_cti module for OpenERP, Pentaho Data Integration Connector
#    Copyright (C) 2012 SYLEAM (<http://www.syleam.fr/>)
#              Christophe CHAUVET <christophe.chauvet@syleam.fr>
#
#    This file is a part of phone_cti
#
#    phone_cti is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    phone_cti is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

try:
    import openerp.addons.web.common.http as openerpweb
except ImportError:
    import web.common.http as openerpweb

import werkzeug.wrappers
import werkzeug.utils

URL_CONFIGURE = 'http://syleam.github.com/phone_cti/configuration.html'


class CtiConnector(openerpweb.Controller):
    _cp_path = "/cti"

    @openerpweb.httprequest
    def incoming(self, request, **args):
        """
        If your database name is demo, use this query
        wget -q -O- http://localhost:8069/cti/incoming?database=demo
        """
        if 'database' not in args:
            return werkzeug.wrappers.Response('Missing "database" parameter', status=400)
        if 'user' not in args:
            return werkzeug.wrappers.Response('Missing "user" parameter', status=400)
        if 'token' not in args:
            return werkzeug.wrappers.Response('Missing "token" parameter', status=400)
        if 'phone' not in args:
            return werkzeug.wrappers.Response('Missing "phone" parameter', status=400)

        try:
            context_cti = {'cti': True}
            return request.session.proxy('cti').incoming(args.get('database'), args.get('user'),
                                                         args.get('token'), args.get('phone'))
        except Exception, e:
            return werkzeug.wrappers.Response(str(e), status=400)

    @openerpweb.httprequest
    def test(self, request, **args):
        """
        You can test this, with wget
        wget -q -O- http://localhost:8069/cti/test?database=demo
        """
        if 'database' not in args:
            # if database parameters is missing, return to the documention page
            return werkzeug.utils.redirect(URL_CONFIGURE)

        try:
            return request.session.proxy('cti').help(args.get('database'))
        except Exception, e:
            return werkzeug.wrappers.Response(str(e), status=400)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
