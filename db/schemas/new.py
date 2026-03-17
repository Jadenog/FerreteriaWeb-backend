def new_schema(new) -> dict:
    return {
        "id": str(new["_id"]),
        "title": new["title"],
        "description": new["description"],
        "image": new["image"],
        "active": new["active"],
        "date": new["date"]
    }


def news_schema(news) -> list:
    return [new_schema(new) for new in news]    
    