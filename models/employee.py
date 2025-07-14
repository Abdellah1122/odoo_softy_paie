# -*- coding: utf-8 -*-
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Salarié Softy Paie'

    # Unique identifiers
    matricule       = fields.Char(
        'Matricule',
        readonly=True,
        default=lambda self:
            self.env['ir.sequence'].next_by_code('hr.employee.matricule'))
    
    cin             = fields.Char('CIN', required=True)

    _sql_constraints = [
        ('matricule_unique',
         'unique(matricule)',
         'Le matricule doit être unique.'),
        ('cnss_unique',
         'unique(cnss_number)',
         'Le numéro CNSS doit être unique.')
    ]

    # Personal info
    name            = fields.Char('Nom Complet', required=True)
    birth_date      = fields.Date('Date de Naissance')
    gender          = fields.Selection(
        [('male', 'Masculin'), ('female', 'Féminin')],
        'Genre')
    
    home_address    = fields.Char('Adresse')
    city            = fields.Char('Ville')
    mobile_phone    = fields.Char('Téléphone')
    photo           = fields.Binary('Photo du Salarié')

    
    cnss_number     = fields.Char('N° CNSS')
    cnam_number     = fields.Char('N° Assurance Maladie')
    cimr_number     = fields.Char('N° CIMR')

    situation       = fields.Selection([
        ('normal', 'Normale'),
        ('accident', 'Accident de Travail'),
        ('conge', 'Congé'),
        ('maladie', 'Maladie'),
        ('maternite', 'Maternité')],
        'Situation', default='normal')
    
    situation_start = fields.Date('Début Situation')
    situation_end   = fields.Date('Fin Situation')
    allow_diffusion = fields.Boolean('Autoriser diffusion Intranet')

    # Structure & affectations
    company_id      = fields.Many2one(
        'res.company', 'Société',
        default=lambda self: self.env.company.id)
    department_id   = fields.Many2one(
        'hr.department', 'Département / Client',
        ondelete='set null')
    service_id      = fields.Many2one(
        'softy_pay.service', 'Service / Site',
        ondelete='set null')
    cost_center_id  = fields.Many2one(
        'account.analytic.account', 'Centre de Coût')
    qualification_id = fields.Many2one(
        'softy_pay.qualification', 'Qualification / Fonction')
    profile_id       = fields.Many2one(
        'softy_pay.employee.profile', 'Profil Salarié')

    # Contract & salary
    contract_type_id   = fields.Many2one(
        'hr.contract.type', 'Type de Contrat')
    contract_start_date = fields.Date('Début Contrat')
    contract_end_date   = fields.Date('Fin Contrat')

    payment_type     = fields.Selection([
        ('monthly', 'Mensuel'), ('hourly', 'Horaire')],
        'Type de Paiement')
    time_entry_type  = fields.Selection([
        ('days', 'Jours'), ('hours', 'Heures')],
        'Mode de Pointage')

    salary           = fields.Float(
        'Salaire de Base', digits='Payroll')
    salary_periodicity = fields.Selection([
        ('weekly', 'Semaine'),
        ('bi_monthly', 'Quinzaine'),
        ('monthly', 'Mois')],
        'Périodicité Paie')
    pay_blocked      = fields.Boolean('Paie Bloquée')

    # Payment details
    payment_mode     = fields.Selection([
        ('bank_transfer', 'Virement'),
        ('cash', 'Cash Entreprise')],
        'Mode de Paiement')
    bank_account_id  = fields.Many2one(
        'res.partner.bank', 'Compte Bancaire')
    cash_account     = fields.Char('N° Compte Cash')
    bank_matricule   = fields.Char('Matricule Banque')
    bank_name        = fields.Char('Banque')

    # Daily allowances
    daily_allowance_ids = fields.One2many(
        'softy_pay.daily.allowance', 'employee_id',
        'Appointements Journaliers')

    # Dynamic complementary info
    additional_info_ids = fields.One2many(
        'softy_pay.employee.additional', 'employee_id',
        'Informations Complémentaires')

    # Annex modules
    dependent_ids    = fields.One2many(
        'softy_pay.employee.family', 'employee_id', 'Famille')
    contract_ids     = fields.One2many(
        'softy_pay.employee.contract', 'employee_id', 'Historique Contrats')
    document_ids     = fields.One2many(
        'softy_pay.employee.document', 'employee_id', 'Documents')
    language_ids     = fields.One2many(
        'softy_pay.employee.language', 'employee_id', 'Langues')
    experience_ids   = fields.One2many(
        'softy_pay.employee.experience', 'employee_id', 'Expériences')
    publication_ids  = fields.One2many(
        'softy_pay.employee.publication', 'employee_id', 'Publications')
    skill_ids        = fields.One2many(
        'softy_pay.employee.skill', 'employee_id', 'Compétences')
    loan_ids         = fields.One2many(
        'softy_pay.employee.loan', 'employee_id', 'Prêts')
    absence_ids      = fields.One2many(
        'softy_pay.employee.absence', 'employee_id', 'Absences')
    accident_ids     = fields.One2many(
        'softy_pay.employee.accident', 'employee_id', 'Accidents')

    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id:
            return {'domain': {
                'service_id': [('department_id', '=', self.department_id.id)]
            }}

    @api.constrains('contract_start_date', 'contract_end_date')
    def _check_contract_dates(self):
        for rec in self:
            if rec.contract_start_date and rec.contract_end_date \
               and rec.contract_end_date < rec.contract_start_date:
                raise ValidationError(
                    _("La date de fin doit être postérieure à la date de début.")
                )

    @api.constrains('department_id', 'company_id')
    def _check_dept_company(self):
        for rec in self:
            if rec.department_id and rec.department_id.company_id != rec.company_id:
                raise ValidationError(
                    _("Le département doit appartenir à la même société.")
                )

    @api.constrains('service_id', 'department_id')
    def _check_service_department(self):
        for rec in self:
            if rec.service_id and rec.service_id.department_id != rec.department_id:
                raise ValidationError(
                    _("Le service doit appartenir au même département.")
                )
