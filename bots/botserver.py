import logging
import os
import threading
import subprocess
import json
import atexit

from bots import RedditStreamer

from flask import Flask
from flask_restful import Resource, Api, reqparse

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)

# BOT_SERVER_PORT = os.environ['PORT']

LIVEBOTS = {}


def cleanup():
    for bot_id, bot in LIVEBOTS.items():
        bot_desc = bot["desc"]
        logging.warning(f"Terminating LIVEBOT on Exit: {bot_id}: {bot['desc']}")
        kill_process(LIVEBOTS, bot_id)


def kill_process(dictionary, process_id):
    pid = int(process_id)
    bot = dictionary[process_id]["process"]
    bot.terminate()



atexit.register(cleanup)

# -----------------------#
class LiveBots(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("source", choices=("reddit"), required=True)
    parser.add_argument("query", required=True)
    # TODO: Generate these based on available models maybe?
    parser.add_argument(
        "analyzer_settings", choices=("dummy"), required=True
    )  # ,'simpleBERT'))

    def get(self):
        return {bot_id: bot["desc"] for bot_id, bot in LIVEBOTS.items()}, 200

    def post(self):
        args = self.parser.parse_args()

        # TODO: Could probably use some error handling here
        popen_args = self._parse_start_bot_params(args)
        bot_description = self._get_bot_description(args)
        process = subprocess.Popen(popen_args)

        process_id = process.pid
        LIVEBOTS[str(process_id)] = {"process": process, "desc": bot_description}

        return process_id, 201  # TODO: Double check this is best practice

    def _parse_start_bot_params(self, args):
        popen_args = []
        if args.source == "reddit":
            bot_type = "reddit_streamer"

        if args.analyzer_settings == "dummy":
            analyzer = "DummyAnalyzer"

        query = args.query

        popen_args = [
            "python3",
            "start_bot.py",
            "--bot_type",
            bot_type,
            "--query",
            query,
            "--analyzer",
            analyzer,
        ]
        return popen_args

    def _get_bot_description(self, args):
        desc = f"{args.source}|{args.analyzer_settings}|{args.query}"
        return desc


class LiveBot(Resource):
    def delete(self, name):
        if name not in LIVEBOTS:
            return {"message": f"Bot ID Not Found: {name}"}, 404
        else:
            logging.info(f"Killing Process: {name}")
            kill_process(LIVEBOTS, name)
            del LIVEBOTS[name]
            return {"message": "Bot Killed"}, 202


api.add_resource(LiveBots, "/livebots")
api.add_resource(LiveBot, "/livebot/<string:name>")


if __name__ == "__main__":
    app.run(port=10555, debug=True)
