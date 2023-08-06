from five4_tools.buscarSeparador import _buscarSeparador
import pandas as pd
import io


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
                self.infoAParsear = self.infoAParsear.split("\n")[3:]
                for elementoNodo1 in self.infoAParsear:
                    if elementoNodo1[:6] != 'dtypes':
                        elementoNodo1 = elementoNodo1.replace("Unnamed: ",'')
                        self.listaParseadaInfo.append(elementoNodo1)
                    else:
                        break
                
                for elementoNodo in self.listaParseadaInfo:
                    self.elementosSplit = elementoNodo.split()
                    self.listaNodos.append(self.elementosSplit)
                
                self.columnas = ['nombreColumna', 'cantidadRegistros', 'propiedadNulos', 'tipoDato']
                self.dfInfo = pd.DataFrame(self.listaNodos, columns=self.columnas)
                # self.dfInfo.set_index('idElemento')
            except Exception as ex:
                print(ex.args)
            return self.dfInfo
        else:
            return pd.DataFrame([])