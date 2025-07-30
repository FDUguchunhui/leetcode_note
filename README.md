# LeetCode Anki Flashcard Generator

Automatically generate Anki flashcards from a list of LeetCode problems using OpenAI's GPT models. This tool creates structured flashcards with problem descriptions, solution approaches, and complexity analysis.

## Features

- 🤖 **AI-Powered**: Uses OpenAI GPT to generate high-quality flashcards
- 📚 **Batch Processing**: Process multiple LeetCode problems at once
- 📊 **Structured Output**: Creates CSV files ready for Anki import
- 🎯 **Optimized Content**: Includes both brute force and optimized solutions
- ⚡ **Fast Processing**: Handles 135+ problems efficiently

## Setup

### Prerequisites

- Python 3.13 or higher
- OpenAI API account and API key

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd leetcode_anki
```

2. Install dependencies using uv (recommended):
```bash
uv install
```

Or using pip:
```bash
pip install -r requirements.txt
```

### Environment Configuration

**⚠️ IMPORTANT: You must create a `.env` file and add your OpenAI API key**

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

To get an OpenAI API key:
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

## Usage

### Quick Start

Run the main script to process all problems in `leetcode_problems.txt`:

```bash
python main.py
```

This will:
1. Test the format with a single question
2. Process all 135+ problems from the problems list
3. Generate `leetcode_flashcards.csv` ready for Anki import

### Customizing Problem List

Edit `leetcode_problems.txt` to include your desired problems. Format each line as:
```
<number>. <title> (<difficulty>)
```

Example:
```
1. Two Sum (easy)
215. Kth Largest Element in an Array (medium)
76. Minimum Window Substring (hard)
```

### Testing Single Questions

To test the output format for a single problem:

```python
from main import test_single_question
test_single_question('1. Two Sum (easy)')
```

## Flashcard Format

Each generated flashcard contains:

### Front Side
- Problem title with number and difficulty
- Problem description
- Sample test cases

### Back Side
- Brute force approach and time complexity
- Optimized solution approach and time complexity
- Key points to remember
- No code (focuses on understanding concepts)

## Output

The script generates `leetcode_flashcards.csv` with two columns:
- **Front**: Problem description and examples
- **Back**: Solution approaches and complexity analysis

### Importing to Anki

1. Open Anki
2. File → Import
3. Select `leetcode_flashcards.csv`
4. Map fields: Front → Front, Back → Back
5. Import as new deck or add to existing deck

## Configuration

### Model Selection

The default model is `gpt-4o-search-preview`. You can change this in the `get_completion()` function:

```python
def get_completion(prompt, model="gpt-4o-search-preview"):
```

### Customizing Flashcard Content

Modify the `system_prompt` in `get_completion()` to change the flashcard format and content structure.

## Project Structure

```
leetcode_anki/
├── main.py                    # Main application script
├── leetcode_problems.txt      # List of problems to process
├── leetcode_flashcards.csv    # Generated flashcards (after running)
├── pyproject.toml            # Project dependencies
├── .env                      # Environment variables (you create this)
└── README.md                 # This file
```

## Troubleshooting

### Common Issues

1. **OpenAI API Error**: Ensure your API key is correct and you have sufficient credits
2. **Empty Flashcards**: Check that problem names in `leetcode_problems.txt` match LeetCode format
3. **Parsing Errors**: The script handles malformed responses gracefully and continues processing

### Error Handling

The script includes robust error handling:
- Failed API calls are logged and marked in the output
- Malformed responses are captured with error messages
- Processing continues even if individual problems fail

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license here]

## Support

If you encounter issues:
1. Check that your `.env` file contains a valid OpenAI API key
2. Verify your OpenAI account has sufficient credits
3. Ensure problem names in `leetcode_problems.txt` are properly formatted

---

**Happy studying! 🚀**
