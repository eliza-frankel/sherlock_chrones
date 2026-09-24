SELECT
    source_id,
    ra, dec,
    parallax, parallax_error,
    pmra, pmra_error,
    pmdec, pmdec_error,
    radial_velocity, radial_velocity_error,
    phot_g_mean_mag, phot_g_mean_flux,
    phot_bp_mean_mag, phot_bp_mean_flux,
    phot_rp_mean_mag, phot_rp_mean_flux,
    bp_rp,
    ruwe, astrometric_excess_noise_sig, astrometric_excess_noise, ipd_gof_harmonic_amplitude, ipd_frac_multi_peak, visibility_periods_used, phot_bp_rp_excess_factor, logg_gspphot, teff_gspphot, 
    ag_gspphot, azero_gspphot, ebpminrp_gspphot,
    DISTANCE(
        POINT('ICRS', ra, dec),
        -- POINT('ICRS', 290.221755, 37.771895)
        POINT('ICRS', 259.280792, 43.135944)
    ) AS ang_sep 
FROM gaiadr3.gaia_source WHERE
CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE(
            'ICRS',
            259.280792, 43.135944,
            0.06 -- half light radius is 1.09 arcmin [0.018167 deg] 
        )
    ) = 1
AND phot_bp_mean_mag < 20.3 -- ~ 2000 off
AND parallax BETWEEN 0.0012 AND 0.212 -- p = 0.112 +/- 0.1
AND pmra BETWEEN -5.5 AND -4.5
AND pmdec BETWEEN -1.5 AND 0.5