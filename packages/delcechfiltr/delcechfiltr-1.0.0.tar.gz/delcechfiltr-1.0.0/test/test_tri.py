import numpy as np
from scipy.spatial.distance import euclidean
import delcechfiltr.tri

def test_circumradius_2D():
    n, d = 3, 2   # number points and dimension
    for i in range(10):
        np.random.seed(i)
        vertices = np.random.rand(n, d)
        radius = delcechfiltr.tri.circumradius(vertices)
        center = delcechfiltr.tri.circumcenter(vertices)
        dist = [euclidean(center, x) for x in vertices]
        err_msg = "mismatch between miniball center and \n" \
                  "miniball radius."
        assert all([np.isclose(radius, dist_i) or radius > dist_i
                    for dist_i in dist]), err_msg

def test_circumradius_3D():
    n, d = 3, 3   # number points and dimension
    for i in range(10):
        np.random.seed(i)
        vertices = np.random.rand(n, d)
        radius = delcechfiltr.tri.circumradius(vertices)
        center = delcechfiltr.tri.circumcenter(vertices)
        dist = [euclidean(center, x) for x in vertices]
        err_msg = "mismatch between miniball center and \n" \
                  "miniball radius."
        assert all([np.isclose(radius, dist_i) or radius > dist_i
                    for dist_i in dist]), err_msg

def test_cech_param_2D():
    n, d = 3, 2   # number points and dimension
    for i in range(10):
        np.random.seed(i)
        vertices = np.random.rand(n, d)
        radius = delcechfiltr.tri.cech_parameter(vertices)
        center = delcechfiltr.tri.miniball_center(vertices)
        dist = [euclidean(center, x) for x in vertices]
        err_msg = "mismatch between miniball center and \n" \
                  "miniball radius."
        assert all([np.isclose(radius, dist_i) or radius > dist_i
                    for dist_i in dist]), err_msg

def test_cech_param_3D():
    n, d = 3, 3   # number points and dimension
    for i in range(10):
        np.random.seed(i)
        vertices = np.random.rand(n, d)
        radius = delcechfiltr.tri.cech_parameter(vertices)
        center = delcechfiltr.tri.miniball_center(vertices)
        dist = [euclidean(center, x) for x in vertices]
        err_msg = "mismatch between miniball center and \n" \
                  "miniball radius."
        assert all([np.isclose(radius, dist_i) or radius > dist_i
                    for dist_i in dist]), err_msg
