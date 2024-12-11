class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        pass


class State(object):
    def __init__(self, FSM):
        self.FSM = FSM

    def Execute(self):
        pass

class MovingUp(State):
    def __init__(self, FSM):
        super(MovingUp, self).__init__(FSM)

    def Execute(self):
        if self.FSM.char.current_floor < self.FSM.char.target_floor:
            if self.FSM.char.current_floor == self.FSM.char.max_floors:
                raise Exception(f"Elevator {self.FSM.char.elevator_id}: Cannot move up from the top floor")
            else:
                self.FSM.char.current_floor += 1
                self.FSM.char.moves += 1
                print(f"Elevator {self.FSM.char.elevator_id} moved up to floor {self.FSM.char.current_floor}")
        if self.FSM.char.current_floor == self.FSM.char.target_floor:
            self.FSM.ToTransition("toOpenDoor")

class MovingDown(State):
    def __init__(self, FSM):
        super(MovingDown, self).__init__(FSM)

    def Execute(self):
        if self.FSM.char.current_floor > self.FSM.char.target_floor:
            if self.FSM.char.current_floor == 1:
                raise Exception(f"Elevator {self.FSM.char.elevator_id}: Cannot move down from the ground floor")
            else:
                self.FSM.char.current_floor -= 1
                self.FSM.char.moves += 1
                print(f"Elevator {self.FSM.char.elevator_id} moved down to floor {self.FSM.char.current_floor}")
        if self.FSM.char.current_floor == self.FSM.char.target_floor:
            self.FSM.ToTransition("toOpenDoor")

class OpenDoor(State):
    def __init__(self, FSM):
        super(OpenDoor, self).__init__(FSM)

    def Execute(self):
        self.FSM.char.door_open = True
        print(f"Elevator {self.FSM.char.elevator_id} doors are open")
        self.FSM.ToTransition("toCloseDoor")



class CloseDoor(State):
    def __init__(self, FSM):
        super(CloseDoor, self).__init__(FSM)

    def Execute(self):
        self.FSM.char.door_open = False
        print(f"Elevator {self.FSM.char.elevator_id} doors are closed")
        self.FSM.ToTransition("toHandler")

class Handler(State):
    def __init__(self, FSM):
        super(Handler, self).__init__(FSM)

    def Execute(self):
        
        if self.FSM.char.active_request:
            call_floor, target_floor = self.FSM.char.active_request
            
            # лифт на этаже вызова
            if self.FSM.char.current_floor == call_floor and self.FSM.char.target_floor == call_floor:
                self.FSM.char.target_floor = target_floor
                if self.FSM.char.current_floor < target_floor:
                    self.FSM.ToTransition("toMovingUp")
                elif self.FSM.char.current_floor > target_floor:
                    self.FSM.ToTransition("toMovingDown")
                else:
                    self.FSM.ToTransition("toOpenDoor")

            # лифт на целевом этаже
            elif self.FSM.char.current_floor == self.FSM.char.target_floor:
                self.FSM.char.active_request = None
                self.FSM.char.target_floor = None
                self.FSM.ToTransition("toHandler")

            # лифт еще не на этаже вызова
            else:
                self.FSM.char.target_floor = call_floor
                if self.FSM.char.current_floor < call_floor:
                    self.FSM.ToTransition("toMovingUp")
                elif self.FSM.char.current_floor > call_floor:
                    self.FSM.ToTransition("toMovingDown")
                else:
                    self.FSM.ToTransition("toOpenDoor")
        elif self.FSM.char.requests:
            
            self.FSM.char.active_request = self.FSM.char.requests.pop(0)


##============================================
# Finite State Machine
class FSM(object):
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None

    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition

    def AddState(self, stateName, state):
        self.states[stateName] = state

    def SetState(self, stateName):
        self.curState = self.states[stateName]

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]

    def Execute(self):
        if self.trans:
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None
        self.curState.Execute()

##============================================
# Elevator Character
class Elevator:
    def __init__(self, current_floor, floors, elevator_id):
        self.current_floor = current_floor
        self.target_floor = None
        self.door_open = False
        self.requests = []
        self.moves = 0
        self.max_floors = floors
        self.elevator_id = elevator_id
        self.active_request = None
        self.FSM = FSM(self)

        self.FSM.AddState("Handler", Handler(self.FSM))
        self.FSM.AddState("MovingUp", MovingUp(self.FSM))
        self.FSM.AddState("MovingDown", MovingDown(self.FSM))
        self.FSM.AddState("OpenDoor", OpenDoor(self.FSM))
        self.FSM.AddState("CloseDoor", CloseDoor(self.FSM))

        self.FSM.AddTransition("toHandler", Transition("Handler"))
        self.FSM.AddTransition("toMovingUp", Transition("MovingUp"))
        self.FSM.AddTransition("toMovingDown", Transition("MovingDown"))
        self.FSM.AddTransition("toOpenDoor", Transition("OpenDoor"))
        self.FSM.AddTransition("toCloseDoor", Transition("CloseDoor"))

        self.FSM.SetState("Handler")

    def AddRequest(self, call_floor, target_floor):
        self.requests.append((call_floor, target_floor))

    def Execute(self):
        self.FSM.Execute()



def simulate_elevators(building_floors, elevators_initial, requests):
    elevators = [Elevator(current_floor, building_floors, i+1) for i, current_floor in enumerate(elevators_initial)]

    results = []
    k = 0
    for call_floor, target_floor in requests:
        best_elevator = min(
            elevators, key=lambda e: abs(e.current_floor - call_floor)
        )

        best_elevator.AddRequest(call_floor, target_floor)

        while best_elevator.requests or best_elevator.active_request or best_elevator.FSM.curState != best_elevator.FSM.states["Handler"]:
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
