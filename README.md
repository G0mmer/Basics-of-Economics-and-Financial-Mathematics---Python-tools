# Financial Mathematics Tools 

Welcome to the open-source repository for Financial Mathematics and Actuarial Science tools! This project aims to provide interactive Python scripts and visualizations for students learning from textbooks like *"Theory of Interest"*.

## Current Tools

* **Chapter 17: Deferred Annuities** (`tools/chapter_17_deferred_annuities/`)
  * Python script to visualize Present Value (PV), Future Value (FV), and Current Value of Deferred Annuities.
  * Generates cash flow timelines, capital behavior graphs, and detailed console calculation reports.

## Repository Structure

We organize our tools by textbook chapters or broad financial topics:

```text
.
├── README.md
├── LICENSE
└── tools/
    ├── deferred_annuities/
    │   └── deferred_annuity_plotter.py
    ├── perpetuities/         # Waiting for contributions!
    └── amortization/         # Waiting for contributions!

```
How to Use:
* Clone this repository to your local machine:
  git clone [https://github.com/YOUR-USERNAME/financial-math-tools.git](https://github.com/YOUR-USERNAME/financial-math-tools.git)
*Install the required dependencies (we use standard math and plotting libraries):
  pip install matplotlib numpy
*Run the script! Navigate to the specific chapter folder and run the Python file. You can easily modify the parameters inside the script to solve your specific homework problems.
How to Contribute (Open Source)
This repository is open for all students taking Financial Mathematics. If you wrote a Python script that visualizes perpetuities, bond pricing, or amortization schedules, we want it here!

Steps to contribute:

Fork this repository.

Create a new folder for your topic in the tools/ directory (if it doesn't exist yet).

Add your Python script. Feel free to add a short README.md inside your specific folder explaining how your tool works.

Commit your changes and push them to your fork.

Open a Pull Request (PR) to our main repository.

We will review your code and merge it into the official collection!
