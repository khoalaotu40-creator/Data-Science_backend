import os
import re

def sanitize_filename(filename):
    """Làm sạch tên file để tránh các ký tự không hợp lệ."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def build_sequential_graph(chunks, output_dir="data/obsidian_vault"):
    """
    Xây dựng đồ thị tuần tự cho Obsidian bằng cách tạo file .md và 
    thêm các liên kết Wikilink [[...]] giữa các chunk liền kề.
    """
    print(f"[*] Đang xây dựng đồ thị Obsidian (Sequential Graph) cho {len(chunks)} chunks...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Bước 1: Tạo danh sách tên file chuẩn cho tất cả các chunks trước
    chunk_filenames = []
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get('source', 'Unknown')
        base_name = sanitize_filename(os.path.basename(source).replace('.md', ''))
        file_name = f"{base_name}_chunk_{i+1}"
        chunk_filenames.append(file_name)

    # Bước 2: Tạo file và chèn Wikilink nối các node
    for i, chunk in enumerate(chunks):
        current_file = chunk_filenames[i]
        file_path = os.path.join(output_dir, f"{current_file}.md")
        
        # --- TẠO METADATA (YAML FRONTMATTER) ---
        content = "---\n"
        content += f"id: chunk_{i+1}\n"
        content += f"source: \"{chunk.metadata.get('source', 'Unknown')}\"\n"
        content += "tags: [chunk, sequential_node]\n"
        content += "---\n\n"
        
        # --- TẠO CÁC ĐƯỜNG NỐI (EDGES) BẰNG WIKILINK ---
        content += "### 🔗 Liên kết Đồ thị (Graph Edges)\n"
        
        # Liên kết đến Chunk trước đó (nếu không phải chunk đầu tiên)
        if i > 0:
            prev_file = chunk_filenames[i-1]
            content += f"- **Trước đó:** [[{prev_file}]]\n"
            
        # Liên kết đến Chunk tiếp theo (nếu không phải chunk cuối cùng)
        if i < len(chunks) - 1:
            next_file = chunk_filenames[i+1]
            content += f"- **Tiếp theo:** [[{next_file}]]\n"
            
        content += "\n---\n\n"
        
        # --- NỘI DUNG CHÍNH ---
        content += chunk.page_content
        
        # Ghi file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print(f"[*] Đã hoàn thành! Mở thư mục '{output_dir}' trong Obsidian để xem Graph View.")