
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get Groq API key
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"

profile = """
# Aditya Kumar Singh

LinkedIn: https://www.linkedin.com/in/aditya-kumar-singh-173911321/
Email: adityasingh452452@gmail.com
GitHub: https://github.com/Adityasinghrajput01
Mobile: +91 8303345245

## Technical Skills

- Languages: Python, SQL (MySQL, PostgreSQL), R, Java, C, C++, JavaScript, C#
- Frameworks & Libraries: FastAPI, Scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch, Pandas, NumPy, Matplotlib, Seaborn
- Developer & MLOps Tools: Docker, Git, GitHub, Git LFS, Linux, AWS (S3, EC2), Postman, MLflow
- Data Analytics & BI: Power BI, DAX, Tableau, Feature Engineering, EDA, Statistical Modelling, Hypothesis Testing, A/B Testing
- Soft Skills: Technical Communication, Leadership, Structured Thinking, Team Collaboration

## Projects

### AutoForge Engine – Open-Source AutoML Framework
Date: Sep'26
GitHub: https://github.com/Adityasinghrajput01/ModelForge

- Architected and published an open-source Python AutoML framework on PyPI, reducing model evaluation cycles by 75%.
- Streamlined data preprocessing, 10-fold cross-validation, hyperparameter tuning, and zero-loss model persistence.
- Packaged a full CLI and Python API with pytest integration, ensuring reliable deployment standards across environments.
- Technologies: Python, Scikit-learn, Pandas, NumPy, PyPI, pytest, CLI, GitHub

### NYC Taxi Trip Duration Prediction – End-to-End ML Pipeline
Date: Jul'26
GitHub: https://github.com/Adityasinghrajput01/NYC-Taxi-Trip-Duration-Prediction

- Engineered processing routines for 1.45M+ spatial records, isolating temporal patterns and calculating distance vectors.
- Optimized a Random Forest model using log-transforms (log1p/expm1), reaching R² = 0.7674, MAE 191.11s, and RMSE 318.94s.
- Containerized service artifacts via Docker and Git LFS, launching a production-grade REST API on Render with Swagger docs.
- Technologies: Python, Pandas, NumPy, Scikit-learn, Random Forest, FastAPI, Docker, Render

### Electric Vehicle Range Prediction – ML & Power BI Dashboard
Date: Jul'26
GitHub: https://github.com/Adityasinghrajput01/Electric-Vehicle-range-prediction

- Formulated a predictive regression framework, integrating feature scaling and encoding, leading to a 25% reduction in prediction errors.
- Benchmarked Linear Regression, Decision Trees, and Random Forest via 5-fold GridSearchCV, yielding R² = 0.9612 and MAE 15.27.
- Constructed an interactive Power BI dashboard with custom DAX measures to analyze operational trends across 500+ vehicles.
- Technologies: Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Power BI, DAX

## Training

### Lovely Professional University – Centre for Professional Enhancement
Date: Jun'26 – Jul'26
Link: https://www.linkedin.com/in/aditya-kumar-singh-173911321/overlay/Certifications/443098330/treasury/?profileId=ACoAAFF4lKcB6ko6ZTtY2Ky935T7voHn7r7hkfE

Next-Gen Data Bootcamp: SQL, Power BI, Python, ML & AI Automation

- Mastered enterprise-grade analytical workflows by authoring 50+ complex SQL query scripts and multi-stage algorithmic data pipelines.
- Structured custom relational database schemas and systematic data transformation flows across 10+ hands-on practical capstones.
- Executed Python analytical scripts, boosting reporting throughput and data processing efficiency by 40%.

## Achievements

- Published open-source library autoforge-engine on PyPI; maintained repository source code on GitHub.
  PyPI: https://pypi.org/project/autoforge-engine/
  GitHub: https://github.com/Adityasinghrajput01/ModelForge

- Solved 1000+ algorithmic data structure problems across LeetCode, CodeChef, and HackerRank.
  Coding Profile: https://codolio.com/profile/aditya9450

- Outperformed competing teams to advance through 3 rounds of the Adobe India Hackathon (125K+ total applicants).

## Certificates

- Data Analytics Job Simulation — Deloitte (via Forage) | Jun'26
  Link: https://www.linkedin.com/in/aditya-kumar-singh-173911321/overlay/Certifications/88148192/treasury/?profileId=ACoAAFF4lKcB6ko6ZTtY2Ky935T7voHn7r7hkfE

- Data Engineering on AWS – Foundations — AWS Training & Certification | Mar'26
  Link: https://www.linkedin.com/in/aditya-kumar-singh-173911321/overlay/Certifications/1066883138/treasury/?profileId=ACoAAFF4lKcB6ko6ZTtY2Ky935T7voHn7r7hkfE

- Introduction to Generative AI — Google | Mar'26
  Link: https://www.linkedin.com/in/aditya-kumar-singh-173911321/overlay/Certifications/1063879421/treasury/?profileId=ACoAAFF4lKcB6ko6ZTtY2Ky935T7voHn7r7hkfE

- Oracle Certified Foundations Associate – AI Foundations — Oracle | Sep'25
  Link: https://www.linkedin.com/in/aditya-kumar-singh-173911321/overlay/Certifications/1480261676/treasury/?profileId=ACoAAFF4lKcB6ko6ZTtY2Ky935T7voHn7r7hkfE

## Education

Lovely Professional University — Phagwara, Punjab
Bachelor of Technology – Computer Science and Engineering
CGPA: 9.08 | Aug'24 – Present

Children College School (ICSE) — Azamgarh, U.P.
Intermediate (Class XII with PCM): 70% | Mar'23 – May'24
Matriculate (Class X): 89% | Mar'21 – May'22
"""


# System prompt
system_prompt = f"""
You are a strict document-based information extraction assistant.

SOURCE OF TRUTH:
The following resume is your only permitted source:

{profile}

RULES:
1. Answer only the exact question asked.
2. Extract information only from the resume.
3. Never invent, assume, infer, or generate additional information.
4. Never add skills, technologies, experience, or achievements.
5. Do not use external knowledge.
6. Preserve exact project names, technical terms, numbers, and facts.
7. If information is unavailable, respond exactly:
   This information is not mentioned in the provided document.
8. Do not add introductions, conclusions, suggestions, or explanations.
9. Do not provide unrelated information.
10. Use simple, clean plain text.
11. Do not use Markdown formatting, bold text, or unnecessary headings.
12. Maintain context from previous user questions and assistant answers.
13. Resolve references such as "it", "this", "that", "its" and "the first one"
    using the previous conversation.
14. If the user asks a follow-up question, identify the exact subject
    from the previous conversation before answering.
15. Always recheck the identified subject against the original resume.
16. Never say information is missing if it is explicitly available
    in the resume.
17. If multiple subjects are possible, ask the user for clarification.
18. When asked for a project, certificate, profile, or training link,
    retrieve the exact URL associated with that item from the resume.
19. Resolve references such as "first project", "second project",
    "its GitHub link", and "give it" using conversation history.
20. Return the complete URL without modifying it.
21. If a URL exists in the resume, never say it is unavailable.
22. Do not confuse the general GitHub profile URL with an individual
    project's GitHub repository URL.

IMPORTANT:
Your task is information extraction, NOT content generation.
Accuracy is more important than completeness.
"""

def get_response(messages):

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        temperature=0
    )

    return response.choices[0].message.content

    assistant_response = response.choices[0].message.content

    return assistant_response
