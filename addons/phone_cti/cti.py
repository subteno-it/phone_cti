# -*- coding: utf-8 -*-
##############################################################################
#
#    phone_cti module for OpenERP, Computer telephony integration
#    Copyright (C) 2013 SYLEAM (<http://www.syleam.fr/>)
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

from openerp.osv import osv
from openerp.osv import fields
import uuid


_default_parameters = {
    "cti.uuid": lambda: str(uuid.uuid1()),
    "cti.url_config": lambda: 'http://syleam.github.com/phone_cti/configuration.html',
}


class cti_action(osv.osv):
    _name = 'cti.action'
    _description = 'Define action for the cti'

    _columns = {
        'name': fields.char('Name', size=64, help='Name of this action'),
        'model_id': fields.many2one('ir.model', 'Model', help='Model to launch search or name_search'),
        'field_name': fields.char('Field name', size=32, help='Field name to pass on search to find records'),
    }

    def init(self, cr):
        """
        we had a token fir the database
        use to authentify the request
        """
        param_obj = self.pool.get('ir.config_parameter')
        for key, func in _default_parameters.iteritems():
            ids = param_obj.search(cr, 1, [('key','=',key)])
            if not ids:
                param_obj.set_param(cr, 1, key, func())

    def compose_incoming_url(self, cr, context=None):
        """
        Compose the URL with
        """
        ir_config_obj = self.pool.get('ir.config_parameter')
        url = ir_config_obj.get_param(cr, 1, 'web.base.url', 'http://localhost:8069')
        token = ir_config_obj.get_param(cr, 1, 'cti.uuid')
        return '%s/cti/incoming?database=%s&user=%s&token=%s&phone=%s' % (url, cr.dbname, 'admin', token, 'XXX')

cti_action()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
