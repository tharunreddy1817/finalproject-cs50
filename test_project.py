import pytest 
import builtins
import project 

def dummy_product():
    return project.Product(
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
        project.main()
    captured = capsys.readouterr()
    assert "RESPONSE: Invalid menu selection.\nPlease try again." in captured.out
    assert "RESPONSE: Exiting the program. Thank you!" in captured.out
    
def test_add_product(monkeypatch, capsys):
    inputs = iter(["https://a.co/d/cqSijmE", "Cricket Ball", "$","20", "Dukes"])

    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.add_product()
    product = project.inventory[-1]  
    captured = capsys.readouterr()
    assert "RESPONSE: Product added successfully." in captured.out
    assert product.name == "Cricket Ball"
    assert product.price == "$20"
    assert product.brand == "Dukes"
    assert product.link == "https://a.co/d/cqSijmE"

def test_update_product_with_empty_list(monkeypatch, capsys):
    project.inventory = []
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.update_product()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

def test_update_product_with_existing_product_id(monkeypatch, capsys):

    inputs = iter(["https://a.co/d/cqSijmE", "Cricket Ball", "$","20", "Dukes"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.add_product()

    inputs = iter(["1","-1",project.inventory[-1].id,"", "New Cricket Ball", "$","25", "New Dukes"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.update_product()

    product = project.inventory[-1]
    captured = capsys.readouterr()
    assert "RESPONSE: Invalid Product ID. Please try again." in captured.out
    assert "RESPONSE: Product updated successfully." in captured.out
    assert product.name == "New Cricket Ball"
    assert product.price == "$25"
    assert product.brand == "New Dukes"

def test_update_product_with_invalid_product_name(monkeypatch, capsys):
    inputs = iter(["2","","Jai Balayya", "New Cricket Ball","https://a.co/d/iWvWhnQ","SG Ball", "$", "15", "SG"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.update_product()
    product = project.inventory[-1]
    captured = capsys.readouterr()
    
    assert "RESPONSE: Product name cannot be empty. Please try again." in captured.out
    assert "+++ You have selected product with name: Jai Balayya" in captured.out
    assert "RESPONSE: Invalid Product name" in captured.out

def test_update_product_with_valid_product_name(monkeypatch, capsys):
    inputs = iter(["2", "New Cricket Ball","https://a.co/d/iWvWhnQ","SG Ball", "$", "15", "SG"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.update_product()
    product = project.inventory[-1]
    captured = capsys.readouterr()
    assert "RESPONSE: Product updated successfully." in captured.out
    assert product.link == "https://a.co/d/iWvWhnQ"
    assert product.name == "SG Ball"
    assert product.price == "$15"
    assert product.brand == "SG"

def test_get_by_name(monkeypatch, capsys):
    project.inventory = []
    monkeypatch.setattr(builtins, "input", lambda _: "SG Ball")
    project.get_by_name()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    project.inventory.append(dummy_product())
    monkeypatch.setattr(builtins, "input", lambda _: "Dummy Product")
    project.get_by_name()
    captured = capsys.readouterr()
    assert "\n\tid : 1,\n\tlink : https://dummy.link/product,\n\tname : Dummy Product,\n\tprice : $10,\n\tbrand : Dummy Brand,\n\tsource : N/A,\n" in captured.out

def test_get_all(monkeypatch, capsys):
    project.inventory = []
    project.get_all()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    project.inventory.append(dummy_product())
    project.get_all()
    captured = capsys.readouterr()
    assert "\n\tid : 1,\n\tlink : https://dummy.link/product,\n\tname : Dummy Product,\n\tprice : $10,\n\tbrand : Dummy Brand,\n\tsource : N/A,\n" in captured.out

def test_delete_product_by_id(monkeypatch,capsys):
    project.inventory = []
    inputs = iter(["1", "2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    project.inventory.append(dummy_product())
    inputs = iter(["1", "1", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.delete_product()
    captured = capsys.readouterr()
    print(repr(captured.out))
    assert "RESPONSE: Product deleted successfully." in captured.out
    assert len(project.inventory) == 0

def test_delete_product_by_name(monkeypatch, capsys):
    project.inventory = []
    project.inventory.append(dummy_product())
    inputs = iter(["2", "Dummy Product", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: Product deleted successfully." in captured.out
    assert len(project.inventory) == 0

    project.inventory.append(dummy_product())
    inputs = iter(["2", "Nonexistent Product", "y"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: Invalid Product Name" in captured.out

    inputs = iter(["2", "Dummy Product", "n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.delete_product()
    captured = capsys.readouterr()
    assert "RESPONSE: Product deletion cancelled." in captured.out

def test_clear_cart(monkeypatch, capsys):
    project.inventory = []
    project.clear_cart()
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    project.inventory.append(dummy_product())
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.clear_cart()
    captured = capsys.readouterr()
    assert "RESPONSE: Cart clearing cancelled."

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.clear_cart()
    captured = capsys.readouterr()
    assert "RESPONSE: Cart cleared successfully."
    assert len(project.inventory) == 0

def test_exit_program(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    project.exit_program()
    captured = capsys.readouterr()
    assert "RESPONSE: Exit cancelled." in captured.out

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    monkeypatch.setattr(project, "save_inventory", lambda: None)
    with pytest.raises(SystemExit):
        project.exit_program()
    captured = capsys.readouterr()
    assert "RESPONSE: Exiting the program. Thank you!" in captured.out


def test_pretty_print(capsys):
    project.inventory = []
    project.pretty_print(project.inventory)
    captured = capsys.readouterr()
    assert "RESPONSE: No items in Cart" in captured.out

    project.inventory = [dummy_product()]
    project.pretty_print(project.inventory)
    captured = capsys.readouterr()
    assert "\n\tid : 1,\n\tlink : https://dummy.link/product,\n\tname : Dummy Product,\n\tprice : $10,\n\tbrand : Dummy Brand,\n\tsource : N/A,\n" in captured.out

def test_del_confirmation(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    ans = project.del_confirmation()
    assert ans == False

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    ans = project.del_confirmation()
    assert ans == True
def test_exit_confirmation(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "n")
    ans = project.exit_confirmation()
    assert ans == False

    monkeypatch.setattr(builtins, "input", lambda _: "y")
    ans = project.exit_confirmation()
    assert ans == True

def test_get_name(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "Tharun")
    name = project.get_name()
    assert name == "Tharun"

    monkeypatch.setattr(builtins, "input", lambda _: "  Jayanth  ")
    name = project.get_name()
    assert name == "Jayanth"

def test_get_source(monkeypatch):
   source =  project.get_source("https://a.co/d/cqSijmE")
   assert source == "a.co"