#!/usr/bin/env python3
"""
Basic usage examples
"""

from jyutping2characters import transcribe

jyutping = "zou6jan4jyu4gwo2mou5mung6soeng2tung4tiu4haam4jyu2jau5me1fan1bit6" # 做人如果冇夢想同條鹹魚有咩分別

print(f"Original jyutping:\t{jyutping}")
print(f"Transcription result:\t{transcribe(jyutping)}")
