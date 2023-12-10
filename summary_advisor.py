import streamlit as st
import openai
import json
import pandas as pd
import base64
import re

#Get the API key from the sidebas called OpenAI API Key
openai.api_key = st.sidebar.text_input("OpenAI API Key", type="password")

client = openai.OpenAI(api_key=openai.api_key)
prompt = """Act as an English native speaker who is great at making a concise summary of a text. 
            You will receive a URL link containing a news article from the user. You should read 
            the article and write a summary of it by using openai.
            The summary should be no longer than 5 sentences and should use B1-level or B2-level words.
            After that, act as a table formatter and format a JSON array containing 10 interesting words in the article.
            Remember that the format of the JSON array is:
            [
                {
                    "Word": "word1",
                    "Definition": "definition1",
                    "Example": "example1"},
                    {"Word": "word2",
                    "Definition": "definition2",
                    "Example": "example2",
                    ...
                }
            ]
            The JSON array should immediately follow the summary above.
            Then, provide the user a download link to download the table as a CSV file.
            Do not say anything at first. Just wait until the user to give you the URL link.
            """

st.title(":rainbow[_English Summary and Vocabulary Recommendation_]:new:")
st.write("**This is a demo of the English Summary and Vocabulary Recommendation. Please enter a URL link below.**:point_down:")
user_input = st.text_area("URL Link", height=25)

# create a summary button
if st.button("Summarize"):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )
    # Show the response from the AI in a box
    st.markdown('**AI response:**')
    suggestion_dictionary = response.choices[0].message.content

    text = suggestion_dictionary
    pattern = r'(.*)(\n+)'
    match = re.search(pattern, text)
    st.markdown(match.group(0))

    text = suggestion_dictionary
    pattern = r'(.*\n\n)'
    replace = r''
    res = re.sub(pattern, replace, text)

    # convert the suggestion dictionary to a dataframe
    sd = json.loads(res)
    suggestion_df = pd.DataFrame.from_dict(sd)
    st.table(suggestion_df)

    st.write("**Download the table as a CSV file.**:100:")
    csv = suggestion_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="summary.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)