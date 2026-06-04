# Test Cases for Ticket #1

TEST CASES
==========

1. [POSITIVE] Forgot Password link navigates to reset request form
   Steps:
     1. Navigate to the login page.
     2. Click the "Forgot Password" link.
   Expected: The user is taken to a password reset request form containing an email input field and a submit button.

2. [NEGATIVE] Submit malformed email on reset request form
   Steps:
     1. Navigate to the password reset request form.
     2. Enter a malformed email such as "notanemail" or "user@".
     3. Click submit.
   Expected: The form displays an inline validation error indicating the email format is invalid; no reset email is sent.

3. [POSITIVE] Reset email delivered within 2 minutes for registered email
   Steps:
     1. Navigate to the password reset request form.
     2. Enter a valid, registered email address (e.g., testuser@example.com).
     3. Click submit and start a timer.
     4. Check the inbox of the registered email.
   Expected: A password reset email containing a reset link arrives within 2 minutes.

4. [NEGATIVE] Generic response shown for unregistered email
   Steps:
     1. Navigate to the password reset request form.
     2. Enter a well-formed but unregistered email (e.g., nobody-xyz@example.com).
     3. Click submit.
   Expected: A generic confirmation message is shown (e.g., "If an account exists for this email, a reset link has been sent.") — identical to the message shown for a registered email. No information leaks about account existence, and no email is sent.

5. [POSITIVE] Valid reset link within 1 hour opens set-new-password form
   Steps:
     1. Request a password reset for a registered account.
     2. Open the reset email within 1 hour of receipt.
     3. Click the reset link.
   Expected: The user is taken to a "Set New Password" form with fields for new password and confirm password.

6. [NEGATIVE] Expired reset link shows error and prompt to request new link
   Steps:
     1. Request a password reset for a registered account.
     2. Wait at least 1 hour and 1 minute (or manually expire the token in the DB).
     3. Click the reset link in the email.
   Expected: The user sees a clear error message such as "This reset link has expired" and is shown a link or button to request a new reset email. The "Set New Password" form is not accessible.

7. [NEGATIVE] Reset link cannot be reused after successful password reset
   Steps:
     1. Request a password reset and click the link within 1 hour.
     2. Successfully set a new valid password and submit.
     3. Return to the original reset email and click the same link again.
   Expected: The link is rejected with a clear message such as "This link has already been used" and the set-new-password form is not displayed.

8. [NEGATIVE] Tampered or invalid reset token is rejected
   Steps:
     1. Obtain a valid reset link from an email.
     2. Modify one or more characters of the token in the URL.
     3. Open the modified URL in the browser.
   Expected: The application rejects the link with an "invalid or expired link" error message and prompts the user to request a new reset.

9. [POSITIVE] New password meeting all security requirements is accepted
   Steps:
     1. Open a valid reset link to access the set-new-password form.
     2. Enter a new password that is at least 8 characters and includes at least one uppercase letter, one lowercase letter, and one digit (e.g., "Passw0rd").
     3. Confirm the same password and submit.
   Expected: The password is accepted, the user sees a success confirmation, and can subsequently log in with the new password.

10. [NEGATIVE] New password shorter than 8 characters is rejected
    Steps:
      1. Open a valid reset link to access the set-new-password form.
      2. Enter a password of fewer than 8 characters that otherwise has upper, lower, and digit (e.g., "Ab1cdef").
      3. Submit the form.
    Expected: The form rejects submission with a clear message indicating the password must be at least 8 characters. Password is not changed.

11. [NEGATIVE] New password missing uppercase letter is rejected
    Steps:
      1. Open a valid reset link to access the set-new-password form.
      2. Enter a password with no uppercase letters (e.g., "password1").
      3. Submit the form.
    Expected: The form rejects submission with a clear message indicating at least one uppercase letter is required. Password is not changed.

12. [NEGATIVE] New password missing lowercase letter is rejected
    Steps:
      1. Open a valid reset link to access the set-new-password form.
      2. Enter a password with no lowercase letters (e.g., "PASSWORD1").
      3. Submit the form.
    Expected: The form rejects submission with a clear message indicating at least one lowercase letter is required. Password is not changed.

13. [NEGATIVE] New password missing digit is rejected
    Steps:
      1. Open a valid reset link to access the set-new-password form.
      2. Enter a password with no digits (e.g., "Passwordd").
      3. Submit the form.
    Expected: The form rejects submission with a clear message indicating at least one digit is required. Password is not changed.