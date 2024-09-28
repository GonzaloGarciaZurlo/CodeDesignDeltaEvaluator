import printer
import regex_uml
import pyreverse_util


class Main:
    @staticmethod
    def ejecutar():
        observer = printer.Printer()
        parser = regex_uml.Regex(observer)

        # Parsear un archivo de ejemplo
        archivo_plantuml = pyreverse_util.generate_plantuml_python(
            '../Samples/SOLID+LoD/I/ISP_P.py')
        parser.parse(archivo_plantuml)
        pyreverse_util.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
