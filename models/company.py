# -*- coding: utf-8 -*-
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RetirementFund(models.Model):
    _name = 'softy_pay.retirement.fund'
    _description = 'Caisse de Retraite'

    name = fields.Char('Nom de la Caisse', required=True)

    _sql_constraints = [
        ('name_unique',
         'unique(name)',
         'Le nom de la caisse de retraite doit être unique.')
    ]


class ResCompany(models.Model):
    _inherit = 'res.company'

    rc_number = fields.Char(
        'Registre de Commerce',
        help='Numéro du registre de commerce de la société.')
    
    tax_ref = fields.Char(
        'Références Fiscales',
        help='Références fiscales de la société.')
    
    social_sec_ref = fields.Char(
        'N° Sécurité Sociale',
        help='Numéro de sécurité sociale de l’entreprise.')
    
    other_reg_ref = fields.Char(
        'Autres Références',
        help='Autres références réglementaires.')
    
    telex = fields.Char(
        'Télex',
          help='Numéro de télex.')
    
    retirement_fund_ids = fields.Many2many(
        'softy_pay.retirement.fund',
        'company_retire_rel',
        'company_id', 'fund_id',
        string='Caisses de Retraite')
    
    logo_image = fields.Binary('Logo Société')

    @api.constrains('rc_number', 'tax_ref')
    def _check_identifiers(self):
        for rec in self:
            if not rec.rc_number and not rec.tax_ref:
                raise ValidationError(
                    _("Au moins un des champs 'Registre de Commerce' "
                      "ou 'Références Fiscales' doit être renseigné.")
                )


class HrDepartment(models.Model):
    _inherit = 'hr.department'
    _description = 'Département / Client Softy Paie'

    company_id = fields.Many2one(
        'res.company', 'Société',
        required=True,
        default=lambda self: self.env.company.id,
        ondelete='cascade')
    code       = fields.Char('Code Département', required=True)
    address    = fields.Char('Adresse')
    phone      = fields.Char('Téléphone')
    fax        = fields.Char('Fax')
    telex      = fields.Char('Télex')

    _sql_constraints = [
        ('dept_code_unique',
         'unique(company_id, code)',
         'Le code Département doit être unique par Société.')
    ]


class SoftyService(models.Model):
    _name = 'softy_pay.service'
    _description = 'Service / Site Softy Paie'
    _order = 'company_id, department_id, code'

    company_id = fields.Many2one(
        'res.company', 'Société',
        required=True, ondelete='cascade')
    department_id = fields.Many2one(
        'hr.department', 'Département / Client',
        required=True, ondelete='cascade')
    code          = fields.Char('Code Service', required=True)
    name          = fields.Char('Nom Service', required=True)

    _sql_constraints = [
        ('service_code_unique',
         'unique(company_id, department_id, code)',
         'Le code Service doit être unique par Société et Département.')
    ]

    @api.constrains('company_id', 'department_id')
    def _check_dept_company(self):
        for rec in self:
            if rec.department_id.company_id != rec.company_id:
                raise ValidationError(
                    _("Le département doit appartenir à la même société "
                      "que le service.")
                )
