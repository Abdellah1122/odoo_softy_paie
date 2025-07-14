# -*- coding: utf-8 -*-
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SoftyPayQualification(models.Model):
    _name = 'softy_pay.qualification'
    _description = "Fonction / Qualification Softy Paie"

    name        = fields.Char("Qualification", required=True)
    description = fields.Text("Description")

    _sql_constraints = [
        ('qualif_name_unique',
         'unique(name)',
         "Chaque qualification doit être unique.")
    ]


class SoftyPayEmployeeProfile(models.Model):
    _name = 'softy_pay.employee.profile'
    _description = "Profil Salarié Softy Paie"

    name        = fields.Char("Nom Profil", required=True)
    description = fields.Text("Description")

    _sql_constraints = [
        ('profile_name_unique',
         'unique(name)',
         "Chaque profil salarié doit être unique.")
    ]


class HrContractType(models.Model):
    _inherit = 'hr.contract.type'
    _description = "Type de Contrat étendu Softy Paie"

    code                  = fields.Char("Code Contrat", required=True)
    months_before_expiry  = fields.Integer(
        "Mois avant échéance",
        help="Déclenche un rappel ce nombre de mois avant la fin.")
    personnel_nature      = fields.Selection([
        ('permanent', "Permanent"),
        ('trainee',   "Stagiaire"),
        ('temporary',"Occasionnel"),
    ], string="Nature Personnel")

    _sql_constraints = [
        ('contract_type_code_unique',
         'unique(code)',
         "Le code Type de Contrat doit être unique.")
    ]


class SoftyPayRelationship(models.Model):
    _name = 'softy_pay.relationship'
    _description = "Type de Lien de Parentalité (Table Réf.)"

    code = fields.Char("Code Lien", required=True)
    name = fields.Char("Libellé Lien", required=True)

    _sql_constraints = [
        ('rel_code_unique',
         'unique(code)',
         "Le code du lien de parenté doit être unique."),
        ('rel_name_unique',
         'unique(name)',
         "Le libellé du lien de parenté doit être unique."),
    ]


class SoftyPayDocumentType(models.Model):
    _name = 'softy_pay.document.type'
    _description = "Type de Document (Table Réf.)"

    code = fields.Char("Code Type", required=True)
    name = fields.Char("Libellé Type", required=True)

    _sql_constraints = [
        ('doc_type_code_unique',
         'unique(code)',
         "Le code du type de document doit être unique."),
        ('doc_type_name_unique',
         'unique(name)',
         "Le nom du type de document doit être unique."),
    ]


class SoftyPayLanguage(models.Model):
    _name = 'softy_pay.language'
    _description = "Langue (Table Réf.)"

    code = fields.Char("Code Langue", required=True)
    name = fields.Char("Libellé Langue", required=True)

    _sql_constraints = [
        ('lang_code_unique',
         'unique(code)',
         "Le code de la langue doit être unique."),
        ('lang_name_unique',
         'unique(name)',
         "Le nom de la langue doit être unique."),
    ]


class SoftyPaySkill(models.Model):
    _name = 'softy_pay.skill'
    _description = "Compétence (Table Réf.)"

    code = fields.Char("Code Compétence", required=True)
    name = fields.Char("Libellé Compétence", required=True)

    _sql_constraints = [
        ('skill_code_unique',
         'unique(code)',
         "Le code de la compétence doit être unique."),
        ('skill_name_unique',
         'unique(name)',
         "Le nom de la compétence doit être unique."),
    ]


class SoftyPayCredit(models.Model):
    _name = 'softy_pay.credit'
    _description = "Crédit / Prêt (Table Réf.)"

    code = fields.Char("Code Crédit", required=True)
    name = fields.Char("Libellé Crédit", required=True)

    _sql_constraints = [
        ('credit_code_unique',
         'unique(code)',
         "Le code de crédit doit être unique."),
        ('credit_name_unique',
         'unique(name)',
         "Le nom du crédit doit être unique."),
    ]


class SoftyPayAbsenceType(models.Model):
    _name = 'softy_pay.absence.type'
    _description = "Type d'Absence (Table Réf.)"

    code = fields.Char("Code Absence", required=True)
    name = fields.Char("Libellé Absence", required=True)

    _sql_constraints = [
        ('abs_type_code_unique',
         'unique(code)',
         "Le code du type d'absence doit être unique."),
        ('abs_type_name_unique',
         'unique(name)',
         "Le nom du type d'absence doit être unique."),
    ]
