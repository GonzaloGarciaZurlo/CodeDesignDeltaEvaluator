import puml_observer


class Printer(puml_observer.Observer):
    def on_class_found(self, class_name: str) -> None:
        print(f"Class found: {class_name}")

    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        print(f"Relationship found: {relation} : {class1} --> {class2}")
