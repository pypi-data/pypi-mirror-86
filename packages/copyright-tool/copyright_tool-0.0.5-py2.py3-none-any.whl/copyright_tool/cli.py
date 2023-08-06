"""Console script for copyright_tool."""
from typing import Dict, List
import datetime
import os
import sys
import git

from gitignore_parser import parse_gitignore


end_terminators = {
    '//style': '// inserted by copyright_tool',
    '#style': '## inserted by copyright_tool'
}

language_support = {
    'c': '//cstyle',
    'cpp': '//cstyle',
    'c++': '//cstyle',
    'h': '//cstyle',
    'hpp': '//cstyle',
    'ts': '//cstyle',
    'js': '//cstyle',
    'tsx': '//cstyle',
    'jsx': '//cstyle',
    'py': '#style',
    'sh': '#style',
    'java': '//cstyle',
    'tf': '#style',
}

def get_copyright_files_map(path):
  file_map = {}
  for file_name in os.listdir(path):
    if file_name.startswith('.copyright.'):
      language = file_name.split('.')[2]
      style = language_support.get(language)
      if not style:
        raise ValueError(f'Language {language} not supported')
      file_map[language] = file_name
  return file_map


def get_all_files(path):
  copyright_ignore_path = f'{path}/.copyrightignore'
  matches = None
  if os.path.exists(copyright_ignore_path):
    matches = parse_gitignore(copyright_ignore_path)
  copyright_file_map = get_copyright_files_map(path)

  def get_tracked_files(trees):
    paths = []
    for tree in trees:
      for blob in tree.blobs:
        language = blob.abspath.split('.')[-1]
        if not matches or not matches(blob.abspath) and copyright_file_map.get(language):
          paths.append(blob.abspath)
      if tree.trees:
        paths.extend(get_tracked_files(tree.trees))
    return paths
  repo = git.Repo(path)

  return get_tracked_files([repo.tree()])


def main():
  if len(sys.argv) != 2:
    print("Please enter the path to the root of your Git repository")
    sys.exit(1)

  path = sys.argv[1]
  copyright_file_map = get_copyright_files_map(path)
  file_name: str
  for file_name in get_all_files(path):
    with open(file_name, 'r') as filed:
      language = file_name.split('.')[-1]
      end_terminator = end_terminators.get(language_support.get(language))

      body_lines: List[str] = filed.readlines()
      if not body_lines:
        continue

      try:
        end_terminator_index = body_lines.index(end_terminator+'\n') + 2
      except:
        end_terminator_index = -1

      start_index = 0
      new_body_lines = []
      if body_lines[0].startswith('#!'):
        start_index = 1
        new_body_lines = [body_lines[0]]

      if end_terminator_index >= 0:
        content_lines = body_lines[end_terminator_index:]
      else:
        content_lines = body_lines[start_index:]

    copyright_file = f"{path}/{copyright_file_map.get(language)}"

    with open(copyright_file) as filed:
      copyright = filed.read().format(year = datetime.datetime.now().year)

    new_body_lines += [copyright, '\n', end_terminator, '\n', '\n'] + content_lines

    with open(file_name, 'w+') as filed:
      filed.write(''.join(new_body_lines))



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
