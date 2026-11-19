# Runbook: VPN disconnects or fails (L1)
1. Ask whether the password has expired; if yes, guide to the self-service reset portal.
2. Check the VPN client version (Help > About). Version 5.3.x has a known MTU issue (Known Error KE0012).
3. For 5.3.x: set MTU 1350 in the client profile, or reinstall 5.2.1 from Software Centre.
4. Clear the cached profile and reconnect to vpn-gw-pune-01.
Escalate to NETWORK-L2 when: more than 3 users at one site are affected, or step 3 does not help.
