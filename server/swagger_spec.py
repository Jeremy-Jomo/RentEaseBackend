# swagger_spec.py

def get_swagger_spec():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Rent Ease API",
            "description": "Backend API for property rental management",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/api/health": {
                "get": {
                    "summary": "Health Check",
                    "responses": {
                        "200": {"description": "API is healthy"}
                    }
                }
            },
            "/api/stats": {
                "get": {
                    "tags": ["System"],
                    "summary": "Get System Statistics",
                    "description": "Get total counts of users, properties, and bookings",
                    "responses": {
                        "200": {
                            "description": "Statistics retrieved successfully",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "total_users": {"type": "integer", "example": 150},
                                    "total_properties": {"type": "integer", "example": 75},
                                    "total_bookings": {"type": "integer", "example": 300}
                                }
                            }
                        },
                        "500": {
                            "description": "Internal server error"
                        }
                    }
                }
            },
            "/properties": {
                "get": {
                    "tags": ["Properties"],
                    "summary": "Get All Properties",
                    "description": "Retrieve a list of all rental properties",
                    "responses": {
                        "200": {
                            "description": "List of properties retrieved successfully",
                            "schema": {
                                "type": "array",
                                "items": {"type": "object"}
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Properties"],
                    "summary": "Create New Property",
                    "description": "Add a new rental property to the system",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "required": ["title", "description", "price", "location"],
                                "properties": {
                                    "title": {"type": "string", "example": "Modern Apartment"},
                                    "description": {"type": "string", "example": "A beautiful modern apartment in the city center"},
                                    "price": {"type": "number", "example": 1200.00},
                                    "location": {"type": "string", "example": "Nairobi, Kenya"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Property created successfully"
                        },
                        "400": {
                            "description": "Missing required fields"
                        }
                    }
                }
            },
            "/properties/{property_id}": {
                "get": {
                    "tags": ["Properties"],
                    "summary": "Get Property by ID",
                    "description": "Retrieve details of a specific property",
                    "parameters": [
                        {
                            "name": "property_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                            "description": "ID of the property to retrieve"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Property details retrieved successfully"
                        },
                        "404": {
                            "description": "Property not found"
                        }
                    }
                },
                "put": {
                    "tags": ["Properties"],
                    "summary": "Update Property",
                    "description": "Update details of an existing property",
                    "parameters": [
                        {
                            "name": "property_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                            "description": "ID of the property to update"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "price": {"type": "number"},
                                    "location": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Property updated successfully"
                        },
                        "404": {
                            "description": "Property not found"
                        }
                    }
                },
                "delete": {
                    "tags": ["Properties"],
                    "summary": "Delete Property",
                    "description": "Remove a property from the system",
                    "parameters": [
                        {
                            "name": "property_id",
                            "in": "path",
                            "required": True,
                            "type": "integer",
                            "description": "ID of the property to delete"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Property deleted successfully"
                        },
                        "404": {
                            "description": "Property not found"
                        }
                    }
                }
            },
            "/login": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "User Login",
                    "description": "Authenticate user and return JWT token",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "required": ["email", "password"],
                                "properties": {
                                    "email": {"type": "string", "example": "user@example.com"},
                                    "password": {"type": "string", "example": "password123"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"},
                                    "token": {"type": "string"},
                                    "user": {"type": "object"}
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid email or password"
                        }
                    }
                }
            },
            "/register": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Register New User",
                    "description": "Create a new user account",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "required": ["name", "email", "password", "role"],
                                "properties": {
                                    "name": {"type": "string", "example": "John Doe"},
                                    "email": {"type": "string", "example": "john@example.com"},
                                    "password": {"type": "string", "example": "password123"},
                                    "role": {"type": "string", "example": "tenant", "enum": ["tenant", "landlord"]}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "User registered successfully"
                        },
                        "400": {
                            "description": "Email already registered or missing fields"
                        }
                    }
                }
            }
        },
        "definitions": {
            "Property": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "rent_price": {"type": "number"},
                    "location": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"}
                }
            },
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "role": {"type": "string"}
                }
            }
        }
    }