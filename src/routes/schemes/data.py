from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):# اي حاجه حتخرج من الشكل ذا حيطلع  خطاء لانها مش متوافقة مع الشكل المطلوب وهذي مسوول عنها ال pydantic
    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0
