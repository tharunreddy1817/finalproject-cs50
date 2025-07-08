import pytest # type: ignore
import builtins
import ecommerce # type: ignore

def test_main(monkeypatch, capsys):
    inputs = iter(["1","9"])
    monkeypatch.setattr(builtins, 'input', lambda _: next(inputs))

    ecommerce.main()
    captured = capsys.readouterr()
    assert "RESPONSE: Product added successfully." in captured.out
    assert "RESPONSE: Invalid menu selection.\nPlease try again." in captured.out
    
    
