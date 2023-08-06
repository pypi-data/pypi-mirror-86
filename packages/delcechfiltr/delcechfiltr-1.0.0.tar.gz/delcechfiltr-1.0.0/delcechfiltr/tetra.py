import delcechfiltr.cpp.binding as _cpp

def circumradius(vertices):
    return _cpp.tetrahedron_circumradius(vertices)

def det_2x2(matrix):
    return _cpp.tetrahedron_det_2x2(matrix)

def det_3x3(matrix):
    return _cpp.tetrahedron_det_3x3(matrix)

def inv_3x3(matrix):
    return _cpp.tetrahedron_inv_3x3(matrix)

def is_on_correct_side(A, B, C, test_point, circum):
    return _cpp.tetrahedron_is_on_correct_side(A, B, C, test_point, circum)

def circumcenter(vertices):
    return _cpp.tetrahedron_circumcenter(vertices)

def cech_parameter(vertices):
    return _cpp.tetrahedron_cech_parameter(vertices)

def cech_param_list(points, tetrahedra):
    return _cpp.tetrahedron_cech_param_list(points, tetrahedra)
