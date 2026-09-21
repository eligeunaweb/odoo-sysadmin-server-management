# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    sysadmin_server_count = fields.Integer(compute="_compute_sysadmin_counts", string="Servidores")
    sysadmin_dns_count = fields.Integer(compute="_compute_sysadmin_counts", string="DNS")
    sysadmin_zone_count = fields.Integer(compute="_compute_sysadmin_counts", string="Zonas DNS")

    def _compute_sysadmin_counts(self):
        Server = self.env["sysadmin.server"]
        Dns = self.env["sysadmin.dns.record"]
        Zone = self.env["sysadmin.dns.zone"]
        for partner in self:
            partner.sysadmin_server_count = Server.search_count([("partner_id", "=", partner.id)])
            partner.sysadmin_dns_count = Dns.search_count([("partner_id", "=", partner.id)])
            partner.sysadmin_zone_count = Zone.search_count([("partner_id", "=", partner.id)])

    def action_view_sysadmin_servers(self):
        self.ensure_one()
        action = self.env.ref("servidores.action_sysadmin_server").read()[0]
        action["domain"] = [("partner_id", "=", self.id)]
        action["context"] = dict(self.env.context, default_partner_id=self.id)
        return action

    def action_view_sysadmin_dns(self):
        self.ensure_one()
        action = self.env.ref("servidores.action_sysadmin_dns_record").read()[0]
        action["domain"] = [("partner_id", "=", self.id)]
        action["context"] = dict(self.env.context, default_partner_id=self.id)
        return action

    def action_view_sysadmin_zones(self):
        self.ensure_one()
        action = self.env.ref("servidores.action_sysadmin_dns_zone").read()[0]
        action["domain"] = [("partner_id", "=", self.id)]
        action["context"] = dict(self.env.context, default_partner_id=self.id)
        return action
