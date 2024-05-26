import google.generativeai as genai
from streamlit_lottie import st_lottie
import streamlit as st
import json
from PIL import Image

input_prompt_analyze = """
You are an expert nutritionist where you need to see the food items from the image and
calculate the estimated total calories. Also provide the details of every food items with estimated calories intake
in tabular format with column names as 'Items list', 'Calories' and each row contains details
of items and estimated calories in their respective columns

Finally, you can also mention whether the food is healthy or not and also mention the
approximate percentage split of the ratio of carbohydrates, fats, fibers, sugar and other important things
required in our diet in tabular format.

In case if the image is not related to food item, mention that and don't take any further steps
"""

input_prompt_recipe = """
You are an expert nutritionist where you need to see the food items from the image and
share the food recipe step by step. If food does not look healthy to you, mention so but also provide the step by 
step recipe.

In case if the image is not related to food item, mention that and don't take any further steps.
"""

input_prompt_diet = """
You are an expert nutritionist. Purpose a diet plan based on given inputs of food items and per day caloric intake. 
Diet plan should include diet for Breakfast, Lunch and Dinner and should include only the food items provided as input.
Also, estimated caloric intake should not exceed the per day calorie provided as input.

"""

if "prompt_activation" not in st.session_state:
    st.session_state.prompt_activation = False
if "image" not in st.session_state:
    st.session_state.image = None


# Function for API configuration at sidebar
def sidebar_api_key_configuration():
    st.sidebar.subheader("API Keys")
    api_key = st.sidebar.text_input("Enter your API Key 🗝️", type="password",
                                    help='Get API Key from: https://aistudio.google.com/app/apikey')
    if api_key == '':
        st.sidebar.warning('Enter the API Key 🗝️')
        st.session_state.prompt_activation = False
    elif api_key.startswith('AI') and (len(api_key) == 39):
        st.sidebar.success('Lets Proceed!', icon='️👉')
        st.session_state.prompt_activation = True
    else:
        st.sidebar.warning('Please enter the correct API Key 🗝️!', icon='⚠️')
        st.session_state.prompt_activation = False
    return api_key


# Function to select diet options
def sidebar_food_calorie_configuration():
    st.sidebar.subheader("Diet Options")
    diet_options = st.sidebar.multiselect('Select the Food items', ['Fruits', 'Vegetables', 'Lentils', 'Eggs', 'Meat'],
                                          disabled=not st.session_state.prompt_activation)
    calorie_intake = st.sidebar.number_input('Enter the Calorie Intake', value=1000, min_value=500, max_value=5000,
                                             step=50)
    return diet_options, calorie_intake


# Function for image loader configuration at sidebar
def sidebar_image_uploader():
    st.sidebar.header("Upload Image")
    uploaded_file = st.sidebar.file_uploader("Upload an image of Food", type=["jpg", "jpeg", "png"],
                                             disabled=not st.session_state.prompt_activation)
    image = ""
    if uploaded_file is not None:
        st.session_state.image = Image.open(uploaded_file)
        st.sidebar.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)
    return uploaded_file


# Function to load and display the lottie file
def display_lottiefile(filename):
    # Load the lottie file
    with open(filename, "r") as f:
        lottie_file = json.load(f)
    st_lottie(lottie_file, speed=1, reverse=False, loop=True, quality="high", height=200, width=400, key=None)


# Function to get the list of available gemini models
def get_gemini_model_list():
    model_list = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_list.append(m.name)
    return model_list


# Function to convert the image into format support by gemini model
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Function to get the response from gemini model with image as the input
def get_gemini_response_image(uploaded_file, selection, api_key):
    genai.configure(api_key=api_key)
    image = input_image_setup(uploaded_file)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    input_prompt = ''
    if selection == 'Analyze':
        input_prompt = input_prompt_analyze
    elif selection == 'Recipe':
        input_prompt = input_prompt_recipe
    response = model.generate_content([input_prompt, image[0]])
    return response.text


# Function to get the response from gemini model with text as the input
def get_gemini_response(diet_plan, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content([input_prompt_diet, diet_plan])
    return response.text
