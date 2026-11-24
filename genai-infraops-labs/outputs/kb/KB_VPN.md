## Title
VPN connection failures and repeated disconnects

## Symptoms (user's words)
- “Cannot connect to VPN” or authentication failure.
- “VPN disconnects every few minutes.”

## Applies to
VPN tickets in the supplied history. The history includes VPN client 5.2.1 and a
client 5.3 MTU issue; applicability to other versions is [VERIFY].

## Cause
- Some connection failures were resolved after a password-expiry reset through the
  self-service portal.
- Repeated disconnect tickets record a known client 5.3 MTU issue. Do not assume this
  explains every VPN failure.

## Resolution steps (L1)
1. For an authentication failure, [VERIFY] use the approved process to check whether the
   password has expired. If it has, guide the user to the self-service reset portal and
   have them reconnect; this outcome is recorded in source tickets
   INC0008021, INC0008027, and INC0008031.
2. For repeated disconnects matching the recorded client issue, the tickets report
   reinstalling VPN client 5.2.1, clearing the cached profile, and reconnecting to
   `vpn-gw-pune-01` (INC0008006, INC0008029). Follow the approved client procedure;
   detailed steps and applicability are [VERIFY].
3. A client 5.3 MTU issue was resolved by setting MTU 1350 (INC0008006). This changes
   network configuration; do not perform it as an L1 action without the approved
   Network procedure and authorisation [VERIFY].

## Escalate when
Escalate unresolved VPN issues to NETWORK-L2, the group recorded on the source tickets.
The history does not define a retry count or other threshold; confirm the current
escalation procedure [VERIFY].

## Keywords
VPN, authentication failed, password expired, disconnect, client 5.2.1, client 5.3,
MTU, cached profile

## Source tickets
- Password expiry pattern: INC0008021, INC0008027, INC0008031, INC0008050, INC0008064,
  INC0008097, INC0008109, INC0008153, INC0008175.
- Repeated disconnect pattern: INC0008006, INC0008029, INC0008030, INC0008036,
  INC0008037, INC0008040, INC0008045, INC0008067, INC0008069, INC0008079, INC0008083,
  INC0008096, INC0008102, INC0008111, INC0008116, INC0008130, INC0008149, INC0008150,
  INC0008151, INC0008154, INC0008155, INC0008168, INC0008179, INC0008193.
