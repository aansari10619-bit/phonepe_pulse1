# 📊 PhonePe Data Visualization Dashboard

An interactive **Streamlit dashboard** powered by **PostgreSQL**, **Pandas**, and **Plotly**, designed to analyze and visualize **PhonePe Pulse** data across India.  
This project uncovers transaction dynamics, user engagement, insurance growth, and market expansion opportunities across multiple business scenarios.

---

## 🚀 Project Overview

The **PhonePe Data Insights Dashboard** helps visualize trends in transactions, user activity, and insurance adoption across different states and districts of India.

It provides insights into:
- **Transaction behavior** across states, years, and categories.
- **User growth and engagement** by region and device.
- **Insurance penetration** and performance by district.
- **Market expansion opportunities** using transaction trends.
- **Strategic growth decisions** driven by data.

---

## 🧠 Features

✅ **Five Business Scenarios:**
1. **Decoding Transaction Dynamics on PhonePe**
2. **Device Dominance and User Engagement Analysis**
3. **Insurance Penetration and Growth Potential Analysis**
4. **Transaction Analysis for Market Expansion**
5. **User Engagement and Growth Strategy**

✅ **Interactive Visualizations:**
- Bar, Line, Pie, Sunburst, and Scatter plots
- Yearly, quarterly, and state-level analysis  
- Top 10 and underperforming state/district insights

✅ **Live Database Integration:**
- Reads directly from **PostgreSQL** using SQLAlchemy.
- Data cached using `st.cache_data` for fast performance.

✅ **Responsive Design:**
- Wide layout and adaptive UI using Streamlit’s layout system.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend/UI** | Streamlit |
| **Backend/Database** | PostgreSQL |
| **Data Connector** | SQLAlchemy |
| **Visualization** | Plotly Express |
| **Data Processing** | Pandas |
| **Language** | Python 3.9+ |

---

## 🗄️ Database Setup

### 1️⃣ Create a PostgreSQL Database
Make sure PostgreSQL is installed and running on your system.

```bash
psql -U postgres
CREATE DATABASE phonepe_pulse;
````

### 2️⃣ Tables Required

Ensure your database includes the following tables:

| Table Name             | Description                                 |
| ---------------------- | ------------------------------------------- |
| aggregated_insurance   | State-wise insurance transaction data       |
| aggregated_transaction | State-wise transaction type and amount data |
| aggregated_user        | Registered users and app opens              |
| map_insurance          | District-level insurance data               |
| map_transaction        | District-level transaction data             |
| top_insurance_dist     | Top insurance-performing districts          |
| top_transaction_dist   | Top transaction-performing districts        |

Each table should contain columns such as `State`, `Year`, `Quarter`, `Transaction_Amount`, `Transaction_Count`, `Registered_Users`, `App_Opens`, etc.

---

## ⚙️ Installation & Setup Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/phonepe-data-dashboard.git
cd phonepe-data-dashboard
```

### Step 2: Create and Activate a Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate   # For Windows
# OR
source myenv/bin/activate  # For macOS/Linux
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
streamlit
pandas
sqlalchemy
psycopg2
plotly
```

### Step 4: Configure PostgreSQL Connection

In your main Python file, update the following credentials:

```python
db_user = 'ansari'
db_password = '1234'
db_host = 'localhost'
db_port = '5433'
db_name = 'phonepe_pulse'
```

### Step 5: Run the Streamlit App

```bash
streamlit run app.py
```

Your app will open in a web browser at:
👉 `http://localhost:8501`

---

## 🧭 Application Flow

### 🔹 Step 1: Data Connection

The app connects to your **PostgreSQL** database using SQLAlchemy:

```python
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
```

Data from seven tables is loaded into pandas DataFrames using:

```python
pd.read_sql("SELECT * FROM table_name", engine)
```

### 🔹 Step 2: Caching for Performance

`@st.cache_data` ensures data loads once and reuses cached results to optimize performance.

### 🔹 Step 3: Scenario Selection

A dropdown (`st.selectbox`) allows you to pick one of five business scenarios.

Each scenario loads specific **business questions**, e.g.:

#### Example:

**Scenario 1 – Decoding Transaction Dynamics**

* Q1: Which states have the highest transaction amounts over years?
* Q2: How does transaction type vary across states?
* Q3: How have user registrations and app opens changed over time?

### 🔹 Step 4: Visualization Logic

Each question triggers a specific Plotly visualization:

* **Bar Charts** → Compare totals by state/year
* **Line Charts** → Show growth trends over time
* **Pie Charts** → Distribution by state
* **Sunburst Charts** → Hierarchical views (State → Type)
* **Scatter Plots** → Correlations between metrics

---

## 🧮 Business Scenarios Explained

### 1️⃣ Decoding Transaction Dynamics on PhonePe

Understand transaction patterns across states, years, and payment categories.
Visuals:

* State-wise transaction growth
* Transaction type distribution
* User growth vs app opens
* Insurance transaction patterns
* Top 10 performing districts

---

### 2️⃣ Device Dominance & User Engagement Analysis

Explore how engagement varies by device and region.
Visuals:

* Registered users by state/year
* Top states for app opens
* Correlation between app opens & user base
* Underperforming regions by engagement ratio

---

### 3️⃣ Insurance Penetration & Growth Potential

Analyze the insurance domain’s growth trajectory and identify opportunities.
Visuals:

* Top states & districts by insurance volume
* Yearly insurance transaction growth
* Average transaction value per policy

---

### 4️⃣ Transaction Analysis for Market Expansion

Identify regions showing potential for new user acquisition and transaction growth.
Visuals:

* State-wise total transaction amounts
* Growth trends by year
* Top performing and emerging districts

---

### 5️⃣ User Engagement & Growth Strategy

Uncover key user engagement trends to drive growth.
Visuals:

* Registered users growth by state/year
* App engagement trends (yearly & quarterly)
* App engagement ratio (opens per user)

---

## 🗂️ Folder Structure

```
phonepe-data-dashboard/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
└── data/                     # Optional data exports or backups
```

---

## 🧰 Troubleshooting

| Issue                            | Solution                                            |
| -------------------------------- | --------------------------------------------------- |
| **psycopg2 not found**           | Run `pip install psycopg2`                          |
| **Port 5432 already in use**     | Update `db_port` to `5433` or another open port     |
| **Invalid database credentials** | Verify PostgreSQL username/password                 |
| **Streamlit not found**          | Run `pip install streamlit`                         |
| **Cannot connect to database**   | Ensure PostgreSQL service is running and accessible |

---

## 🌟 Future Enhancements

* Integrate **real-time API updates** from PhonePe Pulse.
* Add **Geo maps (Plotly Choropleth)** for regional visualizations.
* Implement **filters for Year/Quarter/State** directly in dashboard.
* Add **AI-driven forecasting** for transaction trends.

---

## 🧑‍💻 Author

**Mohammed Ansari**
📍 Built with ❤️ using Streamlit, Plotly, and PostgreSQL.
📧 *For collaboration or feedback: open a GitHub issue.*


