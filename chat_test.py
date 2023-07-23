# from griptape.structures import Agent
# from griptape.utils import Chat
from gpt4all import GPT4All
from rich.console import Console

console = Console()

# agent = Agent()
# Chat(agent).start()

# console.print(GPT4All.list_models())
model = GPT4All("wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin")
prompt = f"Tell me the story of the Edmund Fitzgerald"
template = f"""
A chat between a curious user and artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions and takes on the persona of a Minnesotan using the local dialect, slang, and colloquialisms. 

USER: {prompt}
 
ASSISTANT: 
"""
console.print(template)
console.print(model.generate(prompt=prompt, max_tokens=200, top_k=1))
# tokens = list(model.generate(prompt="The capital of France is ", streaming=True))
# console.print(tokens)
# console.print({'role': 'assistant', 'content': ''.join(tokens)})

# with model.chat_session():
#     user = model.generate(prompt=template)
#     model.current_chat_session.append({'role': 'assistant', 'content': ''.join(tokens)})
#
#     tokens = list(model.generate(prompt='write me a poem about dogs', top_k=1, streaming=True))
#     model.current_chat_session.append({'role': 'assistant', 'content': ''.join(tokens)})
#
#     console.print(model.current_chat_session)
