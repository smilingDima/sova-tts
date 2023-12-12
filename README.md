# SOVA TTS

SOVA TTS is a speech syntthesis solution based on [Tacotron 2](https://arxiv.org/abs/1712.05884) architecture. It is designed as a REST API service and it can be customized (both code and models) for your needs.

## Installation

The easiest way to deploy the service is via docker-compose, so you have to install Docker and docker-compose first. Here's a brief instruction for Ubuntu:

#### Build and deploy

*   Clone the repository, download the pretrained models archive and extract the contents into the project folder:
```bash
git clone --recursive https://github.com/smilingDima/sova-tts.git
cd sova-tts/
wget http://dataset.sova.ai/SOVA-TTS/Data_v1.1.tar
tar -xvf Data_v1.1.tar && rm Data_v1.1.tar
```

*   Build docker image
    <!-- *   Build *sova-tts-gpu* image if you're planning on using GPU:
     ```bash
     sudo docker-compose build sova-tts-gpu
     ``` -->
     *   Build *sova-tts* image if you're planning on using CPU:
     ```bash
     sudo docker-compose build sova-tts
     ```

*	Run the desired service container
     <!-- *   GPU:
     ```bash
     sudo docker-compose up -d sova-tts-gpu
     ``` -->
     *   CPU:
     ```bash
     sudo docker-compose up -d sova-tts
     ```

## Testing

To test the service you can send a POST request:
```bash
curl --request POST 'http://localhost:8899/synthesize/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "Добрый день! Как ваши дел+а?",
    "voice": "Natasha"
}'
```

## Acknowledgements

Original [Tacotron 2](https://github.com/NVIDIA/tacotron2) implementation by NVIDIA.
