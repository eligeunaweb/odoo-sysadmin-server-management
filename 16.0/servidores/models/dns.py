# -*- coding: utf-8 -*-
import ipaddress
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_FQDN_RE = re.compile(r"^(?=.{1,253}$)(?!-)([A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,63}\.?$")

class SysadminDnsRecord(models.Model):
    _name = "sysadmin.dns.record"
    _description = "Registro DNS"
    _order = "zone_id, name, record_type"

    partner_id = fields.Many2one("res.partner", string="Cliente", required=True, index=True)
    responsible_user_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user)
    zone_id = fields.Many2one("sysadmin.dns.zone", string="Zona/Dominio", required=True, index=True)
    server_id = fields.Many2one("sysadmin.server", string="Servidor", ondelete="set null", index=True)

    name = fields.Char(string="Nombre", required=True, help="Ej: @, www, api, mail")
    record_type = fields.Selection(
        selection=[
            ("A", "A"),
            ("AAAA", "AAAA"),
            ("CNAME", "CNAME"),
            ("MX", "MX"),
            ("TXT", "TXT"),
            ("SRV", "SRV"),
            ("NS", "NS"),
            ("CAA", "CAA"),
        ],
        string="Tipo",
        required=True,
        default="A",
    )
    value = fields.Char(string="Valor", required=True, help="IP/host/valor según el tipo")
    ttl = fields.Integer(string="TTL", default=3600)
    priority = fields.Integer(string="Prioridad (MX/SRV)")
    weight = fields.Integer(string="Peso (SRV)")
    port = fields.Integer(string="Puerto (SRV)")
    comment = fields.Char(string="Comentario")

    _sql_constraints = [
        ("uniq_record", "unique(zone_id, name, record_type, value)", "Este registro ya existe en la zona."),
    ]

    @api.constrains("ttl")
    def _check_ttl(self):
        for rec in self:
            if rec.ttl is not None and rec.ttl < 0:
                raise ValidationError(_("TTL no puede ser negativo."))

    @api.constrains("record_type", "value", "priority", "port")
    def _check_value_by_type(self):
        for rec in self:
            v = (rec.value or "").strip()
            if not v:
                continue

            if rec.record_type == "A":
                try:
                    ip = ipaddress.ip_address(v)
                    if ip.version != 4:
                        raise ValueError()
                except Exception:
                    raise ValidationError(_("Un registro A debe tener una IPv4 válida."))

            if rec.record_type == "AAAA":
                try:
                    ip = ipaddress.ip_address(v)
                    if ip.version != 6:
                        raise ValueError()
                except Exception:
                    raise ValidationError(_("Un registro AAAA debe tener una IPv6 válida."))

            if rec.record_type in ("CNAME", "MX", "NS", "SRV"):
                # Permitimos FQDN o nombres relativos sin espacios (p.ej. 'mail' o 'mail.ejemplo.com')
                if " " in v:
                    raise ValidationError(_("El valor no puede contener espacios."))
                if "." in v and not _FQDN_RE.match(v if v.endswith(".") else v + "."):
                    raise ValidationError(_("El valor parece un FQDN inválido."))

            if rec.record_type == "MX" and rec.priority is None:
                raise ValidationError(_("MX requiere 'Prioridad'."))

            if rec.record_type == "SRV":
                if rec.priority is None or rec.port is None:
                    raise ValidationError(_("SRV requiere 'Prioridad' y 'Puerto'."))

    @api.onchange("zone_id")
    def _onchange_zone(self):
        for rec in self:
            if rec.zone_id:
                rec.partner_id = rec.zone_id.partner_id
                if not rec.responsible_user_id:
                    rec.responsible_user_id = rec.zone_id.responsible_user_id

    @api.onchange("server_id")
    def _onchange_server(self):
        for rec in self:
            if rec.server_id:
                rec.partner_id = rec.server_id.partner_id
                rec.responsible_user_id = rec.server_id.responsible_user_id
                # si ya hay zona del mismo cliente, no tocamos; si no, intentamos autoasignar 1ra zona del cliente
                if not rec.zone_id:
                    zone = self.env["sysadmin.dns.zone"].search([("partner_id", "=", rec.partner_id.id)], limit=1)
                    rec.zone_id = zone
