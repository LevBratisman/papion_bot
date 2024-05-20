import g4f


# -------------------Найти рецепт по названию блюда--------------------

def generate_request(text: str) -> str:
    request = f'Напиши необходимые ингридиенты и пошаговый рецепт для приготовления блюда - {text}. Сгенерируй ответ без вступления и заключения, только ингридиенты (в граммовках) и пошаговый рецепт. Если такого блюда не существует, то выведи "Не могу ничего придумать...".'
    return request

def generate_response(recipe: str) -> str:
    request = generate_request(recipe)
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            provider=g4f.Provider.AItianhuSpace,
            messages=[{"role": "user", "content": request}],
            stream=True
        )
        
        response_message = ''
        for message in response:
            response_message += message.replace('*', '')
            
    except Exception as e:
        print(e)
        response_message = 'Не могу ничего придумать...'
        
    return response_message

# ---------------------Найти рецепт по ингридиентам--------------------

def generate_request_by_ingridients(details: dict) -> str:
    request = f'Придумай или найди рецепт используя данные ингридиенты - {details["ingridients"]}, при этом учитывая следующие пожелания - {details["details"]}. Сгенерируй ответ без вступления и заключения, только ингридиенты (в граммовках) и пошаговый рецепт. Если ты не можешь придумать рецепт, то выведи "Не могу ничего придумать...".'
    return request

def generate_response_by_ingridients(recipe: dict) -> str:
    request = generate_request_by_ingridients(recipe)
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            provider=g4f.Provider.FreeGpt,
            messages=[{"role": "user", "content": request}],
            stream=True
        )
        
        response_message = ''
        for message in response:
            response_message += message.replace('*', '')
            
    except Exception as e:
        print(e)
        response_message = 'Не могу ничего придумать...'
        
    return response_message


# --------------------Найти рецепт по предпочтениям--------------------


def generate_request_random(details: str) -> str:
    request = f'Придумай или найди рецепт учитывая следующие детали - {details}, если деталей нет, то выведи случайный рецепт какого-нибудь десерта. Сгенерируй ответ без вступления и заключения, только ингридиенты (в граммовках) и пошаговый рецепт. Если ты не можешь придумать рецепт, то выведи "Не могу ничего придумать...".'
    return request

def generate_response_random(recipe: str) -> str:
    request = generate_request_random(recipe)
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            provider=g4f.Provider.FreeGpt,
            messages=[{"role": "user", "content": request}],
            stream=True
        )
        
        response_message = ''
        for message in response:
            response_message += message.replace('*', '')
            
    except Exception as e:
        print(e)
        response_message = 'Не могу ничего придумать...'
        
    return response_message




# --------------------GPT-4-Free--------------------

# import g4f
# response = g4f.ChatCompletion.create(
#     model=g4f.models.gpt_4,
#     messages=[{"role": "user", "content": "Hello"}],
#     provider=g4f.Provider.Liaobots,
#     stream=True,
# )

# for message in response:
#     print(message)