
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.keyboards import reply_keyboard, inline_keyboard


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n"
        "Выбери язык программирования:",
        reply_markup=reply_keyboard,
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие\n"
        "/help - список команд\n"
        "/docs - документация языков\n"
        "/about - информация о боте"
    )


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "Я учебный Telegram-бот. "
        "Показываю описания языков программирования "
        "и ссылки на их официальную документацию."
    )


@router.message(Command("docs"))
async def cmd_docs(message: Message):
    await message.answer(
        "Выбери язык, чтобы перейти к официальной документации:",
        reply_markup=inline_keyboard,
    )


@router.message(F.text.lower() == "python")
async def answer_python(message: Message):
    await message.answer(
        "Python — простой и читаемый язык программирования. "
        "Подходит для Backend-разработки, автоматизации и анализа данных."
    )


@router.message(F.text.lower() == "java")
async def answer_java(message: Message):
    await message.answer(
        "Java — язык программирования, который используют "
        "для Backend-разработки, корпоративных приложений и Android."
    )


@router.message(F.text.lower() == "javascript")
async def answer_javascript(message: Message):
    await message.answer(
        "JavaScript — язык программирования для интерактивных сайтов "
        "и серверных приложений."
    )
