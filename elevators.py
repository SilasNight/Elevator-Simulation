import tkinter
from typing import Literal

class Elevator:
    def __init__(self, number: int) -> None:
        """
        Initializes the elevator object and assigns it a unique number between 1 and 5 inclusive. So that the x position
        can be calculated and it will be displayed properly.
        :param number: unique number of the elevator
        :return:
        """
        self.floor_y_coordinate = [261, 245, 229, 213, 197, 181, 165, 149, 133, 117, 101, 85, 69, 53, 37, 21, 5]
        self.number = number
        self.floor = 0
        self.moving = False
        self.direction = "None"
        self.last_drawing_object = 0
        self.x_position = 160 + ((self.number-1) * 16)
        self.y_position = 261
        self.stops = []
        self.doors_open = False
        self.doors_open_countdown = 0

    def draw(self, canvas: tkinter.Canvas) -> None:
        """
        This draws the elevator where it is now and deletes the older iteration of the elevator.
        It saves the item ID of the image on the canvas so that it can be removed later.
        :param canvas: This is always the canvas on the main window.
        :return:
        """
        if self.last_drawing_object != 0:
            canvas.delete(self.last_drawing_object)

        if self.doors_open:
            new_drawing = canvas.create_rectangle(self.x_position, self.y_position, self.x_position + 15,
                                                  self.y_position + 15, fill="green")
        else:
            new_drawing = canvas.create_rectangle(self.x_position, self.y_position, self.x_position + 15,
                                                  self.y_position + 15, fill="red")
        self.last_drawing_object = new_drawing

    def tick(self) -> None:
        """
        Makes the elevator move and close or open its doors. And calculates the y pixels that it should be displayed on
        the canvas.
        :return:
        """
        if self.doors_open:
            if self.doors_open_countdown != 0:
                self.doors_open_countdown -= 1
                return
            self.doors_open = False

        if len(self.stops) != 0:
            current_stop = self.stops[0]
            if self.y_position == self.floor_y_coordinate[current_stop]:
                self.moving = False
                self.direction = "None"
                self.doors_open = True
                self.doors_open_countdown = 20
                self.stops.pop(0)
            else:
                if self.y_position < self.floor_y_coordinate[current_stop]:
                    self.moving = True
                    self.direction = "Up"
                    self.y_position += 1

                elif self.y_position > self.floor_y_coordinate[current_stop]:
                    self.moving = True
                    self.direction = "Down"
                    self.y_position -= 1

                if self.y_position in self.floor_y_coordinate:
                    num = self.floor_y_coordinate.index(self.y_position)
                    self.floor = num


    def request_check(self, direction: Literal["up","down"] ,originating_floor: int, desired_floor: int) -> dict:
        """
        :param direction: Direction the person wants to travel
        :param originating_floor: The floor the person is on currently
        :param desired_floor: The floor the person wants to go to
        :return:
        """
        negative_response = {"Available": "no", "Distance": 0}
        if self.direction == "None":
            if self.floor > desired_floor:
                distance = desired_floor - self.floor
            else :
                distance = self.floor - desired_floor
            return {"Available": "yes", "Distance":distance}
        else:
            if self.direction == "Up" and direction == "Up":
                if self.floor < originating_floor:
                    return {"Available": "yes", "Distance": self.floor - originating_floor}
                else:
                    return negative_response
            elif self.direction == "Down" and direction == "Down":
                if self.floor > originating_floor:
                    return {"Available": "yes", "Distance": originating_floor- self.floor}
                else:
                    return negative_response
            else:
                return negative_response

    def request_insert(self,get_passenger_floor: int ,drop_passenger_floor: int) -> None:
        """
        :param get_passenger_floor: Where the passenger is located
        :param drop_passenger_floor: where the passenger is dropped
        :return: None

        This integrates the stops for the next passenger into the stops already in the list. So if the lift has to
        already stop on a floor a duplicate request is not made.
        """
        stops = [get_passenger_floor,drop_passenger_floor]
        if len(self.stops) != 0:
            for potential_stop in stops:
                if potential_stop not in self.stops:
                    for index, stop in enumerate(self.stops):
                        if potential_stop < stop:
                            self.stops.insert(index,potential_stop)
                            break
        else:
            self.stops.append(get_passenger_floor)
            self.stops.append(drop_passenger_floor)






