import classes     # Module, where I have define my classs and it's member function.
import Function    # Module, where I have define my non member function.
import colorama    # Pre Defined Module, which  helps to display colorfull output. 
from colorama import Fore, Back, Style
from sys import argv


    


def main():

    total_occupied_slot = 0          
    parking_existence  =  0
    print("\n")
    parking_queue = []           # Store The Information of All the slots
    car_record = []              # Store the Record about All the Car.
    #file_pointer = open('C:/Users/shubh/Desktop/input.txt','r') # open the file in a read mode.
    file_pointer = open(argv[1],'r')
    number_of_lines = len(file_pointer.readlines())  # Find the total number of lines from file.
    file_pointer.seek(0) 
    
    
    
    for i in range(number_of_lines):
        
         
        user_input = file_pointer.readline()
        user_input = user_input.replace("\n", "")
        user_input = user_input.split(" ")               # User input from CLI.

        if(user_input[0].startswith("create")):  # Responsible for Craeting a Parking Lot

            
            total_number_of_slots = user_input[1]
            total_number_of_slots = int(total_number_of_slots)
            Function.create_parking_slot(total_number_of_slots,parking_queue)
            parking_existence  =  1



        
        
        elif(user_input[0].startswith("park")): # Responsible for allocate A Car in Parking Lot

            if(parking_existence == 0):
                print(Fore.RED + "No Parking Lot has Created Yet")
                print(Style.RESET_ALL)

            elif(total_number_of_slots == total_occupied_slot):

                print(Fore.RED + "Sorry, parking lot is full")
                print(Style.RESET_ALL)
            
            else:
                check = 0
                
                car_registration_no = user_input[1]
                car_color = user_input[2]
                for i in range(len(car_record)):
                    if car_record[i].car_registration_no == car_registration_no:
                        check = 1
                        print(Fore.RED + "Car is already present with same registration_no")
                        print(Style.RESET_ALL)
                        break


                if(check == 0):

                    car_slot_number = Function.allocate_parking_slot(total_number_of_slots,parking_queue)
                    car_record.append( classes.parking(car_slot_number,car_registration_no,car_color) )
                    print(Fore.GREEN + f"Allocated slot number: {car_slot_number}")
                    total_occupied_slot = total_occupied_slot + 1
                    print(Style.RESET_ALL)

                


        elif(user_input[0].startswith("leave")): # Responsible for deallocate A car from Parking Lot.

            if(parking_existence == 0):
                print(Fore.RED + "No Parking Lot has Created Yet")
                print(Style.RESET_ALL)

            else:

                
                slot_number = user_input[1]
                slot_number = int(slot_number)
                result = Function.free_parking_slot(slot_number,total_number_of_slots,parking_queue)
            
                if(result == -1):
                    print(Fore.RED + "Not A Valid Slot Number")
                    print(Style.RESET_ALL)
            
                elif(result == 0):
                    print(Fore.GREEN + "Slot is already free")
                    print(Style.RESET_ALL)
            
                else:
                
                    for i in range(len(car_record)):
                        if car_record[i].car_slot_no == slot_number:
                            del(car_record[i])
                            total_occupied_slot = total_occupied_slot - 1
                            break
                    
                    
                    print(Fore.GREEN  +  f"Slot number {slot_number} is free Now.")
                    print(Style.RESET_ALL)


        elif(user_input[0].startswith("status")):   # Responsible for display the status of occupied slot.
            print("\n")
            print(Fore.BLUE + "Slot No \t Registration No \t Colour")
            print(Style.RESET_ALL)
            print("\n")

            if(parking_existence == 0):
                print(Fore.RED + "No Parking Lot has Created Yet")
                print(Style.RESET_ALL)

            elif(total_occupied_slot == 0):
                print(Fore.GREEN + "Whole Parking Lot is Free")
                print(Style.RESET_ALL)
            
            else:
                for i in range(len(car_record)):
                    car_record[i].Check_status()
                    print("\n")


        elif(user_input[0].startswith("registration_numbers_for_cars_with_colour")): # Responsible for display the color of car which have XYZ Registration_numbers

            print("\n")


            if(parking_existence == 0):
                print(Fore.RED + "No Parking Lot has Created Yet")
                print(Style.RESET_ALL)

            else:
                
                sum = 0
                user_input = user_input[1]
                print(Fore.GREEN + f"Registration Number of those car which have color: {user_input}")
                print(Style.RESET_ALL)
                for i in range(len(car_record)):
                    sum = sum + car_record[i].Registration_numbers_for_cars_with_colour(user_input)

                if sum == 0:
                    print(Fore.RED + "No Record Found")
                    print(Style.RESET_ALL)
            
            


                
        elif(user_input[0].startswith("slot_numbers_for_cars_with_colour")): # Responsible for display the color of car which have XYZ Slot Number.


            print("\n")

            if(parking_existence == 0):
                print(Fore.RED + "No Parking Lot has Created Yet")
                print(Style.RESET_ALL)

            else:

                sum = 0
                user_input = user_input[1]
                print(Fore.GREEN + f"slots Number of car which have color: {user_input}")
                print(Style.RESET_ALL)
                for i in range(len(car_record)):
                    sum = sum + car_record[i].Slot_numbers_for_cars_with_colour(user_input)

                if sum == 0:
                    print(Fore.RED + "No Record Found")
                    print(Style.RESET_ALL)
            
            

                
                    


        elif(user_input[0].startswith("slot_number_for_registration_number")): # Responsible for display the slot no which have XYZ Registration_numbers.



            print("\n")

            if(parking_existence == 0):
                print(Fore.RED + "No Parking Lot has been Created Yet")
                print(Style.RESET_ALL)
            
            else:
                sum = 0
                user_input = user_input[1]
                print(Fore.GREEN + f"Slots Number of those car which have Registration_number : {user_input}")
                print(Style.RESET_ALL)
                for i in range(len(car_record)):
                    sum = sum + car_record[i].Slot_number_for_registration_number(user_input)

                if sum == 0:
                    print(Fore.RED + "No Record Found")
                    print(Style.RESET_ALL)
                
            

        elif(user_input[0].startswith("modify")):

            
            extended_number_of_slots = user_input[1]
            extended_number_of_slots = int(extended_number_of_slots)
            Function.modify_parking_slot(extended_number_of_slots,parking_queue)
            total_number_of_slots =  total_number_of_slots + extended_number_of_slots 


        elif(user_input[0].startswith("display_avaiable_slot")):


            if(parking_existence == 0):
                
                print(Fore.RED + "No Parking Lot has been Created Yet")
                print(Style.RESET_ALL)

            else:
            
                if(total_occupied_slot == total_number_of_slots):

                    print(Fore.GREEN + "No slot is avaiable, All  are Full")
                    print(Style.RESET_ALL)

                else:
                    Function.display_avaiable_slot(total_number_of_slots,parking_queue)

                    
        
        
        
        elif(user_input[0].startswith("exit")):     # Quit from program
            break 


    file_pointer.close()
    print("\n")
    print(Fore.GREEN +"Thank U ..Happy Coding!!!")



if __name__ == "__main__":
    
    main()        # Main Function

    
    

    

            



            
            
    



    
    

    











        
