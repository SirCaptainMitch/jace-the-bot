from rich.console import Console

console = Console()

with open('../data/MagicCompRules 20240206.txt', 'r', encoding='utf-8') as f:
    rules = f.read()

console.print(
    rules.index('Contents')
)

console.print(
    rules.index('1. Game Concepts')
)

console.print(rules[813:823])

