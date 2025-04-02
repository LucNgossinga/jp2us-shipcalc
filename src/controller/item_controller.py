from src.model.item import Item


class ItemController:
    def __init__(self):
        self._items = []
        self._next_item_id = 1

    def add_item(self, name: str, weight: int, price: int) -> Item:
        item = Item(self._next_item_id, name, weight, price)
        self._items.append(item)
        self._next_item_id += 1
        return item

    def delete_item(self, item_no: int):
        self._items = [item for item in self._items if item.item_no != item_no]

    def get_item(self, item_no: int):
        for item in self._items:
            if item.item_no == item_no:
                return item
        return None

    def update_item(self, item_no: int, name: str, weight: int, price: int) -> Item:
        self.delete_item(item_no)
        item = Item(item_no, name, weight, price)
        self._items.append(item)
        return item

    def get_all_items(self):
        return sorted(self._items, key=lambda x: x.item_no)

    def clear_all(self):
        self._items.clear()
        self._next_item_id = 1
