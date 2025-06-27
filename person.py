import random

class Human:
    def __init__(self):
        """

        :param
        time: the time the person will leave.
        """
        self.floor_y_coordinate = [21, 37, 53, 69, 85, 101, 117, 133, 149, 165, 181, 197, 213, 229, 245, 261, 277]
        self.room_x_coordinate = [36, 67, 98, 129, 160, 176, 192, 208, 224, 240, 271, 302, 333, 364, 395]
        self.floor = random.randint(0,17) # the floor the person will go to
        self.current_floor = 0
        self.current_room = 0
        self.room = random.randint(0,10)# the room the person will go to
        if self.room < 6:
            self.room += 5 # adding 5 so that the selection doesn't fall on an elevator.

        # I am assigning the variables to self so that it stays with the person
        self.move_speed = random.randint(1,5)
        # I am adding variability so that it's not consistent movement between people
        self.goal_limit = random.randint(0,10)
        self.x_position = 0
        self.y_position = 0
        self.moving = False
        self.last_drawing_object = 0

    def draw_people(self, dude):
        pass

    def tick(self):
        if self.current_floor != self.floor:
            if self.current_room <= 5:
                self.x_position += self.move_speed
            else:
                self.x_position -= self.move_speed

        else:
            if self.current_room != self.room:
                pass

    def leave(self):
        pass

    def press_button(self):
        pass

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
