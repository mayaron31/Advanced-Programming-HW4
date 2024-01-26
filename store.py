import yaml

from item import Item
from shopping_cart import ShoppingCart

import errors as errors_module

class Store:
    def __init__(self, path):
        """
        Initialize the object with the provided path to the inventory file.

        Args:
            path (str): The path to the inventory file.

        Returns:
            None
        """
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items'] # load items from inventory file
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart() 


    """"""
    def _sorted_items(self, items:list[Item]) -> list:
        """
        Sorts a list of items based on the number of common hashtags with items in the shopping cart.

        Args:
        items (list[Item]): A list of Item objects to be sorted.

        Returns:
        list: A sorted list of items. The sorting is based on the number of common hashtags with items in the shopping cart, in descending order. If two items have the same number of common hashtags, they are sorted in lexicographic order based on their names.

        """
        items_from_shopping_cart = self._shopping_cart.itemList
        tags_from_shopping_cart = [hashtag for item in items_from_shopping_cart for hashtag in item.hashtags]#flattend list of all hashtags in items from shopping cart

        # the next line will create a list of tuples in the form of (item, count_of_common_tags)
        item_tags_amount = [(item, #first index of the tuple is item
                              sum(1 for hashtag in item.hashtags #second index of the tuple is count of common tags. for every hastag in item's list of hastags
                                       for tag_from_shopping_cart in tags_from_shopping_cart # for every hastag in shopping cart
                                         if hashtag == tag_from_shopping_cart)) # if the two hastags are the same, increase the count by 1
                                           for item in items] #for every item in the list of fitting items from the search

        return [item[0] for item in sorted(item_tags_amount, key=lambda x: (-x[1],x[0].name))] # the minus sign is to reverse only the tags amount, but left the lexo order the same
        

    @staticmethod
    def _convert_to_item_objects(items_raw):
        """
        Convert the given list of raw item data into a list of Item objects.

        Args:
            items_raw (list): A list of raw item data, where each item is a dictionary
                containing the keys 'name', 'price', 'hashtags', and 'description'.

        Returns:
            list: A list of Item objects created from the raw item data.
        """
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        """
        Return the list of items.
        """
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """
        Searches for item in list
        Args:
            item_name (str): instance of str to search for
        Returns:
            List: a sorted list of all the items that match the search term.
            The items in the returned list must contain the given phrase and not exactly match it.
            For example, when searching for "soap", items such as "dish soap" and "body soap" should be returned.
        """

        fitting_items = [item for item in self._items if item_name in item.name and not self._shopping_cart.in_cart(item.name)] # create a list containing items that their name contains the item_name that we have searched for
        return self._sorted_items(fitting_items) # return the fitting items list sorted as the assignment declares

  
    def search_by_hashtag(self, hashtag: str) -> list:
        """
        Search for items by hashtag.

        Args:
            hashtag (str): The hashtag to search for.
        
        Returns:
            list: A list of fitting items sorted by some criteria.
        """
        fitting_items = [item for item in self._items if hashtag in item.hashtags and not self._shopping_cart.in_cart(item.name)] # create a list containing items that their hashtags contains the hashtag that we have searched for
        return self._sorted_items(fitting_items) # return the fitting items list sorted as the assignment declares       


    def add_item(self, item_name: str):
        """
        Add an item to the shopping cart if it exists in the store and is not already in the cart.

        Args:
            item_name (str): The name of the item to be added.

        Raises:
            TooManyMatchesError: If there are multiple matching items in the store.
            ItemAlreadyExistsError: If the item is already in the shopping cart.
            ItemNotExistError: If the item does not exist in the store.
        """
        fitting_items = [item for item in self._items if item_name in item.name] # search for items with matching name in store BUT not using the search by name because it returns only items that are not in the shopping cart already
        if fitting_items:
            if len(fitting_items) > 1: # more than 1 in store
                raise errors_module.TooManyMatchesError
            else:
                if (self._shopping_cart.in_cart(fitting_items[0].name)):
                    raise errors_module.ItemAlreadyExistsError
                self._shopping_cart.add_item(fitting_items[0]) # add item to shopping cart
        else:
            raise errors_module.ItemNotExistError 
        
    def remove_item(self, item_name: str):
        """
        Removes the specified item from the shopping cart.

        Args:
            item_name (str): The name of the item to be removed from the shopping cart.

        Raises:
            TooManyMatchesError: If there are more than one matching items in the cart.
            ItemNotExistError: If the specified item does not exist in the shopping cart.
        """
        fitting_items_in_cart = [item for item in self._shopping_cart.itemList if item_name in item.name] # create a list of matching items in the cart

        if fitting_items_in_cart:
            if len(fitting_items_in_cart) > 1: # more than 1 in store
                raise errors_module.TooManyMatchesError
            else:
                self._shopping_cart.remove_item(fitting_items_in_cart[0].name) # remove item from shopping cart
        else:
            raise errors_module.ItemNotExistError 

    def checkout(self) -> int:
        """
        Return the subtotal of the shopping cart.

        Returns:
            int: The subtotal of the shopping cart.
        """
        return self._shopping_cart.get_subtotal()
    