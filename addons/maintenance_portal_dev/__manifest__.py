# -*- coding: utf-8 -*-
{
    'name': "maintenance_portal_dev",
    'summary': """
        Guia de Desarrollo""",
    'author': "Diego Guzmán",
    'website': "http://172.16.2.145:4500/home",
    'category': 'Maintenance',
    'version': '0.1',
    'depends': ['maintenance'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/maintenance_request_views.xml',
        'views/templates.xml',
    ],
    "application": False,
    'sequence': -1000, 
}
