import tkinter as tk
from tkinter import ttk, messagebox
import platform
import os

from src.controller.item_controller import ItemController
from src.controller.ui_controller import UIController
from src.model import shipping_rates as controller_item
from src.ui.shipping_editor import open_shipping_editor


def launch_app():
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()

    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "favicon.ico"))
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print("❌ Icon load failed:", e)
    else:
        print("❌ Icon file not found at:", icon_path)

    def show_about():
        messagebox.showinfo(
            "About JP2US Shipping Calculator",
            "📦 JP2US Shipping Calculator\n\n"
            "Version: 1.0.0\n"
            "Author: Nathan\n"
            "Purpose: Calculate fair shipping allocation from Japan to US "
            "using EMS rate tables with hybrid logic."
        )
    menubar = tk.Menu(root)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menubar)
    root.title("JP2US Shipping Calculator")

    # === Modern Font Settings ===
    if platform.system() == "Windows":
        default_font = ("Segoe UI", 10)
    elif platform.system() == "Darwin":
        default_font = ("Helvetica Neue", 12)
    else:
        default_font = ("Arial", 10)

    style = ttk.Style()
    style.theme_use("default")
    style.configure(".", font=default_font)
    style.configure("TButton", padding=(6, 4))
    style.configure("TEntry", padding=(4, 2))

    if platform.system() == "Darwin":
        default_font = ("Roboto", 14)
        style = ttk.Style()
        style.configure(".", font=default_font)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    controller = ItemController()

    total_weight_label_var = tk.StringVar(value="Total weight: 0 g")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)

    # ========= Section Title =========
    ttk.Label(main_frame, text="📦 Item Entry", font=("Roboto", 16, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 10)
    )

    # ========= Inputs =========
    form_frame = ttk.Frame(main_frame)
    form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
    for i in range(6):
        form_frame.columnconfigure(i, weight=1)

    ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=(0, 4), sticky="e")
    name_var = tk.StringVar()
    name_entry = ttk.Entry(form_frame, textvariable=name_var, width=20)
    name_entry.grid(row=0, column=1, padx=(0, 8), sticky="ew")

    ttk.Label(form_frame, text="Weight (g):").grid(row=0, column=2, padx=(0, 4), sticky="e")
    weight_var = tk.StringVar()
    weight_entry = ttk.Entry(form_frame, textvariable=weight_var, width=10)
    weight_entry.grid(row=0, column=3, padx=(0, 8), sticky="ew")

    ttk.Label(form_frame, text="Price (¥):").grid(row=0, column=4, padx=(0, 4), sticky="e")
    price_var = tk.StringVar()
    price_entry = ttk.Entry(form_frame, textvariable=price_var, width=10)
    price_entry.grid(row=0, column=5, sticky="ew")

    # Focus on weight input on launch
    weight_entry.focus()

    # ========= Table Section Title =========
    ttk.Label(main_frame, text="🧾 Item List", font=("Roboto", 16, "bold")).grid(
        row=2, column=0, sticky="w", pady=(10, 5)
    )

    # ========= Treeview =========
    tree = ttk.Treeview(main_frame, columns=("name", "weight", "price"), show="headings", height=8)
    tree.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
    main_frame.rowconfigure(3, weight=1)

    weight_label = ttk.Label(main_frame, textvariable=total_weight_label_var, anchor="w")
    weight_label.grid(row=4, column=0, sticky="w", pady=(0, 5))

    tree.heading("name", text="Name")
    tree.heading("weight", text="Weight (g)")
    tree.heading("price", text="Price (¥)")

    tree.column("name", width=200, anchor="w")
    tree.column("weight", width=80, anchor="center")
    tree.column("price", width=80, anchor="center")

    # ========= Shipping Input Section =========
    ttk.Label(main_frame, text="🚚 Shipping Settings", font=(default_font[0], 14, "bold")).grid(
        row=5, column=0, sticky="w", pady=(20, 5)
    )

    shipping_frame = ttk.Frame(main_frame)
    shipping_frame.grid(row=6, column=0, sticky="ew", pady=(0, 10))
    for i in range(4):
        shipping_frame.columnconfigure(i, weight=1)

    ttk.Label(shipping_frame, text="Zone:").grid(row=0, column=0, padx=(0, 5), sticky="e")

    zone_var = tk.StringVar(value="Fourth Zone")
    zone_dropdown = ttk.Combobox(shipping_frame, textvariable=zone_var, state="readonly", width=25)
    zone_dropdown["values"] = list(controller_item.EMS_ZONES.keys())  # we'll link this from the model
    zone_dropdown.grid(row=0, column=1, padx=(0, 15), sticky="w")

    ui_controller = UIController(
        tree=tree,
        name_var=name_var,
        weight_var=weight_var,
        price_var=price_var,
        zone_var=zone_var,
        weight_label_var=total_weight_label_var,
        item_controller=controller,
        root=root,
    )

    # ========= Buttons =========
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=7, column=0, pady=(5, 0))

    ttk.Button(button_frame, text="Add Item", command=ui_controller.add_item).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Edit Selected", command=ui_controller.edit_item).grid(row=0, column=1, padx=10)
    ttk.Button(button_frame, text="Delete Selected", command=ui_controller.delete_item).grid(row=0, column=2, padx=10)
    ttk.Button(button_frame, text="Calculate Shipping", command=ui_controller.calculate_shipping).grid(row=0, column=3,
                                                                                                       padx=10)
    ttk.Button(button_frame, text="Clear All", command=ui_controller.clear_all_items).grid(row=0, column=4, padx=10)
    ttk.Button(button_frame, text="Edit EMS Rates", command=lambda: open_shipping_editor(root)).grid(row=0, column=5,
                                                                                                     padx=10)

    root.minsize(650, 450)
    root.mainloop()
