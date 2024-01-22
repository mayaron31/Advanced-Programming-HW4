from item import Item


class ShoppingCart:
    """
    hold itemList
    """
    def __init__(self) -> None:
        self.itemList = []


    """
    adds the given item to the shopping cart.

    Parameters:
    the current instance of ShoppingCart
    an instance of Item.
    Exceptions:
    if the item name already exists in the shopping cart, raises ItemAlreadyExistsError.
    """
    def add_item(self, item: Item):
        if item in self.itemList:
            raise error.ItemAlreadyExistsError
        self.itemList.append(item) # adds item to shopping cart if needed

    """
    Removes the item with the given name from the shopping cart

    Parameters:
    the current instance of ShoppingCart
    an instance of str.
    Exceptions:
    if no item with the given name exists, raises ItemNotExistError.
    """
    def remove_item(self, item_name: str):
        for index, item in enumerate(self.itemList): #iterate over pairs of indexes and items 
            if item.name == item_name: #check if item name is identical to what we want to remove
                del self.itemList[index]
                return #breaks the loop after finding the item to remove

        raise errors.ItemNotExistError


    """
    Returns the subtotal price of all the items currently in the shopping cart.
    """
    def get_subtotal(self) -> int:
        subtotal = 0 # var that holds subtotal
        for item in self.itemList:
            subtotal+= item.price
        return subtotal

