from flask import Flask, render_template, request, redirect, jsonify
# from database.db_connector import connect_to_database, execute_query
import os
import requests
from requests.sessions import session
from gmaps_scraper import WebDriver

# Configuration
app = Flask(__name__)

#global variable to store service choice
service_type = ''
zipcode_input = ''


# Routes 
@app.route('/')
def root():
	'''Return the homepage'''
	print('Root index hit. Redirecting to index.html...')
	return redirect('/index')

@app.route('/index')
def index():
    '''True URL of homepage'''
    print('Welcome to the homepage.')
    return render_template('index.html')

@app.route('/service_submission', methods=['POST'])
def service_submit():
	global service_type
	service_type = request.form["serviceType"]
	print("Service chosen =", service_type)
	print(service_type)
	return render_template('zipcode.html')

@app.route('/service_submission_adv')
def service_submit_adv():
	return render_template('zipcode _adv.html')

@app.route('/zipcode_submission', methods=['POST'])
def zipcode_submit():
	global service_type
	global zipcode_input
	zipcode_input = request.form["inputZipcode"]
	print('Zipcode entered =', zipcode_input)
	gmaps_scraper = WebDriver()
	results = gmaps_scraper.scrape(service_type, zipcode_input)
	# print(results)
	temp_req = requests.get(f"https://cs361-weather-service.herokuapp.com/current?zipcode={zipcode_input}")
	temperature, temp_icon = temp_req.json()['temp'], temp_req.json()['icon']

	return render_template('results.html', temp=temperature, temp_icon=temp_icon, service=service_type, 
	name_bizDescrip=zip(results['name'], results['business_descrip'], results['address']))

@app.route('/zipcode_submission_adv', methods=['POST'])
def zipcode_submit_adv():
	# global service_type
	zipcode_input, adv_service_type = request.form["inputZipcode"], request.form["advService"]
	print('Zipcode entered =', zipcode_input)
	print('Adv service =', adv_service_type)
	# print(service_type)
	gmaps_scraper = WebDriver()
	results = gmaps_scraper.scrape(adv_service_type, zipcode_input)
	print(results)
	temp_req = requests.get(f"https://cs361-weather-service.herokuapp.com/current?zipcode={zipcode_input}")
	temperature, temp_icon = temp_req.json()['temp'], temp_req.json()['icon']
	return render_template('results.html', temp=temperature, temp_icon=temp_icon, service=adv_service_type, name_bizDescrip=zip(results['name'], results['business_descrip']))

@app.route('/service_selection', methods=['POST'])
def service_select():
	global service_type
	global zipcode_input
	name = request.form['name']
	descrip = request.form['descrip']
	addy = request.form['addy']
	print(addy)
	print(name)
	print(zipcode_input)
	# print('hello')
	return render_template('results_final.html', service=service_type, name=name, descrip=descrip, addy=addy, zipcode=zipcode_input)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8888)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 
