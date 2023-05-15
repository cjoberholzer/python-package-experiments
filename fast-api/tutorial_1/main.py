from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

# You can give yor api a title and add additional metadata such as a description, version, etc.
# Description supports markdown formatting
app = FastAPI(
    title="FastAPI Tutorial 1",
    description="This is a tutorial project for FastAPI.",
    version="0.0.1",
)


# Docstrings of classes will be reelected in the API documentation in the 'Schema' section.
class Category(Enum):
    """Category of an item"""
    TOOLS = "tools"
    CONSUMABLES = "consumables"


# You can add metadata to attributes using the field class.
# This information will also be shown in the auto-generated documentation.
class Item(BaseModel):
    """Representation of an item in the system."""
    id: int = Field(description="Unique identifier of the item.")
    name: str = Field(description="Name of the item.")
    category: Category = Field(description="Category of the item.")
    price: float = Field(description="Price of the item in USD.")
    count: int = Field(description="Number of items in stock.")


# This dictionary will be used as a database.
items = {
    0: Item(id=0, name="Hammers", category=Category.TOOLS, price=9.99, count=100),
    1: Item(id=1, name="Screwdrivers", category=Category.TOOLS, price=5.99, count=100),
    2: Item(id=2, name="Screws", category=Category.CONSUMABLES, price=0.49, count=1000),
}


# FastAPI handles JSON serialization and deserialization for us.
# We can simply use built-in python and Pydantic types, in this case dict[int, Item].
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with id({item_id}) does not exist."
        )
    return items[item_id]


# Function parameters that are not path parameters can be specified as query parameters in.
# Here we can query items li this: /items?count=20
Selection = dict[
    str, str | int | float | Category | None
]  # dictionary containing the query parameters


@app.get("/items/")
def query_item_by_parameters(
        name: str | None = None,
        category: Category | None = None,
        price: float | None = None,
        count: int | None = None,
) -> dict[str, list[Item] | Selection]:

    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category == category,
            )
        )
    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


@app.post("/")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        raise HTTPException(
            status_code=400, detail=f"Item with id({item.id}) already exists."
        )

    items[item.id] = item
    return {"added": item}


# If you want to add further limitations to the data your endpoints receive, you can add Path and Query parameters.
# In this case we are setting a lower bound for valid values and a minimal and maximal length for the name.
@app.put(
    "/items/{item_id}",
    responses={
        404: {"description": "Item with the specified id does not exist."},
        400: {"description": "No argument specified."},
    },
)
def update_item(
        item_id: int = Path(ge=0),
        name: str | None = Query(default=None, min_length=1, max_length=50),
        price: float | None = Query(dfault=None, gt=0.0),
        count: int | None = Query(default=None, ge=0),
) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with id({item_id}) does not exist."
        )
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400,
            detail="At least one of the following parameters must be specified: name, price, count.",
        )

    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with id({item_id}) does not exist."
        )

    item = items.pop(item_id)
    return {"deleted": item}
