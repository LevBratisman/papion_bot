import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.user_private import menu_keyboard, show_details
from app.handlers.get_random_recipe import cancel_keyboard
from app.common.texts import feedback_text, menu_text
from app.config import settings

from app.database.dao import add_review, get_id_by_user_id

cmd_router = Router()


class SendFeedback(StatesGroup):
    feedback = State()


@cmd_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(menu_text, reply_markup=menu_keyboard)
    
    
@cmd_router.message(Command("about"))
async def cmd_about(message: Message, state: FSMContext):
    await state.clear()
    await show_details(message)
    

# FSM отправка отзыва -----------------------------------------

@cmd_router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(feedback_text)
    await state.set_state(SendFeedback.feedback)
    await message.answer("✉️Напишите ваш отзыв", reply_markup=cancel_keyboard)
    
@cmd_router.message(StateFilter(SendFeedback.feedback), F.text == "Отмена")
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(menu_text, reply_markup=menu_keyboard)

@cmd_router.message(StateFilter(SendFeedback.feedback), F.text)
async def cmd_feedback(message: Message, state: FSMContext, session: AsyncSession):
    user_id = await get_id_by_user_id(session, message.from_user.id)
    await add_review(session, user_id, message.text)
    await state.clear()
    await message.answer("Спасибо, отзыв был успешно отправлен!")
    await message.answer(menu_text, reply_markup=menu_keyboard)
    
    
@cmd_router.message(StateFilter(SendFeedback.feedback))
async def cmd_feedback(message: Message, state: FSMContext):
    await message.answer("Неверный формат данных")
    
    
# ---------------------------------------------------------------
    
    
@cmd_router.message(Command("contacts"))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("По всем вопросам обращайтесь к моему создателю @bratisman")
    await message.answer(menu_text, reply_markup=menu_keyboard)