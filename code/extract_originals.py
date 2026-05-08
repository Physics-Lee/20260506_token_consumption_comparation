import json
import os

# Mapping: json_file -> output_markdown_filename
files = {
    'data/paulgraham.json': 'resource/Writes_and_Write_Nots.md',
    'data/allende.json': 'resource/Last_Speech_of_Salvador_Allende.md',
    'data/yangzhenning.json': 'resource/Why_China_Should_Not_Build_a_Super_Collider_Today.md',
}

for json_path, md_path in files.items():
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find original text
    original = None
    for t in data['texts']:
        if t['role'] == 'original':
            original = t
            break
    
    if not original:
        print(f"No original found in {json_path}")
        continue
    
    # Write markdown with minimal metadata header
    content = original['content']
    title = original['title']
    
    md_content = f"# {title}\n\n{content}\n"
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Created {md_path} ({len(content)} chars)")

print("Done")
