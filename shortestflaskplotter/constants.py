"""
This module manages the constants of the tool.
"""

import os

UPLOAD = "UPLOAD_FOLDER"
IMAGE = "IMAGE_FOLDER"
UPLOAD_FOLDER = os.path.join('static', 'Images')
IMAGE_FOLDER = os.path.join('static', 'Images')
POST = "POST"
GET = "GET"
VALID_JSON_FIELD = ["node_names", "node_coordinates", "weights_node_coordinates"]
INVALID_START_END_NODE = "Please provide a valid Source and Target nodes."
INVALID_TYPE = "The selected file is not of type JSON."
INVALID_JSON_FILE = "The JSON file selected is not a valid JSON file."
INVALID_FIELDS_IN_JSON = f"The expected fields in the JSON are {VALID_JSON_FIELD}"
NO_FILE_FOUND = "No File Selected"
START_NODE_END_NODE_INVALID = "The start node or end node provided is incorrect."
JSON_PATH_PROVIDED_IS_NOT_VALID = "The data provided in the input json file is not as expected."
NO_PATH_EXISTS_BETWEEN_NODE = "There are no connected path between start and end nodes."
