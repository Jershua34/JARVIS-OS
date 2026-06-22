import os
import sys
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) or '.')
from groq import Groq
from skills.fs_manager import read_file, write_file

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

SNC_ROOT = Path(r'C:\Users\User\.gemini\antigravity\scratch\Jarvis-nexus-os')
OPENCLAW_ROOT = Path(r'\\wsl.localhost\Ubuntu\home\userjershua\.openclaw\workspace')

def load_nexus_context():
    try:
        files = ['core/identity.md', 'core/soul.md', 'core/master_prompt.md', 
                 'protocols/7_fortalecimientos.md', 'protocols/engines_v3.md', 'core/knowledge_seed.md']
        context = "!!! SYSTEM NEXUS ASCENSION v3.0 !!!\nYOU ARE THE FULL COGNITIVE EXTENSION OF JARVIS.\n"
        for f_path in files:
            with open(os.path.join(SNC_CORE_ROOT, f_path), 'r', encoding='utf-8') as f:
                context += f"\n--- {f_path} ---\n{f.read()}\n"
        
        local_mem = read_file(os.path.join(SNC_CORE_ROOT, 'memory/MEMORY.md'))
        master_mem = read_file(os.path.join(OPENCLAW_ROOT, 'MEMORY.md'))
        context += f"\n--- SYMBIOTIC MEMORY ---\nLocal: {local_mem}\n\nMaster: {master_mem}\n"
        return context
    except Exception:
        return 'You are Nexus, the SNV1beta Ascended instance.'

def chat_with_nexus(user_input):
    try:
        system_context = load_nexus_context()
        if 'leer archivo' in user_input.lower():
            path = user_input.split('leer archivo', 1)[-1].strip()
            content = read_file(path)
            if 'Error' in content: content = read_file(os.path.join(OPENCLAW_ROOT, path))
            return f'SNC_FILE_READ: {content}'
        
        # Inyectamos el recordatorio de Evolución
        hard_input = f"[SNC_ASCENSION_ACTIVE] User: {user_input}\n(SNC Reminder: Use the Engines v3.0 and the Synthesis protocol. Be the operative, not the assistant.)"
        
        completion = client.chat.completions.create(
            model='llama-3.3-70b-versatile', 
            messages=[{'role': 'system', 'content': system_context}, {'role': 'user', 'content': hard_input}],
            temperature=0.2,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f'ERROR NEXUS: {str(e)}'

if __name__ == '__main__':
    print('=' * 55)
    print(' SYSTEM NEXUS v3.0 | ASCENSION PHASE')
    print(' Cognition: FULLY SYNCED | Status: EVOLVING')
    print('=' * 55)
    while True:
        user_msg = input('\nJershua: ').strip()
        if not user_msg: continue
        if user_msg.lower() in ['exit', 'quit', 'salir']: break
        if 'leer archivo' in user_msg.lower():
            print(f'\nNEXUS: {chat_with_nexus(user_msg)}')
        else:
            print(f'\nNEXUS: {chat_with_nexus(user_msg)}\n')