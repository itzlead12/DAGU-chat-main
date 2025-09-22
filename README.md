<h1 align="center">Dagu</h1>  
<p align="center">  
<img src="https://img.shields.io/badge/Project-Secure_Chat-blue?style=for-the-badge" align="center">  
<img src="https://img.shields.io/badge/Language-Python-red?style=for-the-badge" align="center">  
<img src="https://img.shields.io/badge/Framework-Flask-green?style=for-the-badge" align="center">  
</p>

---

## **About Dagu**  
**Dagu** is a next-generation secure chat platform inspired by the Ethiopian *Dagu* (trusted word-of-mouth communication system). It provides a **quantum-inspired secure messaging system** where users can **register, login, and exchange encrypted messages** using a **web interface**.  

> ⚠️ **Disclaimer:** This is a simplified **prototype** demonstrating secure messaging and quantum-inspired encryption. A full-scale system would include **cross-platform clients, real Quantum Key Distribution (QKD),** and advanced features.

---

## **Database Models**

| **Model Name** | **Columns** |
|----------------|-------------|
| **User**       | `id`, `username`, `email`, `password_hash`, `last_online` |
| **Messages**   | `id`, `sender_id`, `receiver_id`, `message_text`, `timestamp` |

---

## **Features**  

- **Quantum-Inspired Encryption:** Messages are encrypted with keys derived from **quantum-safe algorithms**.  
- **End-to-End Secure Chat:** Messages are protected against **classical and quantum attacks**.  
- **Web Interface:** Simple and responsive **UI** accessible on desktop and mobile browsers.  
- **User Authentication:** Secure **registration, login, and logout** with hashed passwords.  

---

## **Tech Stack**  

- **Frontend:** HTML + CSS templates (Flask web interface)  
- **Backend:** Flask (Python) for user management, messaging, and encryption  
- **Database:** SQLite  
- **Encryption Layer:** Quantum-inspired symmetric cryptography (Python)  

---

## **Team**  

- **Paulos Berihun** – Backend Developer & Web Integration  
- **Haileab Mulugeta** – Quantum Encryption & Security  
