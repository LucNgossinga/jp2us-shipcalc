import tkinter as tk
from tkinter import ttk, messagebox
from src.model.shipping_rates import EMS_RATE_TABLE, EMS_ZONES


def open_shipping_editor(parent):
    popup = tk.Toplevel(parent)
    popup.title("Edit EMS Shipping Rates")
    popup.geometry("1000x500")
    popup.minsize(900, 400)

    zone_names = list(EMS_ZONES.keys())
    weight_steps = sorted(EMS_RATE_TABLE.keys())
    entry_vars = {}  # key = (weight, zone_index), value = tk.StringVar()

    # === Scrollable Container ===
    container = ttk.Frame(popup)
    container.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))
    popup.rowconfigure(0, weight=1)
    popup.columnconfigure(0, weight=1)

    canvas = tk.Canvas(container, highlightthickness=0)
    v_scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    h_scroll = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="inner_frame")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas_width = event.width
        canvas.itemconfig("inner_frame", width=canvas_width)

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # === Header Row ===
    headers = ["Weight (g)"] + zone_names
    for col, name in enumerate(headers):
        ttk.Label(scrollable_frame, text=name, font=("Segoe UI", 10, "bold")).grid(
            row=0, column=col, padx=5, pady=(0, 5), sticky="nsew"
        )
        scrollable_frame.columnconfigure(col, weight=1, uniform="ratecol")

    # === Editable Grid ===
    for row_index, weight in enumerate(weight_steps, start=1):
        ttk.Label(scrollable_frame, text=f"Up to {weight}g").grid(
            row=row_index, column=0, padx=5, pady=2, sticky="w"
        )
        rates = EMS_RATE_TABLE[weight]
        for col_index, rate in enumerate(rates):
            var = tk.StringVar(value=str(rate))
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=10, justify="right")
            entry.grid(row=row_index, column=col_index + 1, padx=5, pady=2, sticky="ew")
            entry_vars[(weight, col_index)] = var

    # === Save Button ===
    def save_changes():
        updated = {}
        for (weight, zone_index), var in entry_vars.items():
            val = var.get().strip()
            if not val.isdigit():
                messagebox.showerror("Invalid Input", f"Non-integer found at {weight}g / Zone {zone_index + 1}")
                return
            updated.setdefault(weight, [None]*len(zone_names))
            updated[weight][zone_index] = int(val)

        # Apply in-session update
        for weight, new_rates in updated.items():
            EMS_RATE_TABLE[weight] = new_rates

        messagebox.showinfo("Success", "Shipping rates updated for this session.")

    # === Footer Buttons ===
    footer = ttk.Frame(popup)
    footer.grid(row=1, column=0, sticky="ew", pady=10, padx=10)
    ttk.Button(footer, text="Save Changes", command=save_changes).pack(side="right", padx=(0, 10))
    ttk.Button(footer, text="Close", command=popup.destroy).pack(side="right")
