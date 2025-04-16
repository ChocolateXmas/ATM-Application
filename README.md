<a id="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">ATM Application</h1>

  <p align="center">
    Shell UI ATM Aplication
    <br />
    <br />
    <a href="">🐞 Report Bug</a>
    &middot;
    <a href="">✨ Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project 📝</a>
      <ul>
        <li><a href="#built-with">Built With 🛠️</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started 🚀</a>
      <ul>
        <li>
            <a href="#prerequisites">Prerequisites ⚡</a>
            <ul>
                <li><a href="#system-requirements">System Requirements 🖥️</a></li>
                <li><a href="#required-permissions">Required Permissions 🔑</a></li>
                <li><a href="#dependencies">Dependencies ℹ️</a></li>
            </ul>
        </li>
        <li><a href="#installation">Installation 🔧</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
<a id="about-the-project"></a>

## About The Project 📝

An interactive console-based ATM application that allows users to perform essential banking operations, including deposits, withdrawals, balance inquiries, and account management.
The system supports multiple predefined users with unique PIN codes and balances.
Users can securely log in, navigate an intuitive menu, and perform transactions with built-in validation to ensure proper cash handling.
The ATM enforces rules such as deposit multipliers (20, 50, or 100) and withdrawal limits based on available balance.
Additionally, advanced features include PIN code updates and a receipt generation option, enhancing user experience.
The project is structured using loops, lists, and functions for efficient program flow.

<!-- BUILT WITH -->
<a id="built-with"></a>

## Built With 🛠️

- [![Python Badge][python-badge]][python-url]  
- [![Curses Badge][curses-badge]][curses-url]

<!-- INSTALLATION -->
<a id="Installation 🔧"></a>

## Installation 🔧


### 📁 Step 1: Clone the Repository
```bash
git clone https://github.com/ChocolateXmas/ATM-Application.git
cd ATM-Application
```

---

### 🔐 Step 2: Set Up Docker Secrets
We **don't include passwords** directly in this repo for security reasons. Instead, we provide `.example` files. You need to copy and fill them in:

```bash
cp secrets/db_host.txt.example secrets/db_host.txt
cp secrets/db_name.txt.example secrets/db_name.txt
cp secrets/db_password.txt.example secrets/db_password.txt
cp secrets/db_root_password.txt.example secrets/db_root_password.txt
cp secrets/db_root_user.txt.example secrets/db_root_user.txt
cp secrets/db_user_password.txt.example secrets/db_user_password.txt
cp secrets/db_user.txt.example secrets/db_user.txt
```

Then open each file and add your own secure credentials:
```
# secrets/db_root_password.txt
MySuperSecretRootPass123

# secrets/db_user_password.txt
MyUserSecurePassword456
```

> ⚠️ Do not commit these secrets to Git!

---

### 🐳 Step 3: Run the Project with Docker Compose
#### Option 1 - Automatically:

- Runs the interactive shell menu automatically

```bash
docker compose run --rm app
```
#### Option 2 - Manually:
1. 
verbosely:
```bash
docker compose up --build
```
or 
detached:
```bash
docker compose up  --build -d
```
2. run the interactive menu shell
```bash
docker exec -it atm_app python3 main.py
```
---

This will:
- Build the Python app container (`main.py`)
- Start a MySQL container
- Mount secrets securely inside the containers
- Initialize your database using `schema.sql`

### ✅ Optional: Test Access to Secrets Inside Containers
To check if the secrets are loaded correctly:
```bash
docker exec -it atm_app_container_name cat /run/secrets/db_user_password
```

---

### 🧪 Development Tips
- Edit your code on a feature/develop branch (like `feat-sql-integration / develop`)
- Use Docker secrets for local dev, staging, and prod
- Never commit real credentials into GitHub

---

[python-badge]: https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-icon]: https://img.shields.io/badge/-3776AB?style=flat-square&logo=python&logoColor=white
[python-url]: https://www.python.org/

[curses-badge]: https://img.shields.io/badge/curses-000000?style=for-the-badge&logo=terminal&logoColor=white
[curses-icon]: https://img.shields.io/badge/-000000?style=flat-square&logo=terminal&logoColor=white
[curses-url]: https://docs.python.org/3/library/curses.html