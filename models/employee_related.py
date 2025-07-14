# -*- coding: utf-8 -*-
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SoftyPayDailyAllowance(models.Model):
    _name = 'softy_pay.daily.allowance'
    _description = "Appointements Journaliers"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    rule_code = fields.Char(
        "Code Rubrique", required=True,
        help="Référence dje la rubrique salariale.")
    description = fields.Char("Libellé Rubrique")
    rate = fields.Float("Taux", digits='Payroll', default=0.0)
    ceiling = fields.Float("Plafond (facultatif)", digits='Payroll')

    _sql_constraints = [
        ('employee_rule_unique',
         'unique(employee_id, rule_code)',
         "Chaque salarié ne peut avoir qu'une seule rubrique par code.")
    ]

    @api.constrains('rate', 'ceiling')
    def _check_amounts(self):
        for rec in self:
            if rec.rate < 0 or rec.ceiling < 0:
                raise ValidationError(
                    _("Le taux et le plafond doivent être positifs.")
                )


class SoftyPayEmployeeAdditional(models.Model):
    _name = 'softy_pay.employee.additional'
    _description = "Informations Complémentaires Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    code = fields.Char("Code Info", required=True)
    label = fields.Char("Libellé")
    value_text = fields.Char("Valeur Texte")
    value_num = fields.Float("Valeur Numérique")
    value_date = fields.Date("Valeur Date")
    value_list = fields.Char("Valeur Liste")

    _sql_constraints = [
        ('emp_add_unique',
         'unique(employee_id, code)',
         "Chaque info complémentaire doit être unique par code.")
    ]


class SoftyPayEmployeeFamily(models.Model):
    _name = 'softy_pay.employee.family'
    _description = "Membres de la Famille Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    name = fields.Char("Nom Membre", required=True)
    relationship_id = fields.Many2one(
        'softy_pay.relationship', "Lien de Parenté",
        required=True, ondelete='restrict')
    birth_date = fields.Date("Date de Naissance")
    notes = fields.Text("Remarques")

    _sql_constraints = [
        ('family_unique',
         'unique(employee_id, relationship_id, name)',
         "Impossible d'avoir deux fois le même membre de la même relation.")
    ]


class SoftyPayEmployeeContract(models.Model):
    _name = 'softy_pay.employee.contract'
    _description = "Historique des Contrats Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    reference = fields.Char("Réf. Contrat", required=True)
    contract_type_id = fields.Many2one(
        'hr.contract.type', "Type de Contrat", required=True)
    duration_months = fields.Integer("Durée (mois)")
    start_date = fields.Date("Début Contrat", required=True)
    end_date = fields.Date("Fin Contrat", required=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(
                    _("La date de fin doit être postérieure à la date de début.")
                )


class SoftyPayEmployeeDocument(models.Model):
    _name = 'softy_pay.employee.document'
    _description = "Documents Scannés Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    type_id = fields.Many2one(
        'softy_pay.document.type', "Type de Document", required=True)
    file_name = fields.Char("Nom de Fichier", required=True)
    file_data = fields.Binary("Fichier (scanné)", required=True)
    upload_date = fields.Datetime("Date d'Upload", default=fields.Datetime.now)

    _sql_constraints = [
        ('doc_unique',
         'unique(employee_id, type_id, file_name)',
         "Ce document existe déjà pour ce salarié.")
    ]


class SoftyPayEmployeeLanguage(models.Model):
    _name = 'softy_pay.employee.language'
    _description = "Langues Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    language_id = fields.Many2one(
        'softy_pay.language', "Langue", required=True)
    mastery_level = fields.Selection([
        ('basic', "Basique"),
        ('interm', "Intermédiaire"),
        ('advanced', "Avancé"),
        ('native', "Natif")],
        "Niveau", default='basic')
    knowledge_type = fields.Selection([
        ('spoken', "Oral"),
        ('written', "Écrit"),
        ('both', "Oral & Écrit")],
        "Type de Connaissance", default='both')
    certificate_file = fields.Binary("Diplôme / Certificat")

    _sql_constraints = [
        ('lang_emp_unique',
         'unique(employee_id, language_id)',
         "Chaque langue ne peut être déclarée qu'une fois par salarié.")
    ]


class SoftyPayEmployeeExperience(models.Model):
    _name = 'softy_pay.employee.experience'
    _description = "Expériences Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    company_name = fields.Char("Nom Société", required=True)
    sector = fields.Char("Secteur d'Activité")
    function = fields.Char("Fonction")
    start_date = fields.Date("Début")
    end_date = fields.Date("Fin")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(
                    _("La date de fin doit être postérieure à la date de début.")
                )


class SoftyPayEmployeePublication(models.Model):
    _name = 'softy_pay.employee.publication'
    _description = "Publications Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    title = fields.Char("Titre", required=True)
    pub_date = fields.Date("Date de publication")
    theme = fields.Char("Thème")
    language = fields.Char("Langue")
    country = fields.Char("Pays")


class SoftyPayEmployeeSkill(models.Model):
    _name = 'softy_pay.employee.skill'
    _description = "Compétences Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    skill_id = fields.Many2one(
        'softy_pay.skill', "Compétence", required=True)
    mastery_level = fields.Selection([
        ('novice', "Novice"),
        ('interm', "Intermédiaire"),
        ('expert', "Expert")],
        "Degré de Maîtrise", default='novice')

    _sql_constraints = [
        ('skill_emp_unique',
         'unique(employee_id, skill_id)',
         "Chaque compétence ne peut être déclarée qu'une fois par salarié.")
    ]


class SoftyPayEmployeeLoan(models.Model):
    _name = 'softy_pay.employee.loan'
    _description = "Prêts Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    credit_id = fields.Many2one(
        'softy_pay.credit', "Crédit", required=True)
    file_number = fields.Char("N° Dossier", required=True)
    loan_date = fields.Date("Date Prêt", required=True)
    amount = fields.Float("Montant", digits='Payroll', required=True)
    monthly_deduction = fields.Float("Prélèvement Mensuel", digits='Payroll')
    first_due_date = fields.Date("1re Échéance")
    last_due_date = fields.Date("Dernière Échéance")

    _sql_constraints = [
        ('loan_unique',
         'unique(employee_id, file_number)',
         "Ce numéro de dossier existe déjà pour ce salarié.")
    ]


class SoftyPayEmployeeAbsence(models.Model):
    _name = 'softy_pay.employee.absence'
    _description = "Absences Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    absence_type_id = fields.Many2one(
        'softy_pay.absence.type', "Type d'Absence", required=True)
    date_start = fields.Date("Date d'Absence", required=True)
    date_end = fields.Date("Date de Reprise", required=True)
    notes = fields.Text("Remarques")

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_end < rec.date_start:
                raise ValidationError(
                    _("La date de reprise doit être après la date d'absence.")
                )


class SoftyPayEmployeeAccident(models.Model):
    _name = 'softy_pay.employee.accident'
    _description = "Accidents de Travail Salarié"

    employee_id = fields.Many2one(
        'hr.employee', "Salarié", required=True, ondelete='cascade')
    accident_date = fields.Date("Date Accident", required=True)
    accident_time = fields.Float("Heure Accident (h.mm)", digits=(4, 2))
    file_number = fields.Char("N° Dossier AT", required=True)
    nature = fields.Char("Nature AT")
    cause = fields.Text("Causes & Circonstances")
    severity_degree = fields.Integer("Degré de Gravité")
    initial_stop_days = fields.Integer("Jours d’Arrêt Initiaux")

    _sql_constraints = [
        ('accident_unique',
         'unique(employee_id, file_number)',
         "Ce dossier d'accident existe déjà pour ce salarié.")
    ]

    @api.constrains('initial_stop_days', 'severity_degree')
    def _check_values(self):
        for rec in self:
            if rec.initial_stop_days < 0 or rec.severity_degree < 0:
                raise ValidationError(
                    _("Le degré de gravité et les jours d’arrêt doivent être ≥ 0.")
                )
