class HackRF(object):
    """_summary_
    
    Class wrapper for the HackRF Boards
    """
    
    def __init__(self, board, name, serial_num):
        """_summary_

        Instantiate a HackRF Board
        Args:
            board (_type_): _description_
            name (_type_): _description_
            serial_num (_type_): _description_            
        """
        self.board = board
        self.name = name
        self.serial_num = serial_num