import uuid

class Sessions:


    _list = []


    @staticmethod
    def create_session() -> str:
        """ create the session """
        chat_id = str(uuid.uuid4())
        chat_object = None
        Sessions._list.append([chat_id, chat_object])
        return chat_id


    @staticmethod    
    def get_chat_object(chat_id : str) -> object:
        """ get the chat object """
        for item in Sessions._list:
            if item[0] == chat_id: # check if chat_id matches
                return item[1] # return chat_object of the matching chat_id
        return None # otherwise return Nothing (None)

    @staticmethod    
    def set_chat_object(chat_id, chat_object):
        """ map the chat object to the chat id """
        for item in Sessions._list:
            if item[0] == chat_id:
                item[1] = chat_object
                return True # returns true if id found
        return False # return false if id not found