# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SysadminDnsZone(models.Model):
    _name = "sysadmin.dns.zone"
    _description = "Zona DNS"
    _order = "name"

    name = fields.Char(string="Dominio/Zona", required=True, index=True, help="Ej: ejemplo.com")
    partner_id = fields.Many2one("res.partner", string="Cliente", required=True, index=True)
    responsible_user_id = fields.Many2one(
        "res.users", string="Responsable", default=lambda self: self.env.user, tracking=False
    )
    note = fields.Char(string="Notas")

    record_ids = fields.One2many("sysadmin.dns.record", "zone_id", string="Registros")

    _sql_constraints = [
        ("uniq_zone_per_partner", "unique(partner_id, name)", "La zona debe ser única por cliente."),
    ]

    @api.constrains("name")
    def _check_zone_name(self):
        for rec in self:
            if rec.name and " " in rec.name.strip():
                raise ValidationError(_("El nombre de la zona no puede contener espacios."))
