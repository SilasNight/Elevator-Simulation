import tkinter as tk
import elevators
import person


class Main:
    def __init__(self):
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
        self.window.mainloop()

    def populate_elevators(self):
        for i in range(1,6):
            self.elevators.append(elevators.Elevator(number = i))

    def spawn_person(self):
        self.people.append(person.Human())

    def draw_people(self, dude):
        dude.draw(self.canvas)

    def draw_elevators(self, elevator):
        elevator.draw(self.canvas)

    def tick(self)-> None:
        """
        This is the internal clock to make everything move
        :return: None
        """
        for elevator in self.elevators:
            elevator.tick()
            self.draw_elevators(elevator)
        for dude in self.people:
            dude.tick(self.elevators)
            self.draw_people(dude)

    def draw_building(self):
        def rooms(x_block_gap, y_block_gap, block_width, block_height):
            x_rooms = x_block_gap
            for x in range(5): #Horizontal amount of rooms/lifts
                y_rooms = y_block_gap
                for y in range(17):#Vertical amount of rooms/lifts
                    self.canvas.create_rectangle(x_rooms, y_rooms, x_rooms + block_width, y_rooms + block_height, fill="white")
                    y_rooms += block_height +1
                x_rooms += block_width +1

        rooms(5, 5, 30, 15)
        rooms(160, 5, 15, 15)
        rooms(240, 5, 30, 15)
        """
        Different sizes for the rooms and lifts. The rooms are 30 by 15 and the lifts are 15 by 15
        all the colours are white to start with but that will soon change.
        """

Main()


