# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Volume-ID bookkeeping (pure Python)
# Returns and prints absorbing volume IDs as explicit Python sets
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
ABS_ORDER = [
    "ASD3DBGrp", "ASD3DLGrp", "ASD3DRGrp", "ASD3DFGrp", "ASD3DKGrp",
    "ASD3DBLGrp", "ASD3DBRGrp", "ASD3DBFGrp", "ASD3DBKGrp",
    "ASD3DLFGrp", "ASD3DLKGrp", "ASD3DRFGrp", "ASD3DRKGrp",
    "ASD3DBLFGrp", "ASD3DBLKGrp", "ASD3DBRFGrp", "ASD3DBRKGrp",
]


def _abc_counts(nx: int, ny: int, nz: int, abs_layers: int = 1) -> dict[str, int]:
    base = {
        # faces
        "ASD3DBGrp": nx * ny,
        "ASD3DLGrp": ny * nz,
        "ASD3DRGrp": ny * nz,
        "ASD3DFGrp": nx * nz,
        "ASD3DKGrp": nx * nz,
        # edges
        "ASD3DBLGrp": ny,
        "ASD3DBRGrp": ny,
        "ASD3DBFGrp": nx,
        "ASD3DBKGrp": nx,
        "ASD3DLFGrp": nz,
        "ASD3DLKGrp": nz,
        "ASD3DRFGrp": nz,
        "ASD3DRKGrp": nz,
        # corners
        "ASD3DBLFGrp": 1,
        "ASD3DBLKGrp": 1,
        "ASD3DBRFGrp": 1,
        "ASD3DBRKGrp": 1,
    }
    return {k: v * abs_layers for k, v in base.items()}


def get_absorbing_volume_id_set_ranges(nx: int, ny: int, nz: int, abs_layers: int = 1):
    """
    Returns:
      soil_n: number of soil volumes
      ranges: dict[str, tuple[int,int]] mapping combo -> (start, stop_exclusive)
              so the set is: set(range(start, stop_exclusive))
    """
    if nx <= 0 or ny <= 0 or nz <= 0 or abs_layers <= 0:
        raise ValueError("nx, ny, nz, abs_layers must be positive integers")

    soil_n = nx * ny * nz
    counts = _abc_counts(nx, ny, nz, abs_layers)

    cur = soil_n + 1
    ranges: dict[str, tuple[int, int]] = {}
    for key in ABS_ORDER:
        n = counts[key]
        ranges[key] = (cur, cur + n)  # stop is exclusive
        cur += n

    return soil_n, ranges


def emit_absorbing_id_definitions(nx: int, ny: int, nz: int, abs_layers: int = 1) -> str:
    """
    Produces a paste-ready block like:
      B = set(range(101, 126))
      L = set(range(126, 146))
      ...
    """
    soil_n, ranges = get_absorbing_volume_id_set_ranges(nx, ny, nz, abs_layers)

    lines = []
    lines.append(f"# soil volumes: set(range(1, {soil_n + 1}))")
    for key in ABS_ORDER:
        a, b = ranges[key]
        lines.append(f"{key} = set(range({a}, {b}))")
        # alternatively (equivalent):
        # lines.append(f"{key} = {{i for i in range({a}, {b})}}")
    return "\n".join(lines)


# Example (your case)
if __name__ == "__main__":
    print(emit_absorbing_id_definitions(nx=5, ny=5, nz=4, abs_layers=1))

print(set(range(244, 245)))
