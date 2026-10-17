"""
Dataset curado con más de 100 repositorios open source clave para arquitecturas B2B,
con fichas técnicas, métricas de salud e ideas de integración estructuradas.
"""

SEED_REPOSITORIES = [
    # ----------------- 1. AUTENTICACIÓN Y AUTORIZACIÓN -----------------
    {
        "id": "keycloak",
        "name": "Keycloak",
        "full_name": "keycloak/keycloak",
        "category": "Autenticación",
        "description": "Servidor de gestión de identidad y acceso open source para aplicaciones modernas con OIDC, OAuth 2.0 y SAML.",
        "stars": 24200,
        "forks": 6800,
        "open_issues": 1200,
        "last_updated": "2026-10-15T18:22:00Z",
        "license": "Apache-2.0",
        "language": "Java",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.keycloak.org",
        "github_url": "https://github.com/keycloak/keycloak",
        "docs_url": "https://www.keycloak.org/documentation",
        "saas_alternative": "Auth0 / Okta",
        "estimated_monthly_saas_cost": 240,
        "tags": ["auth", "oidc", "oauth2", "sso", "identity", "saml", "security"],
        "integration": {
            "title": "Despliegue Docker y validación JWT en backend",
            "integration_type": "Docker",
            "stack_compatibility": ["Docker", "Node.js", "FastAPI", "Go"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Eventos de login, cambio de password y registro",
            "dependencies": ["docker", "postgres"],
            "docs_link": "https://www.keycloak.org/getting-started/getting-started-docker",
            "explanation": "Despliega Keycloak conectado a Postgres para gestionar SSO centralizado y validar JWTs sin consultar el servidor en cada request.",
            "code_snippet": """# docker-compose.yml para Keycloak con PostgreSQL
services:
  keycloak:
    image: quay.io/keycloak/keycloak:26.0
    command: start-dev
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://db:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: secret_password
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin_password
    ports:
      - "8080:8080"
"""
        }
    },
    {
        "id": "authjs",
        "name": "Auth.js (NextAuth)",
        "full_name": "nextauthjs/next-auth",
        "category": "Autenticación",
        "description": "Librería completa de autenticación para Next.js, SvelteKit, Express y frameworks modernos.",
        "stars": 26800,
        "forks": 3500,
        "open_issues": 310,
        "last_updated": "2026-10-16T10:00:00Z",
        "license": "ISC",
        "language": "TypeScript",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://authjs.dev",
        "github_url": "https://github.com/nextauthjs/next-auth",
        "docs_url": "https://authjs.dev/getting-started",
        "saas_alternative": "Clerk / Auth0",
        "estimated_monthly_saas_cost": 120,
        "tags": ["auth", "nextjs", "oauth", "jwt", "session", "typescript"],
        "integration": {
            "title": "Integración con Next.js App Router y GitHub/Google Provider",
            "integration_type": "SDK",
            "stack_compatibility": ["Next.js", "React", "TypeScript"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Callbacks de signIn, session y jwt",
            "dependencies": ["next-auth@beta", "@auth/core"],
            "docs_link": "https://authjs.dev/getting-started/installation",
            "explanation": "Configura Auth.js en Next.js para sesiones seguras vía cookies HttpOnly con proveedores sociales.",
            "code_snippet": """// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.sub;
      return session;
    },
  },
});
export const { GET, POST } = handlers;
"""
        }
    },
    {
        "id": "supertokens",
        "name": "SuperTokens",
        "full_name": "supertokens/supertokens-core",
        "category": "Autenticación",
        "description": "Alternativa open source a Auth0 y AWS Cognito con soporte nativo para sesiones rotativas y login passwordless.",
        "stars": 13900,
        "forks": 850,
        "open_issues": 120,
        "last_updated": "2026-10-14T14:15:00Z",
        "license": "Apache-2.0",
        "language": "Java",
        "health_score": 92,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://supertokens.com",
        "github_url": "https://github.com/supertokens/supertokens-core",
        "docs_url": "https://supertokens.com/docs",
        "saas_alternative": "Auth0 / Clerk",
        "estimated_monthly_saas_cost": 180,
        "tags": ["auth", "session-management", "passwordless", "mfa", "jwt"],
        "integration": {
            "title": "Middleware de protección de rutas en Node.js Express",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Express", "FastAPI"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Eventos de sesión expirada, logout y MFA",
            "dependencies": ["supertokens-node"],
            "docs_link": "https://supertokens.com/docs/session/introduction",
            "explanation": "Inyecta verificación de sesiones criptográficamente protegidas contra ataques XSS y CSRF.",
            "code_snippet": """import express from "express";
import supertokens from "supertokens-node";
import Session from "supertokens-node/recipe/session";
import { verifySession } from "supertokens-node/recipe/session/framework/express";

const app = express();
app.get("/api/user/profile", verifySession(), async (req, res) => {
  const userId = req.session.getUserId();
  res.json({ userId, status: "authorized" });
});
"""
        }
    },
    {
        "id": "logto",
        "name": "Logto",
        "full_name": "logto-io/logto",
        "category": "Autenticación",
        "description": "Infraestructura de autenticación e identidad moderna con soporte multi-tenant y UI prediseñada.",
        "stars": 10500,
        "forks": 650,
        "open_issues": 95,
        "last_updated": "2026-10-15T09:30:00Z",
        "license": "Mozilla Public License 2.0",
        "language": "TypeScript",
        "health_score": 91,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://logto.io",
        "github_url": "https://github.com/logto-io/logto",
        "docs_url": "https://docs.logto.io",
        "saas_alternative": "Auth0 / WorkOS",
        "estimated_monthly_saas_cost": 210,
        "tags": ["auth", "multi-tenant", "rbac", "b2b", "identity", "nextjs"],
        "integration": {
            "title": "Configuración B2B Multi-tenant con OIDC",
            "integration_type": "REST API",
            "stack_compatibility": ["Next.js", "React", "Vue", "Python"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "User registration, organization created",
            "dependencies": ["@logto/next"],
            "docs_link": "https://docs.logto.io/quick-start",
            "explanation": "Gestiona organizaciones de clientes B2B con permisos RBAC personalizados y portal de login white-label.",
            "code_snippet": """import LogtoClient from "@logto/next";

export const logtoClient = new LogtoClient({
  endpoint: process.env.LOGTO_ENDPOINT,
  appId: process.env.LOGTO_APP_ID,
  appSecret: process.env.LOGTO_APP_SECRET,
  baseUrl: "http://localhost:3000",
  cookieSecret: process.env.COOKIE_SECRET,
  cookieSecure: process.env.NODE_ENV === "production",
});
"""
        }
    },
    {
        "id": "zitadel",
        "name": "Zitadel",
        "full_name": "zitadel/zitadel",
        "category": "Autenticación",
        "description": "Sistema de gestión de identidad cloud-native con soporte B2B multi-tenant, auditoría y passkeys.",
        "stars": 11200,
        "forks": 720,
        "open_issues": 160,
        "last_updated": "2026-10-14T20:10:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 93,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://zitadel.com",
        "github_url": "https://github.com/zitadel/zitadel",
        "docs_url": "https://zitadel.com/docs",
        "saas_alternative": "Okta / Auth0",
        "estimated_monthly_saas_cost": 250,
        "tags": ["auth", "identity", "passkeys", "b2b", "audit-log", "golang"],
        "integration": {
            "title": "Verificación OIDC introspect en Golang / Python",
            "integration_type": "REST API",
            "stack_compatibility": ["Go", "Python", "Node.js"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Token issuance, role change",
            "dependencies": ["zitadel-client"],
            "docs_link": "https://zitadel.com/docs/guides/integrate/api",
            "explanation": "Valida tokens OIDC contra el endpoint de introspección de Zitadel con auditoría completa de acceso.",
            "code_snippet": """# Validación en FastAPI
import requests
from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

def verify_zitadel_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    resp = requests.post("http://zitadel:8080/oauth/v2/introspect", data={"token": token})
    data = resp.json()
    if not data.get("active"):
        raise HTTPException(status_code=401, detail="Token no válido")
    return data
"""
        }
    },
    {
        "id": "ory-kratos",
        "name": "Ory Kratos",
        "full_name": "ory/kratos",
        "category": "Autenticación",
        "description": "Sistema headless de identidad y gestión de usuarios según principios Zero Trust.",
        "stars": 6100,
        "forks": 620,
        "open_issues": 140,
        "last_updated": "2026-10-12T11:00:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 88,
        "maintenance_level": "Activo",
        "active_maintainer": True,
        "website_url": "https://www.ory.sh/kratos",
        "github_url": "https://github.com/ory/kratos",
        "docs_url": "https://www.ory.sh/docs/kratos",
        "saas_alternative": "Auth0 / Firebase Auth",
        "estimated_monthly_saas_cost": 150,
        "tags": ["auth", "zero-trust", "identity", "headless", "self-hosted"],
        "integration": {
            "title": "Flujo de registro y recuperación headless",
            "integration_type": "REST API",
            "stack_compatibility": ["React", "Vue", "FastAPI"],
            "difficulty": "Avanzado",
            "triggers_webhooks": "Webhook de post-registration a CRM",
            "dependencies": ["@ory/client"],
            "docs_link": "https://www.ory.sh/docs/kratos/sdk",
            "explanation": "Permite construir pantallas de login 100% personalizadas consumiendo el motor headless de Kratos.",
            "code_snippet": """import { Configuration, FrontendApi } from "@ory/client";

const frontend = new FrontendApi(
  new Configuration({ basePath: "http://localhost:4433" })
);
const flow = await frontend.createBrowserLoginFlow();
console.log("Login Flow ID:", flow.data.id);
"""
        }
    },

    # ----------------- 2. BASE DE DATOS Y BAAS -----------------
    {
        "id": "supabase",
        "name": "Supabase",
        "full_name": "supabase/supabase",
        "category": "Base de Datos",
        "description": "Alternativa de código abierto a Firebase con PostgreSQL, Auth, Realtime, Edge Functions y Storage.",
        "stars": 74500,
        "forks": 6200,
        "open_issues": 890,
        "last_updated": "2026-10-16T22:15:00Z",
        "license": "Apache-2.0",
        "language": "TypeScript",
        "health_score": 98,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://supabase.com",
        "github_url": "https://github.com/supabase/supabase",
        "docs_url": "https://supabase.com/docs",
        "saas_alternative": "Firebase / AWS Amplify",
        "estimated_monthly_saas_cost": 200,
        "tags": ["postgres", "realtime", "auth", "storage", "database", "baas"],
        "integration": {
            "title": "Conexión Realtime y consultas con RLS (Row Level Security)",
            "integration_type": "SDK",
            "stack_compatibility": ["Next.js", "React", "Node.js", "Python"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Database Webhooks en INSERT/UPDATE/DELETE",
            "dependencies": ["@supabase/supabase-js"],
            "docs_link": "https://supabase.com/docs/reference/javascript",
            "explanation": "Conecta tu cliente frontend directamente a PostgreSQL respetando políticas de seguridad RLS por tenant.",
            "code_snippet": """import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

const channel = supabase
  .channel("pedidos_b2b")
  .on("postgres_changes", { event: "INSERT", schema: "public", table: "pedidos" }, (payload) => {
    console.log("Nuevo pedido recibido:", payload.new);
  })
  .subscribe();
"""
        }
    },
    {
        "id": "appwrite",
        "name": "Appwrite",
        "full_name": "appwrite/appwrite",
        "category": "Base de Datos",
        "description": "Plataforma de Backend-as-a-Service segura y auto-hospedada para web, mobile y Flutter.",
        "stars": 45100,
        "forks": 4100,
        "open_issues": 340,
        "last_updated": "2026-10-15T16:40:00Z",
        "license": "BSD-3-Clause",
        "language": "TypeScript",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://appwrite.io",
        "github_url": "https://github.com/appwrite/appwrite",
        "docs_url": "https://appwrite.io/docs",
        "saas_alternative": "Firebase / AWS Cognito + DynamoDB",
        "estimated_monthly_saas_cost": 170,
        "tags": ["baas", "database", "storage", "functions", "mobile", "auth"],
        "integration": {
            "title": "Subida de archivos y consulta de documentos",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Flutter", "React", "Python"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Webhooks en colecciones y autenticación",
            "dependencies": ["node-appwrite"],
            "docs_link": "https://appwrite.io/docs/quick-starts",
            "explanation": "Almacena contratos, facturas y metadatos con control de permisos granular por usuario.",
            "code_snippet": """import { Client, Databases, ID } from "node-appwrite";

const client = new Client()
  .setEndpoint("https://cloud.appwrite.io/v1")
  .setProject("mi-proyecto-b2b")
  .setKey("API_SECRET_KEY");

const databases = new Databases(client);
const response = await databases.createDocument(
  "database_id",
  "pedidos_col",
  ID.unique(),
  { cliente: "Acme Corp", total: 4500.0, estado: "confirmado" }
);
"""
        }
    },
    {
        "id": "pocketbase",
        "name": "PocketBase",
        "full_name": "pocketbase/pocketbase",
        "category": "Base de Datos",
        "description": "Backend open source en un solo binario de Go con SQLite embebido, auth y suscripciones en tiempo real.",
        "stars": 42000,
        "forks": 2200,
        "open_issues": 45,
        "last_updated": "2026-10-16T19:00:00Z",
        "license": "MIT",
        "language": "Go",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://pocketbase.io",
        "github_url": "https://github.com/pocketbase/pocketbase",
        "docs_url": "https://pocketbase.io/docs",
        "saas_alternative": "Firebase Realtime / Supabase Pro",
        "estimated_monthly_saas_cost": 80,
        "tags": ["sqlite", "baas", "go", "embedded", "realtime", "minimal"],
        "integration": {
            "title": "Arranque en 1 línea y suscripción SDK cliente",
            "integration_type": "SDK",
            "stack_compatibility": ["JavaScript", "Dart", "Svelte", "React"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Hooks en Go y suscripción realtime SSE",
            "dependencies": ["pocketbase"],
            "docs_link": "https://pocketbase.io/docs/js-overview",
            "explanation": "Ideal para MVPs y prototipos que necesitan base de datos, auth y dashboard administrativo sin servidores complejos.",
            "code_snippet": """import PocketBase from "pocketbase";

const pb = new PocketBase("http://127.0.0.1:8090");
await pb.collection("users").authWithPassword("dev@empresa.com", "password123");

pb.collection("facturas").subscribe("*", function (e) {
  console.log("Factura actualizada:", e.action, e.record);
});
"""
        }
    },
    {
        "id": "hasura",
        "name": "Hasura GraphQL Engine",
        "full_name": "hasura/graphql-engine",
        "category": "Base de Datos",
        "description": "API instantánea GraphQL y REST sobre PostgreSQL, MySQL, SQL Server y MongoDB con permisos RBAC.",
        "stars": 31500,
        "forks": 2900,
        "open_issues": 1100,
        "last_updated": "2026-10-14T08:00:00Z",
        "license": "Apache-2.0",
        "language": "Haskell",
        "health_score": 89,
        "maintenance_level": "Activo",
        "active_maintainer": True,
        "website_url": "https://hasura.io",
        "github_url": "https://github.com/hasura/graphql-engine",
        "docs_url": "https://hasura.io/docs",
        "saas_alternative": "AWS AppSync",
        "estimated_monthly_saas_cost": 220,
        "tags": ["graphql", "postgres", "api", "rbac", "subscriptions"],
        "integration": {
            "title": "Exposición de GraphQL y Event Triggers hacia Webhooks",
            "integration_type": "Webhook",
            "stack_compatibility": ["GraphQL", "PostgreSQL", "Docker", "Node.js"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Event Triggers automáticos en modificaciones de filas",
            "dependencies": ["hasura-cli", "docker"],
            "docs_link": "https://hasura.io/docs/latest/event-triggers/overview",
            "explanation": "Genera una API GraphQL lista para producción sobre tu Postgres y dispara webhooks a microservicios en cambios de datos.",
            "code_snippet": """query ObtenerClientesB2B {
  clientes(where: { activo: { _eq: true } }) {
    id
    razon_social
    limite_credito
    pedidos_aggregate {
      aggregate { count sum { total } }
    }
  }
}
"""
        }
    },
    {
        "id": "prisma",
        "name": "Prisma ORM",
        "full_name": "prisma/prisma",
        "category": "Base de Datos",
        "description": "ORM de nueva generación para Node.js y TypeScript con migraciones declarativas y consultas tipadas.",
        "stars": 39500,
        "forks": 1600,
        "open_issues": 1400,
        "last_updated": "2026-10-16T15:20:00Z",
        "license": "Apache-2.0",
        "language": "TypeScript",
        "health_score": 93,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.prisma.io",
        "github_url": "https://github.com/prisma/prisma",
        "docs_url": "https://www.prisma.io/docs",
        "saas_alternative": "PlanetScale Hosted ORM / Fauna",
        "estimated_monthly_saas_cost": 90,
        "tags": ["orm", "typescript", "postgres", "mysql", "sqlite", "database"],
        "integration": {
            "title": "Modelado de catálogo B2B y transacciones seguras",
            "integration_type": "SDK",
            "stack_compatibility": ["Next.js", "Express", "NestJS", "TypeScript"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Prisma Client Extensions para auditoría",
            "dependencies": ["@prisma/client", "prisma"],
            "docs_link": "https://www.prisma.io/docs/getting-started",
            "explanation": "Type-safety de extremo a extremo entre el esquema de la base de datos y tus componentes frontend.",
            "code_snippet": """import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

export async function crearPedidoConInventario(clienteId: string, items: Array<{ sku: string; cant: number }>) {
  return await prisma.$transaction(async (tx) => {
    const pedido = await tx.pedido.create({ data: { clienteId, items: { create: items } } });
    for (const item of items) {
      await tx.producto.update({ where: { sku: item.sku }, data: { stock: { decrement: item.cant } } });
    }
    return pedido;
  });
}
"""
        }
    },
    {
        "id": "drizzle-orm",
        "name": "Drizzle ORM",
        "full_name": "drizzle-team/drizzle-orm",
        "category": "Base de Datos",
        "description": "ORM TypeScript ultra-rápido y ligero con sintaxis tipo SQL y cero sobrecarga de rendimiento.",
        "stars": 36500,
        "forks": 1100,
        "open_issues": 290,
        "last_updated": "2026-10-16T21:00:00Z",
        "license": "Apache-2.0",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://orm.drizzle.team",
        "github_url": "https://github.com/drizzle-team/drizzle-orm",
        "docs_url": "https://orm.drizzle.team/docs/overview",
        "saas_alternative": "Custom DB Drivers",
        "estimated_monthly_saas_cost": 50,
        "tags": ["orm", "typescript", "sql", "serverless", "edge"],
        "integration": {
            "title": "Esquema tipado con soporte nativo de pgvector",
            "integration_type": "SDK",
            "stack_compatibility": ["Next.js", "Cloudflare Workers", "Node.js"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Hooks de aplicación",
            "dependencies": ["drizzle-orm", "pg"],
            "docs_link": "https://orm.drizzle.team/docs/get-started-postgresql",
            "explanation": "Consultas SQL ultra optimizadas compatibles con entornos serverless y microservicios de alto tráfico.",
            "code_snippet": """import { pgTable, serial, text, timestamp, vector } from "drizzle-orm/pg-core";
import { drizzle } from "drizzle-orm/node-postgres";

export const reposTable = pgTable("repos", {
  id: serial("id").primaryKey(),
  nombre: text("nombre").notNull(),
  embedding: vector("embedding", { dimensions: 1536 }),
  creadoEn: timestamp("creado_en").defaultNow(),
});
"""
        }
    },

    # ----------------- 3. BÚSQUEDA Y EMBEDDINGS VECTORIALES -----------------
    {
        "id": "meilisearch",
        "name": "Meilisearch",
        "full_name": "meilisearch/meilisearch",
        "category": "Búsqueda",
        "description": "Motor de búsqueda full-text ultrarrápido, tolerante a fallos tipográficos y con soporte de búsqueda híbrida vectorial.",
        "stars": 47200,
        "forks": 1900,
        "open_issues": 130,
        "last_updated": "2026-10-15T12:00:00Z",
        "license": "MIT",
        "language": "Rust",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.meilisearch.com",
        "github_url": "https://github.com/meilisearch/meilisearch",
        "docs_url": "https://www.meilisearch.com/docs",
        "saas_alternative": "Algolia",
        "estimated_monthly_saas_cost": 300,
        "tags": ["search", "rust", "instant-search", "typo-tolerance", "vector-search"],
        "integration": {
            "title": "Búsqueda instantánea con filtros facetados para catálogo B2B",
            "integration_type": "REST API",
            "stack_compatibility": ["React", "Vue", "Next.js", "Python", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Indexación sincrónica / asincrónica vía webhook",
            "dependencies": ["meilisearch"],
            "docs_link": "https://www.meilisearch.com/docs/learn/getting_started/quick_start",
            "explanation": "Configura búsqueda instantánea (<50ms) con tolerancia a errores ortográficos y filtrado facetado por categoría/licencia.",
            "code_snippet": """import { MeiliSearch } from "meilisearch";

const client = new MeiliSearch({ host: "http://127.0.0.1:7700", apiKey: "MASTER_KEY" });
const index = client.index("catalogo_repos");

const resultados = await index.search("autenticacion oauth2", {
  filter: ["license = 'MIT' AND stars >= 5000"],
  facets: ["category", "language"],
  limit: 20,
});
console.log("Hits:", resultados.hits);
"""
        }
    },
    {
        "id": "typesense",
        "name": "Typesense",
        "full_name": "typesense/typesense",
        "category": "Búsqueda",
        "description": "Motor de búsqueda open-source rápido en memoria con tipado estricto, geosearch y búsqueda semántica.",
        "stars": 20800,
        "forks": 1100,
        "open_issues": 210,
        "last_updated": "2026-10-14T17:30:00Z",
        "license": "GPL-3.0",
        "language": "C++",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://typesense.org",
        "github_url": "https://github.com/typesense/typesense",
        "docs_url": "https://typesense.org/docs",
        "saas_alternative": "Algolia / Elastic Cloud",
        "estimated_monthly_saas_cost": 280,
        "tags": ["search", "fast", "in-memory", "semantic-search", "cpp"],
        "integration": {
            "title": "Búsqueda semántica integrada con embeddings generados",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Python", "Ruby", "PHP"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Index batch webhooks",
            "dependencies": ["typesense"],
            "docs_link": "https://typesense.org/docs/guide/semantic-search.html",
            "explanation": "Permite realizar búsquedas por significado conceptual además de coincidencia exacta de palabras clave.",
            "code_snippet": """import Typesense from "typesense";

const client = new Typesense.Client({
  nodes: [{ host: "localhost", port: 8108, protocol: "http" }],
  apiKey: "xyz",
  connectionTimeoutSeconds: 2
});

const searchResult = await client.collections("repos").documents().search({
  q: "herramienta para colas de tareas background",
  query_by: "description,tags",
});
"""
        }
    },
    {
        "id": "qdrant",
        "name": "Qdrant",
        "full_name": "qdrant/qdrant",
        "category": "Búsqueda",
        "description": "Base de datos vectorial y motor de búsqueda de similitud de vectores de alta performance con API REST y gRPC.",
        "stars": 22300,
        "forks": 1500,
        "open_issues": 160,
        "last_updated": "2026-10-16T18:00:00Z",
        "license": "Apache-2.0",
        "language": "Rust",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://qdrant.tech",
        "github_url": "https://github.com/qdrant/qdrant",
        "docs_url": "https://qdrant.tech/documentation",
        "saas_alternative": "Pinecone",
        "estimated_monthly_saas_cost": 190,
        "tags": ["vector-search", "rag", "embeddings", "similarity", "rust", "ai"],
        "integration": {
            "title": "Almacenamiento y búsqueda RAG con filtrado por metadatos",
            "integration_type": "REST API",
            "stack_compatibility": ["Python", "FastAPI", "Node.js", "Docker"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Colecciones y snapshots",
            "dependencies": ["qdrant-client"],
            "docs_link": "https://qdrant.tech/documentation/quick-start",
            "explanation": "Permite recuperar fragmentos de contexto basados en embeddings semánticos filtrando simultáneamente por categoría funcional.",
            "code_snippet": """from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient("http://localhost:6333")

puntos = client.search(
    collection_name="catalogo_tecnologias",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="IA & LLMs"))]
    ),
    limit=5
)
"""
        }
    },
    {
        "id": "chromadb",
        "name": "ChromaDB",
        "full_name": "chroma-core/chroma",
        "category": "Búsqueda",
        "description": "Base de datos vectorial embebida nativa para IA enfocada en simplicidad y rapidez para pipelines de RAG.",
        "stars": 16800,
        "forks": 1400,
        "open_issues": 280,
        "last_updated": "2026-10-15T20:30:00Z",
        "license": "Apache-2.0",
        "language": "Python",
        "health_score": 93,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.trychroma.com",
        "github_url": "https://github.com/chroma-core/chroma",
        "docs_url": "https://docs.trychroma.com",
        "saas_alternative": "Pinecone / Weaviate Cloud",
        "estimated_monthly_saas_cost": 140,
        "tags": ["vector-database", "rag", "embeddings", "python", "ai"],
        "integration": {
            "title": "Vector store local embebido para agente consultor RAG",
            "integration_type": "SDK",
            "stack_compatibility": ["Python", "FastAPI", "LangChain"],
            "difficulty": "Fácil",
            "triggers_webhooks": "In-memory / persistente en disco",
            "dependencies": ["chromadb"],
            "docs_link": "https://docs.trychroma.com/getting-started",
            "explanation": "Guarda y recupera documentos técnicos con cálculo automático de embeddings sin necesidad de levantar servicios externos.",
            "code_snippet": """import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_or_create_collection("tecnologias")

collection.add(
    documents=["Keycloak servidor OIDC para federación de identidades.", "Supabase BaaS PostgreSQL."],
    metadatas=[{"category": "Autenticación"}, {"category": "Base de Datos"}],
    ids=["keycloak", "supabase"]
)

results = collection.query(query_texts=["cómo gestionar login multi-empresa"], n_results=2)
"""
        }
    },

    # ----------------- 4. INTELIGENCIA ARTIFICIAL Y LLMS -----------------
    {
        "id": "ollama",
        "name": "Ollama",
        "full_name": "ollama/ollama",
        "category": "IA & LLMs",
        "description": "Herramienta líder para ejecutar localmente modelos de lenguaje (Llama 3, Mistral, Gemma, Phi) con API compatible con OpenAI.",
        "stars": 118000,
        "forks": 9800,
        "open_issues": 1300,
        "last_updated": "2026-10-16T23:00:00Z",
        "license": "MIT",
        "language": "Go",
        "health_score": 99,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://ollama.com",
        "github_url": "https://github.com/ollama/ollama",
        "docs_url": "https://github.com/ollama/ollama/blob/main/docs/api.md",
        "saas_alternative": "OpenAI API / Anthropic",
        "estimated_monthly_saas_cost": 350,
        "tags": ["llm", "ai", "local-ai", "inference", "llama", "docker"],
        "integration": {
            "title": "Inferencia privada local de LLMs mediante API REST compatible con OpenAI",
            "integration_type": "REST API",
            "stack_compatibility": ["Python", "Node.js", "Docker", "cURL"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Streaming SSE de tokens generados",
            "dependencies": ["ollama", "docker"],
            "docs_link": "https://ollama.com/library",
            "explanation": "Permite a las consultoras tech procesar datos confidenciales de clientes B2B sin enviarlos a APIs de terceros.",
            "code_snippet": """import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:latest",
    "prompt": "Genera el diagrama C4 para una plataforma de logística B2B.",
    "stream": False
})
print("Respuesta LLM:", response.json()["response"])
"""
        }
    },
    {
        "id": "langchain",
        "name": "LangChain",
        "full_name": "langchain-ai/langchain",
        "category": "IA & LLMs",
        "description": "Framework para construir aplicaciones contextuales impulsadas por modelos de lenguaje razonadores.",
        "stars": 98500,
        "forks": 15800,
        "open_issues": 1900,
        "last_updated": "2026-10-16T20:45:00Z",
        "license": "MIT",
        "language": "Python",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.langchain.com",
        "github_url": "https://github.com/langchain-ai/langchain",
        "docs_url": "https://python.langchain.com/docs",
        "saas_alternative": "Proprietary AI orchestration engines",
        "estimated_monthly_saas_cost": 200,
        "tags": ["llm", "rag", "agents", "python", "ai-framework"],
        "integration": {
            "title": "Pipeline RAG con memoria de conversación y recuperación vectorial",
            "integration_type": "SDK",
            "stack_compatibility": ["Python", "FastAPI"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Callbacks de tokens y ejecuciones",
            "dependencies": ["langchain", "langchain-core"],
            "docs_link": "https://python.langchain.com/docs/tutorials/rag",
            "explanation": "Orquesta la recuperación de fragmentos técnicos del catálogo y compone la respuesta estructurada para el usuario.",
            "code_snippet": """from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "Como arquitecto B2B, analiza este requerimiento: {req}. Contexto: {context}"
)
chain = prompt | model | StrOutputParser()
resultado = chain.invoke({"req": "E-commerce B2B de repuestos", "context": "Keycloak + Supabase + Medusa"})
"""
        }
    },
    {
        "id": "llamaindex",
        "name": "LlamaIndex",
        "full_name": "run-llama/llama_index",
        "category": "IA & LLMs",
        "description": "Framework especializado en ingesta, indexación y recuperación de datos estructurados y no estructurados para RAG.",
        "stars": 38200,
        "forks": 4900,
        "open_issues": 410,
        "last_updated": "2026-10-16T17:15:00Z",
        "license": "MIT",
        "language": "Python",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.llamaindex.ai",
        "github_url": "https://github.com/run-llama/llama_index",
        "docs_url": "https://docs.llamaindex.ai",
        "saas_alternative": "Glean / Enterprise Search AI",
        "estimated_monthly_saas_cost": 300,
        "tags": ["rag", "indexing", "vector", "knowledge-graph", "python"],
        "integration": {
            "title": "Motor de consultas semánticas sobre documentación técnica",
            "integration_type": "SDK",
            "stack_compatibility": ["Python", "FastAPI"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Index updates",
            "dependencies": ["llama-index"],
            "docs_link": "https://docs.llamaindex.ai/en/stable/getting_started/starter_example",
            "explanation": "Indexa repositorios, READMEs y esquemas de base de datos para responder consultas de ingeniería en lenguaje natural.",
            "code_snippet": """from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./docs_catalogo").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
respuesta = query_engine.query("¿Qué tecnología de base de datos soporta Row Level Security out-of-the-box?")
print(respuesta)
"""
        }
    },
    {
        "id": "flowise",
        "name": "Flowise",
        "full_name": "FlowiseAI/Flowise",
        "category": "IA & LLMs",
        "description": "Interfaz gráfica no-code / low-code drag-and-drop para construir flujos de trabajo con LangChain y modelos LLM.",
        "stars": 34100,
        "forks": 17200,
        "open_issues": 430,
        "last_updated": "2026-10-15T21:10:00Z",
        "license": "GPL-3.0",
        "language": "TypeScript",
        "health_score": 92,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://flowiseai.com",
        "github_url": "https://github.com/FlowiseAI/Flowise",
        "docs_url": "https://docs.flowiseai.com",
        "saas_alternative": "Voiceflow / Botpress Cloud",
        "estimated_monthly_saas_cost": 160,
        "tags": ["no-code", "langchain", "llm-ui", "workflow", "typescript"],
        "integration": {
            "title": "Consumo de flujos de IA vía API Prediction",
            "integration_type": "REST API",
            "stack_compatibility": ["React", "Next.js", "Python", "cURL"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Eventos de predicción y chatbot UI widget",
            "dependencies": ["docker"],
            "docs_link": "https://docs.flowiseai.com/api-reference",
            "explanation": "Permite a los analistas de negocio ajustar los prompts y embeddings de RAG visualmente y consumirlos vía API en el backend.",
            "code_snippet": """async function queryFlowise(data) {
  const response = await fetch("http://localhost:3000/api/v1/prediction/<chatflow-id>", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return await response.json();
}
"""
        }
    },
    {
        "id": "dify",
        "name": "Dify",
        "full_name": "langgenius/dify",
        "category": "IA & LLMs",
        "description": "Plataforma de desarrollo de aplicaciones LLM con orquestación visual, gestión de prompts y pipelines RAG de nivel empresarial.",
        "stars": 58900,
        "forks": 8400,
        "open_issues": 890,
        "last_updated": "2026-10-16T22:30:00Z",
        "license": "OLLv1",
        "language": "Python",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://dify.ai",
        "github_url": "https://github.com/langgenius/dify",
        "docs_url": "https://docs.dify.ai",
        "saas_alternative": "OpenAI Assistants / Coze",
        "estimated_monthly_saas_cost": 290,
        "tags": ["llmops", "rag", "ai-agents", "workflow", "enterprise"],
        "integration": {
            "title": "Integración de Agente Conversacional con Workflow API",
            "integration_type": "REST API",
            "stack_compatibility": ["TypeScript", "Python", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "App webhooks, completion streaming",
            "dependencies": ["requests"],
            "docs_link": "https://docs.dify.ai/features/advanced/api-access",
            "explanation": "Despliega agentes con RAG híbrido, memoria de contexto persistente y ejecución de herramientas seguras.",
            "code_snippet": """# Llamada a Dify Completion API
curl -X POST 'http://localhost/v1/chat-messages' \\
  --header 'Authorization: Bearer app-api-key' \\
  --header 'Content-Type: application/json' \\
  --data-raw '{
    "inputs": {},
    "query": "¿Qué stack recomiendas para un CRM inmobiliario B2B?",
    "response_mode": "streaming",
    "user": "consultor-no-country"
  }'
"""
        }
    },
    {
        "id": "litellm",
        "name": "LiteLLM",
        "full_name": "BerriAI/litellm",
        "category": "IA & LLMs",
        "description": "Proxy universal de LLMs que unifica 100+ proveedores (OpenAI, Bedrock, Anthropic, Ollama) con formato estándar y control de costos.",
        "stars": 24800,
        "forks": 2700,
        "open_issues": 310,
        "last_updated": "2026-10-16T16:00:00Z",
        "license": "MIT",
        "language": "Python",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://litellm.ai",
        "github_url": "https://github.com/BerriAI/litellm",
        "docs_url": "https://docs.litellm.ai",
        "saas_alternative": "Portkey / Helicone",
        "estimated_monthly_saas_cost": 150,
        "tags": ["llm-proxy", "cost-tracking", "openai-compatible", "load-balancing"],
        "integration": {
            "title": "Load balancing y fallback automático entre Ollama y OpenAI",
            "integration_type": "REST API",
            "stack_compatibility": ["Python", "FastAPI", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Presupuesto excedido, alertas de latencia",
            "dependencies": ["litellm"],
            "docs_link": "https://docs.litellm.ai/docs/proxy/quick_start",
            "explanation": "Evita vendor lock-in enrutando peticiones a modelos locales gratuitos y saltando a OpenAI solo si se requiere mayor capacidad.",
            "code_snippet": """from litellm import completion

response = completion(
    model="ollama/llama3",
    messages=[{"role": "user", "content": "Escribe un Dockerfile de producción"}],
    fallbacks=["gpt-4o-mini"]
)
print(response.choices[0].message.content)
"""
        }
    },
    {
        "id": "vllm",
        "name": "vLLM",
        "full_name": "vllm-project/vllm",
        "category": "IA & LLMs",
        "description": "Biblioteca de inferencia y servicio de LLMs con PagedAttention de altísimo rendimiento para GPU.",
        "stars": 37100,
        "forks": 5600,
        "open_issues": 750,
        "last_updated": "2026-10-16T19:30:00Z",
        "license": "Apache-2.0",
        "language": "Python",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://vllm.ai",
        "github_url": "https://github.com/vllm-project/vllm",
        "docs_url": "https://docs.vllm.ai",
        "saas_alternative": "Replicate / Together AI",
        "estimated_monthly_saas_cost": 450,
        "tags": ["llm-serving", "paged-attention", "gpu", "high-throughput", "inference"],
        "integration": {
            "title": "Despliegue de servidor OpenAI compatible de alto rendimiento",
            "integration_type": "CLI",
            "stack_compatibility": ["Linux", "Docker", "Python", "Kubernetes"],
            "difficulty": "Avanzado",
            "triggers_webhooks": "Métricas Prometheus de tokens/segundo",
            "dependencies": ["vllm"],
            "docs_link": "https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html",
            "explanation": "Sirve modelos con hasta 24x más throughput de tokens optimizando la memoria RAM de video con PagedAttention.",
            "code_snippet": """python3 -m vllm.entrypoints.openai.api_server \\
  --model mistralai/Mistral-7B-Instruct-v0.3 \\
  --port 8000 \\
  --gpu-memory-utilization 0.90
"""
        }
    },
    {
        "id": "langfuse",
        "name": "Langfuse",
        "full_name": "langfuse/langfuse",
        "category": "IA & LLMs",
        "description": "Plataforma de observabilidad, trazabilidad, analítica y evaluación para aplicaciones basadas en LLMs.",
        "stars": 9800,
        "forks": 890,
        "open_issues": 110,
        "last_updated": "2026-10-16T12:00:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://langfuse.com",
        "github_url": "https://github.com/langfuse/langfuse",
        "docs_url": "https://langfuse.com/docs",
        "saas_alternative": "LangSmith",
        "estimated_monthly_saas_cost": 180,
        "tags": ["llmops", "observability", "tracing", "evals", "analytics"],
        "integration": {
            "title": "Monitoreo de latencia, costos y calidad de respuestas de RAG",
            "integration_type": "SDK",
            "stack_compatibility": ["TypeScript", "Python", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Alertas de coste por usuario",
            "dependencies": ["langfuse"],
            "docs_link": "https://langfuse.com/docs/get-started",
            "explanation": "Registra el costo de cada token, latencia del modelo y puntuaciones de satisfacción del cliente en producción.",
            "code_snippet": """from langfuse import Langfuse
langfuse = Langfuse()

trace = langfuse.trace(name="recomendacion-arquitectura", user_id="cliente-123")
generation = trace.generation(
    name="consulta-rag",
    model="llama-3.2",
    input="Recomiéndame un stack",
    output="Keycloak + Supabase"
)
"""
        }
    },

    # ----------------- 5. PAGOS, FACTURACIÓN Y E-COMMERCE B2B -----------------
    {
        "id": "medusajs",
        "name": "Medusa",
        "full_name": "medusajs/medusa",
        "category": "Pagos & E-Commerce",
        "description": "Motor de comercio electrónico headless y modular en Node.js, alternativa open source a Shopify y commercetools.",
        "stars": 28400,
        "forks": 3200,
        "open_issues": 240,
        "last_updated": "2026-10-16T14:40:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://medusajs.com",
        "github_url": "https://github.com/medusajs/medusa",
        "docs_url": "https://docs.medusajs.com",
        "saas_alternative": "Shopify Plus / commercetools",
        "estimated_monthly_saas_cost": 500,
        "tags": ["ecommerce", "headless", "b2b", "pricing", "inventory", "nodejs"],
        "integration": {
            "title": "Configuración de catálogos B2B con listas de precios personalizadas",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Next.js", "PostgreSQL", "Redis"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "order.placed, payment.captured, customer.created",
            "dependencies": ["@medusajs/medusa", "@medusajs/js-sdk"],
            "docs_link": "https://docs.medusajs.com/resources/b2b",
            "explanation": "Permite asignar diferentes tarifas por volumen y acuerdos comerciales a distintas empresas clientes en una sola tienda.",
            "code_snippet": """import Medusa from "@medusajs/js-sdk";

const medusa = new Medusa({ baseUrl: "http://localhost:9000", maxRetries: 3 });

const { order } = await medusa.admin.orders.create({
  email: "compras@distribuidora.com",
  items: [{ variant_id: "var_repuesto_99", quantity: 50 }],
  billing_address: { company: "Distribuidora Nacional S.A." }
});
"""
        }
    },
    {
        "id": "lago",
        "name": "Lago",
        "full_name": "getlago/lago",
        "category": "Pagos & E-Commerce",
        "description": "Infraestructura open-source de facturación recurrente, medición de consumo y suscripciones para empresas de software B2B.",
        "stars": 6900,
        "forks": 540,
        "open_issues": 85,
        "last_updated": "2026-10-15T18:00:00Z",
        "license": "AGPL-3.0",
        "language": "Ruby",
        "health_score": 93,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.getlago.com",
        "github_url": "https://github.com/getlago/lago",
        "docs_url": "https://docs.getlago.com",
        "saas_alternative": "Stripe Billing / Chargebee",
        "estimated_monthly_saas_cost": 350,
        "tags": ["billing", "metering", "subscriptions", "invoicing", "fintech"],
        "integration": {
            "title": "Envío de eventos de consumo (Usage-based metering) para facturación automática",
            "integration_type": "REST API",
            "stack_compatibility": ["Python", "Node.js", "Go", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "invoice.created, invoice.paid, customer.payment_failure",
            "dependencies": ["lago-javascript-client"],
            "docs_link": "https://docs.getlago.com/guide/events/ingestion",
            "explanation": "Registra el uso de API, gigabytes transferidos o transacciones de tus clientes B2B para generar facturas consolidadas a fin de mes.",
            "code_snippet": """import { Client } from "lago-javascript-client";

const lago = Client("LAGO_API_KEY", { baseUrl: "http://localhost:3000/api/v1" });

await lago.events.createEvent({
  event: {
    transaction_id: "tx_" + Date.now(),
    external_customer_id: "org_acme_corp",
    code: "api_requests_meter",
    timestamp: Math.floor(Date.now() / 1000),
    properties: { units: 1500 }
  }
});
"""
        }
    },
    {
        "id": "saleor",
        "name": "Saleor",
        "full_name": "saleor/saleor",
        "category": "Pagos & E-Commerce",
        "description": "Plataforma de comercio headless basada en GraphQL y construida sobre Python, Django y PostgreSQL.",
        "stars": 20400,
        "forks": 5100,
        "open_issues": 480,
        "last_updated": "2026-10-16T11:00:00Z",
        "license": "BSD-3-Clause",
        "language": "Python",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://saleor.io",
        "github_url": "https://github.com/saleor/saleor",
        "docs_url": "https://docs.saleor.io",
        "saas_alternative": "Shopify / BigCommerce",
        "estimated_monthly_saas_cost": 400,
        "tags": ["ecommerce", "graphql", "python", "django", "headless"],
        "integration": {
            "title": "Gestión de órdenes multi-moneda vía GraphQL",
            "integration_type": "GraphQL",
            "stack_compatibility": ["Python", "Next.js", "React"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "ORDER_CREATED, FULFILLMENT_CREATED",
            "dependencies": ["urllib", "requests"],
            "docs_link": "https://docs.saleor.io/developer/api-reference",
            "explanation": "Permite orquestar ventas internacionales con reglas impositivas dinámicas y pagos en múltiples divisas.",
            "code_snippet": """mutation CrearCheckout {
  checkoutCreate(
    input: {
      channel: "b2b-latam"
      lines: [{ quantity: 10, variantId: "UHJvZHVjdFZhcmlhbnQ6Mzk5" }]
      email: "proveedor@empresa.com"
    }
  ) {
    checkout { id totalPrice { gross { amount currency } } }
    errors { field message }
  }
}
"""
        }
    },
    {
        "id": "killbill",
        "name": "Kill Bill",
        "full_name": "killbill/killbill",
        "category": "Pagos & E-Commerce",
        "description": "Plataforma open source de facturación y gestión de pagos para empresas de escala global.",
        "stars": 4900,
        "forks": 1400,
        "open_issues": 190,
        "last_updated": "2026-10-14T09:00:00Z",
        "license": "Apache-2.0",
        "language": "Java",
        "health_score": 88,
        "maintenance_level": "Activo",
        "active_maintainer": True,
        "website_url": "https://killbill.io",
        "github_url": "https://github.com/killbill/killbill",
        "docs_url": "https://docs.killbill.io",
        "saas_alternative": "Zuora",
        "estimated_monthly_saas_cost": 800,
        "tags": ["billing", "payments", "enterprise", "invoicing", "subscriptions"],
        "integration": {
            "title": "Integración con pasarelas de pago y generación de facturas",
            "integration_type": "REST API",
            "stack_compatibility": ["Java", "Docker", "Python"],
            "difficulty": "Avanzado",
            "triggers_webhooks": "INVOICE_NOTIFICATION, PAYMENT_SUCCESS",
            "dependencies": ["killbill-client"],
            "docs_link": "https://docs.killbill.io/latest/userguide_payment.html",
            "explanation": "Maneja contabilidad compleja, notas de crédito, amortizaciones y pasarelas de pago heterogéneas.",
            "code_snippet": """curl -v -u admin:password \\
  -H "X-Killbill-ApiKey: bob" \\
  -H "X-Killbill-ApiSecret: lazar" \\
  -H "Content-Type: application/json" \\
  -X POST 'http://localhost:8080/1.0/kb/accounts' \\
  -d '{"name": "Corporación Global S.A.", "currency": "USD"}'
"""
        }
    },

    # ----------------- 6. ANALÍTICA Y MÉTRICAS DE PRODUCTO -----------------
    {
        "id": "posthog",
        "name": "PostHog",
        "full_name": "PostHog/posthog",
        "category": "Analítica",
        "description": "Plataforma integral de analítica de producto con feature flags, session recording, encuestas y tests A/B.",
        "stars": 24900,
        "forks": 1900,
        "open_issues": 580,
        "last_updated": "2026-10-16T21:40:00Z",
        "license": "MIT",
        "language": "Python",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://posthog.com",
        "github_url": "https://github.com/PostHog/posthog",
        "docs_url": "https://posthog.com/docs",
        "saas_alternative": "Mixpanel / Amplitude / LaunchDarkly",
        "estimated_monthly_saas_cost": 300,
        "tags": ["analytics", "session-replay", "feature-flags", "product-analytics", "ab-testing"],
        "integration": {
            "title": "Tracking de eventos con Group Analytics para cuentas B2B",
            "integration_type": "SDK",
            "stack_compatibility": ["React", "Next.js", "Python", "Node.js"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Webhook de alertas sobre caída de conversión",
            "dependencies": ["posthog-js"],
            "docs_link": "https://posthog.com/docs/libraries/next-js",
            "explanation": "Permite segmentar métricas por cliente corporativo (Group Analytics) para ver qué empresas usan más tu plataforma.",
            "code_snippet": """import posthog from "posthog-js";

posthog.init("API_KEY_POSTHOG", { api_host: "https://mi-posthog.empresa.com" });

posthog.identify("usr_789", { email: "gerente@b2bclient.com" });
posthog.group("company", "org_acme_corp", {
  plan: "Enterprise",
  empleados: 250
});
posthog.capture("exporto_reporte_mensual", { formato: "PDF" });
"""
        }
    },
    {
        "id": "plausible",
        "name": "Plausible Analytics",
        "full_name": "plausible/analytics",
        "category": "Analítica",
        "description": "Analítica web ligera, open-source y respetuosa de la privacidad (100% compatible con RGPD sin banners de cookies).",
        "stars": 20400,
        "forks": 1200,
        "open_issues": 140,
        "last_updated": "2026-10-15T10:15:00Z",
        "license": "AGPL-3.0",
        "language": "Elixir",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://plausible.io",
        "github_url": "https://github.com/plausible/analytics",
        "docs_url": "https://plausible.io/docs",
        "saas_alternative": "Google Analytics",
        "estimated_monthly_saas_cost": 60,
        "tags": ["web-analytics", "privacy", "gdpr", "elixir", "lightweight"],
        "integration": {
            "title": "Script de analítica liviano (<1KB) sin cookies",
            "integration_type": "SDK",
            "stack_compatibility": ["HTML", "Next.js", "Astro", "Vue"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Weekly digest email",
            "dependencies": ["script tag"],
            "docs_link": "https://plausible.io/docs/quickstart",
            "explanation": "Mide visitas y conversiones sin ralentizar la carga ni requerir consentimientos legales molestos.",
            "code_snippet": """<script defer data-domain="portal.miempresa.com" src="https://plausible.midominio.com/js/script.tagged-events.js"></script>

<script>
  window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) };
  plausible('LeadGenerado', { props: { origen: 'Landing Consultoría' } });
</script>
"""
        }
    },
    {
        "id": "umami",
        "name": "Umami",
        "full_name": "umami-software/umami",
        "category": "Analítica",
        "description": "Alternativa de analítica web self-hosted sencilla, rápida y respetuosa de la privacidad construida en Node.js.",
        "stars": 24200,
        "forks": 3900,
        "open_issues": 160,
        "last_updated": "2026-10-16T13:00:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://umami.is",
        "github_url": "https://github.com/umami-software/umami",
        "docs_url": "https://umami.is/docs",
        "saas_alternative": "Fathom / Google Analytics",
        "estimated_monthly_saas_cost": 50,
        "tags": ["analytics", "nextjs", "privacy", "open-source", "mysql", "postgres"],
        "integration": {
            "title": "Despliegue en Docker y tracking de eventos custom",
            "integration_type": "Docker",
            "stack_compatibility": ["Docker", "PostgreSQL", "Next.js"],
            "difficulty": "Fácil",
            "triggers_webhooks": "API REST de métricas",
            "dependencies": ["docker-compose"],
            "docs_link": "https://umami.is/docs/install",
            "explanation": "Despliegue autónomo con base de datos propia para métricas de tráfico y embudos de ventas.",
            "code_snippet": """import Script from 'next/script';

export function Analytics() {
  return (
    <Script
      defer
      src="https://stats.tu-empresa.com/script.js"
      data-website-id="7d7e98bf-92b4-4b53-979f-d31e91be1a14"
    />
  );
}
"""
        }
    },

    # ----------------- 7. CMS Y GESTIÓN DE CONTENIDOS -----------------
    {
        "id": "strapi",
        "name": "Strapi",
        "full_name": "strapi/strapi",
        "category": "CMS & Contenido",
        "description": "Headless CMS open source líder en Node.js, totalmente extensible y con API REST y GraphQL autogeneradas.",
        "stars": 65100,
        "forks": 8400,
        "open_issues": 740,
        "last_updated": "2026-10-16T16:50:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://strapi.io",
        "github_url": "https://github.com/strapi/strapi",
        "docs_url": "https://docs.strapi.io",
        "saas_alternative": "Contentful / Sanity",
        "estimated_monthly_saas_cost": 300,
        "tags": ["cms", "headless", "nodejs", "rest-api", "graphql", "customizable"],
        "integration": {
            "title": "Webhooks de auto-regeneración de catálogo estático (ISR)",
            "integration_type": "Webhook",
            "stack_compatibility": ["Next.js", "Node.js", "Docker", "PostgreSQL"],
            "difficulty": "Fácil",
            "triggers_webhooks": "entry.create, entry.update, entry.publish",
            "dependencies": ["@strapi/strapi"],
            "docs_link": "https://docs.strapi.io/user-docs/settings/webhooks",
            "explanation": "Dispara revalidación on-demand en Next.js cada vez que el equipo editorial actualiza especificaciones o artículos.",
            "code_snippet": """import { revalidateTag } from "next/cache";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const secret = request.headers.get("x-strapi-signature");
  if (secret !== process.env.STRAPI_WEBHOOK_SECRET) {
    return NextResponse.json({ error: "No autorizado" }, { status: 401 });
  }
  revalidateTag("catalogo-productos");
  return NextResponse.json({ revalidated: true, now: Date.now() });
}
"""
        }
    },
    {
        "id": "directus",
        "name": "Directus",
        "full_name": "directus/directus",
        "category": "CMS & Contenido",
        "description": "Capa de API REST y GraphQL instantánea sobre cualquier base de datos SQL con back-office modular e intuitivo.",
        "stars": 30200,
        "forks": 3800,
        "open_issues": 480,
        "last_updated": "2026-10-16T18:30:00Z",
        "license": "BSL 1.1",
        "language": "TypeScript",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://directus.io",
        "github_url": "https://github.com/directus/directus",
        "docs_url": "https://docs.directus.io",
        "saas_alternative": "Airtable / Contentful",
        "estimated_monthly_saas_cost": 250,
        "tags": ["headless-cms", "database-gui", "rest-api", "graphql", "sql"],
        "integration": {
            "title": "Conexión SDK tipado a tablas existentes en PostgreSQL",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Vue", "React", "TypeScript"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Flows automáticos con triggers de eventos",
            "dependencies": ["@directus/sdk"],
            "docs_link": "https://docs.directus.io/guides/sdk/getting-started.html",
            "explanation": "No altera tu base de datos ni impone esquemas propios: se monta directamente encima de tus tablas SQL existentes.",
            "code_snippet": """import { createDirectus, rest, readItems } from "@directus/sdk";

const client = createDirectus("http://localhost:8055").with(rest());
const proyectos = await client.request(
  readItems("proyectos", {
    filter: { estado: { _eq: "en_progreso" } },
    fields: ["id", "titulo", "cliente.nombre"]
  })
);
"""
        }
    },
    {
        "id": "payload",
        "name": "Payload CMS",
        "full_name": "payloadcms/payload",
        "category": "CMS & Contenido",
        "description": "Headless CMS TypeScript nativo para Next.js con renderizado en el servidor y control total de código.",
        "stars": 28900,
        "forks": 1800,
        "open_issues": 210,
        "last_updated": "2026-10-16T22:00:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 98,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://payloadcms.com",
        "github_url": "https://github.com/payloadcms/payload",
        "docs_url": "https://payloadcms.com/docs",
        "saas_alternative": "Sanity / Contentful",
        "estimated_monthly_saas_cost": 220,
        "tags": ["cms", "nextjs", "typescript", "react", "mongodb", "postgres"],
        "integration": {
            "title": "Ejecución embebida dentro de la carpeta /app de Next.js",
            "integration_type": "SDK",
            "stack_compatibility": ["Next.js", "React", "TypeScript", "PostgreSQL"],
            "difficulty": "Fácil",
            "triggers_webhooks": "afterChange hooks en colecciones",
            "dependencies": ["payload", "@payloadcms/db-postgres"],
            "docs_link": "https://payloadcms.com/docs/getting-started/installation",
            "explanation": "Funciona en el mismo proceso de Next.js sin servidores separados, compartiendo TypeScript types automáticamente.",
            "code_snippet": """import { buildConfig } from "payload/config";
import { postgresAdapter } from "@payloadcms/db-postgres";

export default buildConfig({
  db: postgresAdapter({ pool: { connectionString: process.env.DATABASE_URI } }),
  collections: [
    {
      slug: "articulos_tecnicos",
      fields: [{ name: "titulo", type: "text", required: true }]
    }
  ]
});
"""
        }
    },

    # ----------------- 8. MENSAJERÍA, STREAMING Y COLAS -----------------
    {
        "id": "rabbitmq",
        "name": "RabbitMQ",
        "full_name": "rabbitmq/rabbitmq-server",
        "category": "Mensajería & Colas",
        "description": "Message broker open-source ampliamente implementado con soporte de AMQP, MQTT y STOMP.",
        "stars": 12100,
        "forks": 3900,
        "open_issues": 130,
        "last_updated": "2026-10-15T15:00:00Z",
        "license": "MPL-2.0",
        "language": "Erlang",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.rabbitmq.com",
        "github_url": "https://github.com/rabbitmq/rabbitmq-server",
        "docs_url": "https://www.rabbitmq.com/documentation.html",
        "saas_alternative": "AWS SQS / CloudAMQP",
        "estimated_monthly_saas_cost": 150,
        "tags": ["message-broker", "queues", "amqp", "microservices", "async"],
        "integration": {
            "title": "Procesamiento en segundo plano de tareas pesadas (Generación PDF / Facturas)",
            "integration_type": "Docker",
            "stack_compatibility": ["Python", "Node.js", "Go", "Docker"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Consumers sobre colas durables",
            "dependencies": ["amqplib", "pika"],
            "docs_link": "https://www.rabbitmq.com/tutorials/tutorial-one-python.html",
            "explanation": "Desacopla requests HTTP lentos de la ejecución de procesos intensivos garantizando entregas at-least-once.",
            "code_snippet": """import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='cola_facturas', durable=True)

channel.basic_publish(
    exchange='',
    routing_key='cola_facturas',
    body=json.dumps({"pedido_id": 9845, "email": "contabilidad@empresa.com"}),
    properties=pika.BasicProperties(delivery_mode=2)
)
connection.close()
"""
        }
    },
    {
        "id": "kafka",
        "name": "Apache Kafka",
        "full_name": "apache/kafka",
        "category": "Mensajería & Colas",
        "description": "Plataforma distribuida de streaming de eventos para transmisión de datos en tiempo real de alto rendimiento.",
        "stars": 29400,
        "forks": 14200,
        "open_issues": 1200,
        "last_updated": "2026-10-16T19:00:00Z",
        "license": "Apache-2.0",
        "language": "Java",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://kafka.apache.org",
        "github_url": "https://github.com/apache/kafka",
        "docs_url": "https://kafka.apache.org/documentation/",
        "saas_alternative": "Confluent Cloud / AWS Kinesis",
        "estimated_monthly_saas_cost": 600,
        "tags": ["streaming", "events", "distributed", "big-data", "pubsub"],
        "integration": {
            "title": "Pipeline de telemetría y eventos de clickstream en tiempo real",
            "integration_type": "SDK",
            "stack_compatibility": ["Java", "Python", "Go", "Node.js"],
            "difficulty": "Avanzado",
            "triggers_webhooks": "Consumer groups con offset tracking",
            "dependencies": ["kafkajs", "confluent-kafka"],
            "docs_link": "https://kafka.apache.org/quickstart",
            "explanation": "Ideal para empresas que manejan millones de eventos por segundo (IoT, tracking de flotas, auditoría financiera).",
            "code_snippet": """import { Kafka } from "kafkajs";

const kafka = new Kafka({ clientId: "b2b-tracker", brokers: ["localhost:9092"] });
const producer = kafka.producer();

await producer.connect();
await producer.send({
  topic: "telemetria-logistica",
  messages: [{ key: "camion_42", value: JSON.stringify({ lat: -34.60, lon: -58.38, temp: 4.2 }) }]
});
"""
        }
    },
    {
        "id": "bullmq",
        "name": "BullMQ",
        "full_name": "taskforcesh/bullmq",
        "category": "Mensajería & Colas",
        "description": "Gestor de colas y trabajos en segundo plano ultra-rápido para Node.js basado en Redis con soporte de reintentos y cron.",
        "stars": 8200,
        "forks": 650,
        "open_issues": 90,
        "last_updated": "2026-10-16T17:00:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://bullmq.io",
        "github_url": "https://github.com/taskforcesh/bullmq",
        "docs_url": "https://docs.bullmq.io",
        "saas_alternative": "AWS SQS + Lambda / Inngest",
        "estimated_monthly_saas_cost": 110,
        "tags": ["redis", "queues", "jobs", "cron", "nodejs", "typescript"],
        "integration": {
            "title": "Cola de reintentos con backoff exponencial para sincronización con GitHub API",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "TypeScript", "Redis"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Worker progress & completion events",
            "dependencies": ["bullmq", "ioredis"],
            "docs_link": "https://docs.bullmq.io/guide/jobs/backoff-strategies",
            "explanation": "Ejecuta trabajos recurrentes o encolados con control de concurrencia y reintentos automáticos si la API externa falla.",
            "code_snippet": """import { Queue, Worker } from "bullmq";

const queue = new Queue("sync-github-metrics", { connection: { host: "localhost", port: 6379 } });

await queue.add("sync_repo", { repo: "supabase/supabase" }, {
  attempts: 5,
  backoff: { type: "exponential", delay: 2000 }
});

const worker = new Worker("sync-github-metrics", async (job) => {
  console.log("Sincronizando:", job.data.repo);
}, { connection: { host: "localhost", port: 6379 } });
"""
        }
    },
    {
        "id": "nats",
        "name": "NATS",
        "full_name": "nats-io/nats-server",
        "category": "Mensajería & Colas",
        "description": "Sistema de mensajería seguro, ligero y de ultra-alto rendimiento para microservicios y Edge computing.",
        "stars": 16400,
        "forks": 1500,
        "open_issues": 110,
        "last_updated": "2026-10-15T22:00:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://nats.io",
        "github_url": "https://github.com/nats-io/nats-server",
        "docs_url": "https://docs.nats.io",
        "saas_alternative": "Google Cloud Pub/Sub",
        "estimated_monthly_saas_cost": 180,
        "tags": ["messaging", "pubsub", "microservices", "jetstream", "edge", "golang"],
        "integration": {
            "title": "Comunicación RPC y Event-Driven entre microservicios con JetStream",
            "integration_type": "SDK",
            "stack_compatibility": ["Go", "Node.js", "Python", "Rust"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "NATS JetStream persistent consumers",
            "dependencies": ["nats"],
            "docs_link": "https://docs.nats.io/nats-concepts/jetstream",
            "explanation": "Procesa millones de mensajes por segundo con latencia inferior a 1 milisegundo en binario ultra liviano.",
            "code_snippet": """import { connect, StringCodec } from "nats";

const nc = await connect({ servers: "localhost:4222" });
const sc = StringCodec();

const sub = nc.subscribe("pedidos.b2b.*");
(async () => {
  for await (const m of sub) {
    console.log(`[${m.subject}]: ${sc.decode(m.data)}`);
  }
})();
"""
        }
    },

    # ----------------- 9. AUTOMATIZACIÓN Y WORKFLOWS -----------------
    {
        "id": "n8n",
        "name": "n8n",
        "full_name": "n8n-io/n8n",
        "category": "Automatización",
        "description": "Plataforma de automatización de flujos de trabajo con interfaz visual, conectores para 400+ servicios y soporte nativo de IA.",
        "stars": 54200,
        "forks": 8900,
        "open_issues": 410,
        "last_updated": "2026-10-16T21:10:00Z",
        "license": "Sustainable Use License",
        "language": "TypeScript",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://n8n.io",
        "github_url": "https://github.com/n8n-io/n8n",
        "docs_url": "https://docs.n8n.io",
        "saas_alternative": "Zapier / Make (Integromat)",
        "estimated_monthly_saas_cost": 300,
        "tags": ["workflow", "automation", "integration", "low-code", "ai-agent"],
        "integration": {
            "title": "Webhook trigger para sincronizar leads hacia HubSpot / Base de datos",
            "integration_type": "Webhook",
            "stack_compatibility": ["Docker", "REST API", "JavaScript", "Python"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Webhook nodes y Cron triggers programados",
            "dependencies": ["docker-compose"],
            "docs_link": "https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook",
            "explanation": "Permite crear flujos complejos entre CRM, Slack, correo y bases de datos sin escribir código de integración repetitivo.",
            "code_snippet": """services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=n8n.tu-empresa.com
      - WEBHOOK_URL=https://n8n.tu-empresa.com/
    volumes:
      - ./n8n_data:/home/node/.n8n
"""
        }
    },
    {
        "id": "temporal",
        "name": "Temporal",
        "full_name": "temporalio/temporal",
        "category": "Automatización",
        "description": "Plataforma de orquestación de código abierto para flujos de trabajo distribuidos e irrompibles (Durable Execution).",
        "stars": 12800,
        "forks": 1100,
        "open_issues": 180,
        "last_updated": "2026-10-16T17:40:00Z",
        "license": "MIT",
        "language": "Go",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://temporal.io",
        "github_url": "https://github.com/temporalio/temporal",
        "docs_url": "https://docs.temporal.io",
        "saas_alternative": "AWS Step Functions",
        "estimated_monthly_saas_cost": 400,
        "tags": ["orchestration", "workflow-engine", "durable-execution", "distributed-systems"],
        "integration": {
            "title": "Flujo de cobro y onboarding con tolerancia a caídas de red",
            "integration_type": "SDK",
            "stack_compatibility": ["TypeScript", "Python", "Go", "Java"],
            "difficulty": "Avanzado",
            "triggers_webhooks": "Signals y Queries en Workflows",
            "dependencies": ["@temporalio/workflow", "@temporalio/activity"],
            "docs_link": "https://docs.temporal.io/develop/typescript/core-application",
            "explanation": "Garantiza que flujos que tardan días o semanas (ej. cobro B2B con espera de transferencia) se ejecuten sin perder estado.",
            "code_snippet": """import { proxyActivities, sleep } from "@temporalio/workflow";
import type * as activities from "./activities";

const { cobrarFactura, notificarCliente } = proxyActivities<typeof activities>({
  startToCloseTimeout: "1 minute",
});

export async function onboardingClienteWorkflow(clienteId: string): Promise<void> {
  await cobrarFactura(clienteId);
  await sleep("3 days");
  await notificarCliente(clienteId, "Bienvenido a su período de producción");
}
"""
        }
    },
    {
        "id": "airbyte",
        "name": "Airbyte",
        "full_name": "airbytehq/airbyte",
        "category": "Automatización",
        "description": "Plataforma líder open-source de integración y movimiento de datos (ELT) con 350+ conectores prediseñados.",
        "stars": 16900,
        "forks": 3800,
        "open_issues": 620,
        "last_updated": "2026-10-16T18:20:00Z",
        "license": "ELv2",
        "language": "Java",
        "health_score": 93,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://airbyte.com",
        "github_url": "https://github.com/airbytehq/airbyte",
        "docs_url": "https://docs.airbyte.com",
        "saas_alternative": "Fivetran",
        "estimated_monthly_saas_cost": 750,
        "tags": ["elt", "data-pipelines", "connectors", "data-warehouse", "analytics"],
        "integration": {
            "title": "Sincronización automatizada de GitHub API y Stripe hacia PostgreSQL",
            "integration_type": "Docker",
            "stack_compatibility": ["Docker", "PostgreSQL", "Snowflake", "BigQuery"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Sync start / success / failure notifications",
            "dependencies": ["docker", "abctl"],
            "docs_link": "https://docs.airbyte.com/quickstart/deploy-airbyte",
            "explanation": "Replica datos de APIs externas a tu data warehouse de forma incremental y programada sin programar scripts manuales.",
            "code_snippet": """curl -sS https://airbyte.com/quickstart.sh | bash
# Abre la interfaz en http://localhost:8000 para configurar conectores
"""
        }
    },
    {
        "id": "triggerdotdev",
        "name": "Trigger.dev",
        "full_name": "triggerdotdev/trigger.dev",
        "category": "Automatización",
        "description": "Framework para background jobs y flujos de larga duración en TypeScript sin límites de timeout serverless.",
        "stars": 11500,
        "forks": 820,
        "open_issues": 115,
        "last_updated": "2026-10-16T15:10:00Z",
        "license": "Apache-2.0",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://trigger.dev",
        "github_url": "https://github.com/triggerdotdev/trigger.dev",
        "docs_url": "https://trigger.dev/docs",
        "saas_alternative": "Inngest / Quirrel",
        "estimated_monthly_saas_cost": 120,
        "tags": ["background-jobs", "nextjs", "typescript", "serverless", "cron"],
        "integration": {
            "title": "Ejecución de tareas pesadas en Next.js sin timeout",
            "integration_type": "SDK",
            "stack_compatibility": ["Next.js", "Node.js", "TypeScript"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Realtime task run streaming",
            "dependencies": ["@trigger.dev/sdk"],
            "docs_link": "https://trigger.dev/docs/documentation/guides/using-with-nextjs",
            "explanation": "Ejecuta indexaciones de IA o scraping de repositorios de 30 minutos desde endpoints serverless de Vercel/Next.js.",
            "code_snippet": """import { task } from "@trigger.dev/sdk/v3";

export const procesarRepositorio = task({
  id: "procesar-repositorio",
  run: async (payload: { repoUrl: string }) => {
    const data = await descargarYAnalizarCodigo(payload.repoUrl);
    return { status: "completado", data };
  },
});
"""
        }
    },

    # ----------------- 10. MONITOREO Y OBSERVABILIDAD -----------------
    {
        "id": "grafana",
        "name": "Grafana",
        "full_name": "grafana/grafana",
        "category": "Monitoreo & Logs",
        "description": "Plataforma líder para visualización de métricas, dashboards interactivos y alertas operacionales.",
        "stars": 63400,
        "forks": 12100,
        "open_issues": 4100,
        "last_updated": "2026-10-16T20:00:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://grafana.com",
        "github_url": "https://github.com/grafana/grafana",
        "docs_url": "https://grafana.com/docs",
        "saas_alternative": "Datadog",
        "estimated_monthly_saas_cost": 450,
        "tags": ["metrics", "dashboards", "monitoring", "observability", "alerting"],
        "integration": {
            "title": "Dashboards de salud de infraestructura y negocio en tiempo real",
            "integration_type": "Docker",
            "stack_compatibility": ["Docker", "Prometheus", "Loki", "PostgreSQL"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Alerting webhooks a Slack / Discord / PagerDuty",
            "dependencies": ["grafana-image"],
            "docs_link": "https://grafana.com/docs/grafana/latest/getting-started",
            "explanation": "Permite monitorear el SLA de clientes B2B, uso de CPU, tasa de errores HTTP y KPIs comerciales.",
            "code_snippet": """docker run -d -p 3000:3000 --name=grafana grafana/grafana-oss
"""
        }
    },
    {
        "id": "prometheus",
        "name": "Prometheus",
        "full_name": "prometheus/prometheus",
        "category": "Monitoreo & Logs",
        "description": "Sistema de monitoreo y base de datos de series temporales de código abierto con lenguaje PromQL.",
        "stars": 56200,
        "forks": 9300,
        "open_issues": 850,
        "last_updated": "2026-10-16T16:20:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://prometheus.io",
        "github_url": "https://github.com/prometheus/prometheus",
        "docs_url": "https://prometheus.io/docs",
        "saas_alternative": "Datadog / New Relic",
        "estimated_monthly_saas_cost": 350,
        "tags": ["time-series", "metrics", "promql", "alertmanager", "monitoring"],
        "integration": {
            "title": "Scraping de métricas de FastAPI y Node.js con /metrics endpoint",
            "integration_type": "REST API",
            "stack_compatibility": ["Go", "Python", "Node.js", "Docker"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Alertmanager webhooks",
            "dependencies": ["prometheus_client"],
            "docs_link": "https://prometheus.io/docs/prometheus/latest/getting_started",
            "explanation": "Recolecta métricas de latencia de endpoints, conteo de requests y memoria de los contenedores cada 15 segundos.",
            "code_snippet": """from prometheus_client import start_http_server, Counter

PETICIONES_RAG = Counter('rag_queries_total', 'Total de consultas al asistente RAG')

def atender_consulta():
    PETICIONES_RAG.inc()

start_http_server(8001)
"""
        }
    },
    {
        "id": "uptime-kuma",
        "name": "Uptime Kuma",
        "full_name": "louislam/uptime-kuma",
        "category": "Monitoreo & Logs",
        "description": "Herramienta de monitoreo de disponibilidad autohospedada, moderna y elegante con página de estado pública.",
        "stars": 64200,
        "forks": 5800,
        "open_issues": 320,
        "last_updated": "2026-10-16T22:45:00Z",
        "license": "MIT",
        "language": "JavaScript",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://uptime.kuma.pet",
        "github_url": "https://github.com/louislam/uptime-kuma",
        "docs_url": "https://github.com/louislam/uptime-kuma/wiki",
        "saas_alternative": "Better Uptime / Statuspage / Pingdom",
        "estimated_monthly_saas_cost": 120,
        "tags": ["uptime", "status-page", "monitoring", "ping", "alerts"],
        "integration": {
            "title": "Página de estado pública para clientes B2B con alertas Telegram / Slack",
            "integration_type": "Docker",
            "stack_compatibility": ["Docker", "Node.js", "HTTP"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Notificaciones instantáneas si un servicio se cae",
            "dependencies": ["docker"],
            "docs_link": "https://github.com/louislam/uptime-kuma#--how-to-use",
            "explanation": "Monitorea HTTP(s), TCP, DNS, ping y certificados SSL de los microservicios con reporte visual de SLA.",
            "code_snippet": """docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
"""
        }
    },
    {
        "id": "signoz",
        "name": "SigNoz",
        "full_name": "SigNoz/signoz",
        "category": "Monitoreo & Logs",
        "description": "Plataforma integral de APM open-source basada en OpenTelemetry y ClickHouse para traces, métricas y logs.",
        "stars": 19500,
        "forks": 1400,
        "open_issues": 310,
        "last_updated": "2026-10-16T14:00:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://signoz.io",
        "github_url": "https://github.com/SigNoz/signoz",
        "docs_url": "https://signoz.io/docs",
        "saas_alternative": "DataDog APM / Dynatrace",
        "estimated_monthly_saas_cost": 500,
        "tags": ["opentelemetry", "apm", "tracing", "clickhouse", "logs"],
        "integration": {
            "title": "Instrumentación de OpenTelemetry en microservicios",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Python", "Go", "Java"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Alertas de anomalías en latencia P99",
            "dependencies": ["@opentelemetry/sdk-node"],
            "docs_link": "https://signoz.io/docs/instrumentation/overview",
            "explanation": "Rastrea cuellos de botella exactos en llamadas entre microservicios y consultas lentas de base de datos.",
            "code_snippet": """import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: "http://localhost:4318/v1/traces" }),
});
sdk.start();
"""
        }
    },

    # ----------------- 11. ALMACENAMIENTO DE OBJETOS Y ARCHIVOS -----------------
    {
        "id": "minio",
        "name": "MinIO",
        "full_name": "minio/minio",
        "category": "Almacenamiento",
        "description": "Almacenamiento de objetos de alto rendimiento 100% compatible con la API de Amazon S3.",
        "stars": 46800,
        "forks": 5400,
        "open_issues": 210,
        "last_updated": "2026-10-16T19:30:00Z",
        "license": "AGPL-3.0",
        "language": "Go",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://min.io",
        "github_url": "https://github.com/minio/minio",
        "docs_url": "https://min.io/docs/minio/linux/index.html",
        "saas_alternative": "AWS S3 / Google Cloud Storage",
        "estimated_monthly_saas_cost": 150,
        "tags": ["s3-compatible", "storage", "cloud-storage", "object-storage", "golang"],
        "integration": {
            "title": "URLs prefirmadas para subida directa de archivos pesados desde el cliente",
            "integration_type": "SDK",
            "stack_compatibility": ["Node.js", "Python", "Go", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Eventos de subida de archivos (s3:ObjectCreated:*)",
            "dependencies": ["@aws-sdk/client-s3", "@aws-sdk/s3-request-presigner"],
            "docs_link": "https://min.io/docs/minio/linux/developers/javascript/minio-javascript.html",
            "explanation": "Permite que el navegador suba facturas o imágenes directamente al bucket sin sobrecargar los servidores de API.",
            "code_snippet": """import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({
  endpoint: "http://localhost:9000",
  region: "us-east-1",
  credentials: { accessKeyId: "MINIO_ROOT_USER", secretAccessKey: "MINIO_ROOT_PASSWORD" },
  forcePathStyle: true,
});

export async function getUploadUrl(filename: string) {
  const command = new PutObjectCommand({ Bucket: "archivos-b2b", Key: filename });
  return await getSignedUrl(s3, command, { expiresIn: 3600 });
}
"""
        }
    },
    {
        "id": "seaweedfs",
        "name": "SeaweedFS",
        "full_name": "seaweedfs/seaweedfs",
        "category": "Almacenamiento",
        "description": "Sistema de archivos distribuido rápido y escalable para miles de millones de archivos pequeños y streaming.",
        "stars": 22400,
        "forks": 2400,
        "open_issues": 190,
        "last_updated": "2026-10-15T16:00:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 93,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://github.com/seaweedfs/seaweedfs",
        "github_url": "https://github.com/seaweedfs/seaweedfs",
        "docs_url": "https://github.com/seaweedfs/seaweedfs/wiki",
        "saas_alternative": "AWS S3 + CloudFront",
        "estimated_monthly_saas_cost": 200,
        "tags": ["distributed-filesystem", "storage", "s3-api", "golang"],
        "integration": {
            "title": "Almacenamiento ultra-optimizado con compatibilidad S3 y POSIX",
            "integration_type": "Docker",
            "stack_compatibility": ["Go", "Docker", "S3 Clients"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "File notifications",
            "dependencies": ["docker"],
            "docs_link": "https://github.com/seaweedfs/seaweedfs/wiki/Getting-Started",
            "explanation": "Optimizado para latencia ultrabaja en almacenamiento de fotos de productos, thumbnails y adjuntos.",
            "code_snippet": """docker run -p 8333:8333 -p 9333:9333 chrislusf/seaweedfs server -s3
"""
        }
    },

    # ----------------- 12. INFRAESTRUCTURA, DEPLOY Y DEVOPS -----------------
    {
        "id": "coolify",
        "name": "Coolify",
        "full_name": "coollabsio/coolify",
        "category": "DevOps & Deploy",
        "description": "Alternativa autohospedada 'all-in-one' a Heroku, Netlify y Vercel para desplegar apps, bases de datos y servicios.",
        "stars": 39800,
        "forks": 2200,
        "open_issues": 280,
        "last_updated": "2026-10-16T23:20:00Z",
        "license": "Apache-2.0",
        "language": "PHP",
        "health_score": 98,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://coolify.io",
        "github_url": "https://github.com/coollabsio/coolify",
        "docs_url": "https://coolify.io/docs",
        "saas_alternative": "Heroku / Vercel Pro / Render",
        "estimated_monthly_saas_cost": 250,
        "tags": ["paas", "self-hosted", "docker", "deploy", "vercel-alternative"],
        "integration": {
            "title": "Despliegue automatizado con Git Push y certificados SSL automáticos",
            "integration_type": "CLI",
            "stack_compatibility": ["Git", "Docker", "Next.js", "Python", "Node.js"],
            "difficulty": "Fácil",
            "triggers_webhooks": "GitHub/GitLab push webhooks para CI/CD automático",
            "dependencies": ["curl", "docker"],
            "docs_link": "https://coolify.io/docs/installation",
            "explanation": "Permite a la consultora alojar múltiples proyectos de clientes en servidores VPS económicos con SSL gratuito de Let's Encrypt.",
            "code_snippet": """curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
"""
        }
    },
    {
        "id": "traefik",
        "name": "Traefik",
        "full_name": "traefik/traefik",
        "category": "DevOps & Deploy",
        "description": "Edge router y reverse proxy nativo de la nube que configura automáticamente rutas y certificados SSL.",
        "stars": 52100,
        "forks": 5100,
        "open_issues": 490,
        "last_updated": "2026-10-16T18:00:00Z",
        "license": "MIT",
        "language": "Go",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://traefik.io",
        "github_url": "https://github.com/traefik/traefik",
        "docs_url": "https://doc.traefik.io/traefik/",
        "saas_alternative": "Cloudflare Enterprise / AWS ALB",
        "estimated_monthly_saas_cost": 180,
        "tags": ["reverse-proxy", "ssl", "load-balancer", "docker", "kubernetes"],
        "integration": {
            "title": "Enrutamiento dinámico de microservicios con etiquetas Docker",
            "integration_type": "Docker",
            "stack_compatibility": ["Docker", "Kubernetes", "Linux"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Access logs en formato JSON",
            "dependencies": ["docker-compose"],
            "docs_link": "https://doc.traefik.io/traefik/providers/docker/",
            "explanation": "Detecta automáticamente nuevos contenedores y les asigna subdominio con HTTPS sin reiniciar el servidor proxy.",
            "code_snippet": """labels:
  - "traefik.enable=true"
  - "traefik.http.routers.api.rule=Host(`api.miempresa.com`)"
  - "traefik.http.routers.api.entrypoints=websecure"
  - "traefik.http.routers.api.tls.certresolver=myresolver"
"""
        }
    },
    {
        "id": "caddy",
        "name": "Caddy Server",
        "full_name": "caddyserver/caddy",
        "category": "DevOps & Deploy",
        "description": "Servidor web potente y extensible para empresas con HTTPS automático por defecto.",
        "stars": 59800,
        "forks": 4200,
        "open_issues": 210,
        "last_updated": "2026-10-16T17:15:00Z",
        "license": "Apache-2.0",
        "language": "Go",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://caddyserver.com",
        "github_url": "https://github.com/caddyserver/caddy",
        "docs_url": "https://caddyserver.com/docs/",
        "saas_alternative": "Nginx Plus / Cloudflare SSL",
        "estimated_monthly_saas_cost": 80,
        "tags": ["web-server", "automatic-https", "reverse-proxy", "http3", "golang"],
        "integration": {
            "title": "Reverse proxy con HTTPS automático y compresión gzip/zstd",
            "integration_type": "CLI",
            "stack_compatibility": ["Linux", "Docker", "Go"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Config reload API vía REST",
            "dependencies": ["caddy"],
            "docs_link": "https://caddyserver.com/docs/quick-starts/reverse-proxy",
            "explanation": "Configura un proxy inverso seguro en solo 3 líneas de Caddyfile obteniendo certificados SSL automáticamente.",
            "code_snippet": """api.cliente.com {
    reverse_proxy localhost:8000
    encode zstd gzip
}
"""
        }
    },

    # ----------------- 13. NOTIFICACIONES Y COMUNICACIÓN -----------------
    {
        "id": "novu",
        "name": "Novu",
        "full_name": "novuhq/novu",
        "category": "Notificaciones",
        "description": "Infraestructura open-source de notificaciones para desarrolladores (In-App, Email, SMS, Push, Chat).",
        "stars": 36100,
        "forks": 3400,
        "open_issues": 310,
        "last_updated": "2026-10-16T21:00:00Z",
        "license": "MIT",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://novu.co",
        "github_url": "https://github.com/novuhq/novu",
        "docs_url": "https://docs.novu.co",
        "saas_alternative": "Courier / Knock / OneSignal",
        "estimated_monthly_saas_cost": 220,
        "tags": ["notifications", "email", "sms", "in-app-inbox", "push", "typescript"],
        "integration": {
            "title": "Inbox de notificaciones dentro de la app React y despacho multicanal",
            "integration_type": "SDK",
            "stack_compatibility": ["React", "Next.js", "Node.js", "Python"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Webhook de entrega y clicks en notificaciones",
            "dependencies": ["@novu/node", "@novu/notification-center"],
            "docs_link": "https://docs.novu.co/overview/quickstart",
            "explanation": "Centraliza el envío de emails transaccionales, mensajes SMS y la campana de notificaciones in-app con un solo trigger.",
            "code_snippet": """import { Novu } from "@novu/node";

const novu = new Novu(process.env.NOVU_API_KEY);

await novu.trigger("pedido-confirmado", {
  to: { subscriberId: "usr_456", email: "compras@cliente.com" },
  payload: { pedidoId: "PED-9821", total: "$1,250.00 USD" }
});
"""
        }
    },
    {
        "id": "chatwoot",
        "name": "Chatwoot",
        "full_name": "chatwoot/chatwoot",
        "category": "Notificaciones",
        "description": "Plataforma de soporte y comunicación con clientes omnicanal (Live chat, WhatsApp, Email, Telegram).",
        "stars": 21800,
        "forks": 3900,
        "open_issues": 410,
        "last_updated": "2026-10-16T18:10:00Z",
        "license": "MIT",
        "language": "Ruby",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://www.chatwoot.com",
        "github_url": "https://github.com/chatwoot/chatwoot",
        "docs_url": "https://www.chatwoot.com/docs",
        "saas_alternative": "Intercom / Zendesk",
        "estimated_monthly_saas_cost": 350,
        "tags": ["live-chat", "customer-support", "whatsapp", "inbox", "crm"],
        "integration": {
            "title": "Incrustación del widget de chat con identificación de clientes B2B",
            "integration_type": "SDK",
            "stack_compatibility": ["JavaScript", "React", "Vue", "Docker"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Webhooks en message_created y conversation_resolved",
            "dependencies": ["chatwoot-widget"],
            "docs_link": "https://www.chatwoot.com/docs/product/channels/live-chat/sdk/setup",
            "explanation": "Brinda atención y soporte técnico a las empresas clientes desde un panel unificado sin pagar licencias por agente.",
            "code_snippet": """window.chatwootSettings = { hideMessageBubble: false, position: 'right' };
(function(d,t) {
  var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
  g.src="https://chat.tu-empresa.com/packs/js/sdk.js";
  s.parentNode.insertBefore(g,s);
  g.onload=function(){
    window.chatwootSDK.run({ websiteToken: 'TOKEN_EMPRESA', baseUrl: 'https://chat.tu-empresa.com' });
  }
})(document,"script");
"""
        }
    },

    # ----------------- 14. DOCUMENTOS, FIRMA DIGITAL Y PRODUCTIVIDAD B2B -----------------
    {
        "id": "documenso",
        "name": "Documenso",
        "full_name": "documenso/documenso",
        "category": "Documentos & Firma",
        "description": "Infraestructura open-source de firma digital de contratos y documentos, alternativa a DocuSign.",
        "stars": 9800,
        "forks": 1200,
        "open_issues": 130,
        "last_updated": "2026-10-16T19:20:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://documenso.com",
        "github_url": "https://github.com/documenso/documenso",
        "docs_url": "https://documenso.com/docs",
        "saas_alternative": "DocuSign / PandaDoc",
        "estimated_monthly_saas_cost": 280,
        "tags": ["e-signature", "contracts", "pdf", "security", "b2b-contracts"],
        "integration": {
            "title": "Envío automatizado de contratos comerciales para firma electrónica",
            "integration_type": "REST API",
            "stack_compatibility": ["Node.js", "Python", "Next.js"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "DOCUMENT_SIGNED, DOCUMENT_REJECTED",
            "dependencies": ["@documenso/sdk"],
            "docs_link": "https://documenso.com/docs/developers/api",
            "explanation": "Genera acuerdos de confidencialidad o contratos de servicios y recibe la confirmación con sello criptográfico.",
            "code_snippet": """import { Documenso } from "@documenso/sdk";

const documenso = new Documenso({ apiKey: process.env.DOCUMENSO_API_KEY });

const documento = await documenso.documents.create({
  title: "Contrato de Prestación de Servicios B2B",
  recipients: [{ name: "Representante Legal", email: "legal@cliente.com", role: "SIGNER" }]
});
"""
        }
    },
    {
        "id": "calcom",
        "name": "Cal.com",
        "full_name": "calcom/cal.com",
        "category": "Productividad & CRM",
        "description": "Infraestructura de agendamiento y reserva de citas de código abierto con soporte de calendarios múltiples.",
        "stars": 33100,
        "forks": 8400,
        "open_issues": 590,
        "last_updated": "2026-10-16T21:40:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://cal.com",
        "github_url": "https://github.com/calcom/cal.com",
        "docs_url": "https://cal.com/docs",
        "saas_alternative": "Calendly",
        "estimated_monthly_saas_cost": 150,
        "tags": ["scheduling", "calendar", "meetings", "nextjs", "booking"],
        "integration": {
            "title": "Incrustación de agenda comercial con sincronización Google Calendar / Outlook",
            "integration_type": "SDK",
            "stack_compatibility": ["React", "Next.js", "TypeScript"],
            "difficulty": "Fácil",
            "triggers_webhooks": "BOOKING_CREATED, BOOKING_RESCHEDULED",
            "dependencies": ["@calcom/embed-react"],
            "docs_link": "https://cal.com/docs/core-features/embeddings/react",
            "explanation": "Permite a los prospectos agendar demostraciones técnicas directamente desde el portal web.",
            "code_snippet": """import Cal, { getCalApi } from "@calcom/embed-react";
import { useEffect } from "react";

export function AgendarDemo() {
  useEffect(() => {
    (async function () {
      const cal = await getCalApi();
      cal("ui", { theme: "dark", hideEventTypeDetails: false });
    })();
  }, []);

  return <Cal calLink="tech-consultancy/demo-arquitectura" style={{ width: "100%", height: "100%" }} />;
}
"""
        }
    },
    {
        "id": "twenty",
        "name": "Twenty CRM",
        "full_name": "twentyhq/twenty",
        "category": "Productividad & CRM",
        "description": "CRM open-source moderno, intuitivo y modular, construido como alternativa directa a Salesforce y HubSpot.",
        "stars": 24100,
        "forks": 2500,
        "open_issues": 210,
        "last_updated": "2026-10-16T22:15:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 97,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://twenty.com",
        "github_url": "https://github.com/twentyhq/twenty",
        "docs_url": "https://docs.twenty.com",
        "saas_alternative": "HubSpot Sales / Salesforce",
        "estimated_monthly_saas_cost": 400,
        "tags": ["crm", "sales", "leads", "graphql", "b2b-sales"],
        "integration": {
            "title": "Creación automática de oportunidades y sincronización de contactos vía GraphQL",
            "integration_type": "GraphQL",
            "stack_compatibility": ["TypeScript", "Node.js", "Python"],
            "difficulty": "Intermedio",
            "triggers_webhooks": "Opportunity stage changed, Contact created",
            "dependencies": ["graphql-request"],
            "docs_link": "https://docs.twenty.com/developers/graphql-api",
            "explanation": "Maneja el pipeline de ventas de los proyectos de consultoría con visibilidad de deals y etapas de negociación.",
            "code_snippet": """mutation CrearOportunidad {
  createOpportunity(
    data: {
      name: "Proyecto Desarrollo E-Commerce B2B"
      amount: { amountMicros: 35000000000, currencyCode: "USD" }
      stage: "PROPOSAL"
    }
  ) {
    id
    name
  }
}
"""
        }
    },
    {
        "id": "formbricks",
        "name": "Formbricks",
        "full_name": "formbricks/formbricks",
        "category": "Productividad & CRM",
        "description": "Suite open-source de encuestas y feedback en el producto para medir NPS y satisfacción de clientes.",
        "stars": 9400,
        "forks": 1100,
        "open_issues": 140,
        "last_updated": "2026-10-16T14:30:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 95,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://formbricks.com",
        "github_url": "https://github.com/formbricks/formbricks",
        "docs_url": "https://formbricks.com/docs",
        "saas_alternative": "Typeform / Qualtrics",
        "estimated_monthly_saas_cost": 130,
        "tags": ["surveys", "feedback", "nps", "nextjs", "analytics"],
        "integration": {
            "title": "Encuestas in-app segmentadas por tenant",
            "integration_type": "SDK",
            "stack_compatibility": ["React", "Next.js", "JavaScript"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Response submitted webhook",
            "dependencies": ["@formbricks/js"],
            "docs_link": "https://formbricks.com/docs/getting-started/framework-guides/nextjs",
            "explanation": "Pregunta a los clientes B2B su nivel de satisfacción justo después de cerrar un pedido o transacción crítica.",
            "code_snippet": """import formbricks from "@formbricks/js";

formbricks.init({
  environmentId: "clqxxxxxx",
  apiHost: "https://feedback.miempresa.com",
  userId: "usr_554",
});

formbricks.track("pedido_completado");
"""
        }
    },
    {
        "id": "typebot",
        "name": "Typebot",
        "full_name": "baptisteArno/typebot.io",
        "category": "Productividad & CRM",
        "description": "Creador visual de formularios conversacionales y chatbots interactivos con soporte de WhatsApp y web.",
        "stars": 18200,
        "forks": 4100,
        "open_issues": 210,
        "last_updated": "2026-10-15T19:00:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 94,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://typebot.io",
        "github_url": "https://github.com/baptisteArno/typebot.io",
        "docs_url": "https://docs.typebot.io",
        "saas_alternative": "Landbot / Typeform",
        "estimated_monthly_saas_cost": 110,
        "tags": ["chatbot", "conversational-forms", "lead-capture", "whatsapp"],
        "integration": {
            "title": "Burbuja de onboarding y cotización interactiva",
            "integration_type": "SDK",
            "stack_compatibility": ["React", "HTML", "Next.js"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Webhook de captura de lead calificado",
            "dependencies": ["@typebot.io/react"],
            "docs_link": "https://docs.typebot.io/editor/blocks/integrations/webhook",
            "explanation": "Guía a prospectos a través de un cuestionario dinámico que calcula el costo estimado de su proyecto.",
            "code_snippet": """import { Standard } from "@typebot.io/react";

export function Cotizador() {
  return (
    <Standard
      typebot="cotizador-b2b-v1"
      style={{ width: "100%", height: "600px" }}
    />
  );
}
"""
        }
    },
    {
        "id": "dub",
        "name": "Dub",
        "full_name": "dubinc/dub",
        "category": "Productividad & CRM",
        "description": "Infraestructura open-source de acortamiento de enlaces, analítica de clics y gestión de links para empresas.",
        "stars": 19100,
        "forks": 2400,
        "open_issues": 120,
        "last_updated": "2026-10-16T17:50:00Z",
        "license": "AGPL-3.0",
        "language": "TypeScript",
        "health_score": 96,
        "maintenance_level": "Excelente",
        "active_maintainer": True,
        "website_url": "https://dub.co",
        "github_url": "https://github.com/dubinc/dub",
        "docs_url": "https://dub.co/docs",
        "saas_alternative": "Bitly Enterprise",
        "estimated_monthly_saas_cost": 150,
        "tags": ["link-management", "shortlinks", "analytics", "nextjs", "qr-codes"],
        "integration": {
            "title": "Generación programática de enlaces rastreables para cotizaciones y catálogos",
            "integration_type": "REST API",
            "stack_compatibility": ["TypeScript", "Node.js", "Python"],
            "difficulty": "Fácil",
            "triggers_webhooks": "Link clicked webhook with geolocation",
            "dependencies": ["dub"],
            "docs_link": "https://dub.co/docs/api-reference/introduction",
            "explanation": "Permite saber con precisión qué cliente abrió la propuesta comercial, desde qué país y qué dispositivo.",
            "code_snippet": """import { Dub } from "dub";

const dub = new Dub({ token: process.env.DUB_API_KEY });
const link = await dub.links.create({
  url: "https://portal.empresa.com/propuesta/982",
  domain: "link.miempresa.com",
  key: "propuesta-acme"
});
console.log("Enlace corto:", link.shortLink);
"""
        }
    }
]

EXTENDED_CATALOG_DATA = [
    ("redis", "Redis", "redis/redis", "Base de Datos", "Estructura de datos en memoria para caché, colas y pub/sub ultrarrápido.", 68000, 24000, 750, "BSD-3-Clause", "C", "Upstash / AWS ElastiCache", 140, ["cache", "in-memory", "pubsub", "fast"]),
    ("clickhouse", "ClickHouse", "ClickHouse/ClickHouse", "Base de Datos", "Sistema de gestión de base de datos columnar orientado a analítica OLAP en tiempo real.", 39000, 7100, 1100, "Apache-2.0", "C++", "Snowflake / Google BigQuery", 600, ["olap", "columnar", "big-data", "sql"]),
    ("pgvector", "pgvector", "pgvector/pgvector", "Base de Datos", "Extensión open source para PostgreSQL para búsqueda de similitud de embeddings vectoriales.", 18900, 950, 45, "PostgreSQL", "C", "Pinecone", 160, ["vector", "postgres", "ai", "similarity"]),
    ("surrealdb", "SurrealDB", "surrealdb/surrealdb", "Base de Datos", "Base de datos multi-modelo que combina SQL, Documentos, Grafos y Realtime.", 28400, 1100, 480, "BSL-1.1", "Rust", "Neo4j / DynamoDB", 220, ["multimodel", "graph", "sql", "realtime"]),
    ("milvus", "Milvus", "milvus-io/milvus", "Búsqueda", "Base de datos vectorial diseñada para gestionar billones de embeddings para IA a escala masiva.", 31500, 3100, 680, "Apache-2.0", "Go", "Pinecone Enterprise", 450, ["vector-database", "milvus", "scale", "similarity"]),
    ("weaviate", "Weaviate", "weaviate/weaviate", "Búsqueda", "Base de datos vectorial open-source con soporte de búsqueda híbrida y generación RAG.", 12400, 950, 210, "BSD-3-Clause", "Go", "Pinecone", 200, ["vector-search", "hybrid-search", "rag"]),
    ("zincsearch", "ZincSearch", "zincsearch/zincsearch", "Búsqueda", "Motor de búsqueda full-text ligero en Go como reemplazo moderno de Elasticsearch.", 17800, 890, 85, "Apache-2.0", "Go", "Elasticsearch Cloud", 180, ["search", "lightweight", "go", "indexing"]),
    ("sonic", "Sonic", "valeriansaliou/sonic", "Búsqueda", "Backend de búsqueda rápido y ligero que consume apenas unos pocos megabytes de memoria.", 20100, 720, 40, "MPL-2.0", "Rust", "Algolia", 120, ["search", "rust", "low-memory", "fast"]),
    ("localai", "LocalAI", "mudler/LocalAI", "IA & LLMs", "Reemplazo local directo de las APIs de OpenAI sin necesidad de tarjeta GPU costosa.", 26500, 2100, 310, "MIT", "Go", "OpenAI", 280, ["local-ai", "openai-dropin", "cpu-inference"]),
    ("open-webui", "Open WebUI", "open-webui/open-webui", "IA & LLMs", "Interfaz web extensible y auto-hospedada para interactuar con Ollama y APIs de LLM.", 67200, 8200, 420, "MIT", "Python", "ChatGPT Plus Enterprise", 250, ["ui", "ollama", "chatgpt-clone", "rag"]),
    ("anything-llm", "AnythingLLM", "Mintplex-Labs/anything-llm", "IA & LLMs", "Plataforma todo-en-uno de RAG corporativo con gestión de documentos y multi-usuario.", 31000, 3300, 190, "MIT", "JavaScript", "Custom RAG", 220, ["rag-app", "enterprise", "documents", "chat"]),
    ("text-generation-webui", "Text Generation WebUI", "oobabooga/text-generation-webui", "IA & LLMs", "Interfaz Gradio avanzada para ejecutar cualquier modelo de lenguaje de código abierto.", 39800, 5200, 390, "AGPL-3.0", "Python", "RunPod Hosted", 180, ["gradio", "llm-runner", "transformers"]),
    ("haystack", "Haystack", "deepset-ai/haystack", "IA & LLMs", "Framework orquestador de pipelines de IA para búsqueda neuronal y RAG a escala.", 17100, 1800, 140, "Apache-2.0", "Python", "Enterprise Search AI", 240, ["rag", "search", "pipelines", "nlp"]),
    ("instructor", "Instructor", "jxnl/instructor", "IA & LLMs", "Librería para extraer salidas estructuradas y tipadas (Pydantic) de modelos de lenguaje.", 9200, 680, 50, "MIT", "Python", "OpenAI Structured Outputs", 100, ["structured-data", "pydantic", "validation"]),
    ("solidus", "Solidus", "solidusio/solidus", "Pagos & E-Commerce", "Plataforma de e-commerce flexible y probada en Ruby on Rails para transacciones complejas.", 5100, 1600, 130, "BSD-3-Clause", "Ruby", "Shopify Plus", 400, ["rails", "storefront", "b2b"]),
    ("vendure", "Vendure", "vendure-ecommerce/vendure", "Pagos & E-Commerce", "Framework de comercio headless moderno en TypeScript con GraphQL y NestJS.", 5900, 890, 80, "MIT", "TypeScript", "commercetools", 350, ["graphql", "nestjs", "headless-commerce"]),
    ("invoiceninja", "Invoice Ninja", "invoiceninja/invoiceninja", "Pagos & E-Commerce", "Herramienta completa de facturación, presupuestos y cobros para empresas y consultoras.", 8400, 2400, 310, "Elastic-2.0", "PHP", "FreshBooks / QuickBooks", 180, ["invoicing", "billing", "payments", "quotes"]),
    ("matomo", "Matomo", "matomo-org/matomo", "Analítica", "Plataforma de analítica web número 1 autohospedada para control de privacidad 100%.", 20400, 2900, 840, "GPL-3.0", "PHP", "Google Analytics 360", 400, ["analytics", "privacy", "gdpr", "enterprise"]),
    ("openpanel", "OpenPanel", "OpenPanel-dev/openpanel", "Analítica", "Alternativa moderna y ligera a Mixpanel para análisis de producto y embudos.", 4900, 280, 45, "Apache-2.0", "TypeScript", "Mixpanel", 180, ["product-analytics", "funnels", "lightweight"]),
    ("shynet", "Shynet", "milesmcc/shynet", "Analítica", "Analítica sin cookies ni JS invasivo para sitios y portales corporativos.", 4100, 220, 35, "Apache-2.0", "Python", "Simple Analytics", 90, ["cookieless", "privacy", "lightweight"]),
    ("ghost", "Ghost", "TryGhost/Ghost", "CMS & Contenido", "Plataforma profesional de publicación de contenido y newsletters con membresías.", 47800, 10200, 240, "MIT", "JavaScript", "Substack / Medium", 190, ["publishing", "blog", "newsletters", "memberships"]),
    ("decap-cms", "Decap CMS", "decaporg/decap-cms", "CMS & Contenido", "CMS basado en Git para flujos Jamstack estáticos con cero base de datos.", 17500, 2200, 320, "MIT", "TypeScript", "Netlify CMS", 80, ["git-based", "jamstack", "static-site"]),
    ("keystone", "KeystoneJS", "keystonejs/keystone", "CMS & Contenido", "Framework para backend GraphQL escalable con panel de administración React.", 8600, 750, 140, "MIT", "TypeScript", "Contentful", 200, ["graphql", "headless", "typescript"]),
    ("dragonfly", "Dragonfly", "dragonflydb/dragonfly", "Mensajería & Colas", "Drop-in replacement moderno para Redis con arquitectura multi-hilo 25x más rápida.", 26800, 1100, 180, "BSL-1.1", "C++", "AWS ElastiCache Cluster", 350, ["cache", "multithreaded", "redis-compatible"]),
    ("pulsar", "Apache Pulsar", "apache/pulsar", "Mensajería & Colas", "Sistema de mensajería pub-sub multi-tenant distribuido con arquitectura desacoplada.", 14500, 3500, 680, "Apache-2.0", "Java", "Confluent Cloud", 500, ["pubsub", "multitenant", "streaming"]),
    ("kestra", "Kestra", "kestra-io/kestra", "Automatización", "Plataforma de orquestación declarativa en código y YAML para pipelines de datos y microservicios.", 12400, 1100, 120, "Apache-2.0", "Java", "Airflow / Prefect Cloud", 250, ["data-orchestration", "yaml", "workflows"]),
    ("windmill", "Windmill", "windmill-labs/windmill", "Automatización", "Alternativa open source a Retool y Temporal para scripts en TypeScript y Python.", 13800, 890, 95, "AGPL-3.0", "Rust", "Retool / Airplane", 320, ["internal-tools", "scripts", "workflows", "rust"]),
    ("activepieces", "Activepieces", "activepieces/activepieces", "Automatización", "Automatización de flujos con interfaz intuitiva y conector nativo de ChatGPT y Claude.", 10800, 1300, 140, "MIT", "TypeScript", "Zapier", 190, ["automation", "zapier-alternative", "typescript"]),
    ("netdata", "Netdata", "netdata/netdata", "Monitoreo & Logs", "Monitoreo de infraestructura y métricas de servidor en tiempo real con resolución por segundo.", 71500, 5800, 290, "GPL-3.0", "C", "Datadog Server Agent", 180, ["real-time", "system-metrics", "fast"]),
    ("victoria-metrics", "VictoriaMetrics", "VictoriaMetrics/VictoriaMetrics", "Monitoreo & Logs", "Base de datos de series temporales rápida y costo-eficiente compatible con Prometheus.", 13200, 1200, 80, "Apache-2.0", "Go", "Datadog Metrics", 220, ["time-series", "prometheus-dropin", "efficiency"]),
    ("jaeger", "Jaeger", "jaegertracing/jaeger", "Monitoreo & Logs", "Trazabilidad distribuida de transacciones de microservicios según estándares CNCF.", 19800, 2400, 280, "Apache-2.0", "Go", "AWS X-Ray", 210, ["tracing", "distributed", "cncf", "apm"]),
    ("opentofu", "OpenTofu", "opentofu/opentofu", "DevOps & Deploy", "Bifurcación comunitaria y open-source de Terraform bajo la Linux Foundation.", 24800, 980, 140, "MPL-2.0", "Go", "Terraform Cloud", 200, ["iac", "infrastructure-as-code", "cloud"]),
    ("portainer", "Portainer", "portainer/portainer", "DevOps & Deploy", "Interfaz gráfica para gestionar Docker, Swarm y Kubernetes de forma simple y segura.", 32100, 2600, 510, "zlib", "Go", "Docker Desktop Enterprise", 150, ["docker-ui", "containers", "management"]),
    ("caprover", "CapRover", "caprover/caprover", "DevOps & Deploy", "Plataforma PaaS autohospedada ultra sencilla para apps Node, Python, PHP y Docker.", 14200, 1100, 120, "Apache-2.0", "TypeScript", "Heroku", 120, ["paas", "easy-deploy", "docker"]),
    ("dokku", "Dokku", "dokku/dokku", "DevOps & Deploy", "El PaaS autohospedado más pequeño del mundo propulsado por Docker y Git push.", 26500, 1900, 180, "MIT", "Shell", "Heroku", 110, ["paas", "git-push", "minimalist"]),
    ("matrix-synapse", "Synapse", "element-hq/synapse", "Notificaciones", "Servidor de referencia para el protocolo abierto Matrix de mensajería descentralizada y cifrada.", 13400, 2800, 890, "AGPL-3.0", "Python", "Slack Enterprise", 350, ["matrix", "chat", "encrypted", "decentralized"]),
    ("mattermost", "Mattermost", "mattermost/mattermost", "Notificaciones", "Plataforma segura de colaboración y mensajería en equipo para empresas técnicas.", 30200, 7400, 680, "AGPL-3.0", "Go", "Slack Enterprise Grid", 420, ["chat", "collaboration", "enterprise", "devops"]),
    ("rocket-chat", "Rocket.Chat", "RocketChat/Rocket.Chat", "Notificaciones", "Plataforma de comunicación de código abierto para empresas con cumplimiento estricto de datos.", 39400, 8900, 1400, "MIT", "TypeScript", "Slack", 380, ["chat", "omnichannel", "compliance"]),
    ("plane", "Plane", "makeplane/plane", "Productividad & CRM", "Herramienta open source moderna de gestión de proyectos y desarrollo ágil.", 31500, 2200, 310, "AGPL-3.0", "TypeScript", "Linear / Jira", 250, ["project-management", "linear-alternative", "agile"]),
    ("focalboard", "Focalboard", "mattermost/focalboard", "Productividad & CRM", "Alternativa de código abierto a Notion, Trello y Asana para equipos técnicos.", 21200, 1700, 290, "AGPL-3.0", "TypeScript", "Notion / Trello", 120, ["kanban", "boards", "notion-alternative"]),
    ("appsmith", "Appsmith", "appsmithorg/appsmith", "Automatización", "Plataforma low-code para construir paneles de control, dashboards y herramientas internas de negocio.", 35400, 4100, 480, "Apache-2.0", "Java", "Retool", 300, ["internal-tools", "low-code", "admin-panel"]),
    ("tooljet", "ToolJet", "ToolJet/ToolJet", "Automatización", "Framework low-code extensible para crear herramientas de negocio conectadas a bases de datos.", 31200, 4300, 320, "AGPL-3.0", "JavaScript", "Retool", 280, ["low-code", "internal-tools", "builder"]),
    ("budibase", "Budibase", "Budibase/budibase", "Automatización", "Constructor visual de aplicaciones internas y portales de clientes con base de datos propia.", 23100, 1800, 190, "GPL-3.0", "TypeScript", "Retool / Quickbase", 240, ["internal-apps", "portals", "forms"]),
    ("glitchtip", "GlitchTip", "glitchtip/glitchtip", "Monitoreo & Logs", "Alternativa simple, open-source y ligera a Sentry para seguimiento de errores de software.", 5400, 310, 85, "MIT", "Python", "Sentry SaaS", 160, ["error-tracking", "sentry-compatible", "python"]),
    ("vaultwarden", "Vaultwarden", "dani-garcia/vaultwarden", "Autenticación", "Servidor ligero y eficiente compatible con las aplicaciones y extensiones de Bitwarden.", 38500, 2100, 95, "AGPL-3.0", "Rust", "1Password Teams", 180, ["password-manager", "security", "rust"]),
    ("authelia", "Authelia", "authelia/authelia", "Autenticación", "Portal de autenticación y autorización 2FA / SSO para proteger servicios web en proxies inversos.", 21900, 1100, 160, "Apache-2.0", "Go", "Duo Security / Okta", 200, ["sso", "2fa", "security", "reverse-proxy-auth"]),
    ("casdoor", "Casdoor", "casdoor/casdoor", "Autenticación", "Plataforma UI de gestión de acceso e identidad con soporte de OAuth 2.0, OIDC y CAS.", 10200, 1400, 190, "Apache-2.0", "Go", "Auth0", 220, ["iam", "sso", "oauth2", "oidc"]),
    ("kratos", "Ory Hydra", "ory/hydra", "Autenticación", "Servidor OIDC y OAuth 2.0 certificado por OpenID Foundation para arquitecturas headless.", 15200, 1600, 120, "Apache-2.0", "Go", "Ping Identity", 290, ["oauth2", "oidc", "security", "identity"]),
    ("ory-keto", "Ory Keto", "ory/keto", "Autenticación", "Servidor de control de acceso y permisos basado en la especificación Google Zanzibar.", 5100, 480, 80, "Apache-2.0", "Go", "Auth0 Fine-Grained Authorization", 230, ["zanzibar", "rebac", "authorization", "permissions"]),
    ("openfga", "OpenFGA", "openfga/openfga", "Autenticación", "Motor de autorización granular (Fine-Grained Authorization) inspirado en Google Zanzibar.", 4800, 320, 50, "Apache-2.0", "Go", "Aserto / Auth0 FGA", 240, ["authorization", "rebac", "zanzibar", "security"]),
    ("metabase", "Metabase", "metabase/metabase", "Analítica", "La forma más simple y rápida para que cualquiera en la empresa genere gráficos y dashboards con SQL.", 41500, 5400, 1800, "AGPL-3.0", "Clojure", "Tableau / Looker", 500, ["bi", "dashboards", "business-intelligence", "sql"]),
    ("redash", "Redash", "getredash/redash", "Analítica", "Herramienta open-source para consultar, visualizar y compartir datos de múltiples fuentes SQL y NoSQL.", 25600, 4100, 620, "BSD-2-Clause", "Python", "Tableau", 300, ["data-visualization", "sql-editor", "dashboards"]),
    ("apache-superset", "Apache Superset", "apache/superset", "Analítica", "Plataforma moderna de exploración y visualización de datos de nivel empresarial.", 63000, 13100, 1900, "Apache-2.0", "Python", "PowerBI Enterprise", 650, ["bi", "enterprise-analytics", "dashboards", "sql"]),
    ("crawlee", "Crawlee", "apify/crawlee", "Automatización", "Librería de scraping web y automatización de navegadores para Node.js y Python.", 16800, 1100, 130, "Apache-2.0", "TypeScript", "Apify Cloud / BrightData", 150, ["scraping", "crawling", "headless-browser"]),
    ("playwright", "Playwright", "microsoft/playwright", "DevOps & Deploy", "Framework confiable para pruebas end-to-end y automatización de navegadores Chromium, Firefox y WebKit.", 68500, 4100, 1100, "Apache-2.0", "TypeScript", "BrowserStack", 200, ["e2e-testing", "automation", "browser"]),
    ("k6", "k6", "grafana/k6", "DevOps & Deploy", "Herramienta moderna de pruebas de carga y rendimiento de APIs escrita en Go con scripts en JavaScript.", 26100, 1300, 170, "AGPL-3.0", "Go", "LoadRunner / Gatling Cloud", 250, ["load-testing", "performance", "benchmarking"]),
    ("verdaccio", "Verdaccio", "verdaccio/verdaccio", "DevOps & Deploy", "Registro privado y ligero de paquetes npm con soporte de caché y autenticación corporativa.", 16700, 1900, 190, "MIT", "TypeScript", "Artifactory / Cloudsmith", 180, ["npm-registry", "private-packages", "caching"]),
    ("localstack", "LocalStack", "localstack/localstack", "DevOps & Deploy", "Emulador local completo de servicios de AWS en la nube (S3, SQS, Lambda, DynamoDB).", 56200, 4100, 390, "Apache-2.0", "Python", "AWS Test Environments", 200, ["aws-emulator", "testing", "cloud", "mock"]),
    ("wiremock", "WireMock", "wiremock/wiremock", "DevOps & Deploy", "Simulador flexible de APIs HTTP para pruebas de integración y desacoplamiento de dependencias externas.", 6200, 1500, 95, "Apache-2.0", "Java", "MockLab", 120, ["mocking", "api-testing", "integration"]),
    ("postman-newman", "Newman", "postmanlabs/newman", "DevOps & Deploy", "Ejecutor de colecciones de Postman por línea de comandos para pipelines de CI/CD.", 6900, 1100, 140, "Apache-2.0", "JavaScript", "Postman Enterprise Runner", 100, ["ci-cd", "api-tests", "postman"]),
    ("infisical", "Infisical", "Infisical/infisical", "Seguridad", "Plataforma open-source de gestión de secretos y variables de entorno de extremo a extremo.", 16100, 980, 110, "MIT", "TypeScript", "HashiCorp Vault / Doppler", 280, ["secrets-management", "env-vars", "security"]),
    ("vault", "HashiCorp Vault", "hashicorp/vault", "Seguridad", "Herramienta estándar de la industria para gestión de secretos, cifrado de datos y certificados.", 31200, 4200, 850, "BSL-1.1", "Go", "AWS Secrets Manager", 350, ["secrets", "encryption", "certificates", "pki"]),
    ("trivy", "Trivy", "aquasecurity/trivy", "Seguridad", "Escáner integral de vulnerabilidades para contenedores Docker, repositorios Git y configuraciones cloud.", 24800, 2300, 290, "Apache-2.0", "Go", "Snyk Enterprise", 320, ["vulnerability-scanner", "docker-security", "sbom"]),
    ("sonarqube", "SonarQube", "SonarSource/sonarqube", "Seguridad", "Plataforma de análisis estático continuo de calidad y seguridad de código fuente.", 10400, 2800, 390, "LGPL-3.0", "Java", "SonarCloud Enterprise", 350, ["code-quality", "security-audit", "static-analysis"]),
    ("certbot", "Certbot", "certbot/certbot", "Seguridad", "Herramienta oficial de EFF para obtención y renovación automatizada de certificados Let's Encrypt.", 31000, 3900, 180, "Apache-2.0", "Python", "Paid SSL Certificates", 80, ["ssl", "tls", "https", "certificates"]),
    ("mailpit", "Mailpit", "axllent/mailpit", "DevOps & Deploy", "Servidor de pruebas SMTP y visualizador web de correos electrónicos para desarrollo local.", 6900, 210, 25, "MIT", "Go", "Mailtrap", 90, ["smtp-testing", "emails", "fake-smtp"]),
    ("postal", "Postal", "postalserver/postal", "Notificaciones", "Servidor completo de entrega y recepción de correo electrónico transaccional autohospedado.", 16500, 2200, 280, "GPL-3.0", "Ruby", "SendGrid / Mailgun", 250, ["smtp", "transactional-email", "mail-server"]),
    ("listmonk", "Listmonk", "knadh/listmonk", "Notificaciones", "Gestor de boletines, newsletters y campañas de correo de ultra-alto rendimiento en Go.", 17400, 1400, 85, "AGPL-3.0", "Go", "Mailchimp", 200, ["newsletters", "email-marketing", "fast"]),
    ("nextcloud", "Nextcloud", "nextcloud/server", "Almacenamiento", "Plataforma de colaboración, sincronización de archivos y almacenamiento seguro en la nube propia.", 27800, 4200, 2900, "AGPL-3.0", "PHP", "Google Drive / Dropbox Business", 250, ["cloud-storage", "file-sync", "collaboration"]),
    ("filebrowser", "File Browser", "filebrowser/filebrowser", "Almacenamiento", "Interfaz web ligera y moderna para gestionar directorios y archivos en el servidor.", 26200, 3100, 190, "Apache-2.0", "Go", "Cloud File Managers", 60, ["file-manager", "web-ui", "lightweight"]),
    ("syncthing", "Syncthing", "syncthing/syncthing", "Almacenamiento", "Sincronización continua de archivos peer-to-peer cifrada y descentralizada.", 64500, 4300, 410, "MPL-2.0", "Go", "Resilio Sync", 100, ["p2p", "file-sync", "encrypted"]),
    ("questdb", "QuestDB", "questdb/questdb", "Base de Datos", "Base de datos SQL de series temporales de altísima velocidad para streaming financiero y telemetría.", 15300, 1100, 120, "Apache-2.0", "Java", "Kdb+ / InfluxCloud", 350, ["time-series", "high-throughput", "sql"]),
    ("duckdb", "DuckDB", "duckdb/duckdb", "Base de Datos", "Base de datos analítica columnar en proceso (in-process OLAP), el SQLite de los datos masivos.", 28900, 2100, 450, "MIT", "C++", "Snowflake Small Instances", 180, ["olap", "in-process", "fast-sql", "parquet"]),
    ("edgedb", "EdgeDB (Gel)", "edgedb/edgedb", "Base de Datos", "Base de datos relacional orientada a grafos construida sobre PostgreSQL con esquema declarativo.", 15200, 680, 210, "Apache-2.0", "Python", "FaunaDB", 170, ["graph-relational", "postgres-powered", "modern-db"]),
    ("ferretdb", "FerretDB", "FerretDB/FerretDB", "Base de Datos", "Reemplazo open source directo para MongoDB propulsado por PostgreSQL como motor subyacente.", 9600, 520, 95, "Apache-2.0", "Go", "MongoDB Atlas", 200, ["mongodb-compatible", "postgres", "nosql"]),
    ("meili-vector", "Marqo", "marqo-ai/marqo", "Búsqueda", "Motor de búsqueda vectorial y multimodal de extremo a extremo que procesa texto e imágenes.", 5400, 390, 80, "Apache-2.0", "Python", "Algolia Neural Search", 280, ["multimodal-search", "embeddings", "ai"]),
    ("fastapi", "FastAPI", "fastapi/fastapi", "DevOps & Deploy", "Framework web moderno y de alto rendimiento para construir APIs con Python y tipos estándar.", 78200, 6800, 910, "MIT", "Python", "AWS API Gateway", 120, ["api", "python", "async", "pydantic", "fast"]),
    ("nest", "NestJS", "nestjs/nest", "DevOps & Deploy", "Framework progresivo de Node.js para construir aplicaciones backend empresariales escalables.", 67800, 7800, 340, "MIT", "TypeScript", "Enterprise Spring Cloud", 150, ["backend", "typescript", "enterprise", "modular"]),
    ("hono", "Hono", "honojs/hono", "DevOps & Deploy", "Framework web ultrarrápido y ligero que se ejecuta en cualquier runtime de JavaScript (Node, Bun, Deno, Edge).", 21500, 890, 40, "MIT", "TypeScript", "Cloudflare Workers Enterprise", 100, ["edge", "ultrafast", "router", "web-framework"]),
    ("elysia", "Elysia", "elysiajs/elysia", "DevOps & Deploy", "Framework ergonómico para Bun con tipado estricto y rendimiento extremo.", 13800, 520, 60, "MIT", "TypeScript", "Fastify", 90, ["bun", "type-safety", "blazing-fast"]),
    ("shadcn-ui", "shadcn/ui", "shadcn-ui/ui", "DevOps & Deploy", "Colección de componentes React reusables y hermosos diseñados con Radix UI y Tailwind CSS.", 74200, 6900, 310, "MIT", "TypeScript", "MUI X Commercial", 180, ["ui-components", "tailwind", "radix", "accessible"]),
    ("lucide", "Lucide Icons", "lucide-icons/lucide", "DevOps & Deploy", "Librería de iconos vectoriales hermosos y consistentes, bifurcación comunitaria de Feather Icons.", 16400, 750, 45, "ISC", "TypeScript", "FontAwesome Pro", 80, ["icons", "svg", "design-system"]),
    ("tauri", "Tauri", "tauri-apps/tauri", "DevOps & Deploy", "Framework para construir aplicaciones de escritorio y móviles ultraligeras con frontend web y backend Rust.", 84500, 3200, 410, "Apache-2.0", "Rust", "Electron / Native dev", 150, ["desktop-apps", "rust", "lightweight", "cross-platform"]),
    ("flutter", "Flutter", "flutter/flutter", "DevOps & Deploy", "Framework multiplataforma de Google para crear aplicaciones nativas móviles, web y desktop desde una sola base de código.", 165000, 27100, 5400, "BSD-3-Clause", "Dart", "Native iOS/Android", 200, ["mobile", "cross-platform", "dart", "ui"]),
    ("k3s", "K3s", "k3s-io/k3s", "DevOps & Deploy", "Distribución ligera y certificada de Kubernetes empaquetada en un solo binario de menos de 100MB.", 29800, 2400, 280, "Apache-2.0", "Go", "AWS EKS / GKE", 450, ["kubernetes", "edge", "lightweight", "containers"]),
    ("redpanda", "Redpanda", "redpanda-data/redpanda", "Mensajería & Colas", "Motor de streaming compatible con Apache Kafka implementado en C++ con latencia predecible.", 10800, 690, 240, "BSL-1.1", "C++", "Confluent Cloud", 550, ["kafka-compatible", "low-latency", "cpp"]),
    ("seaweed-cache", "Tile38", "tile38/tile38", "Base de Datos", "Base de datos y motor de geovallado (geofencing) en tiempo real para aplicaciones de logística.", 9100, 580, 45, "MIT", "Go", "Radar.io / AWS Location", 180, ["geospatial", "geofence", "realtime", "logistics"]),
    ("huggingface-tei", "Text Embeddings Inference", "huggingface/text-embeddings-inference", "IA & LLMs", "Servidor de embeddings de texto de ultra-alta velocidad en Rust para modelos BERT y bi-encoders.", 3400, 290, 40, "Apache-2.0", "Rust", "OpenAI Embeddings API", 150, ["embeddings", "rust", "vector", "high-throughput"]),
    ("open-telemetry", "OpenTelemetry Collector", "open-telemetry/opentelemetry-collector", "Monitoreo & Logs", "Componente agnóstico para recibir, procesar y exportar telemetría a cualquier backend de observabilidad.", 4800, 1900, 420, "Apache-2.0", "Go", "DataDog Agent", 200, ["observability", "traces", "metrics", "vendor-neutral"]),
    ("cert-manager", "cert-manager", "cert-manager/cert-manager", "Seguridad", "Controlador nativo de Kubernetes para gestión automatizada de certificados TLS/SSL.", 12400, 1800, 280, "Apache-2.0", "Go", "Commercial Certificate Managers", 250, ["kubernetes", "tls", "certificates", "automation"]),
    ("external-secrets", "External Secrets Operator", "external-secrets/external-secrets", "Seguridad", "Operador de Kubernetes que sincroniza secretos desde AWS Secrets Manager, Vault o Google Secret Manager.", 4900, 980, 120, "Apache-2.0", "Go", "Custom Sync Scripts", 150, ["kubernetes", "secrets", "vault", "sync"]),
    ("velero", "Velero", "vmware-tanzu/velero", "DevOps & Deploy", "Herramienta open source para copias de seguridad, restauración y migración de clústeres de Kubernetes.", 9800, 1400, 260, "Apache-2.0", "Go", "Cloud Backup Services", 200, ["backup", "disaster-recovery", "kubernetes"])
]

def build_complete_catalog():
    repos = list(SEED_REPOSITORIES)
    base_id_set = {r["id"] for r in repos}

    for item in EXTENDED_CATALOG_DATA:
        slug, name, full_name, category, desc, stars, forks, issues, lic, lang, saas, cost, tags = item
        if slug in base_id_set:
            continue

        integration_type = "Docker" if "DevOps" in category or "Base de Datos" in category else "SDK"
        difficulty = "Fácil" if stars > 30000 else "Intermedio"

        snippet = f"""# Integración rápida para {name}
docker run -d --name {slug}-service -p 8080:8080 {slug}:latest
"""
        if lang in ["TypeScript", "JavaScript"]:
            snippet = f"""import {{ Client }} from "{slug}";

const client = new Client({{
  apiKey: process.env.{slug.upper().replace("-", "_")}_API_KEY || "test_token"
}});
console.log("{name} inicializado correctamente");
"""
        elif lang == "Python":
            snippet = f"""import os

API_KEY = os.getenv("{slug.upper().replace("-", "_")}_KEY")
print("Conectando a {name}...")
"""

        repo_obj = {
            "id": slug,
            "name": name,
            "full_name": full_name,
            "category": category,
            "description": desc,
            "stars": stars,
            "forks": forks,
            "open_issues": issues,
            "last_updated": "2026-10-15T12:00:00Z",
            "license": lic,
            "language": lang,
            "health_score": min(98, max(75, int(95 - (issues / (forks + 10)) * 5))),
            "maintenance_level": "Excelente" if stars > 15000 else "Activo",
            "active_maintainer": True,
            "website_url": f"https://github.com/{full_name}",
            "github_url": f"https://github.com/{full_name}",
            "docs_url": f"https://github.com/{full_name}#readme",
            "saas_alternative": saas,
            "estimated_monthly_saas_cost": cost,
            "tags": tags,
            "integration": {
                "title": f"Patrón de integración estándar para {name}",
                "integration_type": integration_type,
                "stack_compatibility": ["Docker", "Node.js", "Python", lang],
                "difficulty": difficulty,
                "triggers_webhooks": "Eventos de servicio y alertas de salud",
                "dependencies": [f"{slug}-client", "docker"],
                "docs_link": f"https://github.com/{full_name}#readme",
                "explanation": f"Permite desacoplar y orquestar {name} en la infraestructura B2B reduciendo costos de SaaS.",
                "code_snippet": snippet
            }
        }
        repos.append(repo_obj)
        base_id_set.add(slug)

    return repos

if __name__ == "__main__":
    catalog = build_complete_catalog()
    print(f"Total repositorios generados: {len(catalog)}")
