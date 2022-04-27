import streamlit as st
import logging
from random import randint

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Hauptstädte-Quiz: Europa",
                   page_icon=":mortar_board:")
st.title('Hauptstädte-Quiz: Europa \n *für Xenia*')

# color "st.buttons" in main page light blue:
st.markdown("""
 <style>
 div.stButton > button:first-child {
     background-color: rgb(200, 54, 180); # rgb(216, 78, 192);
 }
 </style>""", unsafe_allow_html=True)
# hide menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# site-structure and main-widgets:
first = st.container()
second = st.container()
end = st.sidebar.button("Ende")
start = st.sidebar.button("Start")
next = second.button("Nächste Frage")

# Dictionary of all countries and capitals in Europe
europe = {
    'Niederlande' : 'Amsterdam', 'Andorra' : 'Andorra', 'Griechenland' : 'Athen', 'Serbien' : 'Belgrad',
    'Deutschland' : 'Berlin', 'Schweiz' : 'Bern', 'Slowakei' : 'Bratislava', 'Belgien' : 'Brüssel',
    'Ungarn' : 'Budapest', 'Rumänien' : 'Bukarest', 'Republik Moldau' : 'Kischinau', 'San Marino' : 'San Marino',
    'Irland' : 'Dublin', 'Finnland' : 'Helsinki', 'Ukraine' : 'Kiew', 'Dänemark' : 'Kopenhagen',
    'Portugal' : 'Lissabon', 'Slowenien' : 'Ljubljana', 'Vereinigtes Königreich' : 'London',
    'Luxemburg' : 'Luxemburg', 'Spanien' : 'Madrid', 'Belarus' : 'Minsk', 'Monaco' : 'Monaco',
    'Russland' : 'Moskau', 'Republik Zypern' : 'Nikosia', 'Norwegen' : 'Oslo', 'Frankreich' : 'Paris',
    'Montenegro' : 'Podgorica', 'Tschechien' : 'Prag', 'Kosovo' : 'Pristina', 'Island' : 'Reykjavik',
    'Lettland' : 'Riga', 'Italien' : 'Rom', 'Bosnien und Herzegowina' : 'Sarajevo', 'Nordmazedonien' : 'Skopje',
    'Bulgarien' : 'Sofia', 'Schweden' : 'Stockholm', 'Estland' : 'Tallinn', 'Albanien' : 'Tirana',
    'Liechtenstein' : 'Vaduz', 'Malta' : 'Valletta', 'Vatikan' : 'Vatikanstadt', 'Litauen' : 'Vilnius',
    'Polen' : 'Warschau', 'Österreich' : 'Wien', 'Kroatien' : 'Zagreb'
    }

# initiate necessary session_state-variables #########
if 'countries' not in st.session_state:
    st.session_state['countries'] = list(europe.keys())
# number of questions asked:
if 'questions' not in st.session_state:
    st.session_state['questions'] = 0
if 'right' not in st.session_state:
    st.session_state['right'] = 0
if 'wrong' not in st.session_state:
    st.session_state['wrong'] = 0
if 'capital' not in st.session_state:
    st.session_state['capital'] = ""
if 'last' not in st.session_state:
    st.session_state['last'] = "last"
# 'number' stores the number of countries remaining:
if 'number' not in st.session_state:
    st.session_state['number'] = len(st.session_state['countries'])-1
# select a random item out of the coutries list:
x = randint(0, st.session_state['number'])
# 'country' stores the country in the current question:
if 'country' not in st.session_state:
    st.session_state['country'] = st.session_state['countries'][x]

def new():
    try:
        x = randint(0, st.session_state['number'])
    except:
        quit()
    st.session_state['country'] = st.session_state['countries'][x]

def grade(perc):
    if perc == 100:
        grade = "fantastisch! (⊃｡•́‿•̀｡)⊃"
    elif perc > 80:
        grade = "sehr gut! (ɔ ᵔᴗᵔ)ɔ"
    elif perc > 70:
        grade = "gut! ( ͡° ͜ ͡°)"
    elif perc >= 50:
        grade = "ok! (~ • ᴥ •)~"
    elif perc > 30:
        grade = "nicht so gut! (｡ŏ﹏ŏ)"
    elif perc > 20:
        grade = "schlecht! (ɔ ᴗ_ᴗ)ɔ"
    else:
        grade = "traurig! (ɔ •︵•)ɔ"
    return grade

def reset():
    # reset values:
    st.session_state['countries'] = list(europe.keys())
    st.session_state['number'] = len(st.session_state['countries'])-1
    st.session_state['questions'] = 0
    st.session_state['right'] = 0
    st.session_state['wrong'] = 0
    st.session_state['capital'] = ""

def main():
    country = st.session_state['country']
    first.markdown(f"Wie heißt die Hauptstadt von {country}?")
    capital = first.text_input("", "", key=st.session_state['questions'])
    if capital != st.session_state['last'] and capital != "":
        st.session_state['last'] = capital
        st.session_state['questions'] += 1
        st.session_state['capital'] = capital
        if st.session_state['capital'] == europe[country]:
            st.session_state['countries'].remove(country)
            st.session_state['right'] += 1
            st.session_state['number'] -= 1
            if st.session_state['number'] == -1:
                perc = st.session_state['right'] * 100 / st.session_state['questions']
                second.write(f"Du kennst alle Hauptstädte in Europa (ɔ °0°)ɔ\nund hast {st.session_state['right']} von {st.session_state['questions']} Fragen richtig beantwortet ({int(round(perc,0))} Prozent).")
                second.write(f"Das ist {grade(perc)}")
                reset()
            else:
                second.write("Das ist richtig. (✿^‿^)")
                second.write(f"{st.session_state['right']} von {st.session_state['questions']} (Noch {str(st.session_state['number']+1)} Länder)")

        else:
            st.session_state['wrong'] += 1
            second.write(f"'{capital}' ist falsch. (ɔ •︵•)ɔ \n Die Hauptstadt von {country} ist: {europe[st.session_state['country']]}")
            second.write(f"{st.session_state['right']} von {st.session_state['questions']} (Noch {str(st.session_state['number']+1)} Länder)")

def quit():
    try:
        perc = st.session_state['right'] * 100 / st.session_state['questions']
    except:
        perc = 0
    second.write(f"Du hast {st.session_state['right']} von {st.session_state['questions']} Fragen richtig beantwortet ({int(round(perc,0))} Prozent).")
    second.write(f"Das ist {grade(perc)}")
    reset()

if end:
    quit()

if start:
    new()

if next:
    new()

#########################################################################
if __name__ == '__main__':
    main()
