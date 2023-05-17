# import nltk
# import spacy
# nltk.downloader.download('maxent_ne_chunker')
# nltk.downloader.download('words')
# nltk.downloader.download('treebank')
# nltk.downloader.download('maxent_treebank_pos_tagger')
# nltk.downloader.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# import locationtagger
import mysql.connector
import openai
from .gpt import GPT,Example

def openFunction(crust):

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=crust,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completions["choices"][0]["text"]



def productionTable(full_message,broadway_show,cityCode,city): 
    query = productionShows(full_message,broadway_show,cityCode)
    print(query)
    data = querySearcher(query)
    final_que = full_message + f",{data}"
    format_reply = ansShows(final_que,broadway_show,city)
    return format_reply

def regionalTable(full_message,broadway_show,city): 
    query = regionalShows(full_message,broadway_show,city)
    print(query)
    data = querySearcher(query)
    final_que = full_message + f",{data}"
    format_reply = ansShows(final_que,broadway_show,city)
    return format_reply
    
###########openai function###########
openai.api_key = "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"



# nlp = spacy.load("en_core_web_sm")
# def extract_city(sentence):
#     doc = nlp(sentence)
#     if "west end" in sentence.lower():
#         return "London"
#     for ent in doc.ents:
#         if ent.label_ == "GPE":
#             return ent.text
#     return None

# def extract_city(sentence):
#     place_entity = locationtagger.find_locations(text = sentence)
#     cities = place_entity.cities
#     print(cities)
#     if len(cities)==0:
#         return None
#     elif len(cities)>=2 and cities[0]=='Hamilton':
#         return cities[1]
#     return cities[0]


def location_coder(city):
    if city ==None:
        return None
    elif city.lower() == "london":
        data = ["('LN','WE')"]
        print(data)
        return data[0]
    elif city.lower() == "new york":
        data = ["('NY','OF','FF','BR')"]
        print(data)
        return data[0]
    else:
        query = f'''SELECT code FROM movie.code WHERE meaning = "{city}" AND type = 'MarketType';'''
        data = querySearcher(query)
        if len(data)==0:
            print(data)
            return f"('US')"
        print(data)
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


    prod.add_example(Example("What time is the show Kimberly Akimbo tonight?" or "What time is Kimberly Akimbo showing this evening?" or "What are the show timings for Kimberly akimbo this weekend?" or "Is there a kimberly akimbo show tonight" or "is there any shows of kimberly akimbo on sunday",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Kimberly Akimbo%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What time is The Lion King showing tonight in West End?" or "What are the show timings for The Lion King in West End?" or "What time is The Lion King showing this evening in West End?" or "Is there a The Lion King show tonight in West End?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Lion King%" AND market_type_code IN ('LN','WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in New York?" or "What are the show timings for The Belles of the Kitchen this weekend in New york?" or "When can I catch a performance of The Belles of the Kitchen this week in new york?" or "What time does The Belles of the Kitchen start on Friday evening in new york?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('NY','OF','FF','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in off-broadway?" or "What are the show timings for The Belles of the Kitchen this weekend in off-broadway?" or "When can I catch a performance of The Belles of the Kitchen this week in off-broadway?" or "What time does The Belles of the Kitchen start on Friday evening in off-broadway?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('NY','OF','FF','BR') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What are the show timings for The Belles of the Kitchen in London?" or "What are the show timings for The Belles of the Kitchen this weekend in London?" or "When can I catch a performance of The Belles of the Kitchen this week in London?" or "What time does The Belles of the Kitchen start on Friday evening in London?",f'''SELECT schedule_text FROM productions WHERE prodtitle LIKE "%Belles of the Kitchen%" AND market_type_code IN ('LN','WE') AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you give me an overview of the plot for this show?" or "can you tell me more about the show" or "What is the theme of the production" or "What is the central message or lesson of the show?",f'''SELECT tagline FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))
    prod.add_example(Example("How long does the performance last, roughly?" or "Can you give me an estimate of the show's running time?" or "What is the average duration of the performance?" or "Do you know the approximate length of the show?",f'''SELECT running_time FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("How long is the runtime of 'Harry Potter and the Cursed Child'?" or "Can you tell me how many hours I should expect to be in the theater for Harry Potter and the Cursed Child?" or "Can you give me an estimate of the total run time, including any intermissions, for Harry Potter and the Cursed Child?",f'''SELECT running_time FROM productions WHERE prodtitle LIKE "%Harry Potter and the Cursed Child%" AND production_status_code NOT IN ('CA', 'CL') AND running_time is not NULL AND running_time <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you provide me with a link to book tickets for the show" or "Can you give me a link to the box office or ticket sales page for the performance" or "Where can I find more information on booking tickets for the show you just talked about?" or "Can you send me a link to the online ticket sales page for the play/musical",f'''SELECT tickets FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("What is the price range for tickets to the show" or "Can you provide me with information on ticket prices for the show?" or "Do you have any insights on the cost of tickets for the show in the West End?" or "What is the typical price range for tickets to see the show",f'''SELECT ticket_price FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("Can you provide me with more details about the show and where I can learn more?" or "Where can I find more information on the plot of the show?" or "Can you recommend any resources to learn more about the show, such as articles or interviews?",f'''SELECT URL FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND market_type_code IN {cityCode} AND production_status_code NOT IN ('CA', 'CL') AND schedule_text is not NULL AND schedule_text <> '' LIMIT 1;'''))
    prod.add_example(Example("can you tell me some description about the show" or "what is show about",f'''SELECT tagline FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))
    prod.add_example(Example("can you tell me about Jersey Boys" or "can you tell me more about Jersey Boys show", f'''SELECT tagline FROM productions WHERE prodtitle LIKE "%{broadway_show}%" AND production_status_code NOT IN ('CA', 'CL') AND tagline is not NULL AND tagline <> '' LIMIT 1;'''))

    p = prod.submit_request(prompt)

    return p['choices'][0]['text'][8:]

def regionalShows(prompt,broadway_show,city):

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
    regional.add_example(Example("where can I watch American String Quartet show" or "Where is the venue for the American String Quartet show located?" or "Can you give me the address of the theater where the American String Quartet show is being performed?" or "Are there any nearby landmarks or points of reference that can help me locate the venue for the American String Quartet show?","SELECT address,city,Zip FROM regionalshows WHERE showname LIKE '%American String Quartet%';"))
    regional.add_example(Example("where can I get tickets for Girls in the Boat show in Tampa",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%Girls in the Boat%' AND city LIKE '%Tampa%';"))
    regional.add_example(Example("where can I get tickets the show" or "can I get contact number to book tickets" or "can I book tickets on phone for the show",f"SELECT ticketphone FROM regionalshows WHERE showname LIKE '%{broadway_show}%' AND city LIKE '%{city}%';"))
    regional.add_example(Example("what is the estimated runtime of Into The Woods show" or "What is the average duration of Into The Woods performance?","SELECT runningttime FROM regionalshows WHERE showname LIKE '%Into the Woods%' LIMIT 1;"))
    regional.add_example(Example("what is the estimated runtime of The show" or "What is the average duration of The performance?",f"SELECT runningttime FROM regionalshows WHERE showname LIKE '%{broadway_show}%' LIMIT 1;"))
    regional.add_example(Example("can you tell me theatre name" or "which theatre" or "can you tell me vanue of the show",f"SELECT theatrename FROM regionalshows WHERE showname LIKE '%{broadway_show}%' AND city LIKE '%{city}%' LIMIT 1;"))
   
    p = regional.submit_request(prompt)

    return p['choices'][0]['text'][8:]

def ansShows(prompt,broadway_show,city):

    # model to generate the answer
    ans = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=100)


    ans.add_example(Example("what are the timings for The Lion King in London,[('Tuesdays: 7:00pm, Wednesdays: 7:00pm, Thursdays: 7:00pm, Fridays: 8:00pm, Saturdays: 2:00pm and 8:00pm, Sundays: 1:00pm and 6:30pm',)]","The timings for The Lion King show in London are as follows: Tuesdays at 7:00pm, Wednesdays at 7:00pm, Thursdays at 7:00pm, Fridays at 8:00pm, Saturdays at 2:00pm and 8:00pm, and Sundays at 1:00pm and 6:30pm. "))
    ans.add_example(Example("what is the timings for The Lion King in London on sunday,[('Tuesdays: 7:00pm, Wednesdays: 7:00pm, Thursdays: 7:00pm, Fridays: 8:00pm, Saturdays: 2:00pm and 8:00pm, Sundays: 1:00pm and 6:30pm',)]","The timing for Sunday show The Lion King in London are 1:00pm and 6:30pm"))
    ans.add_example(Example("what is ticket price of the show,[('$35',)]",f"The ticket price for the {broadway_show} show is $35 in {city}"))
    ans.add_example(Example("what is estimated runtime of the show,[('2 hours and 30 minutes, with one intermission',)]","The estimated runtime of the show is 2 hours and 30 minutes, with one intermission."))
    ans.add_example(Example('''what shows are currently playing in Portland,[("Where's Bruno?",)]''',"One of the shows currently playing in Portland is 'Where's Bruno?'."))
    ans.add_example(Example("is there any show in Seattle,[('Godspell-2012 Revised Version',), ('Fame',)]","Yes, there are currently two shows playing in Seattle - 'Godspell-2012 Revised Version' and 'Fame'."))
    ans.add_example(Example("can I book tickets on phone,[('408-792-4111',)]",f"Yes you can call on 408-792-4111 to book tickets for {broadway_show}"))
    ans.add_example(Example('''what shows are currently playing in Falls Village,[('94th Season Opening Benefit Concert & Reception',), ('Eleora Piano Quartet',), ('Misha Dichter, Piano & Oskar Espina Ruiz, Clarinet',), ('Horszowski Trio',), ('Arianna String Quartet & Judith Gordon, Piano',), ('Ariel Quartet',), ('PENDERECKI STRING QUARTET & ANYA ALEXEYEV, PIANO',), ('EUCLID QUARTET',), ('American String Quartet',), ('Ulysses Quartet & Oskar Espina Ruiz, Clarinet',), ('Lydian String Quartet & Victoria Schwartzman, Piano',), ('Balourdet Quartet & Simone Dinnerstein, Piano',), ('Parker Quartet & Orion Weiss, Piano',), ('Borromeo String Quartet & Henry Kramer, Piano',), ('Dali Quartet & Vanessa Perez, Piano',), ('Cassatt String Quartet & Ursula Oppens, Piano',), ('PAUL WINTER: JAZZ AT MUSIC MOUNTAIN OPENING CONCERT',), ('NEW BLACK EAGLE JAZZ BAND',), ('WANDA HOUSTON PROJECT',), ('MAUCHA ADNET WITH THE BRAZILIAN TRIO "BOSSA ALWAYS NOVA"',), ('BARBARA FASANO TRIO',), ('SWINGTIME BIG BAND',), ('BILL CHARLAP TRIO',), ('KELLIN HANAS QUINTET',), ('THE CURTIS BROTHERS',), ('NEW YORK GILBERT & SULLIVAN PLAYERS',), ('GALVANIZED JAZZ BAND',)] ''',"There are several shows currently playing in Falls Village. Some of the shows include the 94th Season Opening Benefit Concert & Reception, Eleora Piano Quartet, Horszowski Trio, and the Arianna String Quartet & Judith Gordon, Piano. Other shows include jazz performances by Paul Winter and the New Black Eagle Jazz Band, and performances by the New York Gilbert & Sullivan Players."))
    ans.add_example(Example("what is the ticket price for Jersey Boys in Adrian,[('$22-$44',)]","The ticket prices for Jersey Boys in Adrian range from $22 to $44. Please note that ticket prices may very depending on factors such as seat location and date of performance."))
    ans.add_example(Example("where can I get more information about Jersey Boys,[('https://croswell.org/jerseyboys', 'https://facebook.com/thecroswell', '', 'https://instagram.com/thecroswell')]","You can find more information about Jersey Boys at the Croswell Opera House's website, which is https://croswell.org/jerseyboys. Additionally, you can check out the Croswell Opera House's social media pages on Facebook (https://facebook.com/thecroswell) and Instagram (https://instagram.com/thecroswell) for updates and news about the production."))
    ans.add_example(Example("in which theatre,[('The Orpheum Theatre',)]" or "what is the vanue of the show,[('The Orpheum Theatre',)]",f"{broadway_show} is playing at the Orpheum Theatre"))
    ans.add_example(Example("what is the ticket price of Once On This Island Jr in Racine,[('',)]","sorry but ticket prices are not avaliable yet for Once On This Island Jr show in Racine."))
    ans.add_example(Example("can you tell me address of the vanue,[('1516 Ohio St', 'Racine', '53405')]",f"The address of the venue for {broadway_show} is 1516 Ohio St, Racine, ZIP code- 53405"))
    ans.add_example(Example("what are the timings for fancy nancy the musical,[]",f"Sorry there are no fancy nancy the musical shows in {city}"))
    ans.add_example(Example("what's the vanue of the show,[('Music Mountain',)]" or "vanue name,[('Music Mountain',)]",f"The Vanue for {broadway_show} is Music Mountain"))

    p = ans.submit_request(prompt)

    return p['choices'][0]['text'][8:]


def extraction_info(prompt):

    # model to generate the answer
    extractor = GPT(engine="text-davinci-003",
            temperature=0.2,
            max_tokens=100)


    extractor.add_example(Example("what are the timings for Hamilton show in New York","Hamilton;New York"))
    extractor.add_example(Example("what shows are currently going on in Falls Village","None;Falls Village"))
    extractor.add_example(Example("where can I watch The Lion King","Lion King;None"))
    extractor.add_example(Example("so how can I book tickets for the show","None;None"))
    extractor.add_example(Example("how can I book tickets for the Chicago in Hamilton city","Chicago;Hamilton"))
    

    p = extractor.submit_request(prompt)

    both = p['choices'][0]['text'][8:].split(";")

    for i in range(len(both)):
        if both[i] == 'None':
            both[i] = None
    return both