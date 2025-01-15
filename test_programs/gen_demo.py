########################
# Artificial Data Demo #
########################

# make sure brainflow is installed:
# %pip install brainflow


# NOT WORKING
# The Synthetic Unicorn headset uses BrainFlow's Synthetic Board. 
# This board generates synthetic data that we can use for testing without hardware.
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BrainFlowError, BoardIds
import time

def main():
    # Initialize BrainFlow input parameters with default empty values
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.UNICORN_BOARD, params)
        
    try:
        # Prepare the board
        BoardShim.enable_dev_board_logger()  # Enable debugging logs
        
        # Start the data stream
        board.prepare_session()
        board.start_stream()
        print("Data stream started. Collecting data for 10 seconds...")
        
        # Stream data for a period of time
        time.sleep(10)  # Stream data for 10 seconds
        
        # Stop the data stream and release the session
        data = board.get_board_data()  # Retrieve the data collected
        board.stop_stream()
        board.release_session()
        
        # Output the shape of the data (optional)
        print("Shape of collected data:", data.shape)
        print("Demo complete.")
    
    except BrainFlowError as e:
        print(f"BrainFlowError: {e}")

if __name__ == "__main__":
    main()
