sequenceDiagram
  participant User
  participant API as API Layer
  participant BL as Business Logic Layer
  participant DB as Database

  User->>API: GET /places
  API->>BL: fetchPlaces()
  BL->>DB: SELECT * FROM places
  DB-->>BL: Return place list
  BL-->>API: Return place list
  API-->>User: Display place list
