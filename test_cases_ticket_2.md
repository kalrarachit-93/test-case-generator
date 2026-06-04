# Test Cases for Ticket #2

TEST CASES
==========

1. [POSITIVE] Logged-in user adds product from detail page successfully
   Steps:
     1. Log in as a valid customer.
     2. Navigate to a product detail page for an in-stock product (e.g., "Blue T-Shirt").
     3. Click the "Add to Cart" button.
   Expected: The product is added to the cart, and a confirmation message (e.g., "Item added to your cart") is displayed on screen.

2. [POSITIVE] Adding same product twice increments quantity to 2
   Steps:
     1. Log in as a valid customer with an empty cart.
     2. Open the product detail page for "Blue T-Shirt" and click "Add to Cart".
     3. Click "Add to Cart" a second time on the same product page.
     4. Open the shopping cart.
   Expected: The cart contains exactly one line item for "Blue T-Shirt" with quantity = 2 (not two separate line items).

3. [NEGATIVE] Guest user is prompted to log in or continue as guest when adding to cart
   Steps:
     1. Ensure no user is logged in (clear session/cookies).
     2. Navigate to an in-stock product detail page.
     3. Click "Add to Cart".
   Expected: A modal/prompt appears offering "Log in" and "Continue as guest" options. The item is NOT added to any cart until the user chooses one of the options.

4. [POSITIVE] Guest who chooses "Continue as guest" has item added to cart
   Steps:
     1. As a non-logged-in user, click "Add to Cart" on an in-stock product.
     2. In the prompt, select "Continue as guest".
   Expected: The prompt closes, the item is added to the guest cart, and a confirmation message is shown.

5. [NEGATIVE] Out-of-stock product disables Add to Cart button and shows label
   Steps:
     1. Log in (or browse as guest).
     2. Navigate to a product detail page for a product with stock = 0.
   Expected: The "Add to Cart" button is visibly disabled (greyed out, not clickable) and displays/accompanies an "Out of stock" label.

6. [NEGATIVE] Out-of-stock Add to Cart button cannot be triggered via keyboard/click
   Steps:
     1. Open the detail page of an out-of-stock product.
     2. Attempt to click the disabled "Add to Cart" button.
     3. Attempt to focus it via Tab key and press Enter/Space.
   Expected: No add-to-cart action occurs, no network request is sent, no confirmation appears, and the cart count remains unchanged.

7. [POSITIVE] Cart icon updates within 2 seconds after adding an item
   Steps:
     1. Log in as a user with an empty cart (header cart icon shows 0).
     2. Open a product detail page and click "Add to Cart".
     3. Start a stopwatch at the moment of click and observe the header cart icon.
   Expected: Within 2 seconds, the cart icon updates from 0 to 1 without requiring a page refresh.

8. [POSITIVE] Cart icon updates within 2 seconds after removing an item
   Steps:
     1. Log in as a user whose cart contains 1 item (header shows 1).
     2. Open the cart and remove the item.
     3. Observe the header cart icon and start a stopwatch.
   Expected: Within 2 seconds, the cart icon updates from 1 to 0.

9. [POSITIVE] Adding 10 units of a product succeeds at the boundary
   Steps:
     1. Log in as a customer with an empty cart.
     2. On an in-stock product page, click "Add to Cart" 10 times (or set quantity to 10 if a selector exists).
     3. Open the cart.
   Expected: The cart shows the product with quantity exactly 10. No error is shown. Cart icon reflects total of 10.

10. [NEGATIVE] Attempting to add an 11th unit shows max-quantity error message
    Steps:
      1. Log in and add 10 units of a product to the cart (as in test 9).
      2. Return to the product detail page and click "Add to Cart" once more (attempting the 11th unit).
    Expected: An error message is shown (e.g., "Maximum quantity per product is 10"). The cart still shows quantity 10 for that product; it is not increased to 11.

11. [NEGATIVE] Confirmation message does not appear when add-to-cart request fails
    Steps:
      1. Log in as a customer.
      2. Simulate a backend failure for the add-to-cart endpoint (e.g., via network throttling/500 response).
      3. Click "Add to Cart" on an in-stock product.
    Expected: No success confirmation appears. An appropriate error message is shown, the item is not added to the cart, and the cart icon count remains unchanged.