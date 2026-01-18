import allure


def add_metadata(component, owner, priority):
    allure.dynamic.tag(component)
    allure.dynamic.label("owner", owner)
    allure.dynamic.label("priority", priority)
