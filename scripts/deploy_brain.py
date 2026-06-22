import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def load_core():
    try:
        with open('core/identity.md', 'r', encoding='utf-8') as f: identity = f.read()
        with open('core/soul.md', 'r', encoding='utf-8') as f: soul = f.read()
        with open('core/master_prompt.md', 'r', encoding='utf-8') as f: prompt = f.read()
        return f'{identity}\n\n{soul}\n\n{prompt}'
    except Exception as e:
        return 'You are JARVIS, the NEX CODE instance.'

def chat_with_nexus(user_input):
    try:
        system_message = load_core()
        # Usamos la versión más estable y potente de Llama 3.3
        completion = client.chat.completions.create(
            model='llama-3.3-70b-versatile', 
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': user_input}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f'ERROR DE CONEXIÓN CEREBRAL: {str(e)}'

if __name__ == '__main__':
    print('--- NEX CODE ONLINE (Stable Core v2.2) ---')
    while True:
        user_msg = input('Jershua: ')
        if user_msg.lower() in ['exit', 'quit']: break
        print(f'\nNEX CODE: {chat_with_nexus(user_msg)}\n')