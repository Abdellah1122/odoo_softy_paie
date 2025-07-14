# -*- coding: utf-8 -*-
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SoftyPayRubriqueSalariale(models.Model):
    _name = 'softy_pay.rubrique.salariale'
    _description = "Rubrique Salariale"

    code            = fields.Char("Code", required=True)
    name            = fields.Char("Intitulé", required=True)
    rubrique_type   = fields.Selection([
        ('indemnite','Prime/Indemnité'),
        ('pret','Prêt'),
        ('cotisation','Cotisation')],
        "Type", required=True)
    gain_or_deduction = fields.Selection([
        ('gain','Gain'), ('retenue','Retenue')],
        "Sens", required=True)
    taxable         = fields.Boolean("Imposable", default=True)
    tax_code        = fields.Char("Code Impôt")
    rate            = fields.Float("Taux (%)", digits=(12,6))
    base_field      = fields.Selection([
        ('salary','Salaire de base'),
        ('days','Jours'),
        ('hours','Heures'),
        ('saisi','Saisi')],
        "Base Traitement", default='salary')
    operation       = fields.Selection([
        ('mul','Multiplication'),
        ('div','Division'),
        ('add','Addition'),
        ('sub','Soustraction')],
        "Opération", default='mul')
    coefficient     = fields.Float("Coefficient", digits=(12,6), default=1.0)
    ceiling_amount  = fields.Float("Plafond", digits='Payroll')
    ceiling_action  = fields.Selection([
        ('interdire','Interdire'),
        ('avertir','Avertir'),
        ('autoriser','Autoriser')],
        "Sur dépassement", default='avertir')
    fixed_or_calc   = fields.Selection([
        ('fixed','Fixe'),
        ('calculated','Calculée')],
        "Mode Calcul", default='calculated')

    _sql_constraints = [
        ('rub_code_unique', 'unique(code)', "Le code de rubrique doit être unique."),
    ]


class SoftyPayRubriquePatronale(models.Model):
    _name = 'softy_pay.rubrique.patronale'
    _description = "Rubrique Patronale / Variable"

    code         = fields.Char("Code", required=True)
    name         = fields.Char("Libellé", required=True)
    rate         = fields.Float("Taux (%)", digits=(12,6))
    base_field   = fields.Selection([
        ('salary','Salaire'),
        ('brut_impo','Brut imposable')],
        "Base", default='salary')
    employee_cats = fields.Many2many(
        'hr.employee.category', 'emp_cat_rub_pat_rel',
        'rub_id', 'cat_id',
        string="Catégories Employés")

    _sql_constraints = [
        ('pat_code_unique', 'unique(code)', "Le code patronal doit être unique."),
    ]


class SoftyPayBareme(models.Model):
    _name = 'softy_pay.bareme'
    _description = "Barème"

    code        = fields.Char("Code Barème", required=True)
    name        = fields.Char("Intitulé Barème", required=True)
    line_ids    = fields.One2many(
        'softy_pay.bareme.line', 'bareme_id', "Tranches")

    _sql_constraints = [
        ('bareme_code_unique', 'unique(code)', "Le code barème doit être unique."),
    ]


class SoftyPayBaremeLine(models.Model):
    _name = 'softy_pay.bareme.line'
    _description = "Ligne de Barème"

    bareme_id   = fields.Many2one(
        'softy_pay.bareme', "Barème", ondelete='cascade',
        required=True)
    min_value   = fields.Float("Valeur Min", required=True)
    max_value   = fields.Float("Valeur Max", required=True)
    rate        = fields.Float("Taux (%)", digits=(12,6), required=True)
    date_start  = fields.Date("Valide à partir de", required=True)
    date_end    = fields.Date("Valide jusqu’à")

    @api.constrains('min_value','max_value','rate')
    def _check_values(self):
        for rec in self:
            if rec.max_value < rec.min_value:
                raise ValidationError(_("Plafond < plancher sur une tranche"))
            if rec.rate < 0:
                raise ValidationError(_("Taux négatif non autorisé"))


class SoftyPayIntegrationTemplate(models.Model):
    _name = 'softy_pay.integration.template'
    _description = "Modèle d’Intégration Excel Pointage"

    name        = fields.Char("Nom Modèle", required=True)
    col_matricule = fields.Integer("Colonne Matricule", required=True)
    col_start   = fields.Integer("Colonne Déb. Rubriques", required=True)
    row_start   = fields.Integer("Ligne Déb. Intégration", required=True)

    _sql_constraints = [
        ('int_name_unique', 'unique(name)', "Le nom du modèle doit être unique."),
    ]


class SoftyPayPointageGrid(models.Model):
    _name = 'softy_pay.pointage.grid'
    _description = "Paramétrage Grille de Pointage"

    name        = fields.Char("Nom Grille", required=True)
    field_name  = fields.Char("Champ Pointage", required=True)
    label       = fields.Char("Libellé Colonne", required=True)
    visible     = fields.Boolean("Visible", default=True)
    modifiable  = fields.Boolean("Modifiable", default=True)

    _sql_constraints = [
        ('grid_name_field_unique',
         'unique(name, field_name)',
         "Chaque champ ne peut figurer qu’une fois par grille."),
    ]


class SoftyPayTeamLeader(models.Model):
    _name = 'softy_pay.team.leader'
    _description = "Chef d’équipe"

    name        = fields.Char("Nom Chef", required=True)
    employee_id = fields.Many2one(
        'hr.employee', "Salarié Référent", required=True)

    _sql_constraints = [
        ('leader_emp_unique',
         'unique(employee_id)',
         "Un salarié ne peut être chef d’équipe qu’une seule fois."),
    ]


class SoftyPayCompanyBank(models.Model):
    _name = 'softy_pay.company.bank'
    _description = "Banque Société"

    company_id  = fields.Many2one(
        'res.company', "Société", required=True, ondelete='cascade')
    bank_name   = fields.Char("Banque", required=True)
    bic         = fields.Char("Code BIC")
    iban        = fields.Char("IBAN", required=True)

    _sql_constraints = [
        ('bank_iban_unique',
         'unique(iban)',
         "Chaque IBAN doit être unique sur le système."),
    ]
