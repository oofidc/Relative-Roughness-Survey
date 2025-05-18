import streamlit as st
import fsspec
from pathlib import Path
import os, random, redis, json, datetime

st.title("Relative Roughness Survey")
st.write("This is a survey to collect data on the relative roughness of the surface of the images.\n Rate each of the imagesfrom 1 to 5, where 1 is the lowest and 5 is the highest relative roughness.")
st.write("We thank you for your participation!")
#Pick Random Image from Sample_Images Folder if not already done in previous Run
if not st.session_state.get('random_images'):
    sample_images_path = Path("Sample_Images")
    sample_images = list(sample_images_path.glob("*.jpg")) + list(sample_images_path.glob("*.png"))
    #Pick 5 random images from the list
    random_images = []
    for i in range(5):
        rand_index = random.randint(0, len(sample_images)-1)
        random_images.append(sample_images.pop(rand_index))# Remove from list -- Avoiding Duplicates
    st.session_state['random_images'] = random_images
else:
    random_images = st.session_state['random_images']

#Prompt User to Enter their Name & Gender
if 'name' not in st.session_state:
    st.session_state['name'] = st.text_input("Enter your name:")
else:
    st.session_state['name'] = st.text_input("Enter your name:", value=st.session_state['name'])

if 'gender' not in st.session_state:
    st.session_state['gender'] = st.selectbox("Select your Gender:", ["Male","Female","None"])
else:
    st.session_state['gender'] = st.selectbox("Select your Gender:", ["Male", "Female", "None"],index=["Male", "Female", "None"].index(st.session_state['gender']) )



    
#Display the Images in a grid
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)
ratings = st.session_state.get('ratings', [0, 0, 0, 0, 0])
with col1:
    st.image(random_images[0],   use_container_width=True)
    ratings[0] = st.number_input( "", min_value=1, max_value=5, step=1, key="image_rating_1")
    
with col2:
    st.image(random_images[1],   use_container_width=True)
    ratings[1] = st.number_input( "", min_value=1, max_value=5, step=1, key="image_rating_2")
    
with col3:
    st.image(random_images[2],   use_container_width=True)
    ratings[2] = st.number_input( "", min_value=1, max_value=5, step=1, key="image_rating_3")
    
with col4:      
    st.image(random_images[3],   use_container_width=True)
    ratings[3] = st.number_input( "", min_value=1, max_value=5, step=1, key="image_rating_4")
    
with col5:      
    st.image(random_images[4],   use_container_width=True)
    ratings[4] = st.number_input( "", min_value=1, max_value=5, step=1, key="image_rating_5")
    


r = redis.Redis(
    host=st.secrets['database']['url'],
    port=st.secrets['database']['port'],
    decode_responses=True,
    username=st.secrets['database']['username'],
    password=st.secrets['database']['password'],
)


if st.button("Submit Rankings"):
    # Build a dict of image names to ratings
    image_ratings = {
        image_path.name: ratings[i]
        for i, image_path in enumerate(random_images)
    }
    image_ratings['timestamp'] = str(datetime.datetime.now())
    image_ratings['name'] = st.session_state['name']
    image_ratings['gender'] = st.session_state['gender']
    # Convert to JSON string
    json_data = json.dumps(image_ratings)

    # Push to Redis list (append at the end)
    r.rpush("survey_results", json_data)

    st.success("Thanks! Your ratings were submitted.")
    if st.button("Complete Survey Again"):
        # Clear the session state and reload the page
        st.session_state['random_images'] = None
        st.session_state['ratings'] = [0, 0, 0, 0, 0]
        st.experimental_rerun()
