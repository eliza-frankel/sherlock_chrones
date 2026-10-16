# Supplementary Materials for _Sherlock 'Chrones: The Curious Case of NGC 6791 and Asteroseismic Targets Therein Reveals Mixing Length Dependence on Evolutionary Stage_

This repository contains all the supplemental information from Frankel et al. 2026 including _Gaia_ queries, python scripts, MESA inlists, and more. The contents are as follows:

* M92
  * `bolometric_corrections/`
    * contains bolometric corrections for each value of alpha_MLT, found using https://github.com/casaluca/bolometric-corrections code
  * `isochrones/`
    * contains csv files with each isochrone point, found using building_isochrones.py
  * `M92_plot.py` - plots M92 cluster data with isochrones overlaid
  * `magspace_metrics_M92.py` - does the subgiant branch length and RGB curvature metrics for M92

* MESA
  * `M92_batch.sh`
    * Script for launching grids of stellar tracks with varying alpha_MLTs for M92
  * `PAPER_NGC6791_batch.sh`
    * Script for launching grids of stellar tracks with varying alpha_MLTs for M92
  * `PAPER_mass_evo.sh`
    * Called in X_batch.sh, this is the file that replaces metallicity, helium, stellar mass, and alpha_MLT in `inlist_solo_template` and then runs the modified inlist
  * `inlist_solo_template`
    * This is the inlist used for this project. Everything remains the same between M92 and NGC 6791, except for the parameters labeled <<PARAM>>; these
      include the cluster metallicity, <<initial_z>>, initial helium, <<initial_y>>, stellar model mass, <<initial_mass>>, and mixing length parameter, <<initial_alpha>>.
 
* NGC 6791
  * `best_fit_metrics/`
    * `subgiant_length_metric.py` - Metric 1: Subgiant Branch Length
    * `avg_temp_metric.py` - Metric 2: average RGB temperature
    * `curvature_rgb_metric.py` - Metric 3: Curvature of RGB
    * `most_luminous_metric.py` - Metric 4: Offset from most luminous asteroseismic target
  * `csv_isochrone_plot.py` - plotting NGC 6791
  * `bolometric_corrections/`
    * contains bolometric corrections for each value of alpha_MLT, found using https://github.com/casaluca/bolometric-corrections code
  * `isochrones/`
    * contains csv files with each isochrone point, found using building_isochrones.py
  * `asteroseismology_comparison.py` - plots mass-log(g) comparison to all isochrones and log(g)-T_eff isochrone with asteroseismic targets
  * `define_points.py` - Makes Figure 7
  * `ngc6791_asteroseismic_data.csv` - Asteroseismic data from Pinsonneault et al. 2025 and Tayar & Joyce 2025 (also in Table 5 in Appendix C)

* Queries
  * `(m92/ngc6791)_query.sql` - final query
  * `(m92/ngc6791)_gaia_data.csv`- results of the final query
 
* `building_isochrones.py` - code used to build isochrones from MESA history files & place into a csv file
* `converting_theory_to_obs.py` - conversion from luminosity and effective temperature to magnitude space
* `functions.py` - a list of all the functions used to build isochrones and to do this analysis
* `isochrone_grid.py` - plotting isochrones in a 4x4 grid (Figure 6)
