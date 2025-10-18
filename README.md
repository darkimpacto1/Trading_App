# Stock Market Data Manager

A lightweight **stock market data management system** built with **Python and SQLite**, featuring a command-line interface (CLI) for CRUD operations and automated report generation for visualization in **Tableau**.

---

## 🧠 Overview

This project allows users to manage, store, and analyze stock market data efficiently.  
The system provides:
- **CRUD (Create, Read, Update, Delete)** operations on stock market records  
- **Automated report generation** as CSV files  
- **Integration with Tableau** for data visualization and analytics

---

## ⚙️ Components

### **1. MENU / CLI**
The user interacts with the system through a simple command-line interface to:
- Create and manage stock tickets (company names)
- Insert new market operation data
- Update, view, or delete records
- Export reports to CSV

---

### **2. DATABASE (SQLite)**
All data is stored locally using SQLite for reliability and simplicity.

#### Tables:
- **TICKET**
  - Stores company names (stock identifiers)
- **OPERATIONS**
  - Fields include:
    - `IdOperation`
    - `TICKET`
    - `DATE` and `TIME`
    - `OPEN`, `HIGH`, `LOW`, `CLOSE` prices
    - `VOLUME` quantity

---

### **3. REPORTS**
The system generates structured **CSV reports** including:
- Company list (A–Z)
- Reports by **ticket**, **year**, **month**, **week**, and **day**
- Aggregated **operation reports**

These CSVs can be easily imported into **Tableau** for visualization and deeper insights.

---

### **4. VISUALIZATION (Tableau)**
- The generated CSVs serve as data sources for Tableau dashboards.
- Allows you to explore trends, price fluctuations, and volume changes visually.

---

## 🧰 Tech Stack
- **Python** — core logic & CLI
- **SQLite** — database management
- **CSV** — report export format
- **Tableau** — visualization tool

---

## 🚀 Usage

1. Run the main menu:
   ```bash
   python main.py
   Choose CRUD options or reporting tools.

2. Export reports as .csv.

3. Import the CSVs into Tableau for interactive dashboards.

<img width="721" height="814" alt="image" src="https://github.com/user-attachments/assets/9768564a-9fb5-4ba4-8542-e8b4d2758407" />
