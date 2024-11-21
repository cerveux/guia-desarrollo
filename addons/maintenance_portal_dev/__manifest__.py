# -*- coding: utf-8 -*-
{
    'name': "maintenance_portal_dev",
    'summary': """
        Guia de Desarrollo""",
    'author': "Diego Guzmán",
    'website': "http://172.16.2.145:4500/home",
    'category': 'Maintenance',
    'version': '0.1',
    'depends': ['maintenance', 'hr_timesheet', 'product', 'maintenance_plan', 'maintenance_project', 'maintenance_request_sequence', 'resource'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_line.xml',
        'views/maintenance_request_data.xml',
        'views/maintenance_request_views.xml',
        'views/templates.xml',
        'views/mantenance_equipment.views.xml',
        'views/maintenance_plan_views.xml',
        'views/maintenance_kind_views.xml',
        'reports/templates.xml',
        'reports/report.xml',
        
    ],
    "application": False,
    'sequence': -1000, 
}
