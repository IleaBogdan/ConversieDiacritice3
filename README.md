# Diacritics Converter (3rd Iteration)

A tool to convert broken diacritic characters in subtitle files to their non-diacritic equivalents.

## Installation Guide

1. Clone this repository or download it as a ZIP and extract it
2. Run the `compile.bat` file to compile the program
3. After compilation, navigate to the subtitle file you want to convert
4. Set the program as default application to open subtitle files:
   - Right-click on a subtitle file (.srt or other supported format)
   - Select "Open with" → "Choose another app"
   - Select the generated `.exe` file from this program
   - Check "Always use this app to open .[file extension] files"

*Note:* Windows 11 or higer and Python 3.13 or higher needed.

## Customization

You can modify which characters get converted by editing the `map.json` file. The file contains mappings between diacritic characters and their replacements in the format:

```json
{
    "original_char": "replacement_char"
}
```
## Development History

This is the third iteration of this tool, created after encountering encoding issues and file reading problems with previous C# implementations. Python proved more reliable for handling these cases in testing.

Previous versions:
- [Second iteration (C#)](https://github.com/IleaBogdan/ConversieDiacritice2)
- [Second iteration with more functionalities (C#)](https://github.com/IleaBogdan/SubtitleFixer)

For all test cases so far, the Python implementation has worked most reliably.
