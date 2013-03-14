Custom
======

Many customization are possible, to check different actions process, or retrieve the partner or address since another object

Extend search from phone number
-------------------------------

The function to retrieve the partner and it address since the phone number can be inherit
to custom you specific process, see below how to extend it

.. code-block:: python

    class cti_action(osv.osv):
        _inherit = 'cti.action'

        def find_partner_from_phone_number(self, cr, uid, phone_number, context=None):
            """
            Inherit function to find the partner and it address since the phone number
            """
            (partner_id, address_id) = super(cti_action, self).find_partner_from_phone_number(cr, uid, phone_number, context=context)

            return partner_id, address_id


