import streamlit as st
import fsspec
from pathlib import Path
import os, random, json, datetime





if st.button("Submit Rankings"):
    #Check if each rating has a different value
    
    # Build a dict of image names to ratings
    
    # Convert to JSON string
    #json_data = json.dumps(image_ratings,indent=4)

    #Create divider and display json data of this current run
    #Prompt User to Enter their Name & Gender

    st.divider()
    st.code(json.dumps(st.session_state['history'],indent=4),language='json')
    #TODO: Fix so that this link to my email actually goes to my email
    st.success("Thanks! Your ratings for this session are listed below! Make sure to copy this and send it to [Ndiana Obot's Email](www.ndianaobot8@gmail.com) .")
    if st.button("Complete Survey Again"):
        # Clear the session state and reload the page
        st.session_state['reset_images'] = True
        st.session_state['ratings'] = [0, 0, 0, 0, 0]
        st.rerun()

def append_to_history(image_ratings) -> list:
    if 'history' not in st.session_state:
        st.session_state['history'] = [] 
        st.session_state['history'].append(image_ratings)
    else:
        st.session_state['history'].append(image_ratings)
    return st.session_state['history']

def construct_ratings_dictionary(random_images:list,ratings:list) -> list:
    image_ratings = {
        image_path.name: ratings[i] for i, image_path in enumerate(random_images)
    }
    image_ratings['timestamp'] = str(datetime.datetime.now())
    image_ratings['name'] = st.session_state['name']
    return image_ratings


def ensure_diff_ratings(ratings:list) -> bool:
    if(len(set(ratings)) != len(ratings)):
        st.error("Please make sure each rating is different.")
        st.stop()
    return len(set(ratings)) != len(ratings)

def display_images(random_images:list) -> list:
    #Display the Images in a grid & returns a list of the ratings
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    ratings = st.session_state.get('ratings', [0, 0, 0, 0, 0])
    with col1:
        print("debug -- this is running")
        st.image(random_images[0],   use_container_width=True)
        ratings[0] = st.number_input( "Image 1", min_value=1, max_value=5, step=1, key="image_rating_1")
        
    with col2:
        st.image(random_images[1],   use_container_width=True)
        ratings[1] = st.number_input( "Image 2", min_value=1, max_value=5, step=1, key="image_rating_2")
        
    with col3:
        st.image(random_images[2],   use_container_width=True)
        ratings[2] = st.number_input( "Image 3", min_value=1, max_value=5, step=1, key="image_rating_3")
        
    with col4:      
        st.image(random_images[3],   use_container_width=True)
        ratings[3] = st.number_input( "Image 4", min_value=1, max_value=5, step=1, key="image_rating_4")
        
    with col5:      
        st.image(random_images[4],   use_container_width=True)
        ratings[4] = st.number_input( "Image 5", min_value=1, max_value=5, step=1, key="image_rating_5")

    return ratings



#selects psuedo-random images and returns their names as a list
def select_images() -> list:
    #Pick Random Image from Sample_Images Folder if not already done in previous Run
    sample_images_path = Path("Sample_Images")
    sample_images = list(sample_images_path.glob("*.jpg")) + list(sample_images_path.glob("*.png"))
    #Pick 5 random images`` from the list
    random_images = []
    for i in range(5):
        rand_index = random.randint(0, len(sample_images)-1)
        print(f"rIndex:{rand_index}")
        random_images.append(sample_images.pop(rand_index))# Remove from list -- Avoiding Duplicate
    return random_images


#loads static parts of the webpage
def load_static():
    st.title("Relative Roughness Survey")
    st.write("This is a survey to collect data on the relative roughness of the surface of the images.\n Rank each of the images from 1 to 5, where 1 is the lowest and 5 is the highest relative roughness.")
    st.write("We thank you for your participation!")


def main():
    load_static()
    

    if st.button("Submit Rankings"):

if __name__ == '__main__': 
    main()