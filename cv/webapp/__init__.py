import os

from cv.webapp.application import app

def run(host="0.0.0.0", port="5000", debug=True):
  if debug:
    os.environ["FLASK_ENV"] = "development"
  app.run(host=host, port=port, debug=debug)
