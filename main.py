import tkinter as tk
import logging
from controller import ResearcherController

def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    return logging.getLogger('main')

def main():

    logger = setup_logging()
    
    try:

        root = tk.Tk()
        

        app = ResearcherController(root, "data.csv")
        

        root.mainloop()
        
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)

        print(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()