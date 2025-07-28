import time
import streamlit as st
import fsspec
from pathlib import Path
import os, random, json, datetime
from weighted_randomness import weight_randomness



def append_to_history(image_ratings) -> list:
    if 'history' not in st.session_state:
        st.session_state['history'] = [] 
        st.session_state['history'].append(image_ratings)
    else:
        st.session_state['history'].append(image_ratings)
    return st.session_state['history']

def construct_ratings_dictionary(random_images:list,ratings:list) -> dict:
    image_ratings = {
    
        (image_path): ratings[i] for i, image_path in enumerate(random_images)
    }
    image_ratings['timestamp'] = str(datetime.datetime.now())
    return image_ratings

# Ensures different ratings
# Returns True if there are no images rated the same, false if there are
def ensure_diff_ratings(ratings:list) -> bool:    
    return len(set(ratings)) == len(ratings)


# This ensures that all ratings are different, i.e., no duplicates exist in the ratings list
# returns True if this rating is not the same as the previous rating, False otherwise
# This is used to ensure that the user does not rate the same image twice in a row
def ensure_not_duplicate(ratings: dict) -> bool:
    history = st.session_state.get('history', [])
    if len(history) > 0:
        # Remove 'timestamp' from both dicts before comparison
        current = {k: v for k, v in ratings.items() if k != 'timestamp'}
        last = {k: v for k, v in history[-1].items() if k != 'timestamp'}
        return current != last
    return True


def display_images(random_images:list) -> tuple:
    #Display the Images in a grid & returns a list of the ratings
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    ratings = st.session_state.get('ratings', [0, 0, 0, 0, 0])
    st_imgs = []
    with col1:
        #print("debug -- this is running")
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

#generate a random image
def random_image(sample_images:list):
    #Pick Random Image from Sample_Images Folder if not already done in previous Run
    rand_index = random.randint(0, len(sample_images)-1)
    return sample_images[rand_index].name.split('\\')[-1].split('/')[-1]

#selects psuedo-random images and returns their names as a list
def select_images() -> list:
    sample_images_path = Path("Sample_Images")
    sample_images = list(sample_images_path.glob("*.jpg")) + list(sample_images_path.glob("*.png"))

    #Pick 5 random images`` from the list
    #First try to use weighted images but if that doesn't work put up an alert and then use regular random images
    image_randomizer = weight_randomness(st.session_state.get('history',[]),directory='Sample_Images/')
    random_images = image_randomizer.n_random_images(random_image(sample_images), 5)
    if random_images is None:
        st.warning("These images weren't generated with a weighted random chance\n If your name is not Ndiana this isn't really important")
        random_images = []
        for i in range(5):
            rand_index = random.randint(0, len(sample_images)-1)
            #print(f"rIndex:{rand_index}")
            random_images.append(sample_images.pop(rand_index))# Remove from list -- Avoiding Duplicate
    return random_images


#loads static parts of the webpage
def load_static():
    st.title("Relative Roughness Survey")
    st.write("This is a survey to collect data on the relative roughness of the surface of the images.\n Rank each of the images from 1 to 5, where 1 is the lowest and 5 is the highest relative roughness.")
    st.write("Your work will not save if you refresh this page or close the browser, so make sure to save your ratings and send them to Ndiana Obot or upload them to the Google Drive folder first")
    st.write("To submit the survey you can either copy the the json out below and send it to Ndiana Obot over email or click the download button to download the ratings history as a JSON file and share that with Ndiana Obot through Google Drive or through email.")
    st.write("Please ensure that each rating is different. If you have any questions, please contact Ndiana Obot at [ndianaobot8@gmail.com](mailto:ndianaobot8@gmail.com)")
    st.write("We thank you for your participation!")



def await_submission(ratings, rand_images):
    
    if st.button("Get More Images"):
        st.session_state['reload_form'] = True
        st.rerun()
    if st.download_button("Download Ratings History as JSON",
                           data=json.dumps(st.session_state.get('history', []), indent=4),
                           file_name=f'ratings_history_{time.time()}.json',
                           mime='application/json'):
        st.success("Ratings history downloaded successfully!")
    if st.button("Submit Rankings"):
        if not ensure_diff_ratings(ratings):
            st.error("Please make sure each rating is different.")
            st.stop()
        
        ratings_dict = construct_ratings_dictionary(rand_images, ratings)
        #print(f"r_dict:{ratings_dict}")
        if not ensure_not_duplicate(ratings_dict):
            st.error("Duplicate Rating Submission Detected - Generate New Images")
            st.stop()
        history = append_to_history(ratings_dict)
        st.divider()
        st.code(json.dumps(history, indent=4), language='json')
        st.success("Thanks! Your ratings for this session are listed below! Make sure to copy this and send it to [Ndiana Obot's Email](mailto:ndianaobot8@gmail.com) .")
        if len(st.session_state.get('history', [])) > 15:
            st.warning("You have submitted over 15 ratings, please save your ratings history and reload the page to avoid losing your progress.")


            
def main():
    load_static()
    if not st.session_state.get('random_images') or st.session_state.get('reload_form',False):
        rand_images = select_images()
        st.session_state['random_images'] = rand_images
        st.session_state['reload_form'] = False
    else:
        rand_images = st.session_state['random_images']
    
    ratings, st_imgs = display_images(random_images=rand_images)
    await_submission(ratings,rand_images)
            
if __name__ == '__main__': 
    main()