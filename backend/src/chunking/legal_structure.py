import re
def parse_legal_structure(md_text):
    chapters = re.split(r'(?=# Chương)', md_text)
    final_data = []
    for chapter in chapters:
        if not chapter.strip():
            continue
        
        # Lấy tiêu đề Chương (ví dụ: # Chương I...)
        chapter_title = chapter.split('\n')[0].strip()

        # 2. Tách các Điều trong Chương đó
        articles = re.split(r'(?=# Điều \d+\.)', chapter)

        for article in articles:
            # Bỏ qua phần header của chương hoặc phần trống
            if not article.strip() or article.startswith('# Chương'):
                continue
            
            article_title = article.split('\n')[0].strip()

            # 3. Tách theo từng Khoản (dòng bắt đầu bằng 1., 2., 3...)
            # Tìm các dòng có định dạng "số." nằm đầu dòng
            clauses = re.split(r'(?=\n\d+\.)', article)
            for clause in clauses:
                if not clause.strip():
                    continue
                # Lưu cấu trúc phân cấp vào list
                final_data.append({
                    "chapter": chapter_title,
                    "article": article_title,
                    "content": clause.strip()
                })
    return final_data