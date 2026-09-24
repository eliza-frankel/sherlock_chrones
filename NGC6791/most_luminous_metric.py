# Author: E. Frankel
# 6.5.2026


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
cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DCCD7D', '#E4A05A', '#DAA9D6', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']
cb_colors_16_reversed = ['#1D0101', '#480024', '#9A051E','#7E2954','#9F4A96', '#C26A77', '#DAA9D6','#E4A05A',  '#DCCD7D', '#94CBEC', '#A3DA9A', '#5DA899', '#337538', '#5C53B9', '#2E2585', '#000000']

if __name__ == '__main__':

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
    alpha_mlt_float_reversed = [2.50, 2.40, 2.30, 2.20, 2.10, 2.00, 1.90, 1.80, 1.70, 1.60, 1.50, 1.40, 1.30, 1.20, 1.10, 1.00]

    files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
    files.sort()


    # EAF - getting RGB 

    # found these using hg_targets function and using the interactive annotation
    rgb_luminous_G = 12.990116832840757
    rgb_luminous_BP_RP = 1.9311618036359377


    new_cmap = ListedColormap(cb_colors_16)

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)


    # EAF - reversing colormap for visual purposes on colorbar
    cmap_reversed = ListedColormap(cb_colors_16_reversed)



    fig_bright, ax_bright = plt.subplots(figsize=(10,7))
    

    for INDEX, file in enumerate(files):

        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        alpha = alpha_mlt[INDEX]
        

        amlt = r"$\alpha_{\rm MLT}$"


        # EAF - find nearest G mag on the isochrone
        
        index, closest_G = fn.find_nearest(m, rgb_luminous_G)
        closest_BP_RP = m_teff[index]

        ax_bright.scatter(alpha, closest_BP_RP - rgb_luminous_BP_RP, c=color[INDEX], s=250) #, label = f'{alpha}; {closest_BP_RP - rgb_luminous_BP_RP}')

    ax_bright.set_ylabel(r'$\Delta$G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
    ax_bright.tick_params(axis='both', labelsize=13)
    ax_bright.tick_params(axis='x', labelrotation=30)
    ax_bright.set_xlabel(amlt, fontsize = 15)


    ax_bright.hlines(0, 0, 15, colors='grey', zorder=0, linestyles='dotted')


    plt.savefig('figures/NGC6791/best_fit_metrics/most_luminous/png/pts_NGC6791_most_luminous_comparison.png', dpi=300)
    plt.savefig('figures/NGC6791/best_fit_metrics/most_luminous/pdf/pts_NGC6791_most_luminous_comparison.pdf')
    plt.show()

    