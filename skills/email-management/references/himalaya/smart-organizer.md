# Smart Inbox Organizer — Full Reference

Rules-based Python-driven workflow to intelligently sort a Himalaya-managed inbox based on subject keywords and sender domains.

## Workflow

1. **Security Exclusion**: Always check for security-related keywords (OTP, verification, login alerts) first to ensure critical security emails are never moved.
2. **Rule Definition**: Define a categorization function that checks both `subject` and `from` address.
3. **Robust JSON Parsing**: Use regex to extract JSON array and `strict=False` for control characters.
4. **Page-at-a-Time Processing**: For large inboxes, process page ranges (~30 pages per turn) to stay within 50 tool-call budget. Do NOT try to fetch all pages at once.
5. **Batch Processing**: Move message IDs in chunks (25 at a time) to stay within tool-call budget per page.

## Category Mapping

| Category | Keywords/Senders | Target Folder |
|----------|-----------------|---------------|
| **Finance/Banking** | Bank domains, credit cards, insurance, payment processors | Finance/Banking |
| **Finance/Orders** | Receipts, order confirmations, shipping, e-statements | Finance/Orders |
| **Finance/Investments** | Wealthsimple, Borrowell, Questrade, Fanduel, Shakepay | Finance/Investments |
| **Finance/Crypto** | Crypto exchanges (Coinbase, Binance, Kraken, Shakepay, Zebpay) | Finance/Crypto |
| **Finance/Tax** | CRA, tax slips, assessments, monthly statements | Finance/Tax |
| **Updates/Newsletters** | Digest, edition, tech/learning platforms, community forums | Updates/Newsletters |
| **Updates/Promotions** | Promotions, sales, discounts, retail/entertainment senders | Updates/Promotions |
| **Career/Job Search** | LinkedIn, Indeed, Glassdoor, job boards | Career/Job Search |

**Critical**: Promotional emails are moved to `Updates/Promotions` — **never trashed**. All categories map to real IMAP folders that get auto-created if missing.

## Refined Security/OTP Matching Pattern

**Key lesson**: Overly broad keywords like `"sign-in"`, `"logged in"`, `"identity"`, `"unusual activity"`, and `"authorized"` cause false positives — they match promo subjects like "sign in to access exclusive deals". Use specific compound phrases.

```python
security_kw = [
    "verification code", "one time password", "otp", "security alert",
    "magic sign in code", "password reset", "verify your identity",
    "unusual sign-in activity", "login code", "new device logged in",
    "security code", "verification pin", "one-time password",
    "access code", "new sign-in detected", "login from a new device",
    "an unknown device", "account activity - new passkey",
    "cloudflare access login code", "6-digit code",
    "confirm your", "action required] update nameservers",
    "transaction data accessed", "new login to your account",
    "request to sign in with passkey", "new login to x",
    "google verification code", "bitwarden verification code",
    "your unplex otp code", "your my account verification code",
    "api key exposed on github", "signing in to", "security update",
]

# AVOID these — too broad:
# "sign-in", "logged in", "identity", "unusual activity", "authorized"
```

### Special Sender Handling
- **Cloudflare** (`cloudflare.com`): Sends both login codes AND newsletters. Check subject for `"login code"` or `"action required"` first; otherwise treat as newsletter.
- **Google** (`google.com`): Non-security Google emails → `Updates/Newsletters`. Security/alert/verification emails → keep in INBOX.

## Expanded Sender Domain Lists

### Finance/Banking
```
hdfc, icici, sbionline, onlinesbi, amex, americanexpress, bmo.com, td.com,
tangerine, rbc, scotiabank, cibc, yes.bank, idfcfirstbank, idfcfirst,
ctfs.com, rogersbank, dahabshiil, creditcardgenius, pcfinancial,
canadianmortgageapp, timsfinancial, rci.rogers.com, klarna.com,
creditkarma.ca, petro-canada, frugalflyer.ca, equifax, transunion,
paytm.com, quicko.com, westernunion.com, manulife.com, e.manulife.com,
manulife.ca, sbmbank.co.in, tdinsurance.com, plaid.com, 407etr.com,
tcsion.com, motilaloswal.com, bajajfinance.com, stablebonds.in,
airtel.com, kiwiclub.co.in, mailer.quicko.com, csnpe-nslsc.canada.ca,
interactivebrokers.com, chexy.co, paytmbank.com, tcs.com,
emailer.idfcfirstbank.com, emailers.idfcfirstbank.com
```

### Finance/Investments
```
wealthsimple, borrowell, creditkarma, questrade, qtrade.ca, fanduel,
sportsbookca.fanduel, accountca.fanduel, shakepay.com, zebpay.com,
email.zebpay.com, bseindia.in, nipponindia.email
```

### Finance/Orders (Subject Keywords)
```
receipt, order confirmation, invoice, shipping, delivery, your order,
tracking, dispatched, purchase confirmation, payment receipt,
confirmed - you're going, ticket confirmation, thanks for filling,
form:, registration, it's on the way, on the way, bill is ready,
important document attached, subscription will renew, offer accepted,
shipment is delivered, shipment has been picked up, order renewal,
your app can take payments, reservation at, is confirmed,
has been canceled, common area maintenance charges, your reservation,
transaction success report, transaction initiated report,
we've checked your claims, e-statement, your export has completed,
your export has begun, connected your bank account
```

### Updates/Newsletters (Sender Domains)
```
substack.com, medium.com, beehiiv.com, aitinkerers.org, clickhouse.com,
deeplearning.ai, codedex.io, digitalocean.com, sentry.io, supabase.com,
boot.dev, abacusai.net, codemag.com, maven.com, splice.com,
ecomm.lenovo.com, vercel.com, cornell.edu, nptel.iitm.ac.in,
ucalgary.ca, torontomu.ca, datacamp.com, meetup.com, educative.io,
nvidia.com, native-instruments, emails.reasonstudios, digitalcloud.training,
visme.com, canva.com, oracle-mail.com, termius.com, toptal.com, ghost.io,
capacities.io, meta.com, email.meta.com, name.com, findhub,
lunchmoney.app, yuka.io, huawei.eu, tuya.com, fotoapp.co, mapbox.com,
remitly.com, simplefin.org, mermaid.ai, x.ai, appwrite.io,
trypinecone.com, pinecone.io, frontendmasters.com, uchicago.edu,
otter.ai, discord.com, lovable.dev, unplex.money, windowsinsiderprogram,
firecrawl.dev, openrouter.ai, netdata.cloud, simpleanalytics.com,
honeybadger.io, mit.edu, opensubtitles.org, zyte.com, netlify.com,
inputhealth.com, profilesure.com, mygateliving.in, mygate.com,
mygateapp.in, zed.dev, databricks.com, codescene.io, polypane.app,
sqlgate.com, getsentry.com, quora.com, oreilly.com, et.oreilly.com,
fitbit.com, torontopubliclibrary.ca, tpl.ca, getgitguardian.com,
stablemoney.in, confluent.io, fivetran.com, docker.com, algoexpert.io,
radix.email, porkbun.com, get.tech, lifelabs.com, github.com,
reddit.com, neo4j.com, intercom-mail.com, render.com, notion.so,
mail.notion.so, alumnicomms.com, trustpilotmail.com, mindbodyonline.com,
tailscale.com, dashlane.com, shadeform.io, theleapquest.in, strava.com,
unicef.org
```

### Updates/Promotions (Sender Domains)
```
spotify, netflix, uber.com, ubereats, doordash, skipthedishes,
shoppersdrugmart, walmart, amazon.ca, indigo, costco, loblaws,
no frills, bestbuy, newegg, ebates, rakuten, groupon, h&m, zara,
nike, adidas, crunchyroll, hellofresh, skip, tim hortons, timhortons,
pc optimum, pcoptimum, airmiles, paypal, apple, insideapple, iflyworld,
distacart, shopperplus, melodics, clutch.ca, affirm, ymcagta, aircanada,
mail.aircanada.com, logitech, canadiantire, sobeys, decathlon, metro.ca,
lenscrafters, anbernic, flipkart, fanatical, feverup, flexiroam, crocs,
eventbrite, fox.com, foxone, linktr.ee, ticketweb, creditkarma,
rogersbank, borrowell, em.pcoptimum, e.shoppersdrugmart,
email.borrowell, em.sobeys, promo.flexiroam, crocs-email,
email.canadiantire, email.decathlon, communications-on.metro,
e.lenscrafters, e.rogersbank, immail.fanatical, e.pcexpress,
ma.linktr.ee, newsletter.hellofresh, promo.timhortons, email.feverup,
openai.com, dahabshiil, tm.openai, westjet, sunwing, polymarket,
topcashback, levi.com, sportchek, foodbasics, luma-mail, audible.ca,
pcfinancial, goroamless, polarjoe.com, ticketmaster, cineplex.com,
canoo, tellthestar.ca, joinhoney, my.joinhoney.com, samsung, audible,
mtygroup.com, govee.com, ecovacs.com, fitnessavenue.com, mlse.com,
staples.ca, rates.ca, dell.com, order.dell.com, lyftmail.com,
toogoodtogo.com, nordvpn.com, programmemoi.ca, techedinlabs.com,
starblue.co, amazfit.com, valuevillage.com, utest.com, purolator.com,
spothero.com, oxygenyogafitness.com, oddbunch.ca, namecheap.com,
epicgames.com, email.epicgames.com, ableton.com, news.ableton.com,
swiggy.in, microsoft.com, customeremail.microsoft, tbdine.com,
unplex.app, primevideo.com, instacart.com, mubi.com, releases.mubi.com,
news.mubi.com, airbnb.com, e.ea.com, ea.com
```

### Updates/Promotions (Subject Keywords)
```
sale, discount, off , % off, exclusive deal, limited time, save up to,
free trial, promo code, coupon, cashback, special offer, flash sale,
early access, just dropped, save on, don't miss, hurry, expires in,
last chance, final chance, giving away, off on all, gift expire,
unlock, offers, early bird, giveaway, just for you, specially selected,
mother's day, get 25%, 10% off, 20% off, up to 50%, exclusive,
book now, celebrate, before it ends, coming soon, big day, trending,
new offers, rent-free, calling, getaway, expiring soon, voucher,
deals, thank you for subscribing, welcome to, earn 10k bonus,
extra credit, win it, sweepsta, upgrade smarter, save more,
customer feedback survey, save $300, free fries, get it first,
countdown is on, earn more points, don't miss out, deals
```

**WARNING**: Do NOT use `"watch"` or `"stream"` as promo keywords — they match non-promotional subjects like "watch your investment grow". Restrict to known promo sender domains.

### Career/Job Search (Sender Domains)
```
linkedin, indeed, glassdoor, jobs2web.com, telusinternational, toptal.com,
upwork.com, survey.twilio.com, getujobs.com, cgcinfo.getujobs.com
```

## Page-at-a-Time Processing Pattern

For inboxes with 1000+ emails, the 50 tool-call limit per turn makes all-at-once processing impossible. Use page ranges:

```python
for page in range(start_page, end_page):  # ~30 pages per turn
    res = terminal(f'himalaya envelope list -a {account} -f "INBOX" --page-size 50 --page {page} -o json')
    emails = safe_json_parse(res.get("output", ""))
    if not emails: break
    folder_moves = {}
    for env in emails:
        subject = env.get("subject", "") or ""
        sender = format_sender(env)
        cat = categorize(subject, sender)
        if cat is None: continue
        folder_moves.setdefault(cat, []).append(str(env.get("id")))
    if not folder_moves: continue
    for folder, ids in folder_moves.items():
        for i in range(0, len(ids), 25):
            batch = ids[i:i+25]
            terminal(f'himalaya message move -a {account} -f "INBOX" "{folder}" {" ".join(batch)}')
```

Budget: ~1 fetch + ~1-2 moves per page = ~30 pages per 50-call turn. Use successive turns with `range(0,30)`, `range(30,60)`, etc.

## Auto-Folder Creation

Always verify folders exist before moving. Create if missing:

```python
folder_check = terminal(f'himalaya folder list -a {account} -o json')
folder_names = safe_json_parse(folder_check.get("output", "[]"))
existing = [f.get("name", "") for f in folder_names if isinstance(f, dict)]
if folder not in existing:
    terminal(f'himalaya folder add -a {account} "{folder}"')
```

## Pitfalls
- **Never Trash**: Promotional emails must always go to `Updates/Promotions`, not Trash/Bin.
- **Command Syntax**: Target folder MUST come before IDs in `himalaya message move`.
- **JSON Truncation**: Use `page_size=50` and robust string slicing.
- **NoneType Errors**: Use `val or ""` when concatenating JSON fields.
- **Overly Broad Security Keywords**: `"sign-in"`, `"logged in"`, `"identity"`, `"unusual activity"`, `"authorized"` are too broad. Use compound phrases only.
- **Overly Broad Promo Keywords**: `"watch"` and `"stream"` match non-promo subjects. Restrict or remove.
- **Google/Cloudflare Dual-Nature Senders**: Both send security emails AND newsletters. Check subject, not just domain.
