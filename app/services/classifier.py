import os
import re
import json
from transformers import pipeline
from app.services.nlp import preprocess
from app.services.responders import rule_based_reply

# ==============================
# 1. Inicialização dos Pipelines
# ==============================
try:
    # Classificação em PT-BR (modelo treinado em português)
    _hf_classifier = pipeline(
        "text-classification",
        model="neuralmind/bert-base-portuguese-cased"
    )

    # Geração de texto em PT-BR (GPT-2 small português)
    _hf_generator = pipeline(
        "text-generation",
        model="pierreguillou/gpt2-small-portuguese"
    )
except Exception as e:
    print(f"⚠️ Erro ao carregar modelos Hugging Face: {e}")
    _hf_classifier = None
    _hf_generator = None

# ==============================
# 2. Funções auxiliares
# ==============================
def _huggingface_available():
    return _hf_classifier is not None and _hf_generator is not None

def _classify_with_huggingface(text: str):
    try:
        result = _hf_classifier(text[:512])[0]  # limita tokens
        label = result["label"]
        score = float(result["score"])

        category = "Produtivo" if "POS" in label.upper() else "Improdutivo"

        prompt = (
            f"O seguinte e-mail foi classificado como {category}.\n"
            f"Escreva uma resposta educada, clara e profissional em português.\n\n"
            f"E-mail: {text}\n\nResposta:"
        )

        generated = _hf_generator(
            prompt,
            max_length=120,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
        )

        reply = generated[0]["generated_text"].split("Resposta:")[-1].strip()

        return {
            "category": category,
            "confidence": score,
            "suggested_reply": reply,
            "meta": {"engine": "huggingface/ptbr-classifier+gpt2"}
        }
    except Exception as e:
        return {"error": str(e)}

def _classify_with_rules(text: str):
    """Fallback heurístico caso Hugging Face falhe"""
    raw = text
    t = preprocess(text)
    score_prod = sum(t.count(k) for k in ["status", "suporte", "erro", "prazo", "documento"])
    score_improd = sum(t.count(k) for k in ["obrigado", "feliz", "bom dia", "abraços"])
    category = "Produtivo" if score_prod >= score_improd else "Improdutivo"
    reply, _ = rule_based_reply(category, raw)
    return {
        "category": category,
        "confidence": 0.75,
        "suggested_reply": reply,
        "meta": {"engine": "heuristic"}
    }

# ==============================
# 3. Função principal
# ==============================
def classify_text_and_reply(text: str):
    if _huggingface_available():
        out = _classify_with_huggingface(text)
        if out and "error" not in out:
            return out
    return _classify_with_rules(text)
