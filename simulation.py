import tkinter as tk
import elevators
import person


class Main:
    def __init__(self)->None:
        """
        The main simulation script will interface with both of the other scripts person.py and elevators.py
        :return:None
        """
        self.floor_y_coordinate = [[261, 276], [245, 260], [229, 244], [213, 228], [197, 212], [181, 196], [165, 180],
                                   [149, 164], [133, 148], [117, 132], [101, 116], [85, 100], [69, 84], [53, 68],
                                   [37, 52], [21, 36], [5, 20]]
        self.room_x_coordinate = [[5, 35], [36, 66], [67, 97], [98, 128], [129, 159], [160, 175], [176, 191],
                                  [192, 207], [208, 223], [224, 239], [240, 270], [271, 301], [302, 332], [333, 363],
                                  [364, 394]]
        self.window = tk.Tk()
        self.window.title("Elevator Simulation")
        self.window.geometry("400x285")
        self.window.resizable(False, False)
        self.canvas = tk.Canvas(self.window,width=400,height=285,bg="black")
        self.canvas.pack()
        self.elevators = []
        self.people = []
        self.populate_elevators()
        self.draw_building()
        self.window.bind("<space>", lambda e: self.spawn_person())
        self.window.bind("<t>", lambda e: self.tick())
        self.amount_of_people = 100
        self.window.mainloop()

    def populate_elevators(self)-> None:
        """
        Makes 5 elevator objects that will be numbered 1 to 5
        :return: None
        """
        for i in range(1,6):
            self.elevators.append(elevators.Elevator(number = i))

    def spawn_person(self) -> None:
        """
        Every time this is used it will spawn a person object
        :return: None
        """
        self.people.append(person.Human())

    def draw_people(self, dude:person.Human) -> None:
        """
        This will update and draw the human object where it is now
        :param dude: the human object
        :return: None
        """
        dude.draw(self.canvas)

    def draw_elevators(self, elevator:elevators.Elevator)-> None:
        """
        This will update and draw the elevator object where it is now
        :param elevator: this is the elevator object
        :return: None
        """
        elevator.draw(self.canvas)

    def tick(self)-> None:
        """
        This is the internal clock to make everything move
        :return: None
        """
        for elevator in self.elevators:
            elevator.tick()
            self.draw_elevators(elevator)
        for index, dude in enumerate(self.people):
            dude.tick(self.elevators)
            self.draw_people(dude)
            if dude.leaving and dude.image_clear:
                self.people.pop(index)
            # while self.amount_of_people != len(self.people)-1:
            #     self.spawn_person()
        self.window.after(10, self.tick)

    def draw_building(self)-> None:
        """
        This is the start to draw the building
        :return: None
        """
        def rooms(room_x_position:int, room_y_position:int, block_width:int, block_height:int)-> None:
            """
            The function used to draw each room. always 5 rows horizontally and 17 rows vertically.

            :param room_x_position: The top left x coordinate of the room.
            :param room_y_position: the top left y coordinate of the room.
            :param block_width: The width of the room.
            :param block_height: The height of the room.
            :return: None
            """
            for x in range(5): #Horizontal amount of rooms/lifts
                for y in range(17):#Vertical amount of rooms/lifts
                    self.canvas.create_rectangle(room_x_position, room_y_position, room_x_position + block_width, room_y_position + block_height, fill="white")
                    room_y_position += block_height + 1
                room_x_position += block_width + 1

        rooms(5, 5, 30, 15)
        rooms(160, 5, 15, 15)
        rooms(240, 5, 30, 15)
        """
        Different sizes for the rooms and lifts. The rooms are 30 by 15 and the lifts are 15 by 15
        all the colours are white to start with but that will soon change.
        """

Main()


