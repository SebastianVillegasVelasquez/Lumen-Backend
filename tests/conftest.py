import pytest

from app.schemas.users.user import User


@pytest.fixture
def load_fake_user() -> User:
    from app.enums.enums import UserRole
    return User(
        email="jhondoe@example.com",
        recovery_email=None,
        name="Jhon",
        last_name="Doe",
        password="securepassword",
        role=UserRole.STUDENT
    )



# TEST_DATABASE_URL = settings.DATABASE_URL + "_test"
#
#
# @pytest.fixture(scope="session")
# def event_loop():
#     """Crea una instancia del loop de eventos para toda la sesión de tests."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest.fixture(scope="session")
# async def db_engine():
#     """Crea el motor de base de datos y las tablas al iniciar los tests."""
#     engine = create_async_engine(settings.DATABASE_URL)  # O usar TEST_DATABASE_URL
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     yield engine
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     await engine.dispose()
#
#
# @pytest.fixture
# async def db_session(db_engine):
#     """Crea una sesión de base de datos limpia para cada test individual."""
#     async_session = async_sessionmaker(db_engine, expire_on_commit=False)
#     async with async_session() as session:
#         yield session
#         # Al terminar el test, se cierra la sesión
