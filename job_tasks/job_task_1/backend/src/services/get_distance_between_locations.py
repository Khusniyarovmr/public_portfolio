from geopy.distance import geodesic as GD


def get_distance(cargo_loc: tuple[str, str], truck_loc: tuple[str, str]) -> GD.miles:
    return GD(cargo_loc, truck_loc).miles
