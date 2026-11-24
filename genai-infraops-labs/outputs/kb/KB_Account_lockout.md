## Title
Account lockout caused by stale mobile mail credentials

## Symptoms (user's words)
“Account locked out” or the account “locked repeatedly.”

## Applies to
Account-lockout incidents in the supplied ticket history. The notes specifically
describe stale credentials in a mobile mail app.

## Cause
The resolved tickets attribute the repeated lockout to stale credentials on a mobile
mail app.

## Resolution steps (L1)
1. Check for stale credentials in the mobile mail app using the approved support
   procedure; the exact diagnostic steps are [VERIFY] (INC0008005, INC0008011).
2. Guide the user to remove the old account from the mobile mail app using the approved
   client instructions; the tickets record this action but do not provide its exact
   steps [VERIFY] (INC0008005, INC0008011).
3. Have an authorised AD operator unlock the account under the current identity and
   access policy [VERIFY]. The source tickets record an AD unlock but do not document
   the approval or verification procedure (INC0008005, INC0008011).

## Escalate when
The source tickets were assigned to WINTEL-L2. Escalate there if the approved L1 steps
do not resolve the lockout; the history does not define a retry threshold [VERIFY].

## Keywords
Account lockout, stale credentials, mobile mail app, AD unlock

## Source tickets
INC0008005, INC0008011, INC0008012, INC0008014, INC0008022, INC0008042, INC0008048,
INC0008049, INC0008056, INC0008058, INC0008061, INC0008071, INC0008077, INC0008089,
INC0008091, INC0008120, INC0008131, INC0008136, INC0008138, INC0008144, INC0008146,
INC0008163, INC0008173, INC0008183, INC0008188, INC0008191.
