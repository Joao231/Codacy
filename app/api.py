import sys
sys.path.append("..")
from flask import Flask, jsonify, request, abort
from wrapper.wrapper import GitWrapper 
from prometheus_flask_exporter import PrometheusMetrics
import logging


logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")



@app.route('/list-commits', methods=['GET'])
def list_commits():

    github_url = request.args.get('url')

    if not github_url:
        # Return 400 Bad Request if URL parameter is missing
        abort(400)
    
    git_wrapper = GitWrapper(github_url)

    commit_list = git_wrapper.list_commits()
    
    if isinstance(commit_list, tuple):
        if commit_list[1] == 404:
            abort(404)
        abort(500)
    else:
        return jsonify({'commits': commit_list}), 200


@app.errorhandler(400)
def not_found_error(error):
    return jsonify({'error': 'URL parameter is required', 'status_code': 400}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found', 'status_code': 404}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'status_code': 500}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)