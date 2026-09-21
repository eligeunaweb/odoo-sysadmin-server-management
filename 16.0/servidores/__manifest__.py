# -*- coding: utf-8 -*-
{
    "name": "Sys Admin - Servidores y DNS",
    "version": "16.0.1.1.0",
    "summary": "Gestiona servidores, interfaces de red y registros DNS por cliente",
    "category": "Services/IT",
    "author": "Alvaro Martinez",
    "website": "https://www.adaptatuweb.com",
    "license": "LGPL-3",
    "depends": ["contacts", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/server_views.xml",
        "views/dns_views.xml",
        "views/zone_views.xml",
        "views/partner_views.xml",
        "views/menu.xml",
    ],
    "application": True,
    "installable": True,
}
