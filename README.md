# Telegram Stars Gift Sniper (Parser & Auto-Buyer)

A Python script that **monitors new Telegram Star Gifts** and **auto-buys** limited gifts based on configurable rules (market-cap threshold, max supply, per-user distribution, cooldowns, etc.).  
It uses two Telegram sessions: one for **parsing** the gift catalog and one for **buying/sending** gifts.

> ⚠️ Use responsibly. Respect Telegram’s Terms of Service and local laws. Consider API rate limits (`FloodWait`) and avoid abusive behavior.

---

## Features

- Connects two Telegram accounts:
  - **Parsing account** — reads the gift catalog via `get_star_gifts()`.
  - **Stars account** — sends/buys gifts with `send_star_gift()`.
- Filters **limited** gifts and ignores already-seen IDs (`gift_list`).
- Computes a simple “market cap” score  
  `market_cap_like = price × total_amount × 0.015` and compares it to `mcap` threshold.
- Splits total purchases among **N recipients (1–10)** with per-send delays.
- Sends **notifications** to a specified account.
- Structured logging with `loguru`.

---

## Requirements

- **Python 3.10+**
- Dependencies: `pyrogram`, `loguru` (optionally `python-dotenv` if you prefer `.env`)
- Two Telegram accounts/sessions:
  - one with access to the gift catalog,
  - one that actually **has Stars** to send.
- **API ID / API Hash** from <https://my.telegram.org/auth>

**Example `requirements.txt`:**
```txt
pyrogram==2.2.7
loguru>=0.7.2
python-dotenv>=1.0.1
```

Install:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

---

## Configuration

The script imports settings from `config.py`. Create it next to the script and fill in your values.

```python
# config.py — sample configuration

# Number of recipients (1..10)
num_of_users = 3

# Recipient usernames (Telegram @usernames or numeric IDs)
first_username  = "user1"
second_username = "user2"
third_username  = "user3"
fourth_username = ""
fifth_username  = ""
sixth_username  = ""
seventh_username = ""
eighth_username  = ""
ninth_username   = ""
tenth_username   = ""

# Delay between individual sends (seconds)
time_sleep = 2.0

# Where to send notifications (username or ID)
acc_for_notification = "me"

# Filtering thresholds
# Gifts pass only if:
#   - gift.is_limited == True
#   - computed market_cap_like <= mcap
#   - gift.total_amount <= max_supply
mcap = 50000            # tune this threshold for your strategy
max_supply = 10000      # maximum allowed total_amount

# Budgeting
stars_for_each = 1000   # total Stars you plan to allocate per gift (split among users)

# Main loop cooldown (seconds) between parsing cycles
parsing_cooldown = 5

# Phone numbers for session login (format Telegram accepts)
tg_number_for_parse_acc = "+48111111111"
tg_number_for_buy_acc   = "+48222222222"
```

> You will also set your **API credentials** inside the script (see below) or switch to environment variables if you prefer.

---

## Script Credentials

At the top of the script, set the two app credentials you got from `my.telegram.org`:

```python
# API keys from https://my.telegram.org/auth
parsing_acc_api_id = 1111111
parsing_acc_api_hash = "11111111"

acc_with_stars_api_id = 111111
acc_with_stars_api_hash = "11111111"
```

> Tip: for better security, load these from environment variables or a `.env` file (e.g., with `python-dotenv`).

---

## How It Works

1. **Login sequence:**  
   - Starts a session `parsing_acc` (parsing account).  
   - Prompts you to confirm a code for the **buying** account as well (`acc_with_stars`), then closes it (to ensure the session is initialized).
2. **Main loop:**  
   Every `parsing_cooldown` seconds:
   - Fetches current gifts via `app.get_star_gifts()`.
   - For each new, **limited** gift not in `gift_list`:
     - Computes a simple “market-cap-like” score: `price × total_amount × 0.015`.
     - If `<= mcap` and `total_amount <= max_supply`, it **calculates how many to send** from `stars_for_each`, splits evenly across `num_of_users`, and calls `buy_nft(...)`.
   - Logs success or errors via `loguru`.
3. **Sending gifts:**  
   `buy_nft()` opens the `acc_with_stars` client and iterates recipients with `time_sleep` pauses, calling `send_star_gift(...)`.

---

## Running

Save your script (e.g., `main.py`) and run:

```bash
python main.py
```

On first run, Pyrogram will ask for login codes (per session). Make sure both numbers in `config.py` can receive Telegram login codes.

---

## Important Notes & Tuning

- **Flood control:** The current implementation uses static `time.sleep`. If you hit `pyrogram.errors.FloodWait`, increase `time_sleep` and `parsing_cooldown`. For production, consider adding an exponential backoff and catching `FloodWait`.
- **Seen gifts list (`gift_list`):** Hard-coded in the script to avoid reprocessing known gifts. You can persist it to disk (e.g., JSON) to keep state across restarts.
- **Distribution math:** The script rounds to evenly split total sends among recipients. Adjust logic if you want different prioritization (e.g., first recipients get the remainder).
- **Notifications:** The parser sends a short message to `acc_for_notification` with `(gift.id, gift.sticker.emoji, market_cap_like)` when a qualifying gift appears.

---

## Troubleshooting

- **Stuck on login / codes not arriving:**  
  Ensure `phone_number` values are correct and you can receive Telegram login codes for both accounts.
- **`FloodWait` or rate limits:**  
  Increase `time_sleep` and `parsing_cooldown`. Add jitter or a retry policy.
- **Attribute vs dict access:**  
  The code expects gift objects (`gift.id`, `gift.price`, etc.). If you change providers, keep the same data model.

---

## Roadmap (nice to have)

- Persist `gift_list` to `gift_seen.json` (load on start, atomic save on update).
- Replace `if num_of_users == N` branches with a dynamic `USERNAMES` list.
- Open `acc_with_stars` **once** and pass the client to `buy_nft(...)`.
- Structured logging (bind gift_id/username) + file rotation.
- Central rate limiter with jitter.

---

## License

MIT (feel free to change if needed).
