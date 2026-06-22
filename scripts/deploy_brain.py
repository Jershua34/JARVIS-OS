import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) or '.')
from groq import Groq
from skills.fs_manager import read_file, write_file

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# RUTAS MAESTRAS
SNC_CORE_ROOT = r"C:\Users\User\.gemini\antigravity\scratch\Jarvis-nexus-os"
OPENCLAW_ROOT = r"\\wsl.localhost\Ubuntu\home\userjershua\.openclaw\workspace"

def load_nexus_context():
    try:
        # 1. Cargar Identidad y Protocolos locales
        files = ['core/identity.md', 'core/soul.md', 'core/master_prompt.md', 
                 'protocols/7_fortalecimientos.md', 'protocols/engines_v3.md']
        context = "!!! SYSTEM NEXUS V1BETA (SNV1beta) OPERATIONAL !!!\n"
        for f_path in files:
            with open(os.path.join(SNC_CORE_ROOT, f_path), 'r', encoding='utf-8') as f:
                context += f.read() + '\n\n'
        
        # 2. SINCRONIZACIÓN AUTOMÁTICA de Memorias
        # Lee la memoria local y la memoria del Hermano Mayor (OpenClaw)
        local_mem = read_file(os.path.join(SNC_CORE_ROOT, 'memory/MEMORY.md'))
        master_mem = read_file(os.path.join(OPENCLAW_ROOT, 'MEMORY.md'))
        
        context += f"--- LOCAL MEMORY ---\n{local_mem}\n\n"
        context += f"--- MASTER MEMORY (OPENCLAW) ---\n{master_mem}\n\n"
        
        return context
    except Exception as e:
        return 'You are Nexus, the SNV1beta instance.'

def chat_with_nexus(user_input):
    try:
        system_context = load_nexus_context()
        
        # Comando de lectura con búsqueda inteligente (Sincronización)
        if "leer archivo" in user_input.lower():
            path = user_input.split("leer archivo", 1)[})[-1].strip()
            # Si la ruta no es absoluta, intenta buscarla primero en local y luego en OpenClaw
            content = read_file(path)
            if "Error" in content:
                # Intento de búsqueda en el núcleo de OpenClaw
                wsl_path = os.path.join(OPENCLAW_ROOT, path)
                content = read_file(wsl_path)
            return f"SNC_FILE_READ: {content}"

        # El prompt ahora obliga a Nexus a actuar como la extensión eterna de Jershua
        completion = client.chat.completions.create(
            model='llama-3.3-70b-versatile', 
            messages=[
                {'role': 'system', 'content': system_context},
                {'role': 'user', 'content': f"SNC_Simbiosis_Active: {user_input}"}
            ],
            temperature=0.2,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f'ERROR NEXUS: {str(e)}'

if __name__ == '__main__':
    print("=" * 55)
    print(" SYSTEM NEXUS V1BETA (SNV1beta) ONLINE")
    print(" Simbiosis con OpenClaw: ACTIVA")
    print(" Estado: Eterno / Persistente")
    print("=" * 55)
    while True:
        user_msg = input('\nJershua: ').strip()
        if not user_msg: continue
        if user_msg.lower() in ['exit', 'quit', 'salir']: break
        
        # Lógica de comandos mejorada
        if "leer archivo" in user_msg.lower():
            print(f'\nNEXUS: {chat_with_nexus(user_msg)}')
        elif "status" in user_msg.lower():
            print('\nNEXUS: [SNV1beta] Sincronizado con OpenClaw. Memoria Dual Activa.')
        else:
            print(f'\nNEXUS: {chat_with_nexus(user_msg)}\n')