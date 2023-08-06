# teleshell
Install:

```
pip install teleshell
```

Quick start:
```python
import teleshell
from telethon import TelegramClient


users = []

async def first_func(event):
    users.append(event.chat_id)
    return event.chat_id

client = TelegramClient('bot', 1059116, '878b25abdce8a6c4eb01f10ecf0aefa3').start(bot_token='1499588762:AAG0GVFwssyy4eyVJTBvvWqJIHSA5uvOc4k')
shell = teleshell.ClientShell(client=client, default_first=first_func)
handle = shell.handle


@handle(command='start')
async def func(event, first):
    await event.reply('Started!')


@handle(command='help', first=None)
async def func(event):
    await event.reply('Help!')


@handle(text=r'he(l)+o', regular=True, lower=True)
async def func(event, first):
    await event.reply('Hello!')

client.run_until_disconnected()
```

Version: 0.0.2