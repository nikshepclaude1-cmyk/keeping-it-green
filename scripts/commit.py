#!/usr/bin/env python3
"""
keeping-it-green — smart daily commit script
Logic: date-seeded randomness so commits are reproducible per day
  - Sunday: 9–12 commits (heavy day)
  - Mon/Wed/Fri: 7–10 commits
  - Tue/Thu: 6–9 commits
  - Sat: 5–8 commits (light)
  - Never below 5, never above 12 (looks natural)
"""

import json
import os
import random
import datetime
import subprocess

# ── config ───────────────────────────────────────────────────────────────────
LOG_FILE  = "activity_log.json"
STATS_FILE = "stats.json"
AUTHOR_NAME  = "nikshepclaude1-cmyk"
AUTHOR_EMAIL = "nikshepclaude1@gmail.com"
# ─────────────────────────────────────────────────────────────────────────────

def commit_count_for_date(date: datetime.date) -> int:
    """Deterministic commit count from date seed + small random variance."""
    seed = int(date.strftime("%Y%m%d"))
    rng  = random.Random(seed)
    dow  = date.weekday()          # 0=Mon … 6=Sun

    if dow == 6:                   # Sunday  — heavy
        base = rng.randint(9, 12)
    elif dow in (0, 2, 4):         # Mon/Wed/Fri — medium
        base = rng.randint(7, 10)
    elif dow in (1, 3):            # Tue/Thu — moderate
        base = rng.randint(6, 9)
    else:                          # Saturday — light
        base = rng.randint(5, 8)

    # tiny real-time jitter (±1) so two runs on same day feel alive
    jitter = random.randint(-1, 1)
    return max(5, min(12, base + jitter))


def load_log() -> dict:
    default = {"commits": [], "total": 0, "streak": 0, "last_date": None}
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE) as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️  Could not parse {LOG_FILE} ({e}), starting fresh.")
    return default


def save_log(log: dict):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def update_stats(log: dict):
    today = datetime.date.today().isoformat()
    today_commits = [c for c in log["commits"] if c["date"] == today]

    # streak calc
    streak = 0
    check  = datetime.date.today()
    dated  = {c["date"] for c in log["commits"]}
    while check.isoformat() in dated:
        streak += 1
        check  -= datetime.timedelta(days=1)

    stats = {
        "total_commits": log["total"],
        "streak_days":   streak,
        "today_commits": len(today_commits),
        "last_updated":  datetime.datetime.utcnow().isoformat() + "Z",
        "recent": log["commits"][-30:],          # last 30 entries for dashboard
    }
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


def git(cmd: list[str]):
    result = subprocess.run(["git"] + cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"git {' '.join(cmd)} failed:\n{result.stderr}")
    return result


def make_commit(n: int, date_str: str):
    log = load_log()
    ts  = datetime.datetime.utcnow().isoformat() + "Z"

    entry = {
        "date":      date_str,
        "commit_no": n,
        "timestamp": ts,
        "message":   f"chore: activity log update [{date_str}] #{n}",
    }
    log["commits"].append(entry)
    log["total"] += 1
    log["last_date"] = date_str

    save_log(log)
    update_stats(log)

    git(["add", LOG_FILE, STATS_FILE])
    git(["commit",
         "--author", f"{AUTHOR_NAME} <{AUTHOR_EMAIL}>",
         "-m", entry["message"]])
    print(f"  ✓ commit {n} — {ts}")


def main():
    today     = datetime.date.today()
    date_str  = today.isoformat()
    n_commits = commit_count_for_date(today)

    print(f"📅 {date_str} ({today.strftime('%A')}) — targeting {n_commits} commit(s)")

    # configure git identity (needed in Actions)
    git(["config", "user.name",  AUTHOR_NAME])
    git(["config", "user.email", AUTHOR_EMAIL])

    for i in range(1, n_commits + 1):
        make_commit(i, date_str)

    git(["push"])
    print(f"\n✅ pushed {n_commits} commit(s) for {date_str}")


if __name__ == "__main__":
    main()
