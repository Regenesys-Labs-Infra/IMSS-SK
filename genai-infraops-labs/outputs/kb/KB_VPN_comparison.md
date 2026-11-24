# VPN KB comparison

**Sources:** `data/kb/KB0001_vpn_basic.md` and the VPN records in
`data/tickets/tickets_history.csv`.

## Overlaps supported by tickets

- The existing article covers authentication failure and password expiry. The ticket
  history records password reset through the self-service portal followed by a
  successful VPN connection (for example, INC0008021).
- The existing article mentions reinstalling the VPN client. The history records
  reinstalling client 5.2.1 for repeated disconnects (for example, INC0008006).

## Unsupported details

- Restarting the VPN client is not present in the supplied VPN resolution notes.
- Installing from Software Centre is not specified in the notes; the tickets only name
  client version 5.2.1.
- The escalation threshold “more than 3 users at one site” is not supported by the
  supplied VPN tickets.
- The source tickets do not provide detailed client-reinstall or cached-profile
  procedures.

These are unsupported by this ticket set, not proven false. Keep them only if a current
approved VPN procedure independently verifies them.

## Contradictions and recommended disposition

No direct contradiction is established by the ticket history. Keep the self-service
password-reset guidance, with the approved process marked [VERIFY]. Keep client
reinstallation only as the documented client 5.2.1 resolution pattern and require the
approved procedure before use. Mark the restart instruction and site-count threshold
[VERIFY] or remove them pending an authoritative source.

The existing article says it was last reviewed on 2025-02-10; review it against current
VPN documentation before publication. This is a source-ticket audit, not a neighbour
peer review.
