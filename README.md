# 📄 Smart Resume Parser  

An **AI-powered Resume Parser** that extracts structured candidate information, generates insights, and provides professional scoring to evaluate resumes.  

---

## ✨ Features  

✅ Upload resumes in **PDF/DOCX** format  
✅ Extracts **Name, Email, Phone, Skills, Education, Experience, Projects, Certificates, Links, and Summary**  
✅ **AI-powered Resume Scoring** (out of 100, with feedback & breakdown)  
✅ Modern **Streamlit Dashboard** with custom UI/UX  
✅ Export parsed results into **JSON & CSV**  
✅ Backend built with **FastAPI**, integrated with **OpenRouter (Mistral-7B)**  
✅ Deployable on **Render Cloud**  

---

### 🚀 Live Demo  
- 🔗 **Backend API**: [Smart-Resume-Parser-Backend](https://smart-resume-parser-backend-url.onrender.com)  
- 🎨 **Frontend UI**: [Smart-Resume-Parser-Frontend](https://smart-resume-parser-frontend-url.onrender.com)  

---


## 🛠️ Tech Stack  

**Frontend:**  
- Streamlit (Python)  
- Custom CSS for professional dashboard  

**Backend:**  
- FastAPI (Python)  
- OpenRouter API (Mistral-7B Instruct model)  
- PyPDF2, python-docx (Resume text extraction)  

**Data Handling:**  
- JSON, CSV (Export)  
- Pandas  

**Deployment:**  
- Render Cloud (Backend & Frontend services)  

---

## ⚙️ Installation & Setup  

### 1️⃣ Clone Repository  
```bash
git clone https://github.com/your-username/smart-resume-parser.git
cd smart-resume-parser
2️⃣ Setup Backend
cd backend
pip install -r requirements.txt
Create a .env file:

OPENROUTER_API_KEY=your_openrouter_api_key
Run backend:
uvicorn app:app --host 0.0.0.0 --port 8000
3️⃣ Setup Frontend
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
🚀 Usage
Start backend (uvicorn) and frontend (streamlit).

Open frontend (default: http://localhost:8501).

Upload a resume (PDF/DOCX).

View extracted details (skills, education, experience, projects, links, summary).

Get AI-powered resume score & feedback.

Download results as JSON/CSV.

📦 Deployment (Render)
Create two Web Services on Render:

Backend: Python (FastAPI) → uvicorn app:app --host 0.0.0.0 --port 8000

Frontend: Streamlit → streamlit run streamlit_app.py --server.port 10000 --server.address 0.0.0.0

Add .env with your OPENROUTER_API_KEY.

Both services connect automatically via API.
```

---


# 🔮 Future Enhancements
Role-specific scoring system (e.g., Data Scientist, Web Developer)

Candidate-job matching (resume → job description)

Support for multilingual resumes

ATS (Applicant Tracking System) integration

---


## 👨‍💻 Developed by Krishna Shalawadi
