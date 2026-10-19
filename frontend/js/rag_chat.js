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

let currentTeamScale = 1;

function setTeamScale(scale) {
  currentTeamScale = scale;
  document.querySelectorAll(".scale-btn").forEach(btn => {
    btn.classList.remove("bg-indigo-600", "text-white");
    btn.classList.add("bg-slate-800", "text-slate-400");
  });
  const activeBtn = document.getElementById(`scale-btn-${scale}`);
  if (activeBtn) {
    activeBtn.classList.add("bg-indigo-600", "text-white");
    activeBtn.classList.remove("bg-slate-800", "text-slate-400");
  }

  if (currentRecommendation) {
    const baseMonthly = currentRecommendation.total_monthly_savings_usd || 1420;
    const scaledMonthly = baseMonthly * scale;
    const scaledAnnual = scaledMonthly * 12;

    document.getElementById("rag-monthly-savings").textContent = `$${scaledMonthly.toLocaleString()}`;
    document.getElementById("rag-annual-savings").textContent = `$${scaledAnnual.toLocaleString()}`;
  }
}

function renderRecommendation(data) {
  document.getElementById("rag-industry-badge").textContent = data.industry || "Arquitectura Recomendada";
  document.getElementById("rag-summary-text").textContent = data.executive_summary;
  
  const baseMonthly = data.total_monthly_savings_usd || 1420;
  const scaledMonthly = baseMonthly * currentTeamScale;
  document.getElementById("rag-monthly-savings").textContent = `$${scaledMonthly.toLocaleString()}`;
  document.getElementById("rag-annual-savings").textContent = `$${(scaledMonthly * 12).toLocaleString()}`;

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
          <span class="text-indigo-400 font-semibold uppercase tracking-wider text-[11px] font-mono">${comp.role}</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Health: ${comp.health_score}%
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

  // Populate Infrastructure Sizing Metrics
  if (data.sizing_estimate) {
    const s = data.sizing_estimate;
    const ramEl = document.getElementById("sizing-ram");
    const cpuEl = document.getElementById("sizing-cpu");
    const diskEl = document.getElementById("sizing-disk");
    const vpsEl = document.getElementById("sizing-vps-cost");
    const netEl = document.getElementById("sizing-net-savings");

    if (ramEl) ramEl.textContent = `${s.ram_gb} GB`;
    if (cpuEl) cpuEl.textContent = `${s.cpu_cores} Cores`;
    if (diskEl) diskEl.textContent = `${s.storage_gb} GB`;
    if (vpsEl) vpsEl.textContent = `$${s.vps_monthly_cost_usd} USD/mes`;
    if (netEl) netEl.textContent = `+$${s.net_monthly_savings_usd.toLocaleString()}/mes`;
  }
}

let currentMermaidZoom = 1.0;

function zoomMermaid(factor) {
  currentMermaidZoom *= factor;
  if (currentMermaidZoom < 0.4) currentMermaidZoom = 0.4;
  if (currentMermaidZoom > 2.5) currentMermaidZoom = 2.5;
  const container = document.getElementById("mermaid-container");
  if (container) {
    container.style.transform = `scale(${currentMermaidZoom})`;
  }
}

function resetZoomMermaid() {
  currentMermaidZoom = 1.0;
  const container = document.getElementById("mermaid-container");
  if (container) {
    container.style.transform = `scale(1.0)`;
  }
}

function downloadMermaidSvg() {
  const container = document.getElementById("mermaid-container");
  const svg = container ? container.querySelector("svg") : null;
  if (!svg) {
    showToast("No hay diagrama generado para exportar.");
    return;
  }
  const svgData = new XMLSerializer().serializeToString(svg);
  const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `arquitectura-b2b-topology.svg`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Diagrama de arquitectura descargado en SVG");
}

function downloadDockerCompose() {
  if (!currentRecommendation || !currentRecommendation.docker_compose_yaml) {
    showToast("Genera una arquitectura para descargar el docker-compose.yml");
    return;
  }
  const blob = new Blob([currentRecommendation.docker_compose_yaml], { type: "text/yaml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "docker-compose.yml";
  a.click();
  URL.revokeObjectURL(url);
  showToast("docker-compose.yml descargado con éxito");
}

function downloadEnvExample() {
  if (!currentRecommendation || !currentRecommendation.env_example) {
    showToast("Genera una arquitectura para descargar el .env.example");
    return;
  }
  const blob = new Blob([currentRecommendation.env_example], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = ".env.example";
  a.click();
  URL.revokeObjectURL(url);
  showToast(".env.example descargado con éxito");
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

let currentClientName = "Empresa Cliente B2B";
let currentProjectTitle = "";
let currentBlueprintId = null;

function openSaveBlueprintModal() {
  if (!currentRecommendation) {
    showToast("Genera una arquitectura antes de guardar un blueprint.");
    return;
  }
  const modal = document.getElementById("modal-save-blueprint");
  if (!modal) return;
  const clientInput = document.getElementById("input-client-name");
  const titleInput = document.getElementById("input-project-title");
  if (clientInput) clientInput.value = currentClientName !== "Empresa Cliente B2B" ? currentClientName : "";
  if (titleInput) titleInput.value = currentProjectTitle || `Arquitectura ${currentRecommendation.industry || 'Cloud'}`;
  modal.classList.remove("hidden");
  modal.classList.add("flex");
  if (clientInput) clientInput.focus();
}

function closeSaveBlueprintModal() {
  const modal = document.getElementById("modal-save-blueprint");
  if (!modal) return;
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

async function confirmSaveBlueprint() {
  if (!currentRecommendation) return;
  const clientInput = document.getElementById("input-client-name");
  const titleInput = document.getElementById("input-project-title");
  const clientName = clientInput ? clientInput.value.trim() : "";
  const projectTitle = titleInput ? titleInput.value.trim() : "";

  if (!clientName) {
    showToast("Ingresa el nombre del cliente o empresa.");
    if (clientInput) clientInput.focus();
    return;
  }

  currentClientName = clientName;
  currentProjectTitle = projectTitle;

  try {
    const res = await API.saveBlueprint({
      id: currentBlueprintId,
      client_name: clientName,
      project_title: projectTitle,
      industry: currentRecommendation.industry || "Cloud",
      data: currentRecommendation
    });

    if (res.id) {
      currentBlueprintId = res.id;
      closeSaveBlueprintModal();
      showToast(`Blueprint guardado para ${clientName}`);
      updateSavedBlueprintsCount();
    } else {
      showToast(res.error || "Error al guardar el blueprint");
    }
  } catch (e) {
    console.error(e);
    showToast("Error de conexión al guardar blueprint");
  }
}

async function openSavedBlueprintsDrawer() {
  const modal = document.getElementById("modal-saved-blueprints");
  if (!modal) return;
  modal.classList.remove("hidden");
  modal.classList.add("flex");
  await refreshSavedBlueprintsList();
}

function closeSavedBlueprintsDrawer() {
  const modal = document.getElementById("modal-saved-blueprints");
  if (!modal) return;
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

async function refreshSavedBlueprintsList() {
  const listContainer = document.getElementById("saved-blueprints-list");
  if (!listContainer) return;

  listContainer.innerHTML = `<div class="py-12 text-center text-slate-500 text-sm">Cargando blueprints...</div>`;

  try {
    const res = await API.getBlueprints();
    const items = res.items || [];

    const counterBadge = document.getElementById("saved-blueprints-count");
    if (counterBadge) counterBadge.textContent = items.length;

    if (items.length === 0) {
      listContainer.innerHTML = `
        <div class="py-12 text-center text-slate-500 text-xs">
          <p class="font-medium text-slate-400">No hay blueprints guardados aún.</p>
          <p class="mt-1">Genera una arquitectura y haz clic en "Guardar Blueprint" para registrar clientes.</p>
        </div>
      `;
      return;
    }

    listContainer.innerHTML = items.map(bp => `
      <div class="p-4 bg-slate-950/80 border border-slate-800 rounded-xl hover:border-slate-700 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-bold text-white">${escapeHtml(bp.client_name)}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">${escapeHtml(bp.industry || 'Tecnología')}</span>
          </div>
          <p class="text-xs text-slate-300 font-medium">${escapeHtml(bp.project_title || 'Arquitectura')}</p>
          <div class="flex items-center space-x-3 text-[11px] font-mono text-slate-400">
            <span class="text-emerald-400 font-semibold">Ahorro: +$${(bp.total_monthly_savings || 0).toLocaleString()}/mes</span>
            <span>Fecha: ${bp.created_at ? bp.created_at.split(" ")[0] : "Reciente"}</span>
          </div>
        </div>

        <div class="flex items-center space-x-2 shrink-0">
          <button onclick="loadSavedBlueprint('${bp.id}')" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition flex items-center space-x-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            <span>Cargar</span>
          </button>
          <button onclick="deleteSavedBlueprint('${bp.id}')" class="p-1.5 bg-slate-900 hover:bg-red-950/60 text-slate-400 hover:text-red-400 border border-slate-800 rounded-lg transition" title="Eliminar blueprint">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </div>
    `).join("");
  } catch (e) {
    console.error(e);
    listContainer.innerHTML = `<div class="py-8 text-center text-red-400 text-xs">Error al cargar historial de blueprints.</div>`;
  }
}

async function loadSavedBlueprint(id) {
  try {
    const bp = await API.getBlueprintById(id);
    if (!bp || bp.error) {
      showToast("No se encontró el blueprint");
      return;
    }
    currentBlueprintId = bp.id;
    currentClientName = bp.client_name;
    currentProjectTitle = bp.project_title;
    currentRecommendation = bp.data;

    const input = document.getElementById("rag-input");
    if (input && bp.query) input.value = bp.query;

    renderRecommendation(bp.data);
    const results = document.getElementById("rag-results");
    if (results) {
      results.classList.remove("hidden");
      results.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    closeSavedBlueprintsDrawer();
    showToast(`Blueprint cargado: ${bp.client_name}`);
  } catch (e) {
    console.error(e);
    showToast("Error al cargar el blueprint");
  }
}

async function deleteSavedBlueprint(id) {
  if (!confirm("Deseas eliminar este blueprint de cliente?")) return;
  try {
    const res = await API.deleteBlueprint(id);
    if (res.message) {
      showToast("Blueprint eliminado con éxito");
      await refreshSavedBlueprintsList();
      updateSavedBlueprintsCount();
    } else {
      showToast(res.error || "No se pudo eliminar");
    }
  } catch (e) {
    console.error(e);
    showToast("Error de conexión");
  }
}

async function updateSavedBlueprintsCount() {
  try {
    const res = await API.getBlueprints();
    const count = (res.items || []).length;
    const badge = document.getElementById("saved-blueprints-count");
    if (badge) badge.textContent = count;
  } catch (e) {
    // ignore
  }
}

function printExecutiveReport() {
  if (!currentRecommendation) {
    showToast("Genera una arquitectura para exportar el dossier ejecutivo.");
    return;
  }

  const data = currentRecommendation;
  const client = currentClientName || "Cliente Confidencial";
  const project = currentProjectTitle || `Arquitectura ${data.industry || 'Cloud'}`;
  const dateStr = new Date().toLocaleDateString("es-ES", { year: "numeric", month: "long", day: "numeric" });

  const printArea = document.getElementById("print-dossier-area");
  if (!printArea) {
    window.print();
    return;
  }

  const svgElem = document.querySelector("#mermaid-container svg");
  const svgHtml = svgElem ? svgElem.outerHTML : "";

  printArea.innerHTML = `
    <div class="print-page">
      <!-- Header -->
      <div class="print-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0f172a; padding-bottom: 16px; margin-bottom: 24px;">
          <div>
            <div style="font-size: 10px; font-weight: 800; letter-spacing: 0.15em; color: #4f46e5; text-transform: uppercase;">
              NoCountry B2B Architecture Consulting Services
            </div>
            <h1 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 4px 0 0 0;">
              Dossier de Arquitectura Tecnológica & TCO
            </h1>
            <p style="font-size: 13px; color: #64748b; margin: 4px 0 0 0;">
              Auditoría Técnica, Topología Open Source & Proyección de Ahorro
            </p>
          </div>
          <div style="text-align: right; font-size: 11px; font-family: monospace; color: #475569;">
            <div><strong>DOCUMENTO:</strong> #DOC-${(currentBlueprintId || 'BP01').toUpperCase()}</div>
            <div><strong>FECHA:</strong> ${dateStr}</div>
            <div><span style="display: inline-block; padding: 2px 6px; background: #e0e7ff; color: #3730a3; font-weight: bold; border-radius: 4px;">CONFIDENCIAL</span></div>
          </div>
        </div>

        <!-- Metadata Box -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; margin-bottom: 24px;">
          <div>
            <span style="font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: bold;">Cliente / Organización</span>
            <div style="font-size: 15px; font-weight: 700; color: #0f172a;">${escapeHtml(client)}</div>
          </div>
          <div>
            <span style="font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: bold;">Iniciativa / Proyecto</span>
            <div style="font-size: 15px; font-weight: 700; color: #0f172a;">${escapeHtml(project)}</div>
          </div>
        </div>
      </div>

      <!-- Resumen Ejecutivo -->
      <div style="margin-bottom: 24px;">
        <h2 style="font-size: 14px; text-transform: uppercase; font-weight: 800; color: #1e293b; border-left: 4px solid #4f46e5; padding-left: 8px; margin-bottom: 8px;">
          1. Resumen Ejecutivo & Diagnóstico
        </h2>
        <p style="font-size: 12px; line-height: 1.6; color: #334155;">
          ${escapeHtml(data.executive_summary)}
        </p>
      </div>

      <!-- Impacto Financiero & TCO -->
      <div style="margin-bottom: 24px;">
        <h2 style="font-size: 14px; text-transform: uppercase; font-weight: 800; color: #1e293b; border-left: 4px solid #059669; padding-left: 8px; margin-bottom: 12px;">
          2. Modelo Financiero & Ahorro Estimado (TCO)
        </h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 16px;">
          <div style="border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; text-align: center; background: #f0fdf4;">
            <span style="font-size: 10px; color: #166534; font-weight: 700; text-transform: uppercase;">Ahorro Mensual Estimado</span>
            <div style="font-size: 20px; font-weight: 800; color: #15803d; margin-top: 4px;">+$${(data.total_monthly_savings_usd || 1420).toLocaleString()} USD</div>
          </div>
          <div style="border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; text-align: center; background: #f0fdf4;">
            <span style="font-size: 10px; color: #166534; font-weight: 700; text-transform: uppercase;">Ahorro Anual Proyectado</span>
            <div style="font-size: 20px; font-weight: 800; color: #15803d; margin-top: 4px;">+$${(data.total_annual_savings_usd || 17040).toLocaleString()} USD</div>
          </div>
          <div style="border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; text-align: center; background: #eff6ff;">
            <span style="font-size: 10px; color: #1e40af; font-weight: 700; text-transform: uppercase;">Margen Neto tras VPS</span>
            <div style="font-size: 20px; font-weight: 800; color: #1d4ed8; margin-top: 4px;">+$${(data.sizing_estimate ? data.sizing_estimate.net_monthly_savings_usd : 1396).toLocaleString()} USD/m</div>
          </div>
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
          <thead>
            <tr style="background: #0f172a; color: white;">
              <th style="padding: 8px; text-align: left;">Componente Open Source</th>
              <th style="padding: 8px; text-align: left;">Rol Funcional</th>
              <th style="padding: 8px; text-align: left;">SaaS Reemplazado</th>
              <th style="padding: 8px; text-align: right;">Ahorro Mensual</th>
              <th style="padding: 8px; text-align: center;">Health Score</th>
            </tr>
          </thead>
          <tbody>
            ${data.stack.map((c, i) => `
              <tr style="border-bottom: 1px solid #e2e8f0; background: ${i % 2 === 0 ? '#ffffff' : '#f8fafc'};">
                <td style="padding: 8px; font-weight: bold; color: #0f172a;">${escapeHtml(c.name)}</td>
                <td style="padding: 8px; color: #475569;">${escapeHtml(c.role)}</td>
                <td style="padding: 8px; color: #dc2626;">${escapeHtml(c.saas_alternative)}</td>
                <td style="padding: 8px; text-align: right; font-weight: bold; color: #15803d;">+$${c.estimated_monthly_saas_cost}/mes</td>
                <td style="padding: 8px; text-align: center; font-weight: bold; color: #0284c7;">${c.health_score}%</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>

      <!-- Sizing & Compliance -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; page-break-inside: avoid;">
        <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; background: #fafafa;">
          <h3 style="font-size: 12px; font-weight: 800; text-transform: uppercase; margin-top: 0; color: #0f172a;">
            Dimensionamiento Cloud Requerido
          </h3>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; text-align: center; margin-top: 8px;">
            <div style="padding: 6px; background: white; border: 1px solid #e2e8f0; border-radius: 4px;">
              <span style="font-size: 9px; color: #64748b; display: block;">RAM MÍNIMA</span>
              <strong style="font-size: 13px; color: #0f172a;">${data.sizing_estimate ? data.sizing_estimate.ram_gb : 8} GB</strong>
            </div>
            <div style="padding: 6px; background: white; border: 1px solid #e2e8f0; border-radius: 4px;">
              <span style="font-size: 9px; color: #64748b; display: block;">vCPUS</span>
              <strong style="font-size: 13px; color: #0f172a;">${data.sizing_estimate ? data.sizing_estimate.cpu_cores : 4} Cores</strong>
            </div>
            <div style="padding: 6px; background: white; border: 1px solid #e2e8f0; border-radius: 4px;">
              <span style="font-size: 9px; color: #64748b; display: block;">STORAGE</span>
              <strong style="font-size: 13px; color: #0f172a;">${data.sizing_estimate ? data.sizing_estimate.storage_gb : 60} GB</strong>
            </div>
          </div>
          <p style="font-size: 10px; color: #64748b; margin-top: 8px; margin-bottom: 0;">
            Costo infra estimado: <strong>$${data.sizing_estimate ? data.sizing_estimate.vps_monthly_cost_usd : 24} USD/mes</strong> en VPS Hetzner / AWS Lightsail.
          </p>
        </div>

        <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; background: #fafafa;">
          <h3 style="font-size: 12px; font-weight: 800; text-transform: uppercase; margin-top: 0; color: #0f172a;">
            Garantías de Cumplimiento & Zero-Trust
          </h3>
          <ul style="font-size: 10px; color: #334155; margin: 8px 0 0 0; padding-left: 16px; line-height: 1.6;">
            <li><strong>GDPR / Soberanía Total:</strong> Datos bajo control estricto sin filtraciones a terceros.</li>
            <li><strong>Air-Gapped Ready:</strong> Ejecución autónoma sin dependencias externas obligatorias.</li>
            <li><strong>Cifrado Estricto:</strong> Cifrado en reposo AES-256 y tránsito con TLS 1.3.</li>
            <li><strong>Trazabilidad SOC 2:</strong> Logs estructurados y auditoría centralizada.</li>
          </ul>
        </div>
      </div>

      <!-- Diagrama de Arquitectura -->
      <div style="margin-bottom: 24px; page-break-inside: avoid;">
        <h2 style="font-size: 14px; text-transform: uppercase; font-weight: 800; color: #1e293b; border-left: 4px solid #0284c7; padding-left: 8px; margin-bottom: 12px;">
          3. Topología de Integración del Sistema
        </h2>
        <div style="border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; background: #ffffff; text-align: center;">
          ${svgHtml ? svgHtml : `<pre style="font-size: 10px; text-align: left;">${escapeHtml(data.mermaid_diagram)}</pre>`}
        </div>
      </div>

      <!-- Signoff Footer -->
      <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #cbd5e1; page-break-inside: avoid;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
          <div>
            <div style="font-size: 11px; font-weight: bold; color: #64748b; margin-bottom: 40px;">ENTREGADO POR (CONSULTORÍA):</div>
            <div style="border-top: 1px solid #0f172a; padding-top: 4px; font-size: 12px; font-weight: bold; color: #0f172a;">NoCountry Architecture Team</div>
            <div style="font-size: 10px; color: #64748b;">Acelerador de Integraciones B2B</div>
          </div>
          <div>
            <div style="font-size: 11px; font-weight: bold; color: #64748b; margin-bottom: 40px;">RECIBIDO Y CONFORME (CLIENTE):</div>
            <div style="border-top: 1px solid #0f172a; padding-top: 4px; font-size: 12px; font-weight: bold; color: #0f172a;">${escapeHtml(client)}</div>
            <div style="font-size: 10px; color: #64748b;">Dirección de Tecnología / Arquitectura</div>
          </div>
        </div>
      </div>
    </div>
  `;

  setTimeout(() => {
    window.print();
  }, 100);
}

// Initialize blueprints count on load
document.addEventListener("DOMContentLoaded", () => {
  updateSavedBlueprintsCount();
});

