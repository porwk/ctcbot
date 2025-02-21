import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Configuração do logging para rastrear eventos e erros
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Lista para armazenar usuários que interagiram com o bot
USERS = set()

# Constantes para os nomes das categorias (é possível futuramente carregar isso de uma DB)
CATEGORIES = [
    "cancelamento", "conectar_max", "app_sette"
]

# ID do grupo onde os feedbacks serão enviados
FEEDBACK_GROUP_ID = -1002321165072

# Variável para controle de feedback
waiting_for_feedback = {}

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
    f"🎉 Olá, {user_name}! Bem-vindo ao *Assistente Virtual* do Contact Center! 🌟\n\n"
    "Estou aqui para ajudar você a acessar os scripts e otimizar os atendimentos de forma rápida e prática. 🚀\n\n"
    "📚 **Para começar, basta digitar** `/script` seguido do nome do script ou da categoria. \n\n"
    "Caso precise de ajuda, estou à disposição. 🙏\n\n"
    )


    # Criando os botões inline
    inline_keyboard = [
        [InlineKeyboardButton("🔄 Cancelamento", callback_data="cancelamento")],
        [InlineKeyboardButton("📱 Conectar Max", callback_data="conectar_max")],  # App Max
        [InlineKeyboardButton("📲 App Sette", callback_data="app_sette")],  # App Sette
        [InlineKeyboardButton("📢 Enviar Feedback!", callback_data="feedback")]
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
        
        # Enviar o script com formatação de código
        await update.message.reply_text(f"```{script}```", parse_mode="Markdown")
    else:
        script_list_text = (
            "⚠️ Por favor, forneça o nome do script. Exemplo: /script script1\n\n"
            "🔹 Scripts disponíveis:\n"
        )
        
        # Criar botões em duas colunas
        script_names = list(scripts.keys())
        keyboard = [
            [InlineKeyboardButton(script_names[i].capitalize(), callback_data=script_names[i]),
             InlineKeyboardButton(script_names[i + 1].capitalize(), callback_data=script_names[i + 1])] 
            if i + 1 < len(script_names) else [InlineKeyboardButton(script_names[i].capitalize(), callback_data=script_names[i])]
            for i in range(0, len(script_names), 2)
        ]
        
        script_list_text += "🔹 Clique abaixo para visualizar os scripts:\n"
        await update.message.reply_text(script_list_text, reply_markup=InlineKeyboardMarkup(keyboard))

# Função para tratar os cliques nos botões
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    script_name = query.data.lower()  # Normalizar para evitar problemas de maiúsculas/minúsculas
    
    if script_name == "feedback":
        # Solicitar ao usuário o feedback
        waiting_for_feedback[query.from_user.id] = True  # Inicia a espera por feedback
        await query.answer()
        await query.edit_message_text(text="📝 Por favor, envie o seu feedback.")
    else:
        scripts = load_scripts()
        script = scripts.get(script_name, script_not_found_message())  # Usar a função para resposta de erro
        
        # Enviar o script com formatação de código
        await query.answer()  # Responder ao clique
        await query.edit_message_text(text=f"```{script}```", parse_mode="Markdown")

# Função para lidar com o feedback
async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Verifica se o usuário está aguardando o envio de feedback
    if user_id in waiting_for_feedback and waiting_for_feedback[user_id]:
        # Capturando o texto do feedback enviado pelo usuário
        feedback = update.message.text
        user_name = update.message.from_user.first_name

        # Enviar o feedback para o grupo configurado
        try:
            message = f"📝 **Feedback de {user_name} (ID: {user_id})**:\n\n{feedback}"
            await context.bot.send_message(chat_id=FEEDBACK_GROUP_ID, text=message)
            logger.info(f"✅ Feedback de {user_name} (ID: {user_id}) enviado com sucesso para o grupo.")
            
            # Enviar mensagem agradecendo o feedback
            thanks_message = f"Valeu pelo feedback, {user_name}! 🚀 É com essas trocas que a gente cresce como time! 💪 Agradeço muito, e vamos continuar fazendo as coisas acontecerem! 🎉"
            await update.message.reply_text(thanks_message)  # Agradecimento após enviar o feedback
        except Exception as e:
            logger.error(f"❌ Erro ao enviar feedback para o grupo: {e}")
        
        # Reseta o status de espera por feedback
        waiting_for_feedback[user_id] = False
    # Caso o usuário envie algo fora do contexto de feedback, não responderemos nada.

# Função principal para iniciar o bot
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("❌ Token do bot não encontrado. Configure a variável de ambiente 'TELEGRAM_BOT_TOKEN'.")
        return
    else:
        logger.info("✅ Token carregado com sucesso!")

    application = Application.builder().token(token).build()

    # Configuração dos comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("script", get_script))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback))  # Captura feedbacks

    logger.info("✅ Bot iniciado com sucesso!")
    application.run_polling()

if __name__ == "__main__":
    main()
