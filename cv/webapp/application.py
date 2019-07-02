import toml

from flask import Flask, render_template
from flask_weasyprint import render_pdf, HTML
from pathlib import Path

PATH_ROOT = Path(__file__).resolve().parent

app = Flask(__name__)


def save_pdf(html, path):
  obj_html = HTML(string=html)
  data_pdf = obj_html.write_pdf()
  with open(path, 'wb') as fh:
    fh.write(data_pdf)


@app.route('/')
def cv():
  data_cv = toml.load(Path(PATH_ROOT, "static", "data.toml"))

  # Sort the dates in data.main.values in descending order.
  for key, values in data_cv['main'].items():
    sorted_dates = []
    if type(values) == dict:
      for location, list_dict in values.items():
        for dic in list_dict:
          if dic.get('title'): # Check if work-related.
            sorted_dates.append((
              location,
              dic['start'],
              dic['end'],
              dic['title'],
              dic['type'],
              dic['description']
            ))
          elif dic.get('years'):
            sorted_dates.append((
              location,
              dic['start'],
              dic['end'],
              dic['years'],
              dic['description']
            ))
        if sorted_dates:
          data_cv['main'][key] = list(reversed(sorted(sorted_dates, key=lambda x: x[1])))

  html = render_template("cv.html", data=data_cv, css=['cv'])
  html_pdf = render_template("cv.html", data=data_cv, css=['cv', 'cv_pdf'])
  save_pdf(html_pdf, "cv.pdf")
  return html
