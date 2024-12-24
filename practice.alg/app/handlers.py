from aiogram import F, Router, types
from app.database.models import async_session
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sympy import symbols, solve, simplify, SympifyError

from app.generators import generate
from app.generators import shpora
from app.generators import search

import app.keyboards as kb
import app.database.requests as rq

router = Router()


class Generate (StatesGroup):
    text = State()


class Register(StatesGroup):
    name = State()
    number = State()


class ScheduleStates(StatesGroup):
    selecting_day = State()
    adding_subjects = State()


user_day_selection = {}

user_modes = {}


days = ["Понедельник", "Вторник", "Среда",
        "Четверг", "Пятница", "Суббота", "Воскресенье"]


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, async_session)
    await message.answer("Добро пожаловать! Выберите действие из меню.", reply_markup=kb.main)


@router.message(F.text == "Расписание")
async def show_schedule_options(message: Message):
    await message.answer("Выберите действие:", reply_markup=kb.schedule)


@router.callback_query(F.data == "Insert_schedule")
async def start_adding_subjects(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите день недели, например 'Понедельник'")
    await state.set_state(ScheduleStates.selecting_day)


@router.message(ScheduleStates.selecting_day, lambda message: message.text in days)
async def day_selected(message: types.Message, state: FSMContext):
    user_day_selection[message.from_user.id] = message.text
    await message.answer(
        f"Вы выбрали {message.text}. Теперь введите названия предметов по одному.\n"
        "Напишите 'стоп', чтобы завершить."
    )
    await state.set_state(ScheduleStates.adding_subjects)


@router.message(ScheduleStates.adding_subjects, lambda message: message.text.lower() != "стоп")
async def add_subject(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in user_day_selection:
        day_name = user_day_selection[user_id]
        subject = message.text

        async with async_session() as session:
            await rq.add_schedule_entry(session, user_id=user_id, day_name=day_name, subject=subject)

        await message.answer(f"Предмет '{subject}' добавлен в расписание на {day_name}.")
    else:
        await message.answer("Сначала выберите день недели!")


@router.message(ScheduleStates.adding_subjects, lambda message: message.text.lower() == "стоп")
async def stop_adding(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in user_day_selection:
        del user_day_selection[user_id]
        await message.answer("Ввод завершен. Спасибо!")
        await state.clear()
    else:
        await message.answer("Вы еще не начали ввод.")


@router.callback_query(F.data == "View_the_schedule")
async def view_schedule(callback: CallbackQuery):
    await callback.message.answer("Выберите день недели для просмотра:", reply_markup=kb.days_keyboard)


@router.callback_query(F.data == "view_Понедельник")
async def view_monday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Понедельник")

    if schedule:
        schedule_text = "Понедельник:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Понедельник пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "view_Вторник")
async def view_tuesday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Вторник")
    if schedule:
        schedule_text = "Вторник:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Вторник пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "view_Среда")
async def view_wednesday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Среда")
    if schedule:
        schedule_text = "Среда:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Среда пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "view_Четверг")
async def view_thursday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Четверг")
    if schedule:
        schedule_text = "Четверг:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Четверг пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "view_Пятница")
async def view_friday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Пятница")
    if schedule:
        schedule_text = "Пятница:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Пятница пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "view_Суббота")
async def view_saturday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Суббота")
    if schedule:
        schedule_text = "Суббота:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Суббота пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "view_Воскресенье")
async def view_sunday_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        schedule = await rq.get_user_schedule_by_day(session, user_id, "Воскресенье")
    if schedule:
        schedule_text = "Воскресенье:\n" + "\n".join(schedule)
    else:
        schedule_text = "Расписание на Воскресенье пусто."

    await callback.message.answer(schedule_text)


@router.callback_query(F.data == "delete_schedule")
async def delete_schedule(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        await rq.delete_user_schedule(session, user_id)
    await callback.message.answer("Ваше расписание было успешно удалено.")


@router.message(lambda message: message.text in ["ChatGPT", "Обычный режим", "Генератор шпоргалок", "Поиск ресурсов"])
async def set_mode(message: Message):
    # Установить выбранный режим
    user_modes[message.from_user.id] = message.text
    await message.reply(f"Вы выбрали режим: {message.text}")


@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    mode = user_modes.get(user_id, "Обычный")

    if mode == "ChatGPT":
        await state.set_state(Generate.text)
        response = await generate(message.text)
        await message.answer(response.choices[0].message.content)
        await state.clear()
    elif mode == "Генератор шпоргалок":
        await state.set_state(Generate.text)
        response = await shpora(message.text)
        await message.answer(response.choices[0].message.content)
        await state.clear()
    elif mode == "Поиск ресурсов":
        await state.set_state(Generate.text)
        response = await search(message.text)
        await message.answer(response.choices[0].message.content)
        await state.clear()
    else:
        await message.answer("Вы еще не выбрали режим работы, сделайте это прямо сейчас в меню!")
        await state.clear()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Бог поможет')


@router.message(Command('register'))
async def register_name(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Введите ваше имя")


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.number)
    await message.answer("Введите ваш номер телефона", reply_markup=kb.get_number)


@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Вы успешно зарегистрированы \n Ваше имя: {data["name"]} \n Ваш номер телефона: {data["number"]}')
    await state.clear()
