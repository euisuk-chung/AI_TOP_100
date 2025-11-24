# AI_TOP_100 Preliminary Round: Battle Game Simulation

Source: https://brunch.co.kr/@andkakao/321

### **Simulation Power to Predict Without Battle**

Predict the outcome of a battle game through ML modeling.

* Separate data is required to solve this problem. The data can be found on the problem-solving website to be released later.

### **Problem Description**

Develop a machine learning model using AI that predicts victory or defeat based only on the initial placement information of units.

You have joined the balance patch team, the core of a new battle simulation game. Our team's goal is to run tens of thousands of virtual battles and analyze the results to achieve perfect game balance.

To maximize work efficiency, we want to develop a machine learning model that predicts the outcome based only on the initial placement of units instead of running all actual battles. The detailed stats of the units are veiled, and you must read the tide of the battlefield using only the unit type and 2D coordinates (x, y).

### **Battle Environment Description**

Unit: An entity deployed in battle. There are a total of 5 types of units, and the compatibility varies by unit type.

Team Center: The average of the coordinate values of the units of each team.

Battle Front: The line segment connecting the centers of the two teams is taken as the reference axis, and its perpendicular bisector is the boundary.

Front: A unit located in the half-plane on the side of the opponent's center relative to the boundary line.

Rear: The opposite half-plane.

Center of Coordinates: The space where units are placed has a range of [1, 20] for both x and y axes. Therefore, the reference center of the coordinate space is calculated as (10.5, 10.5).

### **Notes and References**

No separate validation dataset is provided. Properly split the training dataset to verify model performance.

Problem Related Information

Data Feature Engineering: Analyze training data to extract and process features that best represent the battle situation.

Example: Number of units per team, number of units of a specific type, average distance between units, concentration of attacks on specific units, etc.

Win/Loss Prediction Model Implementation: Develop a Classification model that predicts the winning team of the test data based on the extracted features.

---

### Q1. Who is the 1v1 Strongest?

### Choose the unit type that boasts the highest win rate in 1v1 battles.

> 1. eyanoo

> 2. bras

> 3. cbene

> 4. aleo

> 5. dgreg

---

### Q2. Placement Effect

### Which unit has the largest difference in win rate when placed in the front of the battle versus the rear?

![Screenshot](//img1.daumcdn.net/thumb/R1280x0.fpng/?fname=http://t1.daumcdn.net/brunch/service/user/41jj/image/Ps-0pNXyEZ-9eaINa1D_ftCxwj4.png)

> 1. dgreg

> 2. cbene

> 3. eyanoo

> 4. bras

> 5. aleo

---

### Q3. Formation Advantage Prediction

### Based on the entire training data, which formation shows a higher win rate: a formation spread wide horizontally (long in the x-axis direction) or a formation stretched long vertically (long in the y-axis direction)?

> 1. Formation long in x direction

> 2. Formation long in y direction

---

### Q4. Compatibility Relationship

### The compatibility relationship where dominance between units is determined is denoted as A > B (A beats B).

### For example, our familiar 'Rock Paper Scissors' has the compatibility of Scissors > Paper, Paper > Rock, Rock > Scissors. Choose the incorrect statement about the compatibility relationship among the following. *Multiple selections allowed

> □ eyanoo > dgreg

> □ dgreg > cbene

> □ bras > cbene

> □ dgreg > aleo

> □ cbene > aleo

> □ aleo > eyanoo

> □ bras > dgreg

> □ cbene > eyanoo

> □ eyanoo > bras

> □ aleo > bras

---

### Q5. Which of the following is NOT correct based on `train_battels.json`? *Multiple selections allowed

> 1. In 2v2 battles, the aleo+dgreg combination recorded 25 wins in 26 matches against the bras+eyanoo combination.

> 2. dgreg has a higher win rate when located in the front than in the rear.

> 3. In 4v4 battles, the win rate of the aleo+bras+dgreg+eyanoo combination is over 60%.

> 4. There is a tendency for the win rate to increase as the distance between units of the same team decreases.

> 5. The closer the team's center is to the center of coordinates (10.5, 10.5), the higher the win rate.

---

### Q6. Final Battle Result Prediction

### Predict the winner for all battles in the `test_battles.json` dataset and submit it in the format below.

- JSON Array

- The objects constituting the array are individual battle prediction objects

- id: Battle unique ID

- winner: The winning team of the battle ("blue" or "red")

> [  
>  {  
>  "id": "test_001",  
>  "winner": "red"  
>  },  
>  {  
>  "id": "test_002",  
>  "winner": "red"  
>  }  
>  ...  
> ]
