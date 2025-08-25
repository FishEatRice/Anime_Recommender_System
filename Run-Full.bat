@echo off
echo Install Streamlit...

pip install streamlit
pip install scikit-learn
pip install fuzzywuzzy
pip install python-Levenshtein

echo Start Application

cls

streamlit run Full.py

pause
