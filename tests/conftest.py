import pytest

from app.schemas.users.user import User
from app.enums import Language, EnglishLevel


@pytest.fixture
def load_fake_user() -> User:
    from app.enums.enums import UserRole

    return User(
        email="jhondoe@example.com",
        recovery_email=None,
        name="Jhon",
        last_name="Doe",
        password="securepassword",
        role=UserRole.STUDENT,
    )


@pytest.fixture
def cohort_data():
    return {
        "cohort_name": "Test Cohort",
        "component_id": 1,
        "level_id": 1
    }


@pytest.fixture
def component_data():
    return {
        "component_name": "Test Component",
        "language": Language.ENGLISH
    }


@pytest.fixture
def enrollment_data():
    return {
        "user_id": 1,
        "cohort_id": 1,
        "is_active": True
    }


@pytest.fixture
def level_data():
    return {
        "level_name": EnglishLevel.A1
    }


@pytest.fixture
def scorm_progress_data():
    return {
        "user_id": 1,
        "unit_id": 1,
        "score": 75.0,
        "status": "in progress",
        "total_time": "00:30:00",
        "suspend_data": None
    }


@pytest.fixture
def unit_data():
    return {
        "title": "Test Unit",
        "description": "A test unit",
        "scorm_url": "http://example.com/scorm",
        "level_id": 1
    }


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
