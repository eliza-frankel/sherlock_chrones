#!/usr/local/Anaconda2024/bin/python3

#######################################
#                                     
#          Function Library
#       Created: April 1, 2025  
#       Updated: August 16, 2026
#        Author: Eliza Frankel       
#                                                             
#######################################

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import mesa_reader as mr
from glob import glob
import pandas as pd
from datetime import datetime
import csv

from scipy.interpolate import CubicSpline
from scipy.interpolate import pchip_interpolate, PchipInterpolator, interp1d

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



color = [plt.cm.tab20b(i) for i in range(plt.cm.tab20b.N)]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)


################################################################################
################################### CONTENTS ###################################
# 
# 
#    SECTION                    FUNCTION NAME                         
#   ----------------------------------------------------------------------------
#  
#    CONSTANTS               
#                           * N/A
#    GENERAL
#                           * make_tracklist()
#                           * parameters_from_history()
#                           * parameters_from_isochrone_csv()
#                           * find_nearest()
#                           * within_epsilon()
#                           * lower_bound()
#                           * upper_bound()
#                           * make_believe_age()
#                           * make_believe_everything_else()
#                           * artificial_isochrone_point()
#    INTERPOLATION
#                           * create_data_array()
#                           * interpolation_time()
#                           * data_manual_query()
#                           * extinction_law()
#                           * k_m()
#                           * distance_modulus()
#                           * hg_targets()
#    INTERACTIVE TEXTBOXES
#    (PLOTTING)             * annotate()
#                               * update_annot()
#                               * hover()
#    TERMINATION CODES /
#    TERMINATION INFO       * create_termination_codes()
#                           * tally_termination_codes()
#                           * determine_runtime()
#    COLORS AND CMAPS
#                           * get_cmap_colors()
#                           * cmap_discrete()
# 
# 
################################################################################

################################################################################
################################## CONSTANTS ###################################
################################################################################

M_sun_cgs = 1.989e33  # g
R_sun_cgs = 6.955e10  # cm
L_sun_cgs = 3.839e33  # erg s^-1
M_earth_cgs = 5.976e27 # g
R_earth_cgs = 637800  # cm

M_sun_mks = 1.989e30  # kg
R_sun_mks = 6.969e8   # m
L_sun_mks = 3.826e26  # W
M_earth_mks = 5.976e24 # kg
R_earth_mks = 6.378e6 # m


AU_to_m = 1.495979e11 # 1 AU = 1.495979e11 m
AU_to_cm = 1.495979e+13 # 1 AU = 1.495979e+13 cm
seconds_per_yr = 365 * 24 * 3600 # seconds in 1 year

G_cgs = 6.6743e-8  # cm3 g-1 s-2
G_AU_cgs = G_cgs / (AU_to_cm **3) # AU3 g-1 s-2
G_mks = 6.670e-11  # N m^2 kg^-2

year = 3.154e+7  # s
c_cgs = 2.998e10  # cm s^-1
k_cgs = 1.3807e-16  # cm2 g s-2 K-1
h_cgs = 6.6261e-27  # cm2 g s-1
sb_constant_cgs = 5.669e-5 # erg cm-2 K-4 s-1

c_mks = 2.998e10  # m/s
k_mks = 1.381e-23 # J/K
h_mks = 6.626e-34 # J 
sb_constant_mks = 5.669e-8 # W m^-s K^-4

pi = np.pi
m_h_cgs = 1.6733e-24  # g
m_h_mks = 1.6735e-27  # kg

# molecular weights
N_a = 6.022e23 # mol^-1
mu_H2 = 2.01588 #/ N_a
mu_N2 = 28.0134 #/ N_a


################################################################################
#################################### GENERAL ###################################
################################################################################


def make_tracklist(tracklist):
    """ Takes a path and creates a list of all tracks in said directory

    Parameters:
    -----------
    tracklist (str) - path to directory housing desired files

    Returns:
    --------
    list of the names of all files in inputted directory, sorted (ie for history files it will be sorted in ascending mass order)
    """
    
    tracklist = glob(tracklist)
    tracklist.sort()

    return tracklist



def parameters_from_history(filename):
    """ Takes the name of a history file from MESA and returns the model parameters.

    Parameters:
    -----------
    filename (str) - string of history filename. *** MUST BE IN THE FORMAT 'history_m{MASS}_z{METALLICITY}_a{ALPHA_MLT}.data'

    Returns:
    (strings) mass, metallicity, alpha
    """
    history = filename.split('/')[-1] # choosing the actual history files, not any directory it is in
    f = history.split('_') 
    
    mass = f[1][1:]
    metallicity = f[2][1:]
    alpha = f[3][1:-5]  # removing the '.data' from the end of the history filename, just leaving the a & value. Then, removing the a
    
    return mass, metallicity, alpha



def parameters_from_isochrone_csv(filename):
    """ Takes the name of an isochrone CSV created in finding_isochrone and returns the model parameters.

    Parameters:
    -----------
    filename (str) - string of isochrone csv
        *** must be in the format of:
        isochrone_age{AGE}Gyr_z{METALLICITY}_a{ALPHA_MLT}_tolerance{TOLERANCE_RANGE}_tracks{NUM_TRACKS}.csv

    Returns:
    (strings) age, metallicity, alpha, tolerance, num_tracks
    """
    name = filename.split('/')[-1] # choosing the actual history files, not any directory it is in
    f = name.split('_') 
    
    age = f[1][3:-3]  # removes 'age' from the front and 'Gyr' from the end
    metallicity = f[2][1:]
    alpha = f[3][1:] 
    tolerance = f[4][9:]  # removes 'tolerance'
    num_tracks = f[5][6:-4]  # removes 'tracks' from the beginning and '.csv' from the end
    
    return age, metallicity, alpha, tolerance, num_tracks



def find_nearest(array, value):
    """ Finds the index closest to the value in array

    Parameters:
    -----------
    array (np.array) - list of instances/information
    value (float or int) - value to look for in array

    Returns:
    ---------
    index (int) - index of the array instance closest to value
    array[indx] (float or int) - the value in array closest to value
    """

    indx = np.absolute(array - value).argmin()
    return indx, array[indx]



def within_epsilon(value, target_val, epsilon=0.05):
    """ Determines if the age from an array is within epsilon of target_age

    Parameters:
    -----------
    value (int or float) - Value of object
    target_val (int or float) - the target number to compare to
    epsilon (float or int) - tolerance of target_age, to determine if the age is
        viable
        If not specified, it defaults to 5%

    """

    if (np.absolute(value - target_val) / value) < epsilon:
        return True
    else:
        return False



def lower_bound(target_value, array):
    """ Finds the closest (but lower) value from an array to a desired value

    Parameters:
    -----------
    target_value (int or float) - value you are looking for in an array
    array (np.array) - list of values to search through
    
    Returns:
    --------
    index of lower bound (int)
    lower bound value (int or float)

    """

    all_lower = np.where(array <= target_value)[0]

    try:
        return all_lower[-1], array[all_lower[-1]]
    except:
        return 0, array[0]



def upper_bound(target_value, array):
    """ Finds the closest (but lower) value from an array to a desired value

    Parameters:
    -----------
    target_value (int or float) - value you are looking for in an array
    array (np.array) - list of values to search through
    
    Returns:
    --------
    index of upper bound (int)
    lower bound value (int or float)

    """

    all_upper = np.where(array >= target_value)[0]

    try:
        return all_upper[0], array[all_upper[0]]
    except:
        return -1, array[-1]



def make_believe_age(lower, upper, target, num_steps=1000):
    """ Takes the upper and lower bounds of a range, makes an artifical list of 
        values between, then finds the closest from the artificial list. 
        Returns index, value, and number of steps

    Parameters:
    -----------
    lower (float or int) - lower bound
    upper (float or int) - upper bound
    target (float or int) - target value to search for between lower and upper
    num_steps (int) - number of steps to make a range between upper and lower.
        Default value is 1000

    Returns:
    --------
    index (int) - index of closest value
    artificial value at array index (int or float)
    """

    # EAF - check to see if lower and upper are the same
    if lower == upper:
        return None, lower

    artificial_list = np.linspace(lower, upper, num_steps)


    index = find_nearest(artificial_list, target)


    return index, artificial_list[index]


def make_believe_everything_else(index, arr_lower_bound, arr_upper_bound, num_steps):
    """ Takes the index from make_believe_age for the closest value to target 
        age, creates an artificial list for another variable range

    Parameters:
    -----------
    index (int) - index of closest value
    arr_lower_bound (int or float) - lower bound of alternative array at same 
        index as age
    arr_upper_bound (int or float) - upper bound of alternative array at same 
        index as age
    num_steps (int) - number of steps to make a range between upper and lower.

    Returns:
    --------
    artificial value at array index (int or float)

    """

    artificial_list = np.linspace(arr_lower_bound, arr_upper_bound, num_steps)

    return artificial_list[index]



def artificial_isochrone_point(target_age, ages, masses, parameters, num_steps=1000):

    """ Takes values a stellar track from a MESA history file and determines
        the closest point to the target age. Uses the functions find_nearest, 
        lower_bound, upper_bound, make_believe_age, and 
        make_believe_everything_else
        ******** Can add nu_max and delta_nu. Just need to add parameter, 2 lines of code, and return statement ********

    Parameters:
    -----------
    target_age (float or int) - target value to search for between lower & upper
    ages (np.array) - list of ages from stellar track
    masses (np.array) - list of stellar track masses
    temps (np.array) - list of stellar track effective temperatures
    lums (np.array) - list of stellar track luminosities
    loggs (np.array) - list of stellar track surface gravities
    num_steps (int) - number of steps to make a range between upper and lower.
        Default value is 1000
    """


    # EAF - first finding the upper and lower bounds of ages
    #       & the index, closest age, and number of steps
    lower_index, lower_val = lower_bound(target_age, ages)
    upper_index, upper_val = upper_bound(target_age, ages)

    index, closest_age = make_believe_age(lower_val, upper_val, target_age, num_steps)

    # EAF - artificially create the other necessary variables, find value
    #       at the same index as the artificial age

    make_believe_values = []

    mass_inferred = masses[0]
    make_believe_values.append(mass_inferred)

    if index != None:
        for param in parameters:

            inferred_parameter = make_believe_everything_else(index, param[lower_index], param[upper_index], num_steps)
            make_believe_values.append(inferred_parameter)

    else:

        for param in parameters:

            inferred_parameter = param[lower_index]
            make_believe_values.append(inferred_parameter)


    return closest_age, make_believe_values, lower_index



################################################################################
################################ INTERPOLATION #################################
################################################################################


def create_data_array(file):
    """ Creates arrays from a file of all information from CSV file.

    Parameters:
    -----------
    file (string) - path to history files

    Returns:
    --------
    T_eff (np.ndarray) - all temperatures closest to desired age (within epsilon)
    luminosity (np.ndarray) - all luminosities closest to desired age (within epsilon)
    track_num (np.ndarray) - track number! 
    """

    df = pd.read_csv(file)

    # # EAF - extracting columns from csv
    T_eff = df["log_Teff"].to_numpy()
    luminosity = df["log_L"].to_numpy()
    mass = df["mass"].to_numpy()
    logg = df["logg"].to_numpy()

    try:
        G = df["G"].to_numpy()
        Gbp = df["Gbp"]
        Grp = df["Grp"]
        Gbp_Grp = df["Gbp-Grp"]
        Mag_bol = df["Mag_bol"]
        total_mass_he4 = df["total_mass_he4"].to_numpy()
    except:
        print("rip no mag space")



    # EAF - creating array of track number
    track_num = np.arange(0, len(T_eff))
    
    return track_num, T_eff, luminosity, mass, logg



def interpolation_time(T_eff, L_g, track_num, method='pchip', increments=1000):
    """ Does the cubic spline on T_eff and L.

    Parameters:
    -----------
    T_eff (np.ndarray) - all temperatures closest to desired age (within epsilon)
    L_g (np.ndarray) - all luminosities or logg closest to desired age (within epsilon)
    track_num (np.ndarray) - track number! 
    increments (int) - Number of increments to create points for. Defaults to 1000

    Returns:
    --------
    interpolated_temperature (np.ndarray) - the temperatures but cubic splined & interpolated
    interpolated_luminosity (np.ndarray) - the luminosities but cubic splined & interpolated

    """

    if method=='cubicspline':

        T_interpolator = CubicSpline(track_num, T_eff)
        L_g_interpolator = CubicSpline(track_num, L_g)

    elif method=='pchip':

        T_interpolator = PchipInterpolator(track_num, T_eff)
        L_g_interpolator = PchipInterpolator(track_num, L_g)

    interpolated_tracks = np.linspace(0, len(T_eff) - 1, increments)

    interpolated_temperature = T_interpolator(interpolated_tracks)
    interpolated_luminosity_logg = L_g_interpolator(interpolated_tracks)

    return interpolated_temperature, interpolated_luminosity_logg



def data_manual_query(path, save_file=None):
    df = pd.read_csv(path)

    Gmag = df["phot_g_mean_mag"].to_numpy()
    BP_RP = df["bp_rp"].to_numpy()

    source_ids = df["source_id"].to_numpy()

    Teff_phot = df["teff_gspphot"]
    logg_phot = df["logg_gspphot"]

    ag_gspphot = df["ag_gspphot"]
    azero_gspphot = df["azero_gspphot"]
    ebpminrp_gspphot = df["ebpminrp_gspphot"]

    phot_g_mean_flux = df["phot_g_mean_flux"]
    phot_bp_mean_flux = df["phot_bp_mean_flux"]
    phot_rp_mean_flux = df["phot_rp_mean_flux"]


    return Gmag, BP_RP, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux





def extinction_law(logg, BP_RP_iso, G, eb_v, delta=0, Xname='BPRP'):
    """ Calculates Gaia (E)DR3 extinction law from https://www.cosmos.esa.int/web/gaia/edr3-extinction-law

    Parameters:
    -----------
    logg (array, float or int) - value of surface gravity for the star
    BP_RP_iso (array, float or int) - Gaia G_BP - G_RP
    G (array, float or int) - Gaia Gmag
    eb_v (float) - extinction
    Xname (str) - Filter name

    """
    # EAF - determining if we need MS or RGB extinction table 
    A_G, A_BP, A_RP, E_BP_RP = [], [], [], []

    A0 = 3.1 * eb_v
    # A0 = 3.09 * eb_v  # McCall 2004

    for i in range(len(logg)):
        # if logg[i] >= 3.5:
        #     coeff_table = '~/Desktop/Research/Fitz19_EDR3_extinctionlawcoefficients/Fitz19_EDR3_MainSequence.csv'
        # elif logg[i] < 3.5:
        #     coeff_table = '~/Desktop/Research/Fitz19_EDR3_extinctionlawcoefficients/Fitz19_EDR3_HRDTop.csv'

        coeff_table = '~/Desktop/Research/Fitz19_EDR3_extinctionlawcoefficients/Fitz19_EDR3_HRDTop.csv'

        df = pd.read_csv(coeff_table)

        gaia_bands = ['kG','kBP','kRP']
        tables = {}
        column_titles = ['Intercept', 'X', 'X2', 'X3', 'A', 'A2', 'A3', 'XA', 'AX2', 'XA2']
        coeffs = {}

        for band in gaia_bands:
            tables[band] = df[df['Kname'] == band].sort_values('Xname')  # sort by Xname
            coeffs[band] = df[df['Kname'] == band][column_titles].values



        X = BP_RP_iso[i] - delta



        A_G.append(k_m(A0, X, Xname, 'kG', df) * A0)


        a_bp = (k_m(A0, X, Xname, 'kBP', df) * A0)
        a_rp = (k_m(A0, X, Xname, 'kRP', df) * A0)
        E_BP_RP.append(a_bp - a_rp)

        A_BP.append(a_bp)
        A_RP.append(a_rp)


    return A_G, A_BP, A_RP, E_BP_RP



def k_m(A0, X, Xname, band_name, df):
    """
    Calculates k_m (extinction coefficient in m band) from https://www.cosmos.esa.int/web/gaia/edr3-extinction-law

    Parameters:
    -----------
    A0 (float) - 3.1 * eb_v
    X (float) - vaue from Fitz19_EDR3_extinctionlawcoefficients file
    Xname (str) - Filter name 
    band_name (str) - band name (final column in extinction law coefficient table)
    df (Pandas data frame) - Data frame of Fitz19_EDR3_extinctionlawcoefficients file
    """

    a = df[(df['Xname']==Xname) & (df['Kname']==band_name)].iloc[0]

    km = a[0] + (a[1] * X) + (a[2]*(X**2)) + (a[3]*(X**3)) \
        + (a[4] * A0) + (a[5] * (A0**2)) + (a[6] * (A0**3)) \
        + (a[7] * (A0*X)) + (a[8] * (A0*(X**2))) + (a[9] * (X * (A0**2)))

    return km



def distance_modulus(avg_dist):
    """ Calculates the distance modulus using the average distance to an obj (in pc)

    Parameter:
    ----------
    avg_dist (float or int) - average distance to object in parsecs

    Returns:
    --------
    (float or int) distance modulus (m - M)
    """

    m_M = 5 * np.log10(avg_dist / 10)

    return m_M


def hg_targets(objects, source_ids, Gmag, BP_RP, ax, fig=None, questionable_IDs=None, classifications=[], row=0, col=0, plot=True, opacity=1):
    """
    objects = targets
    source_ids = all objects
    """

    G = []
    BPRP = []

    ids = pd.to_numeric(source_ids, errors='coerce')

    for i, obj in enumerate(objects):
        temp = ids == int(obj)
        temp_Gmag = Gmag[temp]
        temp_BP_RP = BP_RP[temp]

        G.append(temp_Gmag)
        BPRP.append(temp_BP_RP)


        if plot:

            marker_color = 'goldenrod'
            m='*'


            if int(obj) == int(2051293118064539520) or int(obj) == int(2051107609839671808):
                # marker_color='gray'
                marker_color='darkgrey'
                # m='*'
                m='v' 



            # possible agb
            if int(obj) == int(2051105754413616000) or int(obj) == int(2051293319920668160):
                marker_color = 'hotpink'
                m='o'

            size = 75

            if row != 0 and col != 0:
                ax[row, col].scatter(temp_BP_RP, temp_Gmag, marker=m, s=size, c=marker_color, alpha=opacity) #, alpha=0.5) #, zorder=30)
            else:
                ax.scatter(temp_BP_RP, temp_Gmag, marker=m, s=size, c=marker_color, alpha=opacity) #, alpha=0.5) #, zorder=30)


            if fig != None:
                if len(temp_Gmag) == 1:
                    stuff = [[obj], temp_Gmag, temp_BP_RP]
                    
                    # annotate(temp_BP_RP, temp_Gmag, stuff, ax, fig, label_text=['ID = {}', 'G = {}', 'BP-RP = {}'])
                    # annotate(temp_BP_RP, temp_Gmag, stuff, ax, fig, label_text='ID = {}')




################################################################################
#################### ADDING INTERACTIVE TEXTBOXES TO PLOTS ####################
################################################################################


def annotate(x, y, label, ax, fig, label_text='{}', c='k'):
    """ Uses ax.annotate to add labels to a figure, enabled by hovering over the point on a scatter plot!

    Parameters:
    -----------
    x (np.array or list) - list of x values
    y (np.array or list) - list of y values
    label (np.array or list) - list of labels to be displayed when cursor hovers
        over specified point. ** Must be in the same corresponding order as x 
        and y
    ax (plt Axes object) - the plot
    fig (plt figure)
    label_text (str) - optional; the label for the pop up box in the display.
        If not specified, defaults to '{}'
    c (str) - optional; color to plot points. If not specified, defaults to 
        black (lame)


    Note:
    -----
    The nitty gritties come from https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot
    * This is for plt.scatter ONLY! 
    * Instructions for plt.plot can be found in the above stack overflow link
    """


    sc = ax.scatter(x, y, marker='o', s=50, c=c)

    # EAF - xy is a touple of where the line begins, xytext is a touple saying
    #       where the line ends.
    annot = ax.annotate("", xy=(0,0), xytext=(-50,20),textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)



    def update_annot(ind):
        """ Changes the annotation / text in the pop up box. Here is where the 
            clor of the textbox can be changed, too
        
        Parameters:
        -----------
        ind (dict) - contains index of the scatter point. Of the form,
            {'ind': array([INDEX], dtype=int32)}
        """
        
        pos = sc.get_offsets()[ind["ind"][0]]

        annot.xy = pos

        # if type(label[0]) == np.ndarray:
        if isinstance(label_text, list):
            text = ""

            # puts all info with proper labeling/identification

            for i in range(len(label)):
                x = label_text[i].format(" ".join([str(label[i][n]) for n in ind["ind"]]))

                text += x

                if (i + 1) != len(label):
                    text += '\n'

            # text = label_text.format(" \n".join([str(label[i][n]) for n in ind["ind"] for i in range(len(label))]))
            print(text)

        else:
            text = label_text.format(" \n".join([str(label[n]) for n in ind["ind"]]))
            print(text)

        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(c)
        annot.get_bbox_patch().set_alpha(0.4)
        

    def hover(event):
        """ Tracking the cursor and changing outcome of textboxes. 
            Takes location of cursor (?) and either makes textbox visible
            or invisible depending on if it is within the bounds of the point.

        Parameters:
        -----------
        event (not sure the type) - location of cursor on screen?
        """

        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    # EAF - I believe this is the command that tracks your cursor and then 
    #       calls hover() to alter the textbox's visibility
    fig.canvas.mpl_connect("motion_notify_event", hover)



########################### TERMINATION CODES ############################


def create_termination_codes(file):
    """ Creates arrays from a CSV file

    Parameters:
    -----------
    file(string) - path to desired file

    Returns:
    --------
    termination_codes (dictionary) - dictionary in the format of {termination number: termination reason}
    """

    df = pd.read_csv(file)

    code = df["code"].to_numpy()
    reason = df["reason"].to_numpy()

    termination_codes = {}
    
    for c, r in zip(code, reason):
        termination_codes[int(c)] = r

    return termination_codes



def tally_termination_codes(file):
    """ Reads through run termination codes and tallys the number of each type

    Parameters:
    -----------
    file (str) - filename/path to file of each track's termination code
    """

    df = pd.read_csv(file, header=None)

    mass = df[0]
    code = df[1]

    run_terminations = np.unique(code)

    termination_codes = create_termination_codes('MESA_termination_codes.csv')
    
    x = {}
    for t in run_terminations:
        name = termination_codes[t]
        x[name] = int(len(code[code == t]))
    
    return run_terminations, x



def determine_runtime(filepath, return_csv=True):
    """ Reads through .out files from MESA runs and returns the runtime
        * must have last two lines be starting and ending times

    Parameters:
    -----------
    filepath (list of str) - path to output file(s)
    return_csv (boolean) - if True, output to CSV file. If False, put in dictionary.
            Defaults to csv output

    Returns:
    --------
    runtimes (dict) - contains output file name and the time it took to run the MESA track

    Notes:
    ------
    determine_runtime only returns runtimes if csv=False (ie no csv output file)

    """

    runtimes = {}

    for file in filepath:

        # getting just the filename, ignoring any directories.
        path = file.split('/')[-1]

        with open(file, 'r') as f:

            # creating a temporary array to get both start and end times
            time = []

            for line in (f.readlines()[-2:]):

                # splitting the string that has date and time
                t_split = line.split('_')[-1]
                t = t_split[0:-1]

                # changing string to datetime object in the format hours:min:sec
                time_obj = datetime.strptime(t, '%H:%M:%S')

                time.append(time_obj)

            # subtracting end time from start time
            x = time[1] - time[0]

        if return_csv == False:

            # Adding run times to a dictionary of the form filename:runtime 
            runtimes[path] = str(x)

        elif return_csv:

            # Finding alpha_MLT from output file name
            parameters = path.split("_")
            # [:4] is to remove '.out'. if alpha_MLT has different values in name, this will have to change!!!!
            alpha = parameters[2][:4]

            output_name = f"track_runtimes_{alpha}0.log"

            # Writing output filename and run time into csv file
            with open(output_name, 'a') as out:
                writer = csv.writer(out)
                writer.writerow([path, str(x)])
   
    if return_csv == False:
        return runtimes



################################################################################
########################### COLORS AND COLORMAPPING ############################
################################################################################


def get_cmap_colors(cmap_name, num_colors):
    """ Function to get a matplotlib color map and segment it into N colors (num_colors)
    
    Parameters:
    -----------
    cmap_name (str) - name of matplotlib colormap
    num_colors (int) - number of colors the colormap should be split into.

    Returns:
    --------
    colors (list) - in the format (X, Y, Z, 1.0)

    Note:
    -----
    written by Gabby Graham

    cmaps:
    # gist_rainbow - pretty rainbow; very bright
    # gnuplot - nice range of colors
    # PuOr - purple and orange
    # viridis - classic purples blues greens yellows
    # plasma - pretty blue purple pink orange yellow
    # magma - like plasma but dark
    # tab20b - nice neutral rainbow vibes - discrete
    # turbo - pretty rainbow, ends with black
    """

    cmap = plt.colormaps.get_cmap(cmap_name)
    colors = [cmap(i) for i in range(cmap.N)]
    return colors



def cmap_discrete(cmap_name, num_colors):
    """ Function to create a custom discrete color map with N colors - meant for 
        plotting colorbars. Uses function get_cmap_colors()

    Parameters:
    -----------
    cmap_name (str) - name of matplotlib colormap
    num_colors (int) - number of colors the colormap should be split into.

    Returns:
    --------
    norm (matplotlib.colors.BoundaryNorm obect) - to be used in plt.scatter()
        This determines the number of colors used in colorbar.

    Note:
    -----
    Should be used as follows:
    >  plt.scatter(x, y, c=$sequence_numbers_mapped_using_cmap_norm, cmap=$COLOR_MAP, norm=norm)
    or
    >  plt.scatter(x, y, c=$c, cmap=$COLOR_MAP, norm=cmap_discrete($COLOR_MAP, $NUM_COLORS))
    """

    segments = get_cmap_colors(cmap_name, num_colors)
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', segments, cmap_name.N)

    bounds = np.linspace(0, num_colors, num_colors + 1)
    norm = mpl.colors.BoundaryNorm(segments, cmap.N)

    return norm


