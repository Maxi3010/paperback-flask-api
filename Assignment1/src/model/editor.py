from .subscriber import Subscriber
# editor is inherited from editor -same main attributes
class Editor(Subscriber):
    def __init__(self, name, address):
        super().__init__(name, address)



