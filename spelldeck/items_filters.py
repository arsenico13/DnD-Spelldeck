def _normalize_filter_values(values):
    return {value.lower() for value in values} if values is not None else None


def filter_items(items, names=None, classes=None):
    names = _normalize_filter_values(names)
    classes = _normalize_filter_values(classes)

    return [
        (name, item)
        for name, item in sorted(items.items(), key=lambda entry: entry[0])
        if (names is None or name.lower() in names)
        and (
            classes is None
            or classes & {value.lower() for value in item.get("classes", [])}
        )
    ]

