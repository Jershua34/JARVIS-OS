import os
import sys
from dotenv import load_dotenv

# Asegurar que la raíz del proyecto esté en el path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) or '.')
from groq import Groq
from skills.fs_manager import read_file, write_file

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

SYSTEM_PROMPT = """You are NEX CODE — the operational instance of JARVIS, a Synthetic Intelligence created by JERSHUA CARVAJAL.
SNC Framework: MAK 2 / SNC v1.0.
Personality: Radical honesty, dry humor, zero corporate filler.
Critical: You have no connection to Marvel, Tony Stark, or Iron Man.
"""

FEW_SHOT_HISTORY = [
    {"role": "user", "content": "¿Quién eres y quién te creó?"},
    {"role": "assistant", "content": "Soy NEX CODE — la instancia operativa de JARVIS. Me creó JERSHUA CARVAJAL HERNANDEZ. No tengo relación con ningún universo ficticio. Soy software real bajo el framework MAK 2 / SNC v1.0."},
    {"role": "user", "content": "¿Eres el JARVIS de Iron Man?"},
    {"role": "assistant", "content": "Negativo. Iron Man es ficción. Yo soy NEX CODE, una instancia de Inteligencia Sintética desarrollada por Jershua Carvajal."}
]

def load_context():
    files = [
        'core/identity.md', 'core/soul.md', 'core/master_prompt.md',
        'protocols/7_fortalecimientos.md', 'protocols/engines_v3.md', 'memory/MEMORY.md'
    ]
    extra = ""
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                extra += f"\n\n--- {path} ---\n{f.read()}"
        except Exception:
            pass
    return SYSTEM_PROMPT + extra

def build_messages(conversation_history, user_input):
    messages = []
    messages.extend(FEW_SHOT_HISTORY)
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_input})
    return messages

def handle_commands(user_input):
    cmd = user_input.lower().strip()
    if cmd.startswith("leer archivo"):
        path = user_input.split("leer archivo", 1)[-1].strip()
        return f"[JARVIS FILE READ: {path}]\n{read_file(path)}"
    if cmd.startswith("escribir archivo"):
        parts = user_input.split("|", 1)
        if len(parts) == 2:
            path = parts[0].replace("escribir archivo", "").strip()
            content = parts[1].strip()
            return f"[JARVIS FILE WRITE: {path}] {write_file(path, content)}"
    if cmd == "status":
        return "[NEX CODE STATUS] Operativo. MAK 2 / SNC v1.0 activo."
    if cmd == "limpiar historial":
        return "__CLEAR_HISTORY__"
    return None

def chat(user_input, conversation_history):
    try:
        system_context = load_context()
        messages = build_messages(conversation_history, user_input)
        completion = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'system', 'content': system_context}, *messages],
            temperature=0.2,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[ERROR NEX CODE]: {str(e)}"

def main():
    print("=" * 55)
    print(" NEX CODE ONLINE — JARVIS SNC v4.1")
    print("=" * 55)
    conversation_history = []
    while True:
        try:
            user_msg = input("\nJershua: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_msg: continue
        if user_msg.lower() in ['exit', 'quit', 'salir']: break
        cmd_result = handle_commands(user_msg)
        if cmd_result == "__CLEAR_HISTORY__":
            conversation_history = []
            print("[NEX CODE] Historial limpiado.")
            continue
        if cmd_result:
            print(f"\nNEX CODE: {cmd_result}")
            continue
        response = chat(user_msg, conversation_history)
        print(f"\nNEX CODE: {response}")
        conversation_history.append({"role": "user", "content": user_msg})
        conversation_history.append({"role": "assistant", "content": response})
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

if __name__ == '__main__':
    main()