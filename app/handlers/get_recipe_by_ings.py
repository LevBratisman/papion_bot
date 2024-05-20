import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums import ChatAction

from app.keyboards.reply import get_keyboard
from app.handlers.user_private import menu_keyboard
from app.handlers.get_random_recipe import cancel_keyboard
from app.services.gpt_openai import generate_response_by_ingridients 
from app.common.texts import recipe, recipe_start, menu_text

get_recipe_by_ings_router = Router()

functional_keyboard = get_keyboard(
    "🧠Подобрать новый рецепт",
    "⬅️Вернуться к меню",
    placeholder="Выберите действие", 
    sizes=(2,))

get_additional_keyboard = get_keyboard(
    "👍Да, давай!",
    "⬅️Вернуться к меню",
    placeholder="Выберите действие", 
    sizes=(2,),
)


class RecipeByIngsDatails(StatesGroup):
    ingridients = State()
    details = State()
    additional = State()
    
    
@get_recipe_by_ings_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Без проблем!")
    await message.answer(menu_text, reply_markup=menu_keyboard)


@get_recipe_by_ings_router.message(StateFilter(None), F.text.casefold() == "3")
async def get_recipe(message: Message, state: FSMContext):
    await state.set_state(RecipeByIngsDatails.ingridients)
    # await asyncio.sleep(1)
    # await message.answer_sticker("CAACAgIAAxkBAAIQq2YVCX2IOu21FjwjlIK_eqU_wnx8AAIwCgAC4_woSqMD6yBTUfobNAQ")
    await message.answer("Введите продукты, которые у вас есть (через запятую)", reply_markup=cancel_keyboard)
    
    
@get_recipe_by_ings_router.message(StateFilter(RecipeByIngsDatails.ingridients), F.text)
async def get_recipe_name(message: Message, state: FSMContext):    
    await state.update_data(ingridients=message.text)
    await state.set_state(RecipeByIngsDatails.details)
    await message.answer(f"Что вы хотите (например, десерт или суп)? Укажите свои предпочтения\n" +
                         f"Если же вам все равно, то <b>введите ' - '</b>",
                         reply_markup=cancel_keyboard)
    
    
@get_recipe_by_ings_router.message(StateFilter(RecipeByIngsDatails.ingridients))
async def incorrect_message(message: Message, state: FSMContext):
    await message.answer("Не понимаю... возможно, вы использовали некорректные данные. Введите ваши продукты еще раз")
    
    
@get_recipe_by_ings_router.message(StateFilter(RecipeByIngsDatails.details), F.text)
async def get_recipe_details(message: Message, state: FSMContext, bot: Bot):    
    await state.update_data(details=message.text)
    await message.answer("Сейчас что-нибудь придумаю для вас...")
    datails = await state.get_data()
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    gpt_response = await generate_response_by_ingridients(datails)
    if gpt_response == "Не могу ничего придумать...":
        await message.answer_sticker("CAACAgIAAxkBAAIQrWYVCZdKKMAyBicW-562kmzMUoyZAAKrCwACLw_wBoLABuDn5cg3NAQ")
        await asyncio.sleep(1)
        await message.answer(gpt_response)
        await asyncio.sleep(1)
        await message.answer(recipe_start, reply_markup=get_additional_keyboard)
        await state.set_state(RecipeByIngsDatails.additional)
    else:
        await message.answer_sticker("CAACAgIAAxkBAAIQqWYVCXpgQgU7O4ExCfV_OdVYwIuqAAJ8DwACzxEgSkGaM72iUQ4iNAQ")
        await asyncio.sleep(1)
        await message.answer(gpt_response, reply_markup=functional_keyboard)
        await state.clear()
    
    
@get_recipe_by_ings_router.message(StateFilter(RecipeByIngsDatails.details))
async def incorrect_message(message: Message, state: FSMContext):
    await message.answer("Не понимаю... возможно, вы использовали некорректные данные. Введите ваши предпочтения еще раз")
    
    
@get_recipe_by_ings_router.message(StateFilter(RecipeByIngsDatails.additional), F.text=="👍Да, давай!")
async def get_additional(message: Message, state: FSMContext):
    await message.answer(recipe, reply_markup=functional_keyboard)
    await state.clear()
    
    
@get_recipe_by_ings_router.message(StateFilter(RecipeByIngsDatails.additional), F.text)
async def to_menu_from_add(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(menu_text, reply_markup=menu_keyboard)
    

@get_recipe_by_ings_router.message(StateFilter(None), F.text.casefold() == "⬅️вернуться к меню")
async def to_menu(message: Message):
    await message.answer(menu_text, reply_markup=menu_keyboard)
    
    
@get_recipe_by_ings_router.message(StateFilter(None), F.text.casefold() == "🧠подобрать новый рецепт")
async def get_recipe_again(message: Message, state: FSMContext):
    await message.answer("Без проблем!", reply_markup=ReplyKeyboardRemove())
    await get_recipe(message, state)