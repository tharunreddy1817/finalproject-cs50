from fastapi import FastAPI,Path 
from typing import Optional
from pydantic import BaseModel
from urllib.parse import urlparse
import json

app = FastAPI()


inventory = []


class Product(BaseModel):
    id : int
    link : str
    name : Optional[str] = None
    price : Optional[str] = None
    brand : Optional[str] = None
    source: Optional[str] = None

def main():
    global inventory
    print("\nWelcome to the E-commerce Cart Management System!")
    print("Please follow the instructions to manage your cart.")
    print_separator()

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            inventory = [Product(**item) for item in data]                                      
    except(FileNotFoundError, json.decoder.JSONDecodeError):
            inventory = []
    exit = True
    while(exit):
        operation = input(display_menu())
        match operation:
            case "1":
                add_product()
            case "2":
                update_product()
            case "3":
                get_by_name()
            case "4":
                get_all()
            case "5":
                delete_product()
            case "6":
                clear_cart()
            case "7":
                exit = exit_program()
                print("\nRESPONSE: Exiting the program. Thank you!\n")
            case _:
                print("\nRESPONSE: Invalid menu selection.\nPlease try again.\n")
        print_separator()


def add_product():
    print_separator()
    print("### Adding a new product to the cart:")
    global inventory
    p_id = len(inventory) + 1
    print(f"Product {p_id}:")
    l = input("Enter the link of the product            : ")
    n=  input("Enter name of the product (Optional)     : ")
    p = "$"+ input("Enter the price of the product (Optional): ")
    b = input("Enter the brand of the product (Optional): ")
    s = get_source(l)
    product = Product(id = p_id, link = l, name = n, price = p, brand = b, source = s)
    inventory.append(product)
    print("\n RESPONSE: Product added successfully.")
    print_line()
    print("--- Updated Cart: ")
    pretty_print(inventory)
    save_inventory()

def update_product():
    global inventory
    if len(inventory) == 0:
        print("\nRESPONSE: No items in Cart")
        return
    print_separator()
    print("### Updating a product in the cart:")
    print("Enter '7' to exit")
    print()

    op = input("1.Choose product by viewing cart\n2.Choose product by name\nEnter your choice: ")
    if op.strip() == "7":
        exit_program()
        return
    match op.strip():
        case "1":
            pretty_print(inventory)
            while True:
                try:
                    p_id = int(input("Enter the id of the product to update: "))
                    if p_id < 1 or p_id > len(inventory):
                        print("\nRESPONSE: Invalid Product ID. Please try again.")
                        continue
                    else:
                        break
                except ValueError:
                    print("\nRESPONSE: Invalid input. Please enter a valid Product ID.")
                    continue
            print("+++ You have selected product with ID:", p_id)

            
            for i in range(len(inventory)):
                if inventory[i].id == p_id:
                    print("Enter new details for the product (leave blank to keep current value):")
                    l = input("Enter the link of the product            : ")
                    n=  input("Enter name of the product (Optional)     : ")
                    p = "$" + input("Enter the price of the product (Optional): ")
                    b = input("Enter the brand of the product (Optional): ")
                    new_l = l if l else inventory[i].link
                    new_n = n if n else inventory[i].name
                    new_p = p if p else inventory[i].price  
                    new_b = b if b else inventory[i].brand
                    s = get_source(new_l)
                    inventory[i] = Product(id = p_id, link = new_l , name = new_n, price = new_p, brand = new_b, source = s)
                    print("\nRESPONSE: Product updated successfully.")
                    print_line()
                    print("--- Updated Cart: ")
                    pretty_print(inventory)
                    break
            else:
                print("\nRESPONSE: Invalid Product ID")
        case "2":
            while True:
                print("+++ Available products:")
                pretty_print(inventory)
                print("Enter '7' to exit")
                print()
                n = get_name()
                if n == "7":
                    exit_program()
                    return
                elif not n:
                    print("RESPONSE: Product name cannot be empty. Please try again.")
                    continue
                else:
                    print("+++ You have selected product with name:", n)
                    break
            for i in range(len(inventory)):
                if inventory[i].name == n:
                    print("Enter new details for the product (leave blank to keep current value):")
                    l = input("Enter the link of the product  : ")
                    p = "$" + input("Enter the price of the product : ")
                    b = input("Enter the brand of the product : ")
                    new_l = l if l else inventory[i].link
                    new_p = p if p else inventory[i].price  
                    new_b = b if b else inventory[i].brand
                    s = get_source(new_l)
                    inventory[i] = Product(id = inventory[i].id, link = new_l , name = n, price = new_p, brand = new_b, source = s)
                    print("\nRESPONSE: Product updated successfully.")
                    print_line()
                    print("--- Updated Cart: ")
                    pretty_print(inventory)
                    break
            else:
                print("\nRESPONSE: Invalid Product name")
    save_inventory()
            



def get_by_name():
    global inventory
    if len(inventory) == 0:
        print("\nRESPONSE: No items in Cart")
        return
    print_separator()
    print("### Getting product by name:")
    print("Enter '7' to exit")
    print()
    b = True
    while(b):
        n = get_name()
        if n == "7":
            exit_program()
            return
        for i in range(len(inventory)):
            if inventory[i].name == n:
                pretty_print([inventory[i]])
                b = False
        if(b):       
            print("\nRESPONSE: Invalid Product name")

def get_all():
    global inventory
    if len(inventory)>0:
        print("\nCart:")
        pretty_print(inventory)
    else:
        print("\nRESPONSE: No items in Cart")

def delete_product():
    global inventory
    if len(inventory) == 0:
        print("\nRESPONSE: No items in Cart")
        return
    print_separator()
    print("### Deleting a product from the cart:")
    print("Enter '7' to exit")
    print()
    op = input("1.Choose product by viewing cart\n2.Choose product by name\nEnter your choice: ")
    if op.strip() == "7":
        exit_program()
        return
    match op.strip():
        case "1":
            pretty_print(inventory)
            p_id = int(input("Enter the id of the product to delete: "))
            for i in range(len(inventory)):
                if inventory[i].id == p_id:
                    del inventory[i]
                    print("\nRESPONSE: Product deleted successfully.")
                    break
            else:
                print("\nRESPONSE: Invalid Product ID")
        case "2":
            n = get_name()
            for i in range(len(inventory)):
                if inventory[i].name == n:
                    del inventory[i]
                    print("\nRESPONSE: Product deleted successfully.")
                    break
            else:
                print("\nRESPONSE: Invalid Product name")
    save_inventory()

def clear_cart():
    global inventory
    inventory.clear()
    save_inventory()
    print_separator()
    print("\nRESPONSE: Cart cleared successfully.")

def exit_program():
    global inventory
    save_inventory()
    return False


def pretty_print(l):
    global inventory
    for i in range(len(l)):
        print(f"Product {i+1} :")
        print_line()
        for k,v in l[i].model_dump().items():
            if v is None:
                v = "N/A"
            print(f"\t{k} : {v},")
        print_line()

def get_name():
    global inventory
    n = input("Enter name of the Product : ").strip()
    return n

def save_inventory():
    global inventory
    with open("data.json", "w") as f:
        json.dump([product.model_dump() for product in inventory], f)

def print_line():
    print("=============================================================================================")

def print_separator():
    print("*********************************************************************************************\n")
  
def get_source(l: str):
    parsed =  urlparse(l)
    domain = parsed.netloc
    return domain

def display_menu():
    return "1.Add Product to the Cart\n2.Update Product details\n3.Get Product by Name\n4.Get all Products in the Cart\n5.Delete Product\n6.Clear cart\n7.Exit\n\nEnter your choice: "

@app.get("/create-product")
def home():
    global inventory
    return inventory



main()