from fastapi import FastAPI,Path 
from typing import Optional
from pydantic import BaseModel
from urllib.parse import urlparse

app = FastAPI()


inventory = []


class product(BaseModel):
    link : str
    name : Optional[str] = None
    price : Optional[float] = None
    brand : Optional[str] = None
    source: Optional[str] = None


def main():
    operation = input(display_menu())
    match operation:
        case "1":
            add_product()
            print(inventory)
        case "2":
            update_product()
        case "3":
            get_by_name()
        case "4":
            get_all()
        case "5":
            delete_product()
        case "6":
            exit_program()
        case _:
            print("Invalid menu selection.")
    


def add_product():
    id = len(inventory) + 1
    print(f"Product {id}:")
    l =  input("Enter the link of the product            : ")
    n =  input("Enter name of the product (Optional)     : ")
    p = input("Enter the price of the product (Optional): ")
    b = input("Enter the brand of the product (Optional): ")

    inventory.append({
        "id" : id,
        "link" : l,
        "name" : n,
        "price" : p,
        "brand" : b,
        "source" : get_source(l)
    })

def update_product():
    op = input("1.Choose product by viewing cart\n2.Choose product by name")
   

def get_by_name():
    return ""

def get_all():
    return ""

def delete_product():
    return ""

def exit_program():
    return ""
  
def get_source(l: str):
    parsed =  urlparse(l)
    domain = parsed.netloc
    return domain

def display_menu():
    return "1.Add Product to the Cart\n2.Update Product details\n3.Get Product by Name\n4.Get all Products in the Cart\n5.Delete Product\n6.Exit\n"

@app.get("/create-product")
def home():
    return inventory



main()