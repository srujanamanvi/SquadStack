import sys
import copy

class Car(object):
    def __init__(self, reg_no, driver_age):
        self.reg_no = reg_no
        self.driver_age = driver_age


class Slot(object):
    def __init__(self, number, available):
        self.number = number
        self.available = available
        self.car = None


class ParkingLot(object):
    def __init__(self):
        self.slots = []

    def create_slots(self, total):
        for num in range(total):
            self.slots.append(Slot(num+1, True))

    def park_car(self, reg_no, driver_age):
        for slot in self.slots:
            if slot.available:
                slot.car = Car(reg_no, driver_age)
                slot.available = False
                return slot
        return None

    def fetch_slots_for_driver(self, driver_age):
        result = []
        for slot in self.slots:
            if not slot.available and slot.car.driver_age == driver_age:
                result.append(str(slot.number))
        return ",".join(result)

    def fetch_slot_for_car(self, reg_no):
        for slot in self.slots:
            if not slot.available and slot.car.reg_no == reg_no:
                return slot.number
        return None

    def exit_parking(self, slot_number):
        for slot in self.slots:
            if slot.number == slot_number and not slot.available:
                slot.available = True
                exit_car = copy.deepcopy(slot)
                slot.car = None
                return exit_car
        return None

    def fetch_vehicle_reg_for_age(self, driver_age):
        result = []
        for slot in self.slots:
            if not slot.available and slot.car.driver_age == driver_age:
                result.append(str(slot.car.reg_no))
        return ", ".join(result)


def operate_parking_lot(contents):
    try:
        if contents:
            total = int(contents[0].strip().split()[1])
            parking_lot = ParkingLot()
            parking_lot.create_slots(total)
            print("Created parking of {0}".format(total))
            for line in contents[1:]:
                n = line.strip().split()
                if n[0] == "Park":
                    slot = parking_lot.park_car(n[1], n[3])
                    if slot:
                        print("Car with vehicle registration number {0} has been parked at slot number {1}".format(n[1], slot.number))
                    else:
                        print("Sorry! Parking lot is full")
                elif n[0] == "Slot_numbers_for_driver_of_age":
                    slots = parking_lot.fetch_slots_for_driver(n[1])
                    if slots:
                        print(slots)
                    else:
                        print("There is no car with driver age {0} parked".format(n[1]))
                elif n[0] == "Slot_number_for_car_with_number":
                    slot_number = parking_lot.fetch_slot_for_car(n[1])
                    if slot_number:
                        print(slot_number)
                    else:
                        print("There is no car with registration number {0} parked".format(n[1]))
                elif n[0] == "Leave":
                    slot = parking_lot.exit_parking(int(n[1]))
                    if slot:
                        print("Slot number {0} vacated, the car with vehicle registration number {1} left space, "
                              "the driver of the car was of age {2}".format(n[1], slot.car.reg_no, slot.car.driver_age))
                    else:
                        print("Slot already vacant")

                elif n[0] == "Vehicle_registration_number_for_driver_of_age":
                    reg_nos = parking_lot.fetch_vehicle_reg_for_age(n[1])
                    if reg_nos:
                        print(reg_nos)
                    else:
                        print("null")
                else:
                    print("Invalid operation")
        else:
            return "Pass valid input"
    except (IndexError, AttributeError) as e:
        print("Please ensure if you are performing a valid operation")
        raise e


if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print("Please pass a input file")
        exit()
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        contents = f.readlines()
        operate_parking_lot(contents)
