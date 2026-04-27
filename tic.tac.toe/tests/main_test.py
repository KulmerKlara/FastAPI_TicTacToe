from app.main import create_app

def test_app_creation():
    app = create_app()
    assert app.title == "TicTacToe API"



def test_routes_exist():
    app = create_app()
    routes = [route.path for route in app.routes]

    assert any("/" in r or "/api" in r for r in routes)