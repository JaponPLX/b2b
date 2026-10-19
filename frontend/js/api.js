/**
 * Cliente de comunicación con la API REST del backend
 */

const API = {
  async getRepos(params = {}) {
    const qs = new URLSearchParams();
    if (params.q) qs.set("q", params.q);
    if (params.category && params.category !== "all") qs.set("category", params.category);
    if (params.language && params.language !== "all") qs.set("language", params.language);
    if (params.license && params.license !== "all") qs.set("license", params.license);
    if (params.maintenance && params.maintenance !== "all") qs.set("maintenance", params.maintenance);
    if (params.min_stars) qs.set("min_stars", params.min_stars);
    if (params.sort_by) qs.set("sort_by", params.sort_by);
    if (params.limit) qs.set("limit", params.limit);
    if (params.offset) qs.set("offset", params.offset);

    const res = await fetch(`/api/repos?${qs.toString()}`);
    return await res.json();
  },

  async getRepoById(id) {
    const res = await fetch(`/api/repos/${id}`);
    return await res.json();
  },

  async getCategories() {
    const res = await fetch("/api/categories");
    return await res.json();
  },

  async getFilters() {
    const res = await fetch("/api/filters");
    return await res.json();
  },

  async getStats() {
    const res = await fetch("/api/stats");
    return await res.json();
  },

  async compareRepos(ids) {
    const res = await fetch(`/api/repos/compare?ids=${ids.join(",")}`);
    return await res.json();
  },

  async addRepo(data) {
    const res = await fetch("/api/repos/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async recommendArchitecture(prompt) {
    const res = await fetch("/api/rag/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    return await res.json();
  },

  async triggerSync(limit = 10) {
    const res = await fetch("/api/pipeline/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ limit })
    });
    return await res.json();
  },

  async getSyncLogs() {
    const res = await fetch("/api/pipeline/logs");
    return await res.json();
  },

  async saveBlueprint(payload) {
    const res = await fetch("/api/blueprints", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  async getBlueprints() {
    const res = await fetch("/api/blueprints");
    return await res.json();
  },

  async getBlueprintById(id) {
    const res = await fetch(`/api/blueprints/${id}`);
    return await res.json();
  },

  async deleteBlueprint(id) {
    const res = await fetch(`/api/blueprints/${id}/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    return await res.json();
  },

  async getNetworkInfo() {
    try {
      const res = await fetch("/api/system/network");
      return await res.json();
    } catch (e) {
      return {
        local_url: window.location.origin,
        network_url: window.location.origin,
        local_ip: window.location.hostname
      };
    }
  }
};
