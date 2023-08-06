import delcechfiltr.cpp.binding as _cpp

def circumradius(vertices):
    dim = len(vertices[0])
    if dim == 2:
        return _cpp.triangle_circumradius_2D(vertices)
    elif dim == 3:
        return _cpp.triangle_circumradius_3D(vertices)
    else:
        print("elements of `vertices` must be 2 or 3 dimensional")
        return None

def circumcenter(vertices):
    dim = len(vertices[0])
    if dim == 2:
        return _cpp.triangle_circumcenter_2D(vertices)
    elif dim == 3:
        return _cpp.triangle_circumcenter_3D(vertices)
    else:
        print("elements of `vertices` must be 2 or 3 dimensional")
        return None

def miniball_center(vertices):
    dim = len(vertices[0])
    if dim == 2:
        return _cpp.triangle_miniball_center_2D(vertices)
    elif dim == 3:
        return _cpp.triangle_miniball_center_3D(vertices)
    else:
        print("elements of `vertices` must be 2 or 3 dimensional")
        return None

def cech_parameter(vertices):
    dim = len(vertices[0])
    if dim == 2:
        return _cpp.triangle_cech_parameter_2D(vertices)
    elif dim == 3:
        return _cpp.triangle_cech_parameter_3D(vertices)
    else:
        print("elements of `vertices` must be 2 or 3 dimensional")
        return None

def cech_param_list(points, triangles):
    dim = len(points[0])
    if dim == 2:
        return _cpp.triangle_cech_param_list_2D(points, triangles)
    elif dim == 3:
        return _cpp.triangle_cech_param_list_3D(points, triangles)
    else:
        print("elements of `list_vertices[0]` must be 2 or 3 dimensional")
        return None
