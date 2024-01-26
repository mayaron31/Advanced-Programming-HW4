from item import Item
import errors as errors_module


class ShoppingCart:

    def __init__(self) -> None:
        """
        hold itemList
        """
        self.itemList = []



    def add_item(self, item: Item):
        """
        adds the given item to the shopping cart.

        Args:
            item: an instance of Item.
        Exceptions:
            if the item name already exists in the shopping cart, raises ItemAlreadyExistsError.
        """
        for _item in self.itemList:
            if _item.name == item.name:
                raise errors_module.ItemAlreadyExistsError
        self.itemList.append(item) # adds item to shopping cart if needed

  
    def remove_item(self, item_name: str):
        """
        Removes the item with the given name from the shopping cart

        Args:
            item_name(str): represents the attribute name of an Item.
        Exceptions:
            if no item with the given name exists, raises ItemNotExistError.
        """
        for index, item in enumerate(self.itemList): #iterate over pairs of indexes and items 
            if item.name == item_name: #check if item name is identical to what we want to remove
                self.itemList.pop(index)
                return #breaks the loop after finding the item to remove

        raise errors_module.ItemNotExistError


    
    def get_subtotal(self) -> int:
        """
        Returns the subtotal price of all the items currently in the shopping cart.
        """
        subtotal = 0 # var that holds subtotal
        for item in self.itemList:
            subtotal+= item.price
        return subtotal

     
    def in_cart(self, item_name: str) -> bool:
        """
        Returns True if an item is in the cart
        
        Args:
            item_name (str): name of the item
        Returns:
            bool: True if an item is in the cart
        """
        for item in self.itemList:
            if item.name == item_name:
                return True
        
        return False
