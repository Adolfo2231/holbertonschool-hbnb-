```mermaid
graph TB
  subgraph Presentation Layer
    API["API Services"]
  end

  subgraph Business Logic Layer
    Logic["Core Logic, Models"]
  end

  subgraph Persistence Layer
    Database["Database"]
  end

  API -->|API Calls| Logic
  Logic -->|Database Queries| Database
