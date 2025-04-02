class Item:
    def __init__(self, item_no: int, name: str, weight: int, price: int):
        self.item_no = item_no
        self.name = name if name.strip() else "(No Name)"
        self.weight = weight
        self.price = price

    def to_row(self):
        """Return values as tuple for inserting into Treeview"""
        return self.name, self.weight, self.price

    def to_dict(self):
        return {
            "no": self.item_no,
            "name": self.name,
            "weight": self.weight,
            "price": self.price,
        }
