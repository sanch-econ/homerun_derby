FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app .

# Expose the port that Streamlit runs on
EXPOSE 8501

CMD ["streamlit","run", "main.py"]

