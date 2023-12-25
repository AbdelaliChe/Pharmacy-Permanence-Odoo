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
<<<<<<< HEAD
=======
        'views/commande_view.xml',
        'views/my_pharmacy_report_template.xml',

>>>>>>> 186d7c5e2fdb0d60528881ac2d11829b65109ee9
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
