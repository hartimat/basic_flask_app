# Name: Matthew Hartigan
# Assignment: CS336 Assignment #9
# Page Name: registrationtable.py
# Created: 4/30/2019
# Description: The registrationtable.py program for Assignment #9.

from app import db_connect

input_csv_file = 'registrant_data.csv'


# Define Registrant class
class Registrant():
	def __init__(self):
		self.date_of_registration = ""
		self.title = ""
		self.firstname = ""
		self.lastname = ""
		self.address1 = ""
		self.address2 = ""
		self.city = ""
		self.state = ""
		self.zipcode = ""
		self.telephone = ""
		self.email = ""
		self.website = ""
		self.position = ""
		self.company = ""
		self.meals = ""
		self.billing_firstname = ""
		self.billing_lastname = ""
		self.card_type = ""
		self.card_number = ""
		self.card_csv = ""
		self.exp_year = ""
		self.exp_month = ""
		self.session1 = ""
		self.session2 = ""
		self.session3 = ""

	def list_attributes(self):
		return ['date_of_registration', 'title', 'firstname', 'lastname', 'address1', 'address2', 'city', 'state',
		        'zipcode', 'telephone', 'email', 'website', 'position', 'company', 'meals', 'billing_firstname',
		        'billing_lastname', 'card_type', 'card_number', 'card_csv', 'exp_year', 'exp_month', 'session1',
		        'session2', 'session3']


# Helper function to read input from file
def read_input(input_filename):
	""" Opens input csv file and returns a list of Registrant objects
	where each object holds the contents of a given line. """

	try:
		with open(input_filename) as inputFile:
			list_of_contents = []

			for line in inputFile:
				line_list = []
				newRegistrant = Registrant()

				for attribute, value in zip(newRegistrant.list_attributes(), line.split(',')):
					setattr(newRegistrant, attribute, (value.strip('\n')))

				list_of_contents.append(newRegistrant)

		inputFile.close()

		return list_of_contents

	except IOError as e:
		print("Error: Input file " + input_filename + " was not found.  Exiting program now.")
		exit()


# MAIN #
# Read contents from input file
input_list = read_input(input_csv_file)

# Connect to db
with db_connect() as db:
	cur = db.cursor()

	# Insert contents into awards table
	for line in input_list:
		sql = ''' INSERT INTO registrants(date_of_registration, title, firstname, lastname, address1, address2, city, state, zipcode, telephone, email, website, position, company, meals, billing_firstname, billing_lastname, card_type, card_number, card_csv, exp_year, exp_month, session1, session2, session3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

		cur.execute(sql, (getattr(line, 'date_of_registration'),
		                  getattr(line, 'title'),
		                  getattr(line, 'firstname'),
		                  getattr(line, 'lastname'),
		                  getattr(line, 'address1'),
		                  getattr(line, 'address2'),
		                  getattr(line, 'city'),
		                  getattr(line, 'state'),
		                  getattr(line, 'zipcode'),
		                  getattr(line, 'telephone'),
		                  getattr(line, 'email'),
		                  getattr(line, 'website'),
		                  getattr(line, 'position'),
		                  getattr(line, 'company'),
		                  getattr(line, 'meals'),
		                  getattr(line, 'billing_firstname'),
		                  getattr(line, 'billing_lastname'),
		                  getattr(line, 'card_type'),
		                  getattr(line, 'card_number'),
		                  getattr(line, 'card_csv'),
		                  getattr(line, 'exp_year'),
		                  getattr(line, 'exp_month'),
		                  getattr(line, 'session1'),
		                  getattr(line, 'session2'),
		                  getattr(line, 'session3')))

db.commit()
db.close()
