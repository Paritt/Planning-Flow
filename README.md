# 🍃 Planning-Flow 

**Planning-Flow** is a flowchart-like GUI application designed for running in RayStation radiotherapy treatment planning system. It enables users to design, save, and execute automated planning workflows through an intuitive graphical interface, eliminating the need for manual scripting.

## 🌏 Overview

Planning-Flow provides a visual workflow designer that allows you to automate various aspects of treatment planning, including:
- Configure beam and plan settings for VMAT and IMPT techniques
- Create new helping ROIs through boolean operations
- Set up initial optimization functions with various dose objectives and constraints (including robust optimization and beam restrictions)
- Define conditional logic based on dose-volume metrics
- Automatically adjust optimization functions or add new ones based on conditions logic
- Automatically create ROIs when certain conditions are met
- Execute multi-round optimization with customizable stopping criteria
- Save workflow configurations as JSON files for reuse
- Selective execution of workflow steps
- Add clinical goals for plan evaluation
- Robust optimization settings for IMPT plans
- Final dose calculation with chosen algorithms
- Comprehensive logging of execution progress and results
- Load previously saved workflows for modification or execution
- Choose which Plan flow steps to execute
  
The application is built with Python and Tkinter, and interfaces directly with the RayStation API.

## 🚲 Installation

### Prerequisites
- **RayStation** treatment planning system (v2025 or compatible)
- **Python** (version used by RayStation, typically Python 3.x)
- **tkinter** (usually included with Python)

### Setup
1. Clone or download this repository to a location accessible from RayStation
2. Ensure the folder structure is maintained:
   ```
   Planning-Flow/
   ├── main.py
   ├── src/
   │   ├── PlanFlowDesigner.py
   │   ├── StartFlow.py
   │   ├── flow/
   │   └── window/
   └── README.md
   ```

## ⭐ Usage

### Starting the Application

1. **Launch from RayStation**:
   - Open RayStation
   - Execute `main.py` through RayStation's scripting interface

2. **Main Window**:
   The application opens with treatment settings:
   - **Machine**: Select treatment machine (Agility, P1, etc.)
   - **Plan Name**: Enter name for the treatment plan
   - **Load Flow**: Load a previously saved workflow
   - **New Flow**: Start designing a new workflow
   - **Edit Flow**: Modify an existing workflow
   - **Select steps**: Choose which steps to execute
   - **Start**: Begin execution of the automate planning workflow

### Creating a Plan flow

1. **Click "New Flow"** to open the PlanFlow designer

2. **Configure Flow Name**:
   - Enter a name for your flow

3. **Add Planning Steps** (in order):
   
   **Step 1: Match ROI**
   - Add all ROI name and it's possible name that you will use in this flow

   **Step 2: Technique Configuration**
   - Choose between VMAT or IMPT
   - Click 'Beam' to Add beam and it's settings (angles, energies, etc.)
   - Click 'Isocenter' to set isocenter location
   - Click 'Prescription' to set dose prescription
   
   **Step 3: Plan Configuration (Optional)**
   - Set clinical goal (This will load template from your RayStation database) and match the ROIs
   - Set Robustness for robust function (Do not set if you don't have robust function)

   **Step 4: Automate ROI**
   - Create helping ROIs you want to use in initial optimization function or match in clinical goal using boolean operations (e.g., ring, OAR-PTV, etc.)

   **Step 5: Initial Function**
   - Add dose initial objectives function and constraints you will use in 1st optimization round
   - Set function types, ROIs, weights
   - Configure robust settings if needed
   - Configure beam restrictions if applicable
   - Tags auto-generate if left empty: `{roi}_{type}_{index}`

   **Step 6: Optimization Settings and Final Calculation setting**
   - Set maximum iterations per round
   - Set optimization tolerance
   - Set algorithm for final dose calculation

   **Step 7: Check Conditions**
   - Define evaluation conditions based on DVH metrics
   - Set active rounds for each condition
   - Condition names auto-generate if left empty: `c_{roi}_{type}_r{round}_{index}`

   **Step 8: Conditional ROI Creation**
   - Create ROIs when specific conditions (in step 7) are met

   **Step 9: Function Adjustment**
   - Modify initial optimization functions if specific conditions (in step 7) are met
   - Add new optimization functions if specific conditions (in step 7) are met (Tags auto-generate if left empty: `{roi}_{type}_{index}`)

   **Step 10: End Planning Flow**
   - Define how many optimization rounds to perform before end the Planning Flow
  

4. **Save or Use Workflow**:
   - **Save Flow**: Saves the workflow as a JSON file for future use
   - **Use Without Saving**: Proceeds to execution selection without saving

### Executing a Workflow

1. After designing (or loading) a workflow

2. **Select Steps to Execute**:
   - Check/uncheck steps you want to run
   - Useful for running only portions of a workflow

3. **Click "Start"** to begin Automated Planning Flow execution

4. **Monitor Progress**:
   - The console window shows real-time progress
   - Step timings are displayed
   - Any errors or warnings appear in the console
   - Execution log can be saved to a text file at the end


### Loading Existing Workflows

1. Click **"Load Flow"** in the main window
2. Select a previously saved JSON workflow file
3. The workflow designer opens with all settings pre-loaded
4. You can modify settings by click 'Edit Flow' or directly proceed to execution

## 🗺️ Plan Flow File Format

Plan flow are saved as JSON files containing:
- Plan configuration (name, technique)
- All step configurations (beams, ROIs, functions, conditions, etc.)

Example structure:
```json
{
    "flow_name": "Esophagus_4140",
    "created_by": "Paritt",
    "created_date": "2026-01-26 13:57:52",
    "version": "1.0",
    "technique": "VMAT",
    "vmat_beam": [
        {
            "beam_name": "1CW181-180",
            "energy": "6",
            "gantry_start": "181.0",
            "gantry_stop": "180.0",
            "rotation": "CW",
            "collimator": "355.0",
            "couch": "0.0"
        },
        {
            "beam_name": "2CCW180-181",
            "energy": "6",
            "gantry_start": "180.0",
            "gantry_stop": "181.0",
            "rotation": "CCW",
            "collimator": "5.0",
            "couch": "0.0"
        }
    ],
    ...
}
```

## 💡 Tips and Best Practices

1. **Naming Conventions**:
   - Use descriptive workflow names
   - Let auto-naming handle function tags and condition names (Or name it yourself if you prefer just make sure they are unique)
   - Keep names under 50 characters

2. **ROI Matching**:
   - Match all required ROIs before every step (but if you forget to match some you can always add them later)

3. **Optimization Strategy**:
   - Start with broader objectives in initial functions
   - Use conditions to refine functions in later rounds
   - Example: Start with PTV coverage, then add OAR sparing based on conditions

4. **Conditional Logic**:
   - Use conditions to create adaptive Plan flows
   - Test this with some cases and make it more complex as you see cases that it not working as expected
   - You can use clinical goals as a guide for setting conditions

## 🛠️ Troubleshooting

**Problem**: "RayStation API not found" error
- **Solution**: Ensure you're running the script from within RayStation

**Problem**: Plan name already exists
- **Solution**: Choose a different plan name or delete the existing plan

**Problem**: ROI not found during execution
- **Solution**: Verify ROI matching is configured correctly

**Problem**: Optimization not converging
- **Solution**: Check function weights, increase iterations, or adjust objectives
  
**If you find any bug or have suggestions, please don't hesitate to contact me.**



## 😊 Developer Notes 
Hi there! my name is Paritt and I am the original developer of Planning-Flow. 
Currently, I am a PhD student focusing on integrating AI and automation into radiotherapy treatment planning. 
This project is part of my ongoing efforts to streamline and enhance the planning process.

The goal of Planning-Flow is to provide a flexible and user-friendly tool that empowers planner to automate complex planning workflows without deep programming knowledge. And also to capture all the planning tip and trick to further use for creating AI agent to assist in treatment planning. Therefore, any feedback, suggestions, or contributions are highly welcome!

**My Contact Info**:
- Email: p.wongtrakool@umcg.nl
  
## 📘 Citation
If you find Planning-Flow useful in your research or clinical work, please consider citing it as follows:
```
@software{Wongtrakool2026,
  author = {Wongtrakool, Paritt},
  title = {Planning-Flow},
  url = {https://github.com/Paritt/Planning-Flow},
  year = {2026}
}
```

## 📃 My TODO List
- Automate Robust Evaluation
- Function Value as condition
- AND OR condition
- Wait for User input (Draw ROI, Manual add function)
- Avoid beam (VMAT)
- Fix Jaw (VMAT)
- Auto save