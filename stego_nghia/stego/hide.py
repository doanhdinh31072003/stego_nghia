import sys
import re

# Các cặp mẫu ngữ nghĩa tương đương
semantic_equivalents = [
    (r"Khi (.*?), (.*)", r"\2 khi \1"),
    (r"Nếu (.*?), thì (.*)", r"\2 nếu \1"),
    (r"(.*) bởi vì (.*)", r"Bởi vì \2, \1")
]

def capitalize_first_letter(sentence):
    sentence = sentence.strip()
    if not sentence:
        return ""
    return sentence[0].upper() + sentence[1:]

def embed_semantic_stegano(secret_bits: str, base_text: str, mappings: list):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s*', base_text) if s.strip()]
    bit_idx = 0
    output_sentences = []

    for sentence in sentences:
        content = sentence.rstrip('.!?')
        punct = sentence[-1] if sentence[-1] in ".!?" else '.'
        modified = False

        for pattern, replacement in mappings:
            if bit_idx >= len(secret_bits):
                break

            match = re.fullmatch(pattern, content, flags=re.IGNORECASE)
            if match:
                if secret_bits[bit_idx] == '1':
                    new_sentence = replacement
                    for i in range(len(match.groups())):
                        new_sentence = new_sentence.replace(f"\\{i+1}", match.group(i+1))
                    content = new_sentence
                bit_idx += 1
                modified = True
                break

        output_sentences.append(capitalize_first_letter(content) + punct)

    return " ".join(output_sentences), bit_idx

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 hide.py text.txt binary.txt")
        return

    text_file = sys.argv[1]
    binary_file = sys.argv[2]

    with open(text_file, "r", encoding="utf-8") as f:
        base_text = f.read().strip()

    with open(binary_file, "r") as f:
        binary_bits = f.read().strip()

    output_text, used_bits = embed_semantic_stegano(binary_bits, base_text, semantic_equivalents)

    with open("hidden_text.txt", "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"Đã giấu {used_bits} bit thông điệp vào văn bản.")
    print("Kết quả lưu trong: hidden_text.txt")

if __name__ == "__main__":
    main()
