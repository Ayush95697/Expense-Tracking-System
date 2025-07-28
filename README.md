# 💰 Expense Management System

A full-stack personal finance tracker that allows users to add, update, and analyze expenses. This system supports SQL-based persistent storage, provides category-wise analytics, uses API communication between frontend and backend, and includes robust logging and testing systems.

---

## 🚀 Features

- 📆 Add and update daily expenses with:
  - Amount
  - Category (Rent, Food, Shopping, Entertainment, Other)
  - Notes
  - Date
- 📊 **Analytics Tab**:
  - Filter expenses by date range
  - Visualize and break down spending by category
- 🛢️ **SQL Database Integration**
- 🔌 **Backend APIs** using FastAPI (or Flask)
- 🖥️ **Frontend UI** using Streamlit
- 📜 **Logging System** for monitoring and debugging
- ✅ **Unit Testing** using `pytest`

---

## 🗂️ Project Structure

├── backend

│   ├── db_helper.py          # DB operations

│   ├── logging_setup.py      # Logging configuration

│   ├── server.py             # API logic

├── frontend

│   └── app.py                # Streamlit UI

├── tests

│   ├── backend/test_db_helper.py

│   ├── frontend/

│   └── conftest.py           # Fixtures

├── database/                 # (Assuming DB files exist here)

├── requirements.txt

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** - frontend interface
- **FastAPI** / **Flask** - API backend
- **SQLite / MySQL** - persistent database
- **pytest** - unit testing
- **Logging** - built-in Python logging module

---

## ✅ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/expense-management-system.git
cd expense-management-system
```
### 2. Create and activate virtual environment (optional but recommended)
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Run Backend Server
```
cd backend
python server.py

```
### 5. Run Frontend
```
cd frontend
streamlit run app.py
```
### 🧪 Running Tests
```
pytest tests/
```
 ### 🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit a pull request. 
### 📜 License
This project is licensed under the MIT License.

### 🙋‍♂️ Author
Ayush Mishra
📧 ayushmishra7548@gmail.com


