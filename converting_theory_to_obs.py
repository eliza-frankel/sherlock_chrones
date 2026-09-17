#!/Users/elizafrankel/anaconda3/bin/python3

######################################################
#                                     
#          Converting log(L) & T_eff to Gaia mags
#                 Created: May 16, 2025  
#                Updated: August 16, 2026
#                 Author: Eliza Frankel       
#                                                             
######################################################


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




if __name__ == '__main__':

    # NGC 6791
    age = 8.3
    Fe_H = '0.31'
    Fe_H_float = float(Fe_H)
    metallicity = '0.034507'
    cluster = 'NGC 6791'
    cluster_folder = 'NGC6791'
    data = 'data_NGC6791/DONE/FINAL'
    dist = 4010  # Brogaard et al 2011
    cluster_EBV = 0.14
    path_to_cluster_data = '~/Desktop/queries/ngc6791/ngc6791_final_query.csv'
    HG_TARGETS = True  # This is to identify if there are holy grail targets; also is this NGC 6791? T or F
    # From ridgeline code
    MSTO_ridgeline_x = 0.86141087
    MSTO_ridgeline_y = 17.14 #17.00009422

    # # M92
    # age = 13.8
    # Fe_H = '-2.30'
    # Fe_H_float = float(Fe_H)
    # metallicity = '0.000145'
    # cluster = 'M92'
    # cluster_folder = 'M92'
    # data = 'data_M92/final'
    # dist = 8501  # Baumgardt & Vasiliev 2021
    # cluster_EBV = 0.02
    # path_to_cluster_data = '/Users/elizafrankel/Desktop/queries/FINAL_M92.csv'
    # HG_TARGETS = False
    # # From ridgeline code
    # MSTO_ridgeline_x = 0.575
    # MSTO_ridgeline_y = 18.45



    location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]


    files = glob(location + f'{cluster_folder}/{data}/isochrone_age{age}Gyr_z{metallicity}_a*.csv')
    files.sort()


    # EAF - reading in Gaia data from Topcat query
    Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

    # EAF - Gaia (E)DR3 extinction law from https://www.cosmos.esa.int/web/gaia/edr3-extinction-law
    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, cluster_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    r_cluster_parsecs = dist

    d = fn.distance_modulus(r_cluster_parsecs)

    print(f"Distance modulus for {cluster} is {d}")


    for INDEX, file in enumerate(files):


        fig, ax = plt.subplots(figsize=(6,8))

        alpha = alpha_mlt[INDEX]


        track_num, T_eff, luminosity, mass, logg = fn.create_data_array(file)

        interp_temperature, interp_Y_val = fn.interpolation_time(T_eff, luminosity, track_num, method='pchip')
        interp_mass, interp_logg = fn.interpolation_time(mass, logg, track_num, method='pchip')
        
        # EAF - Plotting cluster
        plt.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.25)

        if HG_TARGETS == True:

            RGB_objs = [2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808]

            AGB_questionables = [2051293319920668160, 2051105754413616000]

            fn.hg_targets(RGB_objs, source_ids, Gmag_gaia - A_G, BP_RP_gaia - A_BP + A_RP, ax, questionable_IDs=AGB_questionables, fig=fig)


        # # EAF - uncomment this for loop to calculate bolometric corrections for each track:

        # for i in range(len(T_eff)):

        #     if logg[i] < 0:
        #         logg[i] = 0

        #     print(T_eff[i], logg[i])

        #     # Teff, log(g), [Fe/H], E(B-V)
        #     print('',10**T_eff[i],logg[i],Fe_H_float,cluster_EBV)
        #     mybc=bcutil.bcstar('',10**T_eff[i],logg[i],Fe_H_float,cluster_EBV,Rv=3.1,filters='G3 BP3 RP3',retarr=True)
        #     print(mybc)

        #     with open(f'{cluster_folder}/BCs/EBV{cluster_EBV}_a{alpha}_{cluster_folder}_BC_Casagrande_VandenBerg.csv', 'a') as out:
        #         writer = csv.writer(out)
        #         if i == 0:
        #             writer.writerow(['BC_G3, BC_BP3, BC_RP3'])
        #         writer.writerow(mybc[0])  # temp

        # print(f'done with a{alpha}')

        # EAF - reading in BCs
        df = pd.read_csv(f'{cluster_folder}/BCs/EBV{cluster_EBV}_a{alpha}_{cluster_folder}_BC_Casagrande_VandenBerg.csv', skiprows=[0], header=None)



        CV_BC_G = df[0].to_numpy()
        CV_BC_BP = df[1].to_numpy()
        CV_BC_RP = df[2].to_numpy()


        # # # EAF - TEFF TO FLUX (TO LUMINOSITY)
        r_sun_parsecs = 4.848102e-6  # 1 AU in pc
        T_sun_K = 5770
        solar_flux_ratio = (r_sun_parsecs ** 2) * (T_sun_K ** 4)


        # EAF - this is cutting out all things where BC is a nan
        BC_BP_RP = CV_BC_BP - CV_BC_RP
        BC_BP_RP = BC_BP_RP[~np.isnan(BC_BP_RP)]

        BC_BP_cut = CV_BC_BP[~np.isnan(CV_BC_BP)]
        BC_RP_cut = CV_BC_RP[~np.isnan(CV_BC_RP)]
        BC_G_cut = CV_BC_G[~np.isnan(CV_BC_RP)]



        # EAF - interpolating only the points that have valid BCs
        interp_temperature, interp_Y_val = fn.interpolation_time(T_eff[~np.isnan(CV_BC_BP)], luminosity[~np.isnan(CV_BC_BP)], track_num[~np.isnan(CV_BC_BP)], method='pchip')
        _, interp_logg = fn.interpolation_time(mass[~np.isnan(CV_BC_BP)], logg[~np.isnan(CV_BC_BP)], track_num[~np.isnan(CV_BC_BP)], method='pchip')

        # EAF - and interpolating the BCs to get a smooth function
        _, interp_BC_G = fn.interpolation_time(BC_G_cut, BC_G_cut, track_num[~np.isnan(CV_BC_BP)], method='pchip')
        interp_BC_BP, interp_BC_RP = fn.interpolation_time(BC_BP_cut, BC_RP_cut, track_num[~np.isnan(CV_BC_BP)], method='pchip')
                # EAF - interpolating only the points that have valid BCs



        Mbol_L_cut = 4.75 - 2.5 * interp_Y_val 
        M = Mbol_L_cut - interp_BC_G
        m = d + M



        T_cluster_K = interp_temperature
        cluster_flux_ratio = (r_cluster_parsecs ** 2) * (T_cluster_K ** 4)
        cluster_sun_ratio = cluster_flux_ratio / solar_flux_ratio
        Mbol_teff_cut = 4.75 - 2.5 * np.log10(cluster_sun_ratio)

        M_teff_BP = Mbol_teff_cut - interp_BC_BP
        M_teff_RP = Mbol_teff_cut - interp_BC_RP


        m_teff = (d + M_teff_BP) - (d + M_teff_RP)

        # interp_mass[x] line to remove oddity with interpolation
        if HG_TARGETS == True:
            mask = [m_teff[x] <= 2.6 and interp_mass[x] != 1.1543328488865459 and interp_mass[x] != 1.153971824181945 for x in range(len(m_teff))]
        else:
            mask = [m_teff <= 2.6][0]
        m_teff = m_teff[mask]
        m = m[mask]

        interp_mass = interp_mass[mask]





        MSTO_index = np.argmin(m_teff)
        x_diff = m_teff[MSTO_index] - MSTO_ridgeline_x
        y_diff = m[MSTO_index] - MSTO_ridgeline_y

        amlt = r"$\alpha_{MLT}$"


        # ################
        # # To have interactive points on isochrones:

        # # M_pts = 4.74 - 2.5 * luminosity[~np.isnan(CV_BC_BP)] - BC_G_cut
        # M_pts = 4.75 - 2.5 * luminosity[~np.isnan(CV_BC_BP)] - BC_G_cut
        # m_pts = d + M_pts

        # T_cluster_K = T_eff[~np.isnan(CV_BC_BP)]
        # cluster_flux_ratio = (r_cluster_parsecs ** 2) * (T_cluster_K ** 4)
        # cluster_sun_ratio = cluster_flux_ratio / solar_flux_ratio
        # Mbol_teff_cut_pt = (4.75 - 2.5 * np.log10(cluster_sun_ratio))
        # M_teff_BP_pt = Mbol_teff_cut_pt - BC_BP_cut
        # M_teff_RP_pt = Mbol_teff_cut_pt - BC_RP_cut
        # m_teff_pt = (d + M_teff_BP_pt) - (d + M_teff_RP_pt)


        # mask = [m_teff_pt <= 2.6][0]
        # m_teff_pt = m_teff_pt[mask]
        # m_pts = m_pts[mask]

        # # # print(f"max mass is {max(mass[~np.isnan(CV_BC_BP)])}!")

        # stuff = [mass[~np.isnan(CV_BC_BP)], T_eff[~np.isnan(CV_BC_BP)], luminosity[~np.isnan(CV_BC_BP)],logg[~np.isnan(CV_BC_BP)], m_teff_pt, m_pts]
        # fn.annotate(m_teff_pt - x_diff, m_pts - y_diff, stuff, ax, fig, label_text=[r'{} M$\odot$', 'log(Teff) = {}', 'log(L) = {}', 'log(g) = {}', 'M_teff = {}', 'm = {}'], c='thistle')

        # # stuff = [interp_mass, interp_temperature, interp_Y_val, interp_logg]
        # # fn.annotate(m_teff - x_diff, m - y_diff, stuff, ax, fig, label_text=[r'{} M$\odot$', 'log(Teff) = {}', 'log(L) = {}', 'log(g) = {}'], c='thistle')


        ax.plot(m_teff - x_diff, m - y_diff, label = f'a{alpha}')

        # EAF - saving mag space isochrone with and without MS alignment

        pts = pd.DataFrame(list(zip(interp_mass, m_teff - x_diff, m - y_diff)), columns = ['mass', 'x', 'y'])
        csv_name = f'{cluster_folder}/mag_space/offset/a{alpha}_isochrone_coordinate_space_offset.csv'
        csv_save = pts.to_csv(csv_name)

        x_diff = 0
        y_diff = 0

        pts = pd.DataFrame(list(zip(interp_mass, m_teff - x_diff, m - y_diff)), columns = ['mass', 'x', 'y'])
        csv_name = f'{cluster_folder}/mag_space/no_offset/a{alpha}_isochrone_coordinate_space_no_offset.csv'
        csv_save = pts.to_csv(csv_name)



        plt.gca().invert_yaxis()
        plt.legend()

        # plt.savefig(f'{cluster_folder}/figures/offset/png/mag_iso_a{alpha}_offset.png', dpi=300)
        # plt.savefig(f'{cluster_folder}/figures/offset/pdf/mag_iso_a{alpha}_offset.pdf')

        # plt.savefig(f'{cluster_folder}/figures/no_offset/png/mag_iso_a{alpha}_no_offset.png', dpi=300)
        # plt.savefig(f'{cluster_folder}/figures/no_offset/pdf/mag_iso_a{alpha}_no_offset.pdf')
        plt.show()


