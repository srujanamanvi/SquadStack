from SquadStack.main import ParkingLot, operate_parking_lot
import os


class TestParkingLot:

    def fetch_parking_lot(self):
        parking_lot = ParkingLot()
        parking_lot.create_slots(2)
        parking_lot.park_car("KA-01-HH-1234", 21)
        parking_lot.park_car("PB-01-HH-1234", 21)
        return parking_lot

    def test_create_slots(self):
        parking_lot = ParkingLot()
        parking_lot.create_slots(4)
        assert len(parking_lot.slots) == 4
        assert parking_lot.slots[0].available == True
        assert parking_lot.slots[0].number == 1
        assert parking_lot.slots[3].number == 4

    def test_read_input_empty(self):
        filename = os.path.abspath("input_empty.txt")
        filehandle = open(filename, 'r')
        contents = filehandle.readlines()
        res = operate_parking_lot(contents)
        assert res == "Pass valid input"

    def test_parking_lot_add(self):
        parking_lot = ParkingLot()
        parking_lot.create_slots(2)
        car1_slot = parking_lot.park_car("KA-01-HH-1234", 21)
        assert car1_slot.number == 1
        assert car1_slot.car.reg_no == "KA-01-HH-1234"
        car2_slot = parking_lot.park_car("PB-01-HH-1234", 21)
        assert car2_slot.number == 2
        assert car2_slot.car.reg_no == "PB-01-HH-1234"

    def test_parking_lot_full(self):
        parking_lot = self.fetch_parking_lot()
        car3_slot = parking_lot.park_car("TN-01-HB-1234", 21)
        assert car3_slot == None

    def test_car_leave_parking(self):
        parking_lot = ParkingLot()
        parking_lot.create_slots(2)
        parking_lot.park_car("KA-01-HH-1234", 21)
        slot = parking_lot.exit_parking(1)
        assert slot.number == 1
        assert slot.car.reg_no == "KA-01-HH-1234"
        assert slot.car.driver_age == 21

    def test_car_park_after_car_exit(self):
        parking_lot = self.fetch_parking_lot()
        exit_slot = parking_lot.exit_parking(1)
        assert exit_slot.number == 1
        slot = parking_lot.park_car("TN-01-HH-1234", 27)
        assert slot.number == 1
        assert slot.car.reg_no == "TN-01-HH-1234"
        assert slot.car.driver_age == 27

    def test_fetch_slots_for_driver(self):
        parking_lot = self.fetch_parking_lot()
        slot = parking_lot.fetch_slots_for_driver(21)
        assert slot == "1,2"

    def test_fetch_slots_for_invalid_driver(self):
        parking_lot = self.fetch_parking_lot()
        slot = parking_lot.fetch_slots_for_driver(18)
        assert slot == ""

    def test_fetch_slot_for_car_number(self):
        parking_lot = self.fetch_parking_lot()
        parking_lot.fetch_slot_for_car("PB-01-HH-1234")
        assert parking_lot.slots[1].car.reg_no == "PB-01-HH-1234"
        assert parking_lot.slots[1].number == 2

    def test_fetch_slot_for_car_number_invalid(self):
        parking_lot = self.fetch_parking_lot()
        slot = parking_lot.fetch_slot_for_car("PB-02-HH-1234")
        assert slot == None

    def test_fetch_vehicle_reg_for_age(self):
        parking_lot = self.fetch_parking_lot()
        slot = parking_lot.fetch_vehicle_reg_for_age(21)
        assert slot == 'KA-01-HH-1234, PB-01-HH-1234'

    def test_fetch_vehicle_reg_for_age_invalid(self):
        parking_lot = self.fetch_parking_lot()
        slot = parking_lot.fetch_vehicle_reg_for_age(18)
        assert slot == ''
