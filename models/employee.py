# -*- coding: utf-8 -*-
# pyright: reportAttributeAccessIssue=false, reportArgumentType=false
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Salarié Softy Paie'

    # -------------------------------------------------------------------------
    # Identifiants uniques
    # -------------------------------------------------------------------------
    matricule = fields.Char(
        string='Matricule',
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('hr.employee.matricule'),
    )
    cin = fields.Char(string='CIN', required=True)

    _sql_constraints = [
        ('matricule_unique',
         'unique(matricule)',
         'Le matricule doit être unique.'),
    ]

    # -------------------------------------------------------------------------
    # Informations personnelles
    # -------------------------------------------------------------------------
    name         = fields.Char('Nom Complet', required=True)
    birth_date   = fields.Date('Date de Naissance')
    gender       = fields.Selection(
        [('male', 'Masculin'), ('female', 'Féminin')],
        string='Genre',
    )
    home_address = fields.Char('Adresse')
    city         = fields.Char('Ville')
    mobile_phone = fields.Char('Téléphone')
    photo        = fields.Binary('Photo du Salarié')

    # -------------------------------------------------------------------------
    # Affiliations dynamiques (CNSS, AMO, IPE, CIMR…)
    # -------------------------------------------------------------------------
    affiliation_ids = fields.One2many(
        comodel_name='softy_pay.employee.affiliation',
        inverse_name='employee_id',
        string="Affiliations",
    )

    # -------------------------------------------------------------------------
    # Situation & diffusion
    # -------------------------------------------------------------------------
    situation = fields.Selection([
        ('normal', 'Normale'),
        ('accident', 'Accident de Travail'),
        ('conge', 'Congé'),
        ('maladie', 'Maladie'),
        ('maternite', 'Maternité'),
    ], string='Situation', default='normal')

    situation_start = fields.Date('Début Situation')
    situation_end   = fields.Date('Fin Situation')
    allow_diffusion = fields.Boolean('Autoriser diffusion Intranet')

    # -------------------------------------------------------------------------
    # Structure & affectations
    # -------------------------------------------------------------------------
    company_id       = fields.Many2one(
        'res.company', 'Société',
        default=lambda self: self.env.company.id,
    )
    department_id    = fields.Many2one(
        'hr.department', 'Département / Client',
        ondelete='set null',
    )
    service_id       = fields.Many2one(
        'softy_pay.service', 'Service / Site',
        ondelete='set null',
    )
    cost_center_id   = fields.Many2one(
        'account.analytic.account', 'Centre de Coût',
    )
    qualification_id = fields.Many2one(
        'softy_pay.qualification', 'Qualification / Fonction',
    )
    profile_id       = fields.Many2one(
        'softy_pay.employee.profile', 'Profil Salarié',
    )

    # -------------------------------------------------------------------------
    # Contrat & rémunération
    # -------------------------------------------------------------------------
    contract_type_id    = fields.Many2one(
        'hr.contract.type', 'Type de Contrat',
    )
    contract_start_date = fields.Date('Début Contrat')
    contract_end_date   = fields.Date('Fin Contrat')

    payment_type    = fields.Selection([
        ('monthly', 'Mensuel'),
        ('hourly', 'Horaire'),
    ], string='Type de Paiement')
    time_entry_type = fields.Selection([
        ('days', 'Jours'),
        ('hours', 'Heures'),
    ], string='Mode de Pointage')

    salary               = fields.Float('Salaire de Base', digits='Payroll')
    salary_periodicity   = fields.Selection([
        ('weekly', 'Semaine'),
        ('bi_monthly', 'Quinzaine'),
        ('monthly', 'Mois'),
    ], string='Périodicité Paie')
    pay_blocked          = fields.Boolean('Paie Bloquée')

    # -------------------------------------------------------------------------
    # Modalités de paiement
    # -------------------------------------------------------------------------
    payment_mode    = fields.Selection([
        ('bank_transfer', 'Virement'),
        ('cash', 'Cash Entreprise'),
    ], string='Mode de Paiement')
    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Compte Bancaire',
    )
    cash_account    = fields.Char('N° Compte Cash')
    bank_matricule  = fields.Char('Matricule Banque')
    bank_name       = fields.Char('Banque')

    # -------------------------------------------------------------------------
    # Rappels journaliers & annexes
    # -------------------------------------------------------------------------
    daily_allowance_ids  = fields.One2many(
        'softy_pay.daily.allowance', 'employee_id',
        string='Appointements Journaliers',
    )
    additional_info_ids  = fields.One2many(
        'softy_pay.employee.additional', 'employee_id',
        string='Informations Complémentaires',
    )
    dependent_ids        = fields.One2many(
        'softy_pay.employee.family', 'employee_id',
        string='Famille',
    )
    contract_ids         = fields.One2many(
        'softy_pay.employee.contract', 'employee_id',
        string='Historique Contrats',
    )
    document_ids         = fields.One2many(
        'softy_pay.employee.document', 'employee_id',
        string='Documents',
    )
    language_ids         = fields.One2many(
        'softy_pay.employee.language', 'employee_id',
        string='Langues',
    )
    experience_ids       = fields.One2many(
        'softy_pay.employee.experience', 'employee_id',
        string='Expériences',
    )
    publication_ids      = fields.One2many(
        'softy_pay.employee.publication', 'employee_id',
        string='Publications',
    )
    skill_ids            = fields.One2many(
        'softy_pay.employee.skill', 'employee_id',
        string='Compétences',
    )
    loan_ids             = fields.One2many(
        'softy_pay.employee.loan', 'employee_id',
        string='Prêts',
    )
    absence_ids          = fields.One2many(
        'softy_pay.employee.absence', 'employee_id',
        string='Absences',
    )
    accident_ids         = fields.One2many(
        'softy_pay.employee.accident', 'employee_id',
        string='Accidents',
    )

    # -------------------------------------------------------------------------
    # Onchange & contraintes
    # -------------------------------------------------------------------------
    @api.onchange('department_id')
    def _onchange_department(self):
        if self.department_id:
            return {
                'domain': {
                    'service_id': [
                        ('department_id', '=', self.department_id.id)
                    ]
                }
            }

    @api.constrains('contract_start_date', 'contract_end_date')
    def _check_contract_dates(self):
        for rec in self:                                        # ← plus de .filtered()
            if rec.contract_start_date and rec.contract_end_date \
            and rec.contract_end_date < rec.contract_start_date:
                raise ValidationError(
                    _("La date de fin doit être postérieure à la date de début.")
                )

    @api.constrains('department_id', 'company_id')
    def _check_dept_company(self):
        for rec in self.filtered('department_id'):
            if rec.department_id.company_id != rec.company_id:
                raise ValidationError(
                    _("Le département doit appartenir à la même société.")
                )

    @api.constrains('service_id', 'department_id')
    def _check_service_department(self):
        for rec in self.filtered('service_id'):
            if rec.service_id.department_id != rec.department_id:
                raise ValidationError(
                    _("Le service doit appartenir au même département.")
                )
