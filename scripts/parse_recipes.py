import os
import json
from collections import namedtuple

class RecipeParser:
    """
    Parse individual recipe JSON files into a single JSON file so they can be easily retrieved by other scripts.

    For simplicity, only the first choice gets added for recipes that accept different items
    (e.g. substituting coal with charcoal or using different types of wood)

    TODOS:
    * Add smelting recipes if possible (uses 1.13+ ID format, so would need converting)
    ** Can alternatively just hardcode them in
    * Remove non-1.11 recipes if necessary
    """

    def __init__(self, recipe_dir):
        self.recipe_dir = recipe_dir
        self.data_dict = dict()
        self.output_filename = 'recipes.json'

    def add_crafting_shaped(self, input_dict: dict):
        temp_dict = {}
        result_dict = input_dict['result']
        output_dict = {
            'count': 1,
            'ingredients': {}
        }

        for key, key_data in input_dict['key'].items():
            if isinstance(key_data, dict):
                item = key_data['item'].split(':')[1]
            elif isinstance(key_data, list):
                item = key_data[0]['item'].split(':')[1]

            temp_dict[key] = {
                'item': item,
                'count': 0
            }
            if 'data' in key_data:
                temp_dict[key]['data'] = key_data['data']

        for row in input_dict['pattern']:
            for char in row:
                if char != ' ':
                    temp_dict[char]['count'] += 1

        if 'data' in result_dict:
            output_dict['data'] = result_dict['data']
        if 'count' in result_dict:
            output_dict['count'] = result_dict['count']

        for key_data in temp_dict.values():
            output_dict['ingredients'][key_data['item']] = {
                'count': key_data['count']
            }

            if 'data' in key_data:
                output_dict['ingredients'][key_data['item']]['data'] = key_data['data']

        self.data_dict[result_dict['item']] = output_dict

    def add_crafting_shapeless(self, input_dict: dict):
        result_dict = input_dict['result']
        output_dict = {
            'count': 1,
            'ingredients': {}
        }

        if 'data' in result_dict:
            output_dict['data'] = result_dict['data']
        if 'count' in result_dict:
            output_dict['count'] = result_dict['count']

        for ingredient_dict in input_dict['ingredients']:
            if isinstance(ingredient_dict, dict):
                item = ingredient_dict['item'].split(':')[1]
            elif isinstance(ingredient_dict, list):
                item = ingredient_dict[0]['item'].split(':')[1]

            if item in output_dict['ingredients']:
                output_dict['ingredients'][item]['count'] += 1
            else:
                output_dict['ingredients'][item] = {
                    'count': 1
                }
                if 'data' in ingredient_dict:
                    output_dict['ingredients'][item]['data'] = ingredient_dict['data']

        self.data_dict[result_dict['item']] = output_dict

    def parse_dir(self):
        for file in os.scandir(self.recipe_dir):
            if not file.name.endswith('.json'):
                continue

            with open(file) as openfile:
                file_data = json.load(openfile)
                if file_data['type'] == 'crafting_shaped':
                    self.add_crafting_shaped(file_data)
                elif file_data['type'] == 'crafting_shapeless':
                    self.add_crafting_shapeless(file_data)

    def create_output(self):
        """Output self.data_dict into Python file for retrieval"""
        with open(self.output_filename, 'w') as openfile:
            json.dump(self.data_dict, openfile, indent=2)


def main():
    parser = RecipeParser('recipes/')
    parser.parse_dir()
    parser.create_output()


if __name__ == '__main__':
    main()