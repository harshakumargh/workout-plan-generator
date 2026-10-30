import streamlit as st
import requests

#browser caption
st.set_page_config(page_title="WPG", page_icon="💪", layout="centered", initial_sidebar_state="collapsed")

#setting the session
if "step" not in st.session_state:
    st.session_state.step = 1

st.title("Workout Plan Generator")


#progress bar
st.progress(st.session_state.step/3)
st.caption(f"Step {st.session_state.step} of 3")

# Screen 1 
if st.session_state.step == 1:

    st.subheader("Tell us about yourself")

    with st.form("personal_details"):

        name = st.text_input(
            "Name",
            value=st.session_state.get("name", "")
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=st.session_state.get("age"),
            step=1
        )

        sex_options = [
            "Select",
            "Male",
            "Female",
            "Other",
            "Prefer not to say"
        ]

        sex = st.selectbox(
            "Sex",
            sex_options,
            index=sex_options.index(
                st.session_state.get("sex", "Select")
            )
        )

        next_clicked = st.form_submit_button("Next")

    if next_clicked:

        if not name.strip() or age is None or sex == "Select":
            st.error("Please complete all fields.")

        else:
            # Save personal information
            st.session_state.name = name.strip()
            st.session_state.age = age
            st.session_state.sex = sex

            # Navigate to Page 2
            st.session_state.step = 2
            st.rerun()

# Screen 2
elif st.session_state.step == 2:

    st.subheader("Body & Lifestyle")

    with st.form("body_lifestyle"):

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=st.session_state.get("height"),
            step=1.0
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=400.0,
            value=st.session_state.get("weight"),
            step=0.5
        )

        activity_options = [
            "Select",
            "Office job (Mostly sitting)",
            "Field job (Mostly active)",
            "Balanced"
        ]

        activity = st.selectbox(
            "Your daily activity",
            activity_options,
            index=activity_options.index(
                st.session_state.get("activity", "Select")
            )
        )

        next_clicked = st.form_submit_button("Next")

    if next_clicked:
        if height is None or weight is None or activity == "Select":
            st.error("Please complete all fields.")
        else:
            st.session_state.height = height
            st.session_state.weight = weight
            st.session_state.activity = activity

            st.session_state.step = 3
            st.rerun()

    if st.button("Back", key="back_to_page1"):
        st.session_state.step = 1
        st.rerun()

# Screen 3
elif st.session_state.step == 3:
    st.subheader("Workout Preferences")

    with st.form("workout_preferences"):

        goal_options = [
            "Select",
            "Build muscle",
            "Lose fat",
            "General fitness",
            "Improve endurance"
        ]

        goal = st.selectbox(
            "Fitness Goal",
            goal_options,
            index=goal_options.index(
                st.session_state.get("goal", "Select")
            )
        )

        experience_options = [
            "Select",
            "Beginner",
            "Intermediate",
            "Advanced"
        ]

        experience = st.selectbox(
            "Experience Level",
            experience_options,
            index=experience_options.index(
                st.session_state.get("experience", "Select")
            )
        )

        days = st.slider(
            "Days available per week",
            min_value=1,
            max_value=7,
            value=st.session_state.get("days", 3)
        )

        equipment_options = [
            "Select",
            "No equipment",
            "Home dumbbells",
            "Full gym"
        ]

        equipment = st.selectbox(
            "Equipment Access",
            equipment_options,
            index=equipment_options.index(
                st.session_state.get("equipment", "Select")
            )
        )

        limitations = st.text_area(
            "Injuries or Limitations (Optional)",
            value=st.session_state.get("limitations", ""),
            placeholder="e.g. Bad knees, no overhead pressing"
        )

        more = st.text_area(
                    "More (Optional)",
                    value=st.session_state.get("more", ""),
                    placeholder="e.g. Anything else you would like to share, we will use it before building the plan"
                )

        submit_clicked = st.form_submit_button("Submit")

    if submit_clicked:

        if (
            goal == "Select"
            or experience == "Select"
            or equipment == "Select"
        ):
            st.error("Please complete all required fields.")

        else:
            st.session_state.goal = goal
            st.session_state.experience = experience
            st.session_state.days = days
            st.session_state.equipment = equipment
            st.session_state.limitations = limitations
            st.session_state.more = more

            # Collect information from all 3 pages
            workout_profile = {
                "name": st.session_state.name,
                "age": st.session_state.age,
                "sex": st.session_state.sex,
                "height": st.session_state.height,
                "weight": st.session_state.weight,
                "activity": st.session_state.activity,
                "fitness_goal": goal,
                "experience_level": experience,
                "days_per_week": days,
                "equipment": equipment,
                "limitations": limitations,
                "more" : more

            }

            st.success("Workout profile submitted!")

        if st.button("Back", key="back_to_page2"):
            st.session_state.step = 2
            st.rerun()

        st.session_state.pop("workout_plan",None)
        try:
            with st.spinner("Generating Workout Plan"):
                response = requests.post("http://127.0.0.1:8000/workout",json = workout_profile,timeout=90)
                response.raise_for_status()
                result = response.json()
                st.session_state.workout_plan = result["workout_plan"]
        except Exception as e:
            st.error(e)


    if "workout_plan" in st.session_state:

        st.divider()

        st.subheader("Your Personalized Workout Plan")

        col1, col2, col3 = st.columns(3)

        col1.metric("Fitness Goal", st.session_state.goal)
        col2.metric("Experience", st.session_state.experience)
        col3.metric("Days / Week", st.session_state.days)

        with st.container(border=True):
            st.markdown(st.session_state.workout_plan)

        st.download_button(
            label="Download Workout Plan",
            data=st.session_state.workout_plan,
            file_name="workout_plan.md",
            mime="text/markdown"
        )