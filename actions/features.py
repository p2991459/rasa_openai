import nltk
import spacy
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')

import locationtagger
import mysql.connector
import openai
from .gpt import GPT,Example





def productionTable(full_message,broadway_show,cityCode): 
    query = productionShows(full_message,broadway_show,cityCode)
    print(query)
    reply = querySearcher(query)
    format_reply = ", ".join(str(result[0]) for result in reply)
    return format_reply

def regionalTable(full_message,broadway_show): 
    query = regionalShows(full_message,broadway_show)
    print(query)
    reply = querySearcher(query)
    format_reply = ", ".join(str(result[0]) for result in reply)
    return format_reply
    
###########openai function###########
openai.api_key = "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"

def openAiFunction(raw_text):
    prompt = raw_text
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.5,
    )
    print("openai answered",str(completions["choices"][0]["text"]).strip())
    return str(completions["choices"][0]["text"]).strip()

# nlp = spacy.load("en_core_web_sm")
# def extract_city(sentence):
#     doc = nlp(sentence)
#     if "west end" in sentence.lower():
#         return "London"
#     for ent in doc.ents:
#         if ent.label_ == "GPE":
#             return ent.text
#     return None

def extract_city(sentence):
    place_entity = locationtagger.find_locations(text = sentence)
    cities = place_entity.cities
    if len(cities)==0:
        return None
    return cities[0]


def location_coder(city):
    if city ==None:
        return None
    elif city.lower() == "london":
        data = ["('LN','WE','BR')"]
        return data[0]
    elif city.lower() == "new york":
        data = ["('NY','OF','FF')"]
        return data[0]
    else:
        query = f'''SELECT code FROM movie.code WHERE meaning = "{city}" AND type = 'MarketType';'''
        data = querySearcher(query)
        if len(data)<1:
            return f"('US')"
        print(data[0])
        return f"('{data[0][0]}')"


def querySearcher(query):
    dydb = mysql.connector.connect(
            user = "root",
            password = "Shashikant@420",
            database="movie"
        )     
    cursor = dydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    print("##############", data)
    return data

def question_formatter(prompt):

    # model to generate the answer
    gpt = GPT(engine="davinci",
            temperature=0.2,
            max_tokens=50)


    gpt.add_example(Example("does the book of mormon won any of tony awards","What Tony Awards has The Book of Mormon won?"))
    gpt.add_example(Example("what awards does the book of mormon nominated for",'What other awards has The Book of Mormon been nominated for?'))
    gpt.add_example(Example('is there any theatre playing the book of mormon on broadway','What theatre is The Book of Mormon playing on Broadway?'))
    gpt.add_example(Example("in how many broadway shows rosie O'donnell been","How many Broadway shows has Rosie O'Donnell been in?"))
    gpt.add_example(Example("did rosie O'donnell won any awards","What awards has Rosie O'Donnell won?"))
    gpt.add_example(Example("awards that rosid o'donnell won","What awards has Rosie O'Donnell won?"))
    gpt.add_example(Example('list the awards that mandy gozalez nominated for','What awards has Mandy Gonzalez been nominated for?'))
    gpt.add_example(Example('how many west end show kirsten aimee did','How many West End shows has Kirsten Aimee been in'))
    gpt.add_example(Example("broadway shows of jean anderson","How many Broadway shows has Jean Anderson been in?"))
    gpt.add_example(Example("marie andrews west end shows","How many West End shows has Marie Andrews been in?"))

    p = gpt.submit_request(prompt)

    return p['choices'][0]['text'][8:]


def productionShows(prompt,broadway_show,cityCode):

    # model to generate the answer
    prod = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=100)


    prod.add_example(Example("What time is the show Kimberly Akimbo tonight?" or "What time is Kimberly Akimbo showing this evening?" or "What are the show timings for Kimberly akimbo this weekend?" or "Is there a kimberly akimbo show tonight",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Kimberly Akimbo%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What time is The Lion King showing tonight in West End?" or "What are the show timings for The Lion King in West End?" or "What time is The Lion King showing this evening in West End?" or "Is there a The Lion King show tonight in West End?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Lion King%" AND market_type_code IN ('LN','WE','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in New York?" or "What are the show timings for The Belles of the Kitchen this weekend in New york?" or "When can I catch a performance of The Belles of the Kitchen this week in new york?" or "What time does The Belles of the Kitchen start on Friday evening in new york?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('NY','OF','FF') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in off-broadway?" or "What are the show timings for The Belles of the Kitchen this weekend in off-broadway?" or "When can I catch a performance of The Belles of the Kitchen this week in off-broadway?" or "What time does The Belles of the Kitchen start on Friday evening in off-broadway?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('NY','OF','FF') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in London?" or "What are the show timings for The Belles of the Kitchen this weekend in London?" or "When can I catch a performance of The Belles of the Kitchen this week in London?" or "What time does The Belles of the Kitchen start on Friday evening in London?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('LN','WE','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you give me an overview of the plot for this show?" or "What is the theme of the production" or "What is the central message or lesson of the show?",f'''SELECT tagline FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))
    prod.add_example(Example("How long does the performance last, roughly?" or "Can you give me an estimate of the show's running time?" or "What is the average duration of the performance?" or "Do you know the approximate length of the show?",f'''SELECT running_time FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("How long is the runtime of 'Harry Potter and the Cursed Child'?" or "Can you tell me how many hours I should expect to be in the theater for Harry Potter and the Cursed Child?" or "Can you give me an estimate of the total run time, including any intermissions, for Harry Potter and the Cursed Child?",f'''SELECT running_time FROM productions WHERE prodtitle LIKE "%Harry Potter and the Cursed Child%" AND production_status_code NOT IN ('CA', 'CL') AND running_time is not NULL AND running_time <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you provide me with a link to book tickets for the show" or "Can you give me a link to the box office or ticket sales page for the performance" or "Where can I find more information on booking tickets for the show you just talked about?" or "Can you send me a link to the online ticket sales page for the play/musical",f'''SELECT tickets FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What is the price range for tickets to the show" or "Can you provide me with information on ticket prices for the show?" or "Do you have any insights on the cost of tickets for the show in the West End?" or "What is the typical price range for tickets to see the show",f'''SELECT ticket_price FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you provide me with more details about the show and where I can learn more?" or "Where can I find more information on the plot of the show?" or "Can you recommend any resources to learn more about the show, such as articles or interviews?",f'''SELECT URL FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    

    p = prod.submit_request(prompt)

    return p['choices'][0]['text'][8:]

def regionalShows(prompt,broadway_show):

    # model to generate the answer
    regional = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=100)


    regional.add_example(Example("what is the ticket price for Nate the Great show","SELECT ticketprice FROM regionalshows WHERE showname LIKE '%Nate the Great%';"))
    regional.add_example(Example("What's the venue for The Lion King"or"In which theater is The Lion King currently running?"or"What's the name of the theater showing The Lion King?","SELECT theatrename FROM regionalshows WHERE showname LIKE '%Lion King%';"))
    regional.add_example(Example("What's playing at Mountainside Theatre"or"Current shows at Mountainside Theatre"or"Broadway shows at Mountainside Theatre","SELECT showname FROM regionalshows WHERE theatrename LIKE '%Mountainside Theatre%';"))
    regional.add_example(Example("When does Girls in the Boat start" or "When is Girls in the Boat beginning its run" or "When can I see Girls in the Boat?", "SELECT showstart FROM regionalshows WHERE showname LIKE '%Girls in the Boat%';"))
    regional.add_example(Example("What is the end date of Girls in the Boat" or "How long is Girls in the Boat running?" or "When is Girls in the Boat scheduled to end?" or "When is the last performance of Girls in the Boat?","SELECT showend FROM regionalshows WHERE showname LIKE '%Girls in the Boat%';"))
    regional.add_example(Example("What is 'The Masks of Oscar Wilde' about?" or "What's the plot of The Masks of Oscar Wilde?" or "What's the concept of The Masks of Oscar Wilde","SELECT showdesc FROM regionalshows WHERE showname LIKE '%The Masks of Oscar Wilde%';"))
#     regional.add_example(Example("Who is in the cast of Metropolis" or "Could you give me some information about the cast of Metropolis?" or "Can you give me a list of the actors in Metropolis",""))
    regional.add_example(Example("What is the phone number for the ticket office?" or "What is the telephone number to purchase tickets?" or "What is the phone number to book tickets?" or "What's the number to call to reserve tickets" or "where can I get tickets for the show",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%{broadway_show}%';"))
    regional.add_example(Example("What's the phone number to book tickets for Metropolis" or "Can you give me the number to call for Metropolis tickets" or "Is there a phone number I can call to purchase tickets for Metropolis","SELECT ticketphone FROM regionalshows WHERE showname LIKE '%Metropolis%';"))
    regional.add_example(Example("is there any show in Tokyo" or "What musicals can I see in Tokyo?" or "Can you tell me which shows are currently running in Tokyo?" or "Can you recommend a theater or show to see while in Tokyo?","SELECT showname FROM regionalshows WHERE city LIKE '%Tokyo%';"))
    regional.add_example(Example("Where can I find more details about the show" or "any other links about the show details" or "can I get social media or websibe link of show",f"SELECT website,facebook,twitter,instagram FROM regionalshows WHERE showname LIKE '%{broadway_show}%';"))
    regional.add_example(Example("where can I watch American String Quartet show" or "Where is the venue for the American String Quartet show located?" or "Can you give me the address of the theater where the American String Quartet show is being performed?" or "Are there any nearby landmarks or points of reference that can help me locate the venue for the American String Quartet show?","SELECT address,city,state,Zip FROM regionalshows WHERE showname LIKE '%American String Quartet%';"))
    regional.add_example(Example("where can I get tickets for Girls in the Boat show in Tampa",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%Girls in the Boat%' AND city LIKE '%Tampa%';"))
    
    p = regional.submit_request(prompt)

    return p['choices'][0]['text'][8:]