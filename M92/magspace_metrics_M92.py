#!/Users/elizafrankel/anaconda3/bin/python3

# Author: E. Frankel
# 5.16.2025


import sys
sys.path.insert(0, '/Users/elizafrankel/Desktop/Research/')
import functions as fn
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from glob import glob
import matplotlib.patches as patches





# M92
age = 13.8
Fe_H = '-2.30'
Fe_H_float = float(Fe_H)
metallicity = '0.000145'
cluster = 'M92'
cluster_folder = 'M92'
data = 'data_M92/final'
dist = 8501  # Baumgardt & Vasiliev 2021
cluster_EBV = 0.02
path_to_cluster_data = '/Users/elizafrankel/Desktop/queries/FINAL_M92.csv'

amlt = r"$\alpha_\text{MLT}$"



location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

age = 13.8

files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
files.sort()

alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
# alpha_mlt = ['1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

#     path_to_cluster_data = '/Users/elizafrankel/Desktop/m92.csv'


Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

M92_EBV = 0.02

A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, M92_EBV, Xname='BPRP')
A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

# d = fn.distance_modulus(8480)  #  M92 8.48 kpc from the absolute age of M92
d = fn.distance_modulus(8501)
print(f"Distance modulus for M92 is {d}")


# color = [plt.cm.tab20b_r(i) for i in range(plt.cm.tab20b.N)]
color = fn.get_cmap_colors('tab20b', 16)



#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################


def sgb_distance(dynamic='MSTO', save_choice=True):

    location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

    age = 13.8

    files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
    files.sort()

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]


    Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

    M92_EBV = 0.02

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, M92_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    # d = fn.distance_modulus(8480)  #  M92 8.48 kpc from the absolute age of M92
    d = fn.distance_modulus(8501)
    print(f"Distance modulus for M92 is {d}")


    # color = [plt.cm.tab20b_r(i) for i in range(plt.cm.tab20b.N)]
    color = fn.get_cmap_colors('tab20b', 16)

    sgb_pythag_distances = []
    sgb_slopes = []

    for INDEX, file in enumerate(files):


        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        alpha = alpha_mlt[INDEX]

        print(alpha)


        # # EAF - Plots the isochrone
        fig, ax = plt.subplots(figsize=(7.1,7))
        ax.plot(m_teff, m, label = f'a{alpha}', color='purple', linewidth=2, alpha=0.3)

        # EAF - Plots the data
        ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=30, c='grey', alpha=0.3)

        

        # # # # Step 1: Draw line on subgiant branch
        # # # # Define the SGB by eye
        cluster_MSTO_BP_RP = 0.5813
        cluster_MSTO_G = 18.182

        cluster_SGB_BP_RP = 0.829
        cluster_SGB_G = 17.432

        # Draw line for the cluster SGB
        ax.plot([cluster_MSTO_BP_RP, cluster_SGB_BP_RP], [cluster_MSTO_G, cluster_SGB_G], color='k', linewidth=3)

        ax.scatter(cluster_MSTO_BP_RP, cluster_MSTO_G, marker='o', color='k')
        ax.scatter(cluster_SGB_BP_RP, cluster_SGB_G, marker='o', color='k')
        plt.text(0.27, 0.26, 'A', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)
        plt.text(0.68, 0.84, 'B', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)



        # EAF - attempting to find MSTO point by comparing the cluster point to the isochrone
        index_msto, msto_turnoff_pt = fn.find_nearest(m, cluster_MSTO_G)

        if dynamic == 'both':
            index_rgbto, rgb_turnoff_pt = fn.find_nearest(m, cluster_SGB_G)

            iso_SGB_BP_RP = m_teff[index_rgbto]
            iso_SGB_G = m[index_rgbto]
        else:
            # EAF - defining where the RGB turn off is by finding the inflection point

            no_msto = [m[i] < 17.95 and m[i] > 17 for i in range(len(m))]

            p1 = np.array([m_teff[no_msto][0], m[no_msto][0]])
            p2 = np.array([m_teff[no_msto][-1], m[no_msto][-1]])

            line = p2 - p1
            line /= np.linalg.norm(line)

            points = np.column_stack((m_teff[no_msto], m[no_msto]))
            vecs = points - p1

            proj = np.outer(vecs @ line, line)
            perp = vecs - proj

            dist = np.linalg.norm(perp, axis=1)

            bend_idx = np.argmax(dist)

            iso_SGB_BP_RP = m_teff[no_msto][bend_idx]
            iso_SGB_G = m[no_msto][bend_idx]



        # EAF - officially defining the points

        iso_MSTO_BP_RP = m_teff[index_msto]
        iso_MSTO_G = m[index_msto]



        plt.plot(np.array([iso_MSTO_BP_RP, iso_SGB_BP_RP]), np.array([iso_MSTO_G, iso_SGB_G]), color='deepskyblue', linewidth=3)


        # EAF - finding slope:
        cluster_slope = (cluster_MSTO_G - cluster_SGB_G) / (cluster_MSTO_BP_RP - cluster_SGB_BP_RP )
        isochrone_slope = (iso_MSTO_G - iso_SGB_G) / (iso_MSTO_BP_RP - iso_SGB_BP_RP)

        sgb_slopes.append(cluster_slope - isochrone_slope)

        

        # # # Step 4: Calculate distance between the two lines
        # diff = ((iso_MSTO_BP_RP - cluster_MSTO_BP_RP) ** 2) + ((iso_MSTO_G - cluster_MSTO_G)**2) + ((iso_SGB_BP_RP - cluster_SGB_BP_RP) ** 2) + ((iso_SGB_G - cluster_SGB_G)**2)
        msto_diff = (iso_MSTO_BP_RP - cluster_MSTO_BP_RP) ** 2 + (iso_MSTO_G - cluster_MSTO_G)**2
        sgb_diff = (iso_SGB_BP_RP - cluster_SGB_BP_RP) ** 2 + (iso_SGB_G - cluster_SGB_G)**2


        # euclid_dist_old = np.sqrt(diff)
        euclid_dist = np.sqrt(msto_diff) + np.sqrt(sgb_diff)

        sgb_pythag_distances.append(euclid_dist)

        print('alpha =', alpha)
        print('pythag distance SGB =', euclid_dist)
        print(f'The difference between slopes is {cluster_slope - isochrone_slope}')
        print()



        # 4. Inset plot
        axinset = ax.inset_axes([0.4242, 17.35, 0.12, 0.4], transform=ax.transData)

        axinset.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.1)
        axinset.set_xlim(-0.3, 1.7)
        axinset.invert_yaxis()

        axinset.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        # Create a Rectangle patch
        rect = patches.Rectangle((0.4, 17.4), 0.5, 1.5, linewidth=1, edgecolor='r', facecolor='none')

        # Add the patch to the Axes
        axinset.add_patch(rect)

        ax.set_ylim(17.2,18.5)
        ax.set_xlim(0.4, 1.0)


        ax.set_xlabel(r'G$_\text{BP}$ - G$_\text{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)
        ax.tick_params(labelsize=13)

        # EAF - writing the box with info about the cluster

        metallicity = '0.000145'

        
        textstr = f'{amlt} = {alpha}'
        
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        ax.tick_params(labelsize=13)

                





        # cmap boundaries so ticks appear in center of cbar:
        alpha_mlt_float = np.array(alpha_mlt_float)
        step = 0.1
        boundaries = np.concatenate([
                [alpha_mlt_float[0] - step/2],
                (alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
                [alpha_mlt_float[-1] + step/2]
        ])


        ax.set_xlabel(r'G$_\text{BP}$ - G$_\text{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)

        ax.invert_yaxis()
        #     # plt.plot()
        #     # plt.legend()

        if dynamic == 'MSTO' and save_choice == True:
            plt.savefig(f'M92/figures/sgb_length/dynamic_iso_MSTO/pdf/M92_a{alpha}_sgb_length.pdf')
            plt.savefig(f'M92/figures/sgb_length/dynamic_iso_MSTO/png/M92_a{alpha}_sgb_length.png', dpi=300)
        elif dynamic == 'both' and save_choice == True:
            plt.savefig(f'M92/figures/sgb_length/dynamic_MSTO_RGBTO/pdf/M92_a{alpha}_sgb_length.pdf')
            plt.savefig(f'M92/figures/sgb_length/dynamic_MSTO_RGBTO/png/M92_a{alpha}_sgb_length.png', dpi=300)
        elif save_choice == True:
            plt.savefig(f'M92/figures/sgb_length/pdf/M92_a{alpha}_sgb_length.pdf')
            plt.savefig(f'M92/figures/sgb_length/png/M92_a{alpha}_sgb_length.png', dpi=300)
        
        
        plt.show()

    sgb_slopes = np.array(sgb_slopes)
    sgb_pythag_distances = np.array(sgb_pythag_distances)

    sgb_best_slope = np.argmin(np.abs(sgb_slopes))
    sgb_best_dist = np.argmin(sgb_pythag_distances)

    if dynamic == 'MSTO':
        msg = 'Only MSTO is dynamic'
    elif dynamic == 'both':
        msg = 'Both MSTO and RGBTO are dynamic'
    else:
        msg = ''

    txt = f"""
    ---------------------------------------------------------------------------------------------
    SGB length:
    {msg}
    ---------------------------------------------------------------------------------------------
    The most similar slope has a mixing length parameter of {alpha_mlt[sgb_best_slope]}
    The smallest Pythagorean distance has mixing length parameter of {alpha_mlt[sgb_best_dist]}
    ---------------------------------------------------------------------------------------------
    """

    print(txt)
    return txt

    #########################################################################################################################################################
    #########################################################################################################################################################
    #########################################################################################################################################################
    #########################################################################################################################################################
    #########################################################################################################################################################

    # EAF - this time we are going to align at the RGBTO rather than the MSTO

def rgb_curvature(dynamic = False, save_choice = True):

    location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

    age = 13.8

    files = glob(location + f'{cluster_folder}/mag_space/no_offset/a*_isochrone_coordinate_space_no_offset.csv')
    files.sort()

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]


    Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

    M92_EBV = 0.02

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, M92_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    # d = fn.distance_modulus(8480)  #  M92 8.48 kpc from the absolute age of M92
    d = fn.distance_modulus(8501)
    print(f"Distance modulus for M92 is {d}")


    # color = [plt.cm.tab20b_r(i) for i in range(plt.cm.tab20b.N)]
    color = fn.get_cmap_colors('tab20b', 16)



    rgb_pythag_distances = []
    rgb_slopes = []

    for INDEX, file in enumerate(files):


        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        alpha = alpha_mlt[INDEX]

        # M92 MSTO is 0.57973015, 18.51566486 via ridgeline method

        # # EAF - Plots the isochrone
        fig, ax = plt.subplots(figsize=(6,8))
        # ax.plot(m_teff, m, label = f'a{alpha}', color='purple', linewidth=2, alpha=0.25)
        # # EAF - Plots the data
        # ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.3)


        # no_rgb = [m > 16]

        # dy_dx = np.gradient(m_teff[no_rgb[0]], m[no_rgb[0]])

        # index_uhhh, uhhh = fn.find_nearest(dy_dx, 0)

        # # Step 1: Draw line on subgiant branch

        cluster_SGB_BP_RP = 0.829
        cluster_SGB_G = 17.432

        if dynamic == True:
            index_rgbto, rgb_turnoff_pt = fn.find_nearest(m, cluster_SGB_G)

            iso_SGB_BP_RP = m_teff[index_rgbto]
            iso_SGB_G = m[index_rgbto]

        else:
            no_msto = [m[i] < 17.95 and m[i] > 17 for i in range(len(m))]

            p1 = np.array([m_teff[no_msto][0], m[no_msto][0]])
            p2 = np.array([m_teff[no_msto][-1], m[no_msto][-1]])

            line = p2 - p1
            line /= np.linalg.norm(line)

            points = np.column_stack((m_teff[no_msto], m[no_msto]))
            vecs = points - p1

            proj = np.outer(vecs @ line, line)
            perp = vecs - proj

            dist = np.linalg.norm(perp, axis=1)

            bend_idx = np.argmax(dist)


            iso_SGB_BP_RP = m_teff[no_msto][bend_idx]
            iso_SGB_G = m[no_msto][bend_idx]



        

        # This is for RGBTO pinning
        x_diff = cluster_SGB_BP_RP - iso_SGB_BP_RP
        y_diff = cluster_SGB_G - iso_SGB_G


        # RGB SLOPE

        # finding the tip of the RGB of M92
        trgb_cluster = np.argmin(Gmag_gaia)
        cluster_TRGB_BP_RP = BP_RP_gaia[trgb_cluster] - A_BP[trgb_cluster] + A_RP[trgb_cluster]
        cluster_TRGB_G = Gmag_gaia[trgb_cluster] - A_G[trgb_cluster]

        ax.scatter(cluster_SGB_BP_RP, cluster_SGB_G, marker='o', color='k')
        plt.text(0.2, 0.05, 'B', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)

        ax.scatter(cluster_TRGB_BP_RP, cluster_TRGB_G, marker='o', color='k')
        plt.text(0.87, 0.93, 'C', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)

        # finding TRGB for isochrone
        trgb_iso = np.argmax(m_teff)
        iso_TRGB_BP_RP = m_teff[trgb_iso] 
        iso_TRGB_G = m[trgb_iso] 


        iso_TRGB_BP_RP = iso_TRGB_BP_RP + x_diff
        iso_TRGB_G = iso_TRGB_G + y_diff

        iso_SGB_BP_RP = iso_SGB_BP_RP + x_diff
        iso_SGB_G = iso_SGB_G + y_diff

        ax.plot(m_teff + x_diff, m + y_diff, label = f'a{alpha}', color='purple', linewidth=2, alpha=0.25)
        # EAF - Plots the data
        ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=30, c='grey', alpha=0.3)

        ax.plot(np.array([iso_TRGB_BP_RP, iso_SGB_BP_RP]), np.array([iso_TRGB_G, iso_SGB_G]), color='deepskyblue', linewidth=3, alpha=0.75, zorder=100)
        ax.plot([cluster_TRGB_BP_RP, cluster_SGB_BP_RP], [cluster_TRGB_G, cluster_SGB_G], color='k', linewidth=3, alpha=0.75)


        # # # Step 4: Calculate distance between the two lines

        trgb_diff = ((iso_TRGB_BP_RP) - cluster_TRGB_BP_RP) ** 2 + ((iso_TRGB_G) - cluster_TRGB_G)**2
        sgb_diff = ((iso_SGB_BP_RP) - cluster_SGB_BP_RP) ** 2 + ((iso_SGB_G) - cluster_SGB_G)**2


        # euclid_dist_old = np.sqrt(diff)
        euclid_dist = np.sqrt(trgb_diff) + np.sqrt(sgb_diff)

        # EAF - finding slope:
        cluster_slope = (cluster_TRGB_G - cluster_SGB_G) / (cluster_TRGB_BP_RP - cluster_SGB_BP_RP )
        isochrone_slope = (iso_TRGB_G - iso_SGB_G) / (iso_TRGB_BP_RP - iso_SGB_BP_RP)

        rgb_pythag_distances.append(euclid_dist)
        rgb_slopes.append(cluster_slope - isochrone_slope)

        print('alpha =', alpha)
        print('pythag distance TRGB =', euclid_dist)
        print(f'The difference between slopes is {cluster_slope - isochrone_slope}')
        print()

        # 4. Inset plot
        axinset = ax.inset_axes([0.64, 11.6, 0.2, 1.5], transform=ax.transData)

        axinset.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.1)
        axinset.invert_yaxis()
        axinset.set_xlim(-0.3, 1.7)

        axinset.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

        # Create a Rectangle patch
        rect = patches.Rectangle((0.7, 11.5), 0.9, 6, linewidth=1, edgecolor='r', facecolor='none')

        # Add the patch to the Axes
        axinset.add_patch(rect)

        ax.set_ylim(11, 18)
        ax.set_xlim(0.6, 1.6)


        ax.set_xlabel(r'G$_\text{BP}$ - G$_\text{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)
        ax.tick_params(labelsize=13)

        # EAF - writing the box with info about the cluster

        metallicity = '0.000145'

        # textstr = f'{cluster} - {age} Gyr'

        # # these are matplotlib.patch.Patch properties
        # props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
        
        # # place a text box in bottom right in axes coords
        # ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=18,
        #         verticalalignment='top', bbox=props)
        
        textstr = f'{amlt} = {alpha}'
        
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        ax.tick_params(labelsize=13)

                





        # cmap boundaries so ticks appear in center of cbar:
        alpha_mlt_float = np.array(alpha_mlt_float)
        step = 0.1
        boundaries = np.concatenate([
                [alpha_mlt_float[0] - step/2],
                (alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
                [alpha_mlt_float[-1] + step/2]
        ])

        # cmap = mpl.cm.tab20b
        # norm = mpl.colors.BoundaryNorm(boundaries, cmap.N)
        
        # cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        #         ax=ax, ticks=alpha_mlt_float, boundaries=boundaries, orientation='vertical',
        #         label=r"$\alpha_\text{MLT}$")

        # cbar.ax.tick_params(labelsize=13)

        ax.set_xlabel(r'G$_\text{BP}$ - G$_\text{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)

        ax.invert_yaxis()
        #     # plt.plot()
        #     # plt.legend()

        plt.savefig(f'M92/figures/rgb_slope/pdf/M92_a{alpha}_rgb_slope.pdf')
        plt.savefig(f'M92/figures/rgb_slope/png/M92_a{alpha}_rgb_slope.png', dpi=300)

        plt.show()

    rgb_slopes = np.array(rgb_slopes)
    rgb_pythag_distances = np.array(rgb_pythag_distances)

    rgb_best_slope = np.argmin(np.abs(rgb_slopes))
    rgb_best_dist = np.argmin(rgb_pythag_distances)

    if dynamic == False:
        msg = 'iso RGBTO aligned at cluster'
    elif dynamic == True:
        msg = 'iso RGBTO found dynamically (i.e. same Y as cluster)'

    txt = f"""
    ---------------------------------------------------------------------------------------------
    RGB Curvature:
    {msg}
    ---------------------------------------------------------------------------------------------
    The most similar slope has a mixing length parameter of {alpha_mlt[rgb_best_slope]}
    The smallest Pythagorean distance has mixing length parameter of {alpha_mlt[rgb_best_dist]}
    ---------------------------------------------------------------------------------------------
    """

    print(txt)
    

    plt.close()
    return txt

    #########################################################################################################################################################
    #########################################################################################################################################################
    #########################################################################################################################################################
    #########################################################################################################################################################
    #########################################################################################################################################################


    

    
if __name__ == '__main__':
    # EAF - to find best SGB fit
    msto = sgb_distance(dynamic='MSTO', save_choice=True)

    # EAF - to find RGB git
    not_dynamic = rgb_curvature(dynamic=False, save_choice=True)

    print('#'*150)
    print(msto)

    print('#'*150)
    print(not_dynamic)