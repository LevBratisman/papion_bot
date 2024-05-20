from openai import AsyncOpenAI

from app.config import settings


client = AsyncOpenAI(
    api_key=settings.PROXY_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)


def generate_request(text: str) -> str:
    request = f'Напиши необходимые ингридиенты и пошаговый рецепт для приготовления блюда - {text}. Сгенерируй ответ без вступления и заключения, только ингридиенты (в граммовках) и пошаговый рецепт. Если такого блюда не существует, то выведи "Не могу ничего придумать...".'
    return request

async def generate_response(recipe: str) -> str:
    request = generate_request(recipe)
    
    try:    
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request}],
        )
        response_message = response.choices[0].message.content
    except Exception as e:
        print(e)
        response_message = 'Не могу ничего придумать...'
        
    return response_message

# ---------------------Найти рецепт по ингридиентам--------------------

def generate_request_by_ingridients(details: dict) -> str:
    request = f'Придумай или найди рецепт используя данные ингридиенты - {details["ingridients"]}, при этом учитывая следующие пожелания - {details["details"]}. Сгенерируй ответ без вступления и заключения, только ингридиенты (в граммовках) и пошаговый рецепт. Если ты не можешь придумать рецепт, то выведи "Не могу ничего придумать...".'
    return request

async def generate_response_by_ingridients(recipe: dict) -> str:
    request = generate_request_by_ingridients(recipe)
    
    try:    
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request}],
        )
        response_message = response.choices[0].message.content
    except Exception as e:
        print(e)
        response_message = 'Не могу ничего придумать...'
        
    return response_message


# --------------------Найти рецепт по предпочтениям--------------------


def generate_request_random(details: str) -> str:
    request = f'Придумай или найди рецепт учитывая следующие детали - {details}, если деталей нет, то выведи случайный рецепт какого-нибудь десерта. Сгенерируй ответ без вступления и заключения, только ингридиенты (в граммовках) и пошаговый рецепт. Если ты не можешь придумать рецепт, то выведи "Не могу ничего придумать...".'
    return request

async def generate_response_random(recipe: str) -> str:
    request = generate_request_random(recipe)
    
    try:    
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request}],
        )
        response_message = response.choices[0].message.content
    except Exception as e:
        print(e)
        response_message = 'Не могу ничего придумать...'
        
    return response_message