from .mongodb import get_db
from bson.objectid import ObjectId
from django.shortcuts import redirect, render


# database1 = get_db()
# collection1 = database1['collection1']

def some_view(request):
    db = get_db()
    if db is None:
        return JsonResponse({"error": "Database connection failed."}, status=500)

    try:
        # Access a collection in the database
        collection = db['collection1']
        data = collection.find_one()  # Example operation
        return JsonResponse({"data": data})

    except Exception as e:
        print("Error during database operation:", e)
        return JsonResponse({"error": "An error occurred while fetching data."}, status=500)

def index(request):
    items = list(collection1.find())
    for item in items:
        item['id']=str(item['_id'])
    return render(request, 'index.html', {'items': items })
    

def add_item(request):
    if request.method == 'POST' :
       name=  request.POST.get('name')
       phone=  request.POST.get('phone')

       collection1.insert_one({"name": name , "phone":phone})

       return redirect("index")

    return render(request, 'add_item.html' )
    

def update_item(request, item_id  ):
    
    if request.method=="POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        collection1.update_one({'_id': ObjectId(item_id) }, {'$set':{"name":name, "phone": phone}})

        return redirect("index")
    
    item = collection1.find_one({ '_id': ObjectId(item_id) })
    item['id'] = str(item['_id'])
    return render(request, 'update_item.html',{'item': item })
   

def delete_item(request, item_id ):
    collection1.delete_one({"_id":ObjectId(item_id) })
    return redirect('index')
    
