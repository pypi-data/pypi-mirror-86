from five4_tools.datos import Datos

class VariablesInfo(Datos):
    def __init__(self, dataset) -> None:
        self.dataset = dataset
        self.info = str()
        self.infoParseReturn = None
        self.elementosSplit = []
        self.listaNodos = []
        self.listaParseadaInfo = []
        self.resultadoTable = None
        self.contador = 0
        self.contadorx = 0
        self.columnas = ['idElemento', 'nombreColumna', 'cantidadRegistros', 'propiedadNulos', 'tipoDato']
        self.dataFrame = self.cargarDatos()
        self.infoParse = self.crearDf()
        self.dfInfo = self.parsearInfo()
        self.separador = None