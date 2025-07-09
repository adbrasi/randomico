import os
import random
import folder_paths

class DynamicPromptSelector:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        # Caminho para a pasta prompt_files dentro do diretório do node
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_files_path = os.path.join(current_dir, "prompt_files")
        
        # Criar a pasta se não existir
        if not os.path.exists(prompt_files_path):
            os.makedirs(prompt_files_path)
        
        # Listar todos os arquivos .txt na pasta
        txt_files = []
        if os.path.exists(prompt_files_path):
            txt_files = [f for f in os.listdir(prompt_files_path) if f.endswith('.txt')]
        
        # Se não houver arquivos, adicionar uma opção padrão
        if not txt_files:
            txt_files = ["No .txt files found"]
        
        return {
            "required": {
                "file_name": (txt_files, {"default": txt_files[0] if txt_files else "No .txt files found"}),
                "quantidade": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompts",)
    OUTPUT_IS_LIST = (True,)  # Marca a saída como lista
    FUNCTION = "select_prompts"
    CATEGORY = "text/prompts"
    
    def select_prompts(self, file_name, quantidade, seed):
        # Definir seed para reproduzibilidade
        random.seed(seed)
        
        # Caminho completo para o arquivo (relativo ao diretório do node)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_files_path = os.path.join(current_dir, "prompt_files")
        file_path = os.path.join(prompt_files_path, file_name)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path) or file_name == "No .txt files found":
            return (["Arquivo não encontrado ou pasta vazia"],)
        
        try:
            # Ler o arquivo e dividir em linhas
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filtrar linhas vazias e remover quebras de linha
            prompts = [line.strip() for line in lines if line.strip()]
            
            if not prompts:
                return (["Arquivo vazio ou sem prompts válidos"],)
            
            # Determinar quantos prompts selecionar
            # Se temos menos prompts que o solicitado, usar todos disponíveis
            actual_count = min(quantidade, len(prompts))
            
            # Selecionar prompts aleatórios
            if actual_count == len(prompts):
                # Se queremos todos os prompts, embaralhar a lista completa
                selected_prompts = prompts.copy()
                random.shuffle(selected_prompts)
            else:
                # Selecionar uma amostra aleatória sem repetição
                selected_prompts = random.sample(prompts, actual_count)
            
            # Sempre retornar como lista dentro de uma tupla
            return (selected_prompts,)
            
        except Exception as e:
            return ([f"Erro ao ler arquivo: {str(e)}"],)

# Registrar o node
NODE_CLASS_MAPPINGS = {
    "DynamicPromptSelector": DynamicPromptSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicPromptSelector": "Randomico - pageonator"
}
