from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index, name="index"),
    path('usere',views.usere, name="usere"),
    path('checklogin',views.checklogin, name="index"),
    path('login',views.login, name="login"),
    path('Register',views.Register, name="Register"),
    path('register',views.register),
    path('mod',views.mod, name="mod"),
    path('addeval',views.addeval,name="addeval"),
    path('drope',views.drope),
    path('add_prod',views.add_prod),
    path('prod',views.prod),
    path('logout',views.logout),
    path('home',views.home),
    path('add_slot',views.add_slot, name="add_slot"),
    path('up_pass',views.up_pass),
    path('eval',views.eval),
    path('ev_reg',views.ev_reg),
    path('ad_slot',views.ad_slot),
    path('add_slot',views.add_slot),
    #path('evalinfi',views.evalinfi),
    path('display',views.display),
    path('display1',views.display1),
    path('userinfoy',views.userinfoy),
    path('smessage/<int:id>',views.responsepage),
    path('res',views.res),
    path('viewpr',views.viewpr),
    path('smessage1/<int:id>',views.advisepage),
    path('update',views.update),
    path('updatel',views.updatel),
    path('updatee',views.updatee),
    path('profile',views.profile),
    path('viewprofile',views.viewprofile),
    path('shop',views.shop),
    # path('usere/payment',views.payment),
    path('type-select', csrf_exempt(views.type_select),name='type-select'),
    path('type-select1', csrf_exempt(views.type_select1),name='type-select1'),
    path('cartupdate', csrf_exempt(views.cartupdate),name='cartupdate'),
    path('dash',views.dash),
    path('smessage2/<int:id>',views.promote),
    path('nmessage/<int:id>',views.block),
    path('mmessage/<int:id>',views.unblock),
    path('cart',views.cart),
    path('check',views.check),  
    path('table',views.table),
    path('tableuser',views.tableuser),
    path('tableeval',views.tableeval),
    path('pmessage2/<int:cid>',views.addtocart),
    path('rmessage2/<int:id>',views.remove),
    path('cmessage/',views.checkout),
    path('pmessage/',views.placeorder),
    path('paymenthandler', views.paymenthandler, name='paymenthandler'),
    # path('sujith', views.sujith),
    path('ordersi',views.ordersi),
    path('tmessage/<int:id>',views.orderd),
    path('bmessage/<int:cid>',views.buyagain),
    path('remessage/<int:mid>',views.returne),
    path('orders',views.orders),
    path('vmessage/<int:vid>',views.ordersd),
    path('updatequantity/<int:pid>/<int:q>',views.updatequantity),
    path('advise',views.advise),
    path('cultiv',views.cultiv),
    path('add_culti',views.add_culti),
    path('upcult',views.upcult),
    path('cultistatus/<int:ctid>/<str:status>',views.cultistatus),
    path('evalculti',views.evalculti),
    path('dash',views.dash),
    path('track',views.track),
    path('tracky',views.tracky),
    path('adm',views.adm),
    path('admstatus',views.admstatus),
    # path('ordersad',views.ordersad)
]
