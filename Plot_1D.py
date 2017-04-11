#!/usr/bin/env python   # THIS MUST BE THE FIRST LINE OF THE SCRIPT OTHERWISE IT HAS NO MEANING!
# -*- coding: utf8 -*-

'''
####################################
# this script is for 1D plots  #####
# it checks a specific folder  #####
# for .dat files and plots them ####
#         automatically         ####
####################################
General comments:
* There is this thing called docstring in Python.
  You can use it in the beginning of every object/method/function definition, by
  just using three quotes. I'll explain you in person what it does.
* I would recommend you to make comments ABOVE instead of NEXT TO your code.
  that means more line, but it's easier to read.
'''

import os
import pandas as pd
import matplotlib.pyplot as plt


# global variables/constants you define are usually defined in capital letters
# sets the directory with the data as global
DIRECTORY = "/Users/Mel/OneDrive/FLUKA/SMA/plots/sample1/"


def read_file(fullpath, flag = False):
	'''
	reads the file and saves the values in a dataframe
	'''
	# conversion factor to get a Gy/POT value
	CONVERSION_FACTOR = 1.602176462E-7

	with open (fullpath, 'r') as f:
		# skip head line of file
		next(f)
		# reads the values into a dataframe and saves as numeric values
		df = pd.DataFrame((line.rstrip().split() for line in f), dtype=float)

	# adds the conversion factor the y values
	df.loc[:,2] *= CONVERSION_FACTOR

	# we want to get the integrated data for the dose
	# TODO: You should name your code
	if flag:
		df[2] = df[2] * 2.2E10 * 3600 * 24 * 90 * 1E-3 # conversion factor * 90 days * kGy
	df[3] = df[3]/100*df[2] # to get the absolute value for the errorbar
	return df


def plot_data(df, x_label, y_label, title, directory, filename):
	''' function to plot the data '''

	fig = plt.figure(figsize=(12,9))
	ax = fig.add_subplot(111, aspect='auto')

	# removes the plot frame lines
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)

	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)

	ax.errorbar(
			df[0],
			df[2],
			yerr=df[3],
			ecolor='red',
			linestyle='-',
			color='grey',
			marker='o',
			markersize=4,
			drawstyle='steps-mid',
			barsabove=True)

	plt.xlabel(
			x_label,
			fontsize=18,
			labelpad=20)

	plt.ylabel(
			y_label,
			fontsize=18,
			labelpad=20)

	plt.title(
			title,
			fontsize=26)

	fig.text(
			0.05,
			0.005,
			"Data source: FLUKA Simulations 2017 with 50.000.000 primary particles. Bin size 0.5 cm | Angelo Infantino and Melanie Krawina",
			fontsize=9,
			horizontalalignment='left',
			verticalalignment='bottom',
			transform=ax.transAxes)

	plt.tight_layout(pad=3, w_pad=1.0, h_pad=2)
	path = "{}/{}.png".format(directory, filename)
	fig.savefig(path.format(directory, filename), )


def derive_configuration(filename):
	'''
	Derive configuration of plot based on input.
	'''

	LABEL = "{quality} [{unit}]"
	KILOGRAY_POT = 'kGy/POT'
	PER_SQUARE_CM_POT = '1/(cm^2 * POT)'
	CM = "cm"

	flag_labels = ["Dose"]

	labels = {
		"Dose": "Dose",
		"1MeVN": "1MeVN",
		"HEHeq": "HEHeq",
		"HEH": "HEH",
		"Neutron": "Neutron",
		"ThNeutron": "Thermal Neutron",
		"Proton": "Proton"
	}

	units = {
		"Dose": KILOGRAY_POT,
		"1MeVN": PER_SQUARE_CM_POT,
		"HEHeq": PER_SQUARE_CM_POT,
		"HEH": PER_SQUARE_CM_POT,
		"Neutron": PER_SQUARE_CM_POT,
		"ThNeutron": PER_SQUARE_CM_POT,
		"Proton": PER_SQUARE_CM_POT
	}

	# set y label and flag
	flag = True # TODO I didn't check the purpose, just took the logic as it was: but setting this here to True is point less...
	y_label = "unknown"
	for label in labels:
		if label in filename:
			y_label = LABEL.format(quality=labels[label], unit=units[label])
			if label in flag_labels:
				flag = True
			break

	# set x label
	x_quality = ""
	if "X" in filename:
		x_quality = "X"
	elif "Z" in filename:
		x_quality = "Z"
	x_quality += " Axis"
	x_label = LABEL.format(quality=x_quality, unit=CM)

	# set title
	title = filename.replace("_", " ")

	return x_label, y_label, title, flag


	# if filename.find('Dose') > 0:
	# 			y_label = "Dose [kGy/POT]"
	# 			flag = True					# flag = True gives the integrated data for the y values
	# elif filename.find('1MeVN') > 0:
	# 	y_label = "1MeVN [1/(cm^2 * POT)]"
	# elif filename.find('HEHeq') > 0:
	# 	y_label = "HEHeq [1/(cm^2 * POT)]"
	# elif filename.find('HEH') > 0:
	# 	y_label = "HEH [1/(cm^2 * POT)]"
	# elif filename.find('Neutron') > 0:
	# 	y_label = "Neutron [1/(cm^2 * POT)]"
	# elif filename.find('ThNeutron') > 0:
	# 	y_label = "Thermal Neutron [1/(cm^2 * POT)]"
	# elif filename.find('Proton') > 0:
	# 	y_label = "Proton [1/(cm^2 * POT)]"
	# else:
	# 	y_label = "unknown"
	#
	# if filename.find('X') > 0:
	# 	x_label = "X Axis [cm]"
	# elif filename.find('Z') > 0:
	# 	x_label = "Z Axis [cm]"
	# else:
	# 	x_label = " Axis [cm]"
	#
	# title = filename.replace("_", " ")
	#
	# return x_label, y_label, title, flag






if __name__ == "__main__":
	for f in os.listdir(DIRECTORY): #checks the directory for all .dat files
		if f.endswith(".dat"): # searches only for .dat files
			filename = (os.path.splitext(f)[0]) # gets the filename without the .dat extension
			fullpath = directory + f # gets the full path

			x_label, y_label, title, flag = derive_configuration(filename)
			df = read_file(fullpath, flag) # creates a dataframe object with the data
			print("Creating plot for: {}" .format(filename))
			plot_data(df, x_label, y_label, title, directory, filename)
