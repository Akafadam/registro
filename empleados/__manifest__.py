# -*- coding: utf-8 -*-
{
    'name': "empleados",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'citas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/horario.xml',
        'views/cargos.xml',
        'views/asistencias.xml',
        'views/nomina.xml',
        'data/cron_nomina.xml',
        'views/especialidad.xml',
        'views/views.xml',
        'views/citas_inherit_views.xml',
        'views/templates.xml',
        'report/asistencia.xml',
        'report/empleados.xml',
        'report/nomina.xml',
        'report/horario.xml',
        'report/cargos.xml',
        'report/especialidad.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/empleados.cargos.csv',
        'demo/demo.xml',
    ],
}
