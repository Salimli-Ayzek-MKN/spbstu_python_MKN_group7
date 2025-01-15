import parsing
from datetime import date
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = "7900491190:AAEBcRlxhdrZCELhnzvWOvsN8HVbNTKBK2A"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)


class Form(StatesGroup):
    waiting_for_days = State()


def get_available_items(user_id):
    return ["Товар1", "Товар2", "Товар3"]


def get_subscribed_items(user_id):
    return ["ТоварА", "ТоварБ"]


def subscribe_user_to_item(user_id, item):
    pass


def unsubscribe_user_from_item(user_id, item):
    pass


def get_price_changes(user_id, n):
    return "Пример отчёта о изменении цен."


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подписаться")],
        [KeyboardButton(text="Отписаться")],
        [KeyboardButton(text="Получить изменения за n дней")]
    ],
    resize_keyboard=True
)


def create_inline_buttons(items, back_text):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=item, callback_data=item)
    builder.button(text=back_text, callback_data="back_to_main")
    return builder.as_markup()


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать в бот отслеживания цен!", reply_markup=main_menu)


@router.message(lambda message: message.text in ["Подписаться", "Отписаться", "Получить изменения за n дней"])
async def main_menu_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == "Подписаться":
        items = get_available_items(user_id)
        if items:
            await message.answer("Выберите товар для подписки:", reply_markup=create_inline_buttons(items, "Вернуться в главное меню"))
        else:
            await message.answer("Вы уже подписаны на все товары.", reply_markup=main_menu)
    elif message.text == "Отписаться":
        items = get_subscribed_items(user_id)
        if items:
            await message.answer("Выберите товар для отписки:", reply_markup=create_inline_buttons(items, "Вернуться в главное меню"))
        else:
            await message.answer("Вы не подписаны ни на один товар.", reply_markup=main_menu)
    elif message.text == "Получить изменения за n дней":
        await message.answer("Введите количество дней для отчёта:", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Вернуться в главное меню")]], resize_keyboard=True))
        await state.set_state(Form.waiting_for_days)


@router.callback_query()
async def inline_button_handler(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if callback_query.data == "back_to_main":
        await callback_query.message.edit_text("Возвращение в главное меню.", reply_markup=None)
        await callback_query.message.answer("Главное меню:", reply_markup=main_menu)
    elif callback_query.data in get_available_items(user_id):
        subscribe_user_to_item(user_id, callback_query.data)
        await callback_query.message.edit_text("Вы успешно подписались!", reply_markup=None)
        await callback_query.message.answer("Главное меню:", reply_markup=main_menu)
    elif callback_query.data in get_subscribed_items(user_id):
        unsubscribe_user_from_item(user_id, callback_query.data)
        await callback_query.message.edit_text("Вы успешно отписались!", reply_markup=None)
        await callback_query.message.answer("Главное меню:", reply_markup=main_menu)


@router.message(Form.waiting_for_days)
async def handle_days_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.isdigit():
        n = int(message.text)
        report = get_price_changes(user_id, n)
        await message.answer(f"Изменения цен за последние {n} дней:\n{report}", reply_markup=main_menu)
        await state.clear()
    elif message.text == "Вернуться в главное меню":
        await state.clear()
        await message.answer("Главное меню:", reply_markup=main_menu)
    else:
        await message.answer("Введите корректное число дней или выберите 'Вернуться в главное меню'.")


async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
