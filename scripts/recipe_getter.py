import json
import math
import copy

class RecipeGetter:
    """
    Returns recipe requirements and Malmo commands based on JSON file created by parse_recipes.py.
    """

    def __init__(self, input_json):
        with open(input_json) as openfile:
            self.recipe_dict = json.load(openfile)

    def ingredients_helper(self, item_id):
        """Returns dict representing the ingredients and list of craft commands"""

        # TODO: recursively find recipes and handle intermediate crafting steps
        # TODO: return dict of raw ingredients, and list of crafting commands
        if item_id not in self.recipe_dict:
            print('Item "' + item_id + '" not found.')
            return None

        ingredients = copy.deepcopy(self.recipe_dict[item_id]['ingredients'])
        # output_count = self.recipe_dict[item_id]['count']
        commands = ['craft ' + item_id]

        # recursively break down ingredients
        for sub_item, data in self.recipe_dict[item_id]['ingredients'].items():
            sub_count = data['count']

            if sub_item in self.recipe_dict:
                sub_recipe, sub_commands = self.ingredients_helper(sub_item)
                factor = math.ceil(sub_count / self.recipe_dict[sub_item]['count'])

                sub_commands = sub_commands * factor
                commands.extend(sub_commands)

                for key in sub_recipe:
                    sub_recipe[key]['count'] *= factor

                # TODO: replace recipe with sub-ingredients and add intermediate crafting command
                del ingredients[sub_item]
                self.merge_dicts(ingredients, sub_recipe)

        # TODO
        # print(ingredients)
        return ingredients, commands

    def get_ingredients(self, item_id):
        ingredients, commands = self.ingredients_helper(item_id)
        commands.reverse()
        return ingredients, commands

    @staticmethod
    def merge_dicts(dest, source):
        """Updates dest dict merging in source dict"""
        for key in source:
            if key in dest:
                dest[key]['count'] += source[key]['count']
            else:
                dest[key] = {'count': source[key]['count']}
                if 'data' in source[key]:
                    dest[key]['data'] = source[key]['data']

    @staticmethod
    def ceil_to_multiple(x, base):
        """Round x up to nearest multiple of base"""
        return base * math.ceil(x / base)

    def get_command(self, item_id):
        """Returns command string for given item"""

        # TODO: merge with get_ingredients()
        command = 'craft ' + item_id
        return command

def main():
    """Testing code"""
    recipes = RecipeGetter('recipes.json')

    test_recipe(recipes, 'repeater')
    test_recipe(recipes, 'diamond_pickaxe')
    test_recipe(recipes, 'anvil')


def test_recipe(recipes, item_id):
    print(item_id)
    ingredients, commands = recipes.get_ingredients(item_id)
    print('  ' + str(ingredients))
    print('  ' + str(commands) + '\n')

if __name__ == '__main__':
    main()
