import pandas as pd
import io
from Color_Console import *
from five4_tools.buscarSeparador import _buscarSeparador

class Datos():
    """[summary]
    Clase que Inicializa las funciones
    """
    
    def cargarDatos(self):
        print("Cargando Datos...")
        print("Buscando separador de columnas...")
        self.separador = _buscarSeparador(self.dataset)
        if self.separador is False:
            return False
        else:
            print("Separador encontrado: '{}'".format(str(self.separador)))
            self.dataFrame = pd.read_csv(self.dataset, sep=str(self.separador))
            return self.dataFrame
        

    def crearDf(self):
        if self.dataFrame is not False:
            print("Creando DataFrame para análisis")
            try:
                self.buf = io.StringIO()
                # self.df = pd.read_csv(self.dataset)
                self.info = self.dataFrame.info(buf=self.buf)
                self.infoParse = self.buf.getvalue()
            except Exception as ex:
                print(ex.args)
            return self.infoParse
        else:
            return False
    
    
    def parsearInfo(self):
        if self.infoParse is not False:
            print("Parser de Pandas Info")
            try:
                self.listaNodos = []
                self.infoAParsear = self.infoParse
                self.infoAParsear = self.infoAParsear.split("\n")[5:]
                for elementoNodo1 in self.infoAParsear:
                    if elementoNodo1[:6] != 'dtypes':
                        elementoNodo1 = elementoNodo1.replace("Unnamed: ",'')
                        self.listaParseadaInfo.append(elementoNodo1)
                    else:
                        break
                
                for elementoNodo in self.listaParseadaInfo:
                    self.elementosSplit = elementoNodo.split()
                    self.listaNodos.append(self.elementosSplit)
                
                self.columnas = ['idElemento', 'nombreColumna', 'cantidadRegistros', 'propiedadNulos', 'tipoDato']
                self.dfInfo = pd.DataFrame(self.listaNodos, columns=self.columnas)
                self.dfInfo.set_index('idElemento')
            except Exception as ex:
                print(ex.args)
            return self.dfInfo
        else:
            return False
            

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



class Operaciones(VariablesInfo):
    # def __init__(self, rootDf, df) -> str:
    #     self.dataset = self.dfInfo
    #     self.listaDfs = self.infoParse
    #     self.contador = 0
    #     self.contadorx = 0
        
    def nullDataResume(self):
        """[summary]
        El dataset instanciado en la clase Datos(dataset)
        es analizado y retorna distintos metodos de análisis en función
        de los parámetros

        Returns:
            [list]: [tabla con los resultados del análisis]
        """
        if self.dfInfo is not False:
            print("Armando informe...", end='\n\n')
            self.infoParseReturn = self.dfInfo
            dictColumnas = dict()
            self.dfInfo = self.dataFrame

            try:
                for columna in self.dfInfo.columns.tolist():
                    if int(self.dfInfo[columna].isnull().sum()) is not 0:
                        dictColumnas[columna]=self.dfInfo[columna].isnull().sum()
                sumaNull = sum(dictColumnas.values())
                self.contador+=1
                self.contadorx+=1
                self.resultado = 'El df tiene '+ str(len(self.dfInfo.columns.tolist())) + ' columnas de las cuales las siguientes tienen valores nulos:'+ str(dictColumnas)
                        # f"{colored.}El df tiene {len(self.listaDfs.columns.tolist())} columnas de las cuales las siguientes tienen valores nulos: {str(dictColumnas)}")
                self.resultadoTable = pd.DataFrame.from_dict(dictColumnas, 'Index', columns=['CantidadNulos'])

                color(text = "Green" , bg = "black" , delay = 0.67 ,repeat = -1 , dict = {})
                ctext( self.resultado , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
                print(end='\n\n')
                # ctext( self.columnasDF , text = "blue" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
                ctext( self.infoParseReturn , text = "magenta" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
                print(end='\n\n')
                ctext( "Las siguientes columnas tienen datos nulos" , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
                ctext( self.resultadoTable , text = "yellow" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
            except Exception as ex:
                print(ex.args)
        else:
            print("Ocurrió un error al cargar el orígen de datos.")

    def resumenShape(self):
        print(end='\n\n')
        ctext( "El DataFrame tiene el siguiente Shape" , text = "blue" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
        self.shapeDf = self.dataFrame.shape
        ctext( "Registros: {}".format(self.shapeDf[0]) , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
        ctext( "Columnas: {}".format(self.shapeDf[1]) , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )

