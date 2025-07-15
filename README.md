# 📦 Force-Sub Referral Media Bot

A Telegram bot built with Pyrogram + MongoDB that enforces force-subscription, delivers media randomly, and rewards users through referrals. Fully admin-configurable from Telegram.

---

## ✨ Features

- ✅ Force users to join specific channels
- 📦 Random media delivery from media channel
- 🕒 Auto-delete after X minutes
- 🔘 Custom buttons + captions (set by admin)
- 🎁 Referral system with shareable links
- 📊 Stats, previews, user resets, cooldowns
- 🧠 Admin `/settings` panel with inline buttons

---

## 👤 User Commands

| Command     | Description                          |
|-------------|--------------------------------------|
| `/start`    | Starts the bot, checks force-sub     |
| `/refer`    | Get your referral link & stats       |
| `/bonus`    | Claim bonus media (from referrals)   |

---

## 👨‍💻 Admin Commands

| Command             | Description                                |
|---------------------|--------------------------------------------|
| `/setmedia`         | Forward media to set delivery pool         |
| `/setcaption`       | Set global caption for media               |
| `/setbuttons`       | Set inline buttons under media             |
| `/setinfobutton`    | Set info button below final warning        |
| `/setdelay`         | Set auto-delete delay (minutes)            |
| `/setcooldown`      | Time limit between uses (hours)            |
| `/setrefreward`     | Media per successful referral              |
| `/setrefcap`        | Max bonus from referrals                   |
| `/addchnl`          | Add a force-sub channel                    |
| `/delchnl`          | Remove a force-sub channel                 |
| `/resetmedia`       | Clear all saved media                      |
| `/previewmedia`     | Preview indexed media                      |
| `/resetuser <id>`   | Reset referral/media data for a user       |
| `/stats`            | View usage stats                           |
| `/topref`           | Show top referrers                         |
| `/setstrict on/off` | Enable or disable strict force-sub mode    |
| `/adminhelp`        | Full admin command guide                   |
| `/settings`         | Open inline admin panel                    |

---

## 🚀 Local Deployment Guide

### 🔧 Requirements

- Python 3.8+
- MongoDB (Atlas or local)
- Telegram bot token, API ID, API HASH

---

### 🛠 1. Clone or Download

```bash
git clone https://github.com/yourusername/force-sub-referral-bot.git
cd force-sub-referral-bot
