import json
import os
import argparse
from os import path


class TreeParce:
    def __init__(self, file_name) -> None:
        super().__init__()

        with open(file_name, encoding='utf-8') as json_file:
            self.data = json.load(json_file)

        self.file_list = []
        self.dir_lists = []

        self.extract_paths(self.data[0])

    def extract_paths(self, json_root):
        if json_root['type'] == 'directory':
            self.dir_lists.append(json_root['name'])
            for item in json_root['contents']:
                self.extract_paths(item)

        elif json_root['type'] == 'file':
            self.file_list.append(json_root['name'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', default=None, type=str, help='source json')
    parser.add_argument('-p', '--path', default=None, type=str, help='root path to scan')
    parser.add_argument('-d', '--dry_run', default=False, action="store_true", help='dry run')

    args = parser.parse_args()

    if args.source is None:
        print("ERROR: source path is empty")

    dry_run = False
    if args.dry_run:
        dry_run = True

    tree_parce = TreeParce(args.source)

    target_path = args.path

    for item in tree_parce.dir_lists:
        item = target_path + "/" + item

        if not path.exists(item):
            print("NEW DIR:" + item)
            if not dry_run:
                os.makedirs(item, 493, exist_ok=True)

    for item in tree_parce.file_list:
        item = target_path + "/" + item
        if not path.exists(item):
            print("NEW FILE:" + item)
            if not dry_run:
                with open(item, 'w') as fp:
                    pass
