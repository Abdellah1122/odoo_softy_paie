# -*- coding: utf-8 -*-
from odoo import models, fields

class SoftyPayEmployeeAffiliation(models.Model):
    _name = "softy_pay.employee.affiliation"
    _description = "Affiliation salarié"

    employee_id  = fields.Many2one(
        'hr.employee', 
        string="Salarié", 
        required=True, 
        ondelete='cascade')
    type_id      = fields.Many2one(
        'softy_pay.affiliation.type',
        string="Type d'affiliation",
        required=True)
    numero       = fields.Char("Numéro d'affiliation", required=True)
    date_start   = fields.Date("Date d'affiliation", default=fields.Date.context_today)
    date_end     = fields.Date("Date de fin")
    active       = fields.Boolean("Actif", default=True)

    _sql_constraints = [
        ('employee_type_unique',
         'unique(employee_id, type_id)',
         "Ce salarié a déjà une affiliation de ce type."),
    ]
