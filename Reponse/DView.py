import os
from Reponse.DResponse import DResponse

def DView(ViewAddress):
    current_dir = os.getcwd()
    ViewAddress = current_dir+"/View/"+ViewAddress+".html"
    try:
        with open(ViewAddress, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: File '{ViewAddress}' not found"
    except PermissionError:
        return f"Error: Permission denied for file '{ViewAddress}'"
    except Exception as e:
        return f"Error reading file: {str(e)}"