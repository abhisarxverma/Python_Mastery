from ..models.member import Member
from ..utils import AutoErrorDecorate, give_absolute_path, safe_json_dump, safe_json_load
import json

MEMBER_DATA_JSON_PATH = give_absolute_path("data/members.json")

class MemberService(AutoErrorDecorate):

    def __init__(self):
        self.all_members = {}
        self.total_members = 0

    def give_all_members(self):
        return self.all_members.items()
    
    def make_member_object(self, data:dict):
        """Makes and return the member object from the serialized member data imported from the json."""
        member = Member(
            member_id= data["id"],
            name=data["name"],
            max_loans=data["max_loans"],
            current_loans_count = data["current_loans_count"],
            fine_balance= data["fine_balance"]
        )
        return member

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

    def export_members_json(self, filepath=MEMBER_DATA_JSON_PATH):
        """Export the members data to the json file."""

        serialized_data = {id : member.serialize() for id, member in self.give_all_members()}

        safe_json_dump(serialized_data, filepath)

        return True

    def import_members_json(self, filepath=MEMBER_DATA_JSON_PATH):
        """Import the members data from the json file."""

        data = safe_json_load(filepath)

        if not data: return

        for _, member_data in data.items():
            member = self.make_member_object(member_data)
            self.all_members[member.member_id] = member
            member.current_loans_count = 0
            self.total_members += 1

        return True
    
    def increase_member_loan_count(self, member: Member):
        member.current_loans_count += 1