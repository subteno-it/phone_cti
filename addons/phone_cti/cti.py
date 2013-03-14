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
import logging
import urllib

_logger = logging.getLogger('cti')
_logger.isEnabledFor(logging.DEBUG)


# You can inherit the cti.url_config in your profile if you want a custom documentation in your language
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
        'act_window_id': fields.many2one('ir.actions.act_window', 'Act Window', help='Select act windows'),

    }

    def init(self, cr):
        """
        we had a token fir the database
        use to authentify the request
        """
        param_obj = self.pool.get('ir.config_parameter')
        for key, func in _default_parameters.iteritems():
            ids = param_obj.search(cr, 1, [('key', '=', key)])
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

    def find_partner_from_phone_number(self, cr, uid, phone_number, context=None):
        """
        You can inherit this function, if you change the storage format for phone number in your database
        """
        _logger.debug('Phone number: %s' % phone_number)
        if context is None:
            context = self.pool.get('res.users').context_get(cr, uid, context=context)

        search_args = [
            '|',
            ('phone', '=', phone_number),
            ('mobile', '=', phone_number),
        ]
        address_obj = self.pool.get('res.partner.address')
        address_ids = address_obj.search(cr, uid, search_args, context=context)
        if not address_ids:
            return False, False

        address_id = address_ids[0]
        partner_id = address_obj.browse(cr, uid, address_id, context=context).partner_id
        partner_id = partner_id and partner_id.id or False

        return partner_id, address_id

    def _format_url_from_action(self, cr, uid, base_url, model, action_id, partner_id=False, address_id=False, context=None):

        url_param = {
            'id': partner_id,
            'view_type': 'form',
            'model': model,
            'action_id': action_id,
        }
        return base_url + '/#' + urllib.urlencode(url_param)

    def inspect_incoming(self, cr, uid, phone_number, context=None):
        """
        This function, check the phone number, and the user
        """
        # Retrieve the default URL for the web client, use to:
        # - default URL when no action found
        # - Compose the URL to return to the customer
        ir_config_obj = self.pool.get('ir.config_parameter')
        url = ir_config_obj.get_param(cr, 1, 'web.base.url', 'http://localhost:8069')

        # Retrieve the context for the user
        user_obj = self.pool.get('res.users')
        user_context = user_obj.context_get(cr, uid, context=context)
        if context is not None:
            user_context.update(context)

        # Search address and partner for this phone number
        (partner_id, address_id) = self.find_partner_from_phone_number(cr, uid, phone_number, context=user_context)
        if not partner_id and not address_id:
            return url

        # Check if default action is define from the company
        company_id = user_obj.browse(cr, uid, uid, context=user_context).company_id
        if not company_id:
            return url

        company = self.pool.get('res.company').browse(cr, uid, company_id.id, context=user_context)
        if not company.cti_action_id:
            # No action found on this company
            return url

        return self._format_url_from_action(cr, uid, url, company.cti_action_id.model_id.model, company.cti_action_id.act_window_id.id, partner_id, context=user_context)

cti_action()


class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'cti_action_id': fields.many2one('cti.action', 'CTI Action', help='CTI action by default when no match found'),
    }

res_company()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
