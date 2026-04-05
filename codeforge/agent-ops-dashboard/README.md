# AgentOps Dashboard

> **AgentOps Dashboard** – A fullstack monitoring and management system for agent operations with real-time dashboards for agent status, system health, and infrastructure metrics.

---

## 📌 Features

- **Agent Dashboard**: Monitor agent heartbeats, task scores, and project progress.
- **Ops Dashboard**: Real-time system health, error logs, and resource usage monitoring.
- **System Dashboard**: Network status, storage, and blockchain integration monitoring.
- **Real-time Data Visualization**: Live updates of system metrics using interactive UI components.
- **Dockerized Setup**: Full local development environment using PostgreSQL and Redis.

---

## 📦 Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later)
- [Python](https://www.python.org/) (v3.10 or later)
- [Docker](https://www.docker.com/) (optional for deployment)
- [Docker Compose](https://docs.docker.com/compose/) (optional for deployment)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/agent-ops-dashboard.git
cd agent-ops-dashboard
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set up the Environment

```bash
npm run dev
```

### 4. Run the Application

```bash
uvicorn src/backend/main.py
```

---

## 📁 Project Structure

```
agent-ops-dashboard/
├── src/
│   ├── backend/
│   │   └── main.py
│   │   └── api/
│   │   └── models/
│   │   └── database.py
│   └── frontend/
│       └── pages/
│           └── index.tsx
│       └── components/
│           └── AgentStatus.tsx
└── package.json
```

---

## 🧪 Testing

```bash
npm test
```

---

## 📦 Setup

```yaml
# Install dependencies
npm install

# Run the application
npm run dev
```

---

## 🌍 API Documentation

### Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/api/agents` | `GET` | Get agent data |
| `/api/metrics` | `GET` | Get metrics data |
| `/api/system` | `GET` | Get system data |

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.