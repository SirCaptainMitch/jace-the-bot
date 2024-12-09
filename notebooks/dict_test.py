from pprint import pprint

column_mapping = dict.fromkeys([
    'Metadata', 'EQUIP_KEY', 'EQUIP_UNIT_NBR', '0001', '0002', 'ABCD', 'ABCD_E', 'A015', 'A015_A_K'
])

element_definitions = {
    "Metadata": "Metadata"
    , "EQUIP_KEY": "equip_key"
    , "EQUIP_UNIT_NBR": "equip_unit"
    , "0001": "equipment_initial"
    , "0002":" equipment_group"
    , "ABCD": "operational_id"
    , "A015": "some_kind_of_brake"
}

merged_mapping = column_mapping.copy() | element_definitions.copy()

data = merged_mapping.copy()

# Update the dictionary with a comprehension
updated_data = {
    key: (
        f"{data[key[:4]]}{key[4:]}"
        if value is None and key[:4] in data and data[key[:4]] is not None
        else value
    )
    for key, value in data.items()
}

pprint(updated_data)
