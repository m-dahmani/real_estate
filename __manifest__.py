# -*- coding: utf-8 -*-

{
    'name': 'App One',
    'author': 'Mohamed DAHMANI',
    'version': '17.0.0.1.0',
    'category': '',
    'website': '',
    'depends': [
        'base', 'sale_management', 'account_accountant', 'mail', 'contacts',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'views/account_move_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'app_one/static/src/scss/property.scss',
        ],
        'web.report_assets_common': [
            'app_one/static/src/scss/font.scss',
        ],
    },

    'application': True,
}
