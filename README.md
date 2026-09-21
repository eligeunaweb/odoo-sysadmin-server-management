# Odoo SysAdmin — Server & DNS Management

Free Odoo Community module for documenting and managing server infrastructure by customer.

## Supported versions

- Odoo 15 — module version 15.0.1.1.0
- Odoo 16 — module version 16.0.1.1.0

## Features

- Server inventory linked to Odoo Contacts
- Responsible user and server lifecycle status
- Hardware information: motherboard, CPU, RAM and storage
- Network interfaces with MAC, IPv4, IPv6, hostname, port and connection details
- DNS zones and records
- A, AAAA, CNAME, MX, TXT, SRV, NS and CAA records
- Validation for MAC addresses, IP addresses, TTL and DNS values
- Customer-level counters and shortcuts for servers, DNS records and zones
- Odoo chatter and activities on server records
- Access-control and security rules

## Keycloak fields

The module includes optional `keycloak_client` and `keycloak_secret` fields as infrastructure metadata fields. No credentials or customer data are included in this repository.

## Repository structure

```text
15.0/servidores/   Odoo 15 edition
16.0/servidores/   Odoo 16 edition
```

## Installation

Copy the `servidores` directory for your Odoo version into your custom addons path, restart Odoo, update the Apps list and install **Sys Admin - Servidores y DNS**.

## Dependencies

- Contacts
- Discuss / Mail

## License

LGPL-3, as declared by both module manifests.

## Author

**Alvaro Martinez**  
[AdaptaTuWeb](https://www.adaptatuweb.com) · [GitHub](https://github.com/eligeunaweb)

This is one of my free Odoo modules. Commercial modules are maintained separately and are not published in this repository.
