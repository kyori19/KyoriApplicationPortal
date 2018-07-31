from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    title = "Kyori Application Portal"
    return render_template("index.html", title=title)


if __name__ == "__main__":
    app.run(host="localhost", port=1443)
