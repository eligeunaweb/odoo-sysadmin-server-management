# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")

class SysadminServer(models.Model):
    _name = "sysadmin.server"
    _description = "Servidor"
    _inherit = ["mail.thread", "mail.activity.mixin", "image.mixin"]
    _order = "create_date desc, id desc"

    name = fields.Char(string="Nombre", required=True, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", required=True, index=True, tracking=True)
    responsible_user_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user, tracking=True)

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("draft", "Borrador"), ("active", "Activo"), ("inactive", "Inactivo")],
        default="draft",
        tracking=True,
        copy=False,
    )

    location = fields.Char(string="Localización")
    description = fields.Text(string="Descripción")
    keycloak_client = fields.Char(string="Keycloak Client")
    keycloak_secret = fields.Char(string="Keycloak Secret")

    motherboard = fields.Char(string="Placa base")
    cpu = fields.Char(string="CPU")
    ram_gb = fields.Float(string="RAM (GB)")
    storage_type = fields.Selection(
        selection=[("hdd", "HDD"), ("ssd", "SSD"), ("nvme", "NVMe"), ("other", "Otro")],
        string="Tipo de disco",
    )
    storage_size_gb = fields.Float(string="Disco (GB)")

    interface_ids = fields.One2many("sysadmin.server.interface", "server_id", string="Interfaces")
    dns_record_ids = fields.One2many("sysadmin.dns.record", "server_id", string="DNS (del servidor)")

    def action_activate(self):
        self.write({"state": "active"})

    def action_deactivate(self):
        self.write({"state": "inactive"})


class SysadminServerInterface(models.Model):
    _name = "sysadmin.server.interface"
    _description = "Interfaz de red"

    server_id = fields.Many2one("sysadmin.server", string="Servidor", required=True, ondelete="cascade", index=True)
    name = fields.Char(string="Nombre (NIC)", required=True, help="Ej: eth0, ens18, bond0, vlan10")
    mac = fields.Char(string="MAC")
    ipv4 = fields.Char(string="IPv4")
    ipv6 = fields.Char(string="IPv6")
    dns_name = fields.Char(string="Hostname/FQDN")
    connected_to = fields.Char(string="Conectado a")
    port = fields.Char(string="Puerto")
    notes = fields.Char(string="Notas")

    _sql_constraints = [
        ("uniq_mac_per_server", "unique(server_id, mac)", "La MAC debe ser única dentro del servidor."),
    ]

    @api.constrains("mac")
    def _check_mac(self):
        for rec in self:
            if rec.mac and not _MAC_RE.match(rec.mac.strip()):
                raise ValidationError(_("Formato de MAC inválido. Usa XX:XX:XX:XX:XX:XX"))
