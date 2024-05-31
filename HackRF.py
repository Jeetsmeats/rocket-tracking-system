# Imports
import SoapySDR

class HackRF(object):
    """_summary_
    
    Class wrapper for the HackRF Boards
    """
    
    def __init__(self, name, serial_tag):
        """_summary_

        Instantiate a HackRF Board
        Args:
            board (_type_): _description_
            name (_type_): _description_
            serial_tag (string): _description_            
        """
        arg = dict(driver="hackrf", serial=serial_tag)
        self.board = SoapySDR.Device(arg)
        self.name = name
        self.serial_tag = serial_tag
        
    def get_board(self):
        """_summary_
        
        Get the HackRF Board instance
        Returns:
            _type_: HackRF Board
        """
        return self.board

    def get_name(self):
        """_summary_

        Get the board name
        Returns:
            str: Board Name
        """
        return self.name