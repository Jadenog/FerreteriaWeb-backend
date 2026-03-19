def order_schema(order) -> dict:
    return {
        "id": str(order["_id"]),
        "id_user": order["id_user"],
        "id_product": order["id_product"],
        "date": order["date"],
        "total": order["total"]
    }

def orders_schema(orders) -> list:
    return [order_schema(order) for order in orders]    
    