from collections import OrderedDict


class Transaction:

    def __init__(self, sender:str, recipient:str, amount:float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
    
    def to_ordered_dict(self):
        return OrderedDict([
            ('sender', self.sender), 
            ('recipient', self.recipient), 
            ('amount', self.amount)
        ])
    
    def __repr__(self):
            return super().__repr__()