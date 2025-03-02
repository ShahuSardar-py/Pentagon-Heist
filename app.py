import json
import random
import os
import sys
import time
from colorama import Fore, Style

class PentagonHeist:
    def __init__(self):
        self.score=0 
        self.gates=3
        self.gatesPassed=0
        self.Code=None
        self.currentTools=[]
        

    #typywriting effect for the terminal
    def typewriter(self, text, color=Fore.WHITE, delay=0.03):
        for char in text:
            sys.stdout.write(color + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    #custom progress - no of gates passes
    def progressbar(self):
        
        passed = self.gates_passed
        total = self.gates
        progress = f"[{'■' * passed}{'□' * (total - passed)}]"
        self.typewriter(f'\n{Fore.YELLOW}Progress= {progress} | Score= {self.score}')

    #main function for running the game
    def start_game(self, score,gates,gatesPassed,progressbar):
        intro=generate_intro()
        self.typewriter(intro, color=Fore.CYAN)

        for attempt in range(1,self.gates+1):
            challenge= get_challenge(attempt)
            self.typewriter(f"\nSecurity Challenge #{attempt}:", color=Fore.YELLOW)
            self.typewriter(challenge.get("description", "No description provided."), color=Fore.MAGENTA)

        #tool ptions
        options=challenge.get("options")
        for idx, option in enumerate(options, 1):
                self.typewriter(f"  {idx}. {option}", color=Fore.GREEN)
        toolInput=input("/nEnter Your Tool choice for this gate.")
        try:
            toolInput=int(toolInput)
            if toolInput < 1 or toolInput > len(options)
        except ValueError:
                self.typewriter("Invalid selection. " + challenge.get("failure", "Security breach!"), color=Fore.RED)
                self.game_over()
                return
        
        chosenTool=toolInput
        if chosenTool == challenge.get("correctTool"):
            self.typewriter(f"Great! Sucessfully infilterated Gate {attempt}")
            gatesPassed+=1
            progressbar()

            
        



    



