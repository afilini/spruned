from sqlalchemy.exc import IntegrityError
from spruned.application.abstracts import AddressesRepository
from spruned.application.database import Address
from spruned.daemon import exceptions
from spruned.application import database


class AddressesSQLLiteRepository(AddressesRepository):
    def __init__(self, session):
        self.session = session

    @database.atomic
    def save_address(self, address: str):
        session = self.session()
        address = Address(serialized=address)
        session.add(address)
        try:
            session.flush()
        except IntegrityError:
            raise exceptions.DuplicateAddressException

    def is_address(self, address: str):
        session = self.session()
        return bool(session.query(database.Address).filter_by(serialized=address).one_or_none())

    def get_addresses(self):
        session = self.session()
        addresses = session.query(database.Address).all()
        return [address.serialized for address in addresses]

    @database.atomic
    def remove_address(self, address: str):
        session = self.session()
        address = session.query(database.Address).filter_by(serialized=address).one_or_none()
        if not address:
            return False
        session.delete(address)
        session.flush()
        return True
