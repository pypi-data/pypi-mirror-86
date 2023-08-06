from typing import List
import math
from controller import Keyboard, Robot, Emitter, Receiver, Camera, InertialUnit, GPS, Compass, Gyro, LED, Motor
from flockai.utility import Graphics, SimulationConfig


class DroneUtils(Robot):
    def __init__(self):
        super(DroneUtils, self).__init__()
        self._initialize_drone()

    def _initialize_drone(self):
        # self.basic_time_step = int(self.getBasicTimeStep())  # 8  # Timestep
        self.receiver_time_step = 1000
        self.camera_time_step = 10000
        # self.name = self.getName()  # Name

        self._enable_attached_devices()  # Enable attached devices
        self._enable_attached_motors()  # Enable attached motors

        self._set_initial_motor_fields()  # Set any initial value to motors

        self._display_keyboard_controls()  # Display controls
        self._set_empirical_constants()  # Set constants
        self._set_variables()  # Set variables






    # def send_message(self, message: str) -> None:


    # def receive_messages(self) -> None:
    #     """
    #     Receive messages on the receiver device
    #     :param receiver: The attached receiver device instance
    #     :param name: Optional for debugging purposes, the name of the robot
    #     :return: None
    #     """
    #     if self.receiver is None:
    #         print("There is no receiver device attached")
    #         return
    #
    #     while self.receiver.getQueueLength() > 0:
    #         message_received = self.receiver.getData().decode('utf-8')
    #         # print(f'{self.name}: I have received this message {message_received}')
    #         self.receiver.nextPacket()



