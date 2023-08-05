from odoo import api, models


class IrModelData(models.TransientModel):
    _name = 'somconnexio.module'

    @api.model
    def import_bank_data(self):
        bank_data_wizard = self.sudo().env["l10n.es.partner.import.wizard"].create({})
        bank_data_wizard.execute()

    @api.model
    def install_languages(self):
        installer = self.sudo().env['base.language.install'].create({'lang': 'es_ES'})
        installer.lang_install()
        installer = self.sudo().env['base.language.install'].create({'lang': 'ca_ES'})
        installer.lang_install()

    @api.model
    def disable_company_noupdate(self):
        company_imd = self.env['ir.model.data'].search([
            ('name', '=', 'main_company')
        ])
        company_imd.noupdate = False

    @api.model
    def clean_demo_data(self):
        account_invoice_ids = [
            imd.res_id
            for imd in
            self.env['ir.model.data'].search([
                ('model', '=', 'account.invoice'),
                ('module', '=', 'l10n_generic_coa')
            ])
        ]
        bank_statement_ids = [
            imd.res_id
            for imd in
            self.env['ir.model.data'].search([
                ('model', '=', 'account.bank.statement'),
                ('module', '=', 'l10n_generic_coa')
            ])
        ]
        account_invoices = self.env['account.invoice'].search(
            [('id', 'in', account_invoice_ids)]
        )
        bank_statements = self.env['account.bank.statement'].search(
            [('id', 'in', bank_statement_ids)]
        )
        if account_invoices or bank_statements:
            self.env.cr.execute('DELETE FROM account_move_line')
            self.env.cr.execute(
                'DELETE FROM account_invoice WHERE id IN %s',
                (tuple(account_invoices.mapped('id')),)
            )
            self.env.cr.execute(
                'DELETE FROM account_bank_statement WHERE id IN %s',
                (tuple(bank_statements.mapped('id')),)
            )
