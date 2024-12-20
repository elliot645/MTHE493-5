# Adding decimal values each day 
# use this data for 2018, 2019, and 2020!!!!!!
import math
def add_immigrants_to_urns(data, days_in_year=365):
    urns = {}
    for county_id, immigrants in data.items():
        red_immigrants = immigrants['red']
        blue_immigrants = immigrants['blue']
        red_per_day = red_immigrants / days_in_year / 4
        blue_per_day = blue_immigrants / days_in_year / 4
        # we need to divide by 4 because this is over 4 years
        urns[county_id] = {
            'red_balls': 0,
            'blue_balls': 0
        }
        urns[county_id]['red_balls'] = red_per_day
        urns[county_id]['blue_balls'] = blue_per_day

    return urns

# This is people who moved from 2018-2022
# this data will be used for 2018, 2019, 2020
# right is county codes, and then # of movers from red/blue states
immigrants_data = {
    '001': {'red': 21, 'blue': 15},
    '003': {'red': 9, 'blue': 5},
    '005': {'red': 24, 'blue': 18},
    '007': {'red': 6, 'blue': 3},
    '009': {'red': 26, 'blue': 22},
    '011': {'red': 22, 'blue': 22},
    '013': {'red': 7, 'blue': 8},
    '015': {'red': 18, 'blue': 16},
    '017': {'red': 19, 'blue': 18},
    '019': {'red': 18, 'blue': 20},
    '021': {'red': 20, 'blue': 21},
    '023': {'red': 15, 'blue': 7},
    '027': {'red': 11, 'blue': 11},
    '029': {'red': 4, 'blue': 4},
    '031': {'red': 24, 'blue': 22},
    '033': {'red': 24, 'blue': 21},
    '035': {'red': 19, 'blue': 17},
    '037': {'red': 6, 'blue': 4},
    '039': {'red': 7, 'blue': 6},
    '041': {'red': 8, 'blue': 3},
    '043': {'red': 8, 'blue': 5},
    '045': {'red': 7, 'blue': 4},
    '047': {'red': 7, 'blue': 3},
    '049': {'red': 9, 'blue': 4},
    '051': {'red': 4, 'blue': 7},
    '053': {'red': 17, 'blue': 17},
    '055': {'red': 18, 'blue': 16},
    '057': {'red': 25, 'blue': 22},
    '059': {'red': 8, 'blue': 8},
    '061': {'red': 17, 'blue': 19},
    '063': {'red': 11, 'blue': 5},
    '065': {'red': 7, 'blue': 5},
    '067': {'red': 4, 'blue': 1},
    '069': {'red': 20, 'blue': 20},
    '071': {'red': 24, 'blue': 22},
    '073': {'red': 23, 'blue': 20},
    '075': {'red': 9, 'blue': 12},
    '077': {'red': 4, 'blue': 2},
    '079': {'red': 5, 'blue': 5},
    '081': {'red': 23, 'blue': 21},
    '083': {'red': 22, 'blue': 19},
    '085': {'red': 16, 'blue': 18},
    '086': {'red': 24, 'blue': 20},
    '087': {'red': 16, 'blue': 17},
    '089': {'red': 13, 'blue': 11},
    '091': {'red': 25, 'blue': 20},
    '093': {'red': 10, 'blue': 9},
    '095': {'red': 26, 'blue': 22},
    '097': {'red': 18, 'blue': 19},
    '099': {'red': 23, 'blue': 22},
    '101': {'red': 23, 'blue': 21},
    '103': {'red': 23, 'blue': 22},
    '105': {'red': 24, 'blue': 22},
    '107': {'red': 14, 'blue': 11},
    '109': {'red': 21, 'blue': 19},
    '111': {'red': 18, 'blue': 19},
    '113': {'red': 21, 'blue': 18},
    '115': {'red': 24, 'blue': 22},
    '117': {'red': 23, 'blue': 20},
    '119': {'red': 20, 'blue': 14},
    '121': {'red': 7, 'blue': 7},
    '123': {'red': 2, 'blue': 2},
    '125': {'red': 5, 'blue': 4},
    '127': {'red': 21, 'blue': 21},
    '129': {'red': 8, 'blue': 1},
    '131': {'red': 18, 'blue': 11},
    '133': {'red': 9, 'blue': 4},
}

urns = add_immigrants_to_urns(immigrants_data)
# for county_id in list(urns.keys())[:5]:
for county_id in list(urns.keys()):
    print(f"County {county_id}: {urns[county_id]}")
    # printing the county IDs