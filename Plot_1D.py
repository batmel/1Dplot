#!/usr/bin/env python
# THE LINE ABOVE MUST BE THE FIRST LINE OF THE SCRIPT OTHERWISE IT HAS NO MEANING!
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
from sys import argv
from sys import exit


# global variables/constants you define are usually defined in capital letters
# sets the directory with the data as global
# input_dir = "/Users/Mel/OneDrive/FLUKA/SMA/plots/sample1/"
try:
	input_dir = argv[1]
	input_dir += "/"
	input_dir = os.path.normcase(input_dir)
except IndexError:
	exit("Please specify directories on command line: " + __file__ + " /path/to/input_dir /path/to/output_dir")

try:
	output_dir = argv[2]
	output_dir += "/"
	output_dir = os.path.normcase(output_dir)
except IndexError:
	output_dir = input_dir

def read_file(fullpath, integration_flag = False):
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
	if integration_flag:
		df[2] = df[2] * 2.2E10 * 3600 * 24 * 90 * 1E-3 # conversion factor * 90 days * kGy
	df[3] = df[3]/100*df[2] # to get the absolute value for the errorbar
	return df


def plot_data(df, x_label, y_label, title, directory, filename):
	''' function to plot the data '''

	# NOTE uncomment if Latex is installed properly!
	# plt.rc('text', usetex=True)
	# plt.rc('font', family='serif')



	fig = plt.figure(figsize=(12,9))
	ax = fig.add_subplot(111, aspect='auto')

	# removes the plot frame lines
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)

	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)

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
			# fontsize=18,
			fontsize=24,
			labelpad=20)

	plt.ylabel(
			y_label,
			# fontsize=18,
			fontsize=24,
			labelpad=20)

	plt.title(
			title,
			# fontsize=26)
			fontsize=30)

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
	fig.savefig(path, )


def derive_configuration(filename):
	'''
	Derive configuration of plot based on input.
	'''
	from constants import LABEL, y_labels, x_labels, y_units, x_units, flag_labels


	# set y label and flag
	integration_flag = True # TODO I didn't check the purpose, just took the logic as it was: but setting this here to True is point less...
	y_label = "unknown"
	for label in y_labels:
		if label in filename:
			y_label = LABEL.format(quality=y_labels[label], unit=y_units[label])
			if label in flag_labels:
				integration_flag = True
			break

	# set x label
	x_label = " Axis"
	for label in x_labels:
		if label in filename:
			x_label = LABEL.format(quality=x_labels[label], unit=x_units[label])
			break


	# set title
	title = filename.replace("_", " ")

	return x_label, y_label, title, integration_flag

if __name__ == "__main__":
	# loop over content of input directory
	for filename in os.listdir(input_dir):
		# filter for .dat files
		if filename.endswith(".dat"):
			# remove extension from filename
			filename_root = (os.path.splitext(filename)[0])
			# get full path
			fullpath = input_dir + filename
			x_label, y_label, title, flag = derive_configuration(filename_root)
			# create a dataframe object with the data
			df = read_file(fullpath, flag)
			print("Creating plot for: {}".format(filename_root))
			plot_data(df, x_label, y_label, title, output_dir, filename_root)
