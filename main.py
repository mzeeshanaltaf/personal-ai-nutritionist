from streamlit_option_menu import option_menu
from utility import *

# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "AI Nutritionist"
page_icon = "🥗"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

# Display the lottie file
display_lottiefile("nutrition.json")

st.title("Personal AI Nutritionist")
st.write("***See Your Food, Know Your Fuel: Calorie Conscious at a Glance!***")
st.write("***Your Personal AI Nutritionist*** 🥩🥦🥝")

# ---- NAVIGATION MENU -----
selection = option_menu(
    menu_title=None,
    options=["Analyze", "Recipe", "Diet Planner", "About"],
    icons=["bi-boxes", "book", "body-text", "app"],  # https://icons.getbootstrap.com
    orientation="horizontal",
)
if "image" not in st.session_state:
    st.session_state.image = None

# --- SIDEBAR SETUP ---
# Configure the API key
st.sidebar.title("Config️uration Options")
api_key = sidebar_api_key_configuration()

if selection == 'Analyze':
    uploaded_file, st.session_state.image = sidebar_image_uploader()
    st.sidebar.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)
    st.header("Analyze Food")
    st.write("Upload the food image to get the details of food items and caloric intake.")
    submit_analyze = st.button("Analyze", type="primary", disabled=not uploaded_file)

    if submit_analyze:
        with st.spinner("Analyzing ..."):
            response = get_gemini_response_image(uploaded_file, selection, api_key)
            st.write(response)

# If selected menu option is "Recipe"
if selection == 'Recipe':
    uploaded_file = sidebar_image_uploader()
    st.header("Food Recipe")
    st.write("Upload the food image and get the recipe.")
    submit_recipe = st.button("Get Recipe", type="primary", disabled=not uploaded_file)

    if submit_recipe:
        with st.spinner("Generating Recipe..."):
            response = get_gemini_response_image(uploaded_file, selection, api_key)
            st.write(response)

# If selected menu option is "Diet Planner"
if selection == 'Diet Planner':
    diet_options, calorie_intake = sidebar_food_calorie_configuration()
    diet_plan = f"List of food items: {diet_options}. Number of calories per day: {calorie_intake}"
    st.header("Diet Plan")
    st.write("Select the food items and calorie intake to get the customized diet plan.")

    diet_plan_submit = st.button("Get Diet Plan", type="primary", disabled=not diet_options)
    if diet_plan_submit:
        with st.spinner("Generating Diet Plan..."):
            response = get_gemini_response(diet_plan, api_key)
            st.write(response)

# If selected menu option is "About"
if selection == "About":
    with st.expander("About this App"):
        st.markdown(''' This app has following functionality:

    - Get the details of food items and caloric intake by uploading food image.
    - Get the recipie of uploaded food image
    - Make the customized diet plan

        ''')
    with st.expander("Which Large Language models are supported by this App?"):
        st.markdown(''' This app supports following multimodal:

    * Google -- gemini-1.5-pro-latest

        ''')
    with st.expander("Where to get the source code of this app?"):
        st.markdown(''' Source code is available at:
    -  https://github.com/mzeeshanaltaf/genai-rag-groq-faiss
        ''')

    with st.expander("Whom to contact regarding this app?"):
        st.markdown(''' Contact [Zeeshan Altaf](zeeshan.altaf@gmail.com)
        ''')
