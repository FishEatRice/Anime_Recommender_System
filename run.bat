@echo off
echo Install Streamlit...

pip install streamlit
pip install scikit-learn
pip install fuzzywuzzy
pip install python-Levenshtein
pip install streamlit-scroll-to-top

echo Start Application

cls

streamlit run main.py

pause
