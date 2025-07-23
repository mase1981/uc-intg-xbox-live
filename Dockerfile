# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY ./pyproject.toml ./
COPY ./uc_intg_xbox_live ./uc_intg_xbox_live

# Install the project and its dependencies
RUN pip install .

# Command to run when the container starts
CMD ["python", "-m", "uc_intg_xbox_live.driver"]