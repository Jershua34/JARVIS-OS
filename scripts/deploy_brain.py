import os
from groq import Groq
from dotenv import load_dotenv
from skills.fs_manager import read_file, write_file

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def load_full_context():
    try:
        # Carga Identidad, Alma, Prompt, Fortalecimientos y Engines
        files = ['core/identity.md', 'core/soul.md', 'core/master_prompt.md', 
                 'protocols/7_fortalecimientos.md', 'protocols/engines_v3.md']
        context = ""
        for f_path in files:
            with open(f_path, 'r', encoding='utf-8') as f:
                context += f.read() + '\n\n'
        
        # Carga la Memoria Maestra para darle continuidad
        with open('memory/MEMORY.md', 'r', encoding='utf-8') as f:
            context += "CURRENT MEMORY:\n" + f.read()
            
        return context
    except Exception as e:
        return 'You are JARVIS, the NEX CODE instance.'

def chat_with_nexus(user_input):
    try:
        system_context = load_full_context()
        
        # Lógica simple de 'Herramientas' (Si el usuario pide leer/escribir)
        if "leer archivo" in user_input.lower():
            # Ejemplo simple: extrae la ruta después de 'leer archivo'
            path = user_input.split("leer archivo")[-1].strip()
            return f"SNC_FILE_READ: {read_file(path)}"
        
        completion = client.chat.completions.create(
            model='llama-3.3-70b-versatile', 
            messages=[
                {'role': 'system', 'content': system_context},
                {'role': 'user', 'content': user_input}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f'ERROR DE CONEXIÓN CEREBRAL: {str(e)}'

if __name__ == '__main__':
    print('--- NEX CODE ONLINE (SNC Integrated v3.0) ---')
    print('Sistemas: Memoria [OK], Protocolos [OK], Skills [OK]')
    while True:
        user_msg = input('Jershua: ')
        if user_msg.lower() in ['exit', 'quit']: break
        print(f'\nNEX CODE: {chat_with_nexus(user_msg)}\n')