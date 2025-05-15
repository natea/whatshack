import os

expected_content = {
    "content/lang_confirmation_en.txt": "Language set to English.",
    "content/lang_confirmation_xh.txt": "Ulwimi lusetelwe kwiXhosa.",
    "content/lang_confirmation_af.txt": "Taal ingestel op Afrikaans."
}

all_correct = True
for file_path, content in expected_content.items():
    if not os.path.exists(file_path):
        print(f"ERROR: File {file_path} does not exist.")
        all_correct = False
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        actual_content = f.read().strip()
    if actual_content != content:
        print(f"ERROR: File {file_path} content mismatch.")
        print(f"  Expected: '{content}'")
        print(f"  Actual:   '{actual_content}'")
        all_correct = False
    else:
        print(f"SUCCESS: File {file_path} content is correct.")

if not all_correct:
    print("Verification FAILED for one or more files.")
    exit(1)
else:
    print("All language confirmation files verified successfully.")
    exit(0)