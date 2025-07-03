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
├─────────────────────────────────────────────────────────┤
│ External Interfaces                                     │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ MCP Server (Model Context Protocol)                 │ │
│ │ - Tool exposure via MCP protocol                    │ │
│ │ - ADK integration                                   │ │
│ │ - stdio transport                                   │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Principles
- **Separation of Concerns**: Each layer has well-defined responsibilities
- **Dependency Inversion**: Higher layers depend on abstractions, not implementations
- **Single Responsibility**: Each class/module has one reason to change
- **Factory Pattern**: Centralized dependency creation and management
- **Component-Based UI**: Reusable and testable interface components
- **MVC Architecture**: Clear separation between Model, View, and Controller

## 🏗️ Design Patterns

### Factory Pattern
- **Purpose**: Centralizes creation and management of all dependencies
- **Benefits**: Singleton for shared resources, simplified dependency injection
- **Usage**: All instances of DAOs, services and controllers are created by the factory

### Component Pattern
- **Purpose**: Creation of reusable UI components with clear interfaces
- **Benefits**: Separation of presentation logic from business logic, easier testing
- **Usage**: Interface elements like menus, chat, history are independent components

### Router Pattern
- **Purpose**: Centralizes all application navigation logic
- **Benefits**: Clear separation between routing and business logic, extensible for new views
- **Usage**: Controls which screen is displayed based on user session state

### MVC (Model-View-Controller)
- **Model**: Domain entities with business rules
- **View**: User interface and visual components
- **Controller**: Application logic and coordination between layers

## 📦 Layer Structure

### 🖥️ Presentation Layer (`src/app/view/`)
Responsible for user interface and end-user interaction.

**Main functionalities:**
- **Authentication**: Login, registration and access control
- **Chat Interface**: Main interface for conversations with agents
- **Admin Panel**: User management and configuration settings
- **Reusable Components**: Modular and reusable UI elements
- **Styling**: CSS and visual configurations
- **Form Validation**: Basic user input validation

### 🎮 Business Layer (`src/app/controller/`)
Contains business logic and orchestration of application flows.

**Main functionalities:**
- **Chat Control**: Management of conversations and messages
- **Administrative Operations**: Logic for user CRUD and permissions
- **Session Management**: User state control and navigation
- **Routing**: Navigation between different application screens
- **Business Rule Validation**: Application of domain-specific rules
- **Layer Coordination**: Orchestration of complex operations

### 🔧 Infrastructure Layer (`src/app/infrastructure/`)
Provides infrastructure services, data persistence and external integrations.

**Main functionalities:**
- **Data Access**: Database operations (CRUD) for all entities
- **ADK Integration**: Communication with AI agents via Google ADK
- **Authentication and Security**: Password encryption and credential validation
- **Dependency Management**: Factory pattern for object creation
- **Application Configuration**: Settings and Streamlit configurations
- **System Initialization**: Database and schema setup
- **State Management**: Streamlit session control
- **Logging System**: Centralized logging for monitoring and debugging (see [logging.md](logging.md))

### 📊 Domain Layer (`src/app/model/`)
Defines business entities and their specific rules.

**Main functionalities:**
- **User Entities**: Representation and validation of user data
- **Chat Session Management**: Modeling of conversations and history
- **Messages**: Structure and validation of messages between user and agents
- **Email Validation**: Specific rules for email address validation
- **Domain Invariants**: Business rules that must always be respected
- **Specific Behaviors**: Methods and properties of entities

## 🤖 Agents Component (`src/agents/`)
- Independent service for AI agents (Google ADK)
- Communication via ADK
- Horizontally scalable

## 🔄 Main Application Flows

### Authentication Flow
1. **View Layer**: Captures user credentials
2. **Controller Layer**: Validates input and coordinates authentication
3. **Infrastructure Layer**: Verifies credentials in database
4. **Model Layer**: Applies user validation rules

### Chat Flow
1. **View Layer**: Displays chat interface and captures message
2. **Controller Layer**: Processes message and coordinates sending to agent
3. **Infrastructure Layer**: Communicates with ADK and persists messages
4. **Model Layer**: Validates message structure

### Administration Flow
1. **View Layer**: Admin panel with forms
2. **Controller Layer**: Applies authorization rules and coordinates operations
3. **Infrastructure Layer**: Executes CRUD operations in database
4. **Model Layer**: Validates data and business rules

## 🛡️ Security
- Passwords with bcrypt
- Sessions via Streamlit
- Role and permission validation
- User data isolation
- Environment variables for credentials

## 📊 Monitoring & Observability
- **Comprehensive Logging**: All application operations are logged with appropriate levels
- **Log Files**: Daily rotating logs stored in `src/app/logs/`
- **Error Tracking**: Detailed error logs with stack traces for debugging
- **Audit Trail**: User actions, authentication attempts, and system operations are tracked
- **Performance Monitoring**: Key operations timing and resource usage logging
- See [Logging System](logging.md) for detailed information

## 🔮 Roadmap
- Short term: Redis cache, automated tests, CI/CD, metrics
- Medium term: microservices for agents, external API, WebSockets, containerization
- Long term: event-driven architecture, ML pipeline, multi-tenancy, edge computing

---

For feature details, see [Features](features.md).
For development standards, see [Developer Guide](development.md).
For monitoring and debugging, see [Logging System](logging.md).
