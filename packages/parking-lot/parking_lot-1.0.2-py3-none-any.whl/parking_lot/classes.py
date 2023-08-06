import colorama           # Pre Defined Module, which  helps to display color full output
from colorama import Fore, Back, Style



class parking:


    def __init__(self,car_slot_no,car_registration_no,car_color):    # Constructor
        
        self.car_slot_no = car_slot_no
        self.car_registration_no =  car_registration_no
        self.car_color = car_color

    def Registration_numbers_for_cars_with_colour(self,user_input):   # Member Function

        
        if user_input == self.car_color:
            print(self.car_registration_no)
            return 1

        return 0


    def Slot_numbers_for_cars_with_colour(self,user_input):     # Member Function
        
        if  user_input == self.car_color:
            print(self.car_slot_no)
            return 1
      
        return 0

    def Slot_number_for_registration_number(self,user_input):  # Member Function
        
        if  user_input == self.car_registration_no:
            print(self.car_slot_no)
            return 1
        
        return 0


    def Check_status(self):       # Member Function

        
        print(Fore.RED + "",self.car_slot_no,end="\t\t")

        
        print(Fore.GREEN + "",self.car_registration_no,end="\t\t")

        
        print(Fore.YELLOW + "",self.car_color,end="")
        
        print(Style.RESET_ALL)