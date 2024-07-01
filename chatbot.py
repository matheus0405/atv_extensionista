from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

# Dados de coletas para cada bairro
BAIRROS = {
    "Condá": {
        "orgânico": "segunda, quarta e sexta-feira, com início 7:30h A.M.",
        "reciclável": "Segunda-feira, com início 8:00h A.M."
    },
    "Belo Horizonte": {
        "orgânico": "segunda, quarta e sexta-feira, com início 7:30h A.M.",
        "reciclável": "Segunda-feira, com início 8:00h A.M."
    },
    "Frimesa": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Sexta-feira, com início 8:00h A.M."
    },
    "Jardim Irene": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Sexta-feira, com início 8:00h A.M."
    },
    "Paraíso": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Sexta-feira, com início 8:00h A.M."
    },
    "Independência": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Quarta-feira, com início 8:00h A.M"
    },
    "Itaipu": {
        "orgânico": "segunda, quarta e sexta-feira, com início 7:30 A.M.",
        "reciclável": "Quarta-feira, com início 8:00h A.M."
    },
    "São Cristóvão": {
        "orgânico": "segunda, quarta e sexta-feira, com início 7:30 A.M.",
        "reciclável": "Quarta-feira, com início 8:00h A.M."
    },
    "Centro": {
        "orgânico": "diária, com início 13:30h P.M.",
        "reciclável": "Terça-feira, com início 8:00h A.M."
    },
    "Ipê": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Quinta-feira, com início 8:00h A.M."
    },
    "Cidade alta": {
        "orgânico": "diária, com início 7:30h A.M.",
        "reciclável": "Quinta-feira, com início 8:00h A.M."
    },
    "Nazaré": {
        "orgânico": "terça, quinta e sábado, com início  7:30h A.M.",
        "reciclável": "Quinta-feira, início 8:00h A.M."
    },
    "Panorâmico": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Terça-feira, com início 8:00h A.M"
    },
    "Santos Dumont": {
        "orgânico": "terça, quinta e sábado, com início 7:30h A.M.",
        "reciclável": "Terça-feira, com início 8:00h A.M"
    }
}

#cria e treina bot
chatbot = ChatBot('Limpamed')
trainer = ListTrainer(chatbot)

trainer.train([
    "Olá, como vai?",
    "Vou bem, e você?",
    "Como voce se chama?",
    "Me chamo chatbot Limpamed, o seu chat amigo! Estou aqui para te responder perguntas sobre a coleta de lixo orgânico e reciclavel!",
    "Qual seu nome?",
     "Me chamo chatbot Limpamed, o seu chat amigo! Estou aqui para te responder perguntas sobre a coleta de lixo orgânico e reciclavel!",
     "O que voce faz?",
     "Estou aqui para te responder perguntas sobre a coleta de lixo orgânico e reciclavel!"

])

trainer.train([
    "Qual é a diferença entre lixo orgânico e reciclável?",
    "Lixo orgânico é composto por resíduos de origem biológica, como restos de comida, cascas de frutas e legumes. Lixo reciclável inclui materiais como papel, plástico, vidro e metal que podem ser reprocessados e reutilizados.",
    "Qual a importância da separação do lixo?",
    "Separar o lixo é importante para facilitar a reciclagem, reduzir a quantidade de resíduos enviados aos aterros sanitários e diminuir a poluição ambiental.",
    "O que é lixo orgânico?",
    "Lixo orgânico é composto por resíduos de origem biológica, como restos de comida, cascas de frutas e legumes.",
    "O que é lixo reciclável?",
    "Lixo reciclável inclui materiais como papel, plástico, vidro e metal que podem ser reprocessados e reutilizados.",
    "Qual a importância do descarte correto?",
    "O descarte correto do lixo evita a contaminação do solo e da água, reduz a poluição e ajuda a conservar os recursos naturais."
])

trainer.train([
    "Me de exemplos de lixo orgânico",
    "Lixo orgânico é composto por resíduos de origem biológica que podem se decompor naturalmente. Exemplos comuns incluem restos de alimentos como cascas de frutas e legumes, borras de café, ossos, restos de carne, cascas de ovos e pão. Além disso, resíduos de jardinagem como folhas caídas, grama cortada e galhos pequenos, bem como papel e papelão sujos, como guardanapos usados e caixas de pizza sujas, também são considerados lixo orgânico. Estes materiais podem ser utilizados em compostagem, criando adubo orgânico que melhora a saúde do solo.",
    "Me de exemplos de lixo reciclável",
    "Por outro lado, lixo reciclável consiste em materiais que podem ser reprocessados e transformados em novos produtos. Exemplos incluem plásticos como garrafas de refrigerante e água, embalagens de produtos de limpeza, sacolas plásticas e potinhos de iogurte. Metais também são recicláveis, como latas de alumínio de bebidas e latas de aço de alimentos. Papéis, incluindo jornais, revistas, caixas de papelão, papéis de escritório e embalagens de papel, podem ser reciclados. Além disso, vidros, como garrafas, potes e frascos, e certos tipos de embalagens longa vida, como caixas de leite e suco, também podem ser reciclados."
])


#start do bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Cria um teclado com opções
    keyboard = [
        [InlineKeyboardButton("Verificar coletas", callback_data='verificar_coletas')],
        [InlineKeyboardButton("Conversar com chatbot Limpamed", callback_data='conversar_chatbot')],
        [InlineKeyboardButton("Receber notificações", callback_data='receber_notificacoes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)


#menu principal
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Verificar coletas", callback_data='verificar_coletas')],
        [InlineKeyboardButton("Conversar com chatbot Limpamed", callback_data='conversar_chatbot')],
        [InlineKeyboardButton("Receber notificações", callback_data='receber_notificacoes')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)

#Funcao respostas bot
async def chat_itrv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message.lower() == '/sair':
        await show_main_menu(update, context)
    else:
        bot_response = chatbot.get_response(user_message)
        await update.message.reply_text(str(bot_response))

#devolve opcoes bot
async def button_opt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    #opcao consulta bairros
    if query.data == 'verificar_coletas':
        keyboard = [[InlineKeyboardButton(bairro, callback_data=bairro)] for bairro in BAIRROS.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Escolha um bairro:", reply_markup=reply_markup)
    elif query.data in BAIRROS:
        bairro = query.data
        coletas = BAIRROS[bairro]
        resposta = f"Coletas no bairro {bairro}:\n\nLixo orgânico: {coletas['orgânico']}\nLixo reciclável: {coletas['reciclável']}"
        await query.message.reply_text(resposta)
        await show_main_menu(update, context)
    
#mostra bairros
    elif query.data in BAIRROS:
        bairro = query.data
        coletas = BAIRROS[bairro]
        resposta = f"Coletas no bairro {bairro}:\n\nLixo orgânico: {coletas['orgânico']}\nLixo reciclável: {coletas['reciclável']}"
        await query.message.reply_text(resposta)
        await show_main_menu(update, context)

    elif query.data == 'conversar_chatbot':
        await query.message.reply_text("Olá, eu sou o chatbot Limpamed! Estou aqui para te responder perguntas sobre lixo orgânico e lixo reciclável :) \nPara sair, digite /sair")

    #notificacoes
    elif query.data == 'receber_notificacoes':
        keyboard = [[InlineKeyboardButton(bairro, callback_data=f"notificar_{bairro}")] for bairro in BAIRROS.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Escolha um bairro para receber notificações:", reply_markup=reply_markup)
    #finaliza
    elif query.data.startswith('notificar_'):
        bairro = query.data.split('_')[1]
        user_id = query.from_user.id
        if bairro in ["Condá", "Belo Horizonte", "Itaipu", "São Cristóvão"]:
            cron = "30 7 * * 1,3,5"
        elif bairro in ["Frimesa", "Jardim Irene", "Paraíso", "Ipê", "Nazaré", "Panorâmico", "Santos Dumont"]:
            cron = "30 7 * * 2,4,6"
        elif bairro in ["Centro", "Cidade alta"]:
            cron = "30 7 * * 0-6"
        elif bairro in ["Independência"]:
            cron = "30 7 * * 2,3,4,6"
        await agendar_notificacao(user_id, bairro, cron)
        await query.message.reply_text(f"Notificações agendadas para o bairro {bairro}.")
        await show_main_menu(update, context)


async def agendar_notificacao(user_id: int, bairro: str, cron: str):
    #script
    script_content = f"""
import requests
TOKEN = "7026701800:AAEnoLmLtLFzPGfEg0bIAoB6_voHB-yxG-U"
chat_id = {user_id}
bairro = '{bairro}'
BAIRROS = {BAIRROS}
coletas = BAIRROS[bairro]
mensagem = f"Ei, tem coleta no seu bairro Hoje!!:\\nAs coletas no bairro {{bairro}} ocorrem:\\n\\nLixo orgânico: {{coletas['orgânico']}}\\nLixo reciclável: {{coletas['reciclável']}}"
url = f"https://api.telegram.org/bot{{TOKEN}}/sendMessage?chat_id={{chat_id}}&text={{mensagem}}"
print(requests.get(url).json())  
    """

    script_filename = f"/home/notificacao_{user_id}_.py"
    with open(script_filename, 'w') as f_open:
        f_open.write(script_content)
    
    #remove cadastro ja criado
    os.system(f"(crontab -l | grep -v {script_filename}) | crontab -")

    # Adiciona o script ao crontab
    cron_job = f"{cron} /usr/bin/python3 {script_filename}\n"
    os.system(f"(crontab -l ; echo \"{cron_job}\") | crontab -")


#funcao main integra bot
def main() -> None:
    application = Application.builder().token("X").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_opt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_itrv))
    application.add_handler(CommandHandler("sair", show_main_menu))
    #inicia bot
    application.run_polling()

if __name__ == '__main__':
    main()

