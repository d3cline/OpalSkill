# Opalstack Skill

**Plugin:** `oc_skill`
**Auth:** `OPALSTACK_API_TOKEN` — Bearer token via `Token <value>` header
**Base URL:** `https://my.opalstack.com/api/v1` (override with `ENV_STAGING` or `ENV_DEV`)

---

## Environment Variables

| Variable              | Required | Description                                        |
|-----------------------|----------|----------------------------------------------------|
| `OPALSTACK_API_TOKEN` | ✅       | Personal Access Token from my.opalstack.com        |
| `ENV_STAGING`         | —        | Set to any value to target `my.opalstack.live`     |
| `ENV_DEV`             | —        | Set to any value to target `my.opalstack.me`       |

---

## Tools

### `application`

Manages web applications.

⚠️ **For installer-based apps, call `installer_urls` before `create`** to get the
correct `type` and `installer_url` for your target server OS (`el7`/`el9`).

| Action          | HTTP  | Endpoint               | Required payload fields          |
|-----------------|-------|------------------------|----------------------------------|
| `list`          | GET   | `/app/list/`           | —                                |
| `read`          | GET   | `/app/read/{id}`       | `id`                             |
| `create`        | POST  | `/app/create/`         | `name`, `osuser`, `type`         |
| `update`        | POST  | `/app/update/`         | `id`                             |
| `delete`        | POST  | `/app/delete/`         | `id`                             |
| `installer_urls`| local | —                      | —                                |

**`create` payload example (static app):**
```json
{
  "name": "mysite-static",
  "osuser": "<osuser-uuid>",
  "type": "STA",
  "json": { "gzip": true, "expires": "off" }
}
```

**`create` payload example (WordPress via installer):**
```json
{
  "name": "mywp",
  "osuser": "<osuser-uuid>",
  "type": "NPF",
  "installer_url": "https://raw.githubusercontent.com/opalstack/installers/refs/heads/master/el9/wordpress/install.sh",
  "json": { "auto_site_url": true, "php_version": 83, "gzip": true }
}
```

> **Restart:** No dedicated restart endpoint exists in the API.
> To cycle an app, call `update` with the existing payload; the platform will
> reapply configuration which restarts the process stack.

> **Logs:** No log-fetch endpoint exists in the API.
> Access logs via SSH into the OSUser home directory under `~/logs/`.

---

### `domain`

Manages domain and subdomain names. A Domain must exist before assigning it to a Site.

| Action   | HTTP  | Endpoint                  | Required payload fields |
|----------|-------|---------------------------|-------------------------|
| `list`   | GET   | `/domain/list/`           | —                       |
| `read`   | GET   | `/domain/read/{id}`       | `id`                    |
| `create` | POST  | `/domain/create/`         | `name`                  |
| `update` | POST  | `/domain/update/`         | `id`, `name`            |
| `delete` | POST  | `/domain/delete/`         | `id`                    |

---

### `mariadb`

Manages MariaDB databases.  Create a `mariauser` first, then grant permissions via `update`.

| Action   | HTTP  | Endpoint                   | Required payload fields |
|----------|-------|----------------------------|-------------------------|
| `list`   | GET   | `/mariadb/list/`           | —                       |
| `read`   | GET   | `/mariadb/read/{id}`       | `id`                    |
| `create` | POST  | `/mariadb/create/`         | `name`, `server`        |
| `update` | POST  | `/mariadb/update/`         | `id`                    |
| `delete` | POST  | `/mariadb/delete/`         | `id`                    |

---

### `psqldb`

Manages PostgreSQL databases. Same lifecycle as MariaDB — create a `psqluser` first.

| Action   | HTTP  | Endpoint                  | Required payload fields |
|----------|-------|---------------------------|-------------------------|
| `list`   | GET   | `/psqldb/list/`           | —                       |
| `read`   | GET   | `/psqldb/read/{id}`       | `id`                    |
| `create` | POST  | `/psqldb/create/`         | `name`, `server`        |
| `update` | POST  | `/psqldb/update/`         | `id`                    |
| `delete` | POST  | `/psqldb/delete/`         | `id`                    |

---

### `osuser`

Manages OS shell users. Applications run under an OSUser on a specific WEB server.

| Action   | HTTP  | Endpoint                   | Required payload fields |
|----------|-------|----------------------------|-------------------------|
| `list`   | GET   | `/osuser/list/`            | —                       |
| `read`   | GET   | `/osuser/read/{id}`        | `id`                    |
| `create` | POST  | `/osuser/create/`          | `name`, `server`        |
| `update` | POST  | `/osuser/update/`          | `id`                    |
| `delete` | POST  | `/osuser/delete/`          | `id`                    |

---

## Endpoints not available in this API

| Desired capability | Status              | Notes                                      |
|--------------------|---------------------|--------------------------------------------|
| Restart app        | **Not available**   | No `/app/restart/` endpoint exists         |
| Fetch app logs     | **Not available**   | No log endpoint; use SSH                   |
| Cron job management| **Not available**   | No `/cron/` resource in the API            |

---

## Dependency order (create workflow)

```
Server (pre-existing)
 └─ OSUser          → needs: server
     └─ Application → needs: osuser, type
         └─ (optionally) Domain → Site
```

For database-backed apps:
```
Server → MariaDB / PSQLDB → MariaUser / PSQLUser → grant via db.update
```

---

## Registration (OpenClaw)

```python
from oc_skill import TOOLS

for tool_cls in TOOLS:
    openclaw.register(tool_cls())
```
