# ✨ Features

This document summarizes the main features of the AI Agents Platform.

## Overview
- Complete interface for interacting with AI agents
- Authentication and session management
- Conversation history
- Admin panel for user management

## Authentication
- User registration with unique email/username and password validation
- Login with bcrypt password check and role-based access
- Session managed via Streamlit
- Automatic admin creation on first use

## Chat System
- Chat interface with agent selector, message input, and conversation history
- New conversation button to reset session
- Messages sent to agents via Google ADK and persisted in the database

## Agents
- Example: Bibble Agent
- Configurable via code and prompts

## Session Management
- Manual and automatic session creation
- Session history with previews and agent info
- Message persistence in database

## Admin Panel
- Restricted to admin users
- User listing, editing, role management, and deactivation

## Interface & UX
- Sidebar navigation and history
- Responsive layout for mobile/tablet
- Main states: login, register, app, admin panel, initial setup

## Technical Highlights
- Google ADK integration via REST API
- Automatic DB initialization and migrations
- Error handling with user-friendly messages
- Comprehensive logging system for monitoring and debugging

## Accessibility
- Responsive design
- Custom CSS for improved experience

## Roadmap (Highlights)
- Short term: message search, export, themes
- Medium term: multi-agent chat, file uploads, plugin system
- Long term: external API, mobile app, multi-language

## Support
- Report issues via GitHub
- Check application logs for debugging information
- See [Developer Guide](development.md) for contribution
- See [Logging System](logging.md) for monitoring and troubleshooting
