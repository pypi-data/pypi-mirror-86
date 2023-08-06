import pandas as pd
import io
from Color_Console import *
from five4_tools.variables import VariablesInfo

class Operaciones(VariablesInfo):

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
                if self.resultadoTable.empty is not True:
                    ctext( "Las siguientes columnas tienen datos nulos" , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
                    ctext( self.resultadoTable , text = "yellow" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
            except Exception as ex:
                print(ex.args)
        else:
            print("Ocurrió un error al cargar el orígen de datos.")


    def resumenShape(self):
        print(end='\n\n')
        ctext( "El DataFrame tiene el siguiente Shape" , text = "blue" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
        ctext( "Registros: {}".format(self.shapeDf[0]) , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
        ctext( "Columnas: {}".format(self.shapeDf[1]) , text = "red" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
    

    def obtenerPK(self):
        dfCargado = self.dataFrame
        columnasDfTemp = dfCargado.columns.tolist()
        columnasDf = []
        for columnaDf in columnasDfTemp:
            columnaFixed = str(columnaDf).replace(" ","").replace(":", "")
            columnasDf.append(columnaFixed)
        dfCargado.columns = columnasDf

        for columnaIter in columnasDf:
            serieCol = self.dataFrame[columnaIter]
            cantidadUnicos = len(serieCol.unique())
            if self.shapeDf[0] == cantidadUnicos:
                self.candidatoPK[str(columnaIter)] = cantidadUnicos
        print(end='\n\n')
        if len(self.candidatoPK) != 0:
            ctext( "Las siguientes columnas tienen valores únicos y son candidatos a ser PK:" , text = "blue" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
            dfCandidatos = pd.DataFrame.from_dict(self.candidatoPK, 'Index')
            ctext( "Columnas: {}".format(dfCandidatos) , text = "green" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
        else:
            ctext( "No se logró identificar columnas con valores únicos como PK" , text = "blue" , bg = "black" , delay = 0 , repeat = 1 , dict = {} )
