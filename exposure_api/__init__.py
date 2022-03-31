from exposure_api.util import *
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import os
import logging
logging.basicConfig(filename='exposure_api.log', level=logging.DEBUG)


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    db_file_name = os.path.join(app.instance_path, 'dashboard_request.json')
    building_exposure_map = get_building_exposure_map(app.instance_path)
    logging.debug('app started! ' + os.getcwd())

    @app.route('/record_request_info', methods=['GET'])
    def record_request_info():
        error, log = get_value_from_request(request, 'log')
        if error:
            logging.debug('no log provided in the request')
            return make_response({"message": "no log provided in the request!"}, 400)

        logging.debug('writing log to file...')
        write_json(log, db_file_name)
        return make_response({"message": "successful log!"})

    @app.route('/update_building_exposure_map')
    def update_building_exposure_map():
        nonlocal building_exposure_map
        building_exposure_map = get_building_exposure_map(app.instance_path)
        return make_response(jsonify({"exposure_map": building_exposure_map}))

    @app.route('/get_exposure_dates_for_building', methods=['GET'])
    def get_exposure_dates_for_building():
        error, caan = get_value_from_request(request, 'caan')
        if error:
            logging.debug('no caan provided in the request')
            return make_response({"message": "no caan provided in the request!"}, 400)

        if caan not in building_exposure_map:
            logging.debug('provided caan is invalid')
            return make_response({"message": "provided caan is invalid"}, 400)

        logging.debug(f"caan: {caan}, exposure: {building_exposure_map[caan]}")
        return make_response(jsonify({"exposure_dates": building_exposure_map[caan]}))

    return app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = b"\xb7\xe2\xd6\xa3\xe2\xe0\x11\xd1\x92\xf1\x92G&>\xa2:"
    app.debug = True
    app.run(host="0.0.0.0", port=5343)
