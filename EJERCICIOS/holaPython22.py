import pp, time, pylab

def divisoresPrimos(n):
    i = n/2
    primos = []
    while i>0:
        if not n%i:
            primos.append(i)
        i -= 1
    return primos

def perfecto(n):
    suma = 0
    for i in divisoresPrimos(n):
        suma += i
    return suma==n

def encuentraPerfectos(x,init=2):
    i = init #El 1 no es un numero perfecto
    perfectos = []
    while i<x:
        if perfecto(i) and i:
            perfectos.append(i)
        i += 2 #Todos los numeros perfectos son pares
    return perfectos

def test():
    perCount = int(raw_input('Limite para buscar perfectos: '))
    ppservers = ("*",)
    job_server = pp.Server(ppservers=ppservers)
    print 'Iniciando computacion paralela con', job_server.get_ncpus(), 'nucleos'
    NUM_TASKS = (4,8,16,32,64,128,256,512,1024,2048,4096)
    #NUM_TASKS = (1,2,4,8,16,32,64,128)
    job = []
    times = []

    for TASKS in NUM_TASKS:
        print '\n'
        print str(TASKS),'subprocesos...'
        print str(job_server.get_active_nodes())

        cnt = 0
        startTime = time.time()

        #ranges = []

        for tasks in range(TASKS):
            job.append(job_server.submit(encuentraPerfectos, (perCount/TASKS+cnt,cnt), (perfecto,divisoresPrimos), ('math',)))
            #ranges.append((cnt,perCount/TASKS+cnt))
            cnt += perCount/TASKS
        job_server.wait()
        now = time.time()
        #print ranges
        
        perfectos = []

        for item in job:
            if item():
                for i in item():
                    if i not in perfectos:
                        perfectos.append(i)
        tm = now-startTime
        times.append(tm)
        print perfectos
        print 'Tiempo de computacion: ',str(tm),'segundos'
    fig = pylab.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(NUM_TASKS, times, color='blue', lw=2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    #pylab.plot(NUM_TASKS, times)
    print '\n\n'
    job_server.print_stats()
    pylab.show()
    return times

def benchmark():
    data = test()
    mean = 0
    for i in data:
        mean += i
    mean = float(mean)/len(data)

    print '\n\nMedia: ' +str(mean)
    print 'Minimo: '+str(min(data))
    print 'Maximo: '+str(max(data))

