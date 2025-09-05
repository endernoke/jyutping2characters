# Jyutping Transcriber

Convert Jyutping romanization to Traditional Chinese characters using advanced dynamic programming algorithms.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

**Jyutping Transcriber** is a high-performance Python library that converts Jyutping romanization (the standard romanization system for Cantonese) into Traditional Chinese characters. It uses a sophisticated dynamic programming algorithm (Viterbi) to find the most probable sequence of Chinese characters based on word frequencies from real-world usage data.

### Key Features

- 🚀 **High Performance**: Singleton pattern ensures fast repeated transcriptions
- 🎯 **Accurate**: Uses frequency-based optimization for realistic results  
- 📊 **Rich Data**: Built from 300K+ entries from authoritative sources
- 🔄 **Auto-updating**: Fresh data downloaded from online sources
- 🛠️ **Easy to Use**: Simple API with sensible defaults
- ⚡ **CLI Tool**: Command-line interface for quick transcriptions

## Installation

```bash
pip install jyutping-transcriber
```

## Logging Configuration

This library uses Python's standard `logging` module for informational messages and debugging. By default, logging is disabled to keep the library quiet during normal use.

### Enabling Logging

To see informational messages (data loading, initialization, etc.):

```python
import logging
logging.basicConfig(level=logging.INFO)

# Now library operations will show progress
from jyutping_transcriber import transcribe
result = transcribe("ngo5oi3nei5")  # Will show initialization messages
```

### Disabling All Logging

To completely silence the library:

```python
import logging
logging.getLogger('jyutping2characters').setLevel(logging.CRITICAL)

# Library will be completely silent
from jyutping_transcriber import transcribe
result = transcribe("ngo5oi3nei5")  # No output to stdout
```

### Debug Logging

For detailed debugging information (useful for development):

```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Shows detailed data processing steps, downloads, etc.
```

## ⚠️ First Run Notice

**Important**: On first use, this library will download and process mapping data from online sources. This process takes 1-2 minutes but only happens once. The data is then cached locally for instant subsequent use.

## Quick Start

```python
from jyutping_transcriber import transcribe

# Simple transcription
result = transcribe("ngo5oi3nei5")
print(result)  # 我愛你

# More examples
print(transcribe("gam1jat6"))        # 今日
print(transcribe("m4goi1"))          # 唔該
print(transcribe("hou2leng3"))       # 好靚
print(transcribe("zaa2"))            # 早晨 (morning greeting)
```

## Advanced Usage

### Pre-warming for Production

```python
from jyutping_transcriber import warmup, transcribe

# Pre-load data (recommended for production apps)
warmup()  # Takes 1-2 minutes on first run

# All subsequent calls are instant
transcribe("nei5hou2")  # 你好
```

### Custom Transcriber Instances

```python
from jyutping_transcriber import JyutpingTranscriber

# Create custom instance with your own data
custom_data = [
    ("你好", "nei5hou2", 1000),
    ("再見", "zoi3gin3", 800),
    # ... more entries
]

transcriber = JyutpingTranscriber(custom_data)
result = transcriber.transcribe("nei5hou2")
```

## Command Line Interface

The package includes a powerful CLI tool:

```bash
# Transcribe text
jyutping-transcriber transcribe "ngo5oi3nei5"

# Pre-warm the transcriber
jyutping-transcriber warmup

# Rebuild data cache with latest online data
jyutping-transcriber build-data

# Clear cached data
jyutping-transcriber clear-cache

# Show information and statistics
jyutping-transcriber info
```

## How It Works

The transcriber uses a **Viterbi algorithm** (dynamic programming) to find the most probable sequence of Chinese characters for a given Jyutping input. Here's the process:

1. **Data Sources**: Combines authoritative sources:
   - [LSHK Jyutping Table](https://github.com/lshk-org/jyutping-table) - Character mappings
   - [Rime Cantonese](https://github.com/rime/rime-cantonese) - Word frequencies and dictionary

2. **Probabilistic Modeling**: Each word/character has a probability based on real-world usage frequency

3. **Optimal Segmentation**: The algorithm finds the segmentation that maximizes the total probability

### Example Algorithm Behavior

```python
# Input: "gam1jat6hou2leng3"
# Possible segmentations:
# 1. "gam1" + "jat6" + "hou2" + "leng3" → "今" + "日" + "好" + "靚"
# 2. "gam1jat6" + "hou2leng3" → "今日" + "好靚" (chosen - higher probability)

result = transcribe("gam1jat6hou2leng3")
print(result)  # "今日好靚" (Today is beautiful)
```

## Performance

- **Initialization**: ~1-2 minutes (first run only)
- **Subsequent calls**: ~1ms per transcription
- **Memory usage**: ~50MB for full dataset
- **Data size**: ~300K entries, ~16MB cached file

## Data Management

### Cache Location

Data is cached in your system's standard cache directory:
- **Linux**: `~/.cache/jyutping_transcriber/`
- **macOS**: `~/Library/Caches/jyutping_transcriber/`
- **Windows**: `%LOCALAPPDATA%\jyutping_transcriber\`

### Updating Data

```python
from jyutping_transcriber import clear_cache

# Force rebuild with latest data
clear_cache()
# Next transcription will rebuild data
```

## API Reference

### Main Functions

#### `transcribe(text: str) -> str`
Convert Jyutping text to Chinese characters.

**Parameters:**
- `text`: Jyutping romanization string

**Returns:** Traditional Chinese characters

#### `warmup() -> None`  
Pre-initialize the global transcriber instance.

#### `clear_cache() -> None`
Clear cached data and force rebuild on next use.

### Classes

#### `JyutpingTranscriber`
Core transcriber class for advanced usage.

**Methods:**
- `__init__(frequency_data: List[Tuple[str, str, float]])`: Initialize with custom data
- `from_file(data_path: str)`: Create from JSON data file  
- `transcribe(text: str) -> str`: Transcribe Jyutping to Chinese

## Jyutping Reference

This library uses standard Jyutping romanization. Key points:

- **Tones**: Represented by numbers 1-6 (e.g., `aa1`, `aa4`)
- **Initials**: Standard consonants (`b`, `p`, `m`, `f`, etc.)
- **Finals**: Vowel combinations (`aa`, `aai`, `au`, etc.)

Common examples:
- `nei5hou2` → 你好 (hello)
- `m4goi1` → 唔該 (thank you/excuse me)
- `zoi3gin3` → 再見 (goodbye)
- `hou2mei5` → 好美 (very beautiful)

## Contributing

We welcome contributions! Areas where help is needed:

1. **Testing**: More comprehensive test cases
2. **Documentation**: Examples and tutorials
3. **Performance**: Algorithm optimizations
4. **Data**: Additional data sources or validation

## Data Sources & Attribution

This project builds upon excellent open-source data:

- **[LSHK Jyutping Table](https://github.com/lshk-org/jyutping-table)**: Maintained by the Linguistic Society of Hong Kong
- **[Rime Cantonese](https://github.com/rime/rime-cantonese)**: Part of the Rime Input Method Engine project

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- Core transcription functionality  
- CLI interface
- Automatic data management
- Performance optimizations

---

**Note**: This library focuses on Traditional Chinese characters as commonly used in Hong Kong. For Simplified Chinese or other variants, additional processing may be needed.
