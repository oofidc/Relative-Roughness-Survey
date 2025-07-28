# Relative Roughness Survey

A web application built with Streamlit to collect user ratings on the relative roughness of surfaces in images. The application implements a weighted randomization algorithm to ensure comprehensive coverage of image comparisons.

## Features

- Display 5 random images for comparison
- Collect user ratings (1-5) for surface roughness
- Weighted randomization to prioritize less-compared image pairs
- JSON export of survey results
- Session history tracking
- Input validation to ensure unique ratings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Relative_Roughness_Survey.git
cd Relative_Roughness_Survey
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Project Structure

- `main.py` - Main Streamlit application
- `weighted_randomness.py` - Weighted randomization algorithm implementation
- `Sample_Images/` - Directory containing surface images
- `Anonymized_Relative_Roughness_Survey_Results.json` - Survey results storage

## Usage

1. Launch the application using Streamlit
2. Rate each image from 1 (lowest roughness) to 5 (highest roughness)
3. Submit ratings using the "Submit Rankings" button
4. View your session history in JSON format
5. Get new images using the "Get More Images" button

## Algorithm

The weighted randomization algorithm:
- Tracks frequency of image pair comparisons
- Assigns higher weights to less-compared pairs
- Ensures balanced coverage of all images
- Falls back to random selection if no weighted pairs are available

## Requirements

- Python 3.7+
- Streamlit
- pathlib
- fsspec

## Contributing

This is a research project for collecting surface roughness data. Please contact [Ndiana Obot](mailto:ndianaobot8@gmail.com) for more information.
