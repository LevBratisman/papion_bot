from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.reply import get_keyboard
from app.database.dao import get_all_users_id, get_reviews_by_limit, get_all_reviews

from app.handlers.user_private import menu_keyboard


admin_router = Router()
admin_router.message.filter(IsAdmin())
    
    
admin_keyboard = get_keyboard(
    "📊Статистика",
    "🔉Сделать рассылку",
    "💬Отзывы",
    "⬅️Назад",
    "🔄Сбросить",
    placeholder="Выберите действие", 
    sizes=(2, 1, 2)
)


    
class SendAll(StatesGroup):
    photo = State()
    message = State()
    
    
class GetReviews(StatesGroup):
    limit = State()
    
    
@admin_router.message(StateFilter("*"), F.text == "🔄Сбросить")
async def reset(message: Message, state: FSMContext):
    await message.answer("Изменения сброшены", reply_markup=admin_keyboard)
    await state.clear()


@admin_router.message(StateFilter("*"), F.text == "⬅️Назад")
async def back_to_menu(message: Message, state: FSMContext):
    await message.answer('Вы вышли из адпин-панели', reply_markup=menu_keyboard)
    await state.clear()
    
    
@admin_router.message(Command("admin"))
async def open_admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вошли в админ-панель", reply_markup=admin_keyboard)
        
        
# Statistic ------------------------------------------
      
@admin_router.message(StateFilter(None), F.text == "📊Статистика")
async def get_statistic(message: Message, session: AsyncSession):
    await message.answer("Количество пользователей: " + str(len(await get_all_users_id(session))))
    await message.answer("Количество отзывов: " + str(len(await get_all_reviews(session))))
    
# Get reviews -----------------------------------------

@admin_router.message(StateFilter(None), F.text == "💬Отзывы")
async def get_reviews(message: Message, state: FSMContext):
    await state.set_state(GetReviews.limit)
    await message.answer("Сколько отзывов вы хотите получить?")
    
    
@admin_router.message(GetReviews.limit, F.text)
async def get_reviews_limit(message: Message, state: FSMContext, session: AsyncSession):
    try:
        int(message.text)
    except:
        await message.answer("Вы ввели некорректное значение")
        return
    await state.update_data(limit=int(message.text))
    await state.clear()
    await message.answer("Отзывы:" + f'\n\n{"-" * 20}')
    for review in await get_reviews_by_limit(session, message.text):
        await message.answer(review.text + f'\n\n{"-" * 20}')
        
    
# Send all --------------------------------------------

@admin_router.message(F.text == "🔉Сделать рассылку")
async def send_all(message: Message, state: FSMContext):
    await state.set_state(SendAll.photo)
    await message.answer("Теперь отправьте фотографию (либо введите 'n', если пост будет без фотографии)")
    
    
@admin_router.message(SendAll.photo)
async def send_all_photo(message: Message, state: FSMContext):
    try:
        await state.update_data(photo=message.photo[0].file_id)
    except:
        await message.answer("Пост будет без фотографии")
        await state.update_data(photo=None)
    await state.set_state(SendAll.message)
    await message.answer("Теперь введите сообщение")
    
    
@admin_router.message(SendAll.message)
async def send_all_message(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    await state.update_data(message=message.text)
    message_data = await state.get_data()
    data = await get_all_users_id(session)
    print(data)
    await message.answer("Рассылка началась")
    if message_data["photo"] is None:
        for user_id in data:
            await bot.send_message(str(user_id), message_data["message"])
    else:
        for user_id in data:
            await bot.send_photo(str(user_id), message_data["photo"], caption=message_data["message"])
    await message.answer("Рассылка завершена")
    await state.clear()