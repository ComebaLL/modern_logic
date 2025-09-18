class POEExpertSystem:
    def __init__(self):
        self.classes = {
            "duelist": {
                "name": "Duelist",
                "subclasses": ["slayer", "champion", "gladiator"],
                "builds": {
                    "slayer": ["Boneshatter", "Cyclone", "Flicker Strike"],
                    "champion": ["Spectral Helix", "Lightning Strike", "Armour Stacker"],
                    "gladiator": ["Bleed Lacerate", "Blade Flurry", "Max Block Shattering Steel"]
                },
                "playstyle": "melee combat"
            },
            "ranger": {
                "name": "Ranger",
                "subclasses": ["deadeye", "pathfinder", "raider"],
                "builds": {
                    "deadeye": ["Lightning Arrow", "Ice Shot", "Tornado Shot"],
                    "pathfinder": ["Toxic Rain", "Caustic Arrow", "Scourge Arrow"],
                    "raider": ["Spectral Throw", "Frost Blades", "Elemental Hit"]
                },
                "playstyle": "ranged combat"
            },
            "shadow": {
                "name": "Shadow",
                "subclasses": ["assassin", "trickster", "saboteur"],
                "builds": {
                    "assassin": ["Poisonous Concoction", "Blade Trap", "CoC Ice Spear"],
                    "trickster": ["ED/Contagion", "Lightning Trap", "Winter Orb"],
                    "saboteur": ["Lightning Trap", "Ice Trap", "Explosive Trap"]
                },
                "playstyle": "spellcasting"
            },
            "marauder": {
                "name": "Marauder",
                "subclasses": ["juggernaut", "berserker", "chieftain"],
                "builds": {
                    "juggernaut": ["Boneshatter", "Static Strike", "Accuracy Stacking"],
                    "berserker": ["Earthshatter", "Tectonic Slam", "Rage Vortex"],
                    "chieftain": ["Volcanic Fissure", "Consecrated Path", "Fire Cyclone"]
                },
                "playstyle": "melee combat"
            },
            "witch": {
                "name": "Witch",
                "subclasses": ["necromancer", "elementalist", "occultist"],
                "builds": {
                    "necromancer": ["Skeleton Warriors", "Zombie Army", "Carrion Golem"],
                    "elementalist": ["Arc", "Winter Orb", "Golementalist"],
                    "occultist": ["Bane", "Cold DOT", "Power Siphon"]
                },
                "playstyle": "minions/summons"
            },
            "templar": {
                "name": "Templar",
                "subclasses": ["inquisitor", "hierophant", "guardian"],
                "builds": {
                    "inquisitor": ["Spark", "Storm Brand", "CoC"],
                    "hierophant": ["Freezing Pulse", "Arc", "Manabond"],
                    "guardian": ["Dominating Blow", "SRS", "Aura Stacker"]
                },
                "playstyle": "spellcasting"
            },
            "scion": {
                "name": "Scion",
                "subclasses": ["necromancer", "elementalist", "occultist"],
                "builds": {
                    "necromancer": ["Absolution", "Skeleton Mages", "Spectre"],
                    "elementalist": ["Exsanguinate", "Winter Orb", "CoC"],
                    "occultist": ["Cold DOT", "Bane", "Int Stacker"]
                },
                "playstyle": "flexible"
            }
        }
        
        # Создаем словарь для обратного поиска билдов
        self.build_info = {}
        self._create_build_reverse_index()
        
        self.playstyle_questions = {
            "playstyle": {
                "question": "What playstyle do you prefer?",
                "options": {
                    "1": "melee combat",
                    "2": "ranged combat", 
                    "3": "spellcasting",
                    "4": "minions/summons"
                }
            },
            "budget": {
                "question": "What's your build budget?",
                "options": {
                    "1": "free/cheap (self-found)",
                    "2": "medium (a few divine orbs)",
                    "3": "expensive (min-max build)"
                }
            }
        }
        
        self.selected_class = None
        self.selected_subclass = None
        self.selected_build = None
        self.user_preferences = {}
        self.available_classes = []
    
    def _create_build_reverse_index(self):
        """Создает обратный индекс для поиска информации по билдам"""
        for class_key, class_data in self.classes.items():
            for subclass in class_data["subclasses"]:
                builds = class_data["builds"][subclass]
                for i, build in enumerate(builds):
                    budget_level = ""
                    if i == 0:
                        budget_level = "free/cheap (self-found)"
                    elif i == 1:
                        budget_level = "medium (a few divine orbs)"
                    else:
                        budget_level = "expensive (min-max build)"
                    
                    self.build_info[build.lower()] = {
                        "class": class_key,
                        "class_name": class_data["name"],
                        "subclass": subclass,
                        "playstyle": class_data["playstyle"],
                        "budget": budget_level,
                        "full_build_name": build
                    }
    
    def display_menu(self, options, title):
        print(f"\n{title}")
        print("=" * 40)
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                choice = input("\nChoose option (1-{}): ".format(len(options)))
                choice_index = int(choice) - 1
                
                if 0 <= choice_index < len(options):
                    return options[choice_index]
                else:
                    print("Please choose a number from the list!")
            except ValueError:
                print("Please enter a number!")
    
    def ask_playstyle_questions(self):
        for question_key, question_data in self.playstyle_questions.items():
            print(f"\n{question_data['question']}")
            for key, option in question_data['options'].items():
                print(f"{key}. {option}")
            
            while True:
                choice = input("Your choice (1-{}): ".format(len(question_data['options'])))
                if choice in question_data['options']:
                    selected_option = question_data['options'][choice]
                    self.user_preferences[question_key] = selected_option
                    print(f"Selected: {selected_option}")
                    break
                else:
                    print("Please choose a valid option!")
    
    def filter_classes_by_playstyle(self):
        playstyle = self.user_preferences.get('playstyle', '')
        
        if "melee" in playstyle:
            self.available_classes = ["duelist", "marauder", "scion"]
        elif "ranged" in playstyle:
            self.available_classes = ["ranger", "scion"]
        elif "spell" in playstyle:
            self.available_classes = ["shadow", "templar", "witch", "scion"]
        elif "minion" in playstyle:
            self.available_classes = ["witch", "scion"]
        else:
            self.available_classes = list(self.classes.keys())
        
        return self.available_classes
    
    def select_class(self):
        filtered_classes = self.filter_classes_by_playstyle()
        
        if not filtered_classes:
            print("No classes available for your selected playstyle.")
            return None
        
        class_names = [self.classes[cls]['name'] for cls in filtered_classes]
        selected_class_name = self.display_menu(class_names, "Choose your character class")
        
        for key, data in self.classes.items():
            if data['name'] == selected_class_name:
                self.selected_class = key
                break
        
        return self.selected_class
    
    def select_subclass(self):
        if not self.selected_class:
            return None
        
        subclass_options = self.classes[self.selected_class]["subclasses"]
        self.selected_subclass = self.display_menu(subclass_options, 
                                                  f"Choose subclass for {self.classes[self.selected_class]['name']}")
        return self.selected_subclass
    
    def select_build(self):
        if not self.selected_class or not self.selected_subclass:
            return None
        
        budget = self.user_preferences.get('budget', '')
        build_options = self.classes[self.selected_class]["builds"][self.selected_subclass]
        
        # Автоматически выбираем билд на основе бюджета
        if "cheap" in budget:
            selected_build = build_options[0]
        elif "medium" in budget:
            selected_build = build_options[1]
        else:
            selected_build = build_options[2]
        
        print(f"\nBased on your budget preference, recommended build:")
        print(f"{selected_build}")
        
        # Показываем все варианты
        print(f"\nAll available builds for {self.selected_subclass}:")
        for i, build in enumerate(build_options, 1):
            print(f"{i}. {build}")
        
        # Даём возможность выбрать другой билд
        while True:
            choice = input("\nPress Enter to accept recommended build or choose another (1-3): ").strip()
            if choice == "":
                self.selected_build = selected_build
                break
            elif choice in ["1", "2", "3"]:
                self.selected_build = build_options[int(choice) - 1]
                break
            else:
                print("Please enter 1, 2, 3 or press Enter")
        
        return self.selected_build
    
    def show_final_recommendation(self):
        if not self.selected_build:
            return
        
        print(f"\nClass: {self.classes[self.selected_class]['name']}")
        print(f"Subclass: {self.selected_subclass}")
        print(f"Build: {self.selected_build}")
        print("="*40)
        
        self.give_final_advice()
    
    def give_final_advice(self):
        playstyle = self.user_preferences.get('playstyle', '')
        budget = self.user_preferences.get('budget', '')
        
        print(f"\nBased on your preferences:")
        print(f"Playstyle: {playstyle}")
        print(f"Budget: {budget}")
        
        class_advice = {
            "duelist": "Great for melee combat and physical damage. Good for beginners.",
            "ranger": "Master of ranged attacks and evasion. Versatile and mobile.",
            "shadow": "Specializes in critical strikes and stealth. High damage potential.",
            "marauder": "Tanky fighter with high health and damage. Very durable.",
            "witch": "Powerful spellcaster with minions and elemental damage.",
            "templar": "Hybrid class combining spells and attacks. Good all-rounder.",
            "scion": "Flexible class that can adapt to many playstyles. Advanced class."
        }
        
        if self.selected_class in class_advice:
            print(f"Advice: {class_advice[self.selected_class]}")
    
    def backward_chain(self):
        """Обратный логический вывод - поиск по названию билда"""
        print("\nBACKWARD CHAINING")
        print("Enter build name to get information about it")
        #print("Available builds: ", end="")
        
        # Показываем несколько примеров билдов
        example_builds = list(self.build_info.keys())[:5]
        print(", ".join([self.build_info[b]['full_build_name'] for b in example_builds]) + ", ...")
        
        while True:
            build_input = input("\nEnter build name (or 'quit' to exit): ").strip().lower()
            
            if build_input == 'quit':
                break
            
            if build_input in self.build_info:
                info = self.build_info[build_input]
                #print("\n" + "="*50)
                print(f"BUILD INFORMATION: {info['full_build_name']}")
                #print("="*50)
                print(f"Class: {info['class_name']}")
                print(f"Subclass: {info['subclass']}")
                print(f"Playstyle: {info['playstyle']}")
                print(f"Budget: {info['budget']}")
                #print("="*50)
            else:
                print("Build not found. Please try another name.")
                # Подсказка похожих билдов
                similar = [b for b in self.build_info.keys() if build_input in b]
                if similar:
                    print("Similar builds: " + ", ".join([self.build_info[b]['full_build_name'] for b in similar[:3]]))
    
    def forward_chain(self):
        """Прямой логический вывод - выбор через вопросы"""
        #print("\n=== FORWARD CHAINING ===")
        self.ask_playstyle_questions()
        
        if self.select_class():
            if self.select_subclass():
                self.select_build()
                self.show_final_recommendation()
    
    def run(self):
        print("PATH OF EXILE EXPERT SYSTEM")
        
        while True:
            print("\nChoose mode:")
            print("1. Forward chaining (answer questions to get build)")
            print("2. Backward chaining (enter build name to get info)")
            #print("3. Exit")
            
            choice = input("Select mode (1-2): ").strip()
            
            if choice == "1":
                self.forward_chain()
            elif choice == "2":
                self.backward_chain()
            elif choice == "3":
                #print("Goodbye! Good luck in Wraeclast!")
                break
            else:
                print("Invalid choice. Please select 1, 2 or 3.")

def main():
    expert_system = POEExpertSystem()
    expert_system.run()

if __name__ == "__main__":
    main()