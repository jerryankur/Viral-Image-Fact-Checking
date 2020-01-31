import argparse
import pycurl
from flask import Flask, url_for, jsonify, request
from flask_cors import CORS, cross_origin
import io
from bs4 import BeautifulSoup
import certifi
from googlecloudapi import getCloudAPIDetails, saveImage
import requests, json, shutil, os
from basesix4 import basesix4
app = Flask(__name__)
history=[]
alldata=[]
@app.route('/')
def welcome():
    print ('welcome() function called')
    return 'Welcome to the server'
@app.route('/history')
def history():
	print('history() function called')
	return jsonify(history)
@app.route('/data')
def data():
	print('data() function called')
	return alldata;
@app.route('/search', methods = ['POST'])
def search():
	print('search() function called')
	if request.headers['Content-Type'] != 'application/json':
		return "Requests must be in JSON format. Please make sure the header is 'application/json' and the JSON is valid."
	client_json = json.dumps(request.json)
	client_data = json.loads(client_json)
	if app.debug:
	    print('POST: ' + 'https://www.google.com/searchbyimage?hl=en-US&image_url='+client_data['image_url'])
	io_code=io.BytesIO()
	conn = pycurl.Curl()
	conn.setopt(conn.CAINFO, certifi.where())
	conn.setopt(conn.URL, str('https://www.google.com/searchbyimage?hl=en-US&image_url='+client_data['image_url']))
	conn.setopt(conn.FOLLOWLOCATION, 1)
	conn.setopt(conn.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0')
	conn.setopt(conn.WRITEFUNCTION, io_code.write)
	conn.perform()
	conn.close()
	soup = BeautifulSoup(io_code.getvalue().decode('UTF-8'),'html.parser')
	results = {
	    'links': [],
	    'descriptions': [],
	    'titles': [],
	    'similar_images': [],
	    'best_guess': ''
	}
	for div in soup.findAll('div', attrs={'class':'rc'}):
	    sLink = div.find('a')
	    results['links'].append(sLink['href'])
	for desc in soup.findAll('span', attrs={'class':'st'}):
	    results['descriptions'].append(desc.get_text())
	for title in soup.findAll('h3', attrs={'class':'r'}):
	    results['titles'].append(title.get_text())
	for similar_image in soup.findAll('div', attrs={'rg_meta'}):
	    tmp = json.loads(similar_image.get_text())
	    img_url = tmp['ou']
	    results['similar_images'].append(img_url)
	for best_guess in soup.findAll('a', attrs={'class':'fKDtNb'}):
	  results['best_guess'] = best_guess.get_text()
	print("Successful search")
	return json.dumps(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Meta Reverse Image Search API')
    parser.add_argument('-p', '--port', type=int, default=5000, help='port number')
    parser.add_argument('-d','--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-c','--cors', action='store_true', default=False, help="enable cross-origin requests")
    args = parser.parse_args()
    if args.debug:
        app.debug = True
    if args.cors:
        CORS(app, resources=r'/search/*')
        app.config['CORS_HEADERS'] = 'Content-Type'
        search = cross_origin(search)
        print(" * Running with CORS enabled")
    app.run(host='0.0.0.0', port=args.port)