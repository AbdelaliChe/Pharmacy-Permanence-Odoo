{
    'name': 'my_pharmacy',
    'author': 'Ab && Nss',
    'category': 'Healthcare',
    'summary': 'Manage pharmacy permanence',
    'description': 'This module allows you to manage pharmacy permanence and proximite.',
    'depends': ['base', 'website'],
    'data': [
        'views/pharmacy_view.xml',
        'views/pharmacy_template.xml',
        'views/pharmacy_detail_template.xml',
        'views/pharmacy_home.xml',
        'security/ir.model.access.csv',
        'views/medicines_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
