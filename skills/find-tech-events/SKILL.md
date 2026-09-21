---
name: find-tech-events
description: Find, compare, and—when explicitly authorized—register for current local or virtual technology events, meetups, workshops, and networking opportunities. Use for AI, data science, software, startup, cybersecurity, product, developer, or practical tech-networking events; location- or postal-code-based searches; event shortlists; and safe RSVP or registration help.
---

# Find and Register for Tech Events

Use this skill for an on-demand event search or for completing a user-approved registration. Do not create recurring automations unless the user separately asks for one.

## Defaults

Infer missing constraints and state them briefly:

- Search 2–6 weeks ahead unless the user gives dates.
- Use the requested postal code or location and roughly a 10 km radius for in-person events.
- Include virtual events.
- Prioritize free or low-cost AI, data science, software, startup, and practical networking events.
- Prefer official organizer pages, then direct event pages on Luma, Meetup, Eventbrite, AICamp, TechTO, GDG, universities, innovation hubs, and incubators.

## Discovery workflow

1. Confirm or infer date window, location, radius, virtual allowance, interests, audience, and cost ceiling.
2. Search current listings; do not rely on prior results or snippets for availability, price, or schedule.
3. Verify promising events from their detail pages. Capture the title, direct link, exact date and time with timezone, format, venue or online platform, organizer, cost, registration requirements, and fit.
4. Estimate distance only when useful, label it approximate, and flag events outside the radius rather than silently including them.
5. Rank free and low-cost options first, then topical fit, practical value, distance, and networking value.
6. Exclude or de-prioritize stale, sold-out, unclear, expensive, application-only, or low-information listings. Keep a short caveat list when a rejected event may still matter.

## Output for discovery

Recommend 2–4 strongest options. For every recommendation include:

- Event name with direct registration link
- Exact date and time with timezone
- Format and location
- Approximate distance when relevant
- Organizer
- Cost, including whether login is required or price is unclear
- Why it fits
- Caveats, availability, eligibility, application, or payment notes

End with the strongest recommendation and a concise action checklist. State that no registration or purchase was performed when operating in discovery-only mode.

## Registration mode

Registration is a separate side-effecting mode. Enter it only when the user explicitly asks to RSVP, register, join a waitlist, apply, or buy a ticket, and identify the exact event(s) and price ceiling.

### Before touching a registration form

1. Re-open the current event page and verify the event, date/time, organizer, venue or online format, price, ticket type, and availability.
2. Show the user a compact registration plan: event, destination, account/login requirement, information to be shared, price and fees, and the final action to be taken.
3. Get explicit approval for the selected event and any paid amount. Do not treat a general request to “find events” as registration approval.
4. Use the available browser or connected app session. Reuse an existing signed-in session; never ask for or store passwords, one-time codes, recovery codes, or payment details.

### What may be done after approval

- Open the event page and navigate to the RSVP or registration flow.
- Fill only already-authorized basic details from the user’s existing profile or details they provide in the current turn.
- Select a free ticket or a specifically approved paid ticket.
- Stop before final submission if the destination, shared data, ticket type, total price, cancellation policy, or consent language differs from the approved plan.
- After submission, verify the confirmation page or confirmation email and report the event, ticket type, order/confirmation reference if visible, and any follow-up required.

### Mandatory stops

Pause and hand control back to the user when any of these occurs:

- Login, CAPTCHA, MFA, email verification, or account creation is required.
- The form asks for new personal, sensitive, employment, demographic, marketing, or profile data not explicitly approved.
- Payment, donation, membership, deposit, or a paid waitlist is required without exact event-and-price approval.
- The event is sold out, application-only, eligibility-restricted, or materially different from the selected listing.
- The site asks for wallet/token verification, browser extensions, downloads, or unusual permissions.
- The confirmation step would send a message, publish a profile, share a resume, or accept broad marketing consent.

Never bypass CAPTCHA, access controls, login protections, payment safeguards, or organizer eligibility requirements.

## Registration handoff

When blocked, provide the direct page, exact field or step needing the user, what information or action is required, and the safe next step. Do not claim registration succeeded without a visible confirmation.

## Quality bar

- Use exact dates and timezone labels, not only relative dates.
- Prefer direct source links and distinguish organizer facts from inference.
- Report conflicts between organizer pages and aggregators instead of choosing silently.
- Treat “free” as potentially requiring login, profile completion, or organizer approval.
- Never RSVP, purchase, join a waitlist, submit a form, or create an account in discovery-only mode.
