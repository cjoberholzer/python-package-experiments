# import requests
#
# server_url = "http://127.0.0.1:8000/"
#
# # Retrieve index
# index_url = server_url
# # print(requests.get(url=index_url).json())
#
#
# # Retrieve item with id 0
# product_url = server_url + "items/"
# # print(requests.get(url=product_url + "0").json())
#
#
# # Product that doesn't exist
# # print(requests.get(url=product_url + "100").json())
#
# """Fast API handles the validation for you.
#
# The endpoint "query_item_by_id(item_id: int)" expects an integer for the item ID. If an integer isn't provided
# the validation is handled automatically. This is done by FastAPI and Pydantic's type system."""
# # print(requests.get(url=server_url + "items/adas").json())
#
#
# # Query items by parameters
# # parameters_url = product_url
# # print(parameters_url)
# # query_url = "http://127.0.0.1:8000/" + "items/" + "?count=100"
# # print(query_url)
# # print(requests.get(url=query_url).json())
#
#
# print("adding item:")
# creation_url = server_url
# print(requests.post(url=creation_url, json={"id": 3, "name": "test", "category": "tools",
#                                             "price": 9.99, "count": 100}).json())
# print(requests.get(url=server_url).json())
#
#
# print("Updating item:")
# print(requests.put(url=server_url + "items/3?count=122").json())
# print(requests.put(url=server_url + "items/3?name=asd").json())
#
# print("Deleting item:")
# print(requests.delete(url=server_url + "items/3").json())
# print(requests.get(url=server_url).json())