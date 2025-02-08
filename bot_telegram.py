import os
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from typing import Dict

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variáveis globais para cache
CACHE_TIME = 3600  # Cache expira em 1 hora (3600 segundos)
cache = {
    "scripts": None,
    "last_updated": 0
}

# Função para carregar os scripts a partir do arquivo scripts.py com cache
def load_scripts() -> Dict[str, str]:
    current_time = time.time()
    
    # Verificar se o cache ainda é válido
    if cache["scripts"] is not None and (current_time - cache["last_updated"]) < CACHE_TIME:
        logger.info("✅ Usando cache de scripts.")
        return cache["scripts"]
    
    # Se o cache expirou ou não existe, recarregar os scripts
    try:
        from scripts import scripts
        if not isinstance(scripts, dict):
            raise ValueError("O conteúdo de 'scripts.py' não é um dicionário válido.")
        cache["scripts"] = scripts
        cache["last_updated"] = current_time
        logger.info("✅ Scripts carregados com sucesso e cache atualizado.")
        return scripts
    except ImportError:
        logger.error("❌ Não foi possível carregar o arquivo scripts.py. Verifique se o arquivo existe.")
    except ValueError as e:
        logger.error(f"❌ Erro ao verificar o conteúdo de 'scripts.py': {e}")
    except Exception as e:
        logger.error(f"❌ Ocorreu um erro desconhecido ao carregar 'scripts.py': {e}")
    return {}

# Função para lidar com o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # Nome do usuário
    await update.message.reply_text(
        f"👋 Olá, {user_name}! Bem-vindo ao Assistente Virtual de Scripts do Contact Center. 🎯\n\n"
        "💼 Este bot foi desenvolvido para facilitar o acesso aos scripts e aprimorar seu atendimento.\n\n"
        "📋 Para acessar os scripts, digite o comando /script seguido do nome da categoria ou do script que você deseja consultar.\n\n"
        "🔘 **Escolha a categoria de script** que você deseja acessar abaixo e clique para visualizar os detalhes.\n\n"
        "📢 Sua opinião é essencial! Envie sugestões para continuarmos melhorando.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Atendimento", callback_data="atendimento")],
                [InlineKeyboardButton("Principais", callback_data="principais")],
                [InlineKeyboardButton("Serviços", callback_data="servicos")],
                [InlineKeyboardButton("Renovação Contratual", callback_data="renovacao_contratual")],
                [InlineKeyboardButton("Outros Scripts", callback_data="outros_scripts")]
            ]
        )
    )

# Função para lidar com o comando /script
async def get_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scripts = load_scripts()  # Carregar os scripts do arquivo scripts.py
    
    # Verificar se o nome do script foi fornecido
    if context.args:
        script_name = context.args[0].lower()  # Normalizar para evitar problemas de maiúsculas/minúsculas
        script = scripts.get(script_name, "❌ Script não encontrado! Certifique-se de que o nome está correto.")
    else:
        script = "⚠️ Por favor, forneça o nome do script. Exemplo: /script script1\n\n"
        script += "🔹 Scripts disponíveis:\n"
        
        # Organizar os botões lado a lado
        # Agrupar os botões em várias colunas, independentemente da quantidade
        keyboard = []
        script_names = list(scripts.keys())
        
        # Vamos distribuir os botões em colunas de 3
        for i in range(0, len(script_names), 3):  # Passo 3 para distribuir em colunas
            row = []
            for j in range(i, min(i + 3, len(script_names))):  # Verifica se há 3 itens para cada linha
                row.append(InlineKeyboardButton(script_names[j].capitalize(), callback_data=script_names[j]))
            keyboard.append(row)
        
        script += "🔹 Clique abaixo para visualizar os scripts:\n"
        await update.message.reply_text(
            script,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Função para tratar os cliques nos botões
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    script_name = query.data.lower()  # Normalizar para evitar problemas de maiúsculas/minúsculas

    # Carregar os scripts
    scripts = load_scripts()
    script = scripts.get(script_name, "❌ Script não encontrado. Tente novamente!")

    await query.answer()  # Responder ao clique
    await query.edit_message_text(text=script)

# Função para verificar variáveis de ambiente de maneira mais segura
def check_environment_variables() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("❌ Token do bot não encontrado. Configure a variável de ambiente 'TELEGRAM_BOT_TOKEN'.")
        raise ValueError("Token do bot não configurado")
    return token

# Função principal para iniciar o bot
def main():
    try:
        token = check_environment_variables()  # Valida se o token foi configurado
    except ValueError:
        return

    # Criação da aplicação do bot
    application = Application.builder().token(token).build()

    # Configuração dos comandos
    application.add_handler(CommandHandler("start", start))  # Comando /start
    application.add_handler(CommandHandler("script", get_script))  # Comando /script <nome_do_script>
    application.add_handler(CallbackQueryHandler(button))  # Resposta aos botões clicáveis

    # Inicia o bot em modo polling
    logger.info("✅ Bot iniciado com sucesso!")
    application.run_polling()

if __name__ == "__main__":
    main()
