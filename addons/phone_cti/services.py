# -*- coding: utf-8 -*-
##############################################################################
#
#    phone_cti module for OpenERP, PDI Connector
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

import netsvc
import openerp
import pooler
import logging
import openerp.exceptions
from psycopg2 import OperationalError
from openerp import SUPERUSER_ID

_logger = logging.getLogger('cti.service')

class cti(netsvc.ExportService):

    def __init__(self, name="cti"):
        netsvc.ExportService.__init__(self, name)

    def _check_auth(self, db, user, token):
        import pdb
        pdb.set_trace()
        pool = pooler.get_pool(db)
        cr = pooler.get_db(db).cursor()
        # Check if token is valid
        db_token = pool.get('ir.config_parameter').get_param(cr, SUPERUSER_ID, 'cti.uuid')
        if db_token != token:
            cr.close()
            raise openerp.exceptions.AccessDenied()

        # check if user exists
        user_id = pool.get('res.users').search(cr, SUPERUSER_ID, [('login','=',user)])
        if user_id:
            cr.close()
            return user_id[0]

        cr.close()
        raise openerp.exceptions.AccessDenied()

    def _pdi_dispatch(self, dbname, method_name, *method_args):
        try:
            registry = openerp.modules.registry.RegistryManager.get(dbname)
            assert registry, 'Unknown database %s' % dbname
            edi_document = registry['edi.document']
            cr = registry.db.cursor()
            res = None
            res = getattr(edi_document, method_name)(cr, *method_args)
            cr.commit()
        except Exception:
            _logger.exception('Failed to execute EDI method %s with args %r', method_name, method_args)
            raise
        finally:
            cr.close()
        return res

    def exp_incoming(self, dbname, username, token, values=None, *method_args):
        """
        Pass the phone number, token and user to search action to return
        and return the URL
        """
        try:
            registry = openerp.modules.registry.RegistryManager.get(dbname)
            assert registry, 'Unknown database %s' % dbname
            cr = registry.db.cursor()
            res = getattr(registry['cti.action'], 'inspect_incoming')(cr, *method_args)

            cr.commit()
        except Exception:
            _logger.exception('Failed to execute inspect_incoming method on cti.action with args...')
            raise
        finally:
            cr.close()

        return 'http://www.syleam.fr'

    def exp_help(self, dbname):
        """
        Return
        """
        try:
            registry = openerp.modules.registry.RegistryManager.get(dbname)
            assert registry, 'Unknown database %s' % dbname
            cr = registry.db.cursor()
            res = getattr(registry['cti.action'], 'compose_incoming_url')(cr, {})
        except OperationalError:
            raise Exception('Database %s does not exists' % dbname)
        except Exception:
            _logger.exception('Failed to execute inspect_incoming method on cti.action with args...')
            raise
        finally:
            cr.close()

        return res

    def dispatch(self, method, params):
        """
        Check method
        """
        if method in ('incoming'):
            (db, user, token) = params[0:3]
            self._check_auth(db, user, token)
        if method in ('help'):
            pass
        else:
            raise KeyError("Method not found: %s" % method)

        fn = getattr(self, 'exp_' + method)
        return fn(*params)

cti()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
