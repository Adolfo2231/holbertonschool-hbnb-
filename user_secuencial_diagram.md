sequenceDiagram
  participant User
  participant API as API Layer
  participant BL as Business Logic Layer
  participant DB as Database

  User->>API: POST /register (user details)
  API->>BL: validateUser(data)
  BL->>DB: INSERT INTO users
  DB-->>BL: Return user ID
  BL-->>API: Return success response
  API-->>User: Registration success message
