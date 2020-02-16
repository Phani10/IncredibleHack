"""
@author: Phani Kumar Koratamaddi
This script fetches business data, validates with the existing database and calculates whether
the business is eligible for loan or not
"""

from flask import Flask, request, render_template
from difflib import get_close_matches

import insert_to_mysql

app = Flask(__name__)


@app.route('/')
def message():
    """function to render html file"""
    return render_template('message.html')


def activity_factor(desc):
    """
    function to give importance to ACTIVITY DESCRIPTION column
    :parameter desc - Each row of ACTIVITY DESCRIPTION
    :returns - Factor to which it should effect loan eligibility scoring
    """

    if desc in ['Construction', 'Real Estate and Renting', 'Insurance']:
        return 1.1
    elif desc in ['Community, personal & Social Services', 'Agriculture and Allied Activities']:
        return 1.15
    elif desc in ['Transport, storage and Communications']:
        return 0.95
    elif desc in ['Trading', 'Finance']:
        return 0.9
    return 1


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    function that fetches data from html files, validates with the existing database and calculates
    whether the business is eligible for loan or not
    :parameter
     Business details like Company Name, Loan Amount, Loan Tenure in months, Surety amount
    :return - Success or failure message
    """

    if request.method == "POST":
        # Fetch details from HTML page
        # Do basic validations like a numeric column cannot be a string

        nm = request.form['nm']
        try:
            amt = request.form['amt']
            amt = int(amt)

            # Loan amount cannot be more than 10 crores
            if amt > 100000000:
                msg = "Loan cannot be sanctioned for more than 10 crores"
                return render_template('message.html', msg=msg)

        except ValueError:
            msg = "Please enter only numeric value for loan amount"
            return render_template('message.html', msg=msg)
        except TypeError:
            msg = "Please enter only numeric value for loan amount"
            return render_template('message.html', msg=msg)

        try:
            tenure = request.form['tenure']
            tenure = int(tenure)
            tenure = tenure/12
        except ValueError:
            msg = "Please enter only numeric value for tenure"
            return render_template('message.html', msg=msg)
        except TypeError:
            msg = "Please enter only numeric value for tenure"
            return render_template('message.html', msg=msg)

        try:
            surety = request.form['surety']
            surety = int(surety)
        except ValueError:
            msg = "Please enter only numeric value for surety"
            return render_template('message.html', msg=msg)
        except TypeError:
            msg = "Please enter only numeric value for surety"
            return render_template('message.html', msg=msg)

        # Take consent from the customer to approach bank for details
        value = request.form.getlist('consent')
        if len(value) == 0:
            msg = "Bank consent not provided"
            return render_template('message.html', msg=msg)

        # Fetch the existing details given by banks
        obj = insert_to_mysql.MysqlIo()
        df = obj.read_from_db()
        df.drop_duplicates(inplace=True)

        # Check if the company exists in our database. Else, send an error message
        nm = get_close_matches(nm.upper(), df['COMPANY NAME'])
        if len(nm) < 1:
            msg = "Sorry!! Company does not exist in our database"
            return render_template('message.html', msg=msg)
        nm = nm[0]

        # Calculate various factors for evaluation businesses
        df['score_calc'] = 0.717 * df['x1'] + 0.847 * df['x2'] + 0.42 * df['x4'] + 3.107 * df['x3'] + 0.998 * df['x5']
        df['factor'] = df['ACTIVITY DESCRIPTION'].apply(activity_factor)

        temp_df = df[df['COMPANY NAME'] == nm]
        if list(temp_df['COMPANY STATUS'])[0] == 'Not available for efiling':
            msg = "Sorry!! The company status is 'Not available for efiling'"
            return render_template('message.html', msg=msg)
        score = list(temp_df['score_calc'])[0]
        paid_up = list(temp_df['PAIDUP CAPITAL'])[0]
        factor = list(temp_df['factor'])[0]
        turn_over = list(temp_df['TURN OVER'])[0]

        # Calculate Eligibility amount and Loan Requirement
        eligible_amount = ((turn_over*0.1) + (score*25000) + surety)
        loan_req = (paid_up + (amt/tenure))*factor

        # Based on eligible amount and loan amount, decide if the business should be approved loan or not
        flag = 'Loan Approved'
        if eligible_amount < loan_req:
            flag = 'Loan Rejected'
    else:
        flag = 'Site is not secure'

    # Return the loan status message
    return flag


if __name__ == "__main__":
    app.run()
