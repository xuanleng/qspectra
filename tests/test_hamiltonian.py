import numpy as np
import unittest
from numpy.testing import assert_allclose

from qspectra import hamiltonian


class TestElectronicHamiltonian(unittest.TestCase):
    def setUp(self):
        self.M = np.array([[1., 0], [0, 3]])
        self.H_el = hamiltonian.ElectronicHamiltonian(self.M, 1.0, None, 1)

    def test_properties(self):
        self.assertEqual(self.H_el.disorder_fwhm, 1.0)
        self.assertEqual(self.H_el.ref_system, self.H_el)
        self.assertEqual(self.H_el.sampling_freq_extra, 1)
        self.assertEqual(self.H_el.n_sites, 2)
        self.assertEqual(self.H_el.n_states('gef'), 4)
        self.assertEqual(self.H_el.freq_step, 10.0)
        self.assertEqual(self.H_el.time_step, 0.1)
        assert_allclose(self.H_el.H('e'), self.M)
        assert_allclose(self.H_el.E('g'), [0])
        assert_allclose(self.H_el.E('ge'), [0, 1, 3])
        assert_allclose(self.H_el.E('gef'), [0, 1, 3, 4])
        self.assertEqual(self.H_el.central_freq, 2)

    def test_rotating_frame(self):
        H_rw = self.H_el.in_rotating_frame(2)
        assert_allclose(H_rw.H('e'), [[-1, 0], [0, 1]])
        self.assertItemsEqual(H_rw.E('gef'), [0, 1, -1, 0])
        self.assertEqual(H_rw.central_freq, 0.0)
        self.assertEqual(H_rw.freq_step, 6.0)

    def test_sample(self):
        H_sampled = list(self.H_el.sample(1))[0]
        self.assertEqual(self.H_el, H_sampled.ref_system)
        self.assertEqual(H_sampled.disorder_fwhm, 0.0)
