import json

class RecipeGetter:
    """
    Returns recipe requirements and Malmo commands based on JSON file created by parse_recipes.py.
    """

    def __init__(self, input_json):
        with open(input_json) as openfile:
            self.recipe_dict = json.load(openfile)

    def get_ingredients(self, item_id):
        """Returns dict representing the ingredients"""

        if item_id not in self.recipe_dict:
            print('Item "' + item_id + '" not found.')
            return None
        else:
            return self.recipe_dict[item_id]['ingredients']

    def get_command(self, item_id):
        """Returns command string for given item"""

        # TODO: handle items with metadata?
        command = 'craft ' + item_id
        print(command)
        return command

def main():
    """Testing code"""
    recipes = RecipeGetter('recipes.json')

    recipes.get_ingredients('obsidian_pickaxe')
    diamond_pick_reqs = recipes.get_ingredients('diamond_pickaxe')
    print(diamond_pick_reqs)
    recipes.get_command('diamond_pickaxe')


if __name__ == '__main__':
    main()
