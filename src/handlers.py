from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards import reply_keyboard, inline_keyboard, restart_keyboard
from db.users import create_user, get_user
from db.questions import get_all_questions
from db.results import save_result, get_score

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
    user = get_user(message.from_user.id)
    questions = get_all_questions()

    if not user:
        await message.answer("Сначала нажми /start")
        return

    if not questions:
        await message.answer("В базе пока нет вопросов.")
        return

    await state.update_data(
        index=0,
        score=0,
        questions=questions,
        user_id=user["id"],
    )
    await state.set_state(Quiz.waiting_answer)

    await message.answer(
        f"Вопрос 1: {questions[0]['question_text']}"
    )


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await start_quiz(callback.message, state)


@router.message(Command("quiz"))
async def cmd_quiz(message: Message, state: FSMContext):
    await start_quiz(message, state)


@router.message(Command("score"))
async def cmd_score(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Сначала нажми /start")
        return

    result = get_score(user["id"])
    total = result.get("total") or 0
    correct = result.get("correct") or 0

    await message.answer(
        f"Твоя статистика:\n"
        f"Всего ответов: {total}\n"
        f"Правильных ответов: {correct}"
    )


@router.callback_query(F.data == "score")
async def callback_score(callback: CallbackQuery):
    await callback.answer()

    user = get_user(callback.from_user.id)

    if not user:
        await callback.message.answer("Сначала нажми /start")
        return

    result = get_score(user["id"])
    total = result.get("total") or 0
    correct = result.get("correct") or 0

    await callback.message.answer(
        f"Твоя статистика:\n"
        f"Всего ответов: {total}\n"
        f"Правильных ответов: {correct}"
    )


@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправь ответ текстом.")
        return

    data = await state.get_data()
    index = data["index"]
    score = data["score"]
    questions = data["questions"]
    user_id = data["user_id"]

    question = questions[index]

    is_correct = (
        message.text.strip().lower()
        == question["correct_answer"].strip().lower()
    )

    save_result(
        user_id=user_id,
        question_id=question["id"],
        is_correct=is_correct,
    )

    if is_correct:
        score += 1
        await message.answer("Правильно! +1 балл")
    else:
        await message.answer(
            f"Неверно. Правильный ответ: "
            f"{question['correct_answer']}"
        )

    index += 1

    if index >= len(questions):
        await message.answer(
            f"Викторина окончена!\n"
            f"Твой результат: {score}/{len(questions)}",
            reply_markup=restart_keyboard,
        )
        await state.clear()
    else:
        await state.update_data(
            index=index,
            score=score,
        )
        await message.answer(
            f"Вопрос {index + 1}: "
            f"{questions[index]['question_text']}"
        )