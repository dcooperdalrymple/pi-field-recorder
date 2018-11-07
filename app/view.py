class AppView():
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        return False

    def destroy(self):
        return False

    def update(self):
        return False

    def update_view(self, state):
        return False

    def update_levels(self, levels, max_levels):
        return False
