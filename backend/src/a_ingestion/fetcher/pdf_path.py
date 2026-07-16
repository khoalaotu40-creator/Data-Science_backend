from pathlib import Path
from typing import Union

def get_local_pdf(file_path: Union[str, Path]) -> Path:
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Lỗi: Không tìm thấy file tại đường dẫn '{path}'")
    if not path.is_file():
        raise IsADirectoryError(f"Lỗi: Đường dẫn '{path}' trỏ tới một thư mục, không phải file.")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Lỗi: Yêu cầu file PDF, nhưng nhận được file có đuôi '{path.suffix}'")

    return path