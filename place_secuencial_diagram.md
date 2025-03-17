sequenceDiagram
  participant User
  participant API as API Layer
  participant BL as Business Logic Layer
  participant DB as Database

  User->>API: POST /places (place details)
  API->>BL: validatePlace(data)
  BL->>DB: INSERT INTO places
  DB-->>BL: Return place ID
  BL-->>API: Return success response
  API-->>User: Place creation success message
