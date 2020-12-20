import json
import math

class RecipeGetter:
    """
    Returns recipe requirements and Malmo commands based on JSON file created by parse_recipes.py.
    """

    def __init__(self, input_json):
        with open(input_json) as openfile:
            self.recipe_dict = json.load(openfile)

    def _ingredients_helper(self, item_id, count):
        """Recursively breaks recipe into raw materials"""

        if item_id not in self.recipe_dict:
            print('Item "' + item_id + '" not found.')
            return None

        ingredients = {}
        output_multiplier = count / self.recipe_dict[item_id]['count']
        commands = ['craft ' + item_id] * math.ceil(output_multiplier)

        # recursively break down ingredients
        for sub_item, data in self.recipe_dict[item_id]['ingredients'].items():
            sub_count = data['count']

            if sub_item in self.recipe_dict:
                sub_recipe, sub_commands = self._ingredients_helper(sub_item, sub_count)
                commands.extend(sub_commands)
                self._add_to_dict(ingredients, sub_recipe)

            else:
                self._add_to_dict(ingredients, {sub_item: sub_count})

        for key in ingredients:
            ingredients[key] *= output_multiplier

        return ingredients, commands

    def get_ingredients(self, item_id, count=1):
        """Returns dict of raw materials and list of crafting commands for Malmo"""

        ingredients, commands = self._ingredients_helper(item_id, count)
        commands.reverse()
        for ingredient in ingredients:
            ingredients[ingredient] = math.ceil(ingredients[ingredient])

        return ingredients, commands

    @staticmethod
    def _add_to_dict(dest, source):
        """Updates dest dict with source dict"""
        for key in source:
            if key in dest:
                dest[key] += source[key]
            else:
                dest[key] = source[key]


def main():
    """Testing code"""
    recipes = RecipeGetter('recipes.json')

    test_recipe(recipes, 'repeater')
    test_recipe(recipes, 'redstone_torch')
    test_recipe(recipes, 'comparator')
    test_recipe(recipes, 'brewing_stand')
    test_recipe(recipes, 'anvil')


def test_recipe(recipes, item_id):
    print(item_id)
    ingredients, commands = recipes.get_ingredients(item_id)
    print('  ' + str(ingredients))
    print('  ' + str(commands) + '\n')


if __name__ == '__main__':
    main()
