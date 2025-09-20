import random
from setuptools import setup, find_packages

# 🕵️ RiskLab easter egg
messages = [
    "Frank Abagnale would be proud 😉",
    "fly by night, disappear by morning... 🕵️‍♂️",
    "some risks are calculated… some are stolen 💼",
    "follow the numbers, trust no one… 📝",
    "catch me if you can… but the risk always follows ⚡"
]

print(random.choice(messages))

setup(
    name="RiskLab",
    version="0.1.0",
    author="Youcef Chalbi",
    author_email="youcefchalbi39@gmail.com", 
    description="A modular financial risk analysis toolkit with dashboards, risk matrices, and stress testing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Youcef3939/RiskLab",  
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.1",
        "numpy>=1.27",
        "scipy>=1.12",
        "yfinance>=0.2.30",
        "matplotlib>=3.8",
        "seaborn>=0.12",
        "plotly>=6.1",
        "streamlit>=1.25",
        "jinja2>=3.1",
        "pdfkit>=1.0.0"
    ],
    extras_require={
        "dev": ["pytest>=8.2", "black>=24.3", "flake8>=6.1", "jupyter>=1.0"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "risklab-dashboard=dashboard:main",  
        ],
    },
)
