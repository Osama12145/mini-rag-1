from abc import ABC, abstractmethod

class LLMInterface(ABC):#  انشاء كلاس مجرد لواجهة LLMInterfaceبدون تنفيذ أي وظيفة، حيث يتم تحديد الوظائف التي يجب أن تنفذها أي كلاس يرث من هذه الواجهة.

    @abstractmethod # تحديد أن هذه الوظيفة مجردة ويجب أن يتم تنفيذها في الكلاسات التي ترث من هذه الواجهة.
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):# document_type يفرق بين سوال المستخدم والنصوص المعرفة، حيث يمكن استخدامه لتحديد نوع النص الذي يتم تضمينه، مما يساعد في تحسين جودة التضمين وفهم السياق. على سبيل المثال، يمكن أن يكون document_type "user_query" للسوال المستخدم و "knowledge_text" للنصوص المعرفة.
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass
