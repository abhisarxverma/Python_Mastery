from ..models.member import Member
from ..utils import *

class MemberService(AutoErrorDecorate):

    def __init__(self):
        self.all_members = {}
        self.total_members = 0

    def give_all_members(self):
        return self.all_members.items()
    
    def import_members(self, data):
        self.all_members = data

    def register_member(self, name) -> Member:
        """Create a new member and add them to the Data."""
        new_member = Member(name)
        member_check = self.find_member(new_member.member_id)
        if member_check: raise ValueError(f"Member with name {name} already exists.")
        self.all_members[new_member.member_id] = new_member
        self.total_members += 1
        return new_member
    
    def find_member(self, member_id:str) -> Member:
        """Finds and return the member with the given member_id if exists else return None"""

        member = self.all_members.get(member_id, None)
        return member
    
    def add_fine_balance(self, member: Member, balance: int):
        """Adds the given balance in the the fine balance of the member given.

        Args:
            member (Member): Member object whose fine balance to update
            balance (int): Balance to add
        """
        member.fine_balance += balance

    def add_imported_member(self, member:Member):
        member.fine_balance = 0
        self.all_members[member.member_id] = member
        self.total_members += 1

    def get_fine_of_member(self, member_id:str):
        """Show the fine of the member by finding the member by member id."""

        member = self.find_member(member_id)
        if not member: raise ValueError(f"Invalid member id: {member_id} Please recheck.")
        fine = member.fine_balance
        return fine
