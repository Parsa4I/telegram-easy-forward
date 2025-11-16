from telethon import TelegramClient
from telethon.network.connection.tcpmtproxy import ConnectionTcpMTProxyIntermediate
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
proxy_host = os.getenv("PROXY_HOST")
proxy_port = int(os.getenv("PROXY_PORT"))
proxy_secret = os.getenv("PROXY_SECRET")


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", action="store_true")
parser.add_argument("-v", "--video", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-s", "--save", action="store_true")
args = parser.parse_args()
image = args.image
video = args.video
text = args.text
save = args.save
no_filter = not (image or text or video)


PROGRESS_FILE = "progress.txt"


def load_last_msg_id():
    if not os.path.exists(PROGRESS_FILE):
        return None
    try:
        return int(open(PROGRESS_FILE, "r").read().strip())
    except:
        return None


def save_last_msg_id(msg_id):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(msg_id))


def get_chat_and_thread_id(chat: str):
    chat_splitted = chat.split("_")
    chat_id = int(chat_splitted[0])
    thread_id = int(chat_splitted[1]) if len(chat_splitted) > 1 else None

    return chat_id, thread_id


if proxy_port and proxy_port and proxy_secret:
    client = TelegramClient(
        "main",
        api_id,
        api_hash,
        connection=ConnectionTcpMTProxyIntermediate,
        proxy=(proxy_host, proxy_port, proxy_secret),
    )
else:
    client = TelegramClient(
        "main",
        api_id,
        api_hash,
        connection=ConnectionTcpMTProxyIntermediate,
    )
    if any(proxy_port, proxy_host, proxy_secret):
        print(
            "Warning: Connecting without proxy. Make sure to write PROXY_HOST, PROXY_PORT and PROXY_SECRET in .env file."
        )


async def main(
    source_chat_id, target_chat_id, source_thread_id=None, target_thread_id=None
):
    last_id = 0
    if save:
        last_id = load_last_msg_id()

        if last_id:
            print(f"Resuming after message ID {last_id}...")
        else:
            print("No progress found, starting from the oldest...")

    err = False
    async for msg in client.iter_messages(
        source_chat_id, reply_to=source_thread_id, reverse=True
    ):
        if last_id and msg.id <= last_id:
            continue

        is_text = msg.text and not msg.media
        is_image = msg.photo
        is_video = msg.video

        try:
            if is_text and (text or no_filter):
                print(f"Forwarding text {msg.id}...")
                await client.send_message(
                    target_chat_id, msg.text, reply_to=target_thread_id
                )
            elif is_image and (image or no_filter):
                print(f"Forwarding photo {msg.id}...")
                await client.send_file(
                    target_chat_id,
                    msg.photo,
                    reply_to=target_thread_id,
                    caption=msg.text,
                )
            elif is_video and (video or no_filter):
                print(f"Forwarding video {msg.id}...")
                await client.send_file(
                    target_chat_id,
                    msg.video,
                    reply_to=target_thread_id,
                    caption=msg.text,
                )

            last_id = msg.id
        except Exception as e:
            print(f"Failed on {msg.id}: {e}")
            err = True
            break

    if err:
        print("Error!")
    else:
        print("Done!")

    if save:
        save_last_msg_id(last_id)


source_chat_id, source_thread_id = get_chat_and_thread_id(
    input("Source chat (-12345_123): ")
)
target_chat_id, target_thread_id = get_chat_and_thread_id(
    input("Target chat (-12345_123): ")
)

with client:
    client.loop.run_until_complete(main(source_chat_id, target_chat_id))
