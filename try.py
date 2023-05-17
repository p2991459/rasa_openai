# import openai
# from model_rasa.actions.gpt import GPT,Example


# openai.api_key = "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"


# def question_formatter(prompt):

#     # model to generate the answer
#     gpt = GPT(engine="davinci",
#             temperature=0.2,
#             max_tokens=50)


#     gpt.add_example(Example("does the book of mormon won any of tony awards","What Tony Awards has The Book of Mormon won?"))
#     gpt.add_example(Example("what awards does the book of mormon nominated for",'What other awards has The Book of Mormon been nominated for?'))
#     gpt.add_example(Example('is there any theatre playing the book of mormon on broadway','What theatre is The Book of Mormon playing on Broadway?'))
#     gpt.add_example(Example("in how many broadway shows rosie O'donnell been","How many Broadway shows has Rosie O'Donnell been in?"))
#     gpt.add_example(Example("did rosie O'donnell won any awards","What awards has Rosie O'Donnell won?"))
#     gpt.add_example(Example("awards that rosid o'donnell won","What awards has Rosie O'Donnell won?"))
#     gpt.add_example(Example('list the awards that mandy gozalez nominated for','What awards has Mandy Gonzalez been nominated for?'))
#     gpt.add_example(Example('how many west end show kirsten aimee did','How many West End shows has Kirsten Aimee been in'))
#     gpt.add_example(Example("broadway shows of jean anderson","How many Broadway shows has Jean Anderson been in?"))
#     gpt.add_example(Example("marie andrews west end shows","How many West End shows has Marie Andrews been in?"))

#     p = gpt.submit_request(prompt)

#     return p['choices'][0]['text'][8:]

# a = question_formatter("in ow many west End shows has La Vern Baker been")
# print(a)
import openai
openai.api_key = "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"

def openAiFunction(raw_text):
    prompt = raw_text
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=25,
        temperature=0.2,
    )
    print("openai extraction ",completions["choices"][0]["text"])
    return completions["choices"][0]["text"]

text = 'what is the timing for the Haminlton show'
at = openAiFunction(f"extract city from text and return none if not mentioned in text\ntext: {text}")
if at.strip() == "None":
    print("yes")
else:
    print(type(at))
