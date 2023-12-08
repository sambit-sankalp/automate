# Use a specific version of the python image
FROM python:3.11.6

# Set the working directory in the Docker image
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./model.py /app
COPY ./generated_data.csv /app

# Install required Python packages
# Pin the versions to ensure reproducibility
RUN pip install pandas scikit-learn

# Command to run when the container starts
# Here you should pass the input and output directory as arguments when you run the container
CMD ["python", "/app/model.py", "f01927170", "33.67", "6099", "110328", "110328", "0", "0"]