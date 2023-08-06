import numpy as np
from itertools import combinations

from scipy.spatial import Delaunay

import delcechfiltr.cpp.binding as _cpp
import delcechfiltr.tri
import delcechfiltr.tetra

from gudhi import SimplexTree

def delaunay_simplices(points):
    """Simplices of the Euclidean Delaunay triangulation of `points`."""
    dim = len(points[0])
    if dim == 2:
        out_del = Delaunay(points)
        tri_del = out_del.simplices
        tri_del = sorted([sorted(tri) for tri in tri_del])
        edges_del = set()
        for v1, v2, v3 in tri_del:
            edges_del.add((v1, v2))
            edges_del.add((v1, v3))
            edges_del.add((v2, v3))
        edges_del = list(edges_del)
        return np.arange(len(points)), edges_del, tri_del
    elif dim == 3:
        out_del = Delaunay(points)
        tetra_del = out_del.simplices
        tetra_del = sorted([sorted(tetra) for tetra in tetra_del])
        edges_del = set()
        tri_del = set()
        for v1, v2, v3, v4 in tetra_del:
            edges_del.add((v1, v2))
            edges_del.add((v1, v3))
            edges_del.add((v1, v4))
            edges_del.add((v2, v3))
            edges_del.add((v2, v4))
            edges_del.add((v3, v4))

            tri_del.add((v1, v2, v3))
            tri_del.add((v1, v2, v4))
            tri_del.add((v1, v3, v4))
            tri_del.add((v2, v3, v4))

        edges_del = list(edges_del)
        tri_del = list(tri_del)
        return np.arange(len(points)), edges_del, tri_del, tetra_del
    else:
        print("elements of `points` must be 2 or 3 dimensional")
        return None

def simplices_and_cech_param(points, stacked_output=True):
    """Simplices of the Euclidean Delaunay triangulation of `points` and
    their smallest encolisng ball radiuses, i.e. Cech complex parameter."""
    dim = len(points[0])
    if dim == 2:
        vert, edges_del, tri_del = delaunay_simplices(points)
        sim0 = np.array([[v, -1, -1] for v in vert])
        sim1 = np.array([[ed[0], ed[1], -1] for ed in edges_del])
        simplices = np.vstack([sim0, sim1, tri_del])

        param_edges = [_cpp.half_euclidean(points[i], points[j])  for (i,j) in edges_del]
        param_tri = delcechfiltr.tri.cech_param_list(points, tri_del)
        parameterization = np.hstack([np.zeros(len(points)),
                                     param_edges,
                                     param_tri])

        if stacked_output:
            return simplices, parameterization
        else:
            return vert, edges_del, tri_del, np.zeros(len(vert)), param_edges, param_tri
    elif dim == 3:
        vert, edges_del, tri_del, tetra_del = delaunay_simplices(points)
        sim0 = np.array([[v, -1, -1, -1] for v in range(len(points))])
        sim1 = np.array([[ed[0], ed[1], -1, -1] for ed in edges_del])
        sim2 = np.array([[tri[0], tri[1], tri[2], -1]
                         for tri in tri_del])
        simplices = np.vstack([sim0, sim1, sim2, tetra_del])

        param_edges = [_cpp.half_euclidean(points[i], points[j]) for (i,j) in edges_del]
        param_tri = delcechfiltr.tri.cech_param_list(points, tri_del)
        param_tetra = delcechfiltr.tetra.cech_param_list(points, tetra_del)
        parameterization = np.hstack([np.zeros(len(points)),
                                     param_edges,
                                     param_tri,
                                     param_tetra])

        if stacked_output:
            return simplices, parameterization
        else:
            return vert, edges_del, tri_del, tetra_del, np.zeros(len(vert)), param_edges, param_tri, param_tetra
    else:
        print("elements of `points` must be 2 or 3 dimensional")
        return None

def cech(points, homology_coeff_field=2, persistence_dim_max=True):
    """Cech persistence diagrams of two or three-dimensional points
    using `gudhi` and Cech filtration."""
    edges = list(combinations(range(len(points)), 2))
    tri = list(combinations(range(len(points)), 3))
    if persistence_dim_max:
        tetra = list(combinations(range(len(points)), 4))

    st = SimplexTree()
    param_edges = [_cpp.half_euclidean(points[i], points[j]) for (i,j) in edges]
    param_tri = delcechfiltr.tri.cech_param_list(points, tri)
    if persistence_dim_max:
        param_tetra = delcechfiltr.tetra.cech_param_list(points, tetra)

    for i, v in enumerate(points):
        st.insert([i], 0.0)
    for e, r1 in zip(edges, param_edges):
        st.insert(e, r1)
    for t, r2 in zip(tri, param_tri):
        st.insert(t, r2)
    if persistence_dim_max:
        for te, r3 in zip(tetra, param_tetra):
            st.insert(te, r3)
    st.make_filtration_non_decreasing()
    dgms = st.persistence(homology_coeff_field=homology_coeff_field,
                          persistence_dim_max=persistence_dim_max)
    dgm0 = np.array([p for dim, p in dgms if dim == 0])
    dgm0 = dgm0[np.argsort(dgm0[:,1])]
    dgm1 = np.array([p for dim, p in dgms if dim == 1])
    if len(dgm1) > 0:
        dgm1 = dgm1[np.argsort(dgm1[:,1])]

    if persistence_dim_max:
        dgm2 = np.array([p for dim, p in dgms if dim == 2])
        if len(dgm2) > 0:
            dgm2 = dgm2[np.argsort(dgm2[:,1])]
        return dgm0, dgm1, dgm2
    else:
        return dgm0, dgm1

def delcech_2D(points, homology_coeff_field=2, persistence_dim_max=True):
    """Cech persistence diagrams of two-dimensional points
    using `gudhi` and Delaunay-Cech filtration."""
    vert, edges_del, tri_del = delaunay_simplices(points)
    st = SimplexTree()
    param_edges = [_cpp.half_euclidean(points[i], points[j]) for (i,j) in edges_del]
    param_tri = delcechfiltr.tri.cech_param_list(points, tri_del)
    for i, v in enumerate(points):
        st.insert([i], 0.0)
    for e, r1 in zip(edges_del, param_edges):
        st.insert(e, r1)
    for t, r2 in zip(tri_del, param_tri):
        st.insert(t, r2)
    st.make_filtration_non_decreasing()
    dgms = st.persistence(homology_coeff_field=homology_coeff_field,
                          persistence_dim_max=persistence_dim_max)
    dgm0 = np.array([p for dim, p in dgms if dim == 0])
    dgm0 = dgm0[np.argsort(dgm0[:,1])]
    dgm1 = np.array([p for dim, p in dgms if dim == 1])
    dgm1 = dgm1[np.argsort(dgm1[:,1])]
    return dgm0, dgm1

def delcech_3D(points, homology_coeff_field=2, persistence_dim_max=True):
    """Cech persistence diagrams of three-dimensional points
    using `gudhi` and Dekaunay-Cech filtration."""
    vert, edges_del, tri_del, tetra_del = delaunay_simplices(points)

    st = SimplexTree()
    param_edges = [_cpp.half_euclidean(points[i], points[j]) for (i,j) in edges_del]
    param_tri = delcechfiltr.tri.cech_param_list(points, tri_del)
    if persistence_dim_max:
        param_tetra = delcechfiltr.tetra.cech_param_list(points, tetra_del)

    for i, v in enumerate(points):
        st.insert([i], 0.0)
    for e, r1 in zip(edges_del, param_edges):
        st.insert(e, r1)
    for t, r2 in zip(tri_del, param_tri):
        st.insert(t, r2)
    if persistence_dim_max:
        for te, r3 in zip(tetra_del, param_tetra):
            st.insert(te, r3)
    st.make_filtration_non_decreasing()

    dgms = st.persistence(homology_coeff_field=homology_coeff_field,
                          persistence_dim_max=persistence_dim_max)
    dgm0 = np.array([p for dim, p in dgms if dim == 0])
    dgm0 = dgm0[np.argsort(dgm0[:,1])]
    dgm1 = np.array([p for dim, p in dgms if dim == 1])
    if len(dgm1) > 0:
        dgm1 = dgm1[np.argsort(dgm1[:,1])]

    if persistence_dim_max:
        dgm2 = np.array([p for dim, p in dgms if dim == 2])
        if len(dgm2) > 0:
            dgm2 = dgm2[np.argsort(dgm2[:,1])]
        return dgm0, dgm1, dgm2
    else:
        return dgm0, dgm1
