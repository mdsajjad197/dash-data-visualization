from app import app


def find_component_by_id(component, component_id):
    if getattr(component, "id", None) == component_id:
        return component

    children = getattr(component, "children", None)
    if children is None:
        return None

    if not isinstance(children, list):
        children = [children]

    for child in children:
        found = find_component_by_id(child, component_id)
        if found is not None:
            return found

    return None


def test_header_present():
    header = find_component_by_id(app.layout, "header")

    assert header is not None
    assert header.children == "Soul Foods Pink Morsel Sales Dashboard"


def test_graph_present():
    graph = find_component_by_id(app.layout, "sales-chart")

    assert graph is not None


def test_region_picker_present():
    radio = find_component_by_id(app.layout, "region-filter")

    assert radio is not None
