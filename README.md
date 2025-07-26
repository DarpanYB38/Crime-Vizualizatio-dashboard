# 🔍 Crime Similarity Search System using Django

This project is a **Crime Similarity Detection System** built using **Django**. It helps identify and compare similar crime records based on user input, using **TF-IDF vectorization** and **cosine similarity**.

---

## 🚀 Features

- 🔎 Search for similar crimes based on:
  - Crime Type
  - Modus Operandi
  - Weapon Used
  - Location
- 📊 Computes similarity using **TF-IDF** + **Cosine Similarity**
- 📁 Stores historical crime data in a database
- 💡 Simple, clean UI with custom design (no Bootstrap)
- 🧠 Smart matching based on text similarity

---

## ⚙️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Dark Themed Custom UI)
- **Database**: SQLite
- **Algorithm**: TF-IDF + Cosine Similarity (via `sklearn`)

---

## 📦 Python Libraries Used

Make sure to install the following libraries before running:

```bash
pip install django
pip install scikit-learn
```

crime_similarity_project/
│
├── templates/
│   └── similarity_search.html     # Frontend UI
│
├── views.py                       # Logic for similarity detection
├── models.py                      # CrimeRecord model
├── urls.py                        # Routing
├── manage.py                      # Django runner
└── ...


💻 How to Run
Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
2. install dependencies
```bash
pip install -r requirements.txt
```
3.Run the Server
```bash
python manage.py runserver
```
4. Open i Browser
```bash
Visit http://127.0.0.1:8000/ and try the Crime Similarity Search!
```
🧠 Algorithm Explanation
TF-IDF (Term Frequency–Inverse Document Frequency) transforms text inputs into meaningful vectors.

Cosine Similarity is used to find the angle between those vectors, helping identify how similar two crimes are.

Output: Most similar historical crimes ranked by percentage match.

📌 Keywords
Django, Crime Similarity, TF-IDF, Cosine Similarity, Text Matching, Criminal Record Matching, Python, Machine Learning, Information Retrieval, Sklearn, Search Engine, Smart Form, Semantic Search, Dark Theme UI

🙋‍♂️ Author
Darpan YB
If you liked this project, feel free to ⭐️ the repo and connect with me!

📃 License
This project is licensed under the MIT License.

---

Let me know if you'd like me to also generate the `requirements.txt`, or help you push to GitHub step-by-step!
