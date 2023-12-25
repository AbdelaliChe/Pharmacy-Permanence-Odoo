{
    'name': 'my_pharmacy',
    'author': 'Ab && Nss',
    'category': 'Healthcare',
    'summary': 'Manage pharmacy permanence',
    'description': 'This module allows you to manage pharmacy permanence and proximite.',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/pharmacy_view.xml',
        'views/pharmacy_template.xml',
        'views/pharmacy_detail_template.xml',
        'views/pharmacy_home.xml',
        'views/medicines_view.xml',
        'views/permanence_view.xml',
        'views/stock_view.xml',
        'views/commande_view.xml'
        'views/my_pharmacy_report_template.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
