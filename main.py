from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
import time

def detect_tilt(accel_x, accel_y):
    # set threshold values for detecting tilt
    tilt_thresh = 0.5
    x_thresh = 0.2
    y_thresh = 0.2

    # determine tilt direction based on accelerometer data
    if accel_x > tilt_thresh and abs(accel_y) < y_thresh:
        return "Right"
    elif accel_x < -tilt_thresh and abs(accel_y) < y_thresh:
        return "Left"
    elif accel_y > tilt_thresh and abs(accel_x) < x_thresh:
        return "Forward"
    elif accel_y < -tilt_thresh and abs(accel_x) < x_thresh:
        return "Backward"
    else:
        return None

# set up BoardShim and start streaming data
params = BrainFlowInputParams()
params.serial_port = 'COM8'
board = BoardShim(BoardIds.CYTON_BOARD, params)
board.prepare_session()
board.start_stream()

# keep the program running to continue receiving data
while True:
    # read data from the Cyton
    data = board.get_board_data()

    # check that data has been received
    if len(data) == 0:
        print("No data received")
        time.sleep(0.1)
        continue
    if len(data[10]) or len(data[9]) == 0:
        continue
    # extract accelerometer data from the data array
    accel_x = data[9][0]
    accel_y = data[10][0]

    # check that accelerometer data is valid
    if accel_x is None or accel_y is None:
        print("Invalid accelerometer data")
        time.sleep(0.1)
        continue

    # detect tilt and print direction if detected
    tilt_direction = detect_tilt(accel_x, accel_y)
    if tilt_direction is not None:
        print(tilt_direction)

    time.sleep(0.1)
