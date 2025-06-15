# 🏗️ System Architecture

This document describes the architecture of the AI Agents Platform.

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ Presentation Layer (Streamlit Views)                    │
├─────────────────────────────────────────────────────────┤
│ Business Layer (Controllers)                            │
├─────────────────────────────────────────────────────────┤
│ Infrastructure Layer (DAOs, Services, ADK Client)       │
├─────────────────────────────────────────────────────────┤
│ Domain Layer (Models)                                   │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Principles
- Separation of responsibilities by layer
- Dependency inversion for easier testing/maintenance
- Single responsibility per class/module

## 📦 Layer Structure

### 🖥️ Presentation Layer (`src/app/view/`)
- User interface (Streamlit)
- Input capture
- Basic form validation
- Session management

### 🎮 Business Layer (`src/app/controller/`)
- Orchestration of business flows
- Business rule validation
- Coordination between layers
- Transaction management

### 🔧 Infrastructure Layer (`src/app/infrastructure/`)
- Data persistence
- Integration with external APIs
- Service configuration

### 📊 Domain Layer (`src/app/model/`)
- Domain models
- Specific validations and behaviors

## 🤖 Agents Component (`src/agents/`)
- Independent service for AI agents (Google ADK)
- Communication via ADK
- Horizontally scalable

## 🛡️ Security
- Passwords with bcrypt
- Sessions via Streamlit
- Role and permission validation
- User data isolation
- Environment variables for credentials

## 🔮 Roadmap
- Short term: Redis cache, automated tests, CI/CD, metrics
- Medium term: microservices for agents, external API, WebSockets, containerization
- Long term: event-driven architecture, ML pipeline, multi-tenancy, edge computing

---

For feature details, see [Features](features.md).
For development standards, see [Developer Guide](development.md).
