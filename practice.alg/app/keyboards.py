from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Расписание')],
                                     [KeyboardButton(text='ChatGPT'), KeyboardButton(
                                         text='Обычный режим')],
                                     [KeyboardButton(text='Генератор шпоргалок'), KeyboardButton(
                                         text='Поиск ресурсов')],
                                     [KeyboardButton(text='решение матем. задач')]],
                           resize_keyboard=True,
                           input_field_placeholder="Выберите пункт в меню")


solutions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='по фото',
                          callback_data='photo')],
    [InlineKeyboardButton(text='по тексту',
                          callback_data='BYtext')]]),


schedule = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить расписание',
                          callback_data='Insert_schedule')],
    [InlineKeyboardButton(text='Посмотреть расписание',
                          callback_data='View_the_schedule')],
    [InlineKeyboardButton(text='Удалить расписание',
                          callback_data='delete_schedule')]])


days_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понедельник",
                              callback_data="view_Понедельник")],
        [InlineKeyboardButton(text="Вторник", callback_data="view_Вторник")],
        [InlineKeyboardButton(text="Среда", callback_data="view_Среда")],
        [InlineKeyboardButton(text="Четверг", callback_data="view_Четверг")],
        [InlineKeyboardButton(text="Пятница", callback_data="view_Пятница")],
        [InlineKeyboardButton(text="Суббота", callback_data="view_Суббота")],
        [InlineKeyboardButton(text="Воскресенье",
                              callback_data="view_Воскресенье")]
    ]
)


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(
    text="Отправить номер", request_contact=True)]], resize_keyboard=True)
