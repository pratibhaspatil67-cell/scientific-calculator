# Scientific Calculator with DevOps Pipeline

## Project Overview
This is a **Scientific Calculator** implemented as a Python command-line application, demonstrating a complete DevOps pipeline.  
The calculator supports:

- Square root function: `√x`
- Factorial function: `x!`
- Natural logarithm: `ln(x)`
- Power function: `x^b`
- Other basic arithmetic operations

This project showcases a full **DevOps workflow**:

1. Version control with **GitHub**.
2. Testing using **PyTest**.
3. Docker image creation and push to **Docker Hub**.
4. Continuous integration using **Jenkins**.
5. Deployment on a local VM using **Ansible**.

---

## DevOps Pipeline Flow

1. **Push code to GitHub** → triggers webhook → Jenkins pipeline starts.  
2. **Jenkins pipeline** executes stages:
   - Checkout code
   - Install dependencies & run tests
   - Build Docker image
   - Docker login & push to Docker Hub
   - Deploy container using Ansible
   - Send email notification on success/failure (optional)
3. **Ansible** pulls the image and runs it as a container on the target machine (port `5000`).

---
