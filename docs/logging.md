# AI Agents Application Logging System

## Summary
A strategic logging system has been implemented throughout the application to provide focused observability, efficient debugging, and critical monitoring without excessive noise.

## Log Configuration

### Current Configuration
- **Level**: INFO
- **Format**: `%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s`
- **Handlers**:
  - FileHandler (saves to file)
  - StreamHandler (displays in console)
- **Timezone**: UTC-3 (Brasília)

## Logging Philosophy

The logging system follows a **"Strategic Points Only"** approach, focusing on:
- **Security events** (authentication, authorization)
- **Critical operations** (database errors, API failures)
- **Business logic events** (user actions, session management)
- **Error handling** (all exceptions and failures)

## Log Types by Level

### INFO
- Application startup/shutdown
- Authentication events (login/logout)
- New chat session creation
- User registration
- Admin operations
- Database schema initialization

### WARNING
- Failed login attempts
- Invalid session access attempts
- Admin security violations (self-deletion, etc.)
- Application state redirections

### ERROR
- Database connection failures
- ADK communication errors
- User creation/update failures
- Application crashes
- Query execution failures

### DEBUG
- Only kept for critical debugging scenarios
- Password verification results (security debugging)

## Current Benefits

1. **Focused Traceability**: Critical actions are logged without noise
2. **Efficient Debugging**: Clear signal-to-noise ratio for problem identification
3. **Security Audit**: Complete authentication and authorization logging
4. **Performance Optimized**: Reduced I/O overhead from excessive logging
5. **Production Ready**: Clean logs suitable for monitoring and alerting

## Log Location

Logs are saved in:
```
src/app/logs/app_activity_YYYY-MM-DD.log
```

Example: `src/app/logs/app_activity_2025-06-30.log`

## Log Examples

### Authentication Flow:
```
2025-06-30 10:30:15 - INFO - [auth_views.py:15] - Login attempt for user: admin
2025-06-30 10:30:15 - INFO - [auth.py:65] - Attempting to authenticate user: admin  
2025-06-30 10:30:15 - INFO - [auth.py:77] - User authenticated successfully: admin
2025-06-30 10:30:15 - INFO - [auth_views.py:18] - Login successful for user: admin, role: admin
```

### Chat Session Creation:
```
2025-06-30 10:35:20 - INFO - [chat_controller.py:20] - Starting new chat session with agent: bibble
2025-06-30 10:35:21 - INFO - [chat_controller.py:55] - Chat session started successfully for user admin with agent bibble
```

### Error Handling:
```
2025-06-30 10:40:30 - ERROR - [adk_client.py:19] - Error fetching agents: Connection timeout
2025-06-30 10:40:30 - ERROR - [main_app_view.py:58] - Failed to fetch available agents: Connection timeout
```

### Security Events:
```
2025-06-30 11:15:45 - WARNING - [auth_views.py:28] - Login failed for user: testuser
2025-06-30 11:20:12 - WARNING - [admin_controller.py:68] - Admin john attempted to delete own account
```

### Application Lifecycle:
```
2025-06-30 09:00:00 - INFO - [main.py:9] - Starting application
2025-06-30 09:00:01 - INFO - [schema_init.py:7] - Initializing database schema
2025-06-30 09:00:02 - INFO - [schema_init.py:58] - Database schema initialization completed
```

## Best Practices Applied

1. **Log Level Appropriateness**: 
   - INFO for business events
   - WARNING for security concerns
   - ERROR for all failures
   - DEBUG only when absolutely necessary

2. **Message Clarity**:
   - Include context (usernames, operation types)
   - Avoid sensitive data (passwords, tokens)
   - Use consistent formatting

3. **Performance Considerations**:
   - Removed excessive debug logging
   - Focus on actionable information
   - Reduced I/O operations

4. **Security Focus**:
   - All authentication events logged
   - Admin operations tracked
   - Failed access attempts recorded
