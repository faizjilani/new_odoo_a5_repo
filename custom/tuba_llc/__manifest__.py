# -*- coding: utf-8 -*-
{
    'name': "tuba_llc",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/tuba_products.xml',
        'views/tuba_sale_order.xml',
        'views/tuba_sale_damage.xml',
        'views/tuba_purchase_order.xml',
        'views/customer_receiving.xml',
        'views/supplier_payment.xml',
        'wizard/tuba_customer_report_wizard.xml',
        'wizard/tuba_supplier_report_wizard.xml',
        'wizard/tuba_inventory_report_wizard.xml',
        'report/tuba_customer_report.xml',
        'report/tuba_supplier_report.xml',
        'report/tuba_inventory_report.xml',
        'views/menu.xml',
        'data/sequence_tuba_sale_order.xml',
        'data/cron.xml',
    ],
}
