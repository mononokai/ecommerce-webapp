from flask import Flask

app = Flask(__name__)

# API Route
@app.route("/test_list/")
def test_list():
    return {"test_list": ["item1", "item2", "item3"]}


if __name__ == "__main__":
    app.run(debug=True)

