# Import from standard library
import os
import logging
from dataclasses import dataclass

# Import from 3rd party libraries
import streamlit as st

import agents
from agents import rewrite_in_style
from fakeyou import FakeYou

fakeyou_api = FakeYou()

def generate_description(prompt, style):
    return agents.rewrite_in_style(prompt=prompt, style=style)

def generate_review(prompt, style):
    return agents.give_feedback(prompt=prompt, style=style)


def generate_dialogue(prompt, copywriter, reviewer):
    writer_output = generate_description(prompt, copywriter)
    reviewer_output = generate_review(writer_output, reviewer)

def generate_audio(prompt, copywriter, reviewer):

    if prompt == "":
        # st.session_state.text_error = "Please enter a prompt."
        # return
        prompt = placeholder_prompt

    with text_spinner_placeholder:
        with st.spinner("Generating the writer output..."):
            writer_output = generate_description(prompt, copywriter)

            wav = fakeyou_api.say(text=writer_output, tts_model_token=voices[copywriter])
            audio_path = wav.save()

            if audio_path != "":
                st.session_state.conversation.append((copywriter, writer_output, audio_path))

            logging.info("copy: " + writer_output)
            # st.session_state.conversation.append = audio_text

    with text_spinner_placeholder_2:
        with st.spinner("Generating the review..."):

            reviewer_output = generate_review(writer_output, reviewer)
            logging.info("feedback: " + reviewer_output)

            wav = fakeyou_api.say(text=reviewer_output, tts_model_token=voices[reviewer])
            audio_path = wav.save()

            if audio_path != "":
                st.session_state.conversation.append((reviewer, reviewer_output, audio_path))

                # logging.info("conversation: \n" + "\n".join(st.session_state.conversation))



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

placeholder_prompt = "A beach property on the West coast with a hot tub and a golden toilet."

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Configure Streamlit page and state
st.set_page_config(page_title="Vacasa Copywriters", page_icon=":bath:")


# Store the initial value of widgets in session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "copywriter" not in st.session_state:
    st.session_state.copywriter = ""

if "reviewer" not in st.session_state:
    st.session_state.reviewer = ""

if "narrator" not in st.session_state:
    st.session_state.narrator = ""

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



col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.copywriter = st.selectbox('Copywriter', (name for name in voices))

with col2:
    st.session_state.reviewer = st.selectbox('Reviewer', (name for name in voices))

with col3:
    st.session_state.narrator = st.selectbox('Narrator', (name for name in voices))


# textarea
prompt = st.text_area(label="Unit description", placeholder=f"Ex: {placeholder_prompt}", height=100)


par1, par2, par3, par4 = st.columns(4)
with par1:
    param1 = st.text_input(label="Location", placeholder="West coast")

with par2:
    param2 = st.text_input(label="Size", placeholder="Huge")

with par3:
    param3 = st.text_input(label="Amenities", placeholder="Hot tub and golden toilet")

with par4:
    param4 = st.text_input(label="City", placeholder="LA")

# button
st.button(
    label="Generate",
    help="Click to generate audio",
    key="generate_audio",
    type="primary",
    on_click=generate_audio,
    args=(prompt, st.session_state.copywriter, st.session_state.reviewer),
)


text_spinner_placeholder = st.empty()
text_spinner_placeholder_2 = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.conversation:
    for name, message, output_file_path in st.session_state.conversation:
        # st.markdown("""---""")
        st.subheader(name)
        # st.text_area(label="You may read the result while the audio is being generated.", value=message, )

        with open(output_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        # st.text(st.session_state.reviewer)
        st.audio(audio_bytes, format='audio/mp3', start_time=0)