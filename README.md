Here’s the content rewritten in **Markdown** for your `README.md` file:

```markdown
# OCR_Braille

OCR_Braille is an application that performs OCR on a directory of images, utilizing techniques such as text detection, text recognition, and layout analysis. The extracted text is then translated into Braille.

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Running the Script Directly

To run the OCR_Braille script directly, use the following command:

```bash
python main.py -d /path/to/images --segment True --language fr --analyse False
```

- **-d**: Specify the path to the directory containing images.
- **--segment**: Enable or disable segmentation (True/False).
- **--language**: Specify the language of the text (e.g., 'fr' for French).
- **--analyse**: Enable or disable layout analysis (True/False).

### 2. Using Docker

#### 1. Building the Docker Image

To build the Docker image, run:

```bash
docker build -t ocr_app:wt .
```

#### 2. Running the Docker Container

To run the OCR_Braille application within a Docker container, use the following command:

```bash
docker run -e LANGUAGE=en \
           -e DIRECTORY=/app/to_test \
           -v $(pwd)/to_test:/app/to_test \
           -v $(pwd)/outputs:/app/outputs \
           ocr_app:wt
```

- **-e LANGUAGE**: Set the language environment variable (e.g., 'en' for English).
- **-e DIRECTORY**: Set the directory environment variable for the input images.
- **-v**: Bind mount the directories for input images and output results.
```

This format is ready to be placed in a `README.md` file for your **OCR_Braille** project.
