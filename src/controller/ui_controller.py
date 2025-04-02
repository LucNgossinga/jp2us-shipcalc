from tkinter import messagebox
from src.model.shipping_rates import get_ems_shipping_cost
from src.model.calculator import allocate_shipping_costs
from src.ui.result_popup import show_shipping_results


class UIController:
    def __init__(self, tree, name_var, weight_var, price_var, zone_var, weight_label_var, item_controller, root):
        self.tree = tree
        self.name_var = name_var
        self.weight_var = weight_var
        self.price_var = price_var
        self.zone_var = zone_var
        self.weight_label_var = weight_label_var
        self.controller = item_controller
        self.root = root  # for showing popups

    def clear_inputs(self):
        self.name_var.set("")
        self.weight_var.set("")
        self.price_var.set("")
        self.tree.focus_set()

    def update_total_weight(self):
        total = sum(item.weight for item in self.controller.get_all_items())
        self.weight_label_var.set(f"Total weight: {total} g")

    def add_item(self):
        name = self.name_var.get().strip()
        weight_str = self.weight_var.get().strip()
        price_str = self.price_var.get().strip()

        if not weight_str or not weight_str.isdigit():
            messagebox.showerror("Invalid Weight", "Please enter a valid positive weight (grams).")
            return
        if not price_str or not price_str.isdigit():
            messagebox.showerror("Invalid Price", "Please enter a valid price (¥).")
            return

        weight = int(weight_str)
        price = int(price_str)

        if weight <= 0:
            messagebox.showerror("Invalid Weight", "Weight must be greater than 0g.")
            return
        if price < 0:
            messagebox.showerror("Invalid Price", "Price cannot be negative.")
            return

        item = self.controller.add_item(name, weight, price)
        self.tree.insert("", "end", iid=str(item.item_no), values=item.to_row())
        self.clear_inputs()
        self.update_total_weight()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        for iid in selected:
            self.tree.delete(iid)
            self.controller.delete_item(int(iid))
        self.update_total_weight()

    def edit_item(self):
        selected = self.tree.selection()
        if not selected or len(selected) != 1:
            messagebox.showinfo("Edit Item", "Please select exactly one item to edit.")
            return

        iid = selected[0]
        item = self.controller.get_item(int(iid))
        if item:
            self.name_var.set("" if item.name == "(No Name)" else item.name)
            self.weight_var.set(str(item.weight))
            self.price_var.set(str(item.price))
            self.tree.delete(iid)
            self.controller.delete_item(item.item_no)
        self.update_total_weight()

    def calculate_shipping(self):
        items = self.controller.get_all_items()
        if not items:
            messagebox.showinfo("No Items", "You must add at least one item.")
            return

        total_weight = sum(item.weight for item in items)
        zone_name = self.zone_var.get()
        total_cost = get_ems_shipping_cost(total_weight, zone_name)

        allocations = allocate_shipping_costs(items, total_cost, total_weight)
        show_shipping_results(self.root, allocations)

    def clear_all_items(self):
        if not self.tree.get_children():
            messagebox.showinfo("Nothing to Clear", "There are no items in the list to remove.")
            return

        confirm = messagebox.askyesno("Clear All Items", "Are you sure you want to delete all items?")
        if not confirm:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)
        self.controller.clear_all()
        self.update_total_weight()
