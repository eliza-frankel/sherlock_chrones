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
import math
from matplotlib.colors import ListedColormap


# For 9
cb_colors_9 = ['#000000', '#2E2585', '#337538', '#5DA899', '#94CBEC', '#DCCD7D', '#C26A77', '#9F4A96', '#7E2954']

# For 16
# cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DCCD7D', '#E4A05A', '#DAA9D6', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']

cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DCCD7D', '#E4A05A', '#DAA9D6', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101', '#000000']


if __name__ == '__main__':

    age = 8.3
    Fe_H = '0.31'
    Fe_H_float = float(Fe_H)
    metallicity = '0.025490'
    cluster_folder = 'NGC6791'
    cluster = 'NGC 6791'



    location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

    # alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # # EAF - this is for the colormap
    # alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.85', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.85, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]


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

    # Remove Possible AGB star; possible AGB star; silver detection
    rgb_stars = [gaiaid[i] != 2051105754413616000 and gaiaid[i] != 2051293319920668160 and gaiaid[i] != 2051293118064539520 for i in range(len(gaiaid))]

    rgb_Gmag = [12.99011683, 14.52952598, 13.77237662, 14.76537374, 13.88611123, 13.16378577, 14.13053264, 14.46881412, 13.15170327, 12.75465679, 12.76521634, 13.71150795, 14.76162103, 12.93296926, 14.35636453, 14.57263006, 13.47973764]

    rgb_BP_RP = [1.9311618, 1.37303103, 1.50373198, 1.33282331, 1.46367487, 1.70927971, 1.40697352, 1.34774469, 1.73415529, 1.74301225, 1.9020598, 1.51852077, 1.34825287, 1.63671631, 1.38658684, 1.36171107, 1.60269506]

    # EAF - getting RGB 


    # # 2. Avg temperature comparison
    # fig_avgT, ax_avgT = plt.subplots(figsize=(6,8))

    

    # NGC6791_EBV = 0.16
    NGC6791_EBV = 0.14

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, NGC6791_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    


    r_NGC6791_parsecs = 4010  # Brogaard et al 2011

    d = fn.distance_modulus(r_NGC6791_parsecs)

    print(f"Distance modulus for {cluster} is {d}")

    new_cmap = ListedColormap(cb_colors_16)

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)

    for INDEX, file in enumerate(files):

        fig_avgT, ax_avgT = plt.subplots(figsize=(6.75,6))



        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()



        alpha = alpha_mlt[INDEX]


        # 2. Avg temperature comparison

        # # Plot isochrone one time:
        resid = np.zeros(len(m_teff))
        ax_avgT.plot(m, m_teff - m_teff, label=alpha, color='purple', linewidth=2) #color=color[INDEX])
        pythag_dist = 0 

        for target in range(len(rgb_BP_RP)):

            # Step 1: find the nearest magnitude isochrone value to each HG target BP - RP
            # ie what point on the isochrone has the same y value
            # index, closest_G = fn.find_nearest(m, rgb_luminous_G)

            # index, iso_closest_BP_RP = fn.find_nearest(m, rgb_Gmag[target])
            index, iso_closest_G = fn.find_nearest(m, rgb_Gmag[target])
            # print(m_teff[index], rgb_Gmag[target], rgb_BP_RP[target] - m_teff[index])

            # Step 2: Find difference between isochrone and HG target
            diff = m_teff[index] - rgb_BP_RP[target]
            # diff = iso_closest_BP_RP - rgb_BP_RP[INDEX]

            # Step 3: Plot vs isochrone at 0
            ax_avgT.scatter(rgb_Gmag[target], diff, marker='*', c='goldenrod', s=175)

            pythag_dist += diff**2

        print(alpha, 'Pythagorean distance =', pythag_dist**(1/2))


        # EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE
        amlt = r"$\alpha_{MLT}$"


        # textstr = f'Pythagorean Distance = {round(pythag_dist**(1/2), 3)}'

        # props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
        
        # # place a text box in bottom right in axes coords
        # ax_avgT.text(0.465, 0.97, textstr, transform=ax_avgT.transAxes, fontsize=14,
        #         verticalalignment='top', bbox=props)

        
        textstr = f'{amlt} = {alpha}'
        
        # these are matplotlib.patch.Patch properties
        # props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
        props = dict(boxstyle='round', facecolor='mediumpurple', alpha=0.2)
        
        # # place a text box in bottom right in axes coords
        # ax_avgT.text(0.75, 0.89, textstr, transform=ax_avgT.transAxes, fontsize=15, verticalalignment='top', bbox=props)
        ax_avgT.text(0.03, 0.97, textstr, transform=ax_avgT.transAxes, fontsize=15, verticalalignment='top', bbox=props)

        ax_avgT.tick_params(labelsize=13)

        # ax_avgT.set_ylim(-0.25,0.25)
        # ax_avgT.set_xlim(12.5,15)

        ax_avgT.set_ylim(-0.3,0.3)
        ax_avgT.set_xlim(12,15.5)
        

        # # cmap boundaries so ticks appear in center of cbar:
        # alpha_mlt_float = np.array(alpha_mlt_float)
        # step = 0.1
        # boundaries = np.concatenate([
        #     [alpha_mlt_float[0] - step/2],
        #     (alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
        #     [alpha_mlt_float[-1] + step/2]
        # ])
        

        # # cmap = mpl.cm.tab20b
        # # norm = mpl.colors.BoundaryNorm(alpha_mlt_float, new_cmap.N)
        # norm = mpl.colors.BoundaryNorm(boundaries, new_cmap.N)

        # cbar = fig_avgT.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap),
        #         ax=ax_avgT, ticks=alpha_mlt_float, boundaries=boundaries, orientation='horizontal',
        #         label=r"$\alpha_{MLT}$")
        

        # cbar.ax.tick_params(labelsize=13)

        ax_avgT.set_ylabel(r'$\Delta$G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
        ax_avgT.set_xlabel('G', fontsize=15)


        # plt.savefig(f'figures/NGC6791/best_fit_metrics/avg_temp/png/NGC6791_a{alpha}_avg_temp.png', dpi=300)
        # plt.savefig(f'figures/NGC6791/best_fit_metrics/avg_temp/pdf/NGC6791_a{alpha}_avg_temp.pdf')
        plt.show()

