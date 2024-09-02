# OCR_Braille
An application that performs OCR on a directory of images through techniques of text detection, text recognition and layout analysis. Then translates the text into braille.

## Installation


```bash
pip install -r requirements.txt
```

## Running the script

```bash
python main.py -d /path/to/images --segment True --language fr --analyse False
```

## With docker 

1. Building
```bash
docker build -t ocr_app:wt .
```
2.Running the container
```bash
docker run -e LANGUAGE=en \
-e DIRECTORY=/app/to_test \ 
-v $(pwd)/to_test:/app/to_test \
-v $(pwd)/outputs:/app/outputs 
ocr_app:wt
```




