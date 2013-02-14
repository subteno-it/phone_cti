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

{
    'name': 'Phone CTI',
    'version': '1.0',
    'category': 'Custom',
    'description': """Computer telephony integration""",
    'author': 'SYLEAM',
    'website': 'http://www.syleam.fr/',
    'depends': [
        'web',
    ],
    'init_xml': [],
    'images': [],
    'update_xml': [
        #'security/groups.xml',
        #'security/ir.model.access.csv',
        #'view/menu.xml',
        #'wizard/wizard.xml',
        #'report/report.xml',
    ],
    'demo_xml': [],
    'test': [],
    #'external_dependancies': {'python': ['kombu'], 'bin': ['which']},
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
    'application': True,
    'complexity': "expert",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
