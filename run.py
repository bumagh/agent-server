#!flask/bin/python
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(6666)
    app.run(port=port, debug=True)
    # app.run(port=port)
