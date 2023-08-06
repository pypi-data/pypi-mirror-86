import os
import unittest

import numpy as np
import xarray as xr

from drama.io import cfg
import drama.geo as sargeo


class TestSwathGeo(unittest.TestCase):
    def setUp(self):
        self.dau = np.linspace(-400e3, 400e3, 17)
        self.inc_m = np.linspace(20, 50, 31)
        par_dir = os.path.join(os.path.expanduser("~/Code/stereoid"), "PAR")
        runid = "2019_1"
        self.par_file = os.path.join(par_dir, ("Hrmny_%s.cfg" % runid))
        self.par_file_second = os.path.join(
            par_dir, ("Hrmny_%s_orbit_later.cfg" % runid)
        )
        conf = cfg.ConfigFile(self.par_file)
        form_id = conf.formation.id
        drama_dir = os.path.expanduser("~/Code/drama/drama")
        save_dir = os.path.join(
            os.path.join(os.path.join(drama_dir, "geo"), "test_data"), runid
        )
        self.save_dir = os.path.join(save_dir, form_id)

    def test_single_swath_bistatic(self):
        # Attention! This dataset was generated using the harmony_ati
        # formation config, only compare it to that formation
        sample_ds = xr.open_dataset(os.path.join(self.save_dir, "bist_geo.nc"))
        inc_s = np.zeros((17, 31))
        bist_ang_az = np.zeros_like(inc_s)
        for dau_i in range(17):
            swth_bst = sargeo.SingleSwathBistatic(
                par_file=self.par_file, dau=self.dau[dau_i]
            )
            inc_s[dau_i] = np.degrees(
                swth_bst.inc2slave_inc(np.radians(self.inc_m))
            )
            bist_ang_az[dau_i] = np.degrees(
                swth_bst.inc2bist_ang_az(np.radians(self.inc_m))
            )
        inc_m_xr = xr.DataArray(
            self.inc_m,
            dims=["inc"],
            name="inc_m",
            coords={"inc": self.inc_m.astype(np.int)},
        )
        inc_s_xr = xr.DataArray(
            inc_s,
            dims=["dau", "inc"],
            name="inc_s",
            coords={
                "inc": self.inc_m.astype(np.int),
                "dau": (self.dau / 1e3).astype(np.int),
            },
        )
        bist_ang_az_xr = xr.DataArray(
            bist_ang_az,
            dims=["dau", "inc"],
            name="bist_ang_az",
            coords={
                "inc": self.inc_m.astype(np.int),
                "dau": (self.dau / 1e3).astype(np.int),
            },
        )
        dau_xr = xr.DataArray(
            self.dau,
            dims=["dau"],
            name="dau",
            coords={"dau": (self.dau / 1e3).astype(np.int)},
        )
        geo = xr.Dataset(
            {
                "inc_s1": inc_m_xr,
                "inc_hrmny": inc_s_xr,
                "bist_ang_az": bist_ang_az_xr,
                "along_track_distance": dau_xr,
            }
        )
        self.assertIsNone(
            xr.testing.assert_allclose(geo, sample_ds), "datasets do not match"
        )

    def test_single_swath_bistatic_iterator(self):
        swth_bst = sargeo.SingleSwathBistatic(
            par_file=self.par_file, n_orbits=2
        )
        swt_bst_later = sargeo.SingleSwathBistatic(
            par_file=self.par_file_second
        )
        swath_list = []
        for swath in swth_bst:
            swath_list.append(swath)
        self.assertIsNone(
            np.testing.assert_allclose(
                swath_list[1].master_swath.incident, swt_bst_later.master_inc
            ),
            "incident angles are the same",
        )

    def test_single_swath_bistatic_iterator_first(self):
        swth_bst = sargeo.SingleSwathBistatic(
            par_file=self.par_file, n_orbits=2
        )
        swt_bst_later = sargeo.SingleSwathBistatic(
            par_file=self.par_file_second
        )
        swath_list = []
        for swath in swth_bst:
            swath_list.append(swath)
        self.assertIsNone(
            np.testing.assert_allclose(
                swath_list[0].master_swath.incident, swth_bst.master_inc
            ),
            "incident angles are the same",
        )

    def test_single_swath_bistatic_iterator_different(self):
        swth_bst = sargeo.SingleSwathBistatic(
            par_file=self.par_file, n_orbits=2
        )
        swt_bst_later = sargeo.SingleSwathBistatic(
            par_file=self.par_file_second
        )
        swath_list = []
        for swath in swth_bst:
            swath_list.append(swath)
        self.assertTrue(
            np.any(
                np.not_equal(
                    swath_list[0].master_swath.incident,
                    swt_bst_later.master_inc,
                )
            ),
            "incident angles are the same",
        )
