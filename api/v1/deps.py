from fastapi import  Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker



def get_session_maker(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.session_maker


# def get_auth_container(request: Request) -> AuthContainer:
#     if not hasattr(request.app.state, "auth_container"):
#         session_maker = get_session_maker(request)
#         request.app.state.auth_container = AuthContainer(session_maker=session_maker)
#     return request.app.state.auth_container
