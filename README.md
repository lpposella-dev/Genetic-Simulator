# 🧬 Genetic Simulator 🧬

A comprehensive genetic inheritance simulator built with Python and Tkinter that simulates how genetic traits are passed from parents to offspring, including rare mutations.

## Features

### Genetic Traits
The simulator includes the following genetic features:

- **Skin Color**: black, brown, white
- **Ethnicity**: occidental, european, asiatic (japan, korea, china), mid-eastern (saudi arabia, india, iraq, iran), african (north africa, sub-saharan, east africa, west africa, central africa)
- **Eye Color**: blue, green, brown, black
- **Hair Color**: black, dark-brown, light-brown, blonde
- **Hair Style**: curly, straight, wavy, blackpower

### Genetic Mutations
Rare genetic mutations with realistic probabilities:

- **Redhead Mutation** (2% chance):
  - Hair color: red
  - Skin color: white
  - Eye color: green or blue

- **Albinism** (0.5% chance):
  - Hair color: white
  - Skin color: white
  - Eye color: blue

### Inheritance System
The app implements realistic genetic inheritance patterns:

- **Dominant/Recessive Traits**: Some traits are dominant over others
- **Probability-Based Inheritance**: Uses weighted probabilities based on parent traits
- **Mutation Override**: Mutations can override normal inheritance patterns
- **Realistic Twin Generation**: 
  - Identical twins: 0.3% chance (same for everyone)
  - Non-identical twins: 3% base rate, 10% with family history
- **Skin Color-Ethnicity Correlation**: Ethnicity probabilities adjust based on inherited skin color

## How to Use

1. **Run the Application**:
   ```bash
   python genetic_simulator.py
   ```

2. **Data Collection**:
   - The app will guide you through collecting genetic information for Father
   - Then collect genetic information for Mother
   - For each feature, click the button corresponding to the parent's trait
   - Answer the family twin history question for the mother

3. **Generate Offspring**:
   - The app automatically determines if twins occur based on realistic probabilities
   - Identical twins: 0.3% chance (same for everyone)
   - Non-identical twins: 3% base rate, 10% with family history
   - Watch the loading animation while the app processes genetic inheritance
   - View the results showing all inherited traits and any mutations

4. **Results Display**:
   - Baby's sex (Male/Female)
   - All genetic features inherited from parents
   - Any rare mutations that occurred
   - Option to start a new simulation

## Technical Details

### Advanced Genetic Algorithm
The simulator uses a complex, scientifically-inspired inheritance system:

1. **Mutation Check**: First checks for rare mutations
2. **Genetic Distance Calculation**: Uses cosine similarity and genetic distance metrics
3. **Dominant/Recessive Inheritance**: Complex dominance strength calculations
4. **Epistatic Interactions**: Simulates how traits affect each other's expression
5. **Hardy-Weinberg Equilibrium**: Applies population genetics principles
6. **Genetic Drift**: Simulates random genetic fluctuations
7. **Multi-allelic Inheritance**: Handles complex trait combinations
8. **Inverse Transform Sampling**: Advanced probability distribution selection

### User Interface
- Modern, intuitive GUI with Tkinter
- Progress tracking during data collection
- Animated loading screen
- Clear results display with mutation indicators
- Responsive button interactions

## Requirements

- Python 3.6+
- Tkinter (usually included with Python)
- No additional dependencies required

## File Structure

```
genetic_simulator/
├── genetic_simulator.py    # Main application file
└── README.md              # This documentation
```

## Example Usage

1. Launch the application
2. Select Father's traits:
   - Skin Color: Brown
   - Ethnicity: European
   - Eye Color: Blue
   - Hair Color: Dark Brown
   - Hair Style: Straight

3. Select Mother's traits:
   - Skin Color: White
   - Ethnicity: Asiatic
   - Eye Color: Brown
   - Hair Color: Black
   - Hair Style: Wavy

4. Answer family twin history question
5. View results showing automatically generated baby/babies with inherited traits

## Advanced Genetic Science Implementation

This simulator implements sophisticated genetic algorithms inspired by real population genetics:

### Mathematical Models Used:
- **Cosine Similarity**: For genetic compatibility calculations
- **Hardy-Weinberg Equilibrium**: Population genetics principles
- **Genetic Distance Metrics**: Measures genetic divergence between parents
- **Epistatic Interactions**: Trait interaction modeling
- **Normal Distribution**: For genetic drift simulation
- **Inverse Transform Sampling**: Advanced probability selection
- **Twin Probability Modeling**: Based on ethnicity, skin color, and genetic factors
- **Skin Color-Ethnicity Correlation**: Realistic trait correlation modeling

### Scientific Concepts:
- **Dominance Strength**: Variable dominance based on trait frequency
- **Genetic Drift**: Random fluctuations in allele frequencies
- **Multi-allelic Inheritance**: Complex trait combinations
- **Epistasis**: How one gene affects another's expression
- **Population Genetics**: Hardy-Weinberg equilibrium considerations
- **Twinning Genetics**: Realistic twin probability based on genetic factors
- **Trait Correlation**: Skin color and ethnicity correlation modeling

### Real-World Complexity:
While this simulator is for educational purposes, it incorporates many real genetic concepts:
- Multiple inheritance patterns
- Complex probability distributions
- Trait interaction effects
- Population-level genetic considerations

The mathematical models used are inspired by actual genetic research but simplified for computational efficiency.

## Future Enhancements

Potential improvements could include:

- More genetic traits (height, blood type, etc.)
- Additional mutations
- Family tree visualization
- Statistical analysis of inheritance patterns
- Export results to file
- More detailed genetic explanations

---

**Enjoy exploring the fascinating world of genetic inheritance! 🧬** 