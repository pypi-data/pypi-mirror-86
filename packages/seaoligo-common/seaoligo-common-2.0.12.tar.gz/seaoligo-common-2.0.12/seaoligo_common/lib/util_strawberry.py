import os
from typing import Optional, TypedDict
from enum import Enum
from flask import current_app, g, request
from werkzeug.exceptions import Unauthorized
import strawberry
from strawberry.flask.views import GraphQLView
from strawberry.extensions import ExecutionContext, Extension


class UserPayload(TypedDict):
    id: int
    username: str
    email: str


class MyContext(TypedDict):
    current_user: Optional[UserPayload]


class MyGraphQLView(GraphQLView):
    def get_context(self) -> MyContext:
        payload: Optional[UserPayload] = g.current_user

        return {'current_user': payload}


class AuthExtension(Extension):
    def on_request_start(self, *, execution_context: ExecutionContext):
        if (
            execution_context.context.get('current_user')  # Valid login credentials provided
            or execution_context.query
            == 'query __ApolloGetServiceDefinition__ { _service { sdl } }'  # Gateway initialization
            or (os.environ.get('FLASK_ENV') == 'development' and request.headers.get('origin')
                == f"http://localhost:{os.environ.get('NODE_PORT')}")  # GraphiQL request
            or current_app.config['TESTING']  # Test environment
        ):
            return {}
        else:
            raise Unauthorized()


@strawberry.enum(description='Selection of organisms.')
class OrganismSelect(Enum):
    NONE = ''
    HUMAN = 'human'
    MOUSE = 'mouse'
    # RAT = 'rat'


organism_mapping = {
    'human': 9606,
    'mouse': 10090,
    # 'rat': 10116,
}


@strawberry.input
class InputWithOrganism:
    organism: Optional[OrganismSelect] = ''


@strawberry.enum(description='Selection of assemblies.')
class AssemblySelect(Enum):
    NONE = ''
    hg38 = 'hg38'
    mm10 = 'mm10'
    # rn6 = 'rn6'


@strawberry.input
class InputWithAssembly:
    assembly: Optional[AssemblySelect] = ''
