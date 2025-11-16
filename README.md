# Easy Telegram Forward
A dead-simple Python tool to easily forward and back up Telegram messages using Telethon — with filters, resume support, and MTProxy built in.

## What's This Thing?

This script is a simple Python utility that lets you **forward Telegram messages** from one chat/channel/group/topic to another — including support for photos, videos, text, and topic threads.
It also supports **MTProxy** in adition to **resume-after-interruption**, so if your backup gets cut of (due to connection issues or Telegram's API limit) you won't have to start over.

## Features

* Forward **text**, **photos**, and **videos**
* Filter by content type (`--text`, `--image`, `--video`)
* Resume progress with a built-in `progress.txt` tracker (`--save`)
* MTProxy support
* Supports forwarding inside **threaded chats**

## Installation

```bash
git clone https://github.com/Parsa4I/telegram-easy-forward
cd telegram-easy-forward
pip install -r requirements.txt
```

Make sure you have a `.env` file next to the script:

```
API_ID=your_api_id_here
API_HASH=your_api_hash_here

# Optional proxy
PROXY_HOST=your_proxy_host
PROXY_PORT=your_proxy_port
PROXY_SECRET=your_proxy_secret
```

If you don't need a proxy, leave them empty.

## Usage

Run the script:

```bash
python main.py [options]
```

### Options

| Flag            | Description                    |
| --------------- | ------------------------------ |
| `-t`, `--text`  | Forward only text messages     |
| `-i`, `--image` | Forward only images            |
| `-v`, `--video` | Forward only videos            |
| `-s`, `--save`  | Save progress and resume later |

If you don't specify any filters, everything is forwarded. You can also use multiple filters.

### Example Usage

#### Forward everything:

```bash
python main.py
```

#### Forward only images:

```bash
python main.py --image
```

#### Forward only images and texts:

```bash
python main.py -it
```

#### Resume where you left off/Save your progress:

```bash
python main.py --save
```

## Source / Target Format

You'll be prompted for:

```
Source chat (-123456789_123)
Target chat (-987654321_456)
```

Format explanation:

* `CHAT_ID` → `-123456789`
* `_THREAD_ID` → `_123`, only needed for threaded discussions (optional)

Example:

* `-123456789_5` → Chat ID + Topic #5
* `-123456789` → Chat only, no topic

## Progress Tracking

If `--save` is enabled:

* The script writes the last processed message ID into `progress.txt`
* Stopping and restarting will continue right where you left off

## Notes

* This is a **forwarding** script — not an export tool
* Messages retain captions, photos, and videos
* Telegram API limits apply

## Why This Project Exists

Because manually forwarding 20,000 messages is torture and life is too short.
