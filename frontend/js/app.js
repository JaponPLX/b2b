/**
 * Aplicación principal del catálogo B2B
 * Filtros en tiempo real, renderizado de tarjetas, modal de ficha técnica y pipeline
 */

let state = {
  currentTab: "catalog",
  category: "all",
  searchQuery: "",
  language: "all",
  license: "all",
  maintenance: "all",
  minStars: 0,
  sortBy: "stars_desc",
  repos: [],
  categories: [],
  totalRepos: 0,
  selectedForCompare: []
};

let currentModalSnippet = "";

document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  await Promise.all([
    loadStats(),
    loadCategories(),
    loadFilters(),
    fetchAndRenderRepos()
  ]);
});

function setupEventListeners() {
  const searchInput = document.getElementById("search-input");
  let debounceTimeout = null;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      state.searchQuery = e.target.value;
      fetchAndRenderRepos();
    }, 250);
  });

  document.getElementById("filter-language").addEventListener("change", (e) => {
    state.language = e.target.value;
    fetchAndRenderRepos();
  });

  document.getElementById("filter-license").addEventListener("change", (e) => {
    state.license = e.target.value;
    fetchAndRenderRepos();
  });

  document.getElementById("filter-maintenance").addEventListener("change", (e) => {
    state.maintenance = e.target.value;
    fetchAndRenderRepos();
  });
}

function switchTab(tabId) {
  state.currentTab = tabId;
  ["catalog", "rag", "pipeline"].forEach(tab => {
    const sec = document.getElementById(`tab-${tab}`);
    const btn = document.getElementById(`nav-${tab}`);
    if (tab === tabId) {
      sec.classList.remove("hidden");
      btn.classList.add("text-white", "bg-slate-800/80", "border", "border-slate-700");
      btn.classList.remove("text-slate-400");
    } else {
      sec.classList.add("hidden");
      btn.classList.remove("text-white", "bg-slate-800/80", "border", "border-slate-700");
      btn.classList.add("text-slate-400");
    }
  });

  if (tabId === "pipeline") {
    loadSyncLogs();
  }
}

async function loadStats() {
  try {
    const stats = await API.getStats();
    if (stats.total_repos) {
      document.getElementById("stat-total-repos").textContent = stats.total_repos;
      document.getElementById("stat-avg-health").textContent = `${Math.round(stats.avg_health || 95)}%`;
      document.getElementById("stat-saas-savings").textContent = `$${Math.round((stats.total_saas_savings || 32000) / 1000)}k+`;
    }
  } catch (e) {
    console.warn("Error cargando stats:", e);
  }
}

async function loadCategories() {
  try {
    const categories = await API.getCategories();
    state.categories = categories;

    const pillsContainer = document.getElementById("category-pills");
    let html = `
      <button onclick="selectCategory('all')" class="cat-pill active px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap bg-indigo-600 text-white transition">
        Todas (${categories.reduce((a, b) => a + b.count, 0)})
      </button>
    `;

    categories.forEach(cat => {
      html += `
        <button onclick="selectCategory('${cat.category}')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition">
          ${cat.category} <span class="text-slate-500 font-mono text-[11px]">(${cat.count})</span>
        </button>
      `;
    });

    pillsContainer.innerHTML = html;
  } catch (e) {
    console.warn("Error cargando categorías:", e);
  }
}

async function loadFilters() {
  try {
    const filters = await API.getFilters();
    
    const langSelect = document.getElementById("filter-language");
    filters.languages.forEach(l => {
      const opt = document.createElement("option");
      opt.value = l;
      opt.textContent = `Lenguaje: ${l}`;
      langSelect.appendChild(opt);
    });

    const licSelect = document.getElementById("filter-license");
    filters.licenses.forEach(l => {
      const opt = document.createElement("option");
      opt.value = l;
      opt.textContent = `Licencia: ${l}`;
      licSelect.appendChild(opt);
    });
  } catch (e) {
    console.warn("Error cargando filtros:", e);
  }
}

function selectCategory(category) {
  state.category = category;
  document.getElementById("active-category-label").textContent = category === "all" ? "Todas" : category;

  document.querySelectorAll(".cat-pill").forEach(pill => {
    if ((category === "all" && pill.textContent.includes("Todas")) || pill.textContent.includes(category)) {
      pill.classList.add("bg-indigo-600", "text-white", "font-semibold");
      pill.classList.remove("bg-slate-900", "text-slate-300");
    } else {
      pill.classList.remove("bg-indigo-600", "text-white", "font-semibold");
      pill.classList.add("bg-slate-900", "text-slate-300");
    }
  });

  fetchAndRenderRepos();
}

function setMinStars(stars) {
  state.minStars = stars;
  document.querySelectorAll(".star-btn").forEach(btn => {
    btn.classList.remove("active", "bg-indigo-600", "text-white", "font-medium");
    btn.classList.add("bg-slate-800", "text-slate-300");
  });
  event.target.classList.add("active", "bg-indigo-600", "text-white", "font-medium");
  event.target.classList.remove("bg-slate-800", "text-slate-300");

  fetchAndRenderRepos();
}

function applyFilters() {
  state.sortBy = document.getElementById("sort-select").value;
  fetchAndRenderRepos();
}

function resetFilters() {
  state.category = "all";
  state.searchQuery = "";
  state.language = "all";
  state.license = "all";
  state.maintenance = "all";
  state.minStars = 0;
  state.sortBy = "stars_desc";

  document.getElementById("search-input").value = "";
  document.getElementById("filter-language").value = "all";
  document.getElementById("filter-license").value = "all";
  document.getElementById("filter-maintenance").value = "all";
  document.getElementById("sort-select").value = "stars_desc";

  selectCategory("all");
  setMinStars(0);
}

async function fetchAndRenderRepos() {
  try {
    const data = await API.getRepos({
      q: state.searchQuery,
      category: state.category,
      language: state.language,
      license: state.license,
      maintenance: state.maintenance,
      min_stars: state.minStars,
      sort_by: state.sortBy,
      limit: 100
    });

    state.repos = data.items;
    state.totalRepos = data.total;

    document.getElementById("results-count").textContent = data.total;

    const grid = document.getElementById("repos-grid");
    const empty = document.getElementById("empty-state");

    if (data.items.length === 0) {
      grid.innerHTML = "";
      empty.classList.remove("hidden");
      return;
    }

    empty.classList.add("hidden");
    grid.innerHTML = data.items.map(r => renderRepoCard(r)).join("");
  } catch (e) {
    console.error("Error al obtener repositorios:", e);
  }
}

function renderRepoCard(repo) {
  const isSelected = state.selectedForCompare.includes(repo.id);
  const healthBadgeClass = repo.health_score >= 90
    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
    : "bg-blue-500/10 text-blue-400 border-blue-500/20";

  const tagsHtml = (repo.tags || []).slice(0, 3).map(t => `
    <span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 font-mono">#${t}</span>
  `).join("");

  return `
    <div onclick="openModal('${repo.id}')" class="repo-card cursor-pointer bg-slate-900/90 border ${isSelected ? 'border-indigo-500 shadow-lg shadow-indigo-500/10 ring-1 ring-indigo-500' : 'border-slate-800/80'} rounded-2xl p-5 flex flex-col justify-between transition-all">
      <div>
        <div class="flex items-start justify-between gap-2">
          <div>
            <div class="flex items-center space-x-2">
              <h3 class="font-bold text-base text-white group-hover:text-indigo-400 transition">${repo.name}</h3>
              <span class="text-xs font-mono text-amber-400 font-semibold">★ ${formatStars(repo.stars)}</span>
            </div>
            <span class="text-[11px] text-indigo-400 font-medium">${repo.category}</span>
          </div>

          <div class="flex flex-col items-end">
            <span class="px-2 py-0.5 rounded-full text-xs font-mono font-bold border ${healthBadgeClass}">
              ${repo.health_score}%
            </span>
            <span class="text-[9px] text-slate-500 mt-0.5">${repo.maintenance_level}</span>
          </div>
        </div>

        <p class="text-xs text-slate-300 mt-2.5 line-clamp-2 leading-relaxed">
          ${repo.description}
        </p>

        <div class="mt-3 flex flex-wrap gap-1">
          ${tagsHtml}
        </div>
      </div>

      <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
        <div class="flex items-center space-x-2 text-slate-400 font-mono text-[11px]">
          <span>${repo.language}</span>
          <span>•</span>
          <span>${repo.license}</span>
        </div>

        <div class="flex items-center space-x-2">
          ${repo.saas_alternative ? `
            <span class="text-[11px] font-mono text-emerald-400 font-medium" title="Reemplaza a ${repo.saas_alternative}">
              +$${repo.estimated_monthly_saas_cost}/mo
            </span>
          ` : ""}
          <button 
            type="button"
            onclick="toggleCompare('${repo.id}', event)" 
            title="Comparar herramienta" 
            class="px-2 py-0.5 rounded text-[11px] font-medium transition ${isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-800 hover:bg-slate-700 text-slate-300'}"
          >
            ${isSelected ? '✓ Comparando' : '+ Comparar'}
          </button>
        </div>
      </div>
    </div>
  `;
}

function formatStars(count) {
  if (count >= 1000) {
    return (count / 1000).toFixed(1) + "k";
  }
  return count;
}

async function openModal(repoId) {
  try {
    const repo = await API.getRepoById(repoId);
    if (!repo) return;

    document.getElementById("modal-title").textContent = repo.name;
    document.getElementById("modal-fullname").textContent = repo.full_name;
    document.getElementById("modal-category").textContent = repo.category;
    document.getElementById("modal-description").textContent = repo.description;

    document.getElementById("modal-stars").textContent = `★ ${repo.stars.toLocaleString()}`;
    document.getElementById("modal-forks").textContent = repo.forks.toLocaleString();
    document.getElementById("modal-issues").textContent = repo.open_issues.toLocaleString();
    document.getElementById("modal-license").textContent = repo.license;

    document.getElementById("modal-health-badge").textContent = `Health: ${repo.health_score}%`;
    document.getElementById("modal-saas").textContent = repo.saas_alternative || "Alternativa SaaS";
    document.getElementById("modal-cost-savings").textContent = `$${repo.estimated_monthly_saas_cost || 100} USD / mes`;

    document.getElementById("modal-github-link").href = repo.github_url;
    document.getElementById("modal-docs-link").href = repo.docs_url || repo.github_url;

    const integ = (repo.integrations && repo.integrations[0]) || {};
    document.getElementById("modal-integ-type").textContent = integ.integration_type || "SDK";
    document.getElementById("modal-difficulty").textContent = integ.difficulty || "Fácil";
    document.getElementById("modal-integ-explanation").textContent = integ.explanation || "Patrón de integración para desacoplar servicios.";

    const stackContainer = document.getElementById("modal-stack-tags");
    const stackList = integ.stack_compatibility || ["Node.js", "Docker"];
    stackContainer.innerHTML = stackList.map(s => `
      <span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-mono font-medium">${s}</span>
    `).join("");

    currentModalSnippet = integ.code_snippet || "# Snippet no disponible";
    document.getElementById("modal-code-snippet").textContent = currentModalSnippet;

    document.getElementById("repo-modal").classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
  } catch (e) {
    console.error("Error abriendo modal:", e);
  }
}

function closeModal() {
  document.getElementById("repo-modal").classList.add("hidden");
  document.body.classList.remove("overflow-hidden");
}

function copySnippet() {
  if (!currentModalSnippet) return;
  navigator.clipboard.writeText(currentModalSnippet).then(() => {
    const btn = document.getElementById("btn-copy-snippet");
    btn.innerHTML = `
      <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      <span class="text-emerald-400">¡Copiado!</span>
    `;
    setTimeout(() => {
      btn.innerHTML = `
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        <span>Copiar</span>
      `;
    }, 2000);
    showToast("Snippet copiado al portapapeles");
  });
}

async function triggerManualSync() {
  const btn = document.getElementById("btn-sync-now");
  btn.disabled = true;
  btn.classList.add("opacity-50", "cursor-not-allowed");

  try {
    showToast("Ejecutando ingesta en lote con GitHub API...");
    const res = await API.triggerSync(10);
    showToast(res.message);
    document.getElementById("pipeline-rate-limit").textContent = res.rate_limit_remaining;
    await Promise.all([
      loadSyncLogs(),
      loadStats(),
      fetchAndRenderRepos()
    ]);
  } catch (e) {
    showToast("Error en sincronización con GitHub");
  } finally {
    btn.disabled = false;
    btn.classList.remove("opacity-50", "cursor-not-allowed");
  }
}

async function loadSyncLogs() {
  try {
    const logs = await API.getSyncLogs();
    const tbody = document.getElementById("sync-logs-tbody");
    if (!logs || logs.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-slate-500">No hay registros de sincronización aún.</td></tr>`;
      return;
    }

    tbody.innerHTML = logs.map(l => `
      <tr class="hover:bg-slate-900/60">
        <td class="py-2.5 px-3 text-slate-400">${l.timestamp}</td>
        <td class="py-2.5 px-3 text-slate-200">${l.repos_checked}</td>
        <td class="py-2.5 px-3 text-emerald-400 font-semibold">${l.repos_updated}</td>
        <td class="py-2.5 px-3 text-indigo-400">${l.rate_limit_remaining}</td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-[10px] ${l.status === 'OK' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}">
            ${l.status}
          </span>
        </td>
        <td class="py-2.5 px-3 text-slate-400 truncate max-w-xs" title="${l.details}">${l.details}</td>
      </tr>
    `).join("");
  } catch (e) {
    console.warn("Error cargando logs:", e);
  }
}

function showToast(message) {
  const toast = document.getElementById("toast");
  document.getElementById("toast-message").textContent = message;
  toast.classList.remove("hidden");
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3500);
}

// ==================== COMPARACIÓN DE REPOSITORIOS ====================

function toggleCompare(repoId, event) {
  if (event) event.stopPropagation();

  const idx = state.selectedForCompare.indexOf(repoId);
  if (idx !== -1) {
    state.selectedForCompare.splice(idx, 1);
  } else {
    if (state.selectedForCompare.length >= 4) {
      showToast("Puedes comparar hasta 4 herramientas a la vez.");
      return;
    }
    state.selectedForCompare.push(repoId);
  }

  updateCompareDock();
  
  // Re-renderizar tarjetas para reflejar estado seleccionado
  const grid = document.getElementById("repos-grid");
  if (state.repos && state.repos.length > 0) {
    grid.innerHTML = state.repos.map(r => renderRepoCard(r)).join("");
  }
}

function updateCompareDock() {
  const dock = document.getElementById("compare-dock");
  const countSpan = document.getElementById("compare-count");
  const previewDiv = document.getElementById("compare-pills-preview");

  if (state.selectedForCompare.length === 0) {
    dock.classList.add("hidden");
    return;
  }

  countSpan.textContent = state.selectedForCompare.length;
  previewDiv.innerHTML = state.selectedForCompare.map(id => {
    const r = state.repos.find(x => x.id === id);
    const name = r ? r.name : id;
    return `<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">${name}</span>`;
  }).join("");

  dock.classList.remove("hidden");
}

function clearComparison() {
  state.selectedForCompare = [];
  updateCompareDock();
  const grid = document.getElementById("repos-grid");
  if (state.repos && state.repos.length > 0) {
    grid.innerHTML = state.repos.map(r => renderRepoCard(r)).join("");
  }
}

async function openCompareModal() {
  if (state.selectedForCompare.length < 2) {
    showToast("Selecciona al menos 2 herramientas para contrastar.");
    return;
  }

  const container = document.getElementById("compare-modal-content");
  container.innerHTML = `
    <div class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-xs text-slate-400 mt-2">Cargando métricas de comparación técnica...</p>
    </div>
  `;
  document.getElementById("compare-modal").classList.remove("hidden");
  document.body.classList.add("overflow-hidden");

  try {
    const data = await API.compareRepos(state.selectedForCompare);
    const repos = data.items || [];

    if (repos.length === 0) {
      container.innerHTML = `<p class="text-center text-slate-400 py-6">No se pudieron cargar los datos de comparación.</p>`;
      return;
    }

    container.innerHTML = `
      <table class="w-full text-left text-xs text-slate-200 border-collapse">
        <thead>
          <tr class="border-b border-slate-800">
            <th class="p-3 w-40 text-slate-400 font-semibold uppercase text-[10px]">Criterio</th>
            ${repos.map(r => `
              <th class="p-3 min-w-[200px]">
                <div class="font-bold text-sm text-white">${r.name}</div>
                <div class="text-[11px] text-indigo-400 font-normal">${r.category}</div>
              </th>
            `).join("")}
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60 font-sans">
          <tr>
            <td class="p-3 text-slate-400 font-medium">Health Score</td>
            ${repos.map(r => `
              <td class="p-3">
                <span class="px-2 py-0.5 rounded-full text-xs font-mono font-bold ${r.health_score >= 90 ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'}">
                  ${r.health_score}% (${r.maintenance_level})
                </span>
              </td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Estrellas GitHub</td>
            ${repos.map(r => `
              <td class="p-3 font-mono font-bold text-amber-400">★ ${r.stars.toLocaleString()}</td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Lenguaje & Licencia</td>
            ${repos.map(r => `
              <td class="p-3 font-mono text-slate-300">${r.language} • <span class="text-indigo-400">${r.license}</span></td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Alternativa SaaS</td>
            ${repos.map(r => `
              <td class="p-3 text-slate-300">${r.saas_alternative || "Propietario"}</td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Ahorro Mensual Est.</td>
            ${repos.map(r => `
              <td class="p-3 font-mono text-emerald-400 font-semibold">+$${r.estimated_monthly_saas_cost || 100} USD/mes</td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Forks / Issues</td>
            ${repos.map(r => `
              <td class="p-3 font-mono text-slate-400">${r.forks.toLocaleString()} forks / ${r.open_issues} issues</td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Patrón Integración</td>
            ${repos.map(r => `
              <td class="p-3">
                <span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-mono">
                  ${(r.integrations && r.integrations[0] && r.integrations[0].integration_type) || "SDK / REST"}
                </span>
              </td>
            `).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Stack Compatible</td>
            ${repos.map(r => {
              const compat = (r.integrations && r.integrations[0] && r.integrations[0].stack_compatibility) || [];
              return `
                <td class="p-3">
                  <div class="flex flex-wrap gap-1">
                    ${compat.map(c => `<span class="px-1.5 py-0.5 bg-slate-950 border border-slate-800 rounded text-[10px] text-slate-400 font-mono">${c}</span>`).join("")}
                  </div>
                </td>
              `;
            }).join("")}
          </tr>
          <tr>
            <td class="p-3 text-slate-400 font-medium">Enlaces</td>
            ${repos.map(r => `
              <td class="p-3">
                <a href="${r.github_url}" target="_blank" rel="noopener noreferrer" class="text-indigo-400 hover:underline font-mono text-[11px] block">
                  GitHub ↗
                </a>
              </td>
            `).join("")}
          </tr>
        </tbody>
      </table>
    `;
  } catch (err) {
    console.error("Error comparando repos:", err);
    container.innerHTML = `<p class="text-center text-red-400 py-6">Ocurrió un error al cargar la comparativa.</p>`;
  }
}

function closeCompareModal() {
  document.getElementById("compare-modal").classList.add("hidden");
  document.body.classList.remove("overflow-hidden");
}

// ==================== INGESTIÓN DE REPOSITORIO EN VIVO ====================

function openAddRepoModal() {
  document.getElementById("add-repo-modal").classList.remove("hidden");
  document.body.classList.add("overflow-hidden");
  document.getElementById("new-repo-fullname").focus();
}

function closeAddRepoModal() {
  document.getElementById("add-repo-modal").classList.add("hidden");
  document.body.classList.remove("overflow-hidden");
}

async function submitAddRepo(event) {
  event.preventDefault();
  const fullName = document.getElementById("new-repo-fullname").value.trim();
  const category = document.getElementById("new-repo-category").value;
  const saas = document.getElementById("new-repo-saas").value.trim();
  const cost = parseInt(document.getElementById("new-repo-cost").value) || 150;

  if (!fullName || !fullName.includes("/")) {
    showToast("Por favor ingresa un repositorio en formato owner/repo");
    return;
  }

  const btn = document.getElementById("btn-submit-add-repo");
  btn.disabled = true;
  btn.classList.add("opacity-50", "cursor-not-allowed");
  btn.innerHTML = `
    <div class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
    <span>Analizando GitHub...</span>
  `;

  try {
    const res = await API.addRepo({
      full_name: fullName,
      category: category,
      saas_alternative: saas,
      estimated_monthly_saas_cost: cost
    });

    if (res.error) {
      showToast(res.error);
      return;
    }

    showToast(res.message || "Repositorio agregado con éxito");
    closeAddRepoModal();
    document.getElementById("new-repo-fullname").value = "";
    document.getElementById("new-repo-saas").value = "";

    await Promise.all([
      loadStats(),
      loadCategories(),
      fetchAndRenderRepos()
    ]);
  } catch (err) {
    console.error("Error al agregar repo:", err);
    showToast("Error al conectar con el servidor para ingestar");
  } finally {
    btn.disabled = false;
    btn.classList.remove("opacity-50", "cursor-not-allowed");
    btn.innerHTML = `
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
      <span>Analizar e Ingestar</span>
    `;
  }
}
