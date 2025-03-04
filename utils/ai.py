import ollama

omodel = "llama3.2:1b"
oclient = ollama.Client(host="http://0.0.0.0:11434")

def askAI(text):
    messages = [{"role":"user", "content":text}]
    response = oclient.chat(model=omodel, messages=messages, stream=False)
    return response