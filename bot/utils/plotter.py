"""
Module for plotting cadastral polygons on a web map
using geopandas, shapely, contextily, and matplotlib.
"""

from typing import List, Tuple
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import contextily as ctx
import matplotlib.pyplot as plt


def plot_polygon(coords: List[List[Tuple[float, float]]], cadastral_number: str) -> str:
    """
    Plot one or more polygons defined by coordinates on a map with a basemap,
    save it as a PNG image file named after the cadastral number.

    Args:
        coords (list of list of tuple): List of polygons, 
        each a list of (longitude, latitude) pairs.
        cadastral_number (str): Identifier to use for the map title and filename.

    Returns:
        str: The filename of the saved PNG map image.
    """

    polygons = [Polygon(polygon_coords) for polygon_coords in coords]
    if len(polygons) == 1:
        geometry = polygons[0]
    else:
        geometry = MultiPolygon(polygons)

    gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[geometry])
    gdf = gdf.to_crs(epsg=3857)

    fig, ax = plt.subplots(figsize=(8, 8))
    gdf.boundary.plot(ax=ax, color="blue")
    gdf.plot(ax=ax, alpha=0.3, edgecolor="black")

    minx, miny, maxx, maxy = gdf.total_bounds
    padding_x = (maxx - minx) * 0.2
    padding_y = (maxy - miny) * 0.2

    ax.set_xlim(minx - padding_x, maxx + padding_x)
    ax.set_ylim(miny - padding_y, maxy + padding_y)

    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    ax.set_title(f"Участок {cadastral_number}")
    ax.set_xlabel("Долгота")
    ax.set_ylabel("Широта")

    map_file = f"{cadastral_number}_map.png"
    plt.savefig(map_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return map_file
