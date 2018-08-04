from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    title = "Kyori Application Portal"
    return render_template("index.html", title=title)

@app.route("/regulusaurum", methods=["GET"])
def regulusaurum():
    title = "EasyTootSaver ~獅子の黄金~"
    return render_template("regulusaurum.html", title=title)

@app.route("/profile", methods=["GET"])
def profile():
    title = "About きょり/わんせた"
    return render_template("profile.html", title=title)

if __name__ == "__main__":
    app.run(host="localhost", port=1443)
