from pyrogram import Client, filters, emoji
from pyrogram.types.bots_and_keyboards import inline_keyboard_markup, inline_keyboard_button
from config import Messages as tr

@Client.on_message(filters.private & filters.incoming & filters.command(['start']))
async def _start(client, message):
    await client.send_message(chat_id = message.chat.id,
        text = tr.START_MSG.format(message.from_user.first_name),
        parse_mode = "markdown",
        disable_notification = True,
        reply_to_message_id = message.message_id
    )


@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
async def _help(client, message):
    await client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        parse_mode = "markdown",
        disable_notification = True,
        reply_markup = inline_keyboard_markup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
async def help_answer(c, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    await c.edit_message_text(chat_id = chat_id,    message_id = message_id,
        text = tr.HELP_MSG[msg],    reply_markup = inline_keyboard_markup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [inline_keyboard_button(text = '-->', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):

        button = [
            [inline_keyboard_button(text = 'Support Chat', url = "https://www.github.com/cdfxscrq")],
            [inline_keyboard_button(text = 'Feature Request', url = "https://t.me/Akshayan1")],
            [inline_keyboard_button(text = '<--', callback_data = f"help+{pos-1}")]

        ]
    else:
        button = [
            [
                inline_keyboard_button(text = '<--', callback_data = f"help+{pos-1}"),
                inline_keyboard_button(text = '-->', callback_data = f"help+{pos+1}")
            ],
        ]
    return button
