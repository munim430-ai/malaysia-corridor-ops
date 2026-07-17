# WORKER INTAKE SETUP — Wire the Funnel Live

**Time required:** ~15 minutes. **Cost:** $0. **Why this matters:** the site currently links to placeholder addresses — `https://forms.google.com/` and WhatsApp number `8801700000000` — in `site/index.html`, `site/employers/index.html`, and `site/assets/script.js`. Nobody who clicks "register" today reaches a real form. This is the single highest-leverage 15 minutes available before any outreach or marketing push goes out.

---

## Step 1 — Create the worker registration Google Form (5 min)

1. Go to [forms.google.com](https://forms.google.com) (sign in with the account this business will operate from).
2. Create a form titled **"Malaysia Corridor Ops — Worker Registration"** with these fields (matches what `content/DISTRIBUTION.md`'s referral script and the site's promise already assume):
   - Full name
   - Phone number (WhatsApp-reachable)
   - District / Upazila (village-level sourcing needs this)
   - Age
   - Preferred sector (Manufacturing / Plantation / Construction / Services / Other)
   - Previous overseas work experience? (Y/N, where)
   - Who referred you? (Name + phone) — powers the referral tiers in `content/DISTRIBUTION.md` §6
   - Consent checkbox: *"আমি বুঝি যে করিডোর বর্তমানে বন্ধ এবং এটি শুধুমাত্র একটি তথ্য ও নিবন্ধন সেবা। কোনো চাকরি বা ভিসার নিশ্চয়তা দেওয়া হয় না।"* (I understand the corridor is currently closed and this is an information/registration service only — no job or visa is guaranteed.)
3. Click **Send** → copy the shareable link.
4. In Google Sheets, click the form's **Responses** tab → green Sheets icon → **Create Spreadsheet**. This gives you a live spreadsheet CRM at zero cost — every submission lands here automatically.

## Step 2 — Create the employer registration Google Form (5 min)

Same process, second form, titled **"Malaysia Corridor Ops — Employer Registration"**:
- Company name
- Sector
- Contact name + title
- Email / phone
- Approx. foreign worker headcount needed
- Timeline (this year / next year / exploring)

## Step 3 — Get a real WhatsApp Business number (2 min)

Use any number with WhatsApp installed (a dedicated SIM is best, but not required to start). WhatsApp Business (free app) adds auto-reply and labels, useful once volume grows.

## Step 4 — Replace the placeholders in the repo (3 min)

Update these exact locations:

| File | Line(s) | Placeholder | Replace with |
|---|---|---|---|
| `site/index.html` | 214 | `https://forms.google.com/` | Your worker form link |
| `site/index.html` | 215, 242 | `8801700000000` (in `wa.me/...`) | Your real WhatsApp number, no `+` or spaces |
| `site/employers/index.html` | (search for `forms.google.com` and `wa.me`) | same placeholders | Employer form link + same/different WhatsApp number |
| `site/assets/script.js` | (search for `wa.me`) | same | same number |
| `content/DISTRIBUTION.md` | multiple `wa.me/880XXXXXXXXXX` script templates | placeholder | your real number, before using any of the scripts |
| `automation/generate_outreach.py` | `SIGNOFF` constant | `wa.me/880XXXXXXXXXX` | your real number |

Quick way to find every instance:
```bash
grep -rn "forms.google.com\|8801700000000\|880XXXXXXXXXX" site/ content/ automation/
```

Commit and push — GitHub Pages redeploys automatically (see `.github/workflows/deploy.yml`).

## Step 5 — Optional but recommended: Telegram notification on new signups (5 min)

Free, no extra account needed beyond Telegram itself:

1. In Telegram, message **@BotFather** → `/newbot` → follow the prompts → copy the bot token.
2. Create your public Telegram channel (per `content/DISTRIBUTION.md` §5) and add the bot as an admin.
3. In the Google Sheet created in Step 1, go to **Extensions → Apps Script**, paste:

```javascript
function notifyTelegram(e) {
  const token = "YOUR_BOT_TOKEN";
  const chatId = "YOUR_CHANNEL_OR_CHAT_ID";
  const row = e.values;
  const message = `New worker signup:\n${row.join("\n")}`;
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  UrlFetchApp.fetch(url, {
    method: "post",
    payload: { chat_id: chatId, text: message },
  });
}
```

4. In the Apps Script editor: **Triggers (clock icon) → Add Trigger → notifyTelegram → From spreadsheet → On form submit → Save**.

Now every registration — worker or employer — pings your Telegram in real time, at zero cost, with no server to maintain.

## Step 6 — Verify end to end

1. Submit a test entry through the live site.
2. Confirm it lands in the Google Sheet.
3. Confirm the Telegram notification fires (if set up).
4. Delete the test row before real traffic starts.

---

Once this is live, the 30-day distribution targets in `BUSINESS_PLAN.md` §5 and §11 can actually convert clicks into tracked leads instead of dead-ending at a placeholder link.
