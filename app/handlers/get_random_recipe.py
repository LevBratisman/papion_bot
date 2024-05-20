from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums import ChatAction
import asyncio

from app.keyboards.reply import get_keyboard
from app.handlers.user_private import menu_keyboard
from app.services.gpt_openai import generate_response_random
from app.common.texts import recipe, recipe_start, menu_text

get_random_recipe_router = Router()

functional_keyboard = get_keyboard(
    "🧠Придумать новый рецепт",
    "⬅️Вернуться к меню",
    placeholder="Выберите действие", 
    sizes=(2,))

cancel_keyboard = get_keyboard(
    "Отмена",
    placeholder="",
    sizes=(1,)
)

get_additional_keyboard = get_keyboard(
    "👍Да, давай!",
    "⬅️Вернуться к меню",
    placeholder="Выберите действие", 
    sizes=(2,),
)

class RandomRecipeDatails(StatesGroup):
    details = State()
    additional = State()


@get_random_recipe_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Без проблем!")
    await message.answer(menu_text, reply_markup=menu_keyboard)


@get_random_recipe_router.message(StateFilter(None), F.text.casefold() == "2")
async def get_recipe(message: Message, state: FSMContext):
    await state.set_state(RandomRecipeDatails.details)
    # await asyncio.sleep(1)
    # await message.answer_sticker("CAACAgIAAxkBAAIQq2YVCX2IOu21FjwjlIK_eqU_wnx8AAIwCgAC4_woSqMD6yBTUfobNAQ")
    await message.answer(f"Что вы хотите (например, десерт или суп)? Укажите свои предпочтения\n" +
                         f"Если же вам все равно, то <b>введите ' - '</b>",
                         reply_markup=cancel_keyboard)
    
    
@get_random_recipe_router.message(StateFilter(RandomRecipeDatails.details), F.text)
async def get_recipe_name(message: Message, state: FSMContext, bot: Bot):    
    await message.answer("Сейчас что-нибудь придумаю для вас...")
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    gpt_response = await generate_response_random(message.text)
    if gpt_response == "Не могу ничего придумать...":
        await message.answer_sticker("CAACAgIAAxkBAAIQrWYVCZdKKMAyBicW-562kmzMUoyZAAKrCwACLw_wBoLABuDn5cg3NAQ")
        await asyncio.sleep(1)
        await message.answer(gpt_response)
        await asyncio.sleep(1)
        await message.answer(recipe_start, reply_markup=get_additional_keyboard)
        await state.set_state(RandomRecipeDatails.additional)
    else:
        await message.answer_sticker("CAACAgIAAxkBAAIQqWYVCXpgQgU7O4ExCfV_OdVYwIuqAAJ8DwACzxEgSkGaM72iUQ4iNAQ")
        await asyncio.sleep(1)
        await message.answer(gpt_response, reply_markup=functional_keyboard)
        await state.clear()
    
    
@get_random_recipe_router.message(StateFilter(RandomRecipeDatails.details))
async def incorrect_message(message: Message, state: FSMContext):
    await message.answer("Не понимаю... возможно, вы использовали некорректные данные. Введите ваши предпочтения еще раз")
    
    
@get_random_recipe_router.message(StateFilter(RandomRecipeDatails.additional), F.text=="👍Да, давай!")
async def get_additional(message: Message, state: FSMContext):
    await message.answer(recipe, reply_markup=functional_keyboard)
    await state.clear()
    
    
@get_random_recipe_router.message(StateFilter(RandomRecipeDatails.additional), F.text)
async def to_menu_from_add(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(menu_text, reply_markup=menu_keyboard)


@get_random_recipe_router.message(StateFilter(None), F.text.casefold() == "⬅️вернуться к меню")
async def to_menu(message: Message):
    await message.answer(menu_text, reply_markup=menu_keyboard)
    
    
@get_random_recipe_router.message(StateFilter(None), F.text.casefold() == "🧠придумать новый рецепт")
async def get_recipe_again(message: Message, state: FSMContext):
    await message.answer("Без проблем!", reply_markup=ReplyKeyboardRemove())
    await get_recipe(message, state)