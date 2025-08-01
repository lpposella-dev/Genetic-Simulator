import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading

class GeneticSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Simulator")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Genetic features and their inheritance patterns
        self.genetic_features = {
            'skin_color': {
                'options': ['black', 'brown', 'white'],
                'dominant': ['black', 'brown'],
                'recessive': ['white'],
                'probabilities': {'black': 0.3, 'brown': 0.5, 'white': 0.2}
            },
            'ethnicity': {
                'options': ['occidental', 'european', 'asiatic', 'mid-eastern', 'african'],
                'sub_options': {
                    'asiatic': ['japan', 'korea', 'china'],
                    'mid-eastern': ['saudi arabia', 'india', 'iraq', 'iran'],
                    'african': ['north africa', 'sub-saharan', 'east africa', 'west africa', 'central africa']
                },
                'probabilities': {'occidental': 0.2, 'european': 0.2, 'asiatic': 0.2, 'mid-eastern': 0.2, 'african': 0.2}
            },
            'eye_color': {
                'options': ['blue', 'green', 'brown', 'black'],
                'dominant': ['brown', 'black'],
                'recessive': ['blue', 'green'],
                'probabilities': {'brown': 0.55, 'black': 0.25, 'blue': 0.15, 'green': 0.05}
            },
            'hair_color': {
                'options': ['black', 'dark-brown', 'light-brown', 'blonde'],
                'dominant': ['black', 'dark-brown'],
                'recessive': ['light-brown', 'blonde'],
                'probabilities': {'black': 0.4, 'dark-brown': 0.35, 'light-brown': 0.15, 'blonde': 0.1}
            },
            'hair_style': {
                'options': ['curly', 'straight', 'wavy', 'blackpower'],
                'probabilities': {'curly': 0.25, 'straight': 0.4, 'wavy': 0.25, 'blackpower': 0.1}
            }
        }
        
        # Genetic mutations
        self.mutations = {
            'redhead': {
                'probability': 0.02,  # 2% chance
                'features': {
                    'hair_color': 'red',
                    'skin_color': 'white',
                    'eye_color': ['green', 'blue']
                }
            },
            'albinism': {
                'probability': 0.005,  # 0.5% chance
                'features': {
                    'hair_color': 'white',
                    'skin_color': 'white',
                    'eye_color': 'blue'
                }
            }
        }
        
        # Parent data
        self.father_data = {}
        self.mother_data = {}
        self.current_parent = 'father'
        self.current_feature = 0
        self.feature_list = list(self.genetic_features.keys())
        self.family_twin_history = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="🧬 Genetic Simulator 🧬",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Instructions
        self.instruction_label = tk.Label(
            self.main_frame,
            text="Let's collect Father's genetic information",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#34495e'
        )
        self.instruction_label.pack(pady=(0, 20))
        
        # Feature display
        self.feature_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.feature_label.pack(pady=(0, 20))
        
        # Options frame
        self.options_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.options_frame.pack(pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.main_frame,
            variable=self.progress_var,
            maximum=len(self.feature_list) * 2 + 1,  # +1 for twin history question
            length=400
        )
        self.progress_bar.pack(pady=20)
        
        # Progress label
        self.progress_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.progress_label.pack()
        
        # Results frame (initially hidden)
        self.results_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        
        # Start the data collection
        self.collect_feature_data()
        
    def collect_feature_data(self):
        if self.current_feature >= len(self.feature_list):
            if self.current_parent == 'father':
                self.current_parent = 'mother'
                self.current_feature = 0
                self.instruction_label.config(text="Now let's collect Mother's genetic information")
                self.collect_feature_data()
            else:
                self.ask_twin_history()
                return
        
        feature = self.feature_list[self.current_feature]
        self.feature_label.config(text=f"Select {feature.replace('_', ' ').title()}:")
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Create option buttons
        options = self.genetic_features[feature]['options']
        for i, option in enumerate(options):
            btn = tk.Button(
                self.options_frame,
                text=option.replace('-', ' ').title(),
                font=('Arial', 12),
                bg='#3498db',
                fg='white',
                relief='flat',
                padx=20,
                pady=10,
                command=lambda opt=option: self.select_option(feature, opt)
            )
            btn.pack(pady=5)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#2980b9'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#3498db'))
        
        # Update progress
        if self.current_parent == 'father':
            progress = self.current_feature
        else:
            progress = len(self.feature_list) + self.current_feature
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{self.current_parent.title()} - {self.current_feature + 1}/{len(self.feature_list)}")
        
    def select_option(self, feature, option):
        if self.current_parent == 'father':
            self.father_data[feature] = option
        else:
            self.mother_data[feature] = option
        
        self.current_feature += 1
        self.collect_feature_data()
    
    def ask_twin_history(self):
        """Ask about family twin history"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Twin history question
        title_label = tk.Label(
            self.main_frame,
            text="🧬 Genetic Simulator 🧬",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        question_label = tk.Label(
            self.main_frame,
            text="Family Twin History",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#34495e'
        )
        question_label.pack(pady=(0, 10))
        
        explanation_label = tk.Label(
            self.main_frame,
            text="Are there twins in the mother's family history?\nThis affects the chance of having non-identical twins.",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#7f8c8d',
            justify='center'
        )
        explanation_label.pack(pady=(0, 30))
        
        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        buttons_frame.pack()
        
        yes_btn = tk.Button(
            buttons_frame,
            text="Yes, there are twins in the family",
            font=('Arial', 14),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=30,
            pady=15,
            command=lambda: self.set_twin_history(True)
        )
        yes_btn.pack(side='left', padx=10)
        
        no_btn = tk.Button(
            buttons_frame,
            text="No twin history",
            font=('Arial', 14),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=30,
            pady=15,
            command=lambda: self.set_twin_history(False)
        )
        no_btn.pack(side='left', padx=10)
        
        # Update progress
        progress = len(self.feature_list) * 2
        self.progress_var.set(progress)
        self.progress_label.config(text="Twin History Question")
    
    def set_twin_history(self, has_twins):
        """Set twin history and generate baby"""
        self.family_twin_history = has_twins
        
        # Show loading screen
        self.show_loading_screen()
        
        # Generate baby in a separate thread
        def generate():
            time.sleep(2)  # Simulate processing time
            babies = self.generate_babies()
            self.root.after(0, lambda: self.show_results(babies, len(babies) > 1))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def generate_babies(self):
        """Generate babies based on twin probability"""
        # Check for identical twins first (same for everyone)
        identical_twin_chance = 0.003  # 0.3% chance for identical twins
        
        if random.random() < identical_twin_chance:
            # Identical twins
            baby1 = self.create_baby()
            baby2 = self.create_baby()
            # Make them identical (same genetic features except for minor variations)
            baby2.update(baby1)
            baby2['identical_twin'] = True
            baby1['identical_twin'] = True
            return [baby1, baby2]
        
        # Check for non-identical twins based on family history
        non_identical_chance = 0.10 if self.family_twin_history else 0.03  # 10% vs 3%
        
        if random.random() < non_identical_chance:
            # Non-identical twins
            baby1 = self.create_baby()
            baby2 = self.create_baby()
            return [baby1, baby2]
        
        # Single baby
        baby = self.create_baby()
        return [baby]
        
    def show_loading_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Loading screen
        loading_label = tk.Label(
            self.main_frame,
            text="🧬 Generating Baby 🧬",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        loading_label.pack(pady=(100, 20))
        
        # Animated dots
        self.dots_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 16),
            bg='#f0f0f0',
            fg='#3498db'
        )
        self.dots_label.pack()
        
        self.animate_loading()
        

        
    def show_loading_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Loading screen
        loading_label = tk.Label(
            self.main_frame,
            text="🧬 Generating Baby 🧬",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        loading_label.pack(pady=(100, 20))
        
        # Animated dots
        self.dots_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 16),
            bg='#f0f0f0',
            fg='#3498db'
        )
        self.dots_label.pack()
        
        self.animate_loading()
        
    def animate_loading(self):
        dots = self.dots_label.cget("text")
        if len(dots) >= 3:
            dots = ""
        else:
            dots += "."
        
        self.dots_label.config(text=dots)
        self.root.after(500, self.animate_loading)
        
    def create_baby(self):
        # Check for mutations first
        mutation = self.check_mutations()
        
        baby = {
            'sex': random.choice(['Male', 'Female']),
            'mutation': mutation
        }
        
        # Generate genetic features
        for feature in self.feature_list:
            if mutation and feature in mutation['features']:
                if isinstance(mutation['features'][feature], list):
                    baby[feature] = random.choice(mutation['features'][feature])
                else:
                    baby[feature] = mutation['features'][feature]
            else:
                baby[feature] = self.inherit_feature(feature)
        
        return baby
    
    def check_mutations(self):
        for mutation_name, mutation_data in self.mutations.items():
            if random.random() < mutation_data['probability']:
                return {'name': mutation_name, 'features': mutation_data['features']}
        return None
    
    def inherit_feature(self, feature):
        father_value = self.father_data[feature]
        mother_value = self.mother_data[feature]
        
        feature_data = self.genetic_features[feature]
        
        # Check if both parents have the same value (homozygous)
        if father_value == mother_value:
            return father_value
        
        # Complex genetic inheritance with multiple factors
        inheritance_score = self.calculate_inheritance_score(feature, father_value, mother_value)
        
        # Apply Mendelian genetics with modern complexity
        if 'dominant' in feature_data:
            dominant_inheritance = self.calculate_dominant_inheritance(feature, father_value, mother_value)
            if dominant_inheritance is not None:
                return dominant_inheritance
        
        # Multi-allelic inheritance with epistatic interactions
        final_probabilities = self.calculate_complex_probabilities(feature, father_value, mother_value, inheritance_score)
        
        # Apply genetic drift and selection pressure
        final_probabilities = self.apply_genetic_drift(final_probabilities, feature)
        
        # Select based on complex probability distribution
        return self.select_from_probability_distribution(final_probabilities)
    
    def calculate_inheritance_score(self, feature, father_value, mother_value):
        """Calculate inheritance score based on genetic distance and compatibility"""
        import math
        
        feature_data = self.genetic_features[feature]
        options = feature_data['options']
        
        # Calculate genetic distance between parents
        father_index = options.index(father_value)
        mother_index = options.index(mother_value)
        genetic_distance = abs(father_index - mother_index) / (len(options) - 1)
        
        # Calculate compatibility score using cosine similarity
        father_vector = [1 if i == father_index else 0 for i in range(len(options))]
        mother_vector = [1 if i == mother_index else 0 for i in range(len(options))]
        
        dot_product = sum(a * b for a, b in zip(father_vector, mother_vector))
        magnitude_father = math.sqrt(sum(a * a for a in father_vector))
        magnitude_mother = math.sqrt(sum(a * a for a in mother_vector))
        
        if magnitude_father * magnitude_mother == 0:
            compatibility = 0
        else:
            compatibility = dot_product / (magnitude_father * magnitude_mother)
        
        # Combine distance and compatibility
        inheritance_score = (1 - genetic_distance) * 0.6 + compatibility * 0.4
        return inheritance_score
    
    def calculate_dominant_inheritance(self, feature, father_value, mother_value):
        """Calculate dominant/recessive inheritance with complex probability"""
        feature_data = self.genetic_features[feature]
        
        if 'dominant' not in feature_data:
            return None
        
        # Calculate dominance strength
        father_dominant = father_value in feature_data['dominant']
        mother_dominant = mother_value in feature_data['dominant']
        
        if father_dominant and not mother_dominant:
            # Father has dominant, Mother has recessive
            dominance_strength = self.calculate_dominance_strength(father_value, feature)
            inheritance_prob = 0.75 + (dominance_strength * 0.2)
            return father_value if random.random() < inheritance_prob else mother_value
            
        elif mother_dominant and not father_dominant:
            # Mother has dominant, Father has recessive
            dominance_strength = self.calculate_dominance_strength(mother_value, feature)
            inheritance_prob = 0.75 + (dominance_strength * 0.2)
            return mother_value if random.random() < inheritance_prob else father_value
        
        return None
    
    def calculate_dominance_strength(self, trait, feature):
        """Calculate the strength of dominance for a given trait"""
        feature_data = self.genetic_features[feature]
        
        if 'dominant' not in feature_data:
            return 0.5
        
        # Calculate dominance strength based on trait position and frequency
        if trait in feature_data['dominant']:
            base_strength = 0.8
            # Adjust based on trait frequency
            trait_frequency = feature_data['probabilities'].get(trait, 0.25)
            frequency_factor = 1 + (trait_frequency - 0.25) * 2
            return min(1.0, base_strength * frequency_factor)
        
        return 0.3
    
    def calculate_complex_probabilities(self, feature, father_value, mother_value, inheritance_score):
        """Calculate complex inheritance probabilities with epistatic interactions"""
        import math
        
        feature_data = self.genetic_features[feature]
        options = feature_data['options']
        
        # Initialize base probabilities
        base_probabilities = feature_data['probabilities'].copy()
        
        # Apply parent influence with inheritance score
        for option in options:
            parent_influence = 0
            
            if option == father_value:
                parent_influence += inheritance_score * 2.0
            if option == mother_value:
                parent_influence += inheritance_score * 2.0
            
            # Apply epistatic interactions (trait interactions)
            epistatic_factor = self.calculate_epistatic_interactions(feature, option)
            
            # Apply Hardy-Weinberg equilibrium considerations
            hw_factor = self.calculate_hardy_weinberg_factor(feature, option, base_probabilities)
            
            # Special handling for ethnicity based on skin color
            if feature == 'ethnicity':
                skin_color_factor = self.calculate_ethnicity_skin_correlation(option)
                base_probabilities[option] *= skin_color_factor
            
            # Combine all factors
            final_prob = base_probabilities[option] * (1 + parent_influence) * epistatic_factor * hw_factor
            base_probabilities[option] = max(0.01, final_prob)  # Ensure minimum probability
        
        return base_probabilities
    
    def calculate_ethnicity_skin_correlation(self, ethnicity):
        """Calculate ethnicity probability adjustment based on skin color"""
        # Use parent skin colors to estimate baby's likely skin color
        father_skin = self.father_data.get('skin_color', 'brown')
        mother_skin = self.mother_data.get('skin_color', 'brown')
        
        # Simple estimation of baby's likely skin color
        if father_skin == mother_skin:
            estimated_skin = father_skin
        else:
            # If parents have different skin colors, estimate based on dominance
            if 'black' in [father_skin, mother_skin]:
                estimated_skin = 'black'
            elif 'brown' in [father_skin, mother_skin]:
                estimated_skin = 'brown'
            else:
                estimated_skin = 'white'
        
        # Define correlation factors between skin color and ethnicity
        # Occidental is less likely with darker skin colors
        correlation_factors = {
            'occidental': {
                'black': 0.3,    # Much lower probability
                'brown': 0.6,    # Lower probability
                'white': 1.5     # Higher probability
            },
            'european': {
                'black': 0.4,    # Lower probability
                'brown': 0.8,    # Slightly lower
                'white': 1.3     # Higher probability
            },
            'asiatic': {
                'black': 1.2,    # Higher probability
                'brown': 1.1,    # Slightly higher
                'white': 0.9     # Slightly lower
            },
            'mid-eastern': {
                'black': 1.1,    # Slightly higher
                'brown': 1.2,    # Higher probability
                'white': 0.8     # Lower probability
            },
            'african': {
                'black': 1.4,    # Much higher probability
                'brown': 1.3,    # Higher probability
                'white': 0.5     # Much lower probability
            }
        }
        
        # Get the correlation factor for this ethnicity and estimated skin color
        if ethnicity in correlation_factors and estimated_skin in correlation_factors[ethnicity]:
            return correlation_factors[ethnicity][estimated_skin]
        
        return 1.0  # No adjustment if not found
    
    def calculate_epistatic_interactions(self, feature, trait):
        """Calculate epistatic interactions between traits"""
        # Simulate how one trait affects the expression of others
        epistatic_factors = {
            'skin_color': {
                'black': 1.2, 'brown': 1.0, 'white': 0.8
            },
            'eye_color': {
                'brown': 1.1, 'black': 1.0, 'blue': 0.9, 'green': 0.8
            },
            'hair_color': {
                'black': 1.15, 'dark-brown': 1.0, 'light-brown': 0.9, 'blonde': 0.85
            }
        }
        
        if feature in epistatic_factors and trait in epistatic_factors[feature]:
            return epistatic_factors[feature][trait]
        
        return 1.0
    
    def calculate_hardy_weinberg_factor(self, feature, trait, base_probabilities):
        """Calculate Hardy-Weinberg equilibrium factor"""
        import math
        
        # Calculate allele frequencies
        p = base_probabilities[trait]
        q = 1 - p
        
        # Hardy-Weinberg equilibrium: p² + 2pq + q² = 1
        # For heterozygote advantage, we adjust the factor
        hw_factor = 1.0
        
        if p > 0 and q > 0:
            # Calculate expected frequency under Hardy-Weinberg
            expected_freq = p * p + 2 * p * q
            observed_freq = p
            
            # Adjust factor based on deviation from equilibrium
            if observed_freq > 0:
                hw_factor = expected_freq / observed_freq
                hw_factor = max(0.5, min(2.0, hw_factor))  # Clamp between 0.5 and 2.0
        
        return hw_factor
    
    def apply_genetic_drift(self, probabilities, feature):
        """Apply genetic drift effects to probabilities"""
        import math
        
        # Simulate genetic drift with random fluctuations
        drift_factor = random.gauss(1.0, 0.1)  # Normal distribution with mean 1, std 0.1
        drift_factor = max(0.5, min(1.5, drift_factor))  # Clamp between 0.5 and 1.5
        
        # Apply drift to all probabilities
        drifted_probabilities = {}
        for trait, prob in probabilities.items():
            drifted_prob = prob * drift_factor
            drifted_probabilities[trait] = max(0.01, drifted_prob)
        
        return drifted_probabilities
    
    def select_from_probability_distribution(self, probabilities):
        """Select trait based on complex probability distribution"""
        import math
        
        # Convert to cumulative distribution
        traits = list(probabilities.keys())
        probs = list(probabilities.values())
        
        # Normalize probabilities
        total_prob = sum(probs)
        if total_prob == 0:
            return random.choice(traits)
        
        normalized_probs = [p / total_prob for p in probs]
        
        # Use inverse transform sampling for selection
        rand = random.random()
        cumulative = 0
        
        for i, prob in enumerate(normalized_probs):
            cumulative += prob
            if rand <= cumulative:
                return traits[i]
        
        # Fallback
        return random.choice(traits)
    
    def show_results(self, babies, twins=False):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Results title
        title = "Twins Generated!" if twins else "Baby Generated!"
        title_label = tk.Label(
            self.main_frame,
            text=f"🧬 {title} 🧬",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        # Results frame
        results_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        results_frame.pack(expand=True, fill='both')
        
        for i, baby in enumerate(babies):
            baby_frame = tk.Frame(results_frame, bg='#ecf0f1', relief='raised', bd=2)
            baby_frame.pack(fill='x', padx=20, pady=10)
            
            # Baby title
            baby_title = f"Baby {i+1}" if twins else "Baby"
            baby_label = tk.Label(
                baby_frame,
                text=f"{baby_title} ({baby['sex']})",
                font=('Arial', 16, 'bold'),
                bg='#ecf0f1',
                fg='#2c3e50'
            )
            baby_label.pack(pady=(10, 5))
            
            # Mutation indicator
            if baby['mutation']:
                mutation_label = tk.Label(
                    baby_frame,
                    text=f"✨ Mutation: {baby['mutation']['name'].title()} ✨",
                    font=('Arial', 12, 'bold'),
                    bg='#ecf0f1',
                    fg='#e74c3c'
                )
                mutation_label.pack(pady=5)
            
            # Identical twin indicator
            if baby.get('identical_twin', False):
                twin_label = tk.Label(
                    baby_frame,
                    text="👯 Identical Twin 👯",
                    font=('Arial', 12, 'bold'),
                    bg='#ecf0f1',
                    fg='#9b59b6'
                )
                twin_label.pack(pady=5)
            
            # Genetic features
            features_text = ""
            for feature in self.feature_list:
                feature_name = feature.replace('_', ' ').title()
                feature_value = baby[feature].replace('-', ' ').title()
                features_text += f"{feature_name}: {feature_value}\n"
            
            features_label = tk.Label(
                baby_frame,
                text=features_text,
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#34495e',
                justify='left'
            )
            features_label.pack(pady=10)
        
        # New simulation button
        new_sim_btn = tk.Button(
            self.main_frame,
            text="Start New Simulation",
            font=('Arial', 14),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=30,
            pady=15,
            command=self.restart_simulation
        )
        new_sim_btn.pack(pady=20)
        
    def restart_simulation(self):
        # Reset data
        self.father_data = {}
        self.mother_data = {}
        self.current_parent = 'father'
        self.current_feature = 0
        self.family_twin_history = False
        
        # Restart UI
        self.setup_ui()

def main():
    root = tk.Tk()
    app = GeneticSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 