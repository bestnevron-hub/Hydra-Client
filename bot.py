import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Импортируем токен из нашего конфиг-файла
from config import BOT_TOKEN

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Ссылка на товар ---
FUNPAY_URL = "https://funpay.com/lots/offer?id=60185820"

# --- Клавиатуры ---

def get_purchase_keyboard():
    """Создает клавиатуру с одной кнопкой для покупки."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Купить Hydra Client", callback_data="buy_product")
    return builder.as_markup()

def get_funpay_link_keyboard():
    """Создает клавиатуру с кнопкой-ссылкой на FunPay."""
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти к оплате на FunPay", url=FUNPAY_URL)
    return builder.as_markup()

# --- Обработчики ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    await message.answer(
        "Добро пожаловать в магазин Hydra Client!\n\n"
        "Нажмите на кнопку ниже, чтобы перейти к покупке.",
        reply_markup=get_purchase_keyboard()
    )

@dp.callback_query(lambda c: c.data == 'buy_product')
async def process_buy_callback(callback_query: types.CallbackQuery):
    """Обработчик нажатия на кнопку покупки."""
    await callback_query.message.answer(
        "Отлично! Для безопасной покупки мы используем FunPay.\n\n"
        "Нажмите на кнопку ниже, чтобы перейти на страницу товара и оплатить его.",
        reply_markup=get_funpay_link_keyboard()
    )
    await callback_query.answer() # Убираем "часики" на кнопке


# --- Запуск бота ---

async def main():
    """Основная функция для запуска бота."""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
