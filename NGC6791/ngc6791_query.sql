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
        POINT('ICRS', 290.22, 37.777778)
    ) AS ang_sep 
FROM gaiadr3.gaia_source
WHERE
    CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE(
            'ICRS',
            290.22, 37.777778,
            0.204999 -- half light radius is 4.1 arcmin [0.068333 deg] (Kamann et al 2019) 0.2208
        )
    ) = 1
    AND phot_bp_mean_mag < 20.3 -- ~ 2000 off
    -- AND phot_g_mean_mag > 13 -- only 21 off
    -- AND phot_g_mean_mag < 20
    AND parallax BETWEEN 0.09 AND 0.29 -- ~3000 off p = 0.192 +/- 0.1
    AND pmra BETWEEN -1 AND 0
    AND pmdec BETWEEN -3 AND -1.7
    AND pmra_error < 0.3
    AND pmdec_error < 0.3
    AND parallax_error < 0.15
    AND ruwe < 1.15 -- ~550 off
    AND astrometric_excess_noise_sig < 2 -- ~550 off
    AND astrometric_excess_noise < 1 -- ~800 off
    AND ipd_gof_harmonic_amplitude < EXP(0.18 * (phot_g_mean_mag - 33)) -- 200 off
    AND ipd_frac_multi_peak < 2 -- 300 off
    AND visibility_periods_used > 10 -- 300 off
    AND (
    (
        bp_rp >= 0.0 AND bp_rp < 0.5
        AND ABS(
            phot_bp_rp_excess_factor
            -
            (
                1.154360
                + 0.033772 * bp_rp
                + 0.032277 * POWER(bp_rp,2)
            )
        ) < 0.03 -- 0.05
    )
    OR
    (
        bp_rp >= 0.5 AND bp_rp < 4.0
        AND ABS(
            phot_bp_rp_excess_factor
            -
            (
                1.162004
                + 0.011464 * bp_rp
                + 0.049255 * POWER(bp_rp,2)
                - 0.005879 * POWER(bp_rp,3)
            )
        ) < 0.03 -- 0.05
    )
)
