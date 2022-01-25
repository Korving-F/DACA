#!/usr/bin/env python3
import logging

# Set module-level logging
logger = logging.getLogger(__name__)

def set_logging(debug=False):
    """
    Set logging parameters.

    Keyword arguments:
    debug -- enable debug level logging (default False)
    """
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [ %(filename)s:%(lineno)s %(funcName)s %(levelname)s ] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

def test():
    logger.info("Running test()")
    logger.exception("help")
    print("test")


if __name__ == '__main__':
    set_logging() # pass args.debug to it later
    test()