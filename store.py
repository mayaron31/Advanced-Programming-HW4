import yaml

from item import Item
from shopping_cart import ShoppingCart

import errors as errors_module

class Store:
    """
    Consturctor which takes a path to an items file and loads it into the items field of the class
    """
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart() 

    """
    transforms raw item data into item objects
    Arguments:
    item_raw (List): raw item data in a list of dictionaries
    Returns:
    List: list of item objects
    """
    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    """
    returns current list of items
    Return:
    List: a list of items
    """
    def get_items(self) -> list:
        return self._items

    """
    Searches for item in list
    Arguments:
    item_name (str): instance of str to search for
    Returns:
    List: a sorted list of all the items that match the search term.
    The items in the returned list must contain the given phrase and not exactly match it.
    For example, when searching for "soap", items such as "dish soap" and "body soap" should be returned.
    """
    def search_by_name(self, item_name: str) -> list:
        fitting_items = [] # initialize a list which will contain the fitting items that will be returned
        for item in self._items:
            if item_name in item.name:
                fitting_items.append(item)

        return sorted(fitting_items, key=lambda item: item.name) # return the fitting items list sorted , by their names  #TODO: learn fuzzy matching    

  
    """
    Searches items by their hashtags
    Arguments: 
    hashtag (str): the current instance of Store and an instance of str.
    Returns:
    List: a sorted list of all the items matching the search criterion. 
    The items in the returned list must have the given hashtag in their hashtag list. 
    For example, when searching for the hashtag "paper", items with hashtags such as "tissue paper" must not be returned."""
    def search_by_hashtag(self, hashtag: str) -> list:
        fitting_items = [] # initialize a list which will contain the fitting items that will be returned
        for item in self._items:
            if hashtag in item.hashtags:
                fitting_items.append(item) # add the hashtag to the fitting items

        return sorted(fitting_items, key=lambda item: item.name) # return the fitting items list sorted , by their names      

    """
    Adds an item with the given name to the customer’s shopping cart.
    Arguments: the current instance of Store and an instance of str.
    Exceptions: if no such item exists, raises ItemNotExistError. If there are multiple items matching the given name, raises TooManyMatchesError. If the given item is already in the shopping cart, raises ItemAlreadyExistsError.
    To ease the search for the customers, not the whole item’s name must be given, but rather a distinct substring. For example, when adding "soap" to the cart, if an item such as "body soap" exists, and no other item with the substring "soap" in its name, "body soap" should be added to the list.
    You may assume that no two items exist such that one's name is a substring of the other.
    """
    def add_item(self, item_name: str):
        for item in self._items:
            if item_name == item.name:
                self._shopping_cart.add_item(item)
                return
        raise errors_module.ItemNotExistError

        

    """
    Removes an item with the given name from the customer’s shopping cart.
    Arguments: the current instance of Store and an instance of str.#TODO: לכתוב כמו את השאר
    Exceptions: if no such item exists, raises ItemNotExistError. If there are multiple items matching the given name, raises TooManyMatchesError.
    In a similar fashion to add_item, here too, not the whole item’s name must be given for it to be removed.
    """
    def remove_item(self, item_name: str):
        self._shopping_cart.remove_item(item_name)
    """
    checkout(self) – Returns the total price of all the items in the costumer’s shopping cart.
    """
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
