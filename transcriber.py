import math
import collections

class RomanizedTranscriber:
    """
    A tool to transcribe romanized text back to its original non-latin characters
    using a dynamic programming algorithm based on word/phrase frequencies.

    This implementation uses the Viterbi algorithm to find the most probable
    sequence of characters given a continuous string of romanized syllables.
    The "probability" of a sequence is calculated as the sum of the log
    probabilities of its constituent words/phrases, making it a "simple model"
    that does not rely on n-gram transition probabilities between words.

    Author: G. Gemini
    """

    def __init__(self, frequency_data: list[tuple[str, str, int]]):
        """
        Initializes the transcriber with the language data.

        Args:
            frequency_data: A list of tuples, where each tuple contains:
                (original_word: str, romanized_spelling: str, frequency: int)
                Example: [("你好", "nihao", 5000), ("好", "hao", 10000)]
        """
        if not frequency_data:
            raise ValueError("Frequency data cannot be empty.")
        
        # This dictionary will store the pre-calculated log probabilities.
        # The key is the romanized string, and the value is a list of
        # tuples: (original_word, log_probability).
        self.log_prob_dict = self._build_log_prob_dict(frequency_data)
        
        # Find the maximum possible length of a romanized word in our dictionary.
        # This is an optimization to avoid checking excessively long substrings.
        self.max_word_len = max(len(pinyin) for pinyin in self.log_prob_dict.keys())


    def _build_log_prob_dict(self, frequency_data: list[tuple[str, str, int]]) -> dict:
        """
        Processes the raw frequency data into a lookup dictionary of log probabilities.
        Using log probabilities turns multiplication of probabilities into addition,
        which is numerically more stable and avoids floating-point underflow.
        """
        # Calculate the total frequency of all words/phrases in the corpus.
        total_frequency = sum(freq for _, _, freq in frequency_data)
        
        # defaultdict simplifies appending to lists for new keys.
        log_prob_dict = collections.defaultdict(list)
        
        for original_word, romanization, freq in frequency_data:
            if freq <= 0:
                # Frequencies must be positive to avoid log(0) errors.
                continue
            
            # P(word) = frequency(word) / total_frequency
            # We use the natural logarithm.
            log_prob = math.log(freq / total_frequency)
            log_prob_dict[romanization].append((original_word, log_prob))
            
        return dict(log_prob_dict)

    def transcribe(self, romanized_text: str) -> str:
        """
        Transcribes a romanized string into the most likely original character sequence.

        Args:
            romanized_text: The input string to transcribe (e.g., "dagongzuo").

        Returns:
            The most probable transcription (e.g., "大工作"). Returns an empty
            string if no valid transcription can be found.
        """
        n = len(romanized_text)
        
        # scores[i] stores the max log probability of a transcription for the prefix of length i.
        scores = [-float('inf')] * (n + 1)
        scores[0] = 0.0  # The probability of an empty string is 1, so log(1) = 0.

        # backpointers[i] stores the start index of the last word in the optimal path to i.
        backpointers = [0] * (n + 1)
        
        # best_words[i] stores the actual original character/word for that last segment.
        best_words = [''] * (n + 1)

        # --- Forward Pass: Build the probability lattice ---
        # Iterate through each possible end position in the string.
        for j in range(1, n + 1):
            # Iterate through each possible start position for a word ending at j.
            # We add an optimization to not check substrings longer than our longest known word.
            start_range = max(0, j - self.max_word_len)
            for i in range(start_range, j):
                substring = romanized_text[i:j]
                
                if substring in self.log_prob_dict:
                    # This substring is a valid romanization for one or more words.
                    for original_word, log_prob in self.log_prob_dict[substring]:
                        # The score of this path is the score to get to the start of
                        # the current word (scores[i]) plus the score of the current word itself.
                        candidate_score = scores[i] + log_prob
                        
                        # If we've found a better path to position j, update our tables.
                        if candidate_score > scores[j]:
                            scores[j] = candidate_score
                            backpointers[j] = i
                            best_words[j] = original_word
        
        # --- Backtracking: Reconstruct the best path ---
        if scores[n] == -float('inf'):
            # This means no valid sequence of words from our dictionary can form the input string.
            print(f"Warning: Could not find a valid transcription for '{romanized_text}'.")
            return ""
            
        result = []
        current_pos = n
        while current_pos > 0:
            # Get the word that ended at the current position.
            word = best_words[current_pos]
            result.append(word)
            # Jump back to the start of that word.
            current_pos = backpointers[current_pos]
        
        # The result was built backwards, so we reverse it.
        result.reverse()
        
        return "".join(result)

# --- Validation Section ---
if __name__ == "__main__":
    # 1. Define sample data for validation (using Chinese Pinyin as an example).
    # This data is designed to test ambiguity resolution.
    sample_frequency_data = [
        # Single characters
        ("大", "da", 150),
        ("打", "da", 100), # "大" is more frequent than "打"
        ("工", "gong", 200),
        ("作", "zuo", 190),
        ("西", "xi", 80),
        ("安", "an", 90),
        ("先", "xian", 120),
        
        # Phrases / Proper Nouns
        # The phrase "工作" is very frequent, more so than "工" and "作" separately.
        ("工作", "gongzuo", 500),
        # The city "西安" is a very frequent phrase.
        ("西安", "xian", 250),
    ]

    # 2. Instantiate the transcriber with our data.
    print("Initializing transcriber with sample data...")
    transcriber = RomanizedTranscriber(sample_frequency_data)
    print("Initialization complete.\n")

    # 3. Define test cases.
    test_cases = [
        "dagongzuo",
        "xian",
        "xianan",
        "dazuogong"
    ]

    # 4. Run tests and explain the results.
    for text in test_cases:
        transcribed_text = transcriber.transcribe(text)
        print(f"Input:           '{text}'")
        print(f"Transcribed:     '{transcribed_text}'")
        
        if text == "dagongzuo":
            print("Explanation:     The algorithm had two main choices:")
            print("                 1. 'da' | 'gongzuo'  -> 大 | 工作")
            print("                 2. 'da' | 'gong' | 'zuo' -> 大 | 工 | 作")
            print("                 Because the frequency of the combined phrase '工作' (500) is much higher")
            print("                 than the individual frequencies of '工' (200) and '作' (190), the first path was chosen as more probable.")
        
        elif text == "xian":
            print("Explanation:     The algorithm chose between the single character '先' (freq 120) and the")
            print("                 proper noun '西安' (freq 250). Since '西安' has a higher frequency, it was chosen.")

        elif text == "xianan":
            print("Explanation:     The algorithm correctly segmented the string into 'xian' | 'an',")
            print("                 resulting in '西安' (the most likely 'xian') followed by '安'.")

        elif text == "dazuogong":
            print("Explanation:     Here, no combined phrase exists. The algorithm finds the best sequence")
            print("                 of individual characters: 'da' -> '大' (more frequent than '打'), 'zuo' -> '作', 'gong' -> '工'.")
            
        print("-" * 25)