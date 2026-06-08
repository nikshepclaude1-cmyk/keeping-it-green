# keeping-it-green

auto-commits daily to keep your GitHub graph green. smart date-based logic, no spam.

## how it works

`scripts/commit.py` runs via GitHub Actions every day at 2 AM UTC. it updates `activity_log.json` and `stats.json` with real timestamped entries, then pushes.

**commit logic by day:**
| day | commits |
|-----|---------|
| Sunday | 4–7 |
| Mon / Wed / Fri | 2–4 |
| Tue / Thu | 1–3 |
| Saturday | 1–2 |

small ±1 jitter added so it doesn't look robotic.

---

## setup

### 1. add the secret

go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

- name: `GH_PAT`
- value: your GitHub classic token (needs `repo` scope)

### 2. push this repo

```bash
git init
git remote add origin https://github.com/nikshep254/keeping-it-green.git
git add .
git commit -m "init"
git push -u origin main
```

### 3. trigger manually (first run)

go to **Actions → Keep It Green → Run workflow**

after that it runs automatically every day.

---

## dashboard (Vercel)

```bash
cd dashboard
npm install
npm run dev
```

deploy on Vercel by importing the `dashboard/` folder as the root. no env vars needed — it reads public GitHub API + raw stats.json.

---

made by [@nikshep254](https://github.com/nikshep254)
