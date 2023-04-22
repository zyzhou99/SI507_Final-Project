# SI507_FinalProject

To test the program, run the file [ final_project.py ]
Required Python package: request, flask, tree

# API
API: API Already applied. But the cached image links are temporary, so if you try to run the code after a while, the image will not show up. <br/>

* EDAMAM Recipe API: https://api.edamam.com/api/recipes/v2 <br/>
* Nutritiononix Exercise API: https://trackapi.nutritionix.com/v2/natural/exercise <br/>

Format: JSON

# Data Structure
* There are two binary tree groups: one is based on cuisine type, and the other is based on the calories of the dish. 
* The Python file [tree.py] constructs the trees
* Based on the user input, the program will search through both tree groups, and if there is a match for both cuisine type and calorie requirement, then the dish will be recommended to the user. 
* Calorie Requirement calculation: 
  * Breakfast: (Intake goal + exercise calorie - already consumed calorie) / 3
  * Lunch: (Intake goal + exercise calorie - already consumed calorie) / 2
  * Dinner: Intake goal + exercise calorie - already consumed calorie
