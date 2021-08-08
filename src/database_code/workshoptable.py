# Name: Matthew Hartigan
# Assignment: CS336 Assignment #9
# Page Name: workshoptable.py
# Created: 4/30/2019
# Description: The workshoptable.py program for Assignment #9.

from app import db_connect

input_csv_file = 'workshops.csv'


def read_input(input_filename):
	""" Opens input csv file and returns list of lists where each element in
	a list element holds a single field value for that line. """

	try:
		with open(input_filename) as inputFile:
			list_of_contents = []

			for line in inputFile:
				line_dict = {'workshop_title': '', 'time_slot': '', 'room_number': '', 'start_time': '', 'end_time': ''}
				line_list = []

				for value in line.split(','):
					line_list.append(value.strip('\n'))

				line_dict['workshop_title'] = line_list[0]
				line_dict['time_slot'] = line_list[1]
				line_dict['room_number'] = line_list[2]
				line_dict['start_time'] = line_list[3]
				line_dict['end_time'] = line_list[3]
				list_of_contents.append(line_dict)

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
	for entry in input_list:

		sql = ''' INSERT INTO workshops (workshop_title, time_slot, room_number, start_time, end_time) VALUES (?, ?, ?, ?, ?)'''
		cur.execute(sql, (entry['workshop_title'], entry['time_slot'], entry['room_number'], entry['start_time'], entry['end_time']))
db.commit()
db.close()