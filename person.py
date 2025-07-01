import random
import tkinter


class Human:
    def __init__(self)->None:
        """
        This makes the human object
        """
        self.floor_y_coordinate = [[261, 276], [245, 260], [229, 244], [213, 228], [197, 212], [181, 196], [165, 180],
                                   [149, 164], [133, 148], [117, 132], [101, 116], [85, 100], [69, 84], [53, 68],
                                   [37, 52], [21, 36], [5, 20]]
        self.room_x_coordinate = [[5, 35], [36, 66], [67, 97], [98, 128], [129, 159], [160, 175], [176, 191],
                                  [192, 207], [208, 223], [224, 239], [240, 270], [271, 301], [302, 332], [333, 363],
                                  [364, 394]]
        self.floor = random.randint(0,16) # the floor the person will go to
        self.current_floor = 0
        self.current_room = 0
        self.room = random.randint(0,10)# the room the person will go to
        if self.room >= 6:
            self.room += 5 # adding 5 so that the selection doesn't fall on an elevator.

        # I am assigning the variables to self so that it stays with the person
        self.move_speed = 1
        # I am adding variability so that it's not consistent movement between people
        self.goal_limit = random.randint(0,10)
        self.x_position = 0
        self.y_position = 268
        self.last_drawing_object = 0
        self.button_pushed = False
        self.elevator_target = 0 # The elevator that the person is waiting for.
        self.leaving = False # This makes the person target the exit and leave the building.
        self.image_clear = False # this checks if the human targets image is removed before the object is deleted.
        self.pinged = False # This is the check for if the human object has walked off the building on anything but the ground floor....
        self.countdown = 0 # the amount of ticks that will pass before the person will move off to a different room/floor

    def draw(self, canvas:tkinter.Canvas)->None:
        """
        This will draw the human object on the canvas at its current position
        :param canvas: The canvas to draw on
        :return: None
        """
        size = 3
        if self.last_drawing_object != 0:
            canvas.delete(self.last_drawing_object)
        if self.leaving and self.current_floor == 1 and self.current_room == 1:
            self.image_clear = True
        else:
            new_drawing = canvas.create_oval(self.x_position - size, self.y_position - size, self.x_position + size,
                                             self.y_position + size, fill="yellow")
            self.last_drawing_object = new_drawing


    def tick(self,elevators:list)->None:
        """
        Makes the human object move or wait.
        :param elevators: list of elevator objects
        :return: None
        """
        if self.x_position < -10 and not self.pinged:
            print("Ping")
            self.pinged = True
        if self.current_floor != self.floor:
            if self.current_room <= 7:
                self.x_position += self.move_speed
                self.check_room()
            elif self.current_room >= 9:
                self.x_position -= self.move_speed
                self.check_room()
            else:
                if not self.button_pushed:
                    self.button_pushed = True
                    self.press_button(elevators)
                else:
                    if (elevators[self.elevator_target].floor == self.current_floor and
                            elevators[self.elevator_target].doors_open):
                        self.x_position = -10
                        self.y_position = -10
                    if (elevators[self.elevator_target].floor == self.floor and
                            elevators[self.elevator_target].doors_open):
                        self.x_position = elevators[self.elevator_target].x_position
                        self.y_position = elevators[self.elevator_target].y_position + 7
                        self.button_pushed = False
                        self.current_floor = self.floor
        else:
            if self.current_room != self.room:
                if self.room > self.current_room:
                    self.x_position += self.move_speed
                    self.check_room()
                else:
                    self.x_position -= self.move_speed
                    self.check_room()
            else:
                if self.leaving:
                    self.floor = 0
                    self.room = 1
                else:
                    if self.countdown == 0:
                        self.floor = random.randint(0,16)
                        self.room = random.randint(1,10)
                        if self.room >= 6:
                            self.room += 5
                        self.countdown = random.randint(1,1000)
                    else:
                        self.countdown -= 1


    def check_room(self)->None:
        """
        Uses the current x_position to see what room the human object is currently in
        :return: None
        """
        for index,room in enumerate(self.room_x_coordinate):
            if room[0] <= self.x_position <= room[1]:
                self.current_room = index+1


    def press_button(self,elevators:list)->None:
        """
        Goes through the elevators list and makes checks if any elevator is available to pick it up
        :param elevators: a list of elevator objects
        :return: None
        """
        positive_response = []
        if self.floor > self.current_room:
            direction = "up"
        else:
            direction = "down"
        elevator_responses = []
        for elevator in elevators:
            elevator_responses.append(elevator.request_check(direction,self.current_floor,self.floor))
        for index, response in enumerate(elevator_responses):
            if response["Available"] == "yes":
                positive_response.append([index, response["Distance"]])
        if len(positive_response) == 0:
            self.button_pushed = False
        else:
            smallest = positive_response[0]
            for response_distance in positive_response:
                if response_distance[1] < smallest[1]:
                    smallest = response_distance
            elevators[smallest[0]].request_insert(self.current_floor,self.floor)

            self.elevator_target = smallest[0]


    def spawn(self) -> None:
        """
        Sets a random starting room on the edges of the ground floor.
        :return: None
        """
        if random.randint(0,1) == 1:
            self.x_position = 390
            self.y_position = 270
            self.current_room = 10
        else:
            self.x_position = 41
            self.y_position = 270
            self.current_room = 1
