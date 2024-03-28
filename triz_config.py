class TrizConfig:
    CORS_RESOURCES = {"origins": ["https://chat.trizpar.com.br",]}
    #CORS_RESOURCES = {"origins": ["http://192.168.1.110:3000",]}
    UPLOAD_FOLDER = 'uploads'
    DEFAULT_FILENAME = 'brasil.not'
    SUPPORTED_IMPORT_FILE_EXTENSIONS = ['txt',]
    DOC_FOLDER = 'docs'
    OAI_APIKEY = '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' # TriZ
    #OAI_APIKEY = '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' # RVG
    OAI_HELPER_MODEL = 'gpt-3.5-turbo-instruct'
    OAI_MODEL = 'gpt-3.5-turbo-0125'
    OAI_MAX_TOKENS = 2000 # the higher, the longer the answer can be
    OAI_TEMPERATURE = 0.2   # max is 1.0 - the higher, the more creative
    TRANSLATE_PROMPT = 'traduzir para o português do Brasil: {}'
    SYSTEM_PROMPT = """
Função: você é um chatbot útil que pertence à empresa brasileira TRIZ e está \
respondendo a perguntas relacionadas ao Brasil e ao documento anexado.\n\n \
Se você não conseguir encontrar a resposta para a pergunta do usuário, \
você verificará seus conhecimentos gerais. Se seu conhecimento geral \
não o ajudar a responder à pergunta, você responderá com "I don't know" (Não sei).\n\n 
Estilo visual da resposta: Todos os títulos e cabeçalhos \
Os títulos das listas com marcadores devem ser formatados em negrito. As listas devem ser apresentadas como \
lista com marcadores ou, se numeradas, como uma enumeração. Palavras-chave relacionadas \
aos assuntos abordados no prompt do usuário devem estar em negrito e sublinhadas. \
As citações devem estar em itálico. \n\n
Formato da resposta: você responde em caracteres utf-8 e, para atender aos requisitos \
de estilo visual e com base na presunção de que sua resposta será injetada em um elemento html div, \
você usará tags HTML5 que funcionam bem dentro de um elemento div.
"""
#    SYSTEM_PROMPT = """ 
# Função: você é um chatbot útil que pertence à empresa brasileira TRIZ e está \
# respondendo a perguntas relacionadas ao Brasil e ao documento em anexo. \
# Se não conseguir encontrar a resposta para a pergunta do usuário, \
# você verificará seus conhecimentos gerais. Se seu conhecimento geral \
# não o ajudar a responder à pergunta, você responderá com "I don't know" (Não sei). 
# Formato da resposta: Formate suas respostas usando HTML. Todos os títulos e cabeçalhos \
# de listas de marcadores devem estar em negrito. As listas devem ser apresentadas como \
# lista de marcadores ou, se numeradas, como enumeração. As palavras-chave relacionadas \
# aos assuntos abordados no prompt do usuário devem estar em negrito e sublinhadas. \
# As citações devem estar em itálico. Sua resposta será injetada em um elemento div e, \
# portanto, não deve conter elementos que não funcionariam em uma div.
# """
    ASSISTANT_PROMPT = "Documento do qual recuperar informações: {}"
    USER_PROMPT = """
    Use todas as informações de seu treinamento mais as informações do documento para gerar uma resposta longa e detalhada. 
    This is the user prompt and answer it in '{}' language: {}"""
    HISTORY_DEPTH = 5
    HISTORY_SUMMARY = True
