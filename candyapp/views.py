from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime, date
# Create your views here.

def baseprod(request, lg, id):
    pd = producto.objects.get(id_pd=id)
    bases = basepd.objects.all()
    materiap = materia_p.objects.all()
    filtro = []
    for bs in bases:
        if bs.id_pd_id == id:
            for ms in materiap:
                if ms.id_mp == bs.id_mp_id:
                    ms.cantidad = bs.cantidad
                    ms.descripcion = bs.id_bp
                    filtro.append(ms)
    return render(request, "basepd/index.html", {'bases': filtro, 'nombre': pd.nombre, 'id': id, 'lg': lg})

def addbase(request, lg, id):
    pd = producto.objects.get(id_pd=id)
    lugares = lugar.objects.all()
    materiap = materia_p.objects.all()
    formulario = infBaseForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        mats = formulario.data['materias']
        cantidad = formulario.data['cantidad']
        for ms in materiap:
            if (ms.nombre).upper() == (mats).upper():
                for lug in lugares:
                    if lug.id_lg != 1:    
                        pd2 = producto.objects.get(nombre=pd.nombre, id_lg=lug.id_lg)
                        if ms.id_lg_id == lug.id_lg:
                            data = {'id_pd': pd2.id_pd, 'id_mp': ms.id_mp, 'cantidad': cantidad}
                            formulario = basepdForm(data)
                            if formulario.is_valid():
                                formulario.save()
        return redirect('/'+str(lg)+'/'+'base'+str(id))
    return render(request, "basepd/crear.html", {'formulario': formulario})

def delbase(request, id, lg, id2):
    bases = basepd.objects.get(id_bp=id)
    bases.delete()
    return redirect('/'+str(lg)+'/'+'base'+str(id2))

def isactive(): 
    bases = basepd.objects.all()
    mezclas = mezcla.objects.all()
    estado = "Activo"
    for i in mezclas:
        materiap = materia_p.objects.get(id_mp=i.id_mp_id)
        materias = materia_s.objects.get(id_ms=i.id_ms_id)
        if i.cantidad > materiap.cantidad:
            estado = "Inactivo"
        materiap.estado = estado
        materias.estado = estado
        materiap.save()
        materias.save()
        estado = "Activo"
    for j in bases:
        materiap = materia_p.objects.get(id_mp=j.id_mp_id)
        productos = producto.objects.get(id_pd=j.id_pd_id)
        if j.cantidad > materiap.cantidad:
            estado = "Inactivo"
        materiap.estado = estado
        productos.estado = estado
        materiap.save()
        productos.save()
        estado = "Activo"

def add_finz(request, lg):
    id = gen_add(lg)
    finanza.objects.get_or_create(fecha=datetime.now().strftime("%x"), id_lg=lg, id_hs=id)
    finanzas = finanza.objects.get(fecha=datetime.now().strftime("%x"), id_lg=lg) 
    formulario = addfzForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        data = {'servicio': "servicio: "+str(formulario.data['servicio']), 'costo': 0-int(formulario.data['costo']), 'hora': datetime.now().strftime("%X"), 'finz':finanzas.id_fz,'id_sv': -2,'id_lg': lg}
        formulario = fzForm(data)
        if formulario.is_valid():
            formulario.save()
        return redirect('/'+str(lg)+'/'+'finanzas')
    return render(request, "finanza/addfz.html", {'formulario': formulario})

def verfinanza(request, lg):
    if lg == 1:
        return render(request, "finanza/bodvista.html")
    else:
        return render(request, "finanza/vista.html")

def gen_add(lg):
    historial_fz.objects.get_or_create(fecha=datetime.now().strftime("%m")+"/"+datetime.now().strftime("%y"), id_lg=lg)
    historial = historial_fz.objects.get(fecha=datetime.now().strftime("%m")+"/"+datetime.now().strftime("%y"), id_lg=lg)
    return historial.id_hf

def gen_fz(request, lg):
    veract(lg)
    historial = historial_fz.objects.all()
    info = finanza.objects.all()
    costo = 0.0
    filtro = []
    for hs in historial:
        if hs.id_lg == lg:
            for ifo in info:
                if ifo.id_hs == hs.id_hf:
                    if ifo.costot != None:
                        costo += int(ifo.costot)
            hs.costot = costo
            filtro.append(hs)
            costo = 0
    if lg == 1:
        return render(request, "finanza/bodgen.html", {'historiales': filtro, 'lugar': lg })
    else:
        return render(request, "finanza/gen.html", {'historiales': filtro, 'lugar': lg })

def info_fz(request, id, lg):
    histo = compt.objects.all()
    info = []
    for hs in histo:
        if hs.id_lg == lg:
            if hs.finz == id:
                info.append(hs)
    if lg == 1:
        return render(request, "finanza/bodinfo.html", {'infos': info})
    else:
        return render(request, "finanza/masinfo.html", {'infos': info})


def veract(lg):
    historial = finanza.objects.all()
    info = compt.objects.all()
    costo = 0
    for hs in historial:
        if hs.id_lg == lg:
            for ifo in info:
                if ifo.finz == hs.id_fz:
                    costo += ifo.costo
            hs.costot = costo
            hs.save()
            costo = 0


def hist_fz(request, lg, id):
    historial = finanza.objects.all()
    info = compt.objects.all()
    costo = 0
    filtro = []
    for hs in historial:
        if hs.id_lg == lg and hs.id_hs == id:
            for ifo in info:
                if ifo.finz == hs.id_fz:
                    costo += ifo.costo
            hs.costot = costo
            hs.save()
            filtro.append(hs)
            costo = 0
    if lg == 1:
        return render(request, "finanza/bodindex.html", {'historiales': filtro, 'lugar': lg })
    else:
        return render(request, "finanza/index.html", {'historiales': filtro, 'lugar': lg })
    
def finanzas(serv ,servicio, costo, link, lg):
    id = gen_add(lg)
    finanza.objects.get_or_create(fecha=datetime.now().strftime("%x"), id_lg=lg, id_hs=id)
    finanzas = finanza.objects.get(fecha=datetime.now().strftime("%x"), id_lg=lg) 
    data = {'servicio': servicio, 'costo':costo, 'hora': datetime.now().strftime("%X"), 'finz':finanzas.id_fz,'id_sv': serv,'id_lg': lg}
    formulario = fzForm(data)
    formulario.save()
    return redirect('/' + str(lg) + link)

def signup(request):
    formulario = snForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        if formulario.data['name'] == "Admin" and formulario.data['password'] == "12345":
            return redirect('lugar')
        else:
            return redirect('signup')
    return render(request, "signup/index.html", {'formulario': formulario}) 

def lugares(request):
    lugares = lugar.objects.all()
    return render(request, "lugar/index.html", {'lugares': lugares})

def agregar_lg(request):
    entro = "no"
    lugares = lugar.objects.all()
    formulario = lgForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        for lg in lugares:
            if lg.nombre == formulario.data["nombre"]:
                entro = "si"
                break
        if entro == "no":
            formulario.save()
            lug = lugar.objects.get(nombre=formulario.data["nombre"])
            copymp(lug.id_lg)
            copyz(lug.id_lg)
            copyp(lug.id_lg)
            return redirect('lugar')
    return render(request, "lugar/crear.html", {'formulario': formulario})    

def eliminar_lg(request, id):
    lugares = lugar.objects.get(id_lg=id)
    lugares.delete()
    return redirect('lugar')

def log(request, id):
    log = id
    return redirect("/"+ str(log)+ "/" + 'home')

def home(request, lg):
    lugares = lugar.objects.get(id_lg=lg)
    productos = producto.objects.all()
    lista = []
    for pd in productos:
        if pd.id_lg_id == lg:
            lista.append(pd)
    if lg != 1:
        return render(request, "pages/inicio.html", {'productos': lista, 'lugar': lg, 'nombre': lugares.nombre})
    else:
        return render(request, "pages/inbodega.html")

def productos(request, lg):
    productos = producto.objects.all()
    lista = []
    for pd in productos:
        if pd.id_lg_id == lg:
            lista.append(pd)
    return render(request, "Productos/pindex.html", {'productos': lista, 'lugar': lg})

def copybs(bas, pos, lg):
    productos = producto.objects.all()
    materiap = materia_p.objects.all()
    for pd in productos:
        if pd.id_lg_id == lg:
            for mp in materiap:
                if mp.id_lg_id == lg:
                    for bu in bas:
                        if mp.nombre == bu[1] and pd.nombre == bu[0]:
                            data = {'id_pd': pd.id_pd, 'id_mp': mp.id_mp, 'cantidad': bu[1]}
                            formulario = basepdForm(data)
                            if formulario.is_valid():
                                formulario.save() 
            for pus in pos:
                if pd.nombre == pus[0]:
                    data = {'nombre': pus[1].nombre, 'precio': pus[1].precio, 'id_pd': pd.id_pd}
                    formulario = psForm(data)
                    if formulario.is_valid():
                        formulario.save() 

def copyp(lg):
    productos = producto.objects.all()
    bases = basepd.objects.all()
    posiciones = posicion.objects.all()
    pos = []
    bas = []
    nombres = []
    estan = []
    for pd in productos:
        if pd.nombre not in nombres:
            nombres.append(pd.nombre)
            estan.append(pd)
            for bs in bases:
                if bs.id_pd_id == pd.id_pd:
                    bas.append([pd.nombre, materia_p.objects.get(id_mp=bs.id_mp_id).nombre, bs.cantidad])
            for ps in posiciones:
                if ps.id_pd_id == pd.id_pd:
                    pos.append([pd.nombre, ps])
        else:
            for bs in bases:
                if bs.id_pd_id == pd.id_pd:
                    for bus in bas:
                        if materia_p.objects.get(id_mp=bs.id_mp_id).nombre == bus[1]:
                            rep = "si"
                            break
                    if rep == "no":
                        bas.append([pd.nombre, materia_p.objects.get(id_mp=bs.id_mp_id).nombre, bs.cantidad])
                    rep = "no"
            for ps in posiciones:
                if ps.id_pd_id == pd.id_pd:
                    for pus in pos:
                        if ps.nombre == pus[1].nombre:
                            rep = "si"
                            break
                    if rep == "no":
                        pos.append([pd.nombre, ps])
                    rep = "no"

    for et in estan:
        data = {'nombre': et.nombre, 'descripcion': et.descripcion, 'precio': float(et.precio), 'estado': "Activo", 'id_lg': lg}
        formulario = productoForm(data)
        if formulario.is_valid():
            formulario.save()
    copybs(bas, pos, lg)

def agregar_pd(request, lg):
    lugares = lugar.objects.all()
    formulario = infPdForm(request.POST or None, request.FILES or None)
    descripcion = "None"
    if formulario.is_valid():
        if formulario.data['descripcion'] != "":
            descripcion = formulario.data['descripcion']
        precio = formulario.data['precio']
        nombre = formulario.data['nombre']
        for lug in lugares:
            if lug.id_lg != 1:
                data = {'nombre':nombre, 'descripcion': descripcion, 'precio': precio, 'estado': "Activo", 'id_lg': lug.id_lg}
                formulario = productoForm(data)
                formulario.save()
        return redirect('/'+str(lg)+'/'+'productos')
    return render(request, "Productos/crear.html", {'formulario': formulario})

def editar_pd(request, id, lg):
    productos = producto.objects.get(id_pd=id)
    formulario = productoForm(request.POST or None, request.FILES or None, instance=productos)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('/'+str(lg)+'/'+'productos')
    return render(request, "Productos/editar.html", {'formulario': formulario})

def eliminar_pd(request, id, lg):
    productos = producto.objects.get(id_pd=id)
    productos.delete()
    return redirect('/'+str(lg)+'/'+'productos')

#------------------------------materia_p-------------------------------------------------

def materiap(request, lg):
    isactive()
    materiap = materia_p.objects.all()
    lista = []
    for mp in materiap:
        if mp.id_lg_id == lg:
            lista.append(mp)
    if lg == 1:    
        return render(request, "materiap/bodega.html", {'materiap': lista, 'lugar': lg})
    else:
        return render(request, "materiap/index.html", {'materiap': lista, 'lugar': lg})

def copymp(lg):
    materiap = materia_p.objects.all()
    fecha = datetime.now()
    for mp in materiap:
        if mp.id_lg_id == 1:
            data = {'nombre': mp.nombre, 'cantidad': 0, 'unidad': mp.unidad, 'costo': 0, 'costo_u': mp.costo_u, 'proveedor': mp.proveedor, 'contacto': mp.contacto, 'tiempo': mp.tiempo, 'mincant': mp.mincant, 'descripcion': mp.descripcion, 'estado': 'Activo','fecha': str(fecha.strftime("%B")) + "/" + str(fecha.strftime("%Y")) , 'id_lg': lg}
            formulario = mpForm(data)
            if formulario.is_valid():
                formulario.save()

def avastecer(request, id, lg):
    materia = materia_p.objects.get(id_mp=id)
    formulario = avsForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        finanzas(materia.id_mp ,"Avastecido "+ str(formulario.data['cantidad'])+": " + materia.nombre , 0-(float(formulario.data['cantidad']) * materia.costo_u), "/materiap", lg)
        materia.cantidad += int(formulario.data['cantidad'] )
        materia.costo += int(formulario.data['cantidad'] ) * materia.costo_u
        materia.save()
        return redirect('/' + str(lg) + '/materiap')
    return render(request, "materiap/avastecer.html", {'formulario': formulario, 'nombre':materia.nombre})


def agregar_mp(request, lg):
    lugares = lugar.objects.all()
    formulario = dtMpForm(request.POST or None, request.FILES or None)
    fecha = datetime.now()
    contacto = "None"
    tiempo = 0
    mincant = 0
    descripcion = "None"
    if formulario.is_valid():
        if (formulario.data['costo'] == '' and formulario.data['costou'] == '') or (formulario.data['costo'] != '' and formulario.data['costou'] != '') :
            costot = "nada"
            costou = "nada"
        elif formulario.data['costo'] == '':
            costot = float(formulario.data['costou']) * float(formulario.data['cantidad'])
            costou = float(formulario.data['costou'])
        elif formulario.data['costou'] == '':
            costou = float("{0:.2f}".format(int(formulario.data['costo'])/int(formulario.data['cantidad'])))
            costot = float(formulario.data['costo'])

        if formulario.data['contacto'] != '':
            contacto = contacto = formulario.data['contacto']

        if formulario.data['tiempo'] != '':
            tiempo = formulario.data['tiempo']

        if formulario.data['mincant'] != '':    
            mincant = formulario.data['mincant']

        if formulario.data['descripcion'] != '':
            descripcion = formulario.data['descripcion']
        
        nombre = formulario.data['nombre']
        cantidad = int(formulario.data['cantidad'])
        unidad = formulario.data['unidad']
        proveedor = formulario.data['proveedor']

        for lu in lugares:
            if lu.id_lg == lg:
                data = {'nombre': nombre, 'cantidad': cantidad, 'unidad': unidad, 'costo': costot, 'costo_u': costou, 'proveedor': proveedor, 'contacto': contacto, 'tiempo': tiempo, 'mincant': int(mincant), 'descripcion': descripcion, 'estado': 'Activo','fecha': str(fecha.strftime("%B")) + "/" + str(fecha.strftime("%Y")) , 'id_lg': lu.id_lg}
            else:
                data = {'nombre': nombre, 'cantidad': 0, 'unidad': unidad, 'costo': 0, 'costo_u': costou, 'proveedor': proveedor, 'contacto': contacto, 'tiempo': tiempo, 'mincant': int(mincant), 'descripcion': descripcion, 'estado': 'Activo','fecha': str(fecha.strftime("%B")) + "/" + str(fecha.strftime("%Y")) , 'id_lg': lu.id_lg}
            formulario = mpForm(data)
            if formulario.is_valid():
                formulario.save()
                materiap = materia_p.objects.get(nombre=nombre, id_lg=lu.id_lg)
                finanzas(materiap.id_mp ,"Materia prima: "+ nombre , 0-costot, "/materiap", lu.id_lg)
        return redirect('/' + str(lg) + '/materiap')
    return render(request, "materiap/crear.html", {'formulario': formulario})

def editar_mp(request, id, lg):
    materiap = materia_p.objects.get(id_mp=id)
    mezclas = mezcla.objects.all()
    formulario = edmpForm(request.POST or None, request.FILES or None, instance=materiap)
    if formulario.is_valid() and request.POST:
        formulario.save()
        for mz in mezclas:
            if mz.id_mp_id == id:
                if mz.cantidad > materiap.cantidad:
                    materiap.estado = "Inactivo"
                else:
                    materiap.estado = "Activo"
                materiap.save()
        return redirect('/' + str(lg) + '/materiap')
    return render(request, "materiap/editar.html", {'formulario': formulario})

def eliminar_mp(request, id, lg):
    materia = materia_p.objects.get(id_mp=id)
    finanzas = compt.objects.all()
    for fz in finanzas:
        if fz.id_sv == id:
            fz.delete()
    materia.delete()
    return redirect('/' + str(lg) + '/materiap')

#------------------------------materia_s-------------------------------------------------

def materias(request, lg):
    isactive()
    materias = materia_s.objects.all()
    lista = []
    for ms in materias:
        if ms.id_lg_id == lg:
            lista.append(ms)
    return render(request, "materias/index.html", {'materias': lista, 'lugar': lg})

def copypz(mps, lg):
    materias = materia_s.objects.all()
    materiap = materia_p.objects.all()
    for ms2 in materias:
        if ms2.id_lg_id == lg:
            for mp2 in materiap:
                if mp2.id_lg_id == lg:
                    for mu in mps:
                        if mp2.nombre == mu[1] and ms2.nombre == mu[0]:
                            data = {'id_ms': ms2.id_ms, 'id_mp': mp2.id_mp, 'cantidad': mu[2], 'costo': int(mu[2]) * mp2.costo_u}
                            formulario = mzForm(data)
                            if formulario.is_valid():
                                formulario.save()

def copyz(lg):
    materias = materia_s.objects.all()
    mezclas = mezcla.objects.all()
    materiap = materia_p.objects.all()
    rep = "no"
    nombres = []
    estan = []
    mps = []
    for ms in materias:
        if ms.nombre not in nombres:
            nombres.append(ms.nombre)
            estan.append(ms)
            for mz in mezclas:
                if mz.id_ms_id == ms.id_ms:
                    for mp in materiap:
                        if mp.id_mp == mz.id_mp_id:
                            mps.append([ms.nombre, mp.nombre, mz.cantidad])
        else:
            for mz in mezclas:
                if mz.id_ms_id == ms.id_ms:
                    for mp in materiap:
                        if mp.id_mp == mz.id_mp_id:
                            for ml in mps:
                                if mp.nombre == ml[1]:
                                    rep = "si"
                                    break
                            if rep == "no":
                                mps.append([ms.nombre, mp.nombre, mz.cantidad])
                            rep = "no"
    for et in estan:
        data = {'nombre': et.nombre, 'descripcion': et.descripcion, 'estado': "Activo", 'id_lg': lg}
        formulario = msForm(data)
        if formulario.is_valid():
            formulario.save()
    copypz(mps, lg)

def agregar_ms(request, lg):
    materias = materia_s.objects.all()
    lugares = lugar.objects.all()
    formulario = dtMsForm(request.POST or None, request.FILES or None)
    entra = "no"
    descripcion = "None"
    if formulario.is_valid():
        if formulario.data['descripcion'] != '':
            descripcion = formulario.data['descripcion']
        nombre = formulario.data['nombre']
        for lug in lugares:
            for ms in materias: 
                if ms.id_lg_id == lug.id_lg and ms.nombre == nombre:
                    entra = "si"
                    break
            if lug.id_lg != 1 and entra == "no":
                data = {'nombre': nombre, 'descripcion': descripcion, 'estado': "Activo", 'id_lg': lug.id_lg}
                formulario = msForm(data)
                if formulario.is_valid():
                    formulario.save()
            entra = "no"
        return redirect('/'+str(lg)+'/materias')
    return render(request, "materias/crear.html", {'formulario': formulario})

def editar_ms(request, id, lg):
    materias = materia_s.objects.get(id_ms=id)
    formulario = msForm(request.POST or None, request.FILES or None, instance=materias)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('/'+str(lg)+'/materias')
    return render(request, "materias/editar.html", {'formulario': formulario})

def eliminar_ms(request, id, lg):
    materia = materia_s.objects.get(id_ms=id)
    materia.delete()
    return redirect('/'+str(lg)+'/materias')

#------------------------------mezcla-------------------------------------------------
def mezclas(request, id, lg):
    mezclas = mezcla.objects.all()
    materiap = materia_p.objects.all()
    materias = materia_s.objects.get(id_ms=id)
    estado = "Activo"
    ingredientes = []
    prm = []
    filtro = []
    for i in mezclas:
        if i.id_ms_id == id:
            filtro.append(i)
            for j in materiap:
                if j.id_mp == i.id_mp_id:
                    if i.cantidad > j.cantidad:
                        estado = "Inactivo"
                    j.estado = estado
                    materias.estado = estado
                    j.save()
                    materias.save()
                    prm.append(j)
    for a, b in zip(prm, filtro):
        b.id_us_id = id
        b.id_mp_id = a.nombre
        b.id_ms_id = materias.nombre
        ingredientes.append(b)
    return render(request, "mezcla/index.html", {'mezclas': ingredientes, 'materias': id, 'lugar': lg})

def agregar_mz(request, id, lg):
    mat = materia_s.objects.get(id_ms=id)
    materias = materia_s.objects.all()
    materiap = materia_p.objects.all()
    formulario = dtMzForm(request.POST or None, request.FILES or None)
    data = {}
    if formulario.is_valid():
        nombremp = (formulario.data['materia_p']).upper()
        for mp in materiap:
            if (mp.nombre).upper() == nombremp:
                for ms in materias:
                    if ms.nombre == mat.nombre and ms.id_lg_id == mp.id_lg_id:
                        data = {'id_ms': ms.id_ms, 'id_mp': mp.id_mp, 'cantidad': formulario.data['cantidad'], 'costo': int(formulario.data['cantidad']) * mp.costo_u}
                        formulario = mzForm(data)
                        if formulario.is_valid():
                            formulario.save()
        return redirect("/"+ str(lg) +'/mezcla' + str(id))
    return render(request, "mezcla/crear.html", {'formulario': formulario})

def editar_mz(request, id, id2, lg):
    materiap = materia_p.objects.all()
    mezclas = mezcla.objects.get(id_mz=id)
    formulario = mzForm(request.POST or None, request.FILES or None, instance=mezclas)
    if formulario.is_valid() and request.POST:
        formulario.save()
        for mp in materiap:
            if mezclas.cantidad > mp.cantidad:
                mp.estado = "Inactivo"
                mp.save()
        return redirect("/"+ str(lg) +'/mezcla' + str(id2))
    return render(request, "mezcla/editar.html", {'formulario': formulario})

def eliminar_mz(request, id, id2, lg):
    mezclas = mezcla.objects.get(id_mz=id)
    mezclas.delete()
    return redirect("/"+ str(lg) +'/mezcla' + str(id2))

#------------------------------posicion-------------------------------------------------

def posiciones(request, id, lg):
    posiciones = posicion.objects.all()
    productos = producto.objects.get(id_pd=id)
    resultado = []
    filtro = []
    for i in posiciones:
        if i.id_pd_id == id:
            filtro.append(i)
    for a in filtro:
        a.id_us_id = productos.nombre
        resultado.append(a)
    return render(request, "posicion/index.html", {'posiciones': resultado, 'producto': id, 'lugar': lg})

def agregar_ps(request, id, lg):
    nombrepd = producto.objects.get(id_pd=id).nombre
    productos = producto.objects.all()
    lugares = lugar.objects.all()
    formulario = dtPsForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        nombre = formulario.data['nombre']
        precio = formulario.data['precio']
        for lug in lugares:
            for pd in productos:
                if pd.id_lg_id == lug.id_lg and pd.nombre == nombrepd:
                    data = {'nombre': nombre, 'precio': precio, 'id_pd': pd.id_pd}
                    formulario = psForm(data)
                    formulario.save()
        return redirect("/"+str(lg)+'/posicion'+ str(id))
    return render(request, "posicion/crear.html", {'formulario': formulario})

def editar_ps(request, id, id2, lg):
    posiciones = posicion.objects.get(id_ps=id)
    formulario = psForm(request.POST or None, request.FILES or None, instance=posiciones)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("/"+str(lg)+'/posicion'+ str(id2))
    return render(request, "posicion/editar.html", {'formulario': formulario})

def eliminar_ps(request, id, id2, lg):
    posiciones = posicion.objects.get(id_ps=id)
    posiciones.delete()
    return redirect("/"+str(lg)+'/posicion'+ str(id2))

#------------------------------menu-------------------------------------------------

def menus(request, id, lg):
    menus = menu.objects.all()
    materias = materia_s.objects.all()
    posiciones = posicion.objects.get(id_ps=id)
    elementos = []
    sec = []
    filtro = []
    for i in menus:
        if i.id_ps_id == id:
            filtro.append(i)
            for j in materias:
                if j.id_ms == i.id_ms_id:
                    sec.append(j)
    for a, b in zip(sec, filtro):
        b.id_ms_id = a.nombre
        b.id_ps_id = posiciones.nombre
        elementos.append(b)
    return render(request, "menu/index.html", {'menus': elementos, 'posicion': id, 'lugar': lg})

def agregar_mn(request, id, lg):
    productos = producto.objects.all()
    py = posicion.objects.get(id_ps=id) 
    nom = producto.objects.get(id_pd=py.id_pd_id)
    posiciones = posicion.objects.all()
    lugares = lugar.objects.all()
    materias = materia_s.objects.all()
    formulario = dtMnForm(request.POST or None, request.FILES or None)
    data = {}
    if formulario.is_valid():
        mats = formulario.data['materia_s']
        for lug in lugares:
            for pd in productos:
                if pd.id_lg_id == lug.id_lg and pd.nombre == nom.nombre:
                    for ps in posiciones:
                        if ps.nombre == py.nombre and ps.id_pd_id == pd.id_pd:
                            for ms in materias:
                                if (ms.nombre).upper() == (mats).upper():
                                    if ms.id_lg_id == lg:
                                        data = {'id_ms': ms.id_ms, 'id_ps': ps.id_ps}
                                        formulario = mnForm(data)
                                        if formulario.is_valid():
                                            formulario.save()
        return redirect("/"+str(lg)+'/menu' + str(id))
    return render(request, "menu/crear.html", {'formulario': formulario})

def editar_mn(request, id, lg):
    menus = menu.objects.get(id_mn=id)
    formulario = mnForm(request.POST or None, request.FILES or None, instance=menus)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect("/"+str(lg)+'/menu' + str(menus.id_ps_id))
    return render(request, "menu/editar.html", {'formulario': formulario})

def eliminar_mn(request, id, lg):
    menus = menu.objects.get(id_mn=id)
    menus.delete()
    return redirect("/"+str(lg)+'/menu' + str(menus.id_ps_id))

#------------------------------carrito-------------------------------------------------

def carritos(request, lg):
    armados = armado.objects.all()
    menus = menu.objects.all()
    posiciones = posicion.objects.all()
    productos = producto.objects.all()
    carritos = candycarrito.objects.all()
    preciou = 0
    iter = 0
    lista = []
    presu = []
    pres = []
    precio = 0
    resultado = []
    for cr in carritos:
        if cr.id_lg_id == lg:
            lista.append(cr)
    for i in lista:
        for a in armados:
            if a.id_cr_id == i.id_cr:
                for m in menus:
                    if a.id_mn_id == m.id_mn:
                        for p in posiciones:
                            if p.id_ps == m.id_ps_id:
                                if p.id_ps not in pres:
                                    precio += p.precio
                                    preciou += p.precio
                                    pres.append(p.id_ps)
        presu.append(preciou)
        pres.clear()
        preciou = 0
        for j in productos:
            if i.id_pd_id == j.id_pd:
                i.nombre_pd = j.nombre
                i.precio = presu[iter] + j.precio
                precio += j.precio
                resultado.append(i)
                iter += 1
                break
                                
    return render(request, "carrito/index.html", {'carritos': resultado, 'precio': precio, 'lugar': lg})

def agregar_cr(request, id, lg):
    isactive()
    pd = producto.objects.get(id_pd=id)
    if pd.estado == "Inactivo":
        return render(request, "alerta/faltpd.html", {'lugar': lg})
    else:
        bases = basepd.objects.all()
        materiap = materia_p.objects.all()
        for bs in bases:
            if bs.id_pd_id == pd.id_pd:
                for mp in materiap:
                    if mp.id_mp == bs.id_mp_id:
                        mp.cantidad -= bs.cantidad
                        mp.save()
        data = {'id_pd': id, 'nombre_pd': "null", 'precio': 0, 'id_lg': lg} 
        formulario = crForm(data)
        if formulario.is_valid():
            formulario.save()
            return redirect('/'+str(lg)+'/carrito')
        return render(request, "carrito/crear.html", {'formulario': formulario})

def eliminar_cr(request, id, lg, id2):
    bases = basepd.objects.all()
    materiap = materia_p.objects.all()
    for bs in bases:
        if bs.id_pd_id == id2:
            for mp in materiap:
                if mp.id_mp == bs.id_mp_id:
                    mp.cantidad += bs.cantidad
                    mp.save()
    carritos = candycarrito.objects.get(id_cr=id)
    carritos.delete()
    return redirect('/'+str(lg)+'/carrito')

#------------------------------armado-------------------------------------------------

def armados(request, id, lg):
    carritos = candycarrito.objects.get(id_cr=id)
    armados = armado.objects.all()
    menus = menu.objects.all()
    posiciones = posicion.objects.all()
    materias = materia_s.objects.all()
    productos = producto.objects.all()
    precio = 0 # precio
    pres = [] #lista de posiciones ecogidas para regular precio
    arm = [] # lista de adiciones escogidas
    mats = [] # materias secundarias
    filtro = [] # variaciones del producto escogido con los nombres de las materias secundarias 
    for pd in productos:
        if pd.id_pd == carritos.id_pd_id:
            prod=pd
            break
    for ps in posiciones:
        if ps.id_pd_id == prod.id_pd:
            ps.id_pd_id = prod.nombre
            filtro.append(ps)
    for fl in filtro:           
        for mn in menus:
            if mn.id_ps_id == fl.id_ps:
                for ms in materias:
                    if ms.id_ms == mn.id_ms_id:
                        ms.descripcion = fl.id_ps
                        ms.tiempo = mn.id_mn
                        ms.car = id
                        mats.append(ms)
                        for ar in armados:
                            if ar.id_cr_id == carritos.id_cr:
                                if ar.id_mn_id == mn.id_mn:
                                    if fl.id_ps not in pres:
                                        precio += fl.precio
                                        pres.append(fl.id_ps)
                                    ar.nombre_ms = ms.nombre
                                    arm.append(ar)
    if len(arm) == 0:
        precio = 0                    
    return render(request, "armado/index.html", {'posiciones': filtro, 'materias': mats, 'armados': arm, 'precio': precio, 'lugar': lg})

def agregar_ar(request, id, id2, lg, ms):
    isactive()
    mas = materia_s.objects.get(id_ms=ms)
    if mas.estado == "Inactivo":
        return render(request, "alerta/falta.html", {'lugar': lg, 'id':id})
    else:
        mezclas = mezcla.objects.all()
        materiap = materia_p.objects.all()
        for mz in mezclas:
            if mz.id_ms_id == ms:
                for mp in materiap:
                    if mp.id_mp == mz.id_mp_id:
                        mp.cantidad -= mz.cantidad
                        mp.save()
        data = {'id_cr': id, 'id_mn': id2, 'nombre_ms': 'null', 'precio': 0}
        formulario = arForm(data)
        if formulario.is_valid():
            formulario.save()
            return redirect("/"+str(lg)+"/armado"+ str(id))
        return render(request, "armado/crear.html", {'formulario': formulario})

def eliminar_ar(request, id, id2, lg, mn):
    men = menu.objects.get(id_mn=mn)
    mas = materia_s.objects.get(id_ms=men.id_ms_id)
    mezclas = mezcla.objects.all()
    materiap = materia_p.objects.all()
    for mz in mezclas:
        if mz.id_ms_id == mas.id_ms:
            for mp in materiap:
                if mp.id_mp == mz.id_mp_id:
                    mp.cantidad += mz.cantidad
                    mp.save()
    armados = armado.objects.get(id_ar=id)
    armados.delete()
    return redirect("/"+str(lg)+"/armado"+ str(id2))

#------------------------------entregado-------------------------------------------------

def entregados(request, lg):
    entregados = entregado.objects.all()
    filtro = []
    for et in entregados:
        if et.id_lg_id == lg:
            filtro.append(et)
    precio = 0
    clientes = []
    precios = []
    rep = []
    mesas = []
    for en in filtro:
        if en.mesa not in rep:
            precio = en.precio
            clientes.append(en.cliente)
            precios.append(precio)
            rep.append(en.mesa)
        else:
            lugar = rep.index(en.mesa)
            precio = en.precio + precios[lugar]
            precios.pop(lugar)
            rep.pop(lugar)
            clientes.pop(lugar)
            rep.append(en.mesa)
            clientes.append(en.cliente)
            precios.append(precio)
    i = 0
    for ms in rep:
        mesas.append([ms, "|  Precio: "+ str(precios[i]), " |  Cliente: " + clientes[i]])
        i+=1
    return render(request, "entregado/index.html", {'entregados': entregados, 'mesas': mesas, 'lugar': lg})

def agregar_en(request, lg):
    carritos = candycarrito.objects.all()
    productos = producto.objects.all()
    armados = armado.objects.all()
    posiciones = posicion.objects.all()
    menus = menu.objects.all()
    materias = materia_s.objects.all()
    pres = []
    precio = 0
    preciof = 0
    arm = " "
    formulario = dtEnForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        for car in carritos:
            for ar in armados:
                if ar.id_cr_id == car.id_cr:
                    for mn in menus:
                        if mn.id_mn == ar.id_mn_id:
                            for ms in materias:
                                if ms.id_ms == mn.id_ms_id:
                                    arm += str(ms.nombre) + " - "
                            for p in posiciones:
                                if p.id_ps == mn.id_ps_id:
                                    if p.id_ps not in pres:
                                        precio += p.precio
                                        preciof += p.precio
                                        pres.append(p.id_ps)
            pres.clear()
            for prod in productos:
                if prod.id_pd == car.id_pd_id:
                    precio += prod.precio
                    preciof += prod.precio
                    if arm == " ":
                        arm = "Sin adiciones"
                    else:
                        dis = len(arm)
                        arm = arm[:dis-2]
                    data = {'mesa': formulario.data['mesa'], 'cliente': formulario.data['cliente'], 'id_cr': prod.nombre, 'descripcion': arm, 'precio': precio, 'preciot': preciof, 'id_lg': lg} 
                    finanzas(-1 ,"Venta: "+ prod.nombre, precio, "/entregado", lg)
                    form = enForm(data)
                    arm = " "
                    precio = 0
                    if form.is_valid():
                        form.save()
        carritos.delete()                
        return redirect('/'+str(lg)+'/entregado') 
    return render(request, "entregado/crear.html", {'formulario': formulario})

def eliminar_en(request, id, lg):
    entregados = entregado.objects.get(id_eg=id)
    entregados.delete()
    return redirect('/'+str(lg)+'/entregado')

#------------------------------factura-------------------------------------------------
def agregar_ft(request, mesa, lg):
    data = {'id_lg': lg}
    formulario = ftForm(data)
    if formulario.is_valid():
        formulario.save()
        agregar_inft(mesa, lg)
        return redirect('/'+str(lg)+'/entregado') 
    return render(request, "factura/crear.html", {'formulario': formulario})

#------------------------------infoft-------------------------------------------------

def infactura(request, lg):
    infactura = infofactura.objects.all()
    lugares = lugar.objects.all()
    for lug in lugares:
        if lug.id_lg == lg:
            maps = lug.nombre
            break
    filtro = []
    for inf in infactura:
        if inf.lugar == maps:
            filtro.append(inf)
    titulos = []
    tablas = []
    for ft in filtro:
        if ft.id_ft not in tablas:
            tablas.append(ft.id_ft)
            titulos.append([ft.id_ft, [ft.producto], ft.precio, ft.fecha])
        else:
            lugars=tablas.index(ft.id_ft)
            titulos[lugars][1].append(ft.producto)
            titulos[lugars][2] += ft.precio
        
    return render(request, "infofactura/index.html", {'informaciones': filtro, 'titulos': titulos, 'lugar': lg, 'nombre': maps})

def masinfo(request, id, lg):
    infactura = infofactura.objects.all()
    lugares = lugar.objects.all()
    for lug in lugares:
        if lug.id_lg == lg:
            maps = lug.nombre
            break
    info = []
    for ft in infactura:
        if ft.id_ft == id:
            info.append(ft)
    return render(request, "infofactura/masinfo.html", {'infos': info, 'lugar': maps})


def agregar_inft(mesa, lg):
    facturas = factura.objects.all()
    lugares = lugar.objects.all()
    for lug in lugares:
        if lug.id_lg == lg:
            lugars = lug.nombre  
            break 
    for i in facturas:
        id = i.id_ft
        break
    carritos = candycarrito.objects.all()
    entregados = entregado.objects.all()
    for en in entregados:
        if en.mesa == mesa:
            fecha = datetime.now()
            data = {'precio': en.precio, 'entregado': en.id_eg, 'producto': en.id_cr, 'adiciones': en.descripcion, 'fecha': "  " + str(date.today()) + "  |  " + str(fecha.strftime("%X")), 'id_ft': id, 'lugar': lugars}
            formulario = inftForm(data)
            if formulario.is_valid():
                formulario.save() 
            en.delete()
    facturas.delete()
    return redirect('/'+str(lg)+'/entregado')


#---------------------------------------------------------------------------------------------

def admins(request, lg):
    if lg == 1:
        return render(request, "admins/bodega.html", {'lugar': lg}) 
    else:
        return render(request, "admins/index.html", {'lugar': lg})

#--------------------------------------------------------------------------------------------

def enviarp(request, nombrep, lg):
    lugares = lugar.objects.all()
    finanzasi = compt.objects.all()
    materiap = materia_p.objects.all()
    formulario = enviarForm(request.POST or None, request.FILES or None)
    pas = "no"
    if formulario.is_valid() and request.POST:
        for lug in lugares:
            if (lug.nombre).upper() == (formulario.data['lugar']).upper():
                break
        for mp in materiap:
            if (mp.nombre).upper() == (nombrep).upper():
                if mp.id_lg_id == lug.id_lg:
                    mp.cantidad += int(formulario.data['cantidad'])
                    mp.costo += mp.costo_u * int(formulario.data['cantidad'])
                    pas = "si"
                    mp.save()
                    finanzas(mp.id_mp ,"Avastecido "+ str(formulario.data['cantidad'])+": "+ mp.nombre , 0-mp.costo_u * int(formulario.data['cantidad']), "/materiap", lug.id_lg)
                elif mp.id_lg_id == lg:
                    mp.cantidad -= int(formulario.data['cantidad'])
                    mp.costo -= mp.costo_u*int(formulario.data['cantidad'])
                    mp.save()
                    resta = mp.costo_u*int(formulario.data['cantidad'])
                    for fz in finanzasi:
                        if fz.id_sv == mp.id_mp:
                            if fz.costo > 0-(resta):
                                resta += fz.costo
                                fz.costo = 0
                                fz.save()
                            else:
                                fz.costo += resta
                                fz.save()
                                resta = 0
        if pas == "no":
            for mp in materiap:
                if mp.id_lg_id == lg and mp.nombre == nombrep:
                    data = {'nombre': mp.nombre, 'cantidad': int(formulario.data['cantidad']), 'unidad': mp.unidad, 'costo': float("{0:.2f}".format(mp.costo_u*int(formulario.data['cantidad']))), 'costo_u': mp.costo_u, 'proveedor': mp.proveedor, 'contacto': mp.contacto, 'tiempo': mp.tiempo, 'mincant': mp.mincant, 'descripcion': mp.descripcion, 'estado': mp.estado, 'fecha': "  " + str(date.today()), 'id_lg': lug.id_lg}
                    formulario = mpForm(data)
                    formulario.save()
                    materiap2 = materia_p.objects.get(nombre=mp.nombre, id_lg=lug.id_lg)
                    finanzas(materiap2.id_mp ,"Materia prima: "+ materiap2.nombre , 0-materiap2.costo, "/materiap", lug.id_lg)
        return redirect('/'+str(lg)+'/materiap')
    return render(request, "enviarp/enviar.html", {'formulario': formulario})

def alerta(request, nombre, id):
    return render(request, "alerta/index.html",{'nombre':nombre, 'id':id})
