"""
Nomes de exibição e respostas simuladas por domínio.

O assistente NÃO executa nada de verdade nem gera texto: cada domínio tem uma
resposta fixa, só para demonstrar o que um assistente faria depois de
entender a intenção (NLU).
A coluna 'dominio' do CSV usa o código ASCII (ex.: 'alarm'); os nomes
bonitos ficam aqui.
"""

# Nome de exibição de cada domínio (tabela 4.3 do plano)
NOMES = {
    "alarm": "Alarmes",
    "weather": "Clima",
    "play": "Reprodução de música e mídia",
    "iot": "Casa inteligente",
    "calendar": "Calendário",
    "lists": "Listas",
    "datetime": "Data e hora",
    "news": "Notícias",
    "email": "E-mail e contatos",
}

# Resposta simulada de cada domínio
RESPOSTAS = {
    "alarm": "⏰ Pronto! Vou configurar o alarme para você. (resposta simulada)",
    "weather": "🌦️ Vou consultar a previsão do tempo para você. (resposta simulada)",
    "play": "🎵 Certo, vou colocar o que você pediu para tocar. (resposta simulada)",
    "iot": "💡 Feito! Estou ajustando os dispositivos da casa. (resposta simulada)",
    "calendar": "📅 Vou verificar ou atualizar a sua agenda. (resposta simulada)",
    "lists": "📝 Anotado! Vou atualizar a sua lista. (resposta simulada)",
    "datetime": "🕒 Vou consultar a data e a hora para você. (resposta simulada)",
    "news": "📰 Vou buscar as principais notícias para você. (resposta simulada)",
    "email": "✉️ Vou abrir a sua caixa de e-mail e os seus contatos. (resposta simulada)",
}

# Mensagem usada quando a confiança fica abaixo do limiar.
# Não lista os domínios de propósito: assim não precisa mudar se o e-mail sair.
MSG_NAO_ENTENDI = ("Desculpe, não entendi o que você quis dizer. "
                   "Tente reformular, por exemplo: 'acorde-me às sete da manhã' "
                   "ou 'vai chover amanhã?'.")


def nome_exibicao(dominio):
    """Devolve o nome de exibição; se o código não existir, devolve o próprio código."""
    return NOMES.get(dominio, dominio)


def responder(resultado):
    """Recebe o dicionário devolvido por model.prever() e devolve o texto da resposta.
    Se o modelo não entendeu (confiança < limiar), devolve o 'não entendi'."""
    if not resultado["entendeu"]:
        return MSG_NAO_ENTENDI
    return RESPOSTAS[resultado["dominio"]]