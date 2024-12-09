import os
from pathlib import Path
import re
from collections import defaultdict

with open('../data/MagicCompRules 20240206.txt', 'r', encoding='utf-8') as f:
    contents = f.read()

sections = {}
output_dir = Path(os.path.abspath(str('../data/parsed_rules')))


for line in contents.splitlines():
    if line.startswith('Contents'):
        continue
    section_number = str(line[0]) if line and line.strip() else None
    current_section_name = line.strip()[3:] if line and line.strip() else ''
    if not sections or str(section_number) not in [str(k) for k in list(sections.keys())]:
        sections[section_number] = [current_section_name]
    elif re.match(r'^\d+\..*', line):
        line_split = line.split(".")
        section_number = line_split[0]
        line_text = line_split[1:][:1][0].split(' ')[0]
        # print(section_number, line_text)
        file_name_subsection = f'.{line_text}'
        file_name = f'{output_dir}/{section_number}{file_name_subsection if len(line_text) > 0 else ""}.txt'
        print(line_split[1:][:1][0].split(' ')[0:])
        # with open(file_name, 'w', encoding='utf-8') as f:
        #     while True:
        #         next_line = contents.splitlines().pop(0).strip()
        #         if not next_line or not re.match(rf'^{re.escape(str(line[0]))}.*', next_line):
        #             break
        #         f.write(next_line + '\n')
    elif len(line) > 0:
        print(line)

"""
['100', ' General']
['100', '1', ' These Magic rules apply to any Magic game with two or more players, including two-player games and multiplayer games', '']
['100', '1a A two-player game is a game that begins with only two players', '']
"""