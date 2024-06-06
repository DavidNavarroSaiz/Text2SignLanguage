import os
import difflib
import moviepy.editor as mp
import re

def tokenize_text(text):
    # Remove punctuation using regular expressions
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower().split()

def find_similar_word(word, word_list, cutoff=0.8):
    matches = difflib.get_close_matches(word, word_list, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def get_sign_file(word, word_list, base_dir='words'):
    similar_word = find_similar_word(word, word_list)
    if similar_word:
        mp4_file = os.path.join(base_dir, f'{similar_word}.mp4')
        if os.path.exists(mp4_file):
            return mp4_file
    
    letter_files = [os.path.join('alphabet', f'{letter}_small.gif') for letter in word]
    return letter_files

def create_sign_language_sequence(words, word_list):
    clips = []
    for word in words:
        sign_file = get_sign_file(word, word_list)
        if isinstance(sign_file, list):
            for letter_file in sign_file:
                letter_clip = mp.VideoFileClip(letter_file).set_duration(0.5)  # Set duration to 0.5 seconds for each letter
                clips.append(letter_clip)
        else:
            try:
                sign_clip = mp.VideoFileClip(sign_file)
                if sign_clip.duration > 0:
                    clips.append(sign_clip)
                else:
                    print(f"Warning: Video for '{word}' is empty or has zero duration.")
            except Exception as e:
                print(f"Error loading video file {sign_file}: {e}")
    
    if clips:
        final_clip = mp.concatenate_videoclips(clips, method="compose")
        return final_clip
    else:
        print("No clips to concatenate.")
        return None

def save_sign_language_video(sequence_clip, output_path):
    if sequence_clip:
        sequence_clip.write_videofile(output_path, codec="libx264")
    else:
        print("No sequence clip to save.")

def text_to_sign_language(text, output_path="output_2.mp4"):
    words = tokenize_text(text)
    word_list = [os.path.splitext(f)[0] for f in os.listdir('words') if f.endswith('.mp4')]
    sequence_clip = create_sign_language_sequence(words, word_list)
    save_sign_language_video(sequence_clip, output_path)

# Example usage
if __name__ == "__main__":
    text_to_sign_language("hello my name is david and every friday i sleep with her, except in the spring , she is late this night")
