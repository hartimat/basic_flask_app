# Name: Matthew Hartigan
# Assignment: CS336 Assignment #9
# Page Name: userstable.py
# Created: 4/30/2019
# Description: The userstable.py program for Assignment #9.

from app import db_connect

input_csv_file = 'users.csv'


def read_input(input_filename):
	""" Opens input csv file and returns list of lists where each element in
	a list element holds a single field value for that line. """

	try:
		with open(input_filename) as inputFile:
			list_of_contents = []

			for line in inputFile:
				line_list = []

				for value in line.split(','):
					line_list.append(value.strip('\n'))

				list_of_contents.append(line_list)

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
		print(line)
		sql = ''' INSERT INTO users(firstname, lastname, password) VALUES (?, ?, ?)'''
		cur.execute(sql, line)

db.commit()
db.close()