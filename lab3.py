class Elevator:
    def __init__(self, current_floor, floors, elevator_id):
        self.current_floor = current_floor
        self.target_floor = None
        self.door_open = False
        self.requests = []
        self.moves = 0
        self.max_floors = floors
        self.elevator_id = elevator_id


    def AddRequest(self, call_floor, target_floor):
        self.requests.append((call_floor, target_floor))

    def Execute(self):
        while self.requests:
            calls = self.requests.pop(0)
            for call in calls:
                self.Move(call)
                self.OpenDoor()
                self.CloseDoor()


    def Move(self, call):
        while self.current_floor!= call:
            {True: self.MovingUp, False: self.MovingDown}[self.current_floor < call]()

    def MovingUp(self):
        self.current_floor = self.checkAvailability(self.current_floor+1)
        self.moves += 1
        print(f"Elevator {self.elevator_id} moved up to floor {self.current_floor}")


    def MovingDown(self):
        self.current_floor = self.checkAvailability(self.current_floor-1)
        self.moves += 1
        print(f"Elevator {self.elevator_id} moved down to floor {self.current_floor}")

    def OpenDoor(self):
        self.door_open = True
        print(f"Elevator {self.elevator_id} doors are open")

    def CloseDoor(self):
        self.door_open = False
        print(f"Elevator {self.elevator_id} doors are closed")

    def checkAvailability(self, floor):
        move_limits = {
            floor: floor for floor in range(1, self.max_floors+1)
        }
        return move_limits.get(floor) or self.FloorException(floor)
    
    def FloorException(self, floor):
        raise Exception(f"Floor {floor} unavailable.")
        

def simulate_elevators(building_floors, elevators_initial, requests):
    elevators = [Elevator(current_floor, building_floors, i+1) for i, current_floor in enumerate(elevators_initial)]

    results = []
    k = 0
    for call_floor, target_floor in requests:
        best_elevator = min(
            elevators, key=lambda e: abs(e.current_floor - call_floor)
        )

        best_elevator.AddRequest(call_floor, target_floor)
        best_elevator.Execute()
        results.append(best_elevator.moves)
        best_elevator.moves = 0
        print()
    return results




building_floors = 10
elevators_initial = [1, 5]
requests = [(5, 7), (3, 9), (10,1)]

results = simulate_elevators(building_floors, elevators_initial, requests)
for i, moves in enumerate(results):
    print(f"Request {i + 1}: Moves={moves}")
