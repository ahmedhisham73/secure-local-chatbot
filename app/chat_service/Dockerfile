FROM python:3.7-slim

# ✅ Step 1: Add build tools
RUN apt-get update && \
    apt-get install -y build-essential cmake && \
    apt-get clean

# ✅ Step 2: Create working directory
WORKDIR /app

# ✅ Step 3: Copy all app code
COPY . .

# ✅ Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5101

CMD ["gunicorn", "-b", "0.0.0.0:5101", "main:app"]


