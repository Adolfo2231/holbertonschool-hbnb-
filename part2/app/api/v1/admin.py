"""
Admin API Module

This module defines administrative API endpoints for managing users, places, reviews, and amenities.
Only users with `is_admin=True` can access these routes.

Features:
- Full CRUD operations for `Users`, `Places`, `Reviews`, and `Amenities`.
- Restricted access to administrators via `is_admin()`.
- Structured exception handling with `werkzeug.exceptions`.
- Uses `facade` for business logic execution.
- OpenAPI documentation with `@api.expect` and `@api.response` annotations.

All routes require `jwt_required()`, and a valid `Bearer Token` with admin privileges must be provided.
"""

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, InternalServerError
from app.services import facade

api = Namespace("admin", description="Admin operations")

def is_admin() -> dict:
    """
    Verifies if the current user is an administrator.

    Returns:
    - `dict`: User data if the user is an admin.
    
    Raises:
    - `Forbidden(403)`: If the user is not an administrator.
    """
    user = facade.get_user(get_jwt_identity())
    if not user or not user.is_admin:
        raise Forbidden("Admin privileges required")
    return user


# USERS CRUD
@api.route('/users/<string:user_id>')
class AdminUserModify(Resource):
    @api.response(200, "User found")
    @api.response(403, "Permiso denegado")
    @api.response(404, "Usuario no encontrado") 
    @jwt_required()
    def get(self, user_id: str) -> dict:
        """Obtener un usuario por ID (Solo admin)."""
        try:
            is_admin()
            user = facade.get_user(user_id)
            if not user:
                raise NotFound("Usuario no encontrado")
            return {"status": "success", "data": user.to_dict()}, 200
        except NotFound:
            raise NotFound("Usuario no encontrado")
        except Exception as e:
            raise InternalServerError(str(e))
    @api.response(200, "User successfully updated")
    @api.response(403, "Permission denied")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id: str) -> dict:
        """Update any user (Admin only)."""
        try:
            is_admin()
            update_data = request.get_json()
            result = facade.update_user(user_id, update_data, admin_override=True)
            return {"status": "success", "data": result}, 200
        except NotFound:
            raise NotFound("User not found")
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise InternalServerError(str(e))

    @api.response(200, "User successfully deleted")
    @api.response(403, "Permission denied")
    @api.response(404, "User not found")
    @jwt_required()
    def delete(self, user_id: str) -> dict:
        """Delete any user (Admin only)."""
        try:
            current_user_id = get_jwt_identity()
            result = facade.delete_user(user_id, current_user_id)
            
            if result:
                return {
                    "status": "success", 
                    "message": "User deleted successfully"
                }, 200
                
        except PermissionError as e:
            raise Forbidden(str(e))
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise InternalServerError(str(e))


# PLACES CRUD
@api.route('/places/<string:place_id>')
class AdminPlaceModify(Resource):
    @api.response(200, "Place successfully updated")
    @api.response(403, "Permission denied")
    @api.response(404, "Place not found")
    @jwt_required()
    def put(self, place_id: str) -> dict:
        """Update any place (Admin only)."""
        try:
            is_admin()
            update_data = request.get_json()
            result = facade.update_place(place_id, update_data)
            return {"status": "success", "data": result}, 200
        except NotFound:
            raise NotFound("Place not found")
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise InternalServerError(str(e))

    @api.response(200, "Place successfully deleted")
    @api.response(403, "Permission denied")
    @api.response(404, "Place not found")
    @jwt_required()
    def delete(self, place_id: str) -> dict:
        """Delete any place (Admin only)."""
        try:
            is_admin()
            facade.delete_place(place_id)
            return {"status": "success", "message": "Place deleted"}, 200
        except NotFound:
            raise NotFound("Place not found")
        except Exception as e:
            raise InternalServerError(str(e))


# REVIEWS CRUD
@api.route('/reviews/<string:review_id>')
class AdminReviewModify(Resource):
    @api.response(200, "Review successfully updated")
    @api.response(403, "Permission denied")
    @api.response(404, "Review not found")
    @jwt_required()
    def put(self, review_id: str) -> dict:
        """Update any review (Admin only)."""
        try:
            is_admin()
            update_data = request.get_json()
            result = facade.update_review(review_id, update_data)
            return {"status": "success", "data": result}, 200
        except NotFound:
            raise NotFound("Review not found")
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise InternalServerError(str(e))

    @api.response(200, "Review successfully deleted")
    @api.response(403, "Permission denied")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id: str) -> dict:
        """Delete any review (Admin only)."""
        try:
            is_admin()
            facade.delete_review(review_id)
            return {"status": "success", "message": "Review deleted"}, 200
        except NotFound:
            raise NotFound("Review not found")
        except Exception as e:
            raise InternalServerError(str(e))


# AMENITIES CRUD
@api.route('/amenities/<string:amenity_id>')
class AdminAmenityModify(Resource):
    @api.response(200, "Amenity successfully updated")
    @api.response(403, "Permission denied")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def put(self, amenity_id: str) -> dict:
        """Update any amenity (Admin only)."""
        try:
            is_admin()
            update_data = request.get_json()
            result = facade.update_amenity(amenity_id, update_data)
            return {"status": "success", "data": result}, 200
        except NotFound:
            raise NotFound("Amenity not found")
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise InternalServerError(str(e))

    @api.response(200, "Amenity successfully deleted")
    @api.response(403, "Permission denied")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def delete(self, amenity_id: str) -> dict:
        """Delete any amenity (Admin only)."""
        try:
            is_admin()
            facade.delete_amenity(amenity_id)
            return {"status": "success", "message": "Amenity deleted"}, 200
        except NotFound:
            raise NotFound("Amenity not found")
        except Exception as e:
            raise InternalServerError(str(e))
