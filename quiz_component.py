import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def render_quiz(quiz_data):
    """Render the quiz questions with answer toggles"""
    if not quiz_data:
        return
    
    # Initialize session state for quiz answers
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Multiple Choice Questions
    if quiz_data.get('mcq'):
        st.subheader("📝 Multiple Choice Questions")
        for i, question in enumerate(quiz_data['mcq'], 1):
            with st.container(border=True):
                st.markdown(f"**{i}. {question['question']}**")
                
                # Display options
                for option in question.get('options', []):
                    st.markdown(f"- {option}")
                
                # Toggle for answer
                answer_key = f"mcq_{i}"
                if st.button(f"Show Answer {i}", key=f"btn_{answer_key}"):
                    st.session_state.quiz_answers[answer_key] = not st.session_state.quiz_answers.get(answer_key, False)
                
                # Show answer if toggled
                if st.session_state.quiz_answers.get(answer_key, False):
                    with stylable_container(
                        "answer",
                        css_styles="""
                            {
                                background-color: #f8f9fa;
                                border-radius: 0.5rem;
                                padding: 1rem;
                                margin-top: 0.5rem;
                            }
                        """,
                    ):
                        st.markdown(f"**Correct Answer:** {question.get('answer', 'N/A')}")
                        if question.get('explanation'):
                            st.markdown(f"**Explanation:** {question['explanation']}")
    
    # Fill in the Blank Questions
    if quiz_data.get('fillblank'):
        st.subheader("✍️ Fill in the Blank")
        for i, question in enumerate(quiz_data['fillblank'], 1):
            with st.container(border=True):
                st.markdown(f"**{i}. {question['question']}**")
                
                answer_key = f"fill_{i}"
                if st.button(f"Show Answer {i}", key=f"btn_{answer_key}"):
                    st.session_state.quiz_answers[answer_key] = not st.session_state.quiz_answers.get(answer_key, False)
                
                if st.session_state.quiz_answers.get(answer_key, False):
                    with stylable_container(
                        "answer",
                        css_styles="""
                            {
                                background-color: #f8f9fa;
                                border-radius: 0.5rem;
                                padding: 1rem;
                                margin-top: 0.5rem;
                            }
                        """,
                    ):
                        st.markdown(f"**Answer:** {question.get('answer', 'N/A')}")
                        if question.get('explanation'):
                            st.markdown(f"**Explanation:** {question['explanation']}")
    
    # Descriptive Questions
    if quiz_data.get('descriptive'):
        st.subheader("💬 Descriptive Questions")
        for i, question in enumerate(quiz_data['descriptive'], 1):
            with st.container(border=True):
                st.markdown(f"**{i}. {question['question']}**")
                
                answer_key = f"desc_{i}"
                if st.button(f"Show Answer {i}", key=f"btn_{answer_key}"):
                    st.session_state.quiz_answers[answer_key] = not st.session_state.quiz_answers.get(answer_key, False)
                
                if st.session_state.quiz_answers.get(answer_key, False):
                    with stylable_container(
                        "answer",
                        css_styles="""
                            {
                                background-color: #f8f9fa;
                                border-radius: 0.5rem;
                                padding: 1rem;
                                margin-top: 0.5rem;
                            }
                        """,
                    ):
                        st.markdown("**Model Answer:**")
                        st.markdown(question.get('answer', 'No answer provided'))
                        if question.get('key_points'):
                            st.markdown("**Key Points:**")
                            for point in question['key_points']:
                                st.markdown(f"- {point}")

def handle_quiz_events():
    """Handle quiz-related session state changes"""
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}