import g4f

def ask_gpt_normal(promt:str)->str:
    # normal response
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": promt}],
    )
    return response

# streamed completion
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True,
)

for message in response:
    print(message, flush=True, end='')

print(ask_gpt_normal("Какова средняя продолжительность жизни черепахи?"))