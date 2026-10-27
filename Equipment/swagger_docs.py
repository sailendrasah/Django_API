from django.http import HttpResponse, JsonResponse


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Django User API",
        "version": "1.0.0",
        "description": "User registration, authentication, profile, and password endpoints.",
    },
    "security": [{"BearerAuth": []}],
    "tags": [
        {"name": "auth"},
        {"name": "equipment", "description": "Equipment listing endpoints."},
    ],
    "paths": {
        "/register/": {
            "post": {
                "operationId": "registerUser",
                "summary": "Register a user",
                "tags": ["auth"],
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RegisterRequest"}
                        }
                    },
                },
                "responses": {
                    "201": {"description": "User registered"},
                    "400": {"description": "Required field missing or email already exists"},
                },
            }
        },
        "/verify_otp/": {
            "post": {
                "operationId": "verifyOtp",
                "summary": "Verify a user's OTP",
                "tags": ["auth"],
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/OtpRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {"description": "OTP verified"},
                    "400": {"description": "Invalid OTP or user already verified"},
                    "404": {"description": "User not found"},
                },
            }
        },
        "/login/": {
            "post": {
                "operationId": "loginUser",
                "summary": "Log in and obtain JWT tokens",
                "tags": ["auth"],
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Login successful; returns access and refresh tokens"},
                    "401": {"description": "Invalid credentials"},
                    "403": {"description": "Email verification required"},
                },
            }
        },
        "/get_user/": {
            "get": {
                "operationId": "getUser",
                "summary": "Get the authenticated user's profile",
                "tags": ["auth"],
                "responses": {
                    "200": {"description": "User profile"},
                    "401": {"description": "Missing, invalid, or expired access token"},
                    "404": {"description": "User not found"},
                },
            }
        },
        "/update_user/": {
            "put": {
                "operationId": "updateUser",
                "summary": "Update a user by email",
                "tags": ["auth"],
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UpdateUserRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {"description": "User updated"},
                    "400": {"description": "Email is required"},
                    "404": {"description": "User not found"},
                },
            }
        },
        "/froget_password/": {
            "post": {
                "operationId": "requestPasswordReset",
                "summary": "Generate a password-reset OTP",
                "tags": ["auth"],
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/EmailRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {"description": "OTP generated"},
                    "400": {"description": "Email is missing or not found"},
                },
            }
        },
        "/rest_paswword/": {
            "post": {
                "operationId": "resetPassword",
                "summary": "Reset password using an OTP",
                "tags": ["auth"],
                "security": [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ResetPasswordRequest"}
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Password reset"},
                    "400": {"description": "Missing fields, unknown email, or invalid OTP"},
                },
            }
        },
        "/delete/": {
            "delete": {
                "operationId": "deleteEquipment",
                "summary": "Delete equipment owned by the authenticated seller",
                "tags": ["equipment"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/EquipmentDeleteRequest"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Equipment deleted"},
                    "400": {"description": "Equipment ID is required or token format is invalid"},
                    "401": {"description": "Missing or invalid bearer token"},
                    "404": {"description": "Seller not found"},
                    "405": {"description": "Invalid request method"},
                },
            }
        },
        "/equipment_register/": {
            "post": {
                "operationId": "registerEquipment",
                "summary": "Register equipment for the authenticated seller",
                "tags": ["equipment"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/EquipmentRegisterRequest"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {"description": "Equipment registered"},
                    "400": {"description": "Invalid request or equipment details"},
                    "401": {"description": "Missing or invalid bearer token"},
                    "404": {"description": "Seller not found"},
                },
            }
        },
        "/Equipment_update/": {
            "put": {
                "operationId": "updateEquipment",
                "summary": "Update equipment owned by the authenticated seller",
                "tags": ["equipment"],
                "security": [{"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/EquipmentUpdateRequest"
                            },
                            "example": {
                                "equipment_id": "507f1f77bcf86cd799439011",
                                "name_equipment": "Updated equipment name",
                                "available_from": "2026-10-12",
                                "available_to": "2026-10-20",
                            },
                        }
                    },
                },
                "responses": {
                    "200": {"description": "Equipment updated"},
                    "400": {"description": "Invalid request or date range"},
                    "401": {"description": "Missing or invalid bearer token"},
                    "404": {"description": "Seller or equipment not found"},
                    "405": {"description": "Invalid request method"},
                },
            }
        },
        "/get_equipment/": {
            "get": {
                "operationId": "getEquipment",
                "summary": "Get all equipment",
                "tags": ["equipment"],
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {"description": "Equipment list fetched; data is an array"},
                    "401": {"description": "Missing or invalid bearer token"},
                    "405": {"description": "Invalid request method"},
                },
            }
        },
    },
    "components": {
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        },
        "schemas": {
            "RegisterRequest": {
                "type": "object",
                "required": ["name", "email", "phone", "role", "password"],
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "phone": {"type": "string"},
                    "role": {
                        "type": "string",
                        "enum": ["USER", "EQUIPMENT_OWNER"],
                    },
                    "password": {"type": "string", "format": "password"},
                },
            },
            "LoginRequest": {
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string", "format": "password"},
                },
            },
            "EmailRequest": {
                "type": "object",
                "required": ["email"],
                "properties": {"email": {"type": "string", "format": "email"}},
            },
            "OtpRequest": {
                "type": "object",
                "required": ["email", "otp"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "otp": {"type": "integer", "minimum": 100000, "maximum": 999999},
                },
            },
            "ResetPasswordRequest": {
                "type": "object",
                "required": ["email", "otp", "password"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "otp": {"type": "integer", "minimum": 100000, "maximum": 999999},
                    "password": {"type": "string", "format": "password"},
                },
            },
            "UpdateUserRequest": {
                "type": "object",
                "required": ["email"],
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "name": {"type": "string"},
                    "password": {"type": "string", "format": "password"},
                    "otp": {"type": "integer"},
                    "is_verified": {"type": "boolean"},
                },
            },
            "EquipmentRegisterRequest": {
                "type": "object",
                "required": [
                    "name_equipment",
                    "description",
                    "brand",
                    "model",
                    "duration",
                    "price_per_day",
                    "avaliable_from",
                    "available_to",
                ],
                "properties": {
                    "name_equipment": {"type": "string"},
                    "description": {"type": "string"},
                    "brand": {"type": "string"},
                    "model": {"type": "string"},
                    "duration": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["AVAILABLE", "BOOKED", "UNAVAILABLE"],
                    },
                    "price_per_day": {"type": "number", "format": "decimal"},
                    "avaliable_from": {"type": "string", "format": "date"},
                    "available_to": {"type": "string", "format": "date"},
                },
            },
            "EquipmentUpdateRequest": {
                "type": "object",
                "required": ["equipment_id"],
                "properties": {
                    "equipment_id": {"type": "string"},
                    "name_equipment": {"type": "string"},
                    "description": {"type": "string"},
                    "brand": {"type": "string"},
                    "model": {"type": "string"},
                    "duration": {"type": "string"},
                    "price_per_day": {"type": "number", "format": "decimal"},
                    "available_from": {"type": "string", "format": "date"},
                    "available_to": {"type": "string", "format": "date"},
                },
            },
            "EquipmentDeleteRequest": {
                "type": "object",
                "required": ["equipment_id"],
                "properties": {"equipment_id": {"type": "string"}},
            },
        },
    },
}


def openapi_json(request):
    return JsonResponse(OPENAPI_SPEC)


def swagger_ui(request):
    html = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Django User API - Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger-ui" });
    </script>
  </body>
</html>"""
    return HttpResponse(html)
