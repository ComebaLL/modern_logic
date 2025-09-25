import tkinter as tk
from tkinter import ttk, messagebox

class POEFrameViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Path of Exile")
        self.root.geometry("600x400")
        
        # Фреймовая структура классов Path of Exile
        self.frames = {
            # Базовые фреймы           
            "character_class": {
                "имя": "Character Class",
                "является": "poe_entity",
                "свойства": "has_subclasses, has_playstyle, has_builds",
                "отличия": "base_character_archetype"
            },
            
            # Конкретные классы
            "duelist": {
                "имя": "Duelist",
                "является": "character_class",
                "свойства": "melee_combat, physical_damage, good_for_beginners",
                "отличия": "agile_melee_fighter"
            },
            
            "ranger": {
                "имя": "Ranger", 
                "является": "character_class",
                "свойства": "ranged_combat, high_evasion, mobile",
                "отличия": "ranged_specialist"
            },
            
            "shadow": {
                "имя": "Shadow",
                "является": "character_class", 
                "свойства": "spellcasting, critical_strikes, stealth",
                "отличия": "high_damage_potential"
            },
            
            "marauder": {
                "имя": "Marauder",
                "является": "character_class",
                "свойства": "melee_combat, tanky, high_health",
                "отличия": "durable_fighter"
            },
            
            "witch": {
                "имя": "Witch",
                "является": "character_class",
                "свойства": "spellcasting, minions, elemental_damage",
                "отличия": "powerful_spellcaster"
            },
            
            "templar": {
                "имя": "Templar", 
                "является": "character_class",
                "свойства": "spellcasting, hybrid, all_rounder",
                "отличия": "spell_attack_hybrid"
            },
            
            "scion": {
                "имя": "Scion",
                "является": "character_class", 
                "свойства": "flexible, adaptable, advanced",
                "отличия": "versatile_class"
            },
            
            
            # Фреймы подклассов Duelist
            "slayer": {
                "имя": "Slayer",
                "является": "duelist",
                "свойства": "area_damage, leech, culling_strike",
                "отличия": "area_melee_specialist"
            },
            
            "champion": {
                "имя": "Champion",
                "является": "duelist",
                "свойства": "impales, taunt, defensive",
                "отличия": "defensive_melee"
            },
            
            "gladiator": {
                "имя": "Gladiator",
                "является": "duelist",
                "свойства": "block, bleed, attack_speed",
                "отличия": "block_specialist"
            },
            
            # Фреймы подклассов Ranger
            "deadeye": {
                "имя": "Deadeye",
                "является": "ranger", 
                "свойства": "projectiles, chain, pierce",
                "отличия": "projectile_specialist"
            },
            
            "pathfinder": {
                "имя": "Pathfinder",
                "является": "ranger",
                "свойства": "flasks, poison, elemental",
                "отличия": "flask_specialist"
            },
            
            "raider": {
                "имя": "Raider",
                "является": "ranger",
                "свойства": "frenzy_charges, phasing, onslaught",
                "отличия": "speed_specialist"
            },
            
            # Фреймы подклассов Shadow
            "assassin": {
                "имя": "Assassin",
                "является": "shadow",
                "свойства": "critical_strikes, poison, deadly_assassin",
                "отличия": "critical_specialist"
            },
            
            "trickster": {
                "имя": "Trickster",
                "является": "shadow",
                "свойства": "evasion, energy_shield, hybrid_defenses",
                "отличия": "evasion_specialist"
            },
            
            "saboteur": {
                "имя": "Saboteur",
                "является": "shadow",
                "свойства": "traps, mines, area_damage",
                "отличия": "trap_mine_specialist"
            },
            
            # Фреймы подклассов Marauder
            "juggernaut": {
                "имя": "Juggernaut",
                "является": "marauder",
                "свойства": "armour, endurance_charges, unstoppable",
                "отличия": "tank_specialist"
            },
            
            "berserker": {
                "имя": "Berserker",
                "является": "marauder",
                "свойства": "rage, attack_damage, warcries",
                "отличия": "damage_specialist"
            },
            
            "chieftain": {
                "имя": "Chieftain",
                "является": "marauder",
                "свойства": "fire_damage, totems, life_regeneration",
                "отличия": "fire_specialist"
            },
            
            # Фреймы подклассов Witch
            "necromancer": {
                "имя": "Necromancer",
                "является": "witch",
                "свойства": "minions, offerings, bone_army", 
                "отличия": "minion_master"
            },
            
            "elementalist": {
                "имя": "Elementalist",
                "является": "witch",
                "свойства": "golems, elemental_damage, ailments",
                "отличия": "elemental_specialist"
            },
            
            "occultist": {
                "имя": "Occultist",
                "является": "witch",
                "свойства": "curses, chaos_damage, energy_shield",
                "отличия": "curse_specialist"
            },
            
            # Фреймы подклассов Templar
            "inquisitor": {
                "имя": "Inquisitor",
                "является": "templar",
                "свойства": "critical_strikes, elemental_damage, consecrated_ground",
                "отличия": "elemental_critical_specialist"
            },
            
            "hierophant": {
                "имя": "Hierophant",
                "является": "templar",
                "свойства": "totems, mana, arcane_surge",
                "отличия": "totem_specialist"
            },
            
            "guardian": {
                "имя": "Guardian",
                "является": "templar",
                "свойства": "auras, defensive, minions",
                "отличия": "aura_specialist"
            },
            
            # Фреймы подклассов Scion
            "ascendant": {
                "имя": "Ascendant",
                "является": "scion",
                "свойства": "versatile, adaptable, multiple_ascendancies",
                "отличия": "jack_of_all_trades"
            }
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Path of Exile", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left frame - List of frames
        left_frame = ttk.LabelFrame(main_frame, text="Доступные фреймы", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.frames_listbox = tk.Listbox(list_frame, width=20, height=15)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.frames_listbox.yview)
        self.frames_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.frames_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Fill listbox with frame names
        for frame_name in sorted(self.frames.keys()):
            self.frames_listbox.insert(tk.END, frame_name)
        
        # Bind selection event
        self.frames_listbox.bind('<<ListboxSelect>>', self.on_frame_select)
        
        # Right frame - Frame details
        right_frame = ttk.LabelFrame(main_frame, text="Детали фрейма", padding="15")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(1, weight=1)
        
        # Frame details widgets - только основные поля
        ttk.Label(right_frame, text="Имя фрейма:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.name_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.name_var, font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(right_frame, text="Является:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.is_a_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.is_a_var, font=("Arial", 10)).grid(row=1, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(right_frame, text="Свойства:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.properties_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.properties_var, font=("Arial", 10), wraplength=400).grid(row=2, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(right_frame, text="Отличия:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.differences_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.differences_var, font=("Arial", 10), wraplength=400).grid(row=3, column=1, sticky=tk.W, pady=8)
        
        # Configure weights for resizing
        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        
        right_frame.rowconfigure(2, weight=1)
        right_frame.rowconfigure(3, weight=1)
        
        # Show first frame by default
        if self.frames:
            self.frames_listbox.selection_set(0)
            self.display_frame_details(list(self.frames.keys())[0])
    
    def on_frame_select(self, event):
        selection = self.frames_listbox.curselection()
        if selection:
            frame_name = self.frames_listbox.get(selection[0])
            self.display_frame_details(frame_name)
    
    def display_frame_details(self, frame_name):
        frame_data = self.frames[frame_name]
        
        # Basic information - только основные поля
        self.name_var.set(frame_data["имя"])
        self.is_a_var.set(frame_data["является"])
        self.properties_var.set(frame_data["свойства"])
        self.differences_var.set(frame_data["отличия"])

def main():
    root = tk.Tk()
    app = POEFrameViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()