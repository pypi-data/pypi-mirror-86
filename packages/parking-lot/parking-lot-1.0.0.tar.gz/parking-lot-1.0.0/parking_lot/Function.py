import colorama
from colorama import Fore, Back, Style
       



def create_parking_slot(total_number_of_slots,parking_queue):
    
    for i in range(total_number_of_slots):
        parking_queue.append(0)
    
    print("\n")
    print(Fore.GREEN + f"Created a parking lot with {total_number_of_slots} slots.")
    print(Style.RESET_ALL)

    

def modify_parking_slot(extended_number_of_slots,parking_queue):
    
    for i in range(extended_number_of_slots):
        parking_queue.append(0)
    
    print("\n")
    print(Fore.GREEN + f"Extended parking lot with {extended_number_of_slots} slots.")
    print(Style.RESET_ALL)



def allocate_parking_slot(total_numbers_of_slots,parking_queue):

    
    
    for slot_number in range(total_numbers_of_slots):
            
        if(parking_queue[slot_number] == 0):
            parking_queue[slot_number] = 1
            return slot_number + 1
    
def free_parking_slot(slot_number,total_number_of_slots,parking_queue):

    if((slot_number < 1) or (slot_number > total_number_of_slots)):

        return -1
        

    else:
        slot_number = slot_number - 1
        if(parking_queue[slot_number] == 0):
            return 0
            
        else:
            parking_queue[slot_number] = 0
            return 1


def display_avaiable_slot(total_numbers_of_slots,parking_queue):

    print("\n")
    print(Fore.GREEN + "List of Avaiable_slot: ")
    print(Style.RESET_ALL)
    
    for slot_number in range(total_numbers_of_slots):
        
        if(parking_queue[slot_number] == 0):

            print(slot_number + 1)

