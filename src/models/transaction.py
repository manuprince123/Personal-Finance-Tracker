class Transaction:
    def __init__(self, transaction_id, user_id, type, category, amount, date, description):
        self.id = transaction_id
        self.user_id = user_id
        self.type = type
        self.category = category
        self.amount = amount
        self.date = date
        self.description = description

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['user_id'],
            data['type'],
            data['category'],
            data['amount'],
            data['date'],
            data['description']
        )

    def to_tuple(self):
        return (self.date, self.type, self.category, self.amount, self.description)

    def __str__(self):
        return f"Transaction({self.date}, {self.type}, {self.category}, {self.amount})"
