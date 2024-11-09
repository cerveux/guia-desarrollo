# -*- coding: utf-8 -*-
{
    'name': "maintenance_portal",

    'summary': "Adds a maintenance request view to customer portal",

    'author': "Be Innovation Tech SAS",
    'website': "https://beitech.com.ar/",

    'category': 'Maintenance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['maintenance', "maintenance_plan", "maintenance_project", 'portal', 'stock', 'base', 'base_maintenance', "maintenance_timesheet", "resource", "hr_holidays"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report.xml',
        'security/maintenance_portal_security.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    "installable": True,
}
