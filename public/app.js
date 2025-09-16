const btn = document.getElementById('btnProcess');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');

// Atualiza o texto do nome do arquivo
fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    fileName.textContent = fileInput.files[0].name;
  } else {
    fileName.textContent = "Nenhum arquivo escolhido";
  }
});

btn.addEventListener('click', async () => {
  console.log("🚀 Botão clicado!");

  const file = fileInput.files[0];
  const text = document.getElementById('emailText').value;

  const form = new FormData();
  if (file) form.append('file', file);
  if (text) form.append('text', text);

  try {
    console.log("📤 Enviando requisição para /api/process...");
    const res = await fetch("/api/process", {
      method: "POST",
      body: form,
    });

    console.log("📥 Resposta recebida:", res.status);

    if (!res.ok) throw new Error(`Erro ao processar e-mail (status ${res.status})`);

    const data = await res.json();
    console.log("✅ Dados recebidos:", data);

    document.getElementById("result").innerHTML = `
      <div class="result-card">
        <h3>📊 Resultado</h3>
        <p><b>Categoria:</b> ${data.category}</p>
        <p><b>Confiança:</b> ${(data.confidence * 100).toFixed(1)}%</p>
        <p><b>Resposta sugerida:</b> ${data.suggested_reply}</p>
        <hr>
        <small><b>Motor:</b> ${data.meta.engine} | 
        <b>Tempo:</b> ${data.meta.elapsed_ms} ms</small>
      </div>
    `;
  } catch (err) {
    console.error("❌ Erro no fetch:", err);
    document.getElementById("result").innerHTML =
      `<p class="error">❌ Erro: ${err.message}</p>`;
  }
});
