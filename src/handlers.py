from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards import reply_keyboard, inline_keyboard, restart_keyboard
from src.questions import QUESTIONS
from db.users import create_user
from db.results import save_result

router = Router()


class Quiz(StatesGroup):
    waiting_answer = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.full_name or "Аноним",
    )

    await message.answer(
        f"Привет, {message.from_user.full_name}!",
        reply_markup=reply_keyboard,
    )

    print(f"Пользователь добавлен или уже существует: {user}")


@router.message(Command("docs"))
async def cmd_docs(message: Message):
    await message.answer(
        "Выбери язык, чтобы перейти к официальной документации:",
        reply_markup=inline_keyboard,
    )


async def start_quiz(message: Message, state: FSMContext):
    await state.update_data(index=0, score=0)
    await state.set_state(Quiz.waiting_answer)
    await message.answer(
        f"Вопрос 1: {QUESTIONS[0]['q']}"
    )


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(index=0, score=0)
    await state.set_state(Quiz.waiting_answer)
    await callback.message.answer(
        f"Вопрос 1: {QUESTIONS[0]['q']}"
    )


@router.message(Command("quiz"))
async def cmd_quiz(message: Message, state: FSMContext):
    await start_quiz(message, state)


@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправь ответ текстом.")
        return

    data = await state.get_data()
    index = data["index"]
    score = data["score"]

    if message.text.strip().lower() == QUESTIONS[index]["a"].lower():
        score += 1
        await message.answer("Правильно! +1 балл")
    else:
        await message.answer(
            f"Неверно. Правильный ответ: {QUESTIONS[index]['a']}"
        )

    index += 1

    if index >= len(QUESTIONS):
        save_result(
            telegram_id=message.from_user.id,
            score=score,
        )
        await message.answer(
            f"Викторина окончена!\n"
            f"Твой результат: {score}/{len(QUESTIONS)}",
            reply_markup=restart_keyboard,
        )
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(
            f"Вопрос {index + 1}: {QUESTIONS[index]['q']}"
        )

