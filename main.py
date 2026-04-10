import os
import csv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

def load_pizza_prices(csv_file):
    pizza_prices = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, price = row
                pizza_prices[name] = float(price.strip())
    except Exception as e:
        print(f"Error reading pizza prices CSV: {e}")
    return pizza_prices

def save_images(path, image_dict):
    VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    images_file = []              
    for file in os.listdir(path):
        print(file)
        if file.lower().endswith(VALID_IMAGE_EXTENSIONS):
            images_file.append(file)

    images_file.sort()
    for file in images_file:
        try:
            file_name = os.path.splitext(file)[0]
            print(file_name)
            image = Image.open(path + file)
            image = image.resize((80, 80), Image.Resampling.LANCZOS)
            photo_img = ImageTk.PhotoImage(image)
            image_dict[file_name] = photo_img
        except Exception as e:
            print(f"Failed to process {file}: {e}")
    for name, details in image_dict.items():
        print("image_dict:", name, details)

def pizza_images_as_buttons(btn1, btn2, images, pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart, pizza_prices):
    pizza_button = {}
    column = 0
    row = 0
    for pizza_name, pizza_image in images.items():
        # Create a frame for each pizza button and label
        pizza_frame = ttk.Frame(pizza_item_details_frame)
        pizza_frame.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        
        # Pizza image button
        pizza_image_button = ttk.Button(
            pizza_frame,
            image=pizza_image,
            command=lambda name=pizza_name, image=pizza_image: load_image_in_frame(
                name, image, item_details_frame, order_details_frame, pizza_cart, pizza_prices
            )
        )
        pizza_image_button.pack()
        
        # Pizza name label (below the button)
        name_label = ttk.Label(pizza_frame, text=pizza_name)
        name_label.pack()
        
        pizza_button[pizza_name] = pizza_image_button
        
        column += 1
        if column > 5:  # Changed to 5 for 6 columns (0-6)
            column = 0
            row += 1

    btn1.state(["disabled"])
    btn2.state(["!disabled"])

def load_image_in_frame(name, image, item_details_frame, order_details_frame, pizza_cart, pizza_prices):
    for widget in item_details_frame.winfo_children():
        widget.destroy()
    
    # Pizza Image Label
    pizza_image_label = ttk.Label(item_details_frame, image=image)
    pizza_image_label.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

    # Pizza Name Label
    pizza_name_label = ttk.Label(item_details_frame, text=name)
    pizza_name_label.grid(row=0, column=1, sticky="ew")

    # Pizza Price Label
    pizza_price = ""
    for pizza_name, price in pizza_prices.items():
        if pizza_name == name:
            pizza_price = price
    pizza_price_label = ttk.Label(item_details_frame, text=f"Price: £{pizza_price}")
    pizza_price_label.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
    print(pizza_price)

    # Pizza Quantity Label
    quantity_label = ttk.Label(item_details_frame, text="Quantity:")
    quantity_label.grid(row=1, column=1)
    quantity_spinbox = ttk.Spinbox(item_details_frame, from_=1, to=100, width=4)
    quantity_spinbox.grid(row=1, column=2)

    def add_to_cart():
        qty = int(quantity_spinbox.get())
        print(qty)
        price = pizza_prices[name]
        if name in pizza_cart:
            pizza_cart[name]["quantity"] += qty
        else:
            pizza_cart[name] = {
                "quantity": qty,
                "price": price,
                "image": image
            }
        print("Pizza cart: ", pizza_cart)
        for widget in item_details_frame.winfo_children():
            widget.destroy()
        update_order_details_frame(order_details_frame, pizza_cart)

    add_to_cart_button = ttk.Button(item_details_frame, text="Add to Cart", command=add_to_cart)
    add_to_cart_button.grid(row=7, column=1, columnspan=2, pady=10)

    cancel_button = ttk.Button(item_details_frame, text="Cancel", command=lambda: clear_frame(item_details_frame))
    cancel_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")

def update_order_details_frame(order_details_frame, pizza_cart):
    for widget in order_details_frame.winfo_children():
        widget.destroy()

    cart_label = tk.Label(order_details_frame, text="Your order details: ")
    cart_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    row = 1
    total_price = 0.0
    for name, details in pizza_cart.items():
        quantity = details["quantity"]
        price = details["price"]
        line_total = quantity * price
        total_price += line_total

        img_label = tk.Label(order_details_frame, image=details["image"], font=("Arial", 12))
        img_label.grid(row=row, column=0, padx=0, pady=2, sticky="w")

        name_label = tk.Label(order_details_frame, text=name, font=("Arial", 12))
        name_label.grid(row=row, column=0, padx=0, pady=2, sticky="w")

        quantity_label = tk.Label(order_details_frame, text=f"Qty: {quantity}", font=("Arial", 12))
        quantity_label.grid(row=row, column=1, padx=2, pady=2, sticky="e")

        line_total_label = tk.Label(order_details_frame, text=f"Total: £{line_total:.2f}", font=("Arial", 12))
        line_total_label.grid(row=row, column=2, padx=2, pady=2, sticky="e")

        row += 1

    grand_total_label = tk.Label(order_details_frame, text=f"Grand Total: £{total_price:.2f}", font=("Arial", 14, "bold"))
    grand_total_label.grid(row=row, column=0, columnspan=3, pady=10)

    ttk.Button(order_details_frame, text="Cancel", style="big.TButton", width=12, 
              command=lambda: clear_cart(order_details_frame, pizza_cart)).grid(row=row + 1, column=1, pady=10, sticky="e")
    ttk.Button(order_details_frame, text="Confirm", style="big.TButton", width=12, 
              command=lambda: confirm_order(order_details_frame, pizza_cart)).grid(row=row + 1, column=2, pady=10, sticky="e")

def clear_all_frames(btn1, btn2, pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart):
    btn1.state(["!disabled"])
    btn2.state(["disabled"])

    for widget in pizza_item_details_frame.winfo_children():
        widget.destroy()
    for widget in item_details_frame.winfo_children():
        widget.destroy()
    for widget in order_details_frame.winfo_children():
        widget.destroy()
    pizza_cart.clear()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def clear_cart(order_details_frame, pizza_cart):
    for widget in order_details_frame.winfo_children():
        widget.destroy()
    pizza_cart.clear()
    empty_label = ttk.Label(order_details_frame, text="Your cart is empty", font=("Arial", 30, "bold"))
    empty_label.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

def confirm_order(order_details_frame, pizza_cart):
    for widgets in order_details_frame.winfo_children():
        widgets.destroy()
    info_label = ttk.Label(order_details_frame, text="Your order has been placed successfully.", font=("Arial", 30, "bold"))
    info_label.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
    pizza_cart.clear()

def add_pizza():
    print("Add New button activated")

def del_pizza():
    print("Delete button activated")

def quitApp(myApp):
    answer = messagebox.askquestion("Confirm", "Are you sure you want to quit?")
    if answer == "yes":
        myApp.destroy()

def configure_style():
    pass

def create_frames(myApp):
    myApp.grid_rowconfigure(1, weight=1)
    myApp.grid_rowconfigure(2, weight=1)
    myApp.grid_columnconfigure(0, weight=1)
    myApp.grid_columnconfigure(1, weight=1)

    frames = {
        "menu": tk.LabelFrame(
            myApp,
            background="cornsilk2",
            height=80,
            borderwidth=1
        ),
        "pizza": tk.LabelFrame(
            myApp,
            background="tomato2",
            width=450,
            height=350,
            borderwidth=2
        ),
        "details": tk.LabelFrame(
            myApp,
            background="gray9",
            width=100,
            borderwidth=1
        ),
        "cart": tk.LabelFrame(
            myApp,
            background="sea green",
            height=400,
            borderwidth=1
        )
    }

    frames["menu"].grid(row=0, column=0, columnspan=2, sticky="nsew")
    frames["pizza"].grid(row=1, column=0, sticky="nsew")
    frames["details"].grid(row=1, column=1, sticky="nsew")
    frames["cart"].grid(row=2, column=0, columnspan=2, sticky="nsew")

    frames["pizza"].grid_propagate(False)
    frames["details"].grid_propagate(False)
    frames["cart"].grid_propagate(False)

    return frames

def create_buttons(frame, myApp, allPizzaDict, pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart, pizza_prices):
    buttons = {
        "show": ttk.Button(frame, text="Show All Pizzas", style="TButton", width=20),
        "clear": ttk.Button(frame, text="Clear All Pizzas", style="TButton", width=20),
        "add": ttk.Button(frame, text="Add New", style="TButton", width=20),
        "delete": ttk.Button(frame, text="Delete", style="TButton", width=20),
        "quit": ttk.Button(frame, text="Quit", style="TButton", width=20)
    }

    buttons["show"].configure(
        command=lambda: pizza_images_as_buttons(buttons["show"], buttons["clear"], allPizzaDict, pizza_item_details_frame,
                                              item_details_frame, order_details_frame, pizza_cart, pizza_prices)
    )
    buttons["quit"].configure(command=lambda: quitApp(myApp))
    buttons["clear"].configure(command=lambda: clear_all_frames(buttons["show"], buttons["clear"],
        pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart))

    col = 0
    for name, btn in buttons.items():
        print(name, btn)
        btn.grid(row=0, column=col, padx=5, pady=5, ipadx=10, ipady=10)
        col += 1

    buttons["clear"].state(["disabled"])
    return buttons

def main():
    myApp = tk.Tk()
    myApp.title("Online Pizza Store -Sherin Maharjan (w2122515)")
    myApp.geometry("1200x1200")
    myApp.configure(background="red")

    configure_style()
    frames = create_frames(myApp)
   
    pathAllPizza = 'allPizza/'
    pizza_prices_csv = "pizza_prices.csv"

    allPizzaDict, pizza_cart, pizza_prices = {}, {}, load_pizza_prices(pizza_prices_csv)
    save_images(pathAllPizza, allPizzaDict)
    print(f"Number of pizza images: {len(allPizzaDict)}")

    create_buttons(frames["menu"], myApp, allPizzaDict, frames["pizza"], frames["details"], frames["cart"], pizza_cart, pizza_prices)

    myApp.mainloop()

if __name__ == "__main__":
    main()