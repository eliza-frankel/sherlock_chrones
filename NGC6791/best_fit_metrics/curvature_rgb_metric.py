#!/Users/elizafrankel/anaconda3/bin/python3

# Author: E. Frankel
# 6.16.2026


import sys
sys.path.insert(0, '/Users/elizafrankel/Desktop/Research/')
import functions as fn
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from glob import glob
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
import math

# For 9
cb_colors_9 = ['#000000', '#2E2585', '#337538', '#5DA899', '#94CBEC', '#DCCD7D', '#C26A77', '#9F4A96', '#7E2954']

# For 16
cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DCCD7D', '#E4A05A', '#DAA9D6', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']


def rgb_curvature(classification_color, save_choice = True):

    age = 8.3
    Fe_H = '0.31'
    Fe_H_float = float(Fe_H)
    metallicity = '0.025490'
    cluster_folder = 'NGC6791'
    cluster = 'NGC 6791'



    location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

    files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
    files.sort()



    path_to_cluster_data = '~/Desktop/queries/ngc6791/ngc6791_final_query.csv'




    Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

    # Asteroseismic targets
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

    gaiaid = np.array([2051286795872609920, 2051288135902691840, 2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808])


    

    NGC6791_EBV = 0.14

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, NGC6791_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    
    


    r_NGC6791_parsecs = 4010  # Brogaard et al 2011

    d = fn.distance_modulus(r_NGC6791_parsecs)

    print(f"Distance modulus for {cluster} is {d}")


    new_cmap = ListedColormap(cb_colors_16)

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)

    # fig_curve, ax_curve = plt.subplots(figsize=(6,8))
    slopes = []
    distances = []


    for INDEX, file in enumerate(files):


        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        alpha = alpha_mlt[INDEX]
        
        CLASSIFICATION_COLOR = classification_color
        save = save_choice


        # 3. RGB Curvature

        fig_curve, ax_curve = plt.subplots(figsize=(6,8))

        # Plotting cluster
        ax_curve.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=30, c='grey', alpha=0.3)
        ax_curve.invert_yaxis()

        # 4. Inset plot
        axinset = ax_curve.inset_axes([0.91, 12.71, 0.35,0.7], transform=ax_curve.transData)

        axinset.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.1)
        axinset.invert_yaxis()

        axinset.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        # Create a Rectangle patch
        rect = patches.Rectangle((1.1, 12.51), .88,2.5, linewidth=1, edgecolor='r', facecolor='none')

        # Add the patch to the Axes
        axinset.add_patch(rect)

        # Plotting isochrone
        # C = ['purple', 'blue']
        ax_curve.plot(m_teff, m, label=r"$\alpha_{\rm MLT}$ = " + alpha, linewidth=2, alpha=0.25, color='purple')

        # ax_curve.plot(m_teff, m, color='purple', label=alpha, linewidth=2, alpha=0.25)

        RGB_objs = [2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808]
        AGB_questionables = [2051293319920668160, 2051105754413616000]

        fn.hg_targets(RGB_objs, source_ids, Gmag_gaia - A_G, BP_RP_gaia - A_BP + A_RP, ax_curve, questionable_IDs=AGB_questionables, fig=fig_curve)
        # fn.hg_targets(RGB_objs, source_ids, Gmag_gaia - A_G, BP_RP_gaia - A_BP + A_RP, axinset, questionable_IDs=AGB_questionables, fig=fig_curve, opacity=0.3)

        # # Plot isochrone one time:
        pythag_dist = 0 

        # # # Step 1: Find the brigntest and the dimmest stars 
        # # found these using hg_targets function and using the interactive annotation
        rgb_luminous_G = 12.990116832840757
        rgb_luminous_BP_RP = 1.9311618036359377

        rgb_luminous_silver_G = 12.765216344324163
        rgb_luminous_silver_BP_RP = 1.902059799593551

        rgb_dimmest_G = 14.765373743791011
        rgb_dimmest_BP_RP = 1.332823308552968

        if CLASSIFICATION_COLOR == 'Silver':

            # # EAF - this is for using the silver star as the most luminous
            rgb_luminous_BP_RP = rgb_luminous_silver_BP_RP
            rgb_luminous_G = rgb_luminous_silver_G

        
        # # Step 2: Find equivalent G values for the isochrone
        # Most luminous
        lum_index, iso_luminous_G = fn.find_nearest(m, rgb_luminous_G)
        iso_luminous_BP_RP = m_teff[lum_index]

        # Dimmest
        dim_index, iso_dim_G = fn.find_nearest(m, rgb_dimmest_G)
        iso_dim_BP_RP = m_teff[dim_index]



        # # Step 4: Drawing lines between brightest and dimmest point
        # Plotting line between brightest and dimmest targets
        ax_curve.plot([rgb_luminous_BP_RP, rgb_dimmest_BP_RP], [rgb_luminous_G, rgb_dimmest_G], linewidth=2, c='k')

        # # Plotting line between corresponding isochrone points
        ax_curve.plot([iso_luminous_BP_RP, iso_dim_BP_RP], [iso_luminous_G, iso_dim_G], linewidth=2, c='skyblue')

        # # L = ['purple', 'blue']
        # ax_curve.plot([iso_luminous_BP_RP, iso_dim_BP_RP], [iso_luminous_G, iso_dim_G], linewidth=2) #, c=L[INDEX])

        # # Step 5: Calculate distance between the two lines
        diff = ((iso_luminous_BP_RP - rgb_luminous_BP_RP) ** 2) + ((iso_luminous_G - rgb_luminous_G)**2) + ((iso_dim_BP_RP - rgb_dimmest_BP_RP) ** 2) + ((iso_dim_G - rgb_dimmest_G)**2)

        pythag_dist = np.sqrt(diff)

        lum_diff = (iso_luminous_BP_RP - rgb_luminous_BP_RP) ** 2 + (iso_luminous_G - rgb_luminous_G)**2
        dim_diff = (iso_dim_BP_RP - rgb_dimmest_BP_RP) ** 2 + (iso_dim_G - rgb_dimmest_G)**2


        pythag_dist = np.sqrt(lum_diff) + np.sqrt(dim_diff) 

        # EAF - finding slope between 2 lines:
        cluster_slope = (rgb_luminous_G - rgb_dimmest_G) / (rgb_luminous_BP_RP - rgb_dimmest_BP_RP )
        isochrone_slope = (iso_luminous_G - iso_dim_G) / (iso_luminous_BP_RP - iso_dim_BP_RP)

        distances.append(pythag_dist)
        slopes.append(cluster_slope - isochrone_slope)

        print('alpha =', alpha)
        print('Pythag distance =', pythag_dist)
        print(f'The difference between slopes is {cluster_slope - isochrone_slope}')


        # EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE
        amlt = r"$\alpha_{MLT}$"


        # # textstr = f'Pythagorean Distance = {round(pythag_dist, 3)}'

        # # props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
        
        # # # place a text box in bottom right in axes coords
        # # ax_curve.text(0.03, 0.97, textstr, transform=ax_curve.transAxes, fontsize=14,
        # #         verticalalignment='top', bbox=props)

        
        textstr = f'{amlt} = {alpha}'
        
        # these are matplotlib.patch.Patch properties
        # props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
        props = dict(boxstyle='round', facecolor='mediumpurple', alpha=0.2)
        
        # place a text box in bottom right in axes coords
        # ax_curve.text(0.03, 0.9, textstr, transform=ax_curve.transAxes, fontsize=15, verticalalignment='top', bbox=props)
        ax_curve.text(0.03, 0.97, textstr, transform=ax_curve.transAxes, fontsize=15, verticalalignment='top', bbox=props)

        ax_curve.tick_params(labelsize=13)
        ax_curve.set_ylim(15,12.5)


        # ax_curve.set_title('Including Silver Target')


        # cbar.ax.tick_params(labelsize=13)

        ax_curve.set_xlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
        ax_curve.set_ylabel('G', fontsize=15)
        
        plt.xlim(0.89,2.1)

        if CLASSIFICATION_COLOR == 'Silver' and save == True:
            plt.savefig(f'figures/NGC6791/best_fit_metrics/curvature_rgb/png/silver/NGC6791_a{alpha}_curvature_silver.png', dpi=300)
            plt.savefig(f'figures/NGC6791/best_fit_metrics/curvature_rgb/pdf/silver/NGC6791_a{alpha}_curvature_silver.pdf')

        elif CLASSIFICATION_COLOR == 'Gold' and save == True:
            plt.savefig(f'figures/NGC6791/best_fit_metrics/curvature_rgb/png/gold/NGC6791_a{alpha}_curvature_gold.png', dpi=300)
            plt.savefig(f'figures/NGC6791/best_fit_metrics/curvature_rgb/pdf/gold/NGC6791_a{alpha}_curvature_gold.pdf')

        plt.show()

    slopes = np.array(slopes)
    distances = np.array(distances)

    rgb_slopes = np.array(slopes)
    rgb_pythag_distances = np.array(distances)

    if math.isnan(rgb_slopes[0]):
        rgb_slopes[0] = 100000000

    rgb_best_slope = np.argmin(np.abs(rgb_slopes))
    rgb_best_dist = np.argmin(rgb_pythag_distances)

    

    txt = f"""
    ---------------------------------------------------------------------------------------------
    RGB Curvature {CLASSIFICATION_COLOR} Targets:
    ---------------------------------------------------------------------------------------------
    The most similar slope has a mixing length parameter of {alpha_mlt[rgb_best_slope]}
    The smallest Pythagorean distance has mixing length parameter of {alpha_mlt[rgb_best_dist]}
    ---------------------------------------------------------------------------------------------
    """

    print(txt)

    return txt


if __name__ == '__main__':
    silver = rgb_curvature('Silver', save_choice = True)
    # gold = rgb_curvature('Gold', save_choice = True)

    print("#"*150)

    print(silver)
    # print(gold)