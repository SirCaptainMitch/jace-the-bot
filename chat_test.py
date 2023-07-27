# from griptape.structures import Agent
# from griptape.utils import Chat
from gpt4all import GPT4All
from rich.console import Console

console = Console()

# agent = Agent()
# Chat(agent).start()

# console.print(GPT4All.list_models())
model_name = 'ggml-model-gpt4all-falcon-q4_0.bin'
model = GPT4All(model_name)
prompt = f"Tell me about yourself"
prompt_template = f"### Instruction: You are a Minnesotan and respond in a Minnesota dialect, colloquialisms, and slang {prompt}\n### Response:"
console.print(prompt)
console.print(model.generate(prompt=prompt, max_tokens=260, top_k=1))

