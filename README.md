# 🔑 Password Cracking & Analyzer Tool

![GitHub Stars](https://img.shields.io/github/stars/your-username/password-security-lab?style=social)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

> **💡 Unlock the secrets of password security!** This web utility, built with **Python & Flask**, offers an interactive deep-dive into password cracking simulations and robust strength analysis. Discover how strong your passwords truly are and the science behind their security.

|-------------------------------------------------------------------------|

## ✨ Features That Empower You 

Our tool is divided into two powerful, interconnected sections, each designed to educate and inform.

### 🔬 Password Strength Analyzer: Your Digital Security Report

Get instant, comprehensive feedback on your password's resilience.

| Feature | Description |
| :------------------------- | :------------------------------------------------------------------------------------------------------- |
| ✅ **5-Point Scoring** | Evaluates passwords against 5 critical criteria: **Length ($\ge 8$), Uppercase, Lowercase, Digit, Symbol.** |
| 🏆 **Intuitive Tiers** | Categorizes strength as **Strong** 🟢, **Moderate** 🟠, or **Weak** 🔴 for quick understanding.             |
| ⏳ **Real-time Crack Time** | Calculates theoretical **Entropy** and estimates brute-force time using modern hardware assumptions.      |
| 💾 **Dynamic Dictionary** | Every analyzed password is **automatically saved** to `password.txt`, enhancing future simulations!        |
| 📚 **Data Structure Demo** | Witness the practical application of a **History Queue** (`collections.deque`) and a **Stack Simulation**. |

### ⚡ Cracking Simulation: The Race Against Time

Understand the efficiency of password attacks by seeing them in action.

* 🚀 **Algorithm Showdown:** Visually compare **Linear Search** ($O(n)$ - brute-force) against **Binary Search** ($O(\log n)$ - optimized) on our dynamic dictionary.
* ⏱️ **Performance Metrics:** Witness the dramatic difference in **"Number of Attempts"** and **"Time Taken"** between algorithms. It's a clear lesson in computational efficiency!

---

## 🏗️ Technology Stack 

Built with robust and popular technologies to ensure a smooth and educational experience.

| Component         | Technology              | Role                                                                |
| :---------------- | :---------------------- | :------------------------------------------------------------------ |
| **Backend Core** | **Python 3.8+** | Powers all logic, algorithms, and security calculations.            |
| **Web Framework** | **Flask** | The micro-framework handling web routing and serving.               |
| **Data Handling** | **`collections.deque`** | Efficiently manages the real-time history queue (FIFO).             |
| **Frontend UI** | **HTML5, Custom CSS3** | Delivers a sleek, responsive, and professional dark-themed interface. |

---

## 🚀 Quick Start 

Get the Password Cracking & Analyzer Tool up and running in minutes!

### Prerequisites 

Make sure you have **Python 3.x** installed on your system.

### 1\. Clone the Repository

```bash
git clone [https://github.com/ayusjakhmola25/Password-Cracking-Analyzer-Tool.git]
```
> _(Remember to replace `ayusjakhmola25` with your actual GitHub username!)_

### 2\. Set Up Your Environment

Create and activate a virtual environment to manage dependencies cleanly.

```bash
python -m venv venv
# For Linux/macOS
source venv/bin/activate
# For Windows (Command Prompt)
.\venv\Scripts\activate
```

### 3\. Install Dependencies

Only Flask is required!

```bash
pip install Flask
```

### 4\. Launch the Application

Run the Flask server from your project root:

```bash
python app.py
```

🎉 The application will now be live in your browser at: **`http://127.0.0.1:5001/`**

---

## 🎯 How To Use 

### 📊 Strength Analyzer

1.  Navigate to the **Strength Analyzer** tab.
2.  Type any password you wish to evaluate into the input field.
3.  Click **"Analyze Password"**.
4.  Observe its detailed **Strength Rating**, **Estimated Crack Time**, and watch it automatically appear in your **History Queue** and the internal dictionary!

### ⚙️ Cracking Simulation

1.  Switch to the **Cracking Simulation** tab.
2.  Enter a password. (For best results, use a password already in `password.txt` – either a default one or one you just analyzed).
3.  Click **"Start Simulation"**.
4.  Witness the powerful visual comparison as Linear Search and Binary Search race to find your password, highlighting the stark difference in efficiency!

---

## 🤝 Contribute To The Project 

Your contributions make the open-source community thrive! We welcome all improvements.

1.  **Fork** the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  **Push** to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a **Pull Request**.

---

## 📜 License

Distributed under the MIT License. See the `LICENSE` file for more information.

<p align="center">
  Built with 💙 for Cybersecurity Education
</p>
