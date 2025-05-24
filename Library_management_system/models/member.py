from ..utils import *

class Member:
    "Represents a Member of the Library"

    def __init__(self, name, member_id=None, max_loans=5, fine_balance: int=0, current_loans_count: int=0):
        self.name = name
        self.member_id = member_id or create_member_id(self.name)
        self.max_loans = max_loans
        self.fine_balance = fine_balance
        self.current_loans_count = current_loans_count

    def __repr__(self):
        return f"Member(Member_id={self.member_id!r} Member_name={self.name!r}"
    
    def __str__(self):
        return f"Member {self.name!r}"
    
    def __hash__(self):
        return hash((self.name, self.member_id))
    
    def __eq__(self, other):
        return isinstance(other, Member) and self.name == other.name and self.member_id == self.member_id
    
    def serialize(self):
        return {
            "id" : self.member_id,
            "name" : self.name,
            "fine_balance" : self.fine_balance,
            "max_loans" : self.max_loans,
            "current_loans_count" : self.current_loans_count,
        }
    
    @classmethod
    def make_member_object(cls, data:dict):
        """Makes and return the member object from the serialized member data imported from the json."""
        member = cls(
            member_id= data["id"],
            name=data["name"],
            max_loans=data["max_loans"],
            current_loans_count = data["current_loans_count"],
            fine_balance= data["fine_balance"]
        )
        return member
    