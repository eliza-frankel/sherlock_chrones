#!/Users/elizafrankel/anaconda3/bin/python3

# # Author: E. Frankel
# # 5.16.2025

import sys
sys.path.insert(0, '/Users/elizafrankel/Desktop/Research/')
import functions as fn
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from glob import glob
import csv
import bcutil
from matplotlib.colors import ListedColormap

# For 9
cb_colors_9 = ['#000000', '#2E2585', '#337538', '#5DA899', '#94CBEC', '#DCCD7D', '#C26A77', '#9F4A96', '#7E2954']

# For 16
cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DAA9D6', '#DCCD7D', '#E4A05A', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']

# cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DAA9D6', '#DCCD7D', '#E4A05A', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101', '#000000']


new_cmap = ListedColormap(cb_colors_16)

color = [new_cmap(i) for i in range(new_cmap.N)]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)

alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

# alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.85', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
# alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.85, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

age = 8.3
Fe_H = '0.31'
Fe_H_float = float(Fe_H)
metallicity = '0.0345'
cluster = 'NGC 6791'
cluster_folder = 'NGC6791'
cluster_data = 'data_NGC6791/DONE/FINAL'



location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'


files = glob(f'{cluster_folder}/{cluster_data}/isochrone_age8.3Gyr_z0.034507_a*.csv')
files.sort()


df = pd.read_csv('ngc6791_data.csv', delimiter='\t')

ids = df["ID"].to_numpy()
mass = df["Mass"].to_numpy()
simbad_mass = df["SIMBAD_MASS"].to_numpy()
simbad_mass_unc = df["mass_uncertainty"].to_numpy()
logg = df["Logg"].to_numpy()
logg_unc = df["Logg_uncertainty"].to_numpy()
classification = df["classification"].to_numpy()
teff = df["Teff"].to_numpy()
teff_unc = df["Teff_uncertainty"].to_numpy()

# COLOR = ["goldenrod" if classification[i] == 'gold' else "silver" for i in range(len(classification))]

# fig, ax = plt.subplots(figsize=(6,8))
fig, ax = plt.subplots(figsize=(8,7))

for i in range(len(classification)):
	if classification[i] == 'gold':
		COLOR = "goldenrod"
		MARKER = '*'
	elif classification[i] == 'silver':
		COLOR = "darkgrey"
		MARKER = 'v'

	if ids[i] == 2437965 or ids[i] == 2569935:
		COLOR = 'hotpink'
		MARKER = 'o'

	# EAF - looking for potential AGB star
	if ids[i] == 2571093:
		MARKER = 's'

	MSIZE = 16

	

	plt.errorbar(logg[i], simbad_mass[i], xerr=logg_unc[i], yerr=simbad_mass_unc[i], alpha=0.75, fmt=MARKER, markersize=MSIZE, color=COLOR) #, barsabove=True)
	# fn.annotate(logg[i], simbad_mass[i], [ids[i]], ax, fig, label_text='ID = {}', c=COLOR)

# for alpha in alpha_mlt:
for i in range(len(alpha_mlt)):

	alpha = alpha_mlt[i]
	iso_file = files[i]

	df_iso = pd.read_csv(iso_file)

	iso_logg = df_iso["logg"]
	iso_mass = df_iso["mass"]

	amlt = r'$\alpha_{\rm MLT}$'
	plt.plot(iso_logg, iso_mass, zorder=0, label=amlt + f' = {alpha}')

# cmap boundaries so ticks appear in center of cbar:
alpha_mlt_float = np.array(alpha_mlt_float)
step = 0.1
boundaries = np.concatenate([
	[alpha_mlt_float[0] - step/2],
	(alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
	[alpha_mlt_float[-1] + step/2]
])


# cmap = mpl.cm.tab20b
# norm = mpl.colors.BoundaryNorm(alpha_mlt_float, new_cmap.N)
norm = mpl.colors.BoundaryNorm(boundaries, new_cmap.N)

cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap), ax=ax, ticks=alpha_mlt_float, boundaries=boundaries, orientation='vertical')
cbar.set_label(label=r"$\alpha_{\rm MLT}$", size=15)


cbar.ax.tick_params(labelsize=13)

plt.xlim(0.5,3.55)
plt.ylim(0.59,1.42)

plt.xlabel(r"$\log g$", fontsize=16)
plt.ylabel(r"Mass (M$_{\odot}$)", fontsize=16)

plt.tick_params('both', labelsize=13)
# plt.title(r"NGC 6791 - All $\alpha_{MLT}$")

plt.errorbar(0,0, xerr=0.5, yerr=0.1, fmt='*', markersize=MSIZE, color="xkcd:dull yellow", label='Gold')
plt.errorbar(0,0, xerr=0.5, yerr=0.1, fmt='v', markersize=MSIZE, color='grey', label='Silver')

# plt.legend(loc='upper left', fontsize=13)
plt.gca().invert_xaxis()

plt.savefig('figures/NGC6791/best_fit_metrics/asteroseismology/classifications_logg_v_mass_NGC6791.png', dpi=300)
plt.savefig('figures/NGC6791/best_fit_metrics/asteroseismology/classifications_logg_v_mass_NGC6791.pdf')
plt.show()

############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

# # files = glob('8.3Gyr/may20_final/isochrone_age8.3Gyr_z0.025490_a*.csv')
# files = glob('8.3Gyr/may20_final/aaaarange/isochrone_age8.3Gyr_z0.025490_a*.csv')
# # files = glob('8.3Gyr/isochrone_age8.3Gyr_z0.025490_a*.csv')
# files.sort()



# # alpha_mlt = ['1.65', '1.75']
# # c = ['lightskyblue', 'k']

# # alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
# # alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

# alpha_mlt = ['1.60', '1.65', '1.70', '1.75', '1.80', '1.90']
# alpha_mlt_float = [1.60, 1.65, 1.70, 1.75, 1.80, 1.90]


# # fig, ax = plt.subplots(figsize=(6,8))
# for temp, alpha in enumerate(alpha_mlt):
# 	fig, ax = plt.subplots(figsize=(6,8))

# 	for i in range(len(classification)):
# 		if classification[i] == 'gold':
# 			COLOR = "xkcd:dull yellow"
# 			MARKER = '*'
# 		elif classification[i] == 'silver':
# 			COLOR = "darkgrey"
# 			MARKER = 'v'

# 		if mass[i] == 0.84:
# 			COLOR = 'hotpink'
# 			MARKER = 'o'
# 		if logg[i] == 1.60:
# 			COLOR = 'hotpink'
# 			MARKER = 'o'
# 		MSIZE = 13

# 		plt.errorbar(teff[i], logg[i], xerr=teff_unc[i]*2, yerr=logg_unc[i]*2, alpha=0.75, fmt=MARKER, markersize=MSIZE, color=COLOR) #, barsabove=True)

		

# 		# plt.scatter(teff[i], logg[i], color=COLOR, marker=MARKER, s=MSIZE)
		# fn.annotate(teff[i], logg[i], [ids[i]], ax, fig, label_text='ID = {}', c=COLOR)


# 	# for i in range(len(alpha_mlt)):

# 		# alpha = alpha_mlt[i]
# 		# iso_file = files[i]
# 	iso_file = files[temp]

# 	df_iso = pd.read_csv(iso_file)

# 	iso_logg = df_iso["logg"]
# 	iso_teff = df_iso["log_Teff"]

# 	plt.plot(10**iso_teff, iso_logg, zorder=0, label= amlt + f' = {alpha}') #, color=color[index[i]]) #, color=c[i])

# 	plt.errorbar(0,0, xerr=0.5, yerr=0.1, fmt='*', markersize=MSIZE, color="xkcd:dull yellow", label='Gold')
# 	plt.errorbar(0,0, xerr=0.5, yerr=0.1, fmt='v', markersize=MSIZE, color='darkgrey', label='Silver')

# 	plt.xlim(3000,6000)
# 	plt.ylim(0.4, 4.75)

# 	plt.gca().invert_xaxis()
# 	plt.gca().invert_yaxis()

# 	plt.ylabel(r"$\log g$", fontsize=16)
# 	plt.xlabel(r"$T_{\rm eff}$ [K]", fontsize=16)
# 	plt.tick_params('both', labelsize=13)
# 	plt.legend(fontsize=13, loc='upper left')

# 	# plt.savefig('figures/ngc6791/classifications_isochrone_NGC6791.pdf')
# 	plt.show()


############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
# Finding best fit asteroseismic target


# fig, ax = plt.subplots(ncols = 2, sharey = False, figsize = (8, 8), gridspec_kw={'width_ratios':[1.5, 3]})
#         plt.subplots_adjust(wspace = 0.0)
#         ax2, ax = ax[0], ax[1]  # EAF - puts y residuals on the left side!



files = glob(f'{cluster_folder}/{cluster_data}/isochrone_age8.3Gyr_z0.034507_a*.csv')
files.sort()

alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

# alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.85', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
# alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.85, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]


df = pd.read_csv('ngc6791_data.csv', delimiter='\t')

agb = [ids[X] == 2437965 or ids[X] == 2569935 for X in range(len(ids))]
agb_teff = teff[agb]
agb_teff_unc = teff_unc[agb]
agb_logg = logg[agb]
agb_logg_unc = logg_unc[agb]
agb_ids = ids[agb]
agb_classification = classification[agb]


# no = [ids[X] != 2437965 and ids[X] != 2569935 and classification[X] == 'gold' for X in range(len(ids))]
no = [ids[X] != 2437965 and ids[X] != 2569935 for X in range(len(ids))]
classification = classification[no]
teff = teff[no]
teff_unc = teff_unc[no]
logg = logg[no]
logg_unc = logg_unc[no]
ids = ids[no]

# print(classification)

for temp, alpha in enumerate(alpha_mlt):
	fig, ax = plt.subplots(ncols = 2, sharey = False, figsize = (8, 8), gridspec_kw={'width_ratios':[3, 1.5]})
	plt.subplots_adjust(wspace = 0.0)
	ax, ax2 = ax[0], ax[1] 

	# EAF - plotting isochrone

	iso_file = files[temp]

	df_iso = pd.read_csv(iso_file)

	iso_logg = df_iso["logg"].to_numpy()
	iso_teff = df_iso["log_Teff"].to_numpy()

	iso_teff_10 = 10**iso_teff

	ax.plot(iso_teff_10, iso_logg, zorder=0, label= amlt + f' = {alpha}', color='purple')

	ax2.plot(iso_teff_10 - iso_teff_10, iso_logg , label= amlt + f' = {alpha}', color='purple')
	pythag_dist = 0

	VISUALIZATION_FACTOR = 2
	RESID_VISUALIZATION_FACTOR = 1


	for i in range(len(classification)):
		if classification[i] == 'gold':
			COLOR = "goldenrod"
			MARKER = '*'
		elif classification[i] == 'silver':
			COLOR = "darkgrey"
			MARKER = 'v'

		if ids[i] == 2437965 or ids[i] == 2569935:
			COLOR = 'hotpink'
			MARKER = 'o'

		# EAF - checking if it is our potential AGB star
		if ids[i] == 2571093:
			MARKER = 's'
		MSIZE = 10


		ax.errorbar(teff[i], logg[i], xerr=teff_unc[i]*VISUALIZATION_FACTOR, yerr=logg_unc[i]*VISUALIZATION_FACTOR, alpha=0.5, fmt=MARKER, markersize=MSIZE, color=COLOR) #, barsabove=True)

		# EAF - find point on isochrone closest to the targets
		index, iso_closest_logg = fn.find_nearest(iso_logg, logg[i])

		# # Step 2: Find difference between isochrone and HG target
		diff = iso_teff_10[index] - teff[i]
		diff_logspace = iso_teff[index] - np.log10(teff[i])

		# # Step 3: Plot vs isochrone at 0
		# ax2.scatter(diff, logg[i], marker=MARKER, s=MSIZE, c=COLOR)
		ax2.errorbar(diff, logg[i], xerr=teff_unc[i]*RESID_VISUALIZATION_FACTOR, yerr=logg_unc[i]*RESID_VISUALIZATION_FACTOR, alpha=0.5, fmt=MARKER, markersize=MSIZE, color=COLOR)

		# fn.annotate(teff[i], logg[i], [ids[i]], ax, fig, label_text='ID = {}', c=COLOR)


		pythag_dist += diff_logspace**2
	print('alpha =', alpha, 'Pythagorean distance =', pythag_dist**(1/2))

	# EAF - manually adding the AGB stars
	for j in range(len(agb_teff)):
		# EAF - find point on isochrone closest to the targets
		index, iso_closest_logg = fn.find_nearest(iso_logg, agb_logg[j])

		# # Step 2: Find difference between isochrone and HG target
		diff = iso_teff_10[index] - agb_teff[j]
		diff_logspace = iso_teff[index] - np.log10(agb_teff[j])

		# print(agb_teff[j], iso_teff_10[index])

		ax.errorbar(agb_teff[j], agb_logg[j], xerr=agb_teff_unc[j]*VISUALIZATION_FACTOR, yerr=agb_logg_unc[j]*VISUALIZATION_FACTOR, alpha=0.75, fmt='o', markersize=MSIZE, color='hotpink')
		ax2.errorbar(diff, agb_logg[j], xerr=agb_teff_unc[j]*RESID_VISUALIZATION_FACTOR, yerr=agb_logg_unc[j]*RESID_VISUALIZATION_FACTOR, alpha=0.75, fmt='o', markersize=MSIZE, color='hotpink')

	# EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE
	amlt = r"$\alpha_{MLT}$"


	# textstr = f'Pythagorean Distance = {round(pythag_dist**(1/2), 3)}'

	# props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
	
	# ax.text(0.03, 0.97, textstr, transform=ax.transAxes, fontsize=14,
	# 		verticalalignment='top', bbox=props)

	
	textstr = f'{amlt} = {alpha}'
	
	# these are matplotlib.patch.Patch properties
	# props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
	props = dict(boxstyle='round', facecolor='mediumpurple', alpha=0.2)

	
	# place a text box in bottom right in axes coords
	# ax.text(0.03, 0.9, textstr, transform=ax.transAxes, fontsize=15,
	# 		verticalalignment='top', bbox=props)
	ax.text(0.04, 0.97, textstr, transform=ax.transAxes, fontsize=15,
			verticalalignment='top', bbox=props)

	ax.tick_params(labelsize=13)
	# ax2.tick_params(labelright=True, labelleft=False, right=True, left=False)
	ax2.tick_params(labelright=False, labelleft=False, right=False, left=True)
	ax2.invert_yaxis()

	ax2.set_xlabel(r'$\Delta T_{\rm eff}$', fontsize = 16)


	# plt.errorbar(0,0, xerr=0.5, yerr=0.1, fmt='*', markersize=MSIZE, color='goldenrod', label='Gold')
	# plt.errorbar(0,0, xerr=0.5, yerr=0.1, fmt='v', markersize=MSIZE, color='darkgrey', label='Silver')

	# ax.set_xlim(3000,6000)
	# ax.set_ylim(0.4, 4.75)

	ax.invert_xaxis()
	ax.invert_yaxis()

	# plt.gca().invert_xaxis()
	# plt.gca().invert_yaxis()

	ax.set_ylabel(r"$\log g$", fontsize=16)
	ax.set_xlabel(r"$T_{\rm eff}$ [K]", fontsize=16)
	plt.tick_params('both', labelsize=13)
	# plt.legend(fontsize=13, loc='upper left')

	# plt.savefig(f'figures/NGC6791/best_fit_metrics/asteroseismology/png/NGC6791_a{alpha}_astero_T_offset.png', dpi=300)
	# plt.savefig(f'figures/NGC6791/best_fit_metrics/asteroseismology/pdf/NGC6791_a{alpha}_astero_T_offset.pdf')
	plt.show()



