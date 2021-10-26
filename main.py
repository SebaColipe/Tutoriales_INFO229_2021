from fastapi import FastAPI

#o	GET /v1/news?from=2021-01-01&to=2021-01-31&category=sport
app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/")
async def root():
    return {"menssage":"Hello Wordl"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
@app.get("/v1/{item_id}")
async def read_item(item_id: int):
    return {"item_id":item_id+1}
