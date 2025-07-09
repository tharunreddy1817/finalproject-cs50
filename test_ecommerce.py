import pytest 
import builtins
import ecommerce 

def dummy_product():
    return ecommerce.Product(
        id=1,
        name="Dummy Product",
        price="$10",
        brand="Dummy Brand",
        link="https://dummy.link/product"
    )
def test_main(monkeypatch, capsys):
    inputs = iter(["9","7","y"])
    monkeypatch.setattr(builtins, 'input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        ecommerce.main()
    captured = capsys.readouterr()
    assert "RESPONSE: Invalid menu selection.\nPlease try again." in captured.out
    assert "RESPONSE: Exiting the program. Thank you!" in captured.out
    
def test_add_product(monkeypatch, capsys):
    inputs = iter(["https://a.co/d/cqSijmE", "Cricket Ball", "$","20", "Dukes"])

    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.add_product()
    product = ecommerce.inventory[-1]  
    captured = capsys.readouterr()
    assert "RESPONSE: Product added successfully." in captured.out
    assert product.name == "Cricket Ball"
    assert product.price == "$20"
    assert product.brand == "Dukes"
    assert product.link == "https://a.co/d/cqSijmE"

def test_update_product_with_empty_list(monkeypatch, capsys):
    ecommerce.inventory = []
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.update_product()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

def test_update_product_with_existing_product_id(monkeypatch, capsys):

    inputs = iter(["https://a.co/d/cqSijmE", "Cricket Ball", "$","20", "Dukes"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.add_product()

    inputs = iter(["1","-1",ecommerce.inventory[-1].id,"", "New Cricket Ball", "$","25", "New Dukes"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.update_product()

    product = ecommerce.inventory[-1]
    captured = capsys.readouterr()
    assert "RESPONSE: Invalid Product ID. Please try again." in captured.out
    assert "RESPONSE: Product updated successfully." in captured.out
    assert product.name == "New Cricket Ball"
    assert product.price == "$25"
    assert product.brand == "New Dukes"

def test_update_product_with_invalid_product_name(monkeypatch, capsys):
    inputs = iter(["2","","Jai Balayya", "New Cricket Ball","https://a.co/d/iWvWhnQ","SG Ball", "$", "15", "SG"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.update_product()
    product = ecommerce.inventory[-1]
    captured = capsys.readouterr()
    
    assert "RESPONSE: Product name cannot be empty. Please try again." in captured.out
    assert "+++ You have selected product with name: Jai Balayya" in captured.out
    assert "RESPONSE: Invalid Product name" in captured.out

def test_update_product_with_valid_product_name(monkeypatch, capsys):
    inputs = iter(["2", "New Cricket Ball","https://a.co/d/iWvWhnQ","SG Ball", "$", "15", "SG"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.update_product()
    product = ecommerce.inventory[-1]
    captured = capsys.readouterr()
    assert "RESPONSE: Product updated successfully." in captured.out
    assert product.link == "https://a.co/d/iWvWhnQ"
    assert product.name == "SG Ball"
    assert product.price == "$15"
    assert product.brand == "SG"

def test_get_by_name(monkeypatch, capsys):
    ecommerce.inventory = []
    monkeypatch.setattr(builtins, "input", lambda _: "SG Ball")
    ecommerce.get_by_name()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    ecommerce.inventory.append(dummy_product())
    monkeypatch.setattr(builtins, "input", lambda _: "Dummy Product")
    ecommerce.get_by_name()
    captured = capsys.readouterr()
    assert "\n\tid : 1,\n\tlink : https://dummy.link/product,\n\tname : Dummy Product,\n\tprice : $10,\n\tbrand : Dummy Brand,\n\tsource : N/A,\n" in captured.out

def test_get_all(monkeypatch, capsys):
    ecommerce.inventory = []
    ecommerce.get_all()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    ecommerce.inventory.append(dummy_product())
    ecommerce.get_all()
    captured = capsys.readouterr()
    assert "\n\tid : 1,\n\tlink : https://dummy.link/product,\n\tname : Dummy Product,\n\tprice : $10,\n\tbrand : Dummy Brand,\n\tsource : N/A,\n" in captured.out

def test_delete_product_by_id(monkeypatch,capsys):
    ecommerce.inventory = []
    inputs = iter(["1", "2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    ecommerce.inventory.append(dummy_product())
    inputs = iter(["1", "1", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.delete_product()
    captured = capsys.readouterr()
    print(repr(captured.out))
    assert "RESPONSE: Product deleted successfully." in captured.out
    assert len(ecommerce.inventory) == 0

def test_delete_product_by_name(monkeypatch, capsys):
    ecommerce.inventory = []
    ecommerce.inventory.append(dummy_product())
    inputs = iter(["2", "Dummy Product", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: Product deleted successfully." in captured.out
    assert len(ecommerce.inventory) == 0

    ecommerce.inventory.append(dummy_product())
    inputs = iter(["2", "Nonexistent Product", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: Invalid Product Name" in captured.out

    inputs = iter(["2", "Dummy Product", "n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: Product deletion cancelled." in captured.out

def test_clear_cart(monkeypatch, capsys):
    ecommerce.inventory = []
    ecommerce.clear_cart()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    ecommerce.inventory.append(dummy_product())
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.clear_cart()
    captured = capsys.readouterr()
    assert "RESPONSE: Cart clearing cancelled."

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.clear_cart()
    captured = capsys.readouterr()
    assert "RESPONSE: Cart cleared successfully."
    assert len(ecommerce.inventory) == 0

def test_exit_program(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    ecommerce.exit_program()
    captured = capsys.readouterr()
    assert "RESPONSE: Exit cancelled." in captured.out

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    monkeypatch.setattr(ecommerce, "save_inventory", lambda: None)
    with pytest.raises(SystemExit):
        ecommerce.exit_program()
    captured = capsys.readouterr()
    assert "RESPONSE: Exiting the program. Thank you!" in captured.out


def test_pretty_print(capsys):
    ecommerce.inventory = []
    ecommerce.pretty_print(ecommerce.inventory)
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    ecommerce.inventory = [dummy_product()]
    ecommerce.pretty_print(ecommerce.inventory)
    captured = capsys.readouterr()
    assert "\n\tid : 1,\n\tlink : https://dummy.link/product,\n\tname : Dummy Product,\n\tprice : $10,\n\tbrand : Dummy Brand,\n\tsource : N/A,\n" in captured.out

def test_del_confirmation(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    ans = ecommerce.del_confirmation()
    assert ans == False

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    ans = ecommerce.del_confirmation()
    assert ans == True
def test_exit_confirmation(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    ans = ecommerce.exit_confirmation()
    assert ans == False

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    ans = ecommerce.exit_confirmation()
    assert ans == True

def test_get_name(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "Tharun")
    name = ecommerce.get_name()
    assert name == "Tharun"

    monkeypatch.setattr(builtins, "input", lambda _: "  Jayanth  ")
    name = ecommerce.get_name()
    assert name == "Jayanth"

def test_get_source(monkeypatch):
   source =  ecommerce.get_source("https://a.co/d/cqSijmE")
   assert source == "a.co"