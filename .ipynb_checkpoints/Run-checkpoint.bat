@echo off
echo Install Streamlit...

pip install streamlit
pip install scikit-learn

echo Start Application

cls

streamlit run main.py

pause
