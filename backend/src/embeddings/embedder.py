import os
import re

def sanitize_filename(filename):
    """Làm sạch tên file để tránh các ký tự không hợp lệ trên hệ điều hành."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def export_chunks_for_obsidian(chunks, output_dir="data/obsidian_vault"):
    """
    Lưu các chunks thành các file Markdown riêng biệt để trực quan hóa trong Obsidian.
    (Giải pháp thay thế tạm thời cho bước Embedding trong Giai đoạn 1)
    """
    # Tự động tạo thư mục data/obsidian_vault nếu chưa có
    os.makedirs(output_dir, exist_ok=True)
    
    for i, chunk in enumerate(chunks):
        # Lấy tên file gốc để đặt tên cho Node dễ nhận diện
        source = chunk.metadata.get('source', 'Unknown')
        base_name = os.path.basename(source).replace('.md', '')
        safe_base_name = sanitize_filename(base_name)
        
        # Tên file của chunk: VD: "Huong_Dan_Cap_Nhap_chunk_1.md"
        file_name = f"{safe_base_name}_chunk_{i+1}.md"
        file_path = os.path.join(output_dir, file_name)
        
        # Tạo khối YAML Frontmatter cho Obsidian
        # Khối này giúp Obsidian nhận diện metadata (như tag, source) rất mượt
        content = "---\n"
        content += f"id: chunk_{i+1}\n"
        content += f"source: \"{source}\"\n"
        content += "tags: [chunk, rag_node]\n"
        
        # Thêm các metadata khác nếu có
        for key, value in chunk.metadata.items():
            if key not in ['source']: 
                content += f"{key}: {value}\n"
        content += "---\n\n"
        
        # Thêm nội dung chính của chunk
        content += chunk.page_content
        
        # Ghi nội dung ra file .md
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            