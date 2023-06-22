users_state = dict()

class UserSession:
    @staticmethod
    def get_state(session_id):
        if session_id not in users_state:
            users_state[session_id] = {
                'messages': [],
            }
        if session_id:
            state = users_state[session_id]
        else:
            state = {
                'messages': []
            }
        return state

    @staticmethod
    def set_state(session_id, state):
        if session_id in users_state:
            users_state[session_id] = state
            return True
        return False

