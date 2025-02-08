import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Função para carregar os scripts a partir do arquivo scripts.py
def load_scripts():
    try:
        # Supondo que o arquivo 'scripts.py' tenha um dicionário de scripts
        from scripts import scripts
        return scripts
    except ImportError:
        logger.error("❌ Não foi possível carregar o arquivo scripts.py. Verifique se o arquivo existe.")
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
        
        # Criar botões clicáveis para os scripts
        keyboard = [
            [InlineKeyboardButton(script_name.capitalize(), callback_data=script_name)] 
            for script_name in scripts.keys()
        ]
        
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

# Função principal para iniciar o bot
def main():
    # Testando o carregamento da variável de ambiente
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    print(f"Token do bot: {token}")  # Isso deve exibir o token no terminal

    if not token:
        logger.error("❌ Token do bot não encontrado. Configure a variável de ambiente 'TELEGRAM_BOT_TOKEN'.")
        return
    else:
        logger.info("✅ Token carregado com sucesso!")

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
