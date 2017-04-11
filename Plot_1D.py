####################################
# this script is for 1D plots  #####
# it checks a specific folder  #####
# for .dat files and plots them ####
#         automatically         ####
####################################

#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import matplotlib.pyplot as plt
import pandas as pd
directory = "/Users/Mel/OneDrive/FLUKA/SMA/plots/sample1/" # sets the directory with the data as global

def read_file(fullpath, flag = False): # reads the file and saves the values in a dataframe
	conversion_factor = 1.602176462E-7 # conversion factor to get a Gy/POT value
	with open (fullpath, 'r') as f:
		next(f)
		df = pd.DataFrame((l.rstrip().split() for l in f), dtype=float) # reads the values into a dataframe and saves as numeric values
	df.loc[:,2] *= conversion_factor # adds the conversion factor the y values
	if flag: # we want to get the integrated data for the dose
		df[2] = df[2] * 2.2E10 * 3600 * 24 * 90 * 1E-3 # conversion factor * 90 days * kGy
	df[3] = df[3]/100*df[2] # to get the absolute value for the errorbar
	return df

def plot_data(df, x_label, y_label, title, directory, filename): # function to plot the data
	fig = plt.figure(figsize=(12,9))
	ax = fig.add_subplot(111, aspect='auto')

	ax.spines["top"].set_visible(False) # removes the plot frame lines
	ax.spines["right"].set_visible(False)

	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)

	ax.errorbar(df[0],df[2], yerr = df[3], ecolor='red', linestyle='-', color='grey', marker='o', markersize=4, drawstyle='steps-mid', barsabove=True)
	
	plt.xlabel(x_label, fontsize=18, labelpad=20)
	plt.ylabel(y_label, fontsize=18, labelpad=20)
	plt.title(title, fontsize=26)
	fig.text(0.05,0.005, "Data source: FLUKA Simulations 2017 with 50.000.000 primary particles. Bin size 0.5 cm | Angelo Infantino and Melanie Krawina", fontsize=9, horizontalalignment='left',verticalalignment='bottom',transform = ax.transAxes)

	plt.tight_layout(pad=3, w_pad=1.0, h_pad=2)
	fig.savefig(directory + filename + '.png',)

def set_variables(filename):
	flag = True
	if filename.find('Dose') > 0: # sets the Axis labels automatically, if it finds a substring
				y_label = "Dose [kGy/POT]"
				flag = True					# flag = True gives the integrated data for the y values
	elif filename.find('1MeVN') > 0:
		y_label = "1MeVN [1/(cm^2 * POT)]"
	elif filename.find('HEHeq') > 0:
		y_label = "HEHeq [1/(cm^2 * POT)]"
	elif filename.find('HEH') > 0:
		y_label = "HEH [1/(cm^2 * POT)]"
	elif filename.find('Neutron') > 0:
		y_label = "Neutron [1/(cm^2 * POT)]"
	elif filename.find('ThNeutron') > 0:
		y_label = "Thermal Neutron [1/(cm^2 * POT)]"
	elif filename.find('Proton') > 0:
		y_label = "Proton [1/(cm^2 * POT)]"
	else:
		y_label = "unknown"

	if filename.find('X') > 0:
		x_label = "X Axis [cm]"
	elif filename.find('Z') > 0:
		x_label = "Z Axis [cm]"
	else:
		x_label = " Axis [cm]"

	title = filename.replace("_", " ") 

	return x_label, y_label, title, flag


def main():
	for file in os.listdir(directory): #checks the directory for all .dat files
		if file.endswith(".dat"): # searches only for .dat files
			filename = (os.path.splitext(file)[0]) # gets the filename without the .dat extension
			fullpath = directory+file # gets the full path

			x_label, y_label, title, flag = set_variables(filename)
			df = read_file(fullpath, flag) # creates a dataframe object with the data
			print("Creating plot for: {}" .format(filename)) 
			plot_data(df, x_label, y_label, title, directory, filename)

if __name__ == "__main__":
	main()