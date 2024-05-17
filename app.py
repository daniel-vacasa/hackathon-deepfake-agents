# Import from standard library
import os
import logging
from dataclasses import dataclass

# Import from 3rd party libraries
import streamlit as st

from agents import get_response
from fakeyou import FakeYou

fakeyou_api = FakeYou()

def generate_audio_text(prompt, style):
    return get_response(prompt=prompt, style=style)


def generate_audio(prompt, style):

    if prompt == "":
        st.session_state.text_error = "Please enter a prompt."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process the text..."):
            audio_text = generate_audio_text(prompt=prompt, style=style)

            st.session_state.audio_text = audio_text

    with text_spinner_placeholder_2:
        with st.spinner("Please wait while we generate the audio..."):

            if st.session_state.input_file_path != "":
                # audio_path = with_custom_voice(podcaster=podcaster, guest=guest, description=prompt, prompt=st.session_state.podcast_generate, file_path=st.session_state.input_file_path)
                audio_path = "not_implemented"

                if audio_path != "":
                    st.session_state.output_file_path = audio_path

            else:

                wav = fakeyou_api.say(text=st.session_state.audio_text, tts_model_token=voices[style])
                audio_path = wav.save()

                if audio_path != "":
                    st.session_state.output_file_path = audio_path


@dataclass
class Voice:
    name: str
    fakeyou_id: str


voices = {
    "Trump": "weight_cg6heneq0rmkas3qj7ccz0t0r",  # version 3
    "Yoda": "weight_tqpbyrp6t9rmdez9c38zzvp0z",
    "Darth Vader": "weight_cybz3j5kwmsmejb0qfx0dwrr9",
    "C-3PO": "weight_mw6a4360jp2pw23490ddv9z9r",
    "Snoop Dogg": "weight_mqppqpwm7pp8sbpnewy94pjtq",
    "Gordon Ramsey": "weight_hzmpgtkc7mryw5pw3ytf8vxdb",
    "Hal 9000": "weight_5cbvjhp2tsk498f1hq53gq0ew",
    "Jar Jar Binks": "weight_9409hbznp60n6w7ey9f6qw5bh",
    "Joe Biden": "weight_w8f5x9hjwbx6vrfa84sxpntyv",
    "John Cena": "weight_xv98cfyw6rbrbye91bg169w1q",
    "John Oliver": "weight_nex5rhe1ft9vkqzjavgtaz5a0",
    "Johnny Cash": "weight_ntcdscgty22mr3ehd7y21n7cm",
    "Morpheus (The Matrix)": "weight_an4jah6zatpjf4z64hc1faatb",
    "Michael Jackson (singing)": "weight_y0qwsbmqscnqhp5m512hawgc3",
    "Morgan Freeman": "weight_31ewdsvev9bttgb4eg7zy7mj5",
    "Patrick Stewart": "weight_hqba2h55yyyq7kgfx7rgnd2xf",
    "Sam Altman": "weight_j17er7ftf16f37s06s357txhf",
    "Saul Goodman": "weight_f4av238kbadw9h258v1cq1mxw",
    "Sicilian Electrician": "weight_1ptwk6pa8krh3ykfr7rztf3pz",
    "Sir David Attenborough": "weight_bc0tjv6fs7c1ccrtw8mbwxay5",
    "Tony Soprano": "weight_ae78yn7st5s7hfk2jbzk9143g",
    "Amy Lee (Evanescence)": "weight_tmrsxs94sqh0x6faxzxx25v4d",
    "Anna (Frozen)": "weight_z9cjmvy1zm16gq8q563rd0xvy",
    "Arnold Schwarzenegger": "weight_j507a0kxad8dk7tyxt9zkfq5e",
    "Barack Obama": "weight_8f3r8hwt0j58j68ayzzfgsh8h",
    "Barbie": "weight_rn0w1p2cedqd61jtm7ns680b6",
    "Darth Sidious": "weight_06adtw47kdgw6zzpkcttz733m",
    "Frank Sinatra": "weight_57z4cqj0v00ft34hzy6bt2ksy",
}

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Configure Streamlit page and state
st.set_page_config(page_title="Vacasa Copywriters", page_icon=":bath:")


# Store the initial value of widgets in session state
if "audio_text" not in st.session_state:
    st.session_state.audio_text = ""

if "output_file_path" not in st.session_state:
    st.session_state.output_file_path = ""

if "input_file_path" not in st.session_state:
    st.session_state.input_file_path = ""

if 'text_error' not in st.session_state:
    st.session_state.text_error = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"


# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Render Streamlit page


# title of the app
st.title(":superhero: Vacasa Copywriting Department")


# brief description of the app
st.markdown(
    "Give us a unit description and the all-star Vacasa agents team will turn it into a personalized high-quality marketing operation."
)


# header
# st.header("This is a demo of the Eleven Labs + Langchain Tutorial")


# # file upload if you want to use custom voice
# file = st.file_uploader(label="Upload file", type=["mp3",])
# if file is not None:
#     filename = "sample.mp3"
#     with open(filename, "wb") as f:
#         f.write(file.getbuffer())
#     st.session_state.input_file_path = "sample.mp3"


# selectbox
voice = st.selectbox('Choose your voice', (name for name in voices))


# col1, col2 = st.columns(2)
#
# with col1:
#     podcaster = st.text_input(label="Podcaster", placeholder="Ex. Lex Fridman")
#
# with col2:
#     guest = st.text_input(label="Guest", placeholder="Ex. Elon Musk")
#


# textarea
prompt = st.text_area(label="Unit description", placeholder="Ex: A riverside property on the West coast with a hot tub and a golden toilet.", height=100)


# button
st.button(
    label="Generate audio",
    help="Click to generate audio",
    key="generate_audio",
    type="primary",
    on_click=generate_audio,
    args=(prompt, voice),
)


text_spinner_placeholder = st.empty()
text_spinner_placeholder_2 = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.audio_text:
    st.markdown("""---""")
    st.subheader("Read Audio")
    st.text_area(label="You may read the result while the audio is being generated.", value=st.session_state.audio_text, )


if st.session_state.output_file_path:
    st.markdown("""---""")
    st.subheader("Listen to Audio")

    with open(st.session_state.output_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3', start_time=0)