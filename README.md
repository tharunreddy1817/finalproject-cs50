# Personal E-commerce Cart Manager

#### Video Demo: (https://youtu.be/AUri70E1ofo)

#### Description:

The **Personal E-commerce Cart Manager** is a command-line application designed to help users store, manage, and review products from various e-commerce platforms such as Amazon, Temu, and Walmart—all in one personal cart. This tool provides a simple way to keep track of products you want to save or purchase in the future, eliminating the hassle of navigating multiple shopping apps or websites.

This project is built using Python and leverages the Pydantic library for data validation and serialization. It stores cart data persistently in a JSON file (`data.json`), enabling users to maintain their product list across sessions.

### Features:
- Add new products with details such as link, name, price, brand, and source platform.
- Update existing product information by product ID or name.
- Retrieve product details by name.
- View all products currently saved in the cart.
- Delete products by ID or name.
- Clear the entire cart after confirmation.
- Exit the program with data automatically saved.

### Files in this project:
- **project.py**: Contains the main program logic, including all the functions to manage the cart.
- **test_project.py**: Contains comprehensive unit tests using `pytest` and `monkeypatch` to ensure reliability of each feature.
- **data.json**: A JSON file that stores the user's cart data persistently. Created and updated automatically by the program.

### Design Considerations:
I chose a CLI-based application to focus on core functionality and make the tool lightweight and accessible without requiring a web interface. Pydantic was used to ensure the data integrity of each product item. Storing data in JSON allows easy portability and manual editing if needed. 

Future improvements could include adding a GUI or web interface and integrating APIs from e-commerce platforms for direct product import.