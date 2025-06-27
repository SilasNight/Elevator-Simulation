import random


class Human:
    def __init__(self):
        """

        :param
        time: the time the person will leave.
        """
        self.floor_y_coordinate = [[261, 276], [245, 260], [229, 244], [213, 228], [197, 212], [181, 196], [165, 180],
                                   [149, 164], [133, 148], [117, 132], [101, 116], [85, 100], [69, 84], [53, 68],
                                   [37, 52], [21, 36], [5, 20]]
        self.room_x_coordinate = [[5, 35], [36, 66], [67, 97], [98, 128], [129, 159], [160, 175], [176, 191], [192, 207], [208, 223], [224, 239], [240, 270], [271, 301], [302, 332], [333, 363], [364, 394]]
        self.floor = random.randint(0,17) # the floor the person will go to
        self.current_floor = 0
        self.current_room = 0
        self.room = random.randint(0,10)# the room the person will go to
        if self.room >= 6:
            self.room += 5 # adding 5 so that the selection doesn't fall on an elevator.

        # I am assigning the variables to self so that it stays with the person
        self.move_speed = random.randint(1,5)
        # I am adding variability so that it's not consistent movement between people
        self.goal_limit = random.randint(0,10)
        self.x_position = 0
        self.y_position = 268
        self.moving = False
        self.last_drawing_object = 0
        self.button_pushed = False
        self.elevator_target = 0

    def draw(self, canvas):
        size = 3
        if self.last_drawing_object != 0:
            canvas.delete(self.last_drawing_object)
        new_drawing = canvas.create_oval(self.x_position-size, self.y_position-size, self.x_position+size,
                                         self.y_position+size,fill="yellow")
        self.last_drawing_object = new_drawing

    def tick(self,elevators):
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
                chance = random.randint(1,100)
                if chance == 1:
                    self.floor = random.randint(1,17)
                    self.room = random.randint(1,10)
                    if self.room >= 6:
                        self.room += 5


    def check_room(self):
        for index,room in enumerate(self.room_x_coordinate):
            if room[0] <= self.x_position <= room[1]:
                self.current_room = index+1

    def leave(self):
        pass

    def press_button(self,elevators):
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
        smallest = positive_response[0]
        for response in positive_response:
            if response[1] < smallest[1]:
                smallest = response
        elevators[smallest[0]].request_insert(self.current_floor,self.floor)
        self.elevator_target = smallest[0]


    def spawn(self) -> None:
        """
        Sets a random starting room on the edges of the ground floor.
        :return:
        """
        if random.randint(0,1) == 1:
            self.x_position = 390
            self.y_position = 270
            self.current_room = 10
        else:
            self.x_position = 41
            self.y_position = 270
            self.current_room = 1
