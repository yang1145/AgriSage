import json
import math


def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate the distance in meters between two lat/lng points using the Haversine formula."""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_area_from_geojson(geojson):
    """
    Takes a GeoJSON polygon and calculates area in 亩 (mu).

    Uses the Shoelace formula with Haversine distance for lat/lng coordinates.
    1 亩 = 666.67 平方米

    Args:
        geojson: A GeoJSON dict or JSON string containing a Polygon geometry.

    Returns:
        Area in 亩 (mu), or 0 if calculation is not possible.
    """
    if isinstance(geojson, str):
        try:
            geojson = json.loads(geojson)
        except (json.JSONDecodeError, TypeError):
            return 0

    # Extract coordinates from GeoJSON Polygon
    if geojson.get('type') != 'Polygon':
        return 0

    rings = geojson.get('coordinates', [])
    if not rings:
        return 0

    ring = rings[0]  # Outer ring
    if len(ring) < 4:  # A valid polygon ring has at least 4 points (closed)
        return 0

    # Convert to (lat, lng) pairs
    points = [(coord[1], coord[0]) for coord in ring]

    # Calculate area using Shoelace formula with Haversine distances
    n = len(points)
    area_sq_meters = 0.0

    for i in range(n - 1):
        lat1, lng1 = points[i]
        lat2, lng2 = points[i + 1]

        # Distance from origin (first point) to point i
        d1 = haversine_distance(points[0][0], points[0][1], lat1, lng1)
        # Distance from origin to point i+1
        d2 = haversine_distance(points[0][0], points[0][1], lat2, lng2)
        # Distance between point i and point i+1
        d12 = haversine_distance(lat1, lng1, lat2, lng2)

        # Use Heron's formula to get area of triangle (origin, i, i+1)
        s = (d1 + d2 + d12) / 2
        triangle_area = s * (s - d1) * (s - d2) * (s - d12)

        if triangle_area > 0:
            triangle_area = math.sqrt(triangle_area)
        else:
            triangle_area = 0

        # Determine sign using cross product of vectors
        # Vector from origin to i
        v1_lat = lat1 - points[0][0]
        v1_lng = lng1 - points[0][1]
        # Vector from origin to i+1
        v2_lat = lat2 - points[0][0]
        v2_lng = lng2 - points[0][1]

        cross = v1_lat * v2_lng - v1_lng * v2_lat
        if cross < 0:
            triangle_area = -triangle_area

        area_sq_meters += triangle_area

    area_sq_meters = abs(area_sq_meters)

    # Convert to 亩: 1 亩 = 666.67 平方米
    MU_PER_SQ_METER = 1 / 666.67
    area_mu = area_sq_meters * MU_PER_SQ_METER

    return round(area_mu, 2)
