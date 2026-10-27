
# @csrf_exempt
# def Equipment_update(request):

#     if request.method != "PUT":
#         return JsonResponse({
#             "success": False,
#             "msg": "Invalid request method"
#         }, status=405)

#     auth_header = request.headers.get("Authorization", "")

#     auth_part = auth_header.split()

#     if len(auth_part) != 2 or auth_part[0].lower() != "bearer":
#         return JsonResponse({
#             "success": False,
#             "msg": "Bearer token is required"
#         }, status=401)

#     access_token = AccessToken(auth_part[1])
#     seller_id = access_token.get("user_id")

#     if not seller_id:
#         return JsonResponse({
#             "success": False,
#             "msg": "User ID missing from token"
#         }, status=401)


#     data = json.loads(request.body)
#     equipment_id = data.get("equipment_id")
#     name_equipment = data.get("name_equipment")
#     description = data.get("description")
#     brand = data.get("brand")
#     model = data.get("model")
#     duration = data.get("duration")
#     price_per_day = data.get("price_per_day")
#     available_from = data.get("available_from")
#     available_to = data.get("available_to")
    
#     updated_data={}
#     if name_equipment is not None:
#         updated_data["name_equipment"] = name_equipment
        
#     if description is not None:
#         updated_data["description"] = description.strip()

#     if brand is not None:
#         updated_data["brand"] = brand.strip()

#     if model is not None:
#         updated_data["model"] = model.strip()

#     if duration is not None:
#         updated_data["duration"] = duration

#     if price_per_day is not None:
#         updated_data["price_per_day"] = price_per_day

#     if available_from is not None:
#         updated_data["available_from"] = date.fromisoformat(available_from)

#     if available_to is not None:
#         updated_data["available_to"] = date.fromisoformat(available_to)
   
#     equipment = Equipment.objects.filter(id=equipment_id).update(**updated_data)
#     if equipment == 0:
#         return JsonResponse({
#             "success": False,
#             "message": "Equipment not found"
#         }, status=404)

#     equipment = Equipment.objects.get(id=equipment_id)

#     return JsonResponse({
#         "success": True,
#         "message": "Equipment updated successfully",
#         "data": {
#             "id": str(equipment.id),
#             "name_equipment": equipment.name_equipment,
#             "description": equipment.description,
#             "brand": equipment.brand,
#             "model": equipment.model,
#             "duration": equipment.duration,
#             "price_per_day": str(equipment.price_per_day),
#             "available_from": equipment.available_from.isoformat(),
#             "available_to": equipment.available_to.isoformat(),
#             "availability_status": equipment.availability_status
#         }
#     }, status=200)
   