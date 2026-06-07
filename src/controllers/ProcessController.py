from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum

class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):

        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None

    def get_file_content(self, file_id: str):

        loader = self.get_file_loader(file_id=file_id)
        return loader.load()# لانج تشين بتتوقع ان ال load ترجع لست من ال Document objects اللي فيها page_content و metadata

    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_size: int=20):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,# فنكشن عشان تحسب فيها الطول عشان تقدر تقسم النصوص بناء على الطول مش بناء على عدد الكلمات مثلا، لان ممكن يكون 
           # في نصوص فيها كلمات طويلة جدا او قصيرة جدا فلو اعتمدنا على عدد الكلمات ممكن يطلع لنا chunks طويلة او قصيرة جدا، لكن لو اعتمدنا على طول النصوص حيطلع لنا chunks متقاربة في الطول
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]# هذا كمبرهينشن عشان نطلع ال page_content من كل Document object في ال list اللي رجعها ال loader، لان ال text_splitter بيتوقع ان ال input بتاعه يكون لست من النصوص مش لست من ال Document objects

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata# يساعدني اعرف معلومات عن الصفحه اللي جت منها ال chunk دي، مثلا لو حبيت ارجع اصل ال chunk دي منين في الملف اقدر اعرف من ال metadata، او لو حبيت اعرف اي صفحة في ال PDF جت منها ال chunk دي اقدر اعرف من ال metadata
        )

        return chunks


    

