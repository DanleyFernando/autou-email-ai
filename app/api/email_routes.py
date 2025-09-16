import time
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.pdf_utils import extract_text_from_pdf
from app.services.classifier import classify_text_and_reply
from app.schemas.email_schema import ProcessResponse

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
async def process_email(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Endpoint para processar um e-mail.
    - Recebe um arquivo .txt ou .pdf, ou então texto colado no formulário.
    - Retorna categoria, confiança, resposta sugerida e metadados.
    """
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="Envie um arquivo (.txt/.pdf) ou cole o texto do email."
        )

    t0 = time.time()
    content = ""

    # 1) Se enviaram arquivo
    if file:
        filename = (file.filename or "").lower()
        data = await file.read()

        if filename.endswith(".txt"):
            content = data.decode("utf-8", errors="ignore")
        elif filename.endswith(".pdf"):
            content = extract_text_from_pdf(data)
        else:
            raise HTTPException(
                status_code=400,
                detail="Formato não suportado. Use .txt ou .pdf"
            )
    else:
        # 2) Se colaram texto
        content = text or ""

    content = content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Conteúdo vazio.")

    # 3) Chama classificador
    try:
        result = classify_text_and_reply(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no classificador: {str(e)}"
        )

    # 4) Anexa tempo de processamento (sempre garante meta)
    if "meta" not in result:
        result["meta"] = {}
    result["meta"]["elapsed_ms"] = int((time.time() - t0) * 1000)

    return JSONResponse(result)
