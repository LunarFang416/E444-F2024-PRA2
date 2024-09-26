# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose port 5000 for Flask
EXPOSE 5000

# Step 6: Define environment variable for Flask to run
ENV FLASK_APP=hello.py

# Step 7: Command to run the Flask application (with hot-reloading for development)
CMD ["flask", "run", "--host=0.0.0.0"]
