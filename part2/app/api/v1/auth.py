from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        try:
            credentials = api.payload  # Recibe el payload

            # 🔹 Validar que ambos campos existan en la petición
            if not credentials or "email" not in credentials or "password" not in credentials:
                raise ValueError("Both 'email' and 'password' fields are required.")

            # 🔹 Recuperar el usuario
            user = facade.get_user_by_email(credentials['email'])

            # 🔹 Verificar credenciales
            if not user or not user.verify_password(credentials['password']):
                raise Unauthorized({
                    "message": {"The provided email or password is incorrect."
                    }
                })

            # 🔹 Crear el token si todo es válido
            access_token = create_access_token(identity=str(user.id))
            return {"status": "success", "access_token": access_token}, 200

        except ValueError as e:
            raise BadRequest(
                {"message": {"status": "error", "message": str(e)}})

        except Unauthorized as e:
            raise Unauthorized(
                {"message": {"status": "error", "message": str(e)}})

        except Exception as e:
            raise InternalServerError({
                "message": {
                    "status": "error",
                    "message": "Unexpected server error",
                    "details": str(e)
                }
            })


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        user = facade.get_user(current_user)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "message": [
                "Hello, user:",
                f"Name: {user.first_name} {user.last_name}",
                f"ID: {user.id}"
            ]
        }, 200
