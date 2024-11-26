# -*- coding: utf-8 -*-
{
    'name': "helpdesk_mgmt_mod",
    'summary': """
        Guia de desarrollo help desk""",
    'author': "Diego Guzmán",
    'website': "http://172.16.2.145:4500/home",
    'category': 'Maintenance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk_mgmt', 'maintenance_portal_dev', 'helpdesk_type'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/helpdesk_mgmt_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": False,
    "sequence": -100,
}
