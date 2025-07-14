# -*- coding: utf-8 -*-
from odoo import fields, models

class SoftyPayAffiliationType(models.Model):
    _name = "softy_pay.affiliation.type"
    _description = "Type d'affiliation salarié"

    code = fields.Char("Code", required=True)
    name = fields.Char("Libellé", required=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', "Le code doit être unique."),
    ]
