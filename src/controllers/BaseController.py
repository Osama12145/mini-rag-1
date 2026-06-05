from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    
    def __init__(self):

        self.app_settings = get_settings()
        
        self.base_dir = os.path.dirname( os.path.dirname(__file__) )# الميثود دي بتجيب المسار الرئيسي للمشروع يعني لو احنا في src/controllers/BaseController.py راح ترجع المسار اللي فيه src
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )# هنا نجمع المسار الرئيسي للمشروع مع مجلد الملفات اللي راح نخزن فيه الملفات المرفوعة
        
    def generate_random_string(self, length: int=12):# هذي الميثود بتولد لنا مفتاح عشوائي مكون من حروف صغيرة وارقام بطول 12 حرف بشكل افتراضي لكن ممكن نغير الطول اذا حبينا
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
