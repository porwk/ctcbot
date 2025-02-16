import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração do logging para rastrear eventos e erros
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constantes para os nomes das categorias (é possível futuramente carregar isso de uma DB)
CATEGORIES = [
    "Cancelamento", "Conectar_max", "Los", "Transferencia_endereco", "App_sette"
]

# Flag para controlar se o bot está ativo ou não
BOT_ATIVO = True  # Defina como True para ativar o bot

# Função para carregar os scripts (simulada aqui, mas poderia ser de um banco de dados)
def load_scripts():
    try:
        from scripts import scripts
        return scripts
    except ImportError:
        logger.error("❌ Não foi possível carregar o arquivo 'scripts.py'. Verifique se o arquivo existe.")
        return {}

# Função de resposta em caso de erro para evitar duplicação de código
def script_not_found_message():
    return "❌ Script não encontrado! Certifique-se de que o nome está correto."

# Função para lidar com o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # Obtendo o nome do usuário
    welcome_text = (
        f"👋 Olá, {user_name}! Seja muito bem-vindo ao **Assistente Virtual** do Contact Center. 🌟\n\n"
        "🔧 Estou aqui para facilitar sua jornada! Comigo, você pode acessar scripts de forma rápida e prática, e assim, otimizar seu atendimento. 💬\n\n"
        "📚 Para começar, digite o comando `/script` seguido do nome do script ou da categoria que você deseja explorar. Se precisar de ajuda, não hesite em me chamar!\n\n"
        "💡 E lembre-se: sua opinião é muito importante! Se tiver sugestões ou feedbacks, compartilhe comigo e ajude a melhorar nossa experiência juntos. 🚀\n\n"
        "🔘 Agora, escolha uma das opções abaixo para começar a explorar os scripts. Eu estou à disposição para ajudar no que for preciso!"
    )

    # Criando os botões inline
    inline_keyboard = [
        [InlineKeyboardButton(category.capitalize(), callback_data=category)] 
        for category in CATEGORIES
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    # Enviando mensagem com os botões inline
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Função para lidar com o comando /script
async def get_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scripts = load_scripts()  # Carregar os scripts do arquivo 'scripts.py'
    
    # Verificar se o nome do script foi fornecido
    if context.args:
        script_name = context.args[0].lower()  # Normalizar para evitar problemas de maiúsculas/minúsculas
        script = scripts.get(script_name, script_not_found_message())
        await update.message.reply_text(script)
    else:
        script_list_text = (
            "⚠️ Por favor, forneça o nome do script. Exemplo: /script script1\n\n"
            "🔹 Scripts disponíveis:\n"
        )
        
        # Organiza os botões em duas colunas
        script_keys = list(scripts.keys())
        keyboard = [
            [InlineKeyboardButton(script_keys[i].capitalize(), callback_data=script_keys[i]),
             InlineKeyboardButton(script_keys[i+1].capitalize(), callback_data=script_keys[i+1])] 
            for i in range(0, len(script_keys)-1, 2)
        ]

        # Se houver um número ímpar de scripts, adiciona o último botão sozinho
        if len(script_keys) % 2 != 0:
            keyboard.append([InlineKeyboardButton(script_keys[-1].capitalize(), callback_data=script_keys[-1])])

        script_list_text += "🔹 Clique abaixo para visualizar os scripts:\n"
        await update.message.reply_text(script_list_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Função para tratar os cliques nos botões
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    script_name = query.data.lower()  # Normalizar para evitar problemas de maiúsculas/minúsculas
    
    scripts = load_scripts()
    script = scripts.get(script_name, script_not_found_message())  # Usar a função para resposta de erro
    
    await query.answer()  # Responder ao clique
    await query.edit_message_text(text=script)

# Função principal para iniciar o bot
def main():
    # Testando o carregamento da variável de ambiente
    token = os.getenv("TELEGRAM_BOT_TOKEN")
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
