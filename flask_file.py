"""
This module mamages the UI component of the tool. This module initiates the JSON cleanup and generation of output map plot
"""
import json
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from shortestflaskplotter import constants
from shortestflaskplotter.shortest_path import QuickWayFinder

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def allowed_file(filename):
    """
    This method validates the file name.

    :param filename: filename
    :return: True/False
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'json'


def validate_json(jsonfile):
    """
    This method produces JSON dumps from the input file provides. This method also validates the json file.

    :param jsonfile: Json File Name
    :return: True/False, json dumps
    """
    try:
        with open(jsonfile, 'r') as json_data:
            data = json.load(json_data)
    except ValueError as err:
        return False, {}
    return True, data


def validate_json_path(filename, request):
    """
    This method performs validation for the tool.

    :param filename: input file path
    :param request: user requests
    :return: Error Msg
    """
    msg = ""
    if not filename:
        msg = constants.NO_FILE_FOUND
    elif not request.form['start_node'] or not request.form['target_node']:
        msg = constants.INVALID_START_END_NODE
    elif filename and not allowed_file(filename):
        msg = constants.INVALID_TYPE
    if not msg:
        absolute_file_path = os.path.join(app.config[constants.UPLOAD], filename)
        success_validate, json_dump = validate_json(absolute_file_path)
        if not success_validate:
            msg = constants.INVALID_JSON_FILE
        elif set(json_dump.keys()) != set(constants.VALID_JSON_FIELD):
            msg = constants.INVALID_FIELDS_IN_JSON
        elif (request.form['start_node'] not in list(json_dump['node_names'].values())) or (
                request.form['target_node'] not in list(json_dump['node_names'].values())):
            msg = constants.START_NODE_END_NODE_INVALID
    return msg


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
        if validate_json_path(filename, request):
            return validate_json_path(filename, request)
        try:
            absolute_file_path = os.path.join(app.config[constants.UPLOAD], filename)
            f.save(absolute_file_path)
            quick_way_finder = QuickWayFinder(request.form['start_node'], request.form['target_node'],
                                              absolute_file_path)
            if not quick_way_finder.traversed_path:
                return constants.NO_PATH_EXISTS_BETWEEN_NODE
            plotter_image_path = os.path.join(app.config[constants.IMAGE], 'plotter.jpg')
            if os.path.exists(plotter_image_path):
                os.remove(plotter_image_path)
            quick_way_finder.plt.savefig(plotter_image_path)
            shortest_path = f"The path traversed is {quick_way_finder.traversed_path} and total distance is {quick_way_finder.distance}"
            return render_template("index.html", user_image=plotter_image_path, header_info=shortest_path)
        except Exception as e:
            return constants.JSON_PATH_PROVIDED_IS_NOT_VALID


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
