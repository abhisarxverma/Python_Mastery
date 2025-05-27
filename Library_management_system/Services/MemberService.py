from ..models.member import Member

class MemberService:

    def __init__(self):
        self.all_members = {}

    def register_member(self, name) -> Member:
        """Create a new member and add them to the Data."""

        new_member = Member(name)
        self.all_members[new_member.member_id] = new_member
        return new_member
    
    def find_member(self, member_id:str) -> Member:
        """Finds and return the member with the given member_id if exists else return None"""

        member = self.all_members.get(member_id, None)
        return member