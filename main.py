import sys
import copy

'''
    1. Data Structure used: 
            List of objects of type Slot 
            Each slot is composed of:
                Slot number
                Boolean availability - True is the slot is empty and False if it is not
                car/vehicle information of type Car
                Car is composed of:
                    Vehicle registration number 
                    Driver's age
    2. Use object oriented programming to solve this
    3. Base Logic:
            Initalize the parking lot by creating slot of the specified number.
            Slot(number = 1, availability = True, car = None) increasing the slot number 1 upto the specified number
            When the vehicle enters the parking lot, check for the first availability(where Slot(available=True) and assign it to the vehicle by setting Car object to the values specific to the vehicle and available = False
            When the vehicle exits, update the Slot with availability to True and Car = None
'''


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
        self.slots = [] # This list holds objects of type Slot

    def create_slots(self, total):
        for num in range(total):
            # Append Slots with available = True in the beginning.
            self.slots.append(Slot(num+1, True))

    def park_car(self, reg_no, driver_age):
        # Iterate through all slots to check for available ones and assign it to the vehicle
        for slot in self.slots:
            if slot.available:
                slot.car = Car(reg_no, driver_age) # assign the car to the available slot
                slot.available = False # make it unavailable for other cars
                return slot
        return None # returns None with parking lot is full

    def fetch_slots_for_driver(self, driver_age):
        result = []
        # Iterate the slots to check for occupied ones and that match driver's age as specified.
        # Append the slot number to result
        for slot in self.slots:
            if not slot.available and slot.car.driver_age == driver_age:
                result.append(str(slot.number))
        return ",".join(result) # Join the items in result list to form a comma separated string

    def fetch_slot_for_car(self, reg_no):
        # Iterate the slots to check for occupied ones and that match registration number as specified.
        for slot in self.slots:
            if not slot.available and slot.car.reg_no == reg_no:
                # return slot number
                return slot.number
        return None # return None when there is no match found for the registration number

    def exit_parking(self, slot_number):
        # iterate through the slots to look for the car at the specified slot number
        for slot in self.slots:
            if slot.number == slot_number and not slot.available:
                slot.available = True # set the spot to available
                exit_car = copy.deepcopy(slot) # deepcopy the exit car info in order to print results
                slot.car = None # and car object to None so it can used by the future vehicles
                return exit_car
        return None # return None when the slot is already vacant

    def fetch_vehicle_reg_for_age(self, driver_age):
        result = []
        # Iterate the slots to check for occupied ones and that match driver's age as specified.
        # Append the vehicle registration number to result
        for slot in self.slots:
            if not slot.available and slot.car.driver_age == driver_age:
                result.append(str(slot.car.reg_no))
        return ", ".join(result) # Join the items in result list to form a comma separated string. Returns empty string when match was not found


def operate_parking_lot(contents):
    try:
        # Assumption:
        # Registrattion numbers of all cars wil be of same length(13) and follows the same pattern (KA-01-HH-1234)
        # There will be only one Create_parking_lot in the test file and will be in the beginning of the file
        # All cars have a unique registration number
        # Commands will be always in right format
        if contents:
            # If file is not empty
            # Fetch the total number of slots to be created for parking
            total = int(contents[0].strip().split()[1])
            # Initialize the ParkinLot class
            parking_lot = ParkingLot()
            # Create the parking slots
            parking_lot.create_slots(total)
            print("Created parking of {0}".format(total))
            # Perform operation in the Parking lot. Start the line 2 since line 1 is always assumed to be create parking slots.
            for line in contents[1:]:
                n = line.strip().split()
                if n[0] == "Park":
                    # Call method to park car. Pass the 2nd and 4th argument which is the registration number and driver age.
                    slot = parking_lot.park_car(n[1], n[3])
                    if slot:
                        # If slot assigned
                        print("Car with vehicle registration number {0} has been parked at slot number {1}".format(n[1], slot.number))
                    else:
                        # If parking space is full
                        print("Sorry! Parking lot is full")
                elif n[0] == "Slot_numbers_for_driver_of_age":
                    # Method call to fetch the slots assigned to drivers of specific age.
                    slots = parking_lot.fetch_slots_for_driver(n[1])
                    if slots:
                        # Comma separated slot number for driver whose car drivers are of specified age
                        print(slots)
                    else:
                        # if none returned
                        print("There is no car with driver age {0} parked".format(n[1]))
                elif n[0] == "Slot_number_for_car_with_number":
                    # Method to fetch the slot number for a car with specific registration number
                    slot_number = parking_lot.fetch_slot_for_car(n[1])
                    if slot_number:
                        # print the slot number if returned
                        print(slot_number)
                    else:
                        # when no car is present with the specified registration number
                        print("There is no car with registration number {0} parked".format(n[1]))
                elif n[0] == "Leave":
                    # Method to handle the exit of cars from parking space
                    slot = parking_lot.exit_parking(int(n[1]))
                    if slot:
                        # if exit was sucessful
                        print("Slot number {0} vacated, the car with vehicle registration number {1} left space, "
                              "the driver of the car was of age {2}".format(n[1], slot.car.reg_no, slot.car.driver_age))
                    else:
                        # if the specified slot was already empty
                        print("Slot already vacant")

                elif n[0] == "Vehicle_registration_number_for_driver_of_age":
                    # Method to fetch the vehicle registration number with drivers of specific age
                    reg_nos = parking_lot.fetch_vehicle_reg_for_age(n[1])
                    if reg_nos:
                        # Comma separated list of registration numbers returned
                        print(reg_nos)
                    else:
                        # Returns null when there are no vehicles with drivers of specified age
                        print("null")
                else:
                    # Enter here when the input command was invalid
                    print("Invalid operation")
        else:
            #if file is empty, return invalid input message
            return "Pass valid input"
    except (IndexError, AttributeError) as e:
        # Enters here when the specific commands are not in the specified format
        print("Please ensure if you are performing a valid operation")
        raise e


if __name__ == "__main__":
    #Check if input file is passed
    if not len(sys.argv) > 1:
        print("Please pass an input file")
        exit()
    filename = sys.argv[1]
    #Open the file and read the contents
    with open(filename, 'r') as f:
        contents = f.readlines()
        #This method is performing all parking lot operations
        operate_parking_lot(contents)
    print("*************************PROGRAM RAN SUCCESSFULLY**************************************")
