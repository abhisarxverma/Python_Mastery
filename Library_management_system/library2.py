from .models.member import Member
from .Services import MemberService
from .Services import DataService
from .Services import CatalogService
from .Services import LoanService
from .utils import *

LIBRARY_DATA_JSON_PATH = give_absolute_path("data/library.json")

class Library:

    def __init__(self, to_import: bool=True, to_save_data: bool=True):
        self.member_service = MemberService()
        self.data_service = DataService(self)
        self.catalog_service = CatalogService()
        self.loan_service = LoanService()

    def signup_new_member(self, member_name: str):
        new_member = self.member_service.register_member(member_name)
        self.loan_service.open_loan_account(new_member.member_id)
        self.data_service.export_members_json()
