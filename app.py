from ctypes import alignment
from tkinter import CENTER
from turtle import width
import matplotlib.colors as mcolors
import gensim
import gensim.corpora as corpora
from operator import index
from wordcloud import WordCloud
from pandas._config.config import options
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import Similar
from PIL import Image
import time
import os
import smtplib
from dotenv import load_dotenv
import streamlit.components.v1 as components
import base64

#image = Image.open('Images//he.png')
#st.image(image,width= 550)

st.title("HIRE EASY")


# Reading the CSV files prepared by the fileReader.py
Resumes = pd.read_csv('Resume_Data.csv')
Jobs = pd.read_csv('Job_Data.csv') 


############################### JOB DESCRIPTION CODE ######################################
# Checking for Multiple Job Descriptions
# If more than one Job Descriptions are available, it asks user to select one as well.
if len(Jobs['Name']) <= 1:
    st.write(
        "There is only 1 Job Description present. It will be used to create scores.")
else:
    st.write("There are ", len(Jobs['Name']),
             "Job Descriptions available. Please select one.")


# Asking to Print the Job Desciption Names
if len(Jobs['Name']) > 1:
    option_yn = st.selectbox(
        "Show the      Job Description Names?", options=['YES', 'NO'])
    if option_yn == 'YES':
        index = [a+1 for a in range(len(Jobs['Name']))]
        fig = go.Figure(data=[go.Table(header=dict(values=["Job No.", "Job Desc. Name"], line_color='white',
                                                   fill_color='#050b4a'),
                                       cells=dict(values=[index, Jobs['Name']], line_color='white',
                                                  fill_color='#132b4a'))
                              ])
        fig.update_layout(width=700, height=400)
        st.write(fig)


# Asking to chose the Job Description
index = st.slider("Which JD to select ? : ", 1,
                  len(Jobs['Name']), 1)


option_yn = st.selectbox("Show the Job Description ?", options=['YES', 'NO'])
if option_yn == 'YES':
    st.markdown("---")
    st.markdown("### Job Description :")
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Job Description"],
                    fill_color='#0b2430',
                    align='center', font=dict(color='white', size=16)),
        cells=dict(values=[Jobs['Context'][index-1]],
                   fill_color='#13384a',
                   align='left'))])

    fig.update_layout(width=700, height=600)
    st.write(fig)

#################################### SCORE CALCUATION ################################
@st.cache()

def calculate_scores(resumes, job_description):

    scores = []
    for x in range(resumes.shape[0]):
        with open("a.txt", "w", encoding="utf-8") as f:
            f.write(str(resumes['Skills'][x])+"\n")
    
        with open('b.txt', 'w', encoding="utf-8") as g:
            g.write(str(job_description['Skills'][index-1]) + "\n\n")
    
        with open("a.txt", "r", encoding="utf-8") as f:
            resume_skills = f.read()
    
        with open("b.txt", "r", encoding="utf-8") as g:
            job_skills = g.read()
    
        score = Similar.matchLSA(resume_skills, job_skills)
        scores.append(score)

    return scores


Resumes['Scores'] = calculate_scores(Resumes, Jobs)

Ranked_resumes = Resumes.sort_values(
    by=['Scores'], ascending=False).reset_index(drop=True)

Ranked_resumes['Rank'] = pd.DataFrame(
    [i for i in range(1, len(Ranked_resumes['Scores'])+1)]) 

###################################### SCORE TABLE PLOT ####################################

fig1 = go.Figure(data=[go.Table(
    header=dict(values=["Rank", "Name", "Email", "Scores"],
                fill_color='#00416d',
                align='center', font=dict(color='white', size=16)),
    cells=dict(values=[Ranked_resumes.Rank, Ranked_resumes.Name, Ranked_resumes.Email, Ranked_resumes.Scores],
               fill_color='#122545',
               align='left'))])

fig1.update_layout(title="Top Ranked Resumes", width=700, height=1100)
st.write(fig1)

st.markdown("---")

fig2 = px.bar(Ranked_resumes,
              x=Ranked_resumes['Name'], y=Ranked_resumes['Scores'], color='Scores',
              color_continuous_scale='haline', title="Score and Rank Distribution")
fig2.update_layout(width=700, height=700)
st.write(fig2)

st.markdown("---")

############################################ TF-IDF Code ###################################


@st.cache()
def get_list_of_words(document):
    Document = []
    for a in document:
        if isinstance(a, float):
            a = str(a)
        raw = a.split(" ")
        Document.append(raw)
    return Document

document = get_list_of_words(Resumes['Skills'])

id2word = corpora.Dictionary(document)
corpus = [id2word.doc2bow(text) for text in document]


lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=6, random_state=100,
                                            update_every=3, chunksize=100, passes=50, alpha='auto', per_word_topics=True)

################################### LDA CODE ##############################################


@st.cache  # Trying to improve performance by reducing the rerun computations
def format_topics_sentences(ldamodel, corpus):
    sent_topics_df = []
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df.append(
                    [i, int(topic_num), round(prop_topic, 4)*100, topic_keywords])
            else:
                break

    return sent_topics_df


################################# Topic Word Cloud Code #####################################
# st.sidebar.button('Hit Me')
st.markdown("## Topics and Topic Related Keywords ")
st.markdown(
    """This Wordcloud representation shows the Topic Number and the Top Keywords that constitute a Topic.
    This further is used to cluster the resumes.      """)

cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]

cloud = WordCloud(background_color='white',
                  width=2500,
                  height=1800,
                  max_words=10,
                  colormap='tab10',
                  collocations=False,
                  color_func=lambda *args, **kwargs: cols[i],
                  prefer_horizontal=1.0)

topics = lda_model.show_topics(formatted=False)

fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=True, sharey=True)

for i, ax in enumerate(axes.flatten()):
    fig.add_subplot(ax)
    topic_words = dict(topics[i][1])
    cloud.generate_from_frequencies(topic_words, max_font_size=300)
    plt.gca().imshow(cloud)
    plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
    plt.gca().axis('off')


plt.subplots_adjust(wspace=0, hspace=0)
plt.axis('off')
plt.margins(x=0, y=0)
plt.tight_layout()
st.pyplot(plt)

st.markdown("---")

###################### SETTING UP THE DATAFRAME FOR SUNBURST-GRAPH ############################

df_topic_sents_keywords = format_topics_sentences(
    ldamodel=lda_model, corpus=corpus)
df_some = pd.DataFrame(df_topic_sents_keywords, columns=[
                       'Document No', 'Dominant Topic', 'Topic % Contribution', 'Keywords'])
df_some['Names'] = Resumes['Name']

df = df_some

st.markdown("## Topic Modelling of Resumes ")
st.markdown(
    "Using LDA to divide the topics into a number of usefull topics and creating a Cluster of matching topic resumes.  ")
fig3 = px.sunburst(df, 
                   path=['Dominant Topic', 'Names'], 
                   values='Topic % Contribution',
                   color='Dominant Topic', 
                   color_continuous_scale='viridis', 
                   width=800, 
                   height=800, 
                   title="Topic Distribution Graph",
                   labels={'Dominant Topic': ''}
                  )
st.write(fig3)


############################# RESUME PRINTING #############################

option_2 = st.selectbox("Show the Best Matching Resumes?", options=[
    'YES', 'NO'])
if option_2 == 'YES':
    indx = st.slider("Which resume to display ?:",
                     1, Ranked_resumes.shape[0], 1)

    st.write("Displaying Resume with Rank: ", indx)
    
    # get the email of the best matched resume
    email = Ranked_resumes.iloc[indx-1, 3]
    
    st.markdown("---")
    st.markdown("## **Resume** ")
    value = Ranked_resumes.iloc[indx-1, 2]
    st.markdown("#### The Word Cloud For the Resume")
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          colormap='viridis', collocations=False,
                          min_font_size=10).generate(value)
    plt.figure(figsize=(7, 7), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(plt)

    st.write("With a Match Score of :", Ranked_resumes.iloc[indx-1, 4])
    
    # print the email of the best matched resume
    st.write("Best Matched Resume Email: ", email)

    # Set up the email message
    to_address = email
    subject = 'Best Matched Resume'
    body = 'Hello,\n\nYou have been selected for the interview. Please contact for further information.\n\nThank you,\nHire Easy'
    message = f'Subject: {subject}\n\n{body}'

    # Set up the email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    load_dotenv('.env')

    sender_email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    # Define a function to send the email
    def send_email():
        # Log in to the email server
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, to_address, message)

        # Close the connection to the email server
        server.quit()

    # Add a button to send the email
    if st.button('Send email'):
        send_email()
        st.write('Email sent to:', email)


##################### display resume ########################

# Set the default index to 0

# inds = 1

# Create a slider to select the resume to display
# resume_num = st.slider("Select a resume to display", 1, len(Ranked_resumes))

# # Update the indx variable based on the selected resume
# inds = resume_num - 1

# Get the file extension of the selected resume
top_filename = Ranked_resumes.iloc[indx-1, 0]
extension = os.path.splitext(top_filename)[1]

# Display the selected resume

def show_pdf(folder_name, file_name):
    current_dir = os.path.abspath(os.getcwd())
    file_path = os.path.join('Data', 'Resumes', file_name)
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

@st.cache(suppress_st_warning=True)
def show_docx(folder_name, file_name):
    file_path = os.path.join('Data', 'Resumes', file_name)
    with open(file_path, 'rb') as f:
        base64_docx = base64.b64encode(f.read()).decode('utf-8')
    docx_display = f'<iframe src="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_docx}" width="800" height="800" type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"></iframe>'
    st.markdown(docx_display, unsafe_allow_html=True)

if extension == ".pdf":
    show_pdf('Resumes', top_filename)
elif extension == ".docx":
    show_docx('Resumes', top_filename)