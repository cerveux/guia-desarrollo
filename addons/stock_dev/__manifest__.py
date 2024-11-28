# -*- coding: utf-8 -*-
{
    'name': "stock_dev",
    'summary': """
        Guia de Desarrollo""",
    'description': """
        Punto 6 de la guía de desarrollo
    """,
    'author': "Diego Guzmán",
    'website': "http://172.16.2.145:4500/home",
    'category': 'Stock',
    'version': '0.1',
    'depends': ['base', 'stock', 'helpdesk_mgmt'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
