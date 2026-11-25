from router_store import add_router, get_routers, search_router

print("TEST 1: Adding a router")
print(add_router("Router_01", "192.168.1.1", 8080))

print("\nTEST 2: Trying to add the same router again")
print(add_router("Router_01", "192.168.1.5", 8081))

print("\nTEST 3: Displaying all routers")
print(get_routers())

print("\nTEST 4: Searching for Router_01")
print(search_router("Router_01"))

print("\nTEST 5: Testing an invalid IP address")
print(add_router("Router_02", "999.999.1.1", 8080))