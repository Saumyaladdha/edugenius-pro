import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from prompts import (
    validate_topic,
    suggest_topics,
    generate_lesson_objectives,
    generate_subtopics,
    fetch_unsplash_image,
    generate_quiz_questions,
    generate_lesson_summary
)
from quiz_component import render_quiz, handle_quiz_events
from reference_search import search_references, render_references
from ppt_maker import generate_ppt
import os
import json

# --- App Setup ---
st.set_page_config(
    page_title="EduGenius Pro - AI Lesson Planner",
    page_icon="🧠",
    layout="centered"
)

# --- UI Styling ---
def get_css_styles():
    with open('styles.css', 'r') as f:
        return f"<style>{f.read()}</style>"

def create_header():
    return """
    <div class="header">
        <h1 style="margin:0;font-size:2.5rem">🧠 EduGenius Pro</h1>
        <p style="margin:0;opacity:0.9">Advanced AI Lesson Planning with Visuals & References</p>
    </div>
    """

def create_lesson_overview(curriculum, grade, subject, topic):
    return f"""
    <div class="slide-card">
        <h3 style="color:#3a0ca3">📌 Lesson Overview</h3>
        <table style="width:100%;border-collapse:collapse;margin-top:1rem">
            <tr><td style="width:30%"><b>Curriculum:</b></td><td>{curriculum}</td></tr>
            <tr><td><b>Grade:</b></td><td>{grade}</td></tr>
            <tr><td><b>Subject:</b></td><td>{subject}</td></tr>
            <tr><td><b>Topic:</b></td><td style="color:#f72585;font-weight:600">{topic}</td></tr>
        </table>
    </div>
    """

def create_objectives_card(objectives):
    objectives_list = "\n".join([f"<li>{obj.strip()}</li>" for obj in objectives.split('\n') if obj.strip()])
    return f"""
    <div class="slide-card">
        <h3 style="color:#3a0ca3">🎯 Key Learning Objectives</h3>
        <ul class="objectives-list">{objectives_list}</ul>
    </div>
    """

def create_subtopic_card(subtopic, i):
    key_concepts = ', '.join(subtopic.get('key_concepts', ['N/A']))
    example = subtopic.get('examples', ['N/A'])[0]
    misconception = subtopic.get('misconceptions', ['N/A'])[0]
    
    return f"""
    <div class="slide-card">
        <h3 class="subtopic-title">📖 Part {i}: {subtopic['title']}</h3>
        <p>{subtopic['content']}</p>
        <div style="background:#f8f9fa;padding:1rem;border-radius:8px;margin-top:1rem">
            <h4 style="color:#4361ee;margin-top:0">🔍 Key Details</h4>
            <ul>
                <li><b>Key Concepts:</b> {key_concepts}</li>
                <li><b>Example:</b> {example}</li>
                <li><b>Note:</b> {misconception}</li>
            </ul>
        </div>
    </div>
    """

def create_summary_card(summary):
    cleaned_summary = summary.replace("#*", "").replace("🧠", "").strip()
    if not cleaned_summary.endswith("</div>"):
        cleaned_summary += "</div>"
    while cleaned_summary.count("</div>") > 1:
        last_div = cleaned_summary.rfind("</div>")
        cleaned_summary = cleaned_summary[:last_div]
    
    return f"""
    <div class="slide-card" style="background-color:#f8f9fa;border-left:4px solid #3a0ca3">
        <h3 style="color:#3a0ca3">📝 Lesson Summary</h3>
        <div class="summary-content">
            {cleaned_summary}
        </div>
    </div>
    """

def init_session_state():
    if 'valid_topic' not in st.session_state:
        st.session_state.valid_topic = None
    if 'suggestions' not in st.session_state:
        st.session_state.suggestions = []
    if 'show_suggestions' not in st.session_state:
        st.session_state.show_suggestions = False
    if 'objectives' not in st.session_state:
        st.session_state.objectives = None
    if 'temp_subtopics' not in st.session_state:
        st.session_state.temp_subtopics = None
    if 'include_visuals' not in st.session_state:
        st.session_state.include_visuals = False
    if 'include_references' not in st.session_state:
        st.session_state.include_references = True
    if 'unsplash_images' not in st.session_state:
        st.session_state.unsplash_images = {}
    if 'selected_images' not in st.session_state:
        st.session_state.selected_images = {}
    if 'image_attempts' not in st.session_state:
        st.session_state.image_attempts = {}
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'lesson_summary' not in st.session_state:
        st.session_state.lesson_summary = None
    if 'all_references' not in st.session_state:
        st.session_state.all_references = []

def main():
    st.markdown(get_css_styles(), unsafe_allow_html=True)
    st.markdown(create_header(), unsafe_allow_html=True)
    init_session_state()
    handle_quiz_events()

    # Input Form
    with st.form("lesson_form", border=False):
        col1, col2 = st.columns(2)
        with col1:
            curriculum = st.selectbox("📚 Curriculum Standard", 
                                    ["CBSE", "ICSE", "IGCSE", "State Board", "IB"])
        with col2:
            grade = st.selectbox("🎒 Grade Level", 
                               [f"Grade {i}" for i in range(1, 13)] + ["College"])
        
        subject = st.text_input("📝 Subject", placeholder="e.g., Quantum Physics, Art History")
        topic = st.text_input("🔍 Topic", placeholder="e.g., Heisenberg Principle, Renaissance Art")
        
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.include_visuals = st.checkbox("🖼️ Include Visual Aids (from Unsplash)", value=True)
        with col4:
            st.session_state.include_references = st.checkbox("📚 Include Reference Links", value=True)
            
        submitted = st.form_submit_button("✨ Generate Lesson Plan", type="primary")

    if submitted:
        process_form_submission(curriculum, grade, subject, topic)

    display_suggestions(topic, curriculum, grade, subject)

    if st.session_state.valid_topic:
        display_lesson_plan(curriculum, grade, subject)

def process_form_submission(curriculum, grade, subject, topic):
    if not subject or not topic:
        st.warning("Please enter both subject and topic")
    else:
        with st.spinner("🔍 Analyzing topic relevance..."):
            validation = validate_topic(curriculum, grade, subject, topic)
            
            if validation == "valid":
                st.session_state.valid_topic = topic
                st.session_state.show_suggestions = False
                st.session_state.unsplash_images = {}
                st.session_state.selected_images = {}
                st.session_state.image_attempts = {}
                st.session_state.lesson_summary = None
                st.session_state.all_references = []
                
                with st.spinner("📝 Crafting learning objectives..."):
                    st.session_state.objectives = generate_lesson_objectives(
                        curriculum, grade, subject, topic
                    )
                
                with st.spinner("📝 Generating assessment questions..."):
                    lesson_content = f"Topic: {topic}\nSubject: {subject}\nGrade: {grade}\nObjectives: {st.session_state.objectives}"
                    st.session_state.quiz_data = generate_quiz_questions(
                        curriculum, grade, subject, topic, lesson_content
                    )
                
            elif validation == "irrelevant":
                with st.spinner("💡 Generating possible subtopics for your input..."):
                    st.session_state.temp_subtopics = generate_subtopics(
                        curriculum, grade, subject, topic, ""
                    )
                
                if isinstance(st.session_state.temp_subtopics, dict):
                    st.warning(f"⚠️ '{topic}' may not perfectly match {subject}. But here are some related subtopics we found:")
                    st.session_state.show_suggestions = True
                    
                    with st.spinner("🔎 Finding better matching topics..."):
                        st.session_state.suggestions = suggest_topics(
                            curriculum, grade, subject
                        )
                else:
                    st.error("Couldn't generate related content. Please try a different topic.")
            
            elif validation == "harmful":
                st.error("⚠️ This topic isn't appropriate for the selected grade level")

def display_suggestions(topic, curriculum, grade, subject):
    if st.session_state.show_suggestions:
        if st.session_state.temp_subtopics and isinstance(st.session_state.temp_subtopics, dict):
            with st.expander("🌱 Related Subtopic Ideas (from your input)", expanded=True):
                for i, subtopic in enumerate(st.session_state.temp_subtopics["subtopics"], 1):
                    st.markdown(f"**{i}. {subtopic['title']}**")
                    st.markdown(f"{subtopic['content']}")
                    if st.button(f"Use This Subtopic", key=f"subtopic_{i}"):
                        st.session_state.valid_topic = f"{topic}: {subtopic['title']}"
                        st.session_state.show_suggestions = False
                        with st.spinner("📝 Creating objectives for selected subtopic..."):
                            st.session_state.objectives = generate_lesson_objectives(
                                curriculum, grade, subject, 
                                st.session_state.valid_topic
                            )
                        st.rerun()
                    st.write("---")
        
        if st.session_state.suggestions:
            with st.expander("💡 Better Matching Topics We Recommend", expanded=True):
                selected = st.selectbox("Or select one of these perfect matches:", 
                                      st.session_state.suggestions)
                if st.button("✅ Use This Topic Instead"):
                    st.session_state.valid_topic = selected
                    st.session_state.show_suggestions = False
                    with st.spinner("📝 Creating objectives for selected topic..."):
                        st.session_state.objectives = generate_lesson_objectives(
                            curriculum, grade, subject, 
                            st.session_state.valid_topic
                        )
                    st.rerun()

def display_lesson_plan(curriculum, grade, subject):
    st.session_state.current_subject = subject
    st.session_state.current_grade = grade
    
    st.markdown(create_lesson_overview(
        curriculum, grade, subject, st.session_state.valid_topic
    ), unsafe_allow_html=True)
    
    if st.session_state.objectives:
        st.markdown(create_objectives_card(
            st.session_state.objectives
        ), unsafe_allow_html=True)
    
    with st.spinner("📚 Developing detailed lesson content..."):
        subtopics = generate_subtopics(
            curriculum, grade, subject, 
            st.session_state.valid_topic,
            st.session_state.objectives
        )
    
    if isinstance(subtopics, dict) and "subtopics" in subtopics:
        for i, subtopic in enumerate(subtopics["subtopics"], 1):
            with st.container():
                # Collect references if enabled
                if st.session_state.include_references:
                    with st.spinner(f"🔍 Finding references for: {subtopic['title']}"):
                        references = search_references(
                            subtopic['title'], 
                            subject, 
                            grade
                        )
                        st.session_state.all_references.extend(references)
                
                st.markdown(create_subtopic_card(subtopic, i), unsafe_allow_html=True)
                
                if st.session_state.include_visuals:
                    handle_image_selection(subtopic, i)

        with st.spinner("📝 Generating comprehensive lesson summary..."):
            st.session_state.lesson_summary = generate_lesson_summary(
                curriculum, grade, subject,
                st.session_state.valid_topic,
                subtopics["subtopics"]
            )
        
        add_vertical_space(2)
        st.markdown(create_summary_card(st.session_state.lesson_summary), unsafe_allow_html=True)
        
        # Display all references together at the end
        if st.session_state.include_references and st.session_state.all_references:
            st.markdown("---")
            st.markdown(render_references(st.session_state.all_references), unsafe_allow_html=True)
        
        # Render quiz if it exists
        if st.session_state.quiz_data:
            render_quiz(st.session_state.quiz_data)
        
        # Add PPT download button at the very end
        add_vertical_space(2)
        with st.container():
            st.markdown("---")
            st.subheader("📊 Presentation Export")
            
            ppt_data = {
                "curriculum": curriculum,
                "grade": grade,
                "subject": subject,
                "topic": st.session_state.valid_topic,
                "objectives": st.session_state.objectives,
                "subtopics": subtopics["subtopics"],
                "summary": st.session_state.lesson_summary,
                "references": st.session_state.all_references,
                "quiz_data": st.session_state.quiz_data,
                "selected_images": st.session_state.selected_images,
                "unsplash_images": st.session_state.unsplash_images
            }
            
            if st.button("🎨 Generate PowerPoint Presentation", use_container_width=True):
                with st.spinner("🖨️ Creating beautiful PowerPoint presentation..."):
                    try:
                        ppt_file = generate_ppt(ppt_data)
                        st.download_button(
                            label="⬇️ Download PowerPoint",
                            data=ppt_file,
                            file_name=f"EduGenius_Lesson_{subject.replace(' ', '_')}_{st.session_state.valid_topic[:20].replace(' ', '_')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error generating PPT: {str(e)}")

def handle_image_selection(subtopic, i):
    subtopic_key = f"{subtopic['title']}_{i}"
    
    if subtopic_key not in st.session_state.unsplash_images:
        st.session_state.unsplash_images[subtopic_key] = []
        st.session_state.selected_images[subtopic_key] = None
        st.session_state.image_attempts[subtopic_key] = 0
    
    if not st.session_state.unsplash_images[subtopic_key]:
        with st.spinner(f"🖼️ Finding visual options for: {subtopic['title']}..."):
            for _ in range(3):
                attempt = st.session_state.image_attempts[subtopic_key]
                img_data = fetch_unsplash_image(
                    subtopic['title'],
                    st.session_state.current_subject,
                    st.session_state.current_grade,
                    attempt
                )
                if img_data:
                    st.session_state.unsplash_images[subtopic_key].append(img_data)
                st.session_state.image_attempts[subtopic_key] += 1
    
    if st.session_state.unsplash_images[subtopic_key]:
        st.subheader("🎨 Select Visual Aid")
        
        cols = st.columns(3)
        for idx, img_data in enumerate(st.session_state.unsplash_images[subtopic_key][:3]):
            with cols[idx]:
                is_selected = st.session_state.selected_images.get(subtopic_key) == idx
                st.markdown(f"""
                <div class="image-option {'selected' if is_selected else ''}">
                    <img src="{img_data['url']}" class="diagram-img">
                    <p class="unsplash-credit">Photo by {img_data['credit']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select This", key=f"select_{subtopic_key}_{idx}"):
                    st.session_state.selected_images[subtopic_key] = idx
                    st.rerun()
        
        if st.button("🔄 Show Different Images", key=f"refresh_{subtopic_key}"):
            st.session_state.unsplash_images[subtopic_key] = []
            st.rerun()
    
    if (subtopic_key in st.session_state.selected_images and 
        st.session_state.selected_images[subtopic_key] is not None and
        len(st.session_state.unsplash_images[subtopic_key]) > st.session_state.selected_images[subtopic_key]):
        
        selected_idx = st.session_state.selected_images[subtopic_key]
        selected_img = st.session_state.unsplash_images[subtopic_key][selected_idx]
        
        st.markdown(f"""
        <div class="image-container">
            <h4>📷 Selected Visual: {subtopic['title']}</h4>
            <img src="{selected_img['url']}" 
                 class="diagram-img" 
                 style="max-height:400px"
                 alt="Selected visual for {subtopic['title']}">
            <p class="unsplash-credit">
                Photo by <a href="{selected_img['profile']}" target="_blank">{selected_img['credit']}</a> on Unsplash
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()