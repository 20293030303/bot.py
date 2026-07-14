import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ErrorEvent

# إعداد السجلات (للحماية من التعليق)
logging.basicConfig(level=logging.INFO, filename="bot_errors.log", filemode="a")

TOKEN = "8706530595:AAEbkD9ZCuVNbn5SxaqmeUQUbjA5U1zfKXs"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# حالات البوت (لإدارة المستخدمين)
class BotStates(StatesGroup):
    waiting_for_text = State()

# --- القائمة الرئيسية ---
def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕌 زخرفة عربي", callback_data="dec_ar"), InlineKeyboardButton(text="✨ English", callback_data="dec_en")],
        [InlineKeyboardButton(text="🔢 زخرفة أرقام", callback_data="dec_num"), InlineKeyboardButton(text="𝕿 Special", callback_data="dec_sp")],
        [InlineKeyboardButton(text="🇰🇷 كتابة كوري", callback_data="dec_kr"), InlineKeyboardButton(text="💬 داخل المحادثات", callback_data="dec_chat")],
        [InlineKeyboardButton(text="📎 بايو انستا", callback_data="bio_insta"), InlineKeyboardButton(text="📦 بايو قنوات", callback_data="bio_chan")],
        [InlineKeyboardButton(text="✝️ الرموز", callback_data="symbols"), InlineKeyboardButton(text="🕯️ نبذات جاهزة", callback_data="bios")],
        [InlineKeyboardButton(text="🌵 حساب العمر", callback_data="age"), InlineKeyboardButton(text="➕ المزيد", callback_data="more")]
    ])
    return keyboard

# الحارس (منع التعطل)
@dp.error()
async def error_handler(event: ErrorEvent):
    logging.error(f"خطأ: {event.exception}")
    return True

# أمر البداية
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🌿 أهلاً بك في البوت المطور.\nاختر من القائمة أدناه:", reply_markup=get_main_menu())

# --- معالجة الأزرار ---
@dp.callback_query(F.data.startswith("dec_"))
async def start_decoration(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(style=callback.data)
    await state.set_state(BotStates.waiting_for_text)
    await callback.message.answer("أرسل الاسم الذي تريد زخرفته الآن:")
    await callback.answer()

# معالجة النصوص
@dp.message(BotStates.waiting_for_text)
async def process_decoration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    style = data.get("style")
    text = message.text
    
    # هنا المنطق
    result = f"✨ {text} ✨" 
    
    await message.answer(f"النتيجة:\n`{result}`", parse_mode="Markdown")
    await state.clear()

# --- معالجة الأزرار الثابتة ---
@dp.callback_query(F.data.in_({"bio_insta", "bio_chan", "symbols", "bios", "age", "more"}))
async def handle_info_buttons(callback: types.CallbackQuery):
    if callback.data == "bio_insta":
        await callback.message.answer("هذا بايو انستا فخم: \n\n✨ 𝐉𝐔𝐒𝐓 𝐌𝐄 ✨")
    elif callback.data == "symbols":
        await callback.message.answer("الرموز المميزة:\n🦋 🕊️ 🕯️ 🌵 ✝️")
    else:
        await callback.message.answer("هذا القسم قيد التطوير حالياً، انتظر التحديث!")
    await callback.answer()

# التشغيل
async def main():
    print("البوت يعمل الآن..")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

