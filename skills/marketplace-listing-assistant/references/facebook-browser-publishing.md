# Facebook Marketplace Browser Publishing

Read this reference only when creating or publishing a Facebook Marketplace listing through browser computer control. Facebook changes its interface regularly, so derive element targets from fresh visible state rather than relying on stored indexes.

## Reach the Form Reliably

- Prefer the user's existing signed-in browser session and open `https://www.facebook.com/marketplace/create/item` in a fresh task tab.
- If a browser connector is temporarily unavailable but native browser application control is available, continue through the existing browser app rather than declaring the session logged out. Verify the Facebook profile identity and listing form are visibly present.
- Treat the platform's displayed category names as authoritative. Record the exact selected label in the saved listing bundle when it differs from a drafted category path.

## Populate and Upload

- Fill the finalized title, price, category, condition, description, brand, location, and applicable availability or meetup fields. Leave paid boosts, friend-hiding, delivery, and cross-posting options unchanged unless the user requested them.
- Upload only the specific photos authorized for this item. Preserve the intended order: hero image first, then model/proof, accessories, and flaw close-ups.
- Prefer a direct file chooser API when available. In a native macOS file chooser, select the known folder and file from visible state; if reliable multi-select is unavailable, upload one file at a time in final display order. Verify the visible attachment count and that loading completes before advancing.
- When the user supplies a material fact after the form is prepared—such as included accessories—return to the details step, update both the live form and the saved listing bundle, then review again.

## Review and Publish

- Facebook's preview may display phrases such as “Listed a few seconds ago” before publication. This is simulated preview text and is not proof that a listing exists.
- On the final audience step, verify the photos, title, price, Toronto or other intended pickup area, public-meetup preference, condition, brand, and description. Avoid selecting extra groups unless requested.
- Always obtain action-time confirmation immediately before pressing **Publish**, as required for representational communication.

## Verify the Result

- After clicking Publish, wait until Facebook leaves the composer and shows the selling dashboard or listing detail state. A disabled Publish button or “Publishing your listing” message is only an intermediate state.
- On the selling dashboard, an item may be labeled both `Active` and `This listing is being reviewed.` Report both facts: the submission succeeded, but visibility to other users is pending standard review.
- Open the new listing's detail panel or link to capture its canonical URL in the form `https://www.facebook.com/marketplace/item/<listing-id>/`.
- Update local records to `Listed` only after the selling dashboard or detail panel identifies the item, price, and status. Store the canonical URL and the exact review state.
