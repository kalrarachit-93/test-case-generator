"""
Sample Jira-style ticket used as input to the test case generator agent.

This is a realistic example. In a future version of this project, the agent 
would accept tickets via file upload, an API integration, or pasted text.
For now we use this fixture so the development loop is fast and reproducible.
"""

SAMPLE_TICKET = """
TICKET-1042: User can reset password via email

DESCRIPTION:
Users who have forgotten their password should be able to request a reset 
link via their registered email address. The reset link should be sent to 
the user's email and allow them to set a new password. This feature is 
critical for account recovery and reducing support tickets.

ACCEPTANCE CRITERIA:
- Given a user is on the login page, when they click "Forgot Password", 
  then they are taken to a password reset request form.
- Given a user enters a valid registered email address, when they submit 
  the form, then they receive a password reset email within 2 minutes.
- Given a user enters an unregistered email address, when they submit 
  the form, then they see a generic message that does not reveal whether 
  the email is registered.
- Given a user receives a reset link, when they click it within 1 hour, 
  then they are taken to a "set new password" form.
- Given a user clicks an expired reset link (after 1 hour), then they see 
  a clear error message and are prompted to request a new link.
- A reset link can only be used once. After successful password reset, 
  the same link must no longer work.
- The new password must meet security requirements: minimum 8 characters, 
  at least one uppercase letter, one lowercase letter, one digit.

PRIORITY: High
COMPONENT: Authentication
REPORTER: jane.doe@example.com
ASSIGNEE: dev-team-alpha
"""

SAMPLE_TICKET_2 = """
TICKET-2087: Add product to shopping cart

DESCRIPTION:
Customers browsing the product catalog should be able to add items to their 
shopping cart. The cart icon in the header should reflect the current number 
of items. This feature is foundational for the checkout flow.

ACCEPTANCE CRITERIA:
- Given a logged-in user views a product detail page, when they click 
  "Add to Cart", then the product is added and a confirmation message appears.
- Given a logged-in user adds the same product twice, then the cart shows 
  the product with quantity 2, not as two separate line items.
- Given a guest (non-logged-in) user clicks "Add to Cart", then they are 
  prompted to log in or continue as guest before the item is added.
- Given a user views an out-of-stock product, then the "Add to Cart" button 
  is disabled and shows an "Out of stock" label.
- The cart icon in the header must update to show the current item count 
  within 2 seconds of any cart change.
- Maximum quantity per product is 10. Attempting to add more than 10 shows 
  an error message.

PRIORITY: High
COMPONENT: Shopping
REPORTER: pm.team@example.com
ASSIGNEE: dev-team-cart
"""