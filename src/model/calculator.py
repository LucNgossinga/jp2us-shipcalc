def allocate_shipping_costs(items, total_cost: int, total_weight: int, base_weight: int = 500):
    """
    items: List[Item]
    total_cost: total shipping cost (Yen)
    total_weight: total weight of the shipment (grams)

    Returns: List of dicts with shipping allocation per item
    """
    total_price = sum(item.price for item in items)
    total_item_weight = sum(item.weight for item in items)

    base_cost = 0
    extra_cost = 0

    if total_weight > base_weight:
        base_cost = total_cost * (base_weight / total_weight)
        extra_cost = total_cost - base_cost
    else:
        base_cost = total_cost

    result = []
    for item in items:
        base_share = (item.price / total_price) * base_cost if total_price else 0
        extra_share = (item.weight / total_item_weight) * extra_cost if total_item_weight else 0
        result.append({
            "name": item.name,
            "weight": item.weight,
            "price": item.price,
            "base_share": round(base_share),
            "extra_share": round(extra_share),
            "total_shipping": round(base_share + extra_share),
            "final_total": round(item.price + base_share + extra_share)
        })
    return result
