"""
This module mamages the UI component of the tool. This module initiates the JSON cleanup and generation of output map plot
"""
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from shortestpathgraphplotter import constants
from shortestpathgraphplotter.shortest_path import QuickWayFinder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("flask.html")


@app.route('/json_uploader', methods=[constants.GET, constants.POST])
def upload_file():
    """
    This method allows users to upload the JSON file and generates the output HMTL report showing the shortest path between nodes.

    :return: HTML Report
    """

    app.config[constants.UPLOAD] = constants.UPLOAD_FOLDER
    app.config[constants.IMAGE] = constants.IMAGE_FOLDER
    if request.method == constants.POST:
        f = request.files['file']
        filename = secure_filename(f.filename)
        absolute_file_path = os.path.join(app.config[constants.UPLOAD], filename)
        f.save(absolute_file_path)
        quick_way_finder = QuickWayFinder('F', 'H', absolute_file_path)
        plotter_image_path = os.path.join(app.config[constants.IMAGE], 'plotter.jpg')
        if os.path.exists(plotter_image_path):
            os.remove(plotter_image_path)
        quick_way_finder.plt.savefig(plotter_image_path)
        shortest_path = f"The path traversed is {quick_way_finder.traversed_path} and total distance is {quick_way_finder.distance}"
        return render_template("index.html", user_image=plotter_image_path, header_info=shortest_path)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
