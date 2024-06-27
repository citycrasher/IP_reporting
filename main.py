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

def call_api(raw_urls):
    movie_name = "Kalki 2898 AD (2024)"
    access_token = (
        "EAANNzoa1UqQBO8aDlZAURIjz05ep75yJrAeZA6w8Hcd38g5ZAKYEtwyTsg0hroUpnGhQ5ZBwGBIZC9gHhwGQaZAc0g6Ce6LPBbiuWv2ZAVLjuacEZCadzIb6rzTwi83ZA3PIwsfEpmO2gsPTZBEqSLy0dn08IVZB1DaDaZBZBCiufpPjFRvKf8y2o3rihZBEZBG7QZDZD")
    email = settings.bx_legal_email
    job = "Legal Operations"
    name = settings.bx_name
    original_type = "VIDEO"  # PHOTO, VIDEO, ARTWORK, SOFTWARE, NAME, CHARACTER, OTHER
    owner_country = "IN"  # IN-india,
    owner_name = "Vyjayanthi Movies"  # client name
    relationship = "AGENT"  # OWNER, COUNSEL, EMPLOYEE, AGENT, OTHER
    type = "COPYRIGHT"  # COPYRIGHT, TRADEMARK, COUNTERFEIT
    content_urls = raw_urls
    organization = settings.bx_name
    address = settings.bx_address
    original_urls = ["https://www.youtube.com/watch?v=kQDd1AhGIHk", "https://www.imdb.com/title/tt12735488/",
                     "https://en.wikipedia.org/wiki/Kalki_2898_AD"]

    additional_info = api.get_additional_info(movie_name)

    data = api.get_data(access_token=access_token, email=email, job=job, name=name, original_type=original_type,
                        owner_country=owner_country, owner_name=owner_name, relationship=relationship, type=type,
                        organization=organization, address=address, original_urls=original_urls,
                        content_urls=content_urls, additional_info=additional_info)

    response = api.make_request(data)

    return response



@app.route('/submit', methods=['POST'])
def submit():
    urls = str(request.form['ip_url']).split()
    if len(urls) > 0:
      # Log the form data
      response = call_api(raw_urls=urls)
      if type(response) == str:
          app.logger.info('++++++ URLS: %s', urls)
          app.logger.info('++++++ ERROR: %s', response)
          status = "error"
      else:
          app.logger.info('++++++ URLS: %s', urls)
          app.logger.info('++++++ status code: %s, json_resp: %s', response.status_code, response.json())
          status = "success"
    else:
        status = "blank entry"
  return redirect(url_for('index' , status=status))


if __name__ == '__main__':
    # app.run(debug=True, port=8001)
    app.run(debug= True, host='0.0.0.0', port=8001)
