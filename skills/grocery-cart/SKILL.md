---
name: grocery-cart
description: Compare grocery deals, use authorized purchase history to infer suitable staples, and build a reviewable cart in a signed-in grocery delivery service. Use for grocery lists, unit-price comparisons, and coupon-aware basket preparation; checkout remains a separate user action unless explicitly authorized.
---

# Grocery Cart

Prepare the requested groceries at a sensible total cost. Preserve the user's chosen service, store, quantities, dietary requirements, and checkout boundary. Infer modest quantities when missing and state material assumptions.

## Choose a store or recreate a cart

When the user asks for coupon-based store selection, compare current eligible offers alongside grocery prices, delivery fees, membership savings, and availability. A higher percentage alone does not establish the cheapest complete order. Confirm the destination and branch from the signed-in UI. Check that the store accepts the requested delivery time before building a substantial cart: a storefront arrival estimate can still lead to checkout with Standard unavailable and only a future scheduled slot. If necessary, inspect checkout with an initial needed item; do not choose a different delivery date without authorization.

When moving to another service or store, reread the source cart immediately before copying. The user's latest cart edits supersede earlier lists, including added items, removed items, variants, and quantities. Preserve the source cart. Ask only about material ambiguity, then build the requested current basket at the next eligible available store and verify its actual total.

## Select groceries

- Read existing carts before adding anything. Preserve unrelated carts and count existing requested items toward the list.
- When authorized, inspect a relevant recent grocery order for preferred milk type, bread, brands, pack sizes, and delivered substitutions. History suggests preferences, not current pantry inventory or permission to add unrelated products.
- Compare current in-app prices for equivalent products using price per kg, litre, or item. A sale badge alone does not establish value. Prefer reasonable quantities over bulk packs that risk waste. Record the chosen sale prices and displayed reference prices so the handoff can distinguish item-sale savings from coupon savings.
- Search narrowly for exact variants before treating a broad search omission as unavailability; try brand plus distinguishing terms such as plain, zero sugar, or package size. When title weights conflict with pack counts, inspect product details and the packaging photo. Distinguish per-portion weight from total pack weight; state any unresolved discrepancy.
- When an exact item is unavailable, preserve product type and a sensible total quantity across pack formats; disclose material changes in brand, size, preparation, or price. Do not silently equate half-and-half with whipping cream.
- Preserve product meaning: fresh coriander is cilantro, not ground spice; butter is not automatically margarine; a cheese block is not slices. Check ambiguous variants and replacement settings.
- Review substitutions against the user's budget as well as product meaning. If they prefer keeping needed items over automatic refunds, retain suitable substitutions; use comparable-price approved alternatives or shopper notes when available. Keep shopper notes focused on product, size, and replacement-price instructions; basket targets, coupon thresholds, and discount calculations belong in the user-facing planning, not shopper notes. Distinguish an enforceable price cap from a note requesting approval for expensive replacements. Do not invent a numeric premium limit or switch everything to refund by default. Verify that live-order edits are saved, not only present in a draft.
- Suggest history-based extras separately unless the user authorized filling out the basket with staples.

## Coupon arithmetic

Read current offer terms: eligible store and items, delivery/pickup restriction, minimum eligible subtotal, percentage, discount cap, expiry with displayed timezone, exclusions, and stacking restrictions. Treat offer availability as separate from application.

For percentage rate r and cap C, the eligible subtotal that reaches the cap is C/r. Check that this also meets the minimum. For example, 40% capped at $20 reaches its cap at $50 of eligible groceries. Use the service's qualifying subtotal; sale items, fees, taxes, and tips may be excluded. Do not invent eligibility or assume sale discounts stack.

Prioritize needed groceries. Spend beyond the cap only for actual needs; do not add wasteful filler to maximize a coupon. Show the incremental cost and discount when recommending a top-up. A gift card is payment, not an additional merchandise discount.

## Build and verify

Use the available signed-in browser and its supported computer-use interface. Search in small batches if large list searches make the service slow. Derive fresh controls after each navigation or modal transition. With native controls, bring the target into view before clicking: an off-screen accessibility entry can hit another visible control. After adding, wait for the resulting state and any cart toast to settle before entering the next search; verify the new query results rather than assuming Return submitted it.

An add click is not proof of addition. Verify the basket line, quantity, and price. If an action remains pending, inspect the cart before retrying to avoid duplicates. After a failed normal attempt and one reasonable recovery, pause writes if cart state remains uncertain; record the exact blocker and verified progress.

Finish by checking every requested item, quantities, substitutions, duplicates, item subtotal, and offer eligibility. Report unavailable or unresolved items explicitly. Replacement settings and shopper notes do not automatically transfer across services; verify saved controls where exposed and report any limitation rather than claiming they were copied. Save a screenshot of the verified basket using the computer-use screenshot workflow.

Leave coupon entry/application, gift-card redemption, and payment to the user when requested. Never claim checkout or a discount succeeded without visible confirmation. When authorized to inspect checkout, check whether a saved offer applied automatically before entering or selecting another coupon; the checkout discount is authoritative over a storefront banner or cart progress message. Preserve existing delivery and tip choices unless the user requests changes. Recheck the displayed tip after basket changes because a retained percentage can recalculate its amount.

Separate merchandise sale prices, multi-buy discounts, coupon savings, and membership fee savings. If checkout groups discounts, use observed line amounts to explain the components and label inferred arithmetic; do not count the same saving twice. Do not carry a previous coupon code, expiry, minimum, cap, or store eligibility into a new order without checking current terms.

Hand off with the cart, selected deals, qualifying subtotal, expected discount (clearly provisional until applied), and remaining steps. When checkout is visible, report the applied discount, delivery fee, combined or separately displayed taxes/fees, current tip, total before tip, and final estimated total before any gift-card payment. Identify a tip calculated from a pre-discount amount when the UI says so. Do not describe the pre-tip total as the final payable total. Save a screenshot of the verified checkout breakdown and leave the page open for the user.
