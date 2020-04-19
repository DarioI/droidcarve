# This file is part of DroidCarve.
#
# Copyright (C) 2019, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#
__author__ = "Dario Incalza <dario.incalza@gmail.com"
__copyright__ = "Copyright 2020, Dario Incalza"
__maintainer__ = "Dario Incalza"
__email__ = "dario.incalza@gmail.com"

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import utils, os, tempfile, logging
from droidcarve import AnalysisController, DeviceController
from werkzeug.utils import secure_filename

UPLOAD_DIR = tempfile.mkdtemp()
app = Flask("DroidCarve API")
CORS(app)

analysisController = AnalysisController()
deviceController = DeviceController()


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'running', 'version': '0.0.1'})


@app.route('/status', methods=['GET'])
def status():
    return {
        "device": deviceController.get_device()['device'],
        "application": analysisController.get_application()['application']
    }


@app.route('/device/', methods=['GET'])  # get info
@app.route('/device/<action>', methods=['GET', 'POST'])  # perform action on device
def device(action=None):
    try:
        if not action:
            return jsonify(deviceController.get_device()), 200
        if action == "list":
            return jsonify(deviceController.get_device_list()), 200

        if action == "connect":

            if not request.json['serial']:
                return jsonify({'error': 'DEVICE_SERIAL_MISSING'}), 400
            serial = request.json['serial']
            device_info = deviceController.connect_device(serial)

            if not device_info:
                return jsonify({'error': 'DEVICE_CONNECTION_ERROR'}), 400
            else:
                return jsonify(device_info), 200
        else:
            return "", 404

    except AttributeError:
        return jsonify({'error': 'GENERAL_ERROR'}), 400


@app.route('/app/', methods=['GET'])  # get info
@app.route('/app/<action>', methods=['GET', 'POST', 'OPTIONS'])  # perform action on application
def application(action=None):
    if request.method == 'OPTIONS':
        return "", 200

    try:
        if not action:
            return jsonify(analysisController.get_application())

        elif action == "upload":
            file = request.files['file']
            if file and file.filename.rsplit('.', 1)[1].lower() == 'apk':
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_DIR, filename)
                file.save(file_path)
                analysisController.set_application(file_path)
                return "", 200

        elif action == "stats":
            return jsonify(analysisController.get_statistics()), 200

        else:
            return "", 404

    except AttributeError:
        return jsonify({'error': 'APPLICATION_NOT_SET'}), 400
    except TypeError:
        return jsonify({'error': 'NON_VALID_APK'}), 400


@app.route('/source/<action>', methods=['GET', 'POST', 'OPTIONS'])
def source(action=None):
    if request.method == 'OPTIONS':
        return "", 200

    if action == "tree":
        return analysisController.get_source_tree(), 200


@app.route('/file/<action>/<key>', methods=['GET', 'POST', 'OPTIONS'])
def file(action=None, key=None):
    if action == "download":
        if not key:
            return jsonify({'error': "NO_FILE_KEY"}), 400
        try:
            filepath = analysisController.get_source_file_path(key)
            return send_file(filepath, as_attachment=True)
        except FileNotFoundError:
            return jsonify({'error': "FILE_NOT_FOUND"}), 404
        except AttributeError:
            return jsonify({'error': 'APPLICATION_NOT_SET'}), 400


@app.route('/manifest/<action>', methods=['GET'])
def manifest(action):
    if action == "view":
        manifest_xml = analysisController.get_manifest_source()
        return jsonify({'xml': manifest_xml.decode("utf-8")}), 200

    if action == "overview":
        return jsonify(analysisController.get_manifest_overview()), 200

    return jsonify({}), 404


@app.route('/login')
def login():
    return 'login'


def main():
    set_logging()
    app.run(host="127.0.0.1", port=1337)


def set_logging():
    import logging
    logging.basicConfig(level=logging.ERROR)


if __name__ == "__main__":

    if not utils.has_baksmali():
        logging.error("[!!!] - no baksmali binary found - exiting.")
        exit(2)

    if not utils.adb_available():
        logging.error("[!!!] ADB not found. Features that need a connected Android device won't work. Please "
                        "install ADB before using DroidCarve.")
    main()
