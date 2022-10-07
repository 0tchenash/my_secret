from dao.users_dao import UserDAO
from services.users_service import UserService
from dao.contact_dao import ContactDAO
from services.contact_service import ContactService
# from service.auth import AuthService
from files.setup_db import db


user_dao = UserDAO(session=db.session)

user_service = UserService(dao=user_dao)

contact_dao = ContactDAO(session=db.session)

contact_service = ContactService(dao=contact_dao)

# auth_service = AuthService(UserService(user_dao))