import puml_observer


class Printer(puml_observer.Observer):
    def on_class_found(self, class_name):
        print(f"Clase encontrada: {class_name}")

    def on_relation_found(self, class1, class2, relation):
        print(f"Relación encontrada: {relation} : {class1} --> {class2}")
