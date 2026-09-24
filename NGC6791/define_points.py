#!/Users/elizafrankel/anaconda3/bin/python3

# Author: E. Frankel
# 6.17.2026


import sys
sys.path.insert(0, '/Users/elizafrankel/Desktop/Research/')
import functions as fn
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from glob import glob
import math
from matplotlib.colors import ListedColormap




if __name__ == '__main__':

    # age = 15
    # Fe_H = '0.0'
    age = 8.3
    Fe_H = '0.31'
    Fe_H_float = float(Fe_H)
    metallicity = '0.025490'

    # save = True
    save = False

    save_filename =  f'figures/isochrones/{age}Gyr_FeH{Fe_H}_theoretical.png'
    # save_filename = None


    # cluster = None
    cluster = 'NGC 6791'
    cluster_path = None

    theoretical_coords = True
    num_panels = None
    manual_MSTO = [[0,0]]


    # will_they_wont_they = False
    will_they_wont_they = True


    location = f'/Users/elizafrankel/Desktop/Research/2025/fall_2025/massive_grid/'

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

# #     files = glob(location + f'no_offset/a*isochrone*.csv')
#     files = glob(location + f'061926Mbolsun475_offset/a*isochrone*.csv')
#     files.sort()




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

    # Remove Possible AGB star; possible AGB star; silver detection
    rgb_stars = [gaiaid[i] != 2051105754413616000 and gaiaid[i] != 2051293319920668160 and gaiaid[i] != 2051293118064539520 for i in range(len(gaiaid))]

    rgb_Gmag = [12.99011683, 14.52952598, 13.77237662, 14.76537374, 13.88611123, 13.16378577, 14.13053264, 14.46881412, 13.15170327, 12.75465679, 12.76521634, 13.71150795, 14.76162103, 12.93296926, 14.35636453, 14.57263006, 13.47973764]

    rgb_BP_RP = [1.9311618, 1.37303103, 1.50373198, 1.33282331, 1.46367487, 1.70927971, 1.40697352, 1.34774469, 1.73415529, 1.74301225, 1.9020598, 1.51852077, 1.34825287, 1.63671631, 1.38658684, 1.36171107, 1.60269506]

    
    

    # NGC6791_EBV = 0.16
    NGC6791_EBV = 0.14

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, NGC6791_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    
    


    r_NGC6791_parsecs = 4010  # Brogaard et al 2011

    d = fn.distance_modulus(r_NGC6791_parsecs)

    print(f"Distance modulus for {cluster} is {d}")


    cmap_indicies = [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 17, 18, 19]

    new_cmap = ListedColormap(mpl.cm.tab20b(cmap_indicies))
    color = fn.get_cmap_colors(new_cmap, len(cmap_indicies))

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)

    
    


    # 3. Subgiant branch duration

    fig_subgiant, ax_subgiant = plt.subplots(figsize=(6,8))

    # Plotting cluster
    ax_subgiant.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.3)
    ax_subgiant.invert_yaxis()



    # # Subgiant branch points

    # cluster_MSTO_BP_RP = 0.955
    cluster_MSTO_BP_RP = 0.9
    cluster_MSTO_G = 16.790

    cluster_SGB_BP_RP = 1.119
    cluster_SGB_G = 16.873

    # # RGB points

    rgb_luminous_G = 12.990116832840757
    rgb_luminous_BP_RP = 1.9311618036359377

    rgb_dimmest_G = 14.765373743791011
    rgb_dimmest_BP_RP = 1.332823308552968


    # ax_subgiant.scatter(cluster_MSTO_BP_RP, cluster_MSTO_G, marker='o', color='k')
    # plt.text(0.33, 0.37, 'A', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15)

    # ax_subgiant.scatter(cluster_SGB_BP_RP, cluster_SGB_G, marker='o', color='blueviolet')
    # plt.text(0.5, 0.28, 'B', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15, color='blueviolet')

    # ax_subgiant.scatter(rgb_dimmest_BP_RP, rgb_dimmest_G, marker='o', color='cornflowerblue')
    # plt.text(0.55, 0.64, 'C', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15, color='cornflowerblue')

    # ax_subgiant.scatter(rgb_luminous_BP_RP, rgb_luminous_G, marker='o', color='hotpink')
    # plt.text(0.9, 0.9, 'D', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15, color='hotpink')

    ax_subgiant.scatter(cluster_MSTO_BP_RP, cluster_MSTO_G, marker='o', color='k')
    plt.text(0.33, 0.37, 'A', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15)

    ax_subgiant.scatter(cluster_SGB_BP_RP, cluster_SGB_G, marker='o', color='k')
    plt.text(0.5, 0.28, 'B', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15)

    ax_subgiant.scatter(rgb_dimmest_BP_RP, rgb_dimmest_G, marker='o', color='k')
    plt.text(0.55, 0.64, 'C', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15)

    ax_subgiant.scatter(rgb_luminous_BP_RP, rgb_luminous_G, marker='o', color='k')
    plt.text(0.9, 0.9, 'D', horizontalalignment='center', verticalalignment='center', transform=ax_subgiant.transAxes, weight='bold', fontsize=15)


    ax_subgiant.set_xlabel(r'G$_{BP}$ - G$_{RP}$', fontsize=15)
    ax_subgiant.set_ylabel('G', fontsize=15)


    # plt.savefig(f'figures/best_fit_metrics/subgiant_length/png/NGC6791_a{alpha}_subgiant_length.png', dpi=300)
    # plt.savefig(f'figures/best_fit_metrics/subgiant_length/pdf/NGC6791_a{alpha}_subgiant_length.pdf')
    plt.savefig('figures/NGC6791/best_fit_metrics/metric_definitions.png', dpi=300)
    plt.savefig('figures/NGC6791/best_fit_metrics/metric_definitions.pdf')
    plt.show()

