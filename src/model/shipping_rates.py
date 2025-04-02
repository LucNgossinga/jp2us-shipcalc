EMS_ZONES = {
    "First Zone": "China, South Korea, Taiwan",
    "Second Zone": "Asia (excluding China, South Korea, Taiwan)",
    "Third Zone": "Oceania, Canada, Mexico, Middle East, Europe",
    "Fourth Zone": "U.S. (including Guam and other U.S. territories)",
    "Fifth Zone": "Central and South America (excluding Mexico), Africa",
}

EMS_RATE_TABLE = {
    500:   [1450, 1900, 3150, 3900, 3600],
    600:   [1600, 2150, 3400, 4180, 3900],
    700:   [1750, 2400, 3650, 4460, 4200],
    800:   [1900, 2650, 3900, 4740, 4500],
    900:   [2050, 2900, 4150, 5020, 4800],
    1000:  [2200, 3150, 4400, 5300, 5100],
    1250:  [2500, 3500, 5000, 5990, 5850],
    1500:  [2800, 3850, 5550, 6600, 6600],
    1750:  [3100, 4200, 6150, 7290, 7350],
    2000:  [3400, 4550, 6700, 7900, 8100],
    2500:  [3900, 5150, 7750, 9100, 9600],
    3000:  [4400, 5750, 8800, 10300, 11100],
    3500:  [4900, 6350, 9850, 11500, 12600],
    4000:  [5400, 6950, 10900, 12700, 14100],
    4500:  [5900, 7550, 11950, 13900, 15600],
    5000:  [6400, 8150, 13000, 15100, 17100],
    5500:  [6900, 8750, 14050, 16300, 18600],
    6000:  [7400, 9350, 15100, 17500, 20100],
    7000:  [8200, 10350, 17200, 19900, 22500],
    8000:  [9000, 11350, 19300, 22300, 24900],
    9000:  [9800, 12350, 21400, 24700, 27300],
    10000: [10600, 13350, 23500, 27100, 29700],
}

ZONE_INDEX = {
    "First Zone": 0,
    "Second Zone": 1,
    "Third Zone": 2,
    "Fourth Zone": 3,  # default: US
    "Fifth Zone": 4,
}


def get_ems_shipping_cost(weight_grams: int, zone_name: str) -> int:
    """
    Given total weight (grams) and destination zone name,
    return shipping cost based on EMS rate table.
    """
    zone_idx = ZONE_INDEX.get(zone_name, 3)  # default to US
    weight_keys = sorted(EMS_RATE_TABLE.keys())

    for w in weight_keys:
        if weight_grams <= w:
            return EMS_RATE_TABLE[w][zone_idx]

    # If weight > max, just return last known cost
    return EMS_RATE_TABLE[weight_keys[-1]][zone_idx]
