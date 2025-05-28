from .MemberService import MemberService
from .CatalogService import CatalogService

class AnalytsService :

    def __init__(self):
        self.member_service = MemberService()
        self.catalog_service = CatalogService()

        self.data = {}

    def update_data(self, loan):
        self.data["Books"][loan.book.isbn]["Loan count"] += 1
        self.data["Members"][loan.member.member_id]["Loan count"] += 1
        self.export_stats()
        return True