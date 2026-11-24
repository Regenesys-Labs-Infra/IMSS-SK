## Title
Mailbox full and Outlook profile loading issues

## Symptoms (user's words)
- “Mailbox full” and unable to send mail.
- Outlook is “stuck loading profile”; source tickets report webmail remained available.

## Applies to
Email mailbox quota and Outlook profile incidents in the supplied ticket history.
Specific mail platform, client versions, and user instructions are [VERIFY].

## Cause
The mailbox-full notes record archiving older mail and enabling the online archive.
The Outlook profile notes do not establish a root cause; they report that webmail worked
while the Outlook profile was recreated and the OST rebuilt.

## Resolution steps (L1)
1. For a full mailbox, guide the user to archive mail older than one year using the
   approved procedure; do not delete mail. This action is recorded in INC0008002 and
   INC0008003.
2. The same tickets record enabling the online archive. Have an authorised email
   administrator perform this only under the approved procedure [VERIFY]
   (INC0008002, INC0008003).
3. Check the resulting quota using the approved mailbox tool [VERIFY]. The resolved
   tickets report quota returning to 60% (INC0008002, INC0008003).
4. For Outlook stuck loading while webmail works, the history records recreating the
   Outlook profile and rebuilding the OST. Use the approved client procedure; its exact
   steps and data safeguards are [VERIFY] (INC0008026, INC0008052).

## Escalate when
Escalation thresholds and support group are not stated in these resolution notes.
Escalate when the approved archive/profile procedure is unavailable or does not resolve
the issue, using the current email support matrix [VERIFY].

## Keywords
Email, mailbox full, archive, online archive, quota, Outlook profile, OST, webmail

## Source tickets
- Mailbox-full pattern: INC0008002, INC0008003, INC0008009, INC0008013, INC0008028,
  INC0008035, INC0008043, INC0008055, INC0008060, INC0008062, INC0008098, INC0008128,
  INC0008140, INC0008141, INC0008156, INC0008198.
- Outlook-profile pattern: INC0008026, INC0008052, INC0008059, INC0008087, INC0008093,
  INC0008095, INC0008113, INC0008115, INC0008125, INC0008126, INC0008132, INC0008133,
  INC0008134, INC0008135, INC0008142, INC0008152, INC0008165, INC0008172, INC0008184,
  INC0008199.
