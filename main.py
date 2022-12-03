from flask import Flask, render_template, Response, request
from cv import CameraFeed

app = Flask(__name__)
cam = CameraFeed(
    frameResizeFactor=0.9,
    videoFormat="raw",
    showContours=False,
    camera=0
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
      point = request.get_json()
      cam.setPoints(point['x'], point['y'])
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(cam.getFrames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/dev", methods=["GET", "POST"])
def dev():
    return render_template("dev.html")

if __name__ == "__main__":
    app.run(debug=True)
