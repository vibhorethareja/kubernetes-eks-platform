from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Flask on Kubernetes</h1>
    <p>Deployed on AWS EKS via Helm and GitHub Actions</p>
    <p>Auto-scaling with Horizontal Pod Autoscaler</p>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "pod": socket.gethostname(),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }), 200

@app.route("/info")
def info():
    return jsonify({
        "app": "flask-k8s",
        "pod_name": socket.gethostname(),
        "namespace": os.getenv("POD_NAMESPACE", "default"),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)