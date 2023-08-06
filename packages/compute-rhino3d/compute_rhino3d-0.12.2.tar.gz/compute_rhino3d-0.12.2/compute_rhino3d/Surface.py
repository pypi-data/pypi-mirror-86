from . import Util
try:
    from itertools import izip as zip # python 2
except ImportError:
    pass # python 3


def CreateRollingBallFillet(surfaceA, surfaceB, radius, tolerance, multiple=False):
    """
    Constructs a rolling ball fillet between two surfaces.

    Args:
        surfaceA (Surface): A first surface.
        surfaceB (Surface): A second surface.
        radius (double): A radius value.
        tolerance (double): A tolerance value.

    Returns:
        Surface[]: A new array of rolling ball fillet surfaces; this array can be empty on failure.
    """
    url = "rhino/geometry/surface/createrollingballfillet-surface_surface_double_double"
    if multiple: url += "?multiple=true"
    args = [surfaceA, surfaceB, radius, tolerance]
    if multiple: args = list(zip(surfaceA, surfaceB, radius, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreateRollingBallFillet1(surfaceA, flipA, surfaceB, flipB, radius, tolerance, multiple=False):
    """
    Constructs a rolling ball fillet between two surfaces.

    Args:
        surfaceA (Surface): A first surface.
        flipA (bool): A value that indicates whether A should be used in flipped mode.
        surfaceB (Surface): A second surface.
        flipB (bool): A value that indicates whether B should be used in flipped mode.
        radius (double): A radius value.
        tolerance (double): A tolerance value.

    Returns:
        Surface[]: A new array of rolling ball fillet surfaces; this array can be empty on failure.
    """
    url = "rhino/geometry/surface/createrollingballfillet-surface_bool_surface_bool_double_double"
    if multiple: url += "?multiple=true"
    args = [surfaceA, flipA, surfaceB, flipB, radius, tolerance]
    if multiple: args = list(zip(surfaceA, flipA, surfaceB, flipB, radius, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreateRollingBallFillet2(surfaceA, uvA, surfaceB, uvB, radius, tolerance, multiple=False):
    """
    Constructs a rolling ball fillet between two surfaces.

    Args:
        surfaceA (Surface): A first surface.
        uvA (Point2d): A point in the parameter space of FaceA near where the fillet is expected to hit the surface.
        surfaceB (Surface): A second surface.
        uvB (Point2d): A point in the parameter space of FaceB near where the fillet is expected to hit the surface.
        radius (double): A radius value.
        tolerance (double): A tolerance value used for approximating and intersecting offset surfaces.

    Returns:
        Surface[]: A new array of rolling ball fillet surfaces; this array can be empty on failure.
    """
    url = "rhino/geometry/surface/createrollingballfillet-surface_point2d_surface_point2d_double_double"
    if multiple: url += "?multiple=true"
    args = [surfaceA, uvA, surfaceB, uvB, radius, tolerance]
    if multiple: args = list(zip(surfaceA, uvA, surfaceB, uvB, radius, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreateExtrusion(profile, direction, multiple=False):
    """
    Constructs a surface by extruding a curve along a vector.

    Args:
        profile (Curve): Profile curve to extrude.
        direction (Vector3d): Direction and length of extrusion.

    Returns:
        Surface: A surface on success or None on failure.
    """
    url = "rhino/geometry/surface/createextrusion-curve_vector3d"
    if multiple: url += "?multiple=true"
    args = [profile, direction]
    if multiple: args = list(zip(profile, direction))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreateExtrusionToPoint(profile, apexPoint, multiple=False):
    """
    Constructs a surface by extruding a curve to a point.

    Args:
        profile (Curve): Profile curve to extrude.
        apexPoint (Point3d): Apex point of extrusion.

    Returns:
        Surface: A Surface on success or None on failure.
    """
    url = "rhino/geometry/surface/createextrusiontopoint-curve_point3d"
    if multiple: url += "?multiple=true"
    args = [profile, apexPoint]
    if multiple: args = list(zip(profile, apexPoint))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreatePeriodicSurface(surface, direction, multiple=False):
    """
    Constructs a periodic surface from a base surface and a direction.

    Args:
        surface (Surface): The surface to make periodic.
        direction (int): The direction to make periodic, either 0 = U, or 1 = V.

    Returns:
        Surface: A Surface on success or None on failure.
    """
    url = "rhino/geometry/surface/createperiodicsurface-surface_int"
    if multiple: url += "?multiple=true"
    args = [surface, direction]
    if multiple: args = list(zip(surface, direction))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreatePeriodicSurface1(surface, direction, bSmooth, multiple=False):
    """
    Constructs a periodic surface from a base surface and a direction.

    Args:
        surface (Surface): The surface to make periodic.
        direction (int): The direction to make periodic, either 0 = U, or 1 = V.
        bSmooth (bool): Controls kink removal. If true, smooths any kinks in the surface and moves control points
            to make a smooth surface. If false, control point locations are not changed or changed minimally
            (only one point may move) and only the knot vector is altered.

    Returns:
        Surface: A periodic surface if successful, None on failure.
    """
    url = "rhino/geometry/surface/createperiodicsurface-surface_int_bool"
    if multiple: url += "?multiple=true"
    args = [surface, direction, bSmooth]
    if multiple: args = list(zip(surface, direction, bSmooth))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def CreateSoftEditSurface(surface, uv, delta, uLength, vLength, tolerance, fixEnds, multiple=False):
    """
    Creates a soft edited surface from an existing surface using a smooth field of influence.

    Args:
        surface (Surface): The surface to soft edit.
        uv (Point2d): A point in the parameter space to move from. This location on the surface is moved,
            and the move is smoothly tapered off with increasing distance along the surface from
            this parameter.
        delta (Vector3d): The direction and magnitude, or maximum distance, of the move.
        uLength (double): The distance along the surface's u-direction from the editing point over which the
            strength of the editing falls off smoothly.
        vLength (double): The distance along the surface's v-direction from the editing point over which the
            strength of the editing falls off smoothly.
        tolerance (double): The active document's model absolute tolerance.
        fixEnds (bool): Keeps edge locations fixed.

    Returns:
        Surface: The soft edited surface if successful. None on failure.
    """
    url = "rhino/geometry/surface/createsofteditsurface-surface_point2d_vector3d_double_double_double_bool"
    if multiple: url += "?multiple=true"
    args = [surface, uv, delta, uLength, vLength, tolerance, fixEnds]
    if multiple: args = list(zip(surface, uv, delta, uLength, vLength, tolerance, fixEnds))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Smooth(thisSurface, smoothFactor, bXSmooth, bYSmooth, bZSmooth, bFixBoundaries, coordinateSystem, multiple=False):
    """
    Smooths a surface by averaging the positions of control points in a specified region.

    Args:
        smoothFactor (double): The smoothing factor, which controls how much control points move towards the average of the neighboring control points.
        bXSmooth (bool): When True control points move in X axis direction.
        bYSmooth (bool): When True control points move in Y axis direction.
        bZSmooth (bool): When True control points move in Z axis direction.
        bFixBoundaries (bool): When True the surface edges don't move.
        coordinateSystem (SmoothingCoordinateSystem): The coordinates to determine the direction of the smoothing.

    Returns:
        Surface: The smoothed surface if successful, None otherwise.
    """
    url = "rhino/geometry/surface/smooth-surface_double_bool_bool_bool_bool_smoothingcoordinatesystem"
    if multiple: url += "?multiple=true"
    args = [thisSurface, smoothFactor, bXSmooth, bYSmooth, bZSmooth, bFixBoundaries, coordinateSystem]
    if multiple: args = list(zip(thisSurface, smoothFactor, bXSmooth, bYSmooth, bZSmooth, bFixBoundaries, coordinateSystem))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Smooth1(thisSurface, smoothFactor, bXSmooth, bYSmooth, bZSmooth, bFixBoundaries, coordinateSystem, plane, multiple=False):
    """
    Smooths a surface by averaging the positions of control points in a specified region.

    Args:
        smoothFactor (double): The smoothing factor, which controls how much control points move towards the average of the neighboring control points.
        bXSmooth (bool): When True control points move in X axis direction.
        bYSmooth (bool): When True control points move in Y axis direction.
        bZSmooth (bool): When True control points move in Z axis direction.
        bFixBoundaries (bool): When True the surface edges don't move.
        coordinateSystem (SmoothingCoordinateSystem): The coordinates to determine the direction of the smoothing.
        plane (Plane): If SmoothingCoordinateSystem.CPlane specified, then the construction plane.

    Returns:
        Surface: The smoothed surface if successful, None otherwise.
    """
    url = "rhino/geometry/surface/smooth-surface_double_bool_bool_bool_bool_smoothingcoordinatesystem_plane"
    if multiple: url += "?multiple=true"
    args = [thisSurface, smoothFactor, bXSmooth, bYSmooth, bZSmooth, bFixBoundaries, coordinateSystem, plane]
    if multiple: args = list(zip(thisSurface, smoothFactor, bXSmooth, bYSmooth, bZSmooth, bFixBoundaries, coordinateSystem, plane))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def VariableOffset(thisSurface, uMinvMin, uMinvMax, uMaxvMin, uMaxvMax, tolerance, multiple=False):
    """
    Copies a surface so that all locations at the corners of the copied surface are specified distances from the original surface.

    Args:
        uMinvMin (double): Offset distance at Domain(0).Min, Domain(1).Min.
        uMinvMax (double): Offset distance at Domain(0).Min, Domain(1).Max.
        uMaxvMin (double): Offset distance at Domain(0).Max, Domain(1).Min.
        uMaxvMax (double): Offset distance at Domain(0).Max, Domain(1).Max.
        tolerance (double): The offset tolerance.

    Returns:
        Surface: The offset surface if successful, None otherwise.
    """
    url = "rhino/geometry/surface/variableoffset-surface_double_double_double_double_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, uMinvMin, uMinvMax, uMaxvMin, uMaxvMax, tolerance]
    if multiple: args = list(zip(thisSurface, uMinvMin, uMinvMax, uMaxvMin, uMaxvMax, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def VariableOffset1(thisSurface, uMinvMin, uMinvMax, uMaxvMin, uMaxvMax, interiorParameters, interiorDistances, tolerance, multiple=False):
    """
    Copies a surface so that all locations at the corners, and from specified interior locations, of the copied surface are specified distances from the original surface.

    Args:
        uMinvMin (double): Offset distance at Domain(0).Min, Domain(1).Min.
        uMinvMax (double): Offset distance at Domain(0).Min, Domain(1).Max.
        uMaxvMin (double): Offset distance at Domain(0).Max, Domain(1).Min.
        uMaxvMax (double): Offset distance at Domain(0).Max, Domain(1).Max.
        interiorParameters (IEnumerable<Point2d>): An array of interior UV parameters to offset from.
        interiorDistances (IEnumerable<double>): >An array of offset distances at the interior UV parameters.
        tolerance (double): The offset tolerance.

    Returns:
        Surface: The offset surface if successful, None otherwise.
    """
    url = "rhino/geometry/surface/variableoffset-surface_double_double_double_double_point2darray_doublearray_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, uMinvMin, uMinvMax, uMaxvMin, uMaxvMax, interiorParameters, interiorDistances, tolerance]
    if multiple: args = list(zip(thisSurface, uMinvMin, uMinvMax, uMaxvMin, uMaxvMax, interiorParameters, interiorDistances, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def GetSurfaceSize(thisSurface, multiple=False):
    """
    Gets an estimate of the size of the rectangle that would be created
    if the 3d surface where flattened into a rectangle.

    Returns:
        bool: True if successful.
        width (double): corresponds to the first surface parameter.
        height (double): corresponds to the second surface parameter.
    """
    url = "rhino/geometry/surface/getsurfacesize-surface_double_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface]
    if multiple: args = [[item] for item in thisSurface]
    response = Util.ComputeFetch(url, args)
    return response


def ClosestSide(thisSurface, u, v, multiple=False):
    """
    Gets the side that is closest, in terms of 3D-distance, to a U and V parameter.

    Args:
        u (double): A u parameter.
        v (double): A v parameter.

    Returns:
        IsoStatus: A side.
    """
    url = "rhino/geometry/surface/closestside-surface_double_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, u, v]
    if multiple: args = list(zip(thisSurface, u, v))
    response = Util.ComputeFetch(url, args)
    return response


def Extend(thisSurface, edge, extensionLength, smooth, multiple=False):
    """
    Extends an untrimmed surface along one edge.

    Args:
        edge (IsoStatus): Edge to extend.  Must be North, South, East, or West.
        extensionLength (double): distance to extend.
        smooth (bool): True for smooth (C-infinity) extension.
            False for a C1- ruled extension.

    Returns:
        Surface: New extended surface on success.
    """
    url = "rhino/geometry/surface/extend-surface_isostatus_double_bool"
    if multiple: url += "?multiple=true"
    args = [thisSurface, edge, extensionLength, smooth]
    if multiple: args = list(zip(thisSurface, edge, extensionLength, smooth))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Rebuild(thisSurface, uDegree, vDegree, uPointCount, vPointCount, multiple=False):
    """
    Rebuilds an existing surface to a given degree and point count.

    Args:
        uDegree (int): the output surface u degree.
        vDegree (int): the output surface u degree.
        uPointCount (int): The number of points in the output surface u direction. Must be bigger
            than uDegree (maximum value is 1000)
        vPointCount (int): The number of points in the output surface v direction. Must be bigger
            than vDegree (maximum value is 1000)

    Returns:
        NurbsSurface: new rebuilt surface on success. None on failure.
    """
    url = "rhino/geometry/surface/rebuild-surface_int_int_int_int"
    if multiple: url += "?multiple=true"
    args = [thisSurface, uDegree, vDegree, uPointCount, vPointCount]
    if multiple: args = list(zip(thisSurface, uDegree, vDegree, uPointCount, vPointCount))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def RebuildOneDirection(thisSurface, direction, pointCount, loftType, refitTolerance, multiple=False):
    """
    Rebuilds an existing surface with a new surface to a given point count in either the u or v directions independently.

    Args:
        direction (int): The direction (0 = U, 1 = V).
        pointCount (int): The number of points in the output surface in the "direction" direction.
        loftType (LoftType): The loft type
        refitTolerance (double): The refit tolerance. When in doubt, use the document's model absolute tolerance.

    Returns:
        NurbsSurface: new rebuilt surface on success. None on failure.
    """
    url = "rhino/geometry/surface/rebuildonedirection-surface_int_int_lofttype_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, direction, pointCount, loftType, refitTolerance]
    if multiple: args = list(zip(thisSurface, direction, pointCount, loftType, refitTolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def ClosestPoint(thisSurface, testPoint, multiple=False):
    """
    Input the parameters of the point on the surface that is closest to testPoint.

    Args:
        testPoint (Point3d): A point to test against.

    Returns:
        bool: True on success, False on failure.
        u (double): U parameter of the surface that is closest to testPoint.
        v (double): V parameter of the surface that is closest to testPoint.
    """
    url = "rhino/geometry/surface/closestpoint-surface_point3d_double_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, testPoint]
    if multiple: args = list(zip(thisSurface, testPoint))
    response = Util.ComputeFetch(url, args)
    return response


def LocalClosestPoint(thisSurface, testPoint, seedU, seedV, multiple=False):
    """
    Find parameters of the point on a surface that is locally closest to
    the testPoint. The search for a local close point starts at seed parameters.

    Args:
        testPoint (Point3d): A point to test against.
        seedU (double): The seed parameter in the U direction.
        seedV (double): The seed parameter in the V direction.

    Returns:
        bool: True if the search is successful, False if the search fails.
        u (double): U parameter of the surface that is closest to testPoint.
        v (double): V parameter of the surface that is closest to testPoint.
    """
    url = "rhino/geometry/surface/localclosestpoint-surface_point3d_double_double_double_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, testPoint, seedU, seedV]
    if multiple: args = list(zip(thisSurface, testPoint, seedU, seedV))
    response = Util.ComputeFetch(url, args)
    return response


def Offset(thisSurface, distance, tolerance, multiple=False):
    """
    Constructs a new surface which is offset from the current surface.

    Args:
        distance (double): Distance (along surface normal) to offset.
        tolerance (double): Offset accuracy.

    Returns:
        Surface: The offset surface or None on failure.
    """
    url = "rhino/geometry/surface/offset-surface_double_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, distance, tolerance]
    if multiple: args = list(zip(thisSurface, distance, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Fit(thisSurface, uDegree, vDegree, fitTolerance, multiple=False):
    """
    Fits a new surface through an existing surface.

    Args:
        uDegree (int): the output surface U degree. Must be bigger than 1.
        vDegree (int): the output surface V degree. Must be bigger than 1.
        fitTolerance (double): The fitting tolerance.

    Returns:
        Surface: A surface, or None on error.
    """
    url = "rhino/geometry/surface/fit-surface_int_int_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, uDegree, vDegree, fitTolerance]
    if multiple: args = list(zip(thisSurface, uDegree, vDegree, fitTolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def InterpolatedCurveOnSurfaceUV(thisSurface, points, tolerance, multiple=False):
    """
    Returns a curve that interpolates points on a surface. The interpolant lies on the surface.

    Args:
        points (System.Collections.Generic.IEnumerable<Point2d>): List of at least two UV parameter locations on the surface.
        tolerance (double): Tolerance used for the fit of the push-up curve. Generally, the resulting interpolating curve will be within tolerance of the surface.

    Returns:
        NurbsCurve: A new NURBS curve if successful, or None on error.
    """
    url = "rhino/geometry/surface/interpolatedcurveonsurfaceuv-surface_point2darray_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, points, tolerance]
    if multiple: args = list(zip(thisSurface, points, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def InterpolatedCurveOnSurfaceUV1(thisSurface, points, tolerance, closed, closedSurfaceHandling, multiple=False):
    """
    Returns a curve that interpolates points on a surface. The interpolant lies on the surface.

    Args:
        points (System.Collections.Generic.IEnumerable<Point2d>): List of at least two UV parameter locations on the surface.
        tolerance (double): Tolerance used for the fit of the push-up curve. Generally, the resulting interpolating curve will be within tolerance of the surface.
        closed (bool): If false, the interpolating curve is not closed. If true, the interpolating curve is closed, and the last point and first point should generally not be equal.
        closedSurfaceHandling (int): If 0, all points must be in the rectangular domain of the surface. If the surface is closed in some direction,
            then this routine will interpret each point and place it at an appropriate location in the covering space.
            This is the simplest option and should give good results.
            If 1, then more options for more control of handling curves going across seams are available.
            If the surface is closed in some direction, then the points are taken as points in the covering space.
            Example, if srf.IsClosed(0)=True and srf.IsClosed(1)=False and srf.Domain(0)=srf.Domain(1)=Interval(0,1)
            then if closedSurfaceHandling=1 a point(u, v) in points can have any value for the u coordinate, but must have 0<=v<=1.
            In particular, if points = { (0.0,0.5), (2.0,0.5) } then the interpolating curve will wrap around the surface two times in the closed direction before ending at start of the curve.
            If closed=True the last point should equal the first point plus an integer multiple of the period on a closed direction.

    Returns:
        NurbsCurve: A new NURBS curve if successful, or None on error.
    """
    url = "rhino/geometry/surface/interpolatedcurveonsurfaceuv-surface_point2darray_double_bool_int"
    if multiple: url += "?multiple=true"
    args = [thisSurface, points, tolerance, closed, closedSurfaceHandling]
    if multiple: args = list(zip(thisSurface, points, tolerance, closed, closedSurfaceHandling))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def InterpolatedCurveOnSurface(thisSurface, points, tolerance, multiple=False):
    """
    Constructs an interpolated curve on a surface, using 3D points.

    Args:
        points (System.Collections.Generic.IEnumerable<Point3d>): A list, an array or any enumerable set of points.
        tolerance (double): A tolerance value.

    Returns:
        NurbsCurve: A new NURBS curve, or None on error.
    """
    url = "rhino/geometry/surface/interpolatedcurveonsurface-surface_point3darray_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, points, tolerance]
    if multiple: args = list(zip(thisSurface, points, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def ShortPath(thisSurface, start, end, tolerance, multiple=False):
    """
    Constructs a geodesic between 2 points, used by ShortPath command in Rhino.

    Args:
        start (Point2d): start point of curve in parameter space. Points must be distinct in the domain of the surface.
        end (Point2d): end point of curve in parameter space. Points must be distinct in the domain of the surface.
        tolerance (double): tolerance used in fitting discrete solution.

    Returns:
        Curve: a geodesic curve on the surface on success. None on failure.
    """
    url = "rhino/geometry/surface/shortpath-surface_point2d_point2d_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, start, end, tolerance]
    if multiple: args = list(zip(thisSurface, start, end, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Pushup(thisSurface, curve2d, tolerance, curve2dSubdomain, multiple=False):
    """
    Computes a 3d curve that is the composite of a 2d curve and the surface map.

    Args:
        curve2d (Curve): a 2d curve whose image is in the surface's domain.
        tolerance (double): the maximum acceptable distance from the returned 3d curve to the image of curve_2d on the surface.
        curve2dSubdomain (Interval): The curve interval (a sub-domain of the original curve) to use.

    Returns:
        Curve: 3d curve.
    """
    url = "rhino/geometry/surface/pushup-surface_curve_double_interval"
    if multiple: url += "?multiple=true"
    args = [thisSurface, curve2d, tolerance, curve2dSubdomain]
    if multiple: args = list(zip(thisSurface, curve2d, tolerance, curve2dSubdomain))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Pushup1(thisSurface, curve2d, tolerance, multiple=False):
    """
    Computes a 3d curve that is the composite of a 2d curve and the surface map.

    Args:
        curve2d (Curve): a 2d curve whose image is in the surface's domain.
        tolerance (double): the maximum acceptable distance from the returned 3d curve to the image of curve_2d on the surface.

    Returns:
        Curve: 3d curve.
    """
    url = "rhino/geometry/surface/pushup-surface_curve_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, curve2d, tolerance]
    if multiple: args = list(zip(thisSurface, curve2d, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Pullback(thisSurface, curve3d, tolerance, multiple=False):
    """
    Pulls a 3d curve back to the surface's parameter space.

    Args:
        curve3d (Curve): The curve to pull.
        tolerance (double): the maximum acceptable 3d distance between from surface(curve_2d(t))
            to the locus of points on the surface that are closest to curve_3d.

    Returns:
        Curve: 2d curve.
    """
    url = "rhino/geometry/surface/pullback-surface_curve_double"
    if multiple: url += "?multiple=true"
    args = [thisSurface, curve3d, tolerance]
    if multiple: args = list(zip(thisSurface, curve3d, tolerance))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response


def Pullback1(thisSurface, curve3d, tolerance, curve3dSubdomain, multiple=False):
    """
    Pulls a 3d curve back to the surface's parameter space.

    Args:
        curve3d (Curve): A curve.
        tolerance (double): the maximum acceptable 3d distance between from surface(curve_2d(t))
            to the locus of points on the surface that are closest to curve_3d.
        curve3dSubdomain (Interval): A sub-domain of the curve to sample.

    Returns:
        Curve: 2d curve.
    """
    url = "rhino/geometry/surface/pullback-surface_curve_double_interval"
    if multiple: url += "?multiple=true"
    args = [thisSurface, curve3d, tolerance, curve3dSubdomain]
    if multiple: args = list(zip(thisSurface, curve3d, tolerance, curve3dSubdomain))
    response = Util.ComputeFetch(url, args)
    response = Util.DecodeToCommonObject(response)
    return response

