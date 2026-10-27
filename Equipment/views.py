import json

from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import date
from .models_equipment import Equipment


from .models import userRegister


@csrf_exempt
def user_registration(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request method"}, status=405
        )

    data = json.loads(request.body)

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    role = data.get("role")
    password = data.get("password")

    if not name or not email or not phone or not role or not password:
        return JsonResponse(
            {
                "success": False,
                "message": "Name, email, phone, role and password are required",
            },
            status=400,
        )

    if userRegister.objects(email=email).first():
        return JsonResponse(
            {"success": False, "message": "Email already exists"}, status=400
        )

    otp = random.randint(100000, 999999)

    user = userRegister(
        name=name,
        email=email,
        phone=phone,
        role=role,
        password=make_password(password),
        otp=otp,
        is_verified=False,
    )

    user.save()

    return JsonResponse(
        {
            "success": True,
            "message": "User registered successfully",
            "user": {
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "password": user.password,
                "otp": otp,
                " is_verified": False,
            },
        },
        status=201,
    )


# ----------------------------------------------login api---------------------------------
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request method"}, status=405
        )

    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse(
            {"success": False, "message": "Name, email and password are required"},
            status=400,
        )
    try:
        user = userRegister.objects.get(email=email)
    except userRegister.DoesNotExist:
        return JsonResponse({"message": "Invalid email or password"}, status=401)

    if not check_password(password, user.password):
        return JsonResponse(
            {"sucess": False, "message": "invalid password"}, status=401
        )

    if not user.is_verified:
        return JsonResponse(
            {"success": False, "message": "Please verify your email first"}, status=403
        )

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    return JsonResponse(
        {
            "success": True,
            "message": "Login successful",
            "user": {
                "name": user.name,
                "email": user.email,
            },
            "access_token": str(access_token),
            "refresh_token": str(refresh),
        },
        status=200,
    )


# ----------------------------------------------get user api---------------------------------


@csrf_exempt
def get_user(request):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "message": "Invalid request method"}, status=405
        )

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse(
            {"success": False, "message": "Authorization token is required"}, status=401
        )

    auth_parts = auth_header.split()
    if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
        return JsonResponse(
            {
                "success": False,
                "message": "Authorization header must use Bearer token format",
            },
            status=401,
        )

    try:
        access_token = AccessToken(auth_parts[1])
    except TokenError:
        return JsonResponse(
            {"success": False, "message": "Invalid or expired access token"}, status=401
        )

    user_id = access_token.get("user_id")
    if not user_id:
        return JsonResponse(
            {"success": False, "message": "Invalid access token"}, status=401
        )

    user = userRegister.objects(id=user_id).first()
    if not user:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    return JsonResponse(
        {
            "success": True,
            "msg": "user fetched sucessfull",
            "user": {"name": user.name, "email": user.email},
        },
        status=200,
    )


# ----------------------------------------------update user api---------------------------------
@csrf_exempt
def update_user(request):

    if request.method != "PUT":
        return JsonResponse(
            {"success": False, "message": "Invalid request method"}, status=405
        )

    data = json.loads(request.body)

    email = data.get("email")

    if not email:
        return JsonResponse(
            {"success": False, "message": "Email is required"}, status=400
        )

    name = data.get("name")
    password = data.get("password")
    otp = data.get("otp")
    is_verified = data.get("is_verified")

    update_data = {}

    if name is not None:
        update_data["name"] = name

    if password is not None:
        update_data["password"] = password

    if otp is not None:
        update_data["otp"] = otp

    if is_verified is not None:
        update_data["is_verified"] = is_verified

    updated = userRegister.objects.filter(email=email).update(**update_data)

    if updated == 0:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    user = userRegister.objects.get(email=email)

    return JsonResponse(
        {
            "success": True,
            "message": "User updated successfully",
            "data": {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "otp": user.otp,
                "is_verified": user.is_verified,
            },
        },
        status=200,
    )


# ----------------------------------------------verfiy otp---------------------------------


@csrf_exempt
def verify_otp(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request method"}, status=405
        )

    data = json.loads(request.body)

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return JsonResponse(
            {"success": False, "message": "Email and OTP are required"}, status=400
        )

    user = userRegister.objects.filter(email=email).first()

    if not user:
        return JsonResponse({"success": False, "message": "User not found"}, status=404)

    if user.is_verified:
        return JsonResponse(
            {"success": False, "message": "User is already verified"}, status=400
        )

    if user.otp != otp:
        return JsonResponse({"success": False, "message": "Invalid OTP"}, status=400)

    user.is_verified = True
    user.save()

    return JsonResponse(
        {"success": True, "message": "OTP verified successfully"}, status=200
    )


# ----------------------------------------------froget password api---------------------------------
@csrf_exempt
def froget_password(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "msg": "invalid request method"}, status=405
        )

    data = json.loads(request.body)
    email = data.get("email")

    if not email:
        return JsonResponse(
            {"success": False, "msg": " please provide email"}, status=400
        )

    user = userRegister.objects.filter(email=email).first()

    if not user:
        return JsonResponse({"success": False, "msg": "email not found"}, status=400)

    otp = random.randint(100000, 999999)

    user.otp = otp

    user.save()

    return JsonResponse(
        {
            "success": True,
            "msg": "otp send to the mail",
            "data": {"email": user.email, "otp": user.otp},
        }
    )


# ----------------------------------------------reset password api---------------------------------


@csrf_exempt
def rest_paswword(request):

    if request.method != "POST":
        return JsonResponse(
            {"sucess": False, "msg": "invalid request method"}, status=405
        )

    data = json.loads(request.body)

    email = data.get("email")
    otp = data.get("otp")
    password = data.get("password")

    if not email or not otp or not password:
        return JsonResponse(
            {"success": False, "msg": "please provide email ,otp and new_password"},
            status=400,
        )

    user = userRegister.objects.filter(email=email).first()

    if not user:
        return JsonResponse({"success": False, "msg": "email not found"}, status=400)

    if user.otp != otp:
        return JsonResponse({"success": False, "message": "Invalid OTP"}, status=400)

    user.password = make_password(password)

    user.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Password reset successfully",
            "data": {"email": user.email, "password": user.password},
        },
        status=200,
    )


# ----------------------------------------------delete user api---------------------------------
@csrf_exempt
def delete(request):
    if request.method != "DELETE":
        return JsonResponse(
            {"success": False, "msg": "invalid request methhod"}, status=405
        )

    data = json.loads(request.body)
    email = data.get("email")

    user = userRegister.objects.filter(email=email)
    if not user:
        return JsonResponse({"success": False, "msg": "user not found"}, status=400)

    user.delete()

    return JsonResponse(
        {
            "success": True,
            "message": "user delete successfully",
        },
        status=200,
    )


# ----------------------------------------------Equipment_register api---------------------------------


@csrf_exempt
def equipment_register(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "msg": "Invalid request method"}, status=405
        )

    auth_header = request.headers.get("Authorization")
    auth_part = auth_header.split()

    if len(auth_part) != 2 or auth_part[0].lower() != "bearer":
        return JsonResponse(
            {"success": False, "msg": "Bearer token is required"}, status=401
        )

    access_token = AccessToken(auth_part[1])
    seller_id = access_token.get("user_id")

    seller = userRegister.objects(id=seller_id).first()

    if not seller:
        return JsonResponse({"success": False, "msg": "Seller not found"}, status=404)

    if seller.role != "EQUIPMENT_OWNER":
        return JsonResponse(
            {"success": False, "msg": "Only equipment owners can register equipment"},
            status=403,
        )

    data = json.loads(request.body)

    name_equipment = data.get("name_equipment")
    description = data.get("description")
    brand = data.get("brand")
    model = data.get("model")
    duration = data.get("duration")
    price_per_day = data.get("price_per_day")
    available_from_str = data.get("available_from")
    available_to_str = data.get("available_to")

    if (
        not all(
            [
                name_equipment,
                description,
                brand,
                model,
                duration,
                available_from_str,
                available_to_str,
            ]
        )
        or price_per_day is None
    ):
        return JsonResponse(
            {"success": False, "msg": "All fields are required"}, status=400
        )

    available_from = date.fromisoformat(available_from_str)
    available_to = date.fromisoformat(available_to_str)

    if available_from > available_to:
        return JsonResponse(
            {"success": False, "msg": "End date must be after start date"}, status=400
        )

    equipment = Equipment.objects.create(
        seller_id=seller,
        name_equipment=name_equipment.strip(),
        description=description.strip(),
        brand=brand.strip(),
        model=model.strip(),
        duration=duration,
        price_per_day=price_per_day,
        available_from=available_from,
        available_to=available_to,
        availability_status="AVAILABLE",
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Equipment registered successfully",
            "data": {
                "id": str(equipment.id),
                "seller_id": str(seller.id),
                "name_equipment": equipment.name_equipment,
                "description": equipment.description,
                "brand": equipment.brand,
                "model": equipment.model,
                "duration": equipment.duration,
                "price_per_day": str(equipment.price_per_day),
                "available_from": equipment.available_from.isoformat(),
                "available_to": equipment.available_to.isoformat(),
                "availability_status": equipment.availability_status,
            },
        },
        status=201,
    )


# ----------------------------------------------Equipment update api---------------------------------


@api_view(["PUT"])
def Equipment_update(request):
    auth_header = request.headers.get("Authorization", "")

    auth_part = auth_header.split()

    if len(auth_part) != 2 or auth_part[0].lower() != "bearer":
        return JsonResponse(
            {"success": False, "msg": "Bearer token is required"}, status=401
        )

    access_token = AccessToken(auth_part[1])
    register_id = access_token.get("user_id")

    if not register_id:
        return JsonResponse(
            {"success": False, "msg": "User ID missing from token"}, status=401
        )

    seller = userRegister.objects(id=register_id).first()
    if not seller:
        return JsonResponse({"success": False, "msg": "Seller not found"}, status=404)

    if seller.role != "EQUIPMENT_OWNER":
        return JsonResponse(
            {"success": False, "msg": "Only equipment owners can update equipment"},
            status=403,
        )

    data = request.data
    equipment_id = data.get("equipment_id")
    if not equipment_id:
        return JsonResponse(
            {"success": False, "msg": "Equipment ID is required"}, status=400
        )

    equipment = Equipment.objects(id=equipment_id, seller_id=seller).first()
    if not equipment:
        return JsonResponse(
            {"success": False, "msg": "Equipment not found"}, status=404
        )

    name_equipment = data.get("name_equipment")
    description = data.get("description")
    brand = data.get("brand")
    model = data.get("model")
    duration = data.get("duration")
    price_per_day = data.get("price_per_day")
    available_from = data.get("available_from")
    available_to = data.get("available_to")

    updated_data = {}
    if name_equipment and name_equipment.strip():
        updated_data["name_equipment"] = name_equipment.strip()

    if description and description.strip():
        updated_data["description"] = description.strip()

    if brand and brand.strip():
        updated_data["brand"] = brand.strip()

    if model and model.strip():
        updated_data["model"] = model.strip()

    if duration is not None and duration != "":
        updated_data["duration"] = duration

    if price_per_day not in (None, ""):
        updated_data["price_per_day"] = price_per_day

    if available_from not in (None, ""):
        updated_data["available_from"] = date.fromisoformat(available_from)

    if available_to not in (None, ""):
        updated_data["available_to"] = date.fromisoformat(available_to)

    if not updated_data:
        return JsonResponse(
            {"success": False, "message": "Provide at least one field to update"},
            status=400,
        )

    updated_from = updated_data.get("available_from", equipment.available_from)
    updated_to = updated_data.get("available_to", equipment.available_to)
    if updated_from > updated_to:
        return JsonResponse(
            {
                "success": False,
                "message": "End date must be after or equal to start date",
            },
            status=400,
        )

    for field, value in updated_data.items():
        setattr(equipment, field, value)
    equipment.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Equipment updated successfully",
            "data": {
                "id": str(equipment.id),
                "name_equipment": equipment.name_equipment,
                "description": equipment.description,
                "brand": equipment.brand,
                "model": equipment.model,
                "duration": equipment.duration,
                "price_per_day": str(equipment.price_per_day),
                "available_from": equipment.available_from.isoformat(),
                "available_to": equipment.available_to.isoformat(),
                "availability_status": equipment.availability_status,
            },
        },
        status=200,
    )


# ----------------------------------------------get Equipment detail api---------------------------------

@csrf_exempt
def get_equipment(request):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "msg": "Invalid request method"},
            status=405
        )

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse(
            {"success": False, "msg": "Authorization token is required"},
            status=401
        )

    auth_path = auth_header.split()

    if len(auth_path) != 2 or auth_path[0].lower() != "bearer":
        return JsonResponse(
            {"success": False, "msg": "Invalid token format"},
            status=400
        )

    token = AccessToken(auth_path[1])
    user_id = token["user_id"]
    
    

    seller = userRegister.objects(id=user_id).first()
    if not seller:
        return JsonResponse(
            {"success": False, "msg": "Seller not found"},
            status=404
        )


    equipment = Equipment.objects(seller_id=seller)

    if not equipment:
        return JsonResponse(
            {"success": False, "msg": "Equipment not found"},
            status=404
        )

    return JsonResponse({
        "success": True,
        "msg": "Equipment details fetched successfully",
        "data": {
            "equipment": [
                {
                    "id": str(item.id),
                    "seller_id": str(item.seller_id.id),
                    "name_equipment": item.name_equipment,
                    "description": item.description,
                    "brand": item.brand,
                    "model": item.model,
                    "price_per_day": item.price_per_day,
                    "duration": item.duration,
                    "rating": item.rating,
                    "availability_status": item.availability_status,
                    "available_from": item.available_from.isoformat(),
                    "available_to": item.available_to.isoformat(),
                    "created_at": item.created_at.isoformat(), 
                    "updated_at": item.updated_at.isoformat(),
                }
                for item in equipment
            ]
        }
    })
# ----------------------------------------------delete Equipment  api---------------------------------

@csrf_exempt
def delete(request):
    if request.method !="DELETE":
        return JsonResponse({
            "success":False,
            "msg":"invalid request method"
        },status=405)
        
    
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse(
            {"success": False, "msg": "Authorization token is required"},
            status=401
        )

    auth_path = auth_header.split()

    if len(auth_path) != 2 or auth_path[0].lower() != "bearer":
        return JsonResponse(
            {"success": False, "msg": "Invalid token format"},
            status=400
        )

    token = AccessToken(auth_path[1])
    user_id = token["user_id"]
    
    

    seller = userRegister.objects(id=user_id).first()
    if not seller:
        return JsonResponse(
            {"success": False, "msg": "Seller not found"},
            status=404
        )



    data = json.loads(request.body)
    equipment_id = data.get("equipment_id")
    
    if not equipment_id:
        return JsonResponse({
            "success":False,
            "msg":"equipment_id is required"
        },status=400)
        
    Equipment.objects(id=equipment_id,seller_id=seller).delete()
    
    return JsonResponse({
        "success":True,
        "msg":"Equipmet deleted successfully"
    })
        