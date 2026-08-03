from flask import Flask, request
import os

app = Flask(__name__)

APP_TITLE = os.getenv("APP_TITLE", "Calculator App")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")


@app.route("/health")
def health():
    return "OK", 200

@app.route("/")
def home():
    return f"""
    <h1>{APP_TITLE}</h1>
    <h3>Environment: {ENVIRONMENT}</h3>

    <form action="/calculate" method="get">
        Number 1: <input type="number" name="a"><br><br>

        Number 2: <input type="number" name="b"><br><br>

        <select name="operation">
            <option value="add">Add</option>
            <option value="sub">Subtract</option>
            <option value="mul">Multiply</option>
            <option value="div">Divide</option>
        </select>

        <br><br>

        <input type="submit" value="Calculate">
    </form>
    """

@app.route("/calculate")
def calculate():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    operation = request.args.get("operation")

    if operation == "add":
        result = a + b

    elif operation == "sub":
        result = a - b

    elif operation == "mul":
        result = a * b

    elif operation == "div":
        if b == 0:
            return "Cannot divide by zero"

        result = a / b

    else:
        return "Invalid operation"

    return f"""
    <h2>Result: {result}</h2>

    <a href="/">Go Back</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
