
import streamlit as st
from db_helper import init_db, get_random_word, get_categories

init_db()
categories = get_categories()

st.set_page_config(page_title=" Hangman auf Deutsch", page_icon="🎮")
st.title("🎮 Deutsch-Hangman")
st.write("### Lass uns das Wortspiel genießen!")

st.subheader("Wähle eine Kategorie aus!")

# Um die Daten zwischen verschiedenen Interaktionen in Streamlit zu speichern, benutze ich session_state

if "secret_word" not in st.session_state:

    if "stats" not in st.session_state:
        st.session_state.stats = {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "total_attempts": 0
        }

    st.session_state.selected_category = 1
    st.session_state.secret_word = get_random_word(
        st.session_state.selected_category)
    st.session_state.hidden_word = ["_"] * len(st.session_state.secret_word)
    st.session_state.guessed_letters = set()
    st.session_state.wrong_attempts = 0
    st.session_state.word_guessed = False
    st.session_state.max_attempts = 6
    st.session_state.message = ""

with st.sidebar:
    st.header("📊 Spielstatistik")
    if "stats" in st.session_state:
        stats = st.session_state.stats
        st.write(f"Gesamtspiele: {stats['total_games']}")
        st.write(f"🏆 Siege: {stats['wins']}")
        st.write(f"💀 Niederlagen: {stats['losses']}")
        st.write(f"🎯 Versuche gesamt: {stats['total_attempts']}")

        if stats['total_games'] > 0:
            win_rate = (stats['wins'] / stats['total_games']) * 100
            st.metric("Gewinnrate", f"{win_rate:.1f}%")
        else:
            st.write("Gewinnrate: 0%")
    else:
        st.write("Statistik wird initialisiert...")


def reset_game():
    st.session_state.secret_word = get_random_word(
        st.session_state.selected_category)
    st.session_state.hidden_word = ["_"] * len(st.session_state.secret_word)
    st.session_state.guessed_letters = set()
    st.session_state.wrong_attempts = 0
    st.session_state.word_guessed = False
    st.session_state.message = ""


col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Die Natur 🌳"):
        st.session_state.selected_category = 1
        reset_game()

with col2:
    if st.button("Data Science 💻"):
        st.session_state.selected_category = 2
        reset_game()

with col3:
    if st.button("Technik ⚙️"):
        st.session_state.selected_category = 3
        reset_game()

st.write(
    f"Aktuelle Kategorie: **{categories[st.session_state.selected_category]}**")


def process_guess():

    guess = st.session_state.guess_input.strip().upper()

    if not guess:
        return

    st.session_state.guess_input = ""

    # Erlaubte Symbole
    valid_german_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß")

    if not all(char in valid_german_chars for char in guess):
        st.session_state.message = "❌ Ungültige Zeichen! Nur deutsche Buchstaben erlaubt (A-Z, Ä, Ö, Ü, ß)"
        return

    st.session_state.stats["total_attempts"] += 1

    if guess == st.session_state.secret_word:
        st.session_state.hidden_word = list(st.session_state.secret_word)
        st.session_state.word_guessed = True
        st.session_state.message = "🎯 Richtiges Wort! Du hast gewonnen!"
    elif len(guess) > 1:
        st.session_state.wrong_attempts = st.session_state.max_attempts
        st.session_state.message = "❌ Falsches Wort!"
    else:
        letter = guess[0]
        if letter in st.session_state.guessed_letters:
            st.session_state.message = "🔁 Schon geraten."
            return

        st.session_state.guessed_letters.add(letter)
        if letter in st.session_state.secret_word:
            for i, l in enumerate(st.session_state.secret_word):
                if l == letter:
                    st.session_state.hidden_word[i] = letter
            st.session_state.message = "✅ Richtig!"
            if "_" not in st.session_state.hidden_word:
                st.session_state.word_guessed = True
                st.session_state.message = "🎉 Du hast gewonnen!"
        else:
            st.session_state.wrong_attempts += 1
            st.session_state.message = "❌ Falsch!"

    if st.session_state.word_guessed:
        st.session_state.stats["wins"] += 1
        st.session_state.stats["total_games"] += 1
    elif st.session_state.wrong_attempts >= st.session_state.max_attempts:
        st.session_state.stats["losses"] += 1
        st.session_state.stats["total_games"] += 1


game_over = st.session_state.word_guessed or st.session_state.wrong_attempts >= st.session_state.max_attempts


with st.form("guess_form"):
    st.text_input("❓ Rate einen Buchstaben oder das ganze Wort:",
                  key="guess_input",
                  max_chars=20,
                  disabled=game_over)
    st.form_submit_button(
        "Absenden", on_click=process_guess, disabled=game_over)


def show_hangman(state):
    stages = [
        "________\n|      |\n|\n|\n|\n|",
        "________\n|      |\n|      0\n|\n|\n|",
        "________\n|      |\n|      0\n|     /\n|\n|",
        "________\n|      |\n|      0\n|     /|\n|\n|",
        "________\n|      |\n|      0\n|     /|\\\n|\n|",
        "________\n|      |\n|      0\n|     /|\\\n|     /\n|",
        "________\n|      |\n|      0\n|     /|\\\n|     / \\\n| 💀 DU HAST VERLOREN"
    ]
    st.text(stages[min(state, 6)])


show_hangman(st.session_state.wrong_attempts)

progress = st.session_state.wrong_attempts / st.session_state.max_attempts
st.progress(progress)
st.caption(
    f"Verbleibende Versuche: {st.session_state.max_attempts - st.session_state.wrong_attempts}")

st.markdown(
    f"**Wort:** {' '.join(st.session_state.hidden_word)}   besteht aus {len(st.session_state.secret_word)} Buchstaben")
st.write(
    f"❌ Fehlversuche: {st.session_state.wrong_attempts} / {st.session_state.max_attempts}")
st.markdown(
    f"**Geratene Buchstaben:** {', '.join(sorted(st.session_state.guessed_letters))}")


if st.session_state.message:
    if "gewonnen" in st.session_state.message:
        st.balloons()
        st.success(st.session_state.message)
    else:
        st.write(st.session_state.message)

if game_over:
    if st.session_state.word_guessed:
        st.success(
            f"🎉 Gewonnen! Das Wort war **{st.session_state.secret_word}**")
    else:
        st.error(
            f"💀 Verloren! Das Wort war **{st.session_state.secret_word}**")

    if st.button("🔁 Neue Runde starten"):
        reset_game()
        st.session_state.message = ""  # Sicherheitshalber
        st.rerun()
