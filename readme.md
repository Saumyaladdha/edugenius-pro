# **EduGenius Pro - AI-Powered Lesson Planner**  
**🚀 Streamline Lesson Planning with AI-Generated Content, Visuals, and Assessments**  

---

## **📌 Table of Contents**  
1. [Project Overview](#-project-overview)  
2. [Key Features](#-key-features)  
3. [Tech Stack](#-tech-stack)  
4. [Installation & Setup](#-installation--setup)  
5. [How It Works](#-how-it-works)  
6. [API Integrations](#-api-integrations)  
7. [File Structure](#-file-structure)  
8. [Customization Guide](#-customization-guide)  
9. [Known Issues & Troubleshooting](#-known-issues--troubleshooting)  
10. [Future Roadmap](#-future-roadmap)  
11. [Contributing](#-contributing)  
12. [License](#-license)  

---

## **🌐 Project Overview**  
EduGenius Pro is an **AI-powered lesson planning assistant** that helps educators:  
✅ Generate **structured lesson plans** aligned with curriculum standards (CBSE, IB, IGCSE, etc.)  
✅ Automate **learning objectives, subtopics, quizzes, and summaries**  
✅ Fetch **high-quality educational images** from Unsplash  
✅ Curate **credible reference links** from Google Scholar and academic sources  
✅ Export lessons as **PowerPoint presentations** with one click  

**Target Users:**  
- Teachers  
- Tutors  
- Homeschooling parents  
- Education content creators  

---

## **✨ Key Features**  

### **1. Smart Topic Validation**  
- AI checks if a topic is **grade-appropriate** and **subject-relevant**  
- Suggests alternatives if the topic is too advanced or irrelevant  

### **2. Dynamic Lesson Generation**  
- **Learning Objectives:** Clear, measurable goals (no vague fluff!)  
- **Subtopics:** Broken down with:  
  - Key concepts  
  - Real-world examples  
  - Common student misconceptions  
- **Assessment Questions:**  
  - Multiple Choice (MCQs)  
  - Fill-in-the-blanks  
  - Descriptive (with model answers)  

### **3. Automated Visual Aids**  
- **Unsplash Integration:** Fetches **copyright-free educational images**  
- **Smart Selection:** Different images for each subtopic to avoid repetition  

### **4. Reference Aggregator**  
- Pulls **credible sources** (.edu, .gov, academic journals) via Google Custom Search API  
- Filters out unreliable or paywalled content  

### **5. One-Click PowerPoint Export**  
- **Professional slide layouts**  
- **Auto-formatted content** (no manual tweaking needed)  
- **Image credits embedded** (to avoid plagiarism issues)  

### **6. Interactive Quiz System**  
- Toggle answers on/off (prevents accidental spoilers)  
- Explanations for each question (reinforces learning)  

---

## **🛠 Tech Stack**  
| Category          | Technologies Used |  
|-------------------|------------------|  
| **Frontend**      | Streamlit, HTML/CSS |  
| **Backend**       | Python (Gemini AI, PPTX, Requests) |  
| **APIs**          | Google Custom Search, Unsplash |  
| **AI**            | Google Gemini 1.5 Flash |  
| **Deployment**    | Docker, Streamlit Cloud (optional) |  

---

## **⚙ Installation & Setup**  

### **Prerequisites**  
- Python 3.10+  
- `pip` (latest version)  
- Google Gemini API Key  
- Unsplash API Key  
- Google Custom Search API Key  

### **Setup Steps**  
1. **Clone the repo**  
   ```bash
   git clone https://github.com/saumyaLaddha/edugenius-pro.git
   cd edugenius-pro
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   Create a `.env` file in the root directory:  
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   UNSPLASH_ACCESS_KEY=your_unsplash_key
   GOOGLE_API_KEY=your_google_api_key
   SEARCH_ENGINE_ID=your_search_engine_id
   ```

4. **Run the app**  
   ```bash
   streamlit run app.py
   ```

5. **Access the app**  
   Open `http://localhost:8501` in your browser.  

---

## **🔍 How It Works**  

### **Step 1: Input Lesson Details**  
- Select **Curriculum, Grade, Subject, and Topic**  
- Toggle options for **visuals & references**  

### **Step 2: AI Validates & Generates Content**  
1. **Topic Check:** AI confirms if the topic is suitable.  
2. **Lesson Plan Generated:**  
   - Objectives  
   - Subtopics (with examples & misconceptions)  
   - Quiz questions  
   - Summary  

### **Step 3: Customize & Export**  
- **Add/remove subtopics**  
- **Swap images** (if Unsplash results aren’t perfect)  
- **Export PPT** with one click  

---

## **🔌 API Integrations**  

| **API**               | **Usage** | **Rate Limits** |  
|-----------------------|----------|----------------|  
| **Google Gemini**      | Generates lesson content | 60 RPM (requests per minute) |  
| **Unsplash**           | Fetches educational images | 50 requests/hour |  
| **Google Custom Search** | Finds academic references | 100 queries/day |  

---

## **📂 File Structure**  
```plaintext
edugenius-pro/  
├── app.py                 # Main Streamlit app  
├── prompts.py             # AI prompt templates  
├── quiz_component.py      # Interactive quiz logic  
├── reference_search.py    # Google Search API handler  
├── ppt_maker.py           # PowerPoint generator  
├── styles.css             # Custom CSS for UI  
├── requirements.txt       # Python dependencies  
├── .env.example           # API key template  
└── README.md              # This file  
```

---

## **🎨 Customization Guide**  

### **1. Changing the UI Theme**  
Edit `styles.css` to modify:  
- Colors  
- Fonts  
- Card layouts  

### **2. Adjusting AI Output**  
Modify prompts in `prompts.py` to:  
- Change **tone** (more formal/casual)  
- Add/remove **sections** (e.g., case studies)  

### **3. Adding New Curriculum Standards**  
Update the `validate_topic()` function in `prompts.py` to support more frameworks (e.g., Common Core).  

---

## **⚠ Known Issues & Troubleshooting**  

| **Issue** | **Solution** |  
|-----------|-------------|  
| "JSON decode error" in subtopics | Manually check AI output in `prompts.py` |  
| Unsplash images not loading | Verify API key + check rate limits |  
| PPT formatting breaks | Reduce text length or adjust `pptx` settings |  

---

## **🚀 Future Roadmap**  
- **Multi-language support** (Spanish, French, Hindi)  
- **Student-facing quiz mode**  
- **Google Classroom integration**  
- **Collaborative editing** (real-time co-authoring)  

---

## **🤝 Contributing**  
1. Fork the repo  
2. Create a branch (`git checkout -b feature/your-feature`)  
3. Commit changes (`git commit -m 'Add some feature'`)  
4. Push (`git push origin feature/your-feature`)  
5. Open a **Pull Request**  

---

## **📜 License**  
MIT License - See [LICENSE](LICENSE) for details.  

---

**Happy Teaching!** 🍎📚