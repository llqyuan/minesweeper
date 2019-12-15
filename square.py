
class Square:
    '''
    Fields:
     * is_revealed (Bool)
     * has_bomb (Bool)
     * is_flagged (Bool)
    '''
    def __init__(self, rev, bomb, flag):
        self.is_revealed = rev
        self.has_bomb = bomb
        self.is_flagged = flag

