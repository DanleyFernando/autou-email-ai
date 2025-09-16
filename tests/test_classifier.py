from app.services.classifier import classify_text_and_reply

def test_produtivo():
    text = 'Preciso de atualização sobre o status do chamado.'
    result = classify_text_and_reply(text)
    assert result['category'] == 'Produtivo'

def test_improdutivo():
    text = 'Feliz Natal e boas festas!'
    result = classify_text_and_reply(text)
    assert result['category'] == 'Improdutivo'
