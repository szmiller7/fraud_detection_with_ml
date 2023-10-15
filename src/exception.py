import sys
from src.logger import logging

def error_message_detail(error, error_detail:sys):
    """
    create function that will be called whenever we get an error
    """
    #  only traceback object is of interest
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename 
    line_numer = exc_tb.tb_lineno
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, line_numer, str(error)
        )
    return error_message
    


class CustomException(Exception):
    """ Inherit from Exception """

    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message =  error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """
        Ensure that printing class object will return its printable representation
        """
        return self.error_message

## uncomment and run python src/exception.py to check if works
# if __name__ == "__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Divide by Zero")
#         raise CustomException(e, sys)