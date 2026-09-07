# CAP-X Trainer (slice 1)

Static website + spreadsheet. Original ChatGPT files in Drive `CAP Exam Coach` were copied, not edited.

## What you have
- `index.html` + `app.js` + `styles.css` + `data/questions.json` — the player
- `data/CAP-X_Trainer_Data.xlsx` — bank + empty Progress / Sessions / Tallies
- `data/chatgpt_bank_backup.json` — untouched copy of the ChatGPT 100

Pool is **115 items** (100 imported + 15 new). A form is 115 questions with CAP-X-like domain mix. Slots A/B/C are named shuffles. Timer optional 3 hours.

## Open it
Do not double-click `index.html` if the questions fail to load (browsers block `fetch` on `file://`).

```bash
cd cap-x-trainer
python3 -m http.server 8080
```

Then open http://127.0.0.1:8080

Or drop the folder on Vercel / Netlify / Cloudflare Pages / GitHub Pages. No build step.

## Progress on another computer
1. Export progress JSON in the player
2. Put that file in your CAP Drive folder
3. On the other computer, open the site and Import the JSON

Browser storage does not travel by itself. The Sheet is the human-readable backup of the bank.

## Print / PDF
Use **Print / PDF study** then “Save as PDF” in the browser. Upload that PDF to Drive when you want an offline copy.
