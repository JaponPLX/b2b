/**
 * Asistente Consultor de Arquitectura RAG
 * Manejo de recomendaciones, diagramas Mermaid, guía de conexión y exportación.
 */

let currentRecommendation = null;

const PROMPT_EXAMPLES = {
  1: "Estoy construyendo un e-commerce B2B de logística con tracking de flotas en tiempo real, autenticación multi-tenant y pagos recurrentes por volumen.",
  2: "SaaS de telemedicina para clínicas privadas con videollamadas, historias clínicas encriptadas, agenda médica y firma digital de consentimientos informados.",
  3: "Plataforma corporativa de IA para análisis de contratos con modelos LLM ejecutados de forma privada local (sin enviar datos a OpenAI) y búsqueda vectorial.",
  4: "Sistema de analítica en tiempo real para dispositivos IoT industriales con ingestión de millones de eventos por segundo, alertas y dashboards operacionales."
};

function setExamplePrompt(id) {
  const text = PROMPT_EXAMPLES[id];
  if (text) {
    document.getElementById("rag-input").value = text;
  }
}

async function generateArchitecturePlan() {
  const input = document.getElementById("rag-input");
  const prompt = input.value.trim();
  if (!prompt) {
    showToast("Por favor ingresa una descripción del proyecto.");
    input.focus();
    return;
  }

  const btn = document.getElementById("btn-generate-architecture");
  const loading = document.getElementById("rag-loading");
  const results = document.getElementById("rag-results");

  btn.disabled = true;
  btn.classList.add("opacity-50", "cursor-not-allowed");
  loading.classList.remove("hidden");
  results.classList.add("hidden");

  try {
    const data = await API.recommendArchitecture(prompt);
    if (data.error) {
      showToast(data.error);
      return;
    }

    currentRecommendation = data;
    renderRecommendation(data);
    results.classList.remove("hidden");
    results.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    console.error("Error al generar arquitectura:", err);
    showToast("Error al conectar con el motor RAG");
  } finally {
    btn.disabled = false;
    btn.classList.remove("opacity-50", "cursor-not-allowed");
    loading.classList.add("hidden");
  }
}

function renderRecommendation(data) {
  document.getElementById("rag-industry-badge").textContent = data.industry || "Arquitectura Recomendada";
  document.getElementById("rag-summary-text").textContent = data.executive_summary;
  document.getElementById("rag-monthly-savings").textContent = `$${data.total_monthly_savings_usd.toLocaleString()}`;
  document.getElementById("rag-annual-savings").textContent = `$${data.total_annual_savings_usd.toLocaleString()}`;

  const mermaidContainer = document.getElementById("mermaid-container");
  mermaidContainer.innerHTML = `<pre class="mermaid">${data.mermaid_diagram}</pre>`;
  try {
    mermaid.run({ nodes: mermaidContainer.querySelectorAll(".mermaid") });
  } catch (e) {
    console.warn("Mermaid error:", e);
  }

  const stackGrid = document.getElementById("rag-stack-grid");
  stackGrid.innerHTML = data.stack.map(comp => `
    <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between hover:border-slate-700 transition">
      <div>
        <div class="flex items-center justify-between text-xs mb-2">
          <span class="text-indigo-400 font-semibold uppercase tracking-wider text-[11px]">${comp.role}</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            ★ ${comp.health_score}%
          </span>
        </div>
        <h4 class="text-base font-bold text-white">${comp.name}</h4>
        <p class="text-xs text-slate-400 mt-1 line-clamp-2">${comp.description}</p>
      </div>

      <div class="mt-4 pt-3 border-t border-slate-900 flex items-center justify-between text-xs font-mono">
        <span class="text-slate-500 text-[11px]">vs ${comp.saas_alternative}</span>
        <span class="text-emerald-400 font-semibold">+$${comp.estimated_monthly_saas_cost}/mo</span>
      </div>
    </div>
  `).join("");

  const stepsContainer = document.getElementById("rag-steps-container");
  if (data.integration_guide && data.integration_guide.length > 0) {
    stepsContainer.innerHTML = data.integration_guide.map(step => `
      <div class="border border-slate-800/80 rounded-xl bg-slate-950/60 p-4 space-y-2">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-full bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 text-xs font-bold font-mono flex items-center justify-center">
            ${step.step}
          </span>
          <h4 class="text-sm font-semibold text-white">${step.title}</h4>
        </div>
        <p class="text-xs text-slate-400 pl-8">${step.description}</p>
        <div class="pl-8 pt-1">
          <pre class="p-3 bg-slate-950 text-slate-200 text-xs font-mono rounded-lg border border-slate-800 overflow-x-auto leading-relaxed">${escapeHtml(step.code)}</pre>
        </div>
      </div>
    `).join("");
  } else {
    stepsContainer.innerHTML = `<p class="text-xs text-slate-500">No hay pasos de integración adicionales requeridos.</p>`;
  }
}

function exportBlueprintMarkdown() {
  if (!currentRecommendation) return;

  const data = currentRecommendation;
  let md = `# Blueprint de Arquitectura Open Source - ${data.industry}\n\n`;
  md += `**Generado por**: NoCountry Integrations Accelerator\n`;
  md += `**Consulta**: "${data.query}"\n\n`;
  md += `## Resumen Ejecutivo\n${data.executive_summary}\n\n`;
  md += `### Impacto Financiero\n`;
  md += `- **Ahorro Mensual Estimado**: $${data.total_monthly_savings_usd.toLocaleString()} USD / mes\n`;
  md += `- **Ahorro Anual Proyectado**: $${data.total_annual_savings_usd.toLocaleString()} USD / año\n\n`;
  
  md += `## Stack Tecnológico Recomendado\n\n`;
  data.stack.forEach(c => {
    md += `### ${c.role}: ${c.name}\n`;
    md += `- **Descripción**: ${c.description}\n`;
    md += `- **Health Score**: ${c.health_score}%\n`;
    md += `- **Licencia**: ${c.license}\n`;
    md += `- **Reemplaza a**: ${c.saas_alternative} (Ahorro est.: $${c.estimated_monthly_saas_cost}/mes)\n`;
    md += `- **GitHub**: ${c.github_url}\n\n`;
  });

  md += `## Diagrama de Arquitectura (Mermaid)\n\n\`\`\`mermaid\n${data.mermaid_diagram}\n\`\`\`\n\n`;

  md += `## Guía de Integración Paso a Paso\n\n`;
  data.integration_guide.forEach(s => {
    md += `### Paso ${s.step}: ${s.title}\n`;
    md += `${s.description}\n\n`;
    md += `\`\`\`\n${s.code}\n\`\`\`\n\n`;
  });

  const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `blueprint-arquitectura-${data.industry.toLowerCase().replace(/[^a-z0-9]/g, "-")}.md`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Blueprint exportado con éxito en formato Markdown");
}

function escapeHtml(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
