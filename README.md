# 🚀 CI/CD Pipeline for Flask (Backend) and Express (Frontend) Applications using Jenkins

## 📌 Project Overview

This project demonstrates a **complete CI/CD pipeline implementation** using **Jenkins** to automate the deployment of two independent applications:

* **Flask Backend Application**
* **Express Frontend Application**

Each application has its **own Jenkins pipeline**, enabling **independent deployment**, **dependency installation**, and **service restart using process managers**.

Deployment is triggered automatically via **GitHub Webhooks** on every push.

---

## 🏗️ Architecture

```
Developer Push → GitHub Repository → GitHub Webhook → Jenkins Pipeline
                                              ↓
                                           SSH Deploy
                                              ↓
                                        Application Server
                                              ↓
                      Flask → systemd restart | Express → pm2 restart
```

---

## 🖥️ Infrastructure Setup

### Jenkins Server (EC2-1)

* Jenkins installed using Docker
* Required Plugins:

  * Git Plugin
  * Pipeline Plugin
  * SSH Agent Plugin
  * Credentials Binding Plugin
  * GitHub Integration Plugin

### Application Server (EC2-2)

* Hosts both applications
* Flask managed by **systemd**
* Express managed by **pm2**

---

## 📂 Application Server Folder Structure

```
/home/ubuntu/
   flask-app/
       app.py
       requirements.txt
       venv/
   express-app/
       app.js
       package.json
```

---

## ⚙️ Runtime Setup

### 🔹 Flask Application Setup

```bash
sudo apt update
sudo apt install python3-venv -y

mkdir ~/flask-app
cd ~/flask-app
git clone https://github.com/<your-user>/flask-repo.git .

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create systemd Service

```bash
sudo nano /etc/systemd/system/flask-app.service
```

```ini
[Unit]
Description=Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/flask-app
ExecStart=/home/ubuntu/flask-app/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reexec
sudo systemctl enable flask-app
sudo systemctl start flask-app
```

---

### 🔹 Express Application Setup

```bash
sudo apt install nodejs npm -y
sudo npm install -g pm2

mkdir ~/express-app
cd ~/express-app
git clone https://github.com/<your-user>/express-repo.git .

npm install
pm2 start app.js --name express-app
pm2 save
pm2 startup
```

---

## 🔐 Jenkins Credential Configuration

Add SSH credential:

```
Manage Jenkins → Credentials → Global → Add Credentials
```

* Type: **SSH Username with Private Key**
* Username: `ubuntu`
* Credential ID: `app-server-ssh`

---

## 🔄 Jenkins Pipeline — Flask (Backend)

```groovy
pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/<your-user>/flask-repo.git'
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['app-server-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@<APP_SERVER_IP> "
                        cd ~/flask-app &&
                        git pull &&
                        source venv/bin/activate &&
                        pip install -r requirements.txt &&
                        sudo systemctl restart flask-app
                    "
                    '''
                }
            }
        }
    }
}
```

---

## 🔄 Jenkins Pipeline — Express (Frontend)

```groovy
pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/<your-user>/express-repo.git'
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['app-server-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@<APP_SERVER_IP> "
                        cd ~/express-app &&
                        git pull &&
                        npm install &&
                        pm2 restart express-app
                    "
                    '''
                }
            }
        }
    }
}
```

---

## 🔔 GitHub Webhook Configuration

For both repositories:

```
Settings → Webhooks → Add Webhook
```

* Payload URL:

```
http://<JENKINS_PUBLIC_IP>:8080/github-webhook/
```

* Content Type: `application/json`
* Trigger: **Push Event**

---

## 🧪 Optional Enhancements

### Add Testing Stage

Flask:

```groovy
stage('Test') {
    steps {
        sh 'pytest || true'
    }
}
```

Express:

```groovy
stage('Test') {
    steps {
        sh 'npm test || true'
    }
}
```

### Environment Variables

Manage secrets in Jenkins:

```
Manage Jenkins → Credentials
```

Use in pipeline:

```groovy
environment {
    API_KEY = credentials('api-key-id')
}
```

---

## ✅ Verification Checklist

On Application Server:

### Flask Service

```bash
sudo systemctl status flask-app
```

### Express Process

```bash
pm2 list
```

### Port Verification

```bash
ss -tulnp
```

### Browser Access

```
http://<APP_SERVER_IP>:8000
http://<APP_SERVER_IP>:3000
```

---

## 📸 Deliverables

* Jenkins Flask pipeline success screenshot
* Jenkins Express pipeline success screenshot
* GitHub webhook delivery screenshot
* `pm2 list` output screenshot
* `systemctl status flask-app` screenshot
* Application running in browser screenshot

---

## 🎯 Key Learnings

* Implemented **independent CI/CD pipelines**
* Automated deployment using **GitHub Webhooks**
* Used **systemd** for Python process management
* Used **pm2** for Node.js process supervision
* Achieved **secure remote deployment using SSH credentials in Jenkins**
* Ensured **idempotent deployments using git pull + dependency installation**

---

## 👨‍💻 Author

**Tanmay Agarwal**

DevOps CI/CD Assignment – Jenkins Pipeline Automation
