from dao.models.models import Contact

class ContactDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """Получение всех отзывов"""
        return self.session.query(Contact).all()

    def create(self, data):
        """создание отзыва"""
        contact = Contact(**data)

        self.session.add(contact)
        self.session.commit()

        return contact

    def delete(self, contact_id):
        """Удаление отзыва"""
        contact = self.session.query(Contact).get(contact_id)

        self.session.delete(contact)
        self.session.commit()

    def get_by_userid(self, uid):
        """Получение определенного отзыва по айди пользователя"""
        return self.session.query(Contact).filter(Contact.user_id == uid).first()