from flask_restplus import Api
from .auth import api as auth_ns
from .user import api as user_ns

api = Api(
    title='Users',
    version='1.0',
    description='User and authentication service'
)

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
