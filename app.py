#!/usr/bin/env python
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__,
             template_folder='web/dcu.ca2/webapp')

@app.route("/")
def hello():
  message = "Hello, World"
  return render_template("index-cdn.html", message=message)

@app.route('/<path:filename>')
def serve_static_file(filename):
    static_dir = os.path.join(app.root_path, 'web/dcu.ca2/webapp')
    return send_from_directory(static_dir, filename)

if __name__ == "__main__":
  app.run(debug=True)