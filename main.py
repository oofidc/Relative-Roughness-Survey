import streamlit as st
import fsspec
from pathlib import Path
import os, random, json, datetime

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
    return image_ratings


def ensure_diff_ratings(ratings:list) -> bool:    
    return len(set(ratings)) == len(ratings)

def display_images(random_images:list) -> tuple:
    #Display the Images in a grid & returns a list of the ratings
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    ratings = st.session_state.get('ratings', [0, 0, 0, 0, 0])
    st_imgs = []
    with col1:
        print("debug -- this is running")
        st_imgs.append(st.image(random_images[0],   use_container_width=True))
        ratings[0] = st.number_input( "Image 1", min_value=1, max_value=5, step=1, key="image_rating_1")
        
    with col2:
        st_imgs.append(st.image(random_images[1],   use_container_width=True))
        ratings[1] = st.number_input( "Image 2", min_value=1, max_value=5, step=1, key="image_rating_2")
        
    with col3:
        st_imgs.append(st.image(random_images[2],   use_container_width=True))
        ratings[2] = st.number_input( "Image 3", min_value=1, max_value=5, step=1, key="image_rating_3")
        
    with col4:      
        st_imgs.append(st.image(random_images[3],   use_container_width=True))
        ratings[3] = st.number_input( "Image 4", min_value=1, max_value=5, step=1, key="image_rating_4")
        
    with col5:      
        st_imgs.append(st.image(random_images[4],   use_container_width=True))
        ratings[4] = st.number_input( "Image 5", min_value=1, max_value=5, step=1, key="image_rating_5")

    return ratings, st_imgs



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

def reload_form():
    rand_images = select_images()
    st.session_state['random_images'] = rand_images  # <-- update session state
    ratings = [0, 0, 0, 0, 0]
    st.session_state['ratings'] = ratings
    ratings, st_imgs = display_images(rand_images)
    await_submission(ratings, rand_images)

def await_submission(ratings, rand_images):
    if st.button("Submit Rankings"):
        if not ensure_diff_ratings(ratings):
            st.error("Please make sure each rating is different.")
            st.stop()
        ratings_dict = construct_ratings_dictionary(rand_images, ratings)
        history = append_to_history(ratings_dict)
        st.divider()
        st.code(json.dumps(history, indent=4), language='json')
        st.success("Thanks! Your ratings for this session are listed below! Make sure to copy this and send it to [Ndiana Obot's Email](mailto:ndianaobot8@gmail.com) .")
        if st.button("Complete Survey Again"):
            reload_form()  # <-- just call reload_form, which resets images and ratings
            
def main():
    load_static()
    if not st.session_state.get('random_images'):
        rand_images = select_images()
        st.session_state['random_images'] = rand_images
    else:
        rand_images = st.session_state['random_images']
    
    ratings, st_imgs = display_images(random_images=rand_images)
    await_submission(ratings,rand_images)
            

        



if __name__ == '__main__': 
    main()