# Lab 4.1 workspace - Ansible
The playbook installs nginx, disables server version tokens, adds security
headers, and enables and starts the service. Run it with `--check` first:

```bash
ansible-playbook -i localhost, -c local --check harden_nginx.yml
```

Privilege escalation is required. If nginx is not installed, check mode cannot
create its configuration directory or service; it reports and skips those tasks.
The security headers apply at the nginx HTTP level; server or location blocks
that define their own `add_header` directives can override them.
