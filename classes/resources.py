import os
import time
from classes.colors import *

# Function to clear the screen
def clear_screen():
    """
    Clears the terminal screen.

    It works on both Windows and Unix systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to show the logo
def display_logo():
    """
    Show the SpeedBox logo on the screen.

    The logo uses colors and special text formatting.
    """
    logo = f"""
    {Colors.BLUE}{Colors.BOLD}
    ███████╗██████╗ ███████╗███████╗██████╗ ██████╗  ██████╗ ██╗  ██╗
    ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝
    ███████╗██████╔╝█████╗  █████╗  ██║  ██║██████╔╝██║   ██║ ╚███╔╝ 
    ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║██╔══██╗██║   ██║ ██╔██╗ 
    ███████║██║     ███████╗███████╗██████╔╝██████╔╝╚██████╔╝██╔╝ ██╗
    ╚══════╝╚═╝     ╚══════╝╚══════╝╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    {Colors.ENDC}
    {Colors.CYAN}Your fast and secure delivery system!{Colors.ENDC}
    """
    print(logo)

# Function to show a welcome message
def welcome_message():
    """
    Clears the screen and shows a welcome message.

    It also shows a loading animation before the system starts.
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.GREEN}{Colors.BOLD}Welcome to SpeedBox!{Colors.ENDC}")
    print(f"{Colors.CYAN}The delivery system that connects customers, businesses, and couriers.{Colors.ENDC}")
    print("\nLoading system", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")
    time.sleep(0.5)

# Function to show the main menu
def main_menu():
    """
    Shows the main menu with options.

    Returns the option the user chose as a string.

    Returns:
        str: The user’s choice (1, 2, or 3).
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}MAIN MENU{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Login")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Register")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Exit")
    
    return input(f"\n{Colors.GREEN}Choose an option: {Colors.ENDC}")
