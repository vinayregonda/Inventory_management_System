from django.contrib import admin
from django.urls import path
from inventory import views
urlpatterns = [
    path('',views.loginpage, name='login'),
    path('create_user/', views.create_user, name='create_user'),

    path('logout',views.logout1,name='logout'),

    path('dashboard',views.dashboard,name='dashboard'),
    path('customermodule/',views.customermodule,name='customermodule'),
    path('categorymodule',views.categorymodule,name='categorymodule'),
    path('deletecategory/<int:categoryid>/',views.deletecategory,name='deletecategory'),
    path('editcategory/<int:categoryid>/',views.editcategory,name='editcategory'),
    path('updatecategory/<int:categoryid>/',views.updatecategory,name='updatecategory'),

    
    path('brandmodule/',views.brandmodule,name='brandmodule'),

    path('suppliermodule',views.suppliermodule,name='suppliermodule'),
    path('deletesupplier/<int:supplierid>',views.deletesupplier,name='deletesupplier'),
    path('editsupplier/<int:supplierid>',views.editsupplier,name='editsupplier'),
    path('updatesupplier/<int:supplierid>',views.updatesupplier,name='updatesupplier'),

    path('productmodule/',views.productmodule,name='productmodule'),
    
    path('purchasemodule',views.purchasemodule,name='purchasemodule'),
    path('deletepurchase/<int:purchase_id>/',views.deletepurchase,name='deletepurchase'),
    path('editpurchase/<int:purchase_id>/',views.editpurchase,name='editpurchase'),
    path('updatepurchase/<int:purchase_id>/',views.updatepurchase,name='updatepurchase'),

    path('ordersmodule/',views.ordersmodule,name='ordersmodule'),
    path('editorder/<int:order_id>/',views.editorder,name='editorder'),
    path('updateorder/<int:order_id>/',views.updateorder,name='updateorder'),

]

