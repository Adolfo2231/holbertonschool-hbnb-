sequenceDiagram
  participant User
  participant API as API Layer
  participant BL as Business Logic Layer
  participant DB as Database

  User->>API: POST /reviews (review details)
  API->>BL: validateReview(data)
  BL->>DB: INSERT INTO reviews
  DB-->>BL: Return review ID
  BL-->>API: Return success response
  API-->>User: Review submission success message
