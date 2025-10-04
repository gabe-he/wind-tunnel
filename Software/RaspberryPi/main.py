import view as View
import controller as Controller
import model as Model

Model.init()

Controller.run()

View.run()

# view.run() never return, so never add code after this.
