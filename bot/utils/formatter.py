from typing import Any, List, Tuple


def format_cadastral_info(feat: Any) -> Tuple[str, List[Tuple[float, float]]]:
    """
    Extract and format cadastral information from a feature object.

    Args:
        feat: An object representing a cadastral feature with properties and geometry.
            Expected to have:
            - feat.properties.options: attributes with cadastral details.
            - feat.geometry.coordinates: a nested list of coordinate objects with
              longitude and latitude attributes.

    Returns:
        tuple:
            - info (str): Formatted multiline string with cadastral info.
            - coords (list of tuple): List of (longitude, latitude) coordinate tuples
              representing the polygon vertices if available, otherwise empty list.
    """
    props = feat.properties
    options = props.options

    feat_data = {
        "object_type": getattr(options, "land_record_type", "Неизвестно"),
        "address": getattr(options, "readable_address", "Неизвестен"),
        "area": (
            getattr(options, "specified_area", None)
            or getattr(options, "land_record_area", None)
            or "Неизвестна"
        ),
        "cost": getattr(options, "cost_value", "Не указана"),
        "land_category": getattr(options, "land_record_category_type", "Не указана"),
        "permitted_use": getattr(
            options, "permitted_use_established_by_document", "Не установлен"
        ),
        "coords": [],
    }

    geometry = getattr(feat, "geometry", None)
    if geometry and geometry.coordinates:
        if geometry.type == "MultiPolygon":
            coords: List[List[Tuple[float, float]]] = [
                [(pos.longitude, pos.latitude) for pos in polygon[0]]
                for polygon in geometry.coordinates
            ]
        elif geometry.type == "Polygon":
            coords: List[List[Tuple[float, float]]] = [
                [(pos.longitude, pos.latitude) for pos in geometry.coordinates[0]]
            ]
        else:
            coords = []
        feat_data["coords"] = coords
    else:
        coords = []

    cost = feat_data["cost"]
    formatted_cost = f"{cost:,}".replace(",", " ")

    info = (
        f"🏷 **Тип объекта:** {feat_data['object_type']}\n"
        f"📍 **Адрес:** {feat_data['address']}\n"
        f"📐 **Площадь:** {feat_data['area']} кв.м\n"
        f"💰 **Кадастровая стоимость:** {formatted_cost} ₽\n"
        f"🏞 **Категория земель:** {feat_data['land_category']}\n"
        f"📄 **Вид разрешенного использования:** {feat_data['permitted_use']}\n"
    )

    return info, coords
