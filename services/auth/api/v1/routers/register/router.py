
# TODO:
# @router.post(
#     path="/register",
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         201: {
#             "description": "Успешная регистрация",
#             "content": {
#                 "application/json": {"example": {"id": 1, "email": "ivan@example.com"}}
#             },
#         },
#         400: {
#             "description": "Ошибки валидации",
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "detail": {
#                             "email": ["Enter a valid email address."],
#                             "password": ["Passwords do not match."],
#                         }
#                     }
#                 }
#             },
#         },
#         409: {
#             "description": "Пользователь с таким `email` уже существует",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "User with this email already exists."}
#                 }
#             },
#         },
#     },
#     response_model=RegisterResponse,
#     dependencies=[Depends(validate_content_type)],
# )
# async def register(
#     body: RegisterRequests,
#     usecase: RegisterUseCase = Depends(get_register_usecase),
# ):
#     try:
#         user = await usecase.execute(*map_register_request_to_form(body))
#     except ValidationError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors
#         ) from e
#     except RegisterError as e:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail=e.args[0]
#         ) from e

#     return map_user_to_response(user)
