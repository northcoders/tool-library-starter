# Checks your AI provider details in .env work.
# Run from the server/ folder with:  python -m scratch.hello_llm
import asyncio
import sys

from dotenv import load_dotenv

from llm import send_message

load_dotenv()


async def main():
    reply = await send_message(
        system="You are a helpful assistant. Reply in one short sentence.",
        messages=[{"role": "user", "content": "Say hello to the Tool Library."}],
    )
    print(reply["content"])


try:
    asyncio.run(main())
except Exception as err:
    print(err)
    sys.exit(1)
