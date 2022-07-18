"""candyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from candyapp import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name="signup"),
    path('lugares', views.lugares, name="lugar"),
    path('alertalg/<str:nombre>/<int:id>', views.alerta, name="alerta"),
    path('<int:id>', views.log, name="log"),
    path('agregarlg', views.agregar_lg, name="agregar_lg"),
    path('eliminarlg/<int:id>', views.eliminar_lg, name="eliminar_lg"),
    path('<int:lg>/home', views.home, name="inicio"),
    path('nosotros', views.nosotros, name="nosotros"),
#-------------------------------------------------------------------------------------------    
    path('<int:lg>/productos', views.productos, name="productos"),
    path('<int:lg>/addproductos', views.agregar_pd, name="agregar"),
    path('<int:lg>/eliminar/<int:id>', views.eliminar_pd, name="eliminar"),
    path('<int:lg>/editproductos<int:id>', views.editar_pd, name="editar"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/base<int:id>', views.baseprod, name="basepd"),
    path('<int:lg>/addbase<int:id>', views.addbase, name="addbasepd"),
    path('<int:lg>/delbase/<int:id>/<int:id2>', views.delbase, name="delbasepd"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/materiap', views.materiap, name="materiap"),
    path('<int:lg>/materiap<int:id>', views.avastecer, name="avastecer"),
    path('<int:lg>/addmateriap', views.agregar_mp, name="agregar_mp"),
    path('<int:lg>/editmateriap<int:id>', views.editar_mp, name="editar_mp"),
    path('<int:lg>/eliminarm/<int:id>', views.eliminar_mp, name="eliminar_mp"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/materias', views.materias, name="materias"),
    path('<int:lg>/addmaterias', views.agregar_ms, name="agregar_ms"),
    path('<int:lg>/editmaterias<int:id>', views.editar_ms, name="editar_ms"),
    path('<int:lg>/eliminars/<int:id>', views.eliminar_ms, name="eliminar_ms"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/mezcla<int:id>', views.mezclas, name="mezclas"),
    path('<int:lg>/addmix<int:id>', views.agregar_mz, name="agregar_mz"),
    path('<int:lg>/editmix<int:id>/<int:id2>', views.editar_mz, name="editar_mz"),
    path('<int:lg>/eliminarmix/<int:id>/<int:id2>', views.eliminar_mz, name="eliminar_mz"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/posicion<int:id>', views.posiciones, name="posiciones"),
    path('<int:lg>/addpos<int:id>', views.agregar_ps, name="agregar_ps"),
    path('<int:lg>/editpos<int:id>/<int:id2>', views.editar_ps, name="editar_ps"),
    path('<int:lg>/eliminarpos/<int:id>/<int:id2>', views.eliminar_ps, name="eliminar_ps"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/menu<int:id>', views.menus, name="menus"),
    path('<int:lg>/addmenu<int:id>', views.agregar_mn, name="agregar_mn"),
    path('<int:lg>/editmenu<int:id>', views.editar_mn, name="editar_mn"),
    path('<int:lg>/eliminarmenu/<int:id>', views.eliminar_mn, name="eliminar_mn"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/carrito', views.carritos, name="carritos"),
    path('<int:lg>/addcar<int:id>', views.agregar_cr, name="agregar_cr"),
    path('<int:lg>/eliminarcr/<int:id>/<int:id2>', views.eliminar_cr, name="eliminar_cr"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/armado<int:id>', views.armados, name="armado"),
    path('<int:lg>/addarm<int:id>/<int:id2>/<int:ms>', views.agregar_ar, name="agregar_ar"),
    path('<int:lg>/eliminarar<int:id>/<int:id2>/<int:mn>', views.eliminar_ar, name="eliminar_ar"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/entregado', views.entregados, name="entregado"),
    path('<int:lg>/addent', views.agregar_en, name="agregar_en"),
    path('<int:lg>/eliminaren/<int:id>', views.eliminar_en, name="eliminar_en"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/factura/<str:mesa>', views.agregar_ft, name="factura"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/historial', views.infactura, name="historial"),
    path('<int:lg>/historial<int:id>', views.masinfo, name="masinfo"),
#------------------------------------------------------------------------------------------
    path('<int:lg>/admin', views.admins, name="admin"),
#-------------------------------------------------------------------------------------------
    path('<int:lg>/enviar/<str:nombrep>', views.enviarp, name="enviarp"),
#---------------------------------------------------------------------------------------------
    path('<int:lg>/finanzas', views.verfinanza, name="finanzas"),
    path('<int:lg>/addfinanzas', views.add_finz, name="addfinanzas"),
    path('<int:lg>/historiafz', views.gen_fz, name="hfz"),
    path('<int:lg>/verfz<int:id>', views.hist_fz, name="verfz"),
    path('<int:lg>/masinfofz<int:id>', views.info_fz, name="infz")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)