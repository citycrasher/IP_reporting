from flask import Flask, request, render_template, redirect, url_for
import logging
import api, settings
app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='api.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/')
def index():
    status = request.args.get('status')
    return render_template('form.html', status=status)

def call_api(owner_name, original_type, original_work_url, message, infringing_url):
    access_token = ("EAANNzoa1UqQBO0EZAZB1ZAgrMNz483f3EoMUGTruA3m5d85qm55cK15cuTXieKRX6E6gz8bfEZBzmJRZARZB8SmZC1Y9YyGVixZCBit3SUuZAKkCJrQBM6p6ofLbunIdkvl1FKHWeDG3xUc5aA1NsfLvsXKvjRElCminjeFPXfWIEypFI41xgyeoYPxEWoAZDZD")
    email = settings.bx_legal_email
    job = "TEST"
    #job = "Legal Operations"
    name = settings.bx_name
    owner_country = "IN"  # IN-india,
    owner_name = owner_name  # client name
    relationship = "AGENT"  # OWNER, COUNSEL, EMPLOYEE, AGENT, OTHER
    type = "COPYRIGHT"  # COPYRIGHT, TRADEMARK, COUNTERFEIT
    content_urls = infringing_url
    organization = settings.bx_name
    address = settings.bx_address
    original_urls = original_work_url
    additional_info = message
    data = api.get_data(access_token=access_token, email=email, job=job, name=name, original_type=original_type,
                        owner_country=owner_country, owner_name=owner_name, relationship=relationship, type=type,
                        organization=organization, address=address, original_urls=original_urls,
                        content_urls=content_urls, additional_info=additional_info)

    response = api.make_request(data)

    return response



@app.route('/submit', methods=['POST'])
def submit():
    urls = str(request.form['infringing_url']).split()
    original_type = str(request.form['original_type'])
    original_work_url = str(request.form['original_url'])
    message = str(request.form['message'])
    infringing_url = str(request.form['infringing_url'])
    owner_name = str(request.form['owner_name'])

    # Log the form data
    #response = call_api(raw_urls=urls)
    response = call_api(owner_name=owner_name, original_type=original_type,
                        original_work_url=original_work_url, message=message, infringing_url=infringing_url)
    if type(response) == str:
        app.logger.info('++++++ URLS: %s', urls)
        app.logger.info('++++++ ERROR: %s', response)
        status = "error"
    else:
        app.logger.info('++++++ URLS: %s', urls)
        app.logger.info('++++++ status code: %s, json_resp: %s', response.status_code, response.json())
        status = "success"
    return redirect(url_for('index' , status=status))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
