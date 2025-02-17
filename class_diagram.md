classDiagram
  class User {
    +UUID id {unique}
    +String username {unique}
    +String first_name
    +String last_name
    #String email {unique}
    -String password
    #Boolean is_admin
    +DateTime created_at
    +DateTime updated_at
    +register()
    +update_profile()
    +delete_account()
    -encrypt_password()
  }

  class Place {
    +UUID id {unique}
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +User owner
    +Boolean is_active
    +List~Amenity~ amenities
    +DateTime created_at
    +DateTime updated_at
    +create_place()
    +update_place()
    +delete_place()
    +list_places()
    +Float get_average_rating()
    +set_active(status: Boolean)
  }

  class Review {
    +UUID id {unique}
    +Place place
    +User user
    +Integer rating
    +String comment
    +DateTime created_at
    +DateTime updated_at
    +create_review()
    +update_review()
    +delete_review()
    +list_reviews()
  }

  class Amenity {
    +UUID id {unique}
    +String name {unique}
    +String description
    +DateTime created_at
    +DateTime updated_at
    +create_amenity()
    +update_amenity()
    +delete_amenity()
    +list_amenities()
  }

  User "1" o-- "many" Place : owns
  User "1" o-- "many" Review : writes
  Place "1" *-- "many" Review : has reviews
  Place "many" o-- "many" Amenity : has amenities
