"""
A quiz app for learning the capitals of Europe made with streamlit.
"""

import logging
from random import randint

import Levenshtein
import streamlit as st

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Hauptstädte-Quiz: Europa", page_icon=":mortar_board:")
st.title("Hauptstädte-Quiz: Europa \n *für Xenia*")

# color "st.buttons" in main page light blue:
st.markdown(
    """
 <style>
 div.stButton > button:first-child {
     background-color: rgb(200, 54, 180); # rgb(216, 78, 192);
 }
 </style>""",
    unsafe_allow_html=True,
)
# hide menu
st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)

# site-structure and main-widgets:
first = st.container()
second = st.container()
start = st.sidebar.button("Start")
end = st.sidebar.button("Ende")
next = second.button("Nächste Frage")

# Dictionary of all countries and capitals in Europe
europe = {
    "Niederlande": "Amsterdam",
    "Andorra": "Andorra",
    "Griechenland": "Athen",
    "Serbien": "Belgrad",
    "Deutschland": "Berlin",
    "Schweiz": "Bern",
    "Slowakei": "Bratislava",
    "Belgien": "Brüssel",
    "Ungarn": "Budapest",
    "Rumänien": "Bukarest",
    "Republik Moldau": "Kischinau",
    "San Marino": "San Marino",
    "Irland": "Dublin",
    "Finnland": "Helsinki",
    "Ukraine": "Kiew",
    "Dänemark": "Kopenhagen",
    "Portugal": "Lissabon",
    "Slowenien": "Ljubljana",
    "Vereinigtes Königreich": "London",
    "Luxemburg": "Luxemburg",
    "Spanien": "Madrid",
    "Belarus": "Minsk",
    "Monaco": "Monaco",
    "Russland": "Moskau",
    "Republik Zypern": "Nikosia",
    "Norwegen": "Oslo",
    "Frankreich": "Paris",
    "Montenegro": "Podgorica",
    "Tschechien": "Prag",
    "Kosovo": "Pristina",
    "Island": "Reykjavik",
    "Lettland": "Riga",
    "Italien": "Rom",
    "Bosnien und Herzegowina": "Sarajevo",
    "Nordmazedonien": "Skopje",
    "Bulgarien": "Sofia",
    "Schweden": "Stockholm",
    "Estland": "Tallinn",
    "Albanien": "Tirana",
    "Liechtenstein": "Vaduz",
    "Malta": "Valletta",
    "Vatikan": "Vatikanstadt",
    "Litauen": "Vilnius",
    "Polen": "Warschau",
    "Österreich": "Wien",
    "Kroatien": "Zagreb",
}

# initiate necessary session_state-variables #########
if "countries" not in st.session_state:
    st.session_state["countries"] = list(europe.keys())
# number of questions asked:
if "questions" not in st.session_state:
    st.session_state["questions"] = 0
if "right" not in st.session_state:
    st.session_state["right"] = 0
if "wrong" not in st.session_state:
    st.session_state["wrong"] = 0
if "capital" not in st.session_state:
    st.session_state["capital"] = ""
if "last" not in st.session_state:
    st.session_state["last"] = "last"
# 'number' stores the number of countries remaining:
if "number" not in st.session_state:
    st.session_state["number"] = len(st.session_state["countries"]) - 1
x = randint(0, st.session_state["number"])
# 'country' stores the country in the current question:
if "country" not in st.session_state:
    st.session_state["country"] = st.session_state["countries"][x]


def new():
    try:
        x = randint(0, st.session_state["number"])
    except:
        quit()
    st.session_state["country"] = st.session_state["countries"][x]


def grade(perc):
    if perc == 100:
        grad = "fantastisch! (⊃｡•́‿•̀｡)⊃"
    elif perc > 80:
        grad = "sehr gut! (ɔ ᵔᴗᵔ)ɔ"
    elif perc > 70:
        grad = "gut! ( ͡° ͜ ͡°)"
    elif perc >= 50:
        grad = "ok! (~ • ᴥ •)~"
    elif perc > 30:
        grad = "nicht so gut! (｡ŏ﹏ŏ)"
    elif perc > 20:
        grad = "schlecht! (ɔ ᴗ_ᴗ)ɔ"
    else:
        grad = "traurig! (ɔ •︵•)ɔ"
    return grad


def reset():
    # reset values:
    st.session_state["countries"] = list(europe.keys())
    st.session_state["number"] = len(st.session_state["countries"]) - 1
    st.session_state["questions"] = 0
    st.session_state["right"] = 0
    st.session_state["wrong"] = 0
    st.session_state["capital"] = ""


def check_distance(target, entry):
    return Levenshtein.distance(target.lower(), entry.lower())


def main():
    country = st.session_state["country"]
    first.markdown(
        f"Wie heißt die Hauptstadt von {country}? [(Wikipedia)](https://de.wikipedia.org/wiki/{country.replace(' ', '_')})"
    )
    capital = first.text_input("", "", key=st.session_state["questions"])
    if capital != st.session_state["last"] and capital != "":
        st.session_state["last"] = capital
        st.session_state["questions"] += 1
        st.session_state["capital"] = capital
        if check_distance(europe[country], st.session_state["capital"]) < 5:
            st.session_state["countries"].remove(country)
            st.session_state["right"] += 1
            st.session_state["number"] -= 1
            if st.session_state["number"] == -1:
                perc = st.session_state["right"] * 100 / st.session_state["questions"]
                second.write(
                    f"Du kennst alle Hauptstädte in Europa (ɔ °0°)ɔ  und hast {st.session_state['right']} von {st.session_state['questions']} Fragen richtig beantwortet ({int(round(perc,0))} Prozent)."
                )
                second.write(f"Das ist {grade(perc)}")
                reset()
            else:
                second.write(f"{europe[country]} ist richtig. (✿^‿^)")
                second.write(
                    f"{st.session_state['right']} von {st.session_state['questions']} (Noch {str(st.session_state['number']+1)} Länder)"
                )

        else:
            st.session_state["wrong"] += 1
            second.write(
                f"'{capital}' ist falsch. (ɔ •︵•)ɔ  Die Hauptstadt von {country} ist: {europe[st.session_state['country']]}"
            )
            second.write(
                f"{st.session_state['right']} von {st.session_state['questions']} (Noch {str(st.session_state['number']+1)} Länder)"
            )


def quit():
    try:
        perc = st.session_state["right"] * 100 / st.session_state["questions"]
    except:
        perc = 0
    second.write(
        f"Du hast {st.session_state['right']} von {st.session_state['questions']} Fragen richtig beantwortet ({int(round(perc,0))} Prozent)."
    )
    second.write(f"Das ist {grade(perc)}")
    reset()


if end:
    quit()

if start:
    new()

if next:
    new()


#########################################################################
if __name__ == "__main__":
    main()
