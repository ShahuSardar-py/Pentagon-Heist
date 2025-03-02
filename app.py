import json
import random
import os
import sys
import time
from colorama import Fore, Style
from utils import generate_intro, get_challenge

class PentagonHeist:
    def __init__(self):
        self.bounty = 0 
        self.gates = 3
        self.gatesPassed = 0
        self.score = 0

        self.Code = None
        self.currentTools = []
        
    # typywriting effect for the terminal
    def typewriter(self, text, color=Fore.WHITE, delay=0.03):
        if not isinstance(color, str):
            raise ValueError("Color must be a string.")
    
        # Ensure text is a string
        text = str(text)
    
        for char in text:
            sys.stdout.write(color + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # custom progress - no of gates passes
    def progressbar(self):
        passed = self.gatesPassed
        total = self.gates
        progress = f"[{'■' * self.gatesPassed}{'□' * (self.gates - self.gatesPassed)}]"
        self.typewriter(f'\n{Fore.YELLOW}Progress= {progress} | Score= {self.bounty}')
    
    def mainChamber(self):
        self.clear_screen()
        self.typewriter(f"{Fore.GREEN}╔══════════════════════════════════╗")
        self.typewriter(f"║    FINAL CODE DECRYPTED: {Fore.YELLOW}{self.Code}    ║")
        self.typewriter(f"╚══════════════════════════════════╝{Style.RESET_ALL}")
        self.typewriter(f"\n{Fore.CYAN}Total Score: {self.bounty}{Style.RESET_ALL}")
        self.typewriter("\nYou vanish into the night... the perfect digital thief", Fore.MAGENTA)
    
    # main function for running the game
    def start_game(self):
        intro = generate_intro()
        self.typewriter(intro, color=Fore.CYAN)
        
        # New line added: Wait for the user to press Enter to start the mission.
        input("PRESS ENTER TO START THE MISSION")
    
        for attempt in range(1, self.gates + 1):
            challenge = get_challenge(attempt, intro)
            self.Code = challenge.get("Code")
    
            self.typewriter(f"\nSecurity Challenge #{attempt}:", color=Fore.YELLOW)
            self.typewriter(challenge.get("description", "No description provided."), color=Fore.MAGENTA)
        
            options = challenge.get("options", [])
            for idx, option in enumerate(options, 1):
                self.typewriter(f"  {idx}. {option}", color=Fore.GREEN)
    
            # Tool options
            while True:
                try:
                    userChoice = int(input(Fore.BLUE + "Choose your option (enter the number): "))    
                    if 1 <= userChoice <= len(options):  # Changed from self.currentTools to options
                        break
                    else:
                        self.typewriter("Invalid selection", color=Fore.RED)
                except ValueError:
                    self.typewriter("Invalid input. Enter a number corresponding to an option.", color=Fore.YELLOW)
        
            chosen_option = options[userChoice - 1]
            # Compare with correct answer
            if chosen_option == challenge.get("correct"):
                self.typewriter("Success! You've bypassed this security gate.", color=Fore.GREEN)
                self.bounty += 100
                self.gatesPassed += 1  # Update progress
                self.progressbar()
            else:
                self.typewriter("Wrong choice! " + challenge.get("failure", "Security breach!"), color=Fore.RED)
                self.game_over()
                return  # Add return to exit after game over
    
            # Only show main chamber if all gates are passed
        self.mainChamber()
    
    def game_over(self):
        self.typewriter("\nGame Over! The system has locked you out.", color=Fore.RED)
    
if __name__ == "__main__":
    game = PentagonHeist()
    game.start_game()
