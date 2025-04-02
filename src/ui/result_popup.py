import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv


def show_shipping_results(parent, allocations):
    """
    Opens a new popup window to show allocation results in a Treeview.
    Allows exporting to CSV.
    """
    popup = tk.Toplevel(parent)
    popup.title("Shipping Allocation Results")
    popup.geometry("800x350")
    popup.minsize(800, 350)
    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(0, weight=1)

    result_tree = ttk.Treeview(popup, columns=("name", "weight", "price", "base", "extra", "total", "final"),
                               show="headings")
    result_tree.pack(expand=True, fill="both", padx=10, pady=(10, 0))

    col_widths = {
        "name": 150,
        "weight": 80,
        "price": 80,
        "base": 80,
        "extra": 80,
        "total": 100,
        "final": 100,
    }

    for col, name in zip(
        ("name", "weight", "price", "base", "extra", "total", "final"),
        ["Name", "Weight", "Price ¥", "Base ¥", "Extra ¥", "Shipping ¥", "Final ¥"]
    ):
        result_tree.heading(col, text=name)
        result_tree.column(col, anchor="center", width=col_widths.get(col, 80))

    for row in allocations:
        result_tree.insert("", "end", values=(
            row["name"], row["weight"], row["price"],
            row["base_share"], row["extra_share"], row["total_shipping"],
            row["final_total"]
        ))

    # Totals
    total_price = sum(r["price"] for r in allocations)
    total_shipping = sum(r["total_shipping"] for r in allocations)
    total_final = sum(r["final_total"] for r in allocations)

    result_tree.insert("", "end", values=("", "", "", "", "", "", ""), tags=("spacer",))
    result_tree.insert("", "end", values=(
        "TOTAL", "", total_price, "", "", total_shipping, total_final
    ), tags=("total",))
    result_tree.tag_configure("total", font=("Segoe UI", 10, "bold"))

    # CSV Export
    def export_to_csv():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Allocation Results as CSV"
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Name", "Weight", "Price", "Base ¥", "Extra ¥", "Shipping ¥", "Final ¥"])
                for row in allocations:
                    writer.writerow([
                        row["name"], row["weight"], row["price"],
                        row["base_share"], row["extra_share"],
                        row["total_shipping"], row["final_total"]
                    ])
                writer.writerow([])
                writer.writerow(["TOTAL", "", total_price, "", "", total_shipping, total_final])
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not save CSV:\n{str(e)}")

    button_frame = ttk.Frame(popup)
    button_frame.pack(fill="x", padx=10, pady=(5, 10))
    ttk.Button(button_frame, text="Save as CSV", command=export_to_csv).pack(anchor="e")
