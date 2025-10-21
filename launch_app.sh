#!/bin/bash
# Launch the Ethiopian School Financial Modeling App

echo "🎓 Ethiopian School Financial Modeling App"
echo "=========================================="
echo ""
echo "Starting web application..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd /home/user/FINMOD
streamlit run app.py
