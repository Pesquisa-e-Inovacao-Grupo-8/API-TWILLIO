from flask import Flask, jsonify , request
from twilio.rest import Client
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Credenciais
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# ============================================
# ENVIAR MENSAGEM
# ============================================
def enviar_mensagem(numero, mensagem):

    numero = ''.join(caractere for caractere in numero if caractere.isdigit())

    sms = client.messages.create(
        body=mensagem,
        from_="whatsapp:+14155238886",  # sandbox Twilio
        to=f"whatsapp:{"+55"+numero}"
    )
    
    return sms


# ============================================
# ENDPOINT - AGENDAMENTO
# ============================================
@app.route("/notify/agendamento", methods=["POST"])
def notify_agendamento():

    print("REQUISIÇÃO RECEBIDA", flush=True)
    corpo_bruto = request.get_data(as_text=True)
    dataBruta = request.get_json(silent=True)

    print("+=+=+= PAYLOAD RECEBIDO +=+=+=+=", flush=True)
    print(f"Content-Type: {request.content_type}", flush=True)
    print(f"Corpo bruto: {corpo_bruto}", flush=True)
    print(f"JSON: {dataBruta}", flush=True)
    print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=", flush=True)

    if dataBruta is None:
        return jsonify({
            "success": False,
            "error": "Payload ausente ou inválido. Envie JSON com Content-Type application/json."
        }), 400

    data = {
        "servico": dataBruta["servico"],
        "ordemPedido": dataBruta["ordemPedido"],
        "horaInicio": dataBruta["horaInicio"],
        "data": dataBruta["data"],
        "cliente": dataBruta["cliente"],
        "telefone": dataBruta["telefone"]
    }

    sms = enviar_mensagem(
        data["telefone"],
        mensagem_agendamento(data)
    )

    return jsonify({
        "success": True,
        "sid": sms.sid
    })


# ============================================
# ENDPOINT - PAGAMENTO
# ============================================
@app.route("/notify/pagamento", methods=["POST"])
def notify_pagamento():

    data = request.get_json()

    sms = enviar_mensagem(
        data["telefone"],
        mensagem_pagamento(data)
    )

    return jsonify({
        "success": True,
        "sid": sms.sid
    })


# ============================================
# ENDPOINT - LEMBRETE AGENDAMENTO
# ============================================
@app.route("/notify/lembrete-agendamento", methods=["POST"])
def notify_lembrete():

    data = request.get_json()

    sms = enviar_mensagem(
        data["telefone"],
        mensagem_lembrete_agendamento(data)
    )

    return jsonify({
        "success": True,
        "sid": sms.sid
    })


# ==============================================
# TEMPLATES - TEMPLATES - TEMPLATES - TEMPLATES 
# MENSAGENS - MENSAGENS - MENSAGENS - MENSAGENS 
# TEMPLATES - TEMPLATES - TEMPLATES - TEMPLATES 
# ==============================================

# ============================================
# TEMPLATE - AGENDAMENTO CRIADO
# ============================================
def mensagem_agendamento(data):

    return f"""
📅 Olá, {data['cliente']}!

Seu agendamento foi criado com sucesso ✅

📌 Serviço: {data['servico']}
🗓️ Data: {data['data']}
⏰ Horário: {data['horaInicio']}

🧾 Pedido: #{data['ordemPedido']}

Obrigado pela preferência ❤️
"""


# ============================================
# TEMPLATE - PAGAMENTO APROVADO
# ============================================
def mensagem_pagamento(data):

    return f"""
💳 Pagamento aprovado com sucesso ✅

📌 Serviço: {data['servico']}
💰 Valor pago: R$ {data['preco']}
🧾 Pedido: #{data['ordemPedido']}

Seu horário está confirmado 🎉
"""


# ============================================
# TEMPLATE - LEMBRETE AGENDAMENTO
# ============================================
def mensagem_lembrete_agendamento(data):

    return f"""
⏰ *Lembrete de Agendamento*

Olá, {data['cliente']} 😊

Passando para confirmar seu atendimento agendado.

📅 *Data:* {data['data']}
⏰ *Horário:* {data['horaInicio']}
🧾 *Pedido:* {data['ordemPedido']}

Nosso time está pronto para te atender com todo cuidado 💙

Qualquer dúvida, estamos à disposição!
"""

# ============================================
# TEMPLATE - LEMBRETE PACOTE
# ============================================
def mensagem_lembrete_pacote(data):

    return f"""
    ⏰ Lembrete do seu pacote!  
    """


# ============================================
# START
# ============================================
if __name__ == "__main__":
    app.run(debug=True, port=8090)

