FROM tensorflow/serving:latest-gpu

WORKDIR /home/app
COPY . .

# Don't hardcode this.
CMD ["--rest_api_port=8501", "--model_name=simpleBERT", "--model_base_path=/home/app/models/simpleBERT"]


