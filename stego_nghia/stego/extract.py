import sys
import re

# Các mẫu câu ngữ nghĩa tương đương
semantic_equivalents = [
    (r"Khi (.*?), (.*)", lambda g: f"{g[1]} khi {g[0]}"),  # Mẫu "Khi ... thì ..."
    (r"Nếu (.*?), thì (.*)", lambda g: f"{g[1]} nếu {g[0]}"),  # Mẫu "Nếu ... thì ..."
    (r"(.*) bởi vì (.*)", lambda g: f"Bởi vì {g[1]}, {g[0]}")  # Mẫu "X bởi vì Y"
]

def extract_bits_from_text(text: str, mappings: list):
    # Chia văn bản thành các câu dựa trên dấu chấm, dấu hỏi hoặc dấu cảm thán.
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s*', text) if s.strip()]
    extracted_bits = ""

    for sentence in sentences:
        content = sentence.rstrip('.!?')

        matched = False

        # Kiểm tra câu theo các mẫu ngữ nghĩa
        for pattern, inverse_func in mappings:
            # Kiểm tra câu có khớp với pattern gốc
            match = re.fullmatch(pattern, content, flags=re.IGNORECASE)
            if match:
                extracted_bits += '0'  # Câu không đảo ngữ, ghi '0'
                matched = True
                break

        # Nếu không khớp với bất kỳ pattern nào, mặc định là ghi '1'
        if not matched:
            extracted_bits += '1'  # Câu không match với bất kỳ pattern nào, ghi '1'

    return extracted_bits

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract.py hidden_text.txt")
        return

    input_file = sys.argv[1]

    try:
        # Đọc nội dung file hidden_text.txt
        with open(input_file, "r", encoding="utf-8") as f:
            hidden_text = f.read().strip()
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {input_file}")
        return

    # Trích xuất chuỗi nhị phân từ văn bản
    bits = extract_bits_from_text(hidden_text, semantic_equivalents)

    # Lưu kết quả vào file
    with open("extracted_bits.txt", "w") as f:
        f.write(bits)

    print(f"Đã trích xuất chuỗi nhị phân ({len(bits)} bit) vào extracted_bits.txt.")
  

if __name__ == "__main__":
    main()
