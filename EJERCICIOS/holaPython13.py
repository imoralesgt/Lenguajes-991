#Intro a OOP. Estudiantes con cursos asignados.

class estudiante(object): #Clase estudiante
    def __init__(self, carnet, nombre, cursos = []): #Constructor
        self.carnet = carnet #Ingresar los parametros de inicializacion
        self.nombre = nombre #para ser accedidos desde todos los metodos de la clase
        self.cursos = cursos

    def getCarnet(self): #Devuelve el carnet del estudiante
        return self.carnet

    def getNombre(self):
        return self.nombre

    def getCursos(self): #Devuelve un listado de cursos con su ID y nota
        a = []
        for i in self.cursos:
            a.append(i.getCodigo()+': '+i.getNombre()+'. Nota '+str(i.getNota()))
        return a

    def countCursos(self): #Devuelve la cantidad de cursos asignados
        return len(self.getCursos())

    def addCurso(self, curso): #Agrega un curso al estudiante
        self.cursos.append(curso)

    def __str__(self):  #Print class
        return str('Yo soy ' + self.getNombre())



class curso(object): #Clase curso
    def __init__(self, codigo, nombre, nota):
        self.codigo = codigo
        self.nombre = nombre
        self.nota   = nota

    def getCodigo(self): #Devuelve el codigo
        return str(self.codigo)

    def getNombre(self):
        return self.nombre

    def getNota(self):
        return self.nota

    def setNota(self, val):
        self.nota = val



#Creacion de instancias
Juan = estudiante(201414567, 'Juan Perez',
                  [curso('0769','Progra',61),curso('0018','Filo',62)])

Carlos = estudiante(200815521, 'Carlos Gonzalez',
                  [curso('0018','Filo',61),curso('0769','Progra',60)])

Rodrigo = estudiante(200617283, 'Rodrigo Lopez',
                  [curso('0018','Filo',60),curso('0152','Fisica 2',95)])

FB = curso('0147','Fisica Basica',95)
F1 = curso('0150','Fisica 1',84)

Rodrigo.addCurso(FB) #Agregar Fisica Basica a Rodrigo
Juan.addCurso(F1) #Agregar Fisica 1 a Juan
