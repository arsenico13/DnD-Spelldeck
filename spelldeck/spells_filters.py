def _normalize_filter_values(values):
    return {value.lower() for value in values} if values is not None else None


def parse_levels(levels):
    parsed_levels = None

    if levels is not None:
        parsed_levels = set()

        for level_spec in levels:
            boundaries = level_spec.split("-")
            if len(boundaries) == 1:
                parsed_levels.add(int(boundaries[0]))
            elif len(boundaries) == 2:
                parsed_levels |= set(range(int(boundaries[0]), int(boundaries[1]) + 1))

    return parsed_levels


def filter_spells(spells, classes=None, levels=None, schools=None, names=None):
    classes = _normalize_filter_values(classes)
    schools = _normalize_filter_values(schools)
    names = _normalize_filter_values(names)

    return [
        (name, spell)
        for name, spell in sorted(spells.items(), key=lambda entry: entry[0])
        if (classes is None or classes & {value.lower() for value in spell["classes"]})
        and (schools is None or spell["school"].lower() in schools)
        and (levels is None or spell["level"] in levels)
        and (names is None or name.lower() in names)
    ]

