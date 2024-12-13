# Use the official Python 3.12.8 image from the Docker Hub
FROM python:3.12.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Set the default command to run the main.py script
CMD ["python", "main.py"]
