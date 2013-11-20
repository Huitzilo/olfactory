#!/usr/bin/env python
# encoding: utf-8
'''
'''
from flask import Flask, request, Response, render_template, json
from werkzeug.utils import secure_filename
import core
import os
import csv
import numpy as np

UPLOAD_FOLDER = './results'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
  """
  Show the start page of the app.
  """
  return render_template("index.html")


@app.route("/fs/")
def feature_selection():
  """
  Render the page for feature selection.
  A user must upload a *.csv file, select a method and define the number features required
  """
  return render_template('feature_selection_upload.html')


@app.route("/fs/upload", methods=["POST"])
def feature_selection_upload():
  """
  Upload a *.csv file to the server and return a job id.
  """
  if request.method == 'POST':
    try:
      f = request.files['file']
      if f and core.allowed_file(f.filename):
        # save csv to server in new results/<id>
        job_id = core.get_job_id()
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], str(job_id))
        os.makedirs(save_path)
        f.save(os.path.join(save_path, "data.csv"))

        #read the csv to present information in client
        path_to_csv = os.path.join(save_path, "data.csv")
        d = []
        with open(path_to_csv) as csvfile:
          reader = csv.reader(csvfile, delimiter=',')

          for row in reader:
            d.append(row)

        d = np.asarray(d)
        response = np.asarray(d[1:, 1:])
        data_names = d[0, :]
        feature_names = d[:, 0]

        js = [{"job_id": job_id, "number_data": response.shape[0], "number_features": response.shape[1],
               "data_names": data_names.tolist(), "feature_names": feature_names.tolist(), }]
        return Response(json.dumps(js), mimetype='application/json', status=200)
    except:
      return Response(response="Upload failed", status=400)


@app.route("/fs/results/<job_id>", methods=["GET", "DELETE"])
def results(job_id=None):
  if request.method == 'GET':
    path = os.path.join(app.config['UPLOAD_FOLDER'], str(job_id), "data.csv")
    d = []
    with open(path) as csvfile:
      reader = csv.reader(csvfile, delimiter=',')

      for row in reader:
        d.append(row)

    d = np.asarray(d)
    response = np.asarray(d[1:, 1:])
    data_names = d[0, :]
    feature_names = d[:, 0]

    return render_template("results.html", items=data_names)
  elif request.method == 'DELETE':
    path = os.path.join(app.config['UPLOAD_FOLDER'], str(job_id))
    os.rmdir(path)
    return "Deleted Job Id: %i" % int(job_id)
  pass


if __name__ == '__main__':
  app.run(debug=True)