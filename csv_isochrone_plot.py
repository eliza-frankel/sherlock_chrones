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
# cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DAA9D6', '#DCCD7D', '#E4A05A', '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']
# EAF - I changed '#E4A05A' to  "#DD7F20" to be darker compared to Gold targets in the grid
cb_colors_16 = ['#000000', '#2E2585', '#5C53B9', '#337538', '#5DA899', '#A3DA9A', '#94CBEC', '#DAA9D6', '#DCCD7D',  "#DD7F20", '#C26A77', '#9F4A96','#7E2954', '#9A051E', '#480024', '#1D0101']




if __name__ == '__main__':


    age = 8.3
    Fe_H = '0.31'
    Fe_H_float = float(Fe_H)
    metallicity = '0.034507'
    cluster = 'NGC 6791'
    cluster_folder = 'NGC6791'

    save_filename =  f'figures/{cluster}/isochrones/{age}Gyr_FeH{Fe_H}_theoretical.png'


    location = f'/Users/elizafrankel/Desktop/Research/2025/FINAL_PAPER_EVERYTHING/'

    files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
    files.sort()


    path_to_cluster_data = '~/Desktop/queries/ngc6791/ngc6791_final_query.csv'


    Gmag_gaia, BP_RP_gaia, Teff_phot, logg_phot, source_ids, ag_gspphot, azero_gspphot, ebpminrp_gspphot, phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux = fn.data_manual_query(path_to_cluster_data)

    NGC6791_EBV = 0.14

    A_G, A_BP, A_RP, E_BP_RP = fn.extinction_law(logg_phot, BP_RP_gaia, Gmag_gaia, NGC6791_EBV, Xname='BPRP')
    A_G, A_BP, A_RP, E_BP_RP = np.array(A_G), np.array(A_BP), np.array(A_RP),np.array(E_BP_RP)

    r_NGC6791_parsecs = 4010  # Brogaard et al 2011

    d = fn.distance_modulus(r_NGC6791_parsecs)

    print(f"Distance modulus for {cluster} is {d}")

    # fig, ax = plt.subplots(figsize=(6,8))

    # color = [plt.cm.tab20b(i) for i in range(plt.cm.tab20b.N)]
    # color = fn.get_cmap_colors('tab20b', 16)

    # ########################################################################################################################################################
    # ########################################################################################################################################################
    # ##################################################################### individual #######################################################################
    # ########################################################################################################################################################
    # ########################################################################################################################################################



    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]




    for INDEX, file in enumerate(files):
        print(file)

        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        fig, ax = plt.subplots(figsize=(6,8))
        # EAF - Plotting cluster
        plt.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.25)

        alpha = alpha_mlt[INDEX]
        
        

        RGB_objs = [2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808]
        AGB_questionables = [2051293319920668160, 2051105754413616000]

        fn.hg_targets(RGB_objs, source_ids, Gmag_gaia - A_G, BP_RP_gaia - A_BP + A_RP, ax, questionable_IDs=AGB_questionables, fig=fig)



        amlt = r"$\alpha_{MLT}$"

        # plt.xlim(0.25, 2.75)
        # c = color[INDEX]
        # c_file = 'tab20b'

        c = 'purple'
        c_file = 'purple'

        ax.plot(m_teff, m, label = f'a{alpha}', color=c, linewidth = 2)

        # # if alpha == '1.00' or alpha == '1.10' or alpha == '1.20' or alpha == '1.30' or alpha == '1.40' or alpha == '1.50' or alpha == '1.60' or alpha == '1.65' or alpha == '1.70' or alpha == '1.75':
        # #     ax.plot(m_teff + 0.03, m+0.05, label = f'a{alpha}', color=c, linewidth = 2)
        # # else:
        # #     ax.plot(m_teff + 0.03, m, label = f'a{alpha}', color=c, linewidth = 2)

        # if alpha == '1.00' or alpha == '1.10' or alpha == '1.20' or alpha == '1.30' or alpha == '1.50' or alpha == '1.60' or alpha == '1.65' or alpha == '1.70' or alpha == '1.75':
        #     ax.plot(m_teff, m+0.05, label = f'a{alpha}', color=c, linewidth = 2)
        # else:
        #     ax.plot(m_teff, m, label = f'a{alpha}', color=c, linewidth = 2)

        # EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE

        textstr = f'NGC 6791 - {age} Gyr'
       
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        textstr = '\n'.join((
        f'z = {metallicity}',
        f'[Fe/H] = +{Fe_H}'))

        props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        
        textstr = f'{amlt} = {alpha}'
       
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.3)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.79, textstr, transform=ax.transAxes, fontsize=15,
                verticalalignment='top', bbox=props)

        ax.tick_params(labelsize=13)

        # cmap = mpl.cm.tab20b
        # norm = mpl.colors.BoundaryNorm(alpha_mlt_float, cmap.N)
        
        # cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        #         ax=ax, orientation='vertical',
        #         label=r"$\alpha_{MLT}$")

        # cbar.ax.tick_params(labelsize=13)

        ax.set_xlabel(r'G$_{BP}$ - G$_{RP}$', fontsize=15)
        ax.set_ylabel('G', fontsize=15)

        plt.gca().invert_yaxis()
        # # plt.legend()
        # plt.savefig(f'figures/ngc6791/single_comparison/png/NGC6791_a{alpha}_{c_file}.png', dpi=300)
        # plt.savefig(f'figures/ngc6791/single_comparison/pdf/NGC6791_a{alpha}_{c_file}.pdf')
        plt.show()

############################################################################################################################################################
############################################################################################################################################################
########################################################################## GRID ############################################################################
############################################################################################################################################################
############################################################################################################################################################

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

    files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
    files.sort()


    # # color = [plt.cm.tab20b(i) for i in range(plt.cm.tab20b.N)]
    # # color = fn.get_cmap_colors('turbo', 16)
    # color = ["#0D0887","#2C0694","#49039F","#6201A6","#7905A6","#8F0DA4","#A31E98","#B6308B","#C7417D","#D4536F","#E16462","#EB7754","#F48B47","#FA9F3A","#FCC53B","#F9DF21"]
    # # print(color)

    fig, ax = fig, ax = plt.subplots(nrows = 4, ncols = 4, figsize=(12,16))

    cols = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    rows = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]

    # cmap_indicies = [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 17, 18, 19]
    # # cmap_indicies = [4, 5, 6, 8, 10, 11, 12, 14, 15, 16, 17, 18, 19, 0, 2, 3]
    # # cmap_indicies = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 124, 15, 16, 17, 18, 19]
    # print(len(cmap_indicies))
    # new_cmap = ListedColormap(mpl.cm.tab20b(cmap_indicies))
    # color = fn.get_cmap_colors(new_cmap, len(cmap_indicies))

    new_cmap = ListedColormap(cb_colors_16)

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)



    for INDEX, file in enumerate(files):

        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        # fig, ax = plt.subplots(figsize=(6,8))

        alpha = alpha_mlt[INDEX]
        
        # # EAF - Plotting cluster
        # plt.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.25)

        RGB_objs = [2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808]
        AGB_questionables = [2051293319920668160, 2051105754413616000]


        # EAF - plotting each in its own subplot
        row = INDEX % 4 - 1
        column = math.ceil(INDEX / 4) - 1


        amlt = r"$\alpha_{MLT}$"


        # EAF - setting tick sizes without specifying label or location
        ax[cols[INDEX],rows[INDEX]].tick_params(axis='x', labelsize=15)
        ax[cols[INDEX],rows[INDEX]].tick_params(axis='y', labelsize=15)

        ax[cols[INDEX],rows[INDEX]].scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.15)
        fn.hg_targets(RGB_objs, source_ids, Gmag_gaia - A_G, BP_RP_gaia - A_BP + A_RP, ax[cols[INDEX],rows[INDEX]])

        ax[cols[INDEX],rows[INDEX]].invert_yaxis()

        ax[cols[INDEX],rows[INDEX]].plot(m_teff, m, label = f'{amlt} = {alpha}', color=color[INDEX], linewidth = 2.5)

        ax[cols[INDEX],rows[INDEX]].legend(loc="lower right")



    fig.supxlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=25)
    fig.supylabel('G', fontsize=25)
    fig.suptitle('NGC 6791', fontsize = 30)

    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.075)

    plt.savefig("figures/NGC6791/png/grid_of_isochrones_NGC6791.png", dpi=300)
    plt.savefig("figures/NGC6791/pdf/grid_of_isochrones_NGC6791.pdf")
    plt.show()


###########################################################################################################################################################
###########################################################################################################################################################
########################################################################## ALL ############################################################################
###########################################################################################################################################################
###########################################################################################################################################################

    # EAF - this plots all the isochrones, aligned at MSTO, in one figure

    alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # EAF - this is for the colormap
    alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]


    files = glob(location + f'{cluster_folder}/mag_space/offset/a*_isochrone_coordinate_space_offset.csv')
    files.sort()


    fig, ax = plt.subplots(figsize=(6,8))
    # # EAF - Plotting cluster
    plt.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=10, c='grey', alpha=0.25) #, zorder=20)

    color = fn.get_cmap_colors('tab20b', len(alpha_mlt))


    for INDEX, file in enumerate(files):

        df = pd.read_csv(file)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()


        alpha = alpha_mlt[INDEX]
        

        RGB_objs = [2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808]
        AGB_questionables = [2051293319920668160, 2051105754413616000]

        # fn.hg_targets(RGB_objs, source_ids, Gmag_gaia - A_G, BP_RP_gaia - A_BP + A_RP, ax, questionable_IDs=AGB_questionables, fig=fig)



        amlt = r"$\alpha_{MLT}$"

        # plt.xlim(0.25, 2.75)
        c = color[INDEX]
        c_file = 'tab20b'

        ax.plot(m_teff, m, label = f'a{alpha}', color=c, linewidth = 2, zorder=16-INDEX)


    # EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE

    ax.scatter(0.86141087, 17.14, c='k', marker='o', s=50, zorder=100)

    textstr = f'NGC 6791 - {age} Gyr'
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=15,
            verticalalignment='top', bbox=props)

    textstr = '\n'.join((
    f'z = {metallicity}',
    f'[Fe/H] = +{Fe_H}'))

    props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=15,
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
    

    cmap = mpl.cm.tab20b
    norm = mpl.colors.BoundaryNorm(boundaries, cmap.N)

    
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            ax=ax, ticks=alpha_mlt_float, boundaries=boundaries, orientation='vertical',
            label=r"$\alpha_{MLT}$")


    cbar.ax.tick_params(labelsize=13)

    ax.set_xlabel(r'G$_{BP}$ - G$_{RP}$', fontsize=15)
    ax.set_ylabel('G', fontsize=15)

    plt.gca().invert_yaxis()
    # plt.savefig(f'figures/ngc6791/all_NGC6791_{c_file}_offset.png', dpi=300)
    # plt.savefig(f'figures/ngc6791/all_NGC6791_{c_file}_offset.pdf')
    # # plt.savefig(f'figures/ngc6791/all_NGC6791_{c_file}.png', dpi=300)
    # # plt.savefig(f'figures/ngc6791/all_NGC6791_{c_file}.pdf')
    plt.show()


###########################################################################################################################################################
###########################################################################################################################################################
################################################################# PINNED AND NOT PINNED ###################################################################
###########################################################################################################################################################
###########################################################################################################################################################

    # alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # # EAF - this is for the colormap
    # alpha_mlt_float = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50]

    alpha_mlt = ['1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10']
    # EAF - this is for the colormap
    alpha_mlt_float = [1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10]

    files_offset = glob(location + f'{cluster_folder}/mag_space/offset/subset/a*_isochrone_coordinate_space_offset.csv')
    files_offset.sort()

    files_no = glob(location + f'{cluster_folder}/mag_space/no_offset/subset/a*_isochrone_coordinate_space_no_offset.csv')
    files_no.sort()


    fig, ax = plt.subplots(nrows=1, ncols=2, sharex=False, sharey = True, figsize=(11,8), gridspec_kw={'width_ratios':[3, 3.5]})
    plt.subplots_adjust(wspace = 0.0)
    ax, ax2 = ax[0], ax[1]

    # EAF - plot Gaia data on both plots
    ax.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.25) #, zorder=20)
    ax2.scatter(BP_RP_gaia - A_BP + A_RP, Gmag_gaia - A_G, marker='.', s=20, c='grey', alpha=0.25) #, zorder=20)


    new_cmap = ListedColormap(cb_colors_9)

    color = [new_cmap(i) for i in range(new_cmap.N)]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)


    for INDEX, file_offset in enumerate(files_offset):

        # EAF - plotting the offset isochrones 

        df = pd.read_csv(file_offset)
        mass = df["mass"].to_numpy()
        m_teff = df["x"].to_numpy()
        m = df["y"].to_numpy()

        df_no = pd.read_csv(files_no[INDEX])
        mass_no = df_no["mass"].to_numpy()
        m_teff_no = df_no["x"].to_numpy()
        m_no = df_no["y"].to_numpy()

        alpha = alpha_mlt[INDEX]
        

        RGB_objs = [2051294251936167424, 2051287311268706432, 2051294045777739520, 2051286933311576192, 2051293221143725952, 2051293152424246912, 2051287070750544128, 2051294114497261952, 2051292877546340864, 2051293319920668160, 2051293118064539520, 2051105135938204160, 2051293118064542976, 2051105754413616000, 2051293599100902016, 2051104276944822912, 2051296760197357184, 2051107609839671808]
        AGB_questionables = [2051293319920668160, 2051105754413616000]


        amlt = r"$\alpha_{MLT}$"

        c = color[INDEX]
        c_file = 'tab20b'

        ax2.plot(m_teff, m, label = f'a{alpha}', color=c, linewidth = 2, zorder=16-INDEX)
        ax.plot(m_teff_no, m_no, label = f'a{alpha}', color=c, linewidth = 2, zorder=16-INDEX)


    # EAF - THIS IS FOR TEXT BOX OF INFO ON FIGURE

    ax2.scatter(0.86141087, 17.14, c='k', marker='*', s=150, zorder=100)

    textstr = f'NGC 6791 - {age} Gyr'
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='slateblue', alpha=0.3)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=15,
            verticalalignment='top', bbox=props)

    textstr = '\n'.join((
    f'z = {metallicity}',
    f'[Fe/H] = +{Fe_H}'))

    props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
    
    # place a text box in bottom right in axes coords
    ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=15,
            verticalalignment='top', bbox=props)
    

    ax.tick_params(labelsize=13)
    ax2.tick_params(labelsize=13)

    # ax.set_xlim(0.3, 2.65)
    # ax2.set_xlim(0.3, 2.65)

    # cmap boundaries so ticks appear in center of cbar:
    alpha_mlt_float = np.array(alpha_mlt_float)
    step = 0.1
    boundaries = np.concatenate([
        [alpha_mlt_float[0] - step/2],
        (alpha_mlt_float[:-1] + alpha_mlt_float[1:]) / 2,
        [alpha_mlt_float[-1] + step/2]
    ])

    

    norm = mpl.colors.BoundaryNorm(boundaries, new_cmap.N)
    
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap),
            ax=ax2, ticks=alpha_mlt_float, boundaries=boundaries, orientation='vertical')
    cbar.set_label(label=r"$\alpha_{\rm MLT}$", size=15)


    cbar.ax.tick_params(labelsize=13)

    ax.set_xlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
    ax2.set_xlabel(r'G$_{\rm BP}$ - G$_{\rm RP}$', fontsize=15)
    ax.set_ylabel('G', fontsize=15)

    plt.gca().invert_yaxis()
    plt.savefig(f'figures/NGC6791/png/NGC6791_both_offset_and_no.png', dpi=300)
    plt.savefig(f'figures/NGC6791/pdf/NGC6791_both_offset_and_no.pdf')
    plt.show()