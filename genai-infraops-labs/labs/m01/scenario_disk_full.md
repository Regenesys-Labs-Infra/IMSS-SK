# Scenario: "Server slow / disk full" (synthetic)

## Ticket INC0010231
Caller: Finance - Ravi K. | Channel: email | Opened: 09:03 IST
"Portal very slow since morning, sometimes disk full error shown, pls fix urgent!!"

## Monitoring alert
alertname=DiskSpaceLow instance=srv-fin-app-02 mount=/var value=96% severity=critical (fired 08:58 IST)

## df -h (collected by L1 via read-only access)
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        30G   14G   15G  49% /
/dev/sdb1        50G   48G  2.1G  96% /var
tmpfs           3.9G     0  3.9G   0% /dev/shm
```

## systemctl status finapp (excerpt)
```
finapp.service - Finance Reporting App
   Active: active (running) since Mon 2026-11-09 07:02:11 IST
   ... WARN write to /var/log/finapp/report.log failed: No space left on device
```

## Known facts
- CI srv-fin-app-02 belongs to Finance Reporting, support group LINUX-L2 (see data/cmdb/ci_inventory.csv)
- No change was recorded in the last 24 hours
