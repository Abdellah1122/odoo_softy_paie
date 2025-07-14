# -*- coding: utf-8 -*-
__manifest__ = {
    'name':        'Softy Paie (Models Only)',
    'version':     '1.0',
    'category':    'Hidden',
    'summary':     'Load only the Python models',
    'author':      'Abdellah Jorf',
    'depends':     ['base', 'hr', 'hr_contract', 'account'],
    # no data, no views, no security
    'data':        [],
    'installable': True,
    'application': False,
}
