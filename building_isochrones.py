# Author: E. Frankel
# 10/21/2025

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import mesa_reader as mr
from glob import glob
import pandas as pd
from datetime import datetime
import csv

from scipy.interpolate import CubicSpline
from time import time

import functions as fn


print('hi')


color = [plt.cm.Spectral(i) for i in range(plt.cm.Spectral.N)]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color)


if __name__ == '__main__':
    # obj_z = 'z0.000130' # M92
    # obj_z = 'z0.025490' # NGC 6791


    # alpha_mlt = ['1.00', '1.10', '1.20', '1.30', '1.40', '1.50', '1.60', '1.70', '1.80', '1.90', '2.00', '2.10', '2.20','2.30', '2.40', '2.50']
    # alpha_mlt = ['1.00', '1.70', '2.50']
    # alpha_mlt = ['1.10', '1.70', '2.40']

    # alpha_mlt = ['1.80', '1.90']
    alpha_mlt = ['1.60']
    # alpha_mlt = ['2.10', '2.20','2.30', '2.40', '2.50']


    tt = 0
    list_appending = 0
    iso_points_plotting_time = 0
    data_gathering = 0
    plotting_tracks = 0

    # plt.figure(figsize=(6,8))

    for alpha in alpha_mlt:
        # # # file_directory = f"LOGS/a{alpha}/history_m*"
        # file_directory = f"LOGS/history_m*z0.000145_a{alpha}*"
        # amlt = r"$\alpha_{\rm MLT}$"
        # metallicity = '0.000145'
        # obj_z = float(metallicity)
        # y = 0.25256
        # target_year = 13.8
        # cluster_name = 'M92'
        # FOLDER_NAME = 'M92/final'
        # MASS_RANGE = r'$0.60 - 0.77$ M$_{\odot}$' # M92

        file_directory = f"LOGS/NGC6791/DONE/history_m*z0.034507_a{alpha}*"
        amlt = r"$\alpha_{\rm MLT}$"
        metallicity = '0.034507'
        obj_z = float(metallicity)
        y = 0.296310
        target_year = 8.3 # NGC 6791
        cluster_name = 'NGC 6791'
        FOLDER_NAME = 'NGC6791'
        MASS_RANGE = r'$0.80 - 1.17$ M$_{\odot}$' # NGC 6791
        

        print("\nNEW METHOD!!!\n")

        t1 = time()

        tracklist = fn.make_tracklist(file_directory)

        outfile_name_termination_codes = f'termination_codes_{target_year}Gyr_{obj_z}_a{alpha}.csv'


        two = time()

        # iso_points = []
        iso_T = []
        iso_L = []
        iso_M = []
        iso_logg = []
        iso_ages = []


        phases = []



        fig, ax = plt.subplots(figsize=(7,8))

        for i, f in enumerate(tracklist):

            # color_index = (len(color) // (i + 1)) - 1

            # print(f)

            mass_label = f.split('/')[-1].split("_")[1][1:]

            one = time()

            data = mr.MesaData(f)    
        

            T, L, logg, ages, M = data.log_Teff, data.log_L, data.log_g, data.star_age, data.star_mass
            # phase = data.phase_of_evolution
            total_he4 = data.total_mass_he4
            center_he4 = data.center_he4
            

            # phases.append(phase[-1])



            two = time()
            

            # term_code = data.termination_code[-1]

            target_age = target_year * (1e9)  # from Gyr to yr
        
            a = time()


            closest_age, make_believe_values, INDEX = \
                fn.artificial_isochrone_point(target_age, ages, M, [T, L, logg, total_he4, center_he4], num_steps=1000)

            mass_inferred = make_believe_values[0]
            temp_inferred = make_believe_values[1]
            lums_inferred = make_believe_values[2]
            logg_inferred = make_believe_values[3]

            total_mass_he4_inferred = make_believe_values[4]
            center_he4_inferred = make_believe_values[5]


            b = time()

            c = time()
            if type(mass_inferred) == np.ndarray:
                mass_inferred = mass_inferred[0][0]

            if type(temp_inferred) == np.ndarray:
                temp_inferred = temp_inferred[0][0]

            if type(lums_inferred) == np.ndarray:
                lums_inferred = lums_inferred[0][0]

            if type(logg_inferred) == np.ndarray:
                logg_inferred = logg_inferred[0][0]



            
            iso_M.append(mass_inferred)
            iso_T.append(temp_inferred)
            iso_L.append(lums_inferred)
            iso_logg.append(logg_inferred)
            iso_ages.append(closest_age)


            d = time()


            import matplotlib.colors as colors
            import matplotlib.cm as cm
            from matplotlib.colors import LinearSegmentedColormap, ListedColormap

            norm = colors.LogNorm(vmin=0.8, vmax=1.17)
            # cmap = cm.viridis

            colors = ['#2E2585', '#337538', '#5DA899', '#94CBEC', '#DCCD7D', '#C26A77', '#9F4A96', '#7E2954']


            cmap = LinearSegmentedColormap.from_list("mycmap", colors)

            plt.plot(T, L, linewidth=0.5, color=cmap(norm(mass_inferred)))#, zorder=0, alpha=0.1) #, label=mass_label + 'M_sun') 
            plt.xlabel(r'log($T_{\rm eff}$)', fontsize=18)
            plt.ylabel('log(L)', fontsize=18)
            ax.tick_params(labelsize=15)
            plt.scatter(temp_inferred, lums_inferred, s=25, zorder=100, c=cmap(norm(mass_inferred))) #, c='k',)                       

            plt.gca().invert_xaxis
            # plt.legend(loc='lower right').set_zorder(100)

            e = time()

            tt += b - a 

            list_appending += d - c
            iso_points_plotting_time += e - d
            data_gathering += two - one
            plotting_tracks += a - two

            print('done with', f)

            # # Writing termination codes

            # with open(outfile_name_termination_codes, 'a') as f:
            #     writer = csv.writer(f)
            #     writer.writerow([round(M[0], 5), term_code])

        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical')
        cbar.set_ticks(ticks=[0.8, 0.9, 1.0, 1.1, 1.17], labels=[0.8, 0.9, 1.0, 1.1, 1.17])
        cbar.set_label(label=r"Mass (M$_{\odot}$)", size=15)

        cbar.ax.tick_params(labelsize=13)
    

        textstr = f'{cluster_name} - {target_age / 1e9} Gyr'
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='lavender', alpha=0.5)
        
        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=18, verticalalignment='top', bbox=props)

        textstr = '\n'.join((
        f'{amlt} = {alpha}',
        f'z = {metallicity}',
        f'y = {y}',
        MASS_RANGE # NGC 6791
        ))

        props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)

        # place a text box in bottom right in axes coords
        ax.text(0.05, 0.9, textstr, transform=ax.transAxes, fontsize=15, verticalalignment='top', bbox=props)
            
            
        # EAF - saving a CSV
        df = pd.DataFrame(list(zip(iso_T, iso_L, iso_M, iso_logg, iso_ages)), columns =['log_Teff','log_L','mass','logg','age'])
        csv_name = f'isochrone_csv/{FOLDER_NAME}/isochrone_age{target_year}Gyr_z{obj_z}_a{alpha}_toleranceX_tracks{len(tracklist)}.csv'
        csv_save = df.to_csv(csv_name)


        num_tracks = np.arange(0, len(iso_T))
        interp_T, interp_L = fn.interpolation_time(iso_T, iso_L, num_tracks)


        fig_save_prefix = f'figures/{FOLDER_NAME}/'
        fig_save_name = f'{cluster_name}_isochrone_{target_year}Gyr_{obj_z}_a{alpha}_{len(tracklist)}tracks' 

        plt.gca().invert_xaxis()
        plt.show()
        plt.savefig(fig_save_prefix + 'png/' + fig_save_name + '.png', dpi=300,bbox_inches='tight')
        plt.savefig(fig_save_prefix + 'pdf/' + fig_save_name + '.pdf', bbox_inches='tight')
        plt.close()

        
        t2 = time()
        print()
        print(f'Gathering the data from history files took {data_gathering} seconds')
        print(f'Plotting stellar tracks took {plotting_tracks} seconds')
        print(f'Plotting the isochrone points took {iso_points_plotting_time} seconds')
        print(f'Appending correct value to list took {list_appending} seconds')
        print(f'Determining the artificial points took {tt} seconds to run {len(tracklist)} tracks')
        print(f"\na{alpha} took {t2 - t1} seconds to run\n")


        # # ''' ELIZA - THIS IS TO PLOT TRACKS BASED ON TERMINATION CODE '''

        # # # read termination code file
        # # # separate colors into that many colors
        # # # plot track into correct color

        # plt.gca().invert_xaxis()

        # files = fn.make_tracklist(file_directory)
        # fname = files[0].split('/')
        # params = fname[-1].split('history_')[1].split('.data')[0]
        # x = params.split('_')
        # z_a = x[1] + '_' + x[2]

        # term_file = f'termination_codes_{target_year}Gyr_{z_a}'
        # codes, x = fn.tally_termination_codes(term_file + '.csv')

        # colors = plt.cm.tab20b(np.linspace(0, 1, len(codes)))

        # # Map variables to colors
        # var_to_color = {v: c for v, c in zip(codes, colors)}

        # plotted_vars = set()
        
        # for f in files:
        #     data = mr.MesaData(f)

        #     term_code = data.termination_code[-1]

        #     MESA_termination_codes = fn.create_termination_codes('MESA_termination_codes.csv')
        
        #     name = MESA_termination_codes[term_code]
        
        #     T = data.log_Teff
        #     L = data.log_L

        #     label = f'{name}' if term_code not in plotted_vars else None
        #     plt.plot(T, L, color=var_to_color[term_code], label=label)
        #     plotted_vars.add(term_code)

        # plt.legend()

        # plt.savefig(term_file + ".png", dpi=300)

        # plt.show()
        # plt.close()

    