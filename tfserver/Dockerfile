FROM tensorflow/serving:latest-gpu


# TODO: This is a temporary fix to deal with stupid tfhub shit.
# Needs to be fixed. We should not be depending on the tfhub cache
COPY .tfhub_modules /tmp/tfhub_modules

WORKDIR /home/app
COPY . .

# Don't hardcode this.
CMD ["--rest_api_port=8501", "--model_name=simpleBERT", "--model_base_path=/home/app/models/simpleBERT"]


