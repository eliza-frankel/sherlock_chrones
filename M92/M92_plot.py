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
import csv
import bcutil

from statsmodels.nonparametric.smoothers_lowess import lowess
import seaborn as sns
from scipy.interpolate import CubicSpline, interp1d
from matplotlib.colors import ListedColormap

cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DCCD7D', '#E4A05A', '#DAA9D6', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']

new_cmap = ListedColormap(cb_colors_16)

color = [new_cmap(i) for i in range(new_cmap.N)]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)
# norm = mpl.colors.BoundaryNorm(boundaries, new_cmap.N) # to get new_cmap to work for a cbar, NEED this line in the body

if __name__ == '__main__':


    Fe_H = '-2.30'  # M92
    metallicity = '0.000145'
    cluster = 'M92'

    amlt = r"$\alpha_{MLT}$"

    cluster_path = '/Users/elizafrankel/Desktop/queries/FINAL_M92.csv'



    directories = 'M92/data_M92/final/'

    age = 13.8

    files = glob(directories + f'isochrone_age{age}Gyr*.csv')
    files.sort()

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # alpha_mlt = ['1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

    path_to_cluster_data = '/Users/elizafrankel/Desktop/queries/FINAL_M92.csv'



    Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

    M92_EBV = 0.02

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, M92_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    # d = fn.distance_modulus(8480)  #  M92 9.48 kpc from the absolute age of M92
    d = fn.distance_modulus(8501)  # Baumgardt & Vasiliev 2021
    print(f"Distance modulus for M92 is {d}")

#     fig, ax = plt.subplots(figsize=(6,8))
#     ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.3)



    for INDEX, file in enumerate(files):


        alpha = alpha_mlt[INDEX]

        print(alpha)

        track_num, T_eff, luminosity, mass, logg = fn.create_data_array(file)

        interp_temperature, interp_Y_val = fn.interpolation_time(T_eff, luminosity, track_num, method='pchip')
        _, interp_logg = fn.interpolation_time(T_eff, logg, track_num, method='pchip')
        
        ridgeline = pd.read_csv('M92_ridgeline_pts.csv')
        ridge_x = ridgeline["x"].to_numpy()
        ridge_y = ridgeline["y"].to_numpy()

        mask = [~np.isnan(ridge_x)][0]
        
        ridge_x = ridge_x[mask]
        ridge_y = ridge_y[mask]

        fig, ax = plt.subplots(figsize=(6,8))
        ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.3)

        # fig, ax = plt.subplots(nrows = 1, ncols=2, sharey = True, figsize = (8, 8), gridspec_kw={'width_ratios':[3, 1.5]})
        # plt.subplots_adjust(wspace = 0.0)
        # ax, ax2 = ax[0], ax[1]

        # ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.3)
        # # ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='k', alpha=0.3)
        



        # for i in range(len(T_eff)):

        #     if logg[i] < 0:
        #         logg[i] = 0

        #     print(T_eff[i], logg[i])

        #     # Teff, log(g), [Fe/H], E(B-V)
        #     mybc=bcutil.bcstar('',10**T_eff[i],logg[i],-2.30,M92_EBV,Rv=3.1,filters='G3 BP3 RP3',retarr=True)
        #     print(mybc)

        #     with open(f'EBV0.02_a{alpha}_M92_BC_Casagrande_VandenBerg.csv', 'a') as out:
        #         writer = csv.writer(out)
        #         if i == 0:
        #             writer.writerow(['BC_G3, BC_BP3, BC_RP3'])
        #         writer.writerow(mybc[0])  # temp


        df = pd.read_csv(f'M92/BCs/EBV0.02_a{alpha}_M92_BC_Casagrande_VandenBerg.csv', skiprows=[0], header=None)
        CV_BC_G = df[0].to_numpy()
        CV_BC_BP = df[1].to_numpy()
        CV_BC_RP = df[2].to_numpy()



        # # # TEFF TO FLUX (TO LUMINOSITY)

        r_sun_parsecs = 4.848102e-6  # 1 AU in pc
        T_sun_K = 5770
        solar_flux_ratio = (r_sun_parsecs ** 2) * (T_sun_K ** 4)

        r_M92_parsecs = 8200



        BC_BP_RP = CV_BC_BP - CV_BC_RP
        BC_BP_RP = BC_BP_RP[~np.isnan(BC_BP_RP)]

        BC_BP_cut = CV_BC_BP[~np.isnan(CV_BC_BP)]
        BC_RP_cut = CV_BC_RP[~np.isnan(CV_BC_RP)]
        BC_G_cut = CV_BC_G[~np.isnan(CV_BC_G)]


        interp_temperature, interp_Y_val = fn.interpolation_time(T_eff[~np.isnan(CV_BC_BP)], luminosity[~np.isnan(CV_BC_BP)], track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)
        _, interp_logg = fn.interpolation_time(T_eff[~np.isnan(CV_BC_BP)], logg[~np.isnan(CV_BC_BP)], track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)

        _, interp_BC_G = fn.interpolation_time(BC_G_cut, BC_G_cut, track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)
        interp_BC_BP, interp_BC_RP = fn.interpolation_time(BC_BP_cut, BC_RP_cut, track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)


        Mbol_L_cut = 4.74 - 2.5 * interp_Y_val #luminosity[~np.isnan(CV_BC_BP)]
        M = Mbol_L_cut - interp_BC_G
        m = d + M



        T_M92_K = interp_temperature
        M92_flux_ratio = (r_M92_parsecs ** 2) * (T_M92_K ** 4)
        M92_sun_ratio = M92_flux_ratio / solar_flux_ratio
        Mbol_teff_cut = 4.74 - 2.5 * np.log10(M92_sun_ratio)

        M_teff_BP = Mbol_teff_cut - interp_BC_BP
        M_teff_RP = Mbol_teff_cut - interp_BC_RP

        m_teff = (d + M_teff_BP) - (d + M_teff_RP)

        MSTO_index = np.argmin(m_teff)
        # From ridgeline code
        # MSTO_ridgeline_x = 0.57915729
        # MSTO_ridgeline_y = 18.51566486

        # MSTO_ridgeline_x = 0.57
        # MSTO_ridgeline_x = 0.57915729
        MSTO_ridgeline_x = 0.575
        MSTO_ridgeline_y = 18.45
        # MSTO_ridgeline_x = 0.57965213
        # MSTO_ridgeline_y = 18.51566427

        # MSTO_ridgeline_x = 0
        # MSTO_ridgeline_y = 0

        x_diff = m_teff[MSTO_index] - MSTO_ridgeline_x
        y_diff = m[MSTO_index] - MSTO_ridgeline_y
        
        # x_diff = 0
        # y_diff = 0

        # M92 MSTO is 0.57973015, 18.51566486 via ridgeline method

        ax.plot(m_teff - x_diff, m - y_diff, label = f'a{alpha}', color=color[INDEX], linewidth=2)
        # ax.plot(m_teff - x_diff, m - y_diff, label = f'a{alpha}', color='purple', linewidth=2)
        # ax.scatter(m_teff[MSTO_index] - x_diff, m[MSTO_index] - y_diff, marker='*', s=100)
        # ax.set_xlim(-0.45, 1.8)

        # #####################################################################################################################################

        # # THE FOLLOWING LINES (UNTIL 324 ARE FOR THE RIDGELINE EUCLIDIAN DISTANCE METHOD)

        # high_mag = [ridge_y < MSTO_ridgeline_y][0]
        # temp = m_teff - x_diff
        # temp_y = m - y_diff
        # high_mag_iso = [temp_y < MSTO_ridgeline_y][0]

        # ridge_x_high = ridge_x[high_mag]
        # ridge_y_high = ridge_y[high_mag]

        # iso_x_high = temp[high_mag_iso]
        # iso_y_high = temp_y[high_mag_iso]

        # sum_dist = 0


        # mags = np.linspace(min(ridge_y), MSTO_ridgeline_y, 1000)

        # for i in range(len(mags) - 1):
        #     ridge_indices = np.where(np.logical_and(ridge_y_high>=mags[i], ridge_y_high<=mags[i+1]))
        #     iso_indices = np.where(np.logical_and(iso_y_high>=mags[i], iso_y_high<=mags[i+1]))

        #     binned_ridge_x = np.array(ridge_x_high[ridge_indices])
        #     binned_iso_x = np.array(iso_x_high[iso_indices])

        #     avg_bin_ridge = np.mean(binned_ridge_x)
        #     avg_bin_iso = np.mean(binned_iso_x)


        #     diff = avg_bin_iso - avg_bin_ridge
        #     if ~np.isnan(diff):
        #         sum_dist += (diff ** 2)

        #     ax2.scatter(diff, mags[i], marker='.')

        # print(np.sqrt(sum_dist))

        # # # THIS IS A BOX FOR INFORMATION; LIKE A LEGEND BUT HARDCODED IN
        # textstr = f'Euclidian Distance = {round(np.sqrt(sum_dist), 3)}'
        # # these are matplotlib.patch.Patch properties
        # props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
        
        # # place a text box in top center of residual plot
        # ax2.text(1.025, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        #         verticalalignment='top', bbox=props)


        # ax.plot(ridge_x, ridge_y, color='hotpink', label='ridgeline')

        # ax2.set_xlim(-1, 1)
        # ax2.axvline(x=0, color='lightgrey', linestyle='dotted', zorder=0)

        # txt = r'$\Delta$ (G$_{BP}$ - G$_{RP}$)$_{isochrone - ridgeline}$'
        
        # ax2.set_xlabel(txt)
        # ax2.tick_params(labelsize=13)

        # #####################################################################################################################################

        ax.set_xlabel(r'G$_{BP}$ - G$_{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)
        ax.tick_params(labelsize=13)

        # EAF - writing the box with info about the cluster

        metallicity = '0.000145'

        textstr = '\n'.join((
        f'z = {metallicity}',
        f'[Fe/H] = {Fe_H}'))

        props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.895, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        textstr = f'{cluster} - {age} Gyr'

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=18,
                verticalalignment='top', bbox=props)
        
        textstr = f'{amlt} = {alpha}'
        
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.79, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        ax.tick_params(labelsize=13)

                


        # ax.invert_yaxis()
        # # plt.plot()
        # # plt.legend()
        # # plt.savefig(f'M92_plots/pdf/M92_a{alpha}.pdf')
        # # plt.savefig(f'M92_plots/M92_a{alpha}_distance_offset.png', dpi=300)
        # plt.savefig(f'M92_plots/pdf/M92_all.pdf')
        # plt.savefig(f'M92_plots/M92_all.png', dpi=300)
        # plt.show()








                # M_teff_BP = M_bol_teff - BC_BP
                # M_teff_RP = M_bol_teff - BC_RP

                # # M_teff = M_bol_teff - (BC_BP - BC_RP)
                # M_teff = M_teff_BP - M_teff_RP
                # # m_teff = d + M_teff
                # m_teff = (d + M_teff_BP) - (d + M_teff_RP)

                # ax.plot(m_teff, m, label = f'a{alpha}')

                # fn.annotate(m_teff, m, [BC_G_cut, BC_BP_cut-BC_RP_cut], ax, fig, label_text=['BC_G = {}', 'BC(BP-RP) = {}'])


        # cmap boundaries so ticks appear in center of cbar:
        alpha_mlt_float = np.array(alpha_mlt_float)
        step = 0.1
        boundaries = np.concatenate([
                [alpha_mlt_float[0] - step/2],
                (alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
                [alpha_mlt_float[-1] + step/2]
        ])


        new_cmap = ListedColormap(cb_colors_16)

        color = [new_cmap(i) for i in range(new_cmap.N)]
        norm = mpl.colors.BoundaryNorm(boundaries, new_cmap.N)
        
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap),
                ax=ax, ticks=alpha_mlt_float, boundaries=boundaries, orientation='vertical',
                label=r"$\alpha_{MLT}$")

        cbar.ax.tick_params(labelsize=13)

        ax.set_xlabel(r'G$_{BP}$ - G$_{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)

        ax.set_xlim(-0.6, 1.85)

        ax.invert_yaxis()
        #     # plt.plot()
        #     # plt.legend()
        #     # plt.savefig(f'M92_plots/pdf/M92_a{alpha}.pdf')
        #     # plt.savefig(f'M92_plots/png/M92_a{alpha}.png', dpi=300)
        #     plt.savefig(f'M92_plots/pdf/M92_all_pinned.pdf')
        #     plt.savefig(f'M92_plots/png/M92_all_pinned.png', dpi=300)
        plt.show()


    metallicity = '0.000145'

    textstr = '\n'.join((
    f'z = {metallicity}',
    f'[Fe/H] = {Fe_H}'))

    props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=15,
            verticalalignment='top', bbox=props)

    textstr = f'{cluster} - {age} Gyr'
   
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=18,
            verticalalignment='top', bbox=props)
    
    ax.tick_params(labelsize=13)
    
    # plt.legend()

#     # # ax.plot(interp_temperature*-1 + 5, m, label = 'a1.00')
#     ax.invert_yaxis()
#     plt.savefig('M92_all_isochrones_withBC.pdf')
#     plt.show()




#############################################################################################################################################################
#############################################################################################################################################################
################################################################### PINNED AND NOT PINNED ###################################################################
#############################################################################################################################################################
#############################################################################################################################################################

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]



    fig, ax = plt.subplots(nrows=1, ncols=3, sharex=False, sharey = True, figsize=(14,8), gridspec_kw={'width_ratios':[3, 3, 3.5]})
    plt.subplots_adjust(wspace = 0.0)
    ax, ax2, ax3 = ax[0], ax[1], ax[2]

    # EAF - plot Gaia data on all plots
    ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.25) #, zorder=20)
    ax2.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.25) #, zorder=20)
    ax3.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.25) #, zorder=20)

    new_cmap = ListedColormap(cb_colors_16)

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)

    print(files)

    for INDEX, file in enumerate(files):


        alpha = alpha_mlt[INDEX]

        print(alpha)

        track_num, T_eff, luminosity, mass, logg = fn.create_data_array(file)

        interp_temperature, interp_Y_val = fn.interpolation_time(T_eff, luminosity, track_num, method='pchip')
        _, interp_logg = fn.interpolation_time(T_eff, logg, track_num, method='pchip')

        amlt = r"$\alpha_{MLT}$"

        df = pd.read_csv(f'M92/BCs/EBV0.02_a{alpha}_M92_BC_Casagrande_VandenBerg.csv', skiprows=[0], header=None)
        CV_BC_G = df[0].to_numpy()
        CV_BC_BP = df[1].to_numpy()
        CV_BC_RP = df[2].to_numpy()



        # # # TEFF TO FLUX (TO LUMINOSITY)

        r_sun_parsecs = 4.848102e-6  # 1 AU in pc
        T_sun_K = 5770
        solar_flux_ratio = (r_sun_parsecs ** 2) * (T_sun_K ** 4)

        r_M92_parsecs = 8200



        BC_BP_RP = CV_BC_BP - CV_BC_RP
        BC_BP_RP = BC_BP_RP[~np.isnan(BC_BP_RP)]

        BC_BP_cut = CV_BC_BP[~np.isnan(CV_BC_BP)]
        BC_RP_cut = CV_BC_RP[~np.isnan(CV_BC_RP)]
        BC_G_cut = CV_BC_G[~np.isnan(CV_BC_G)]


        interp_temperature, interp_Y_val = fn.interpolation_time(T_eff[~np.isnan(CV_BC_BP)], luminosity[~np.isnan(CV_BC_BP)], track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)
        _, interp_logg = fn.interpolation_time(T_eff[~np.isnan(CV_BC_BP)], logg[~np.isnan(CV_BC_BP)], track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)

        _, interp_BC_G = fn.interpolation_time(BC_G_cut, BC_G_cut, track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)
        interp_BC_BP, interp_BC_RP = fn.interpolation_time(BC_BP_cut, BC_RP_cut, track_num[~np.isnan(CV_BC_BP)], method='pchip', increments=1667)


        Mbol_L_cut = 4.74 - 2.5 * interp_Y_val #luminosity[~np.isnan(CV_BC_BP)]
        M = Mbol_L_cut - interp_BC_G
        m = d + M



        T_M92_K = interp_temperature
        M92_flux_ratio = (r_M92_parsecs ** 2) * (T_M92_K ** 4)
        M92_sun_ratio = M92_flux_ratio / solar_flux_ratio
        Mbol_teff_cut = 4.74 - 2.5 * np.log10(M92_sun_ratio)

        M_teff_BP = Mbol_teff_cut - interp_BC_BP
        M_teff_RP = Mbol_teff_cut - interp_BC_RP

        m_teff = (d + M_teff_BP) - (d + M_teff_RP)

        MSTO_index = np.argmin(m_teff)


        MSTO_ridgeline_x = 0.575
        MSTO_ridgeline_y = 18.45

        # MSTO_ridgeline_y = 0

        x_diff = m_teff[MSTO_index] - MSTO_ridgeline_x
        y_diff = m[MSTO_index] - MSTO_ridgeline_y


        ax3.plot(m_teff - x_diff, m - y_diff, label = f'a{alpha}', linewidth = 2, zorder=16-INDEX)
        ax2.plot(m_teff, m, label = f'a{alpha}', linewidth = 2, zorder=16-INDEX)

    # EAF - THIS IS FOR DISPLAYING POINTS A, B, AND C ON M92
    # These points are from metrics_M92.py

    cluster_MSTO_BP_RP = 0.5813
    cluster_MSTO_G = 18.182

    cluster_SGB_BP_RP = 0.829
    cluster_SGB_G = 17.432

    cluster_TRGB_BP_RP = 1.5630689113726766
    cluster_TRGB_G = 11.555539162351607

    ax.scatter(cluster_MSTO_BP_RP, cluster_MSTO_G, marker='o', color='k')
    plt.text(0.37, 0.3, 'A', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)

    ax.scatter(cluster_SGB_BP_RP, cluster_SGB_G, marker='o', color='k')
    plt.text(0.5, 0.37, 'B', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)

    ax.scatter(cluster_TRGB_BP_RP, cluster_TRGB_G, marker='o', color='k')
    plt.text(0.86, 0.95, 'C', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, weight='bold', fontsize=15)




    # EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE

    ax3.scatter(MSTO_ridgeline_x, MSTO_ridgeline_y, c='k', marker='*', s=150, zorder=100)

    textstr = f'M92 - {age} Gyr'
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=15,
            verticalalignment='top', bbox=props)

    textstr = '\n'.join((
    f'z = {metallicity}',
    f'[Fe/H] = {Fe_H}'))

    props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=15,
            verticalalignment='top', bbox=props)
    
    ax.tick_params(labelsize=13)
    ax2.tick_params(labelsize=13)
    ax3.tick_params(labelsize=13)

    ax.set_xlim(-0.3, 1.7)
    ax2.set_xlim(-0.3, 1.9)
    ax3.set_xlim(-0.3, 1.9)

    # cmap boundaries so ticks appear in center of cbar:
    alpha_mlt_float = np.array(alpha_mlt_float)
    step = 0.1
    boundaries = np.concatenate([
        [alpha_mlt_float[0] - step/2],
        (alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
        [alpha_mlt_float[-1] + step/2]
    ])
    
    
    # cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap),
    #         ax=ax3, ticks=alpha_mlt_float, boundaries=boundaries, orientation='vertical')
    # cbar.set_label(label=r"$\alpha_{\rm MLT}$", size=15)

    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap),
		ax=ax3, boundaries=boundaries, orientation='vertical', ticks=alpha_mlt_float)
    cbar.set_label(label=r"$\alpha_{\rm MLT}$", size=15)


    cbar.ax.tick_params(labelsize=13)

    ax.set_xlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
    ax2.set_xlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
    ax3.set_xlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
    ax.set_ylabel('G', fontsize=15)

    plt.gca().invert_yaxis()
    plt.savefig(f'M92_both_offset_and_no.png', dpi=300)
    plt.savefig(f'M92_both_offset_and_no.pdf')
    plt.show()






# ############################################################################################################
# ############################################################################################################
# ############################################################################################################
# ############################################################################################################
# # RIDGELINE
# ############################################################################################################
# ############################################################################################################
# ############################################################################################################
# ############################################################################################################


# """
# M92 ridgeline MSTO = [0.57973015, 18.51566486]
# """


# path = '~/Desktop/m92.csv'

# Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path)


# M92_EBV = 0.02

# A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, M92_EBV, Xname='BPRP')
# A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)



# BP_RP_corrected = BP_RP_gaia - A_BP + A_RP
# G_corrected = Gmag_gaia - A_G


# # Ridgeline code
# lower_limit_G, upper_limit_G, color_index_upper_lim = 20, 10, 1.5  #hard limits for the photometric parameters

# arr = np.column_stack((BP_RP_corrected, G_corrected))
# arr = arr[(arr[:, 1] < lower_limit_G) & ~((arr[:, 0] < color_index_upper_lim) & (arr[:, 1] < upper_limit_G))]

# df = pd.DataFrame(arr, columns=['bprp', 'gmag']).dropna().sort_values('gmag')
# df[['ridge_bprp', 'ridge_gmag']] = lowess(df['bprp'], df['gmag'], frac=0.2)[:, [1, 0]]
# blue_x, blue_y = df.loc[df['ridge_bprp'].idxmin(), ['ridge_bprp', 'ridge_gmag']]


# def numerical_derivative(x, y):
#     x, y = np.asarray(x), np.asarray(y)
#     d = np.zeros_like(y)
#     d[0] = (y[1] - y[0]) / (x[1] - x[0])
#     d[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
#     d[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
#     return d

# def rotate_points(x, y, rx, ry, inverse=False):
#     a = np.arctan(numerical_derivative(ry, rx))
#     if inverse:
#         a = -a
#     c, s = np.cos(a), np.sin(a)
#     x_rot = x * c - y * s
#     y_rot = x * s + y * c
#     if not inverse:
#         y_rot += ry
#     return x_rot, y_rot

# # --- Rotation and Binning ---
# df[['x_new', 'y_new']] = np.column_stack(
#     rotate_points(df['bprp']-df['ridge_bprp'], df['gmag']-df['ridge_gmag'], df['ridge_bprp'], df['ridge_gmag'])
# )
# df["x_new0"] = 0
# df = df.sort_values(by='y_new')

# bins = np.array([11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.25, 17.5, 17.75, 18.5, 19.5]) #Adjust the bins as needed
# # # bins = np.array([13.5, 14, 14.5, 15, 15.5, 16, 16.5, 16.75, 17, 17.5, 18, 18.5,  19.25])
# # # bins = np.array([13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5])
# # bins = np.array([13, 14, 15, 16, 17, 19])

# # bins = np.array([13.5, 14, 14.5, 15, 15.5, 16, 16.5, 16.75, 17, 17.5, 18, 18.5, 19]) #Adjust the bins as needed
# # bins = np.array([13.5, 14.5, 15.5, 16, 16.1, 16.25, 16.5, 17, 17.5,  18, 18.5, 19.5])

# bin_labels = [str(b) for b in bins[:-1]]
# df['bin'] = pd.cut(df['y_new'], bins=bins, labels=bin_labels, right=False)

# # --- KDE Calculation ---
# def calculate_kde(df, column, y_column, bandwidth='scott'):
#     results = []
#     for bin_label, group in df.groupby('bin', observed=False):
#         if group[column].empty:
#             continue
#         fig, ax = plt.subplots()
#         kde_plot = sns.kdeplot(group[column], bw_method=bandwidth, ax=ax)
#         xxx, yyy = kde_plot.lines[0].get_data()
#         plt.close(fig)
#         idx_max = pd.Series(yyy).idxmax()
#         results.append({
#             'bin': bin_label,
#             'x_at_max_density': xxx[idx_max],
#             'median_y': group[y_column].median()
#         })
#     return results

# kde_results = calculate_kde(df, 'x_new', 'y_new')
# results_df = pd.DataFrame(kde_results).sort_values(by='median_y')
# y_sorted = results_df['median_y'].values
# x_sorted = results_df['x_at_max_density'].values

# # --- Interpolation and Inverse Rotation ---
# cs = CubicSpline(y_sorted, x_sorted)
# mask = (df['y_new'] >= bins[0]) & (df['y_new'] < bins[-1])
# df.loc[mask, 'x_interpolate'] = cs(df.loc[mask, 'y_new'])
# df.loc[~mask, 'x_interpolate'] = np.nan  

# df['x_back2'], df['y_back2'] = rotate_points(
#     df['x_interpolate'], df['y_new'] - df['ridge_gmag'], df['ridge_bprp'], df['ridge_gmag'], inverse=True
# )
# df['x_back2'] += df['ridge_bprp']
# df['y_back2'] += df['ridge_gmag']

# # --- Final Sorting and Linear Interpolation ---
# df_sorted = df[['x_back2', 'y_back2']].sort_values(by='y_back2').dropna().reset_index(drop=True)
# x_sorted = df_sorted['x_back2'].values
# y_sorted = df_sorted['y_back2'].values
# linear_interp = interp1d(y_sorted, x_sorted, kind='linear', fill_value="extrapolate")
# y_fine2 = np.linspace(y_sorted.min(), y_sorted.max(), 10000)
# x_fine2 = linear_interp(y_fine2)


# # PLOTTING

# # # Set the font size and family for the plot
# # plt.rcParams.update({'font.size': 20})
# # #plt.rcParams["font.family"] = "Liberation Serif" ## specital font family, can be changed to any other font family installed on the system

# # Set the point size and transparency
# s = 3
# alpha = 0.5

# fig, axs = plt.subplots(2, 2, figsize=(9, 9))

# # Top left: CMD with primary ridgeline
# axs[0, 0].invert_yaxis()
# #axs[0, 0].set_xlim(0.75, 1.5)
# axs[0, 0].scatter(df['bprp'], df['gmag'], s=s, c='grey', alpha=alpha)
# axs[0, 0].plot(df['ridge_bprp'], df["ridge_gmag"], c="black", lw=3, label="primary ridgeline")
# axs[0, 0].set_xlabel('$G_{BP}-G_{RP}$ [mag]')
# axs[0, 0].set_ylabel('$G$ [mag]')
# axs[0, 0].legend(loc='upper left')

# # Top right: Rotated CMD with primary ridgeline
# axs[0, 1].invert_yaxis()
# #axs[0, 1].set_xlim(-0.6, 0.4)
# axs[0, 1].scatter(df['x_new'], df['y_new'], s=s, color='grey', alpha=alpha)
# axs[0, 1].plot(df['x_new0'], df['y_new'], c="black", lw=3, label="primary ridgeline")
# axs[0, 1].set_xlabel('relative color')
# axs[0, 1].set_ylabel('$G$ [mag]')
# axs[0, 1].legend(loc='upper left')

# # Bottom left: Rotated CMD with KDE maxima and interpolated curve
# axs[1, 0].invert_yaxis()
# #axs[1, 0].set_xlim(-0.6, 0.4)
# axs[1, 0].set_ylim(20, 11)
# axs[1, 0].scatter(df['x_new'], df['y_new'], s=s, color='grey', alpha=alpha)
# axs[1, 0].scatter(results_df['x_at_max_density'].values, results_df['median_y'].values, edgecolor='black', color='navy', zorder=3, label="interpolating points")
# axs[1, 0].plot(df['x_interpolate'], df['y_new'], c="darkorange", zorder=1, lw=3, label="corrected ridgeline")
# axs[1, 0].set_xlabel('relative color')
# axs[1, 0].set_ylabel('$G$ [mag]')
# axs[1, 0].legend(loc='upper left')


# x_df_np = df['x_back2'].to_numpy()
# x_df = x_df_np[~np.isnan(x_df_np)]

# y_df_np = df['y_back2'].to_numpy()
# y_df = y_df_np[~np.isnan(y_df_np)]



# MSTO_point = np.argmax(x_df)
# print(MSTO_point)
# print(x_df[MSTO_point], np.min(x_df))

# MSTO_point = np.where(x_df==np.min(x_df))

# # Bottom right: CMD with corrected ridgeline
# axs[1, 1].invert_yaxis()
# #axs[1, 1].set_xlim(0.75, 1.5)
# axs[1, 1].scatter(df['bprp'], df['gmag'], s=s, color='grey', alpha=alpha)
# axs[1, 1].plot(df['x_back2'], df['y_back2'], color='darkorange', lw=3, label="corrected ridgeline")

# # axs[1, 1].scatter(df['x_back2'][TEMP[0]], df['y_back2'][TEMP[0]])
# axs[1, 1].scatter(x_df[MSTO_point[0]], y_df[MSTO_point[0]])

# print(x_df[MSTO_point[0]], y_df[MSTO_point[0]])

# ridgeline_datapts = pd.DataFrame(list(zip(df['x_back2'], df['y_back2'])), columns = ['x', 'y'])
# csv_name = f'M92_ridgeline_pts.csv'
# csv_save = ridgeline_datapts.to_csv(csv_name)

# axs[1, 1].set_xlabel('$G_{BP}-G_{RP}$ [mag]')
# axs[1, 1].set_ylabel('$G$ [mag]')
# axs[1, 1].legend()

# ## Add annotation for the panels a, b, c, d
# axs[0, 0].annotate('A', xy=(0.96, 0.96), xycoords='axes fraction', fontsize=24, fontweight='bold',
#                   ha='right', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# axs[0, 1].annotate('B', xy=(0.96, 0.96), xycoords='axes fraction', fontsize=24, fontweight='bold',
#                   ha='right', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# axs[1, 0].annotate('C', xy=(0.96, 0.96), xycoords='axes fraction', fontsize=24, fontweight='bold',
#                   ha='right', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# axs[1, 1].annotate('D', xy=(0.96, 0.96), xycoords='axes fraction', fontsize=24, fontweight='bold',
#                   ha='right', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

# plt.tight_layout()
# #plt.savefig("ridgeline_analysis.png", dpi=300)
# plt.show()



# # plt.scatter()

    
