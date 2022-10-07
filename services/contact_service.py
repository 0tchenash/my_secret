from dao.contact_dao import ContactDAO



class ContactService:
    def __init__(self, dao: ContactDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_by_userid(self, uid):
        return self.dao.get_by_username(uid)

    def create(self, data):
        return self.dao.create(data)

    def delete(self, user_id):
        return self.dao.delete(user_id)