def rule_based_reply(category: str, text: str):
    if category.lower() == 'produtivo':
        return (
            'Olá! Recebemos sua solicitação e vamos dar andamento. Em breve retornaremos com a atualização.',
            0.75
        )
    return (
        'Olá! Muito obrigado pela mensagem. Se precisar de algo específico, é só responder este e-mail.',
        0.65
    )
