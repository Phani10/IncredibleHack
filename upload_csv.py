"""
@author: Phani Kumar Koratamaddi
This script is to fetch csv files and store it in mysql db
"""

from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename
import pandas as pd

import insert_to_mysql

app = Flask(__name__)


@app.route('/')
def index():
    """function to render html file"""
    return render_template('message.html')


@app.route('/uploader', methods=['POST'])
def upload():
    """
    function to save the csv file uploaded in html page to mysql df
    :parameter
     csv file
    :return success or failure message back to the user
    """
    if request.method == 'POST':
        files = request.files['file']
        # files.save('test.csv')
        data = pd.read_csv(files)

        obj = insert_to_mysql.MysqlIo()
        msg = obj.write_to_db(data)

        return render_template('message.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
