from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Python")],
        [KeyboardButton(text="Java")],
        [KeyboardButton(text="JavaScript")],
    ],
    resize_keyboard=True,
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Документация Python",
            url="https://docs.python.org/3/"
        )],
        [InlineKeyboardButton(
            text="Документация JS",
            url="https://developer.mozilla.org/en-US/docs/Web/JavaScript"
        )],
        [InlineKeyboardButton(
            text="Документация Java",
            url="https://docs.oracle.com/en/java/"
        )],
    ]
)