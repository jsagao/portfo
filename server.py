from flask import Flask, render_template, url_for, request, redirect
import csv
import smtplib
from email.message import EmailMessage
from string import Template


app = Flask(__name__)

print(__name__)

if __name__ == '__main__':
    app.run()

@app.route('/')
# check this it was '/' before 
def my_home():
    return render_template('/index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email_msg = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email_msg, subject, message])


email = EmailMessage()


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        # data = request.form['email', 'password']
        data = request.form.to_dict()
        write_to_csv(data)
        email['from'] = request.form.get('name')
        email['to'] = 'james@omegadivision.com'
        email['subject'] = request.form.get('email')
        email.set_content(request.form.get('message'))
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('james.agao@gmail.com', 'unpeykbedtzgiqus')
            smtp.send_message(email)
            print('all good boss!')
        return redirect('/thankyou.html')
    else:
        return 'something went wrong. Try again!'


# @app.route('/works.html')
# def works():
#     return render_template('/works.html')


# @app.route('/work.html')
# def work():
#     return render_template('/work.html')


# @app.route('/work2.html')
# def work2():
#     return render_template('/work2.html')


# @app.route('/about.html')
# def about():
#     return render_template('/about.html')


# @app.route('/contact.html')
# def contact():
#     return render_template('/contact.html')
