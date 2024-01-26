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


    """"""
    def _sorted_items(self, items:list[Item]) -> list:
        items_from_shopping_cart = self._shopping_cart.itemList
        tags_from_shopping_cart = [hashtag for item in items_from_shopping_cart for hashtag in item.hashtags]#flattend list of all hashtags in items from shopping cart

        item_tags_amount = [] # list of (item, count_of_common_tags)

        for item in items:
            count = 0
            for hashtag in item.hashtags:
                for tag_from_shopping_cart in tags_from_shopping_cart:
                    if hashtag == tag_from_shopping_cart:
                        count += 1
            
            item_tags_amount.append((item, count))
        
        return [item[0] for item in sorted(item_tags_amount, key=lambda x: (x[1],x[0].name))]
        


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
        fitting_items = [item for item in self._items if item_name in item.name and not self._shopping_cart.in_cart(item.name)] # create a list containing items that their name contains the item_name that we have searched for
        return self._sorted_items(fitting_items) # return the fitting items list sorted as the assignment declares

  
    """
    Searches items by their hashtags
    Arguments: 
    hashtag (str): the current instance of Store and an instance of str.
    Returns:
    List: a sorted list of all the items matching the search criterion. 
    The items in the returned list must have the given hashtag in their hashtag list. 
    For example, when searching for the hashtag "paper", items with hashtags such as "tissue paper" must not be returned."""
    def search_by_hashtag(self, hashtag: str) -> list:
        fitting_items = [item for item in self._items if hashtag in item.hashtags and not self._shopping_cart.in_cart(item.name)] # create a list containing items that their hashtags contains the hashtag that we have searched for
        return self._sorted_items(fitting_items) # return the fitting items list sorted as the assignment declares       

    """
    Adds an item with the given name to the customer’s shopping cart.
    Arguments: the current instance of Store and an instance of str.
    Exceptions: if no such item exists, raises ItemNotExistError. If there are multiple items matching the given name, raises TooManyMatchesError. If the given item is already in the shopping cart, raises ItemAlreadyExistsError.
    To ease the search for the customers, not the whole item’s name must be given, but rather a distinct substring. For example, when adding "soap" to the cart, if an item such as "body soap" exists, and no other item with the substring "soap" in its name, "body soap" should be added to the list.
    You may assume that no two items exist such that one's name is a substring of the other.
    """
    def add_item(self, item_name: str):
        fitting_items = self.search_by_name(item_name) # search for items with matching name in store
        if fitting_items:
            if len(fitting_items) > 1: # more than 1 in store
                raise errors_module.TooManyMatchesError
            else:
                
                self._shopping_cart.add_item(fitting_items[0]) # add item to shopping cart
        else:
            raise errors_module.ItemNotExistError 
        

    """
    Removes an item with the given name from the customer’s shopping cart.
    Arguments: the current instance of Store and an instance of str.#TODO: לכתוב כמו את השאר
    Exceptions: if no such item exists, raises ItemNotExistError. If there are multiple items matching the given name, raises TooManyMatchesError.
    In a similar fashion to add_item, here too, not the whole item’s name must be given for it to be removed.
    """
    def remove_item(self, item_name: str):
        fitting_items_in_cart:list[Item] = [item for item in self._shopping_cart.itemList if item_name in item.name] # create a list of matching items in the cart

        if fitting_items_in_cart:
            if len(fitting_items_in_cart) > 1: # more than 1 in store
                raise errors_module.TooManyMatchesError
            else:
                self._shopping_cart.remove_item(fitting_items_in_cart[0].name) # remove item from shopping cart
        else:
            raise errors_module.ItemNotExistError 
    """
    checkout(self) – Returns the total price of all the items in the costumer’s shopping cart.
    """
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
    