from collections import defaultdict
from datetime import datetime
from itertools import chain

from .items import (
    get_collection,
    get_item,
    get_item_by_code,
    items_for_collection,
    parse_data,
)
from .models import Settings
from .sheet_transform import get_col_item_needs, get_no_hide_collections, get_rows


def get_important(rows):
    imp_items = defaultdict(set)

    for col_name, items in get_col_item_needs(rows).items():
        for item_name in items:
            of_import = not item_name.startswith('!')
            item_name = item_name.strip('!')
            item = get_item(item_name, col_name)
            print(f'{col_name:>30} - {item_name:>30} --> {item.name}')
            imp_items[of_import].add(item)

    return imp_items[True], imp_items[False]


def remove_no_hide_cols(unimportant, rows):
    no_hide_col_names = get_no_hide_collections(rows)
    no_hide_cols = [get_collection(name) for name in no_hide_col_names]

    return {it for it in unimportant if it.collection not in no_hide_cols}


def get_weekly_items(items):
    weekly_items = items_for_collection('Weekly', items)
    return {get_item_by_code(item.code, items) for item in weekly_items}

def get_settings(sheet_names=None):
    sheet_names = sheet_names or (None,)

    _, items = parse_data()

    sheet_rows = []
    for sheet_name in sheet_names:
        sheet_conf = {'sheet_name': sheet_name} if sheet_name else {}
        rows = get_rows(**sheet_conf)
        sheet_rows.append(rows)

    importants, unimportants = zip(*[get_important(rows) for rows in sheet_rows])
    important = merge_sets(importants)
    unimportant = merge_sets(unimportants)

    # always mark weekly items as important
    important |= get_weekly_items(items)

    unimportant |= items - important

    unimportants = zip(*[remove_no_hide_cols(unimportant, rows) for rows in sheet_rows])
    unimportant = merge_sets(unimportants)

    return Settings(important_items=important, unimportant_items=unimportant)


def merge_sets(sets):
    return set(chain(*sets))


def get_export_filename():
    now = datetime.now()
    return now.strftime('%Y-%m-%d_%H-%M-%S.json')


def write_export(export_path):
    path = export_path / get_export_filename()

    s = get_settings()
    path.write_text(s.as_json())

    print(f'export written to {path}')
