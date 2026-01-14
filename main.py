import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#Lamus:
"""<"""
    # def pole_elektryczne(t, r):
#     """Zwraca wektor pola E [Ex, Ey, Ez] w danej pozycji r i czasie t."""
#     # Przykład: stałe pole elektryczne skierowane w górę osi Z
#     # E = 0,1 * k
#     return np.array([1.0, 0.0, 0.1])





# def pole_magnetyczne(t, r):
#     """Zwraca wektor pola B [Bx, By, Bz] w danej pozycji r i czasie t."""
#     # Przykład: stałe pole magnetyczne wzdłuż osi Z
#     # B = 1.0 * k
    
#     return np.array([0.0, 1.0, 1.0])

# --- ROZWIĄZANIE RÓWNANIA ---
"""
sol = solve_ivp(
    fun=lambda t, y: rownanie_ruchu(t, y, q, m),
    t_span=t_span,
    y0=y0,
    t_eval=t_eval,
    method='RK45'  # Metoda Runge-Kutta rzędu 4/5 (standardowa)
)
"""

"""x, y, z = sol.y[0], sol.y[1], sol.y[2]"""

""">"""

# metoda Eulera Cromera (działa ciut lepiej niż zwykły euler)
def solver(position, velocity,  mass, charge , evaluation_points):
    #implementacja algorytmu podobnego do algorytmu verlet'a
    position_memeory = [[position[0]],[position[1]],[position[2]]]
    t = evaluation_points[1] - evaluation_points[0]
    
    acceletarion = rownanie_ruchu(velocity, charge, mass)[3:6]

    for iterator in range(1, len(evaluation_points)):
        
        velocity[0] +=  acceletarion[0]*t
        velocity[1] +=  acceletarion[1]*t
        velocity[2] +=  acceletarion[2]*t
        
        zmianawX = position_memeory[0][iterator-1] + velocity[0]*t + 0.5*(acceletarion[0])*t**2
        zmianawY = position_memeory[1][iterator-1] + velocity[1]*t + 0.5*(acceletarion[1])*t**2
        zmianawZ = position_memeory[2][iterator-1] + velocity[2]*t + 0.5*(acceletarion[2])*t**2
        
        position_memeory[0].append(zmianawX)
        position_memeory[1].append(zmianawY)
        position_memeory[2].append(zmianawZ)
        
        acceletarion = rownanie_ruchu(velocity, charge, mass)[3:6]
        
    return position_memeory
    
    


# --- KONFIGURACJA PÓL ---
# pole w naszym problemie jest stałe w przestrzeni i czasie

print("|-- Konfiguracja pól --|")
print("podaj wektor opisujący pole elektryczne E (3 wartości oddzielone spacją): ")
E = np.array(input().split()).astype(float)

print("podaj wektor opisujący pole magnetyczne B (3 wartości oddzielone spacją): ")
B = np.array(input().split()).astype(float)
while( math.sqrt(B[0]**2 + B[1]**2+ B[2]**2) > 10):
    print("Wartość pola magnetycznego jest zbyt duża, podaj wartość mniejszą niż 10 T (długość wektora B < 10): ")
    B = np.array(input().split()).astype(float)



# --- FIZYKA (SIŁA LORENTZA) + siła elektryczna++++ ---
def rownanie_ruchu(velocity, charge, mass):
    """
    Funkcja definiująca układ równań różniczkowych.
    y to wektor stanu: [x, y, z, vx, vy, vz]
    """
    # Rozpakowanie pozycji i prędkości 
    # Pobranie wartości pól w danym punkcie
    # Obliczenie siły F = q(E + v x B)
    # np.cross to iloczyn wektorowy
    F = charge* (E + np.cross(velocity, B))

    # Przyspieszenie a = F / m
    acceleration = F / mass

    # Zwracamy pochodne: [dr/dt, dv/dt] czyli [v, a]
    dydt = np.concatenate((velocity, acceleration))
    return dydt


# --- PARAMETRY SYMULACJI ---
# Jednostki umowne (dla elektronu w realnych jednostkach liczby byłyby bardzo małe)
print("|-- Parametry cząstki --|")
q = float(input("Podaj wartość ładunku cząstki (c): "))  # Ładunek
m = float(input("Podaj wartość masy cząstki (kg): "))  # Masa
pos = np.array(input("Podaj początkową pozycję cząstki (3 wartości oddzielone spacją): ").split()).astype(float)  # Pozycja początkowa
vel = np.array(input("Podaj wektor początkowej prędkości cząstki (3 wartości oddzielone spacją): ").split()).astype(float)  # Prędkość początkowa
czas = float(input("Podaj czas symulacji (s): "))  # Czas symulacji


t_span = (0, czas)  # Czas symulacji od 0 do czasu symulacji
t_eval = np.linspace(t_span[0], t_span[1], 20000)  # Punkty czasowe do zapisu


# --- ROZWIĄZANIE RÓWNANIA RUCHU ---
sol = solver(position=pos, velocity=vel, mass=m, charge=q , evaluation_points=t_eval)

# --- WIZUALIZACJA ---
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Wyciągnięcie współrzędnych z rozwiązania


x,y,z = sol[0], sol[1], sol[2]


ax.plot(x, y, z, label='Tor ruchu cząsteczki', color='b')
ax.scatter(x[0], y[0], z[0], color='g', label='Start')  # Punkt startowy
ax.scatter(x[-1], y[-1], z[-1], color='r', label='Koniec')  # Punkt końcowy

# Opisy osi
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Ruch ładunku w polach E i B\nq={q}, m={m}')
ax.legend()

plt.show()