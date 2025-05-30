from ..models.member import Member

class MemberService:

    def __init__(self):
        self.all_members = {}

    def all_members(self):
        return self.all_members.items()

    def register_member(self, name) -> Member:
        """Create a new member and add them to the Data."""

        new_member = Member(name)
        self.all_members[new_member.member_id] = new_member
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
        self.members[id] = member
