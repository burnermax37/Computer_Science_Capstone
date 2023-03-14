# Computer Science Capstone
These are files from my computer science Capstone project. It originated as a PyCharm project.

## Code Files
The project uses QT and PyQT5 to generate the GUI. The following files each generate one window.
"LoginGUI.py" generates the initial login window.
"PricerGUI.py" generates the window uses to enter diamond characteristics and recieve a prediction for price.
"AdminGUI.py" generates the Admin window, used to assess the predictive model and update it if new data is added.
"HelpGUI.py" generates a window with additional details on how to use the Admin window.
"PopupGUI.py" generates a generic pop-up window, used in various areas such as error messages.

Other than these, there are two additional .py files:
DiamondModel.py describes the diamond model object, which contains the parameters and methods for the predictive
  model.
main.py contains the main function where the program starts.

## Data Files
Several CSV and text files support the program.
"diamonds.csv" contains the data used to train the predictive model.
"username_password.csv" contains username, password, and aadmin privileges for each user.


## Created Files
When running, the program will use some other files, but these are not included because the program can create them anew
if they are not already present.

