import requests
import webbrowser

BASE_URL = "http://localhost:5000"

while True:
    print("\n--- Menú Cliente API ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Ver tareas (HTML)")
    print("4. Salir")
    opcion = input("Elegí una opción: ").strip()

    if opcion == "1":
        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()
        try:
            res = requests.post(f"{BASE_URL}/registro", json={"usuario": usuario, "contraseña": contraseña})
            print(f"\n[Status {res.status_code}] {res.json()}")
        except requests.exceptions.ConnectionError:
            print("\nError: No me pude conectar al servidor Flask.")

    elif opcion == "2":
        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()
        try:
            res = requests.post(f"{BASE_URL}/login", json={"usuario": usuario, "contraseña": contraseña})
            print(f"\n[Status {res.status_code}] {res.json()}")
        except requests.exceptions.ConnectionError:
            print("\nError: No me pude conectar al servidor Flask.")

    elif opcion == "3":
        print("\nAbriendo la página en el navegador...")
        webbrowser.open(f"{BASE_URL}/tareas")

    elif opcion == "4":
        break
    else:
        print("Opción incorrecta.")