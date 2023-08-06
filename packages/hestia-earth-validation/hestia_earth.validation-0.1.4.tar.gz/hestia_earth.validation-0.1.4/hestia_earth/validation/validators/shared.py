from typing import List
from functools import reduce
from dateutil.parser import parse
import re
from hestia_earth.schema import NodeType

from .data.lookups import import_lookup_table, get_table_value


def validate_dates(node: dict):
    start = node.get('startDate')
    end = node.get('endDate')
    return start is None or end is None or (len(start) <= 7 and len(end) <= 7 and end >= start) or end > start


def validate_list_dates(node: dict, prop: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return validate_dates(value) or {
            'level': 'error',
            'dataPath': f".{prop}[{index}].endDate",
            'message': 'must be greater than startDate'
        }

    results = list(map(validate, enumerate(node.get(prop, []))))
    return next((x for x in results if x is not True), True)


def validate_list_min_max(node: dict, prop: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return value.get('min', 0) <= value.get('max', 0) or {
            'level': 'error',
            'dataPath': f".{prop}[{index}].max",
            'message': 'must be greater than min'
        }

    results = list(map(validate, enumerate(node.get(prop, []))))
    return next((x for x in results if x is not True), True)


def same_properties(value: dict, props: List[str]):
    def identical(test: dict):
        same_values = list(filter(lambda prop: get_dict_key(value, prop) == get_dict_key(test, prop), props))
        return test if len(same_values) == len(props) else None
    return identical


def validate_list_duplicated(node: dict, prop: str, props: List[str]):
    def validate(values):
        value = values[1]
        index = values[0]
        values = node[prop].copy()
        values.pop(index)
        duplicates = list(filter(same_properties(value, props), values))
        return len(duplicates) == 0 or {
            'level': 'error',
            'dataPath': f".{prop}[{index}]",
            'message': f"Duplicates found. Please make sure there is only one entry with the same {', '.join(props)}"
        }

    results = list(map(validate, enumerate(node.get(prop, []))))
    return next((x for x in results if x is not True), True)


def diff_in_days(from_date: str, to_date: str):
    difference = parse(to_date) - parse(from_date)
    return round(difference.days + difference.seconds/86400, 1)


def diff_in_years(from_date: str, to_date: str):
    return round(diff_in_days(from_date, to_date)/365.2425, 1)


def list_has_props(values: List[dict], props: List[str]):
    return filter(lambda x: all(prop in x for prop in props), values)


def get_dict_key(value: dict, key: str):
    keys = key.split('.')
    return reduce(lambda x, y: x if x is None else x.get(y), keys, value)


def is_term(node: dict):
    return isinstance(node, dict) and node.get('type', node.get('@type')) == NodeType.TERM.value


def has_terms_list(value):
    return isinstance(value, list) and all(is_term(x) for x in value)


def validate_node_children_termType(node: dict):
    lookups = import_lookup_table('property-to-termType.csv')
    node_type = node.get('type', node.get('@type'))

    def validate_dict(key: str, term: dict):
        term_type = term.get('termType')
        values = get_table_value(lookups, 'schemaproperty', '.'.join([node_type, key]), 'termtype')
        values = values[0].split(';') if values else None
        return term_type in values or {
            'level': 'error',
            'dataPath': f".{key}.termType",
            'message': 'invalid termType',
            'params': {
                'termType': values
            }
        } if values and term_type else True

    def validate_list(key: str):
        def validate_list_item(values):
            term = values[1]
            index = values[0]
            validation = validate_dict(key, term)
            return True if validation is True else {
                **validation,
                'dataPath': f".{key}[{index}].termType"
            }

        return list(map(validate_list_item, enumerate(node.get(key, []))))

    # only check those who are Term
    dict_keys = list(filter(lambda key: is_term(node.get(key)), node.keys()))
    list_keys = list(filter(lambda key: has_terms_list(node.get(key)), node.keys()))
    return list(map(lambda key: validate_dict(key, node.get(key, {})), dict_keys)) + \
        list(reduce(lambda x, y: x + validate_list(y), list_keys, []))


def validate_region(node: dict):
    country = node.get('country', {})
    region_id = node.get('region', {}).get('@id', '')
    return region_id[0:8] == country.get('@id') or {
        'level': 'error',
        'dataPath': '.region',
        'message': 'must be within the country',
        'params': {
            'country': country.get('name')
        }
    }


def validate_country(node: dict):
    country_id = node.get('country', {}).get('@id', '')
    return bool(re.search(r'GADM-[A-Z]{3}', country_id)) or {
        'level': 'error',
        'dataPath': '.country',
        'message': 'must be a country'
    }
