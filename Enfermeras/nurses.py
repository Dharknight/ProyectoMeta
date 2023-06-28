import random
import csv
import copy

# Parámetros del algoritmo Tabú
MAX_ITERATIONS = 100
TABU_TENURE = 10

# Definir la representación del horario
DAYS = 5  # Número de días de la semana
TIMESLOTS = 4  # Número de turnos (cada turno de 6 horas)
SLOTS = DAYS * TIMESLOTS

# Restricciones del problema
nurses = []  # Lista de enfermeras

# Leer datos desde el archivo CSV
with open('datos.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == 'Nurses':
            nurses = row[1:]

# Función de generación de horarios aleatorios
def generate_schedule():
    schedule = [[None] * TIMESLOTS for _ in range(DAYS)]
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            nurse = random.choice(nurses)
            schedule[day][timeslot] = nurse
    return schedule

# Función de evaluación de horarios
def evaluate_schedule(schedule):
    fitness = 0
    
    # Restricción: Asignación de un solo turno por día a cada enfermera
    for day in range(DAYS):
        nurse_counts = {}
        for timeslot in range(TIMESLOTS):
            nurse = schedule[day][timeslot]
            if nurse in nurse_counts:
                nurse_counts[nurse] += 1
                fitness -= 1  # Penalización por asignar más de un turno a la misma enfermera en un día
            else:
                nurse_counts[nurse] = 1
    
    # Otras restricciones y objetivos pueden implementarse aquí
    return fitness

# Función para obtener los movimientos vecinos
def get_neighborhood(schedule):
    neighborhood = []
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            for new_day in range(DAYS):
                for new_timeslot in range(TIMESLOTS):
                    if new_day != day or new_timeslot != timeslot:
                        neighbor = copy.deepcopy(schedule)
                        neighbor[day][timeslot], neighbor[new_day][new_timeslot] = neighbor[new_day][new_timeslot], neighbor[day][timeslot]
                        neighborhood.append(neighbor)
    return neighborhood

# Algoritmo de búsqueda Tabú para asignar turnos a enfermeras
def tabu_search():
    current_schedule = generate_schedule()
    best_schedule = current_schedule
    tabu_list = []
    
    for _ in range(MAX_ITERATIONS):
        neighborhood = get_neighborhood(current_schedule)
        best_neighbor = None
        best_fitness = float('-inf')
        
        for neighbor in neighborhood:
            if neighbor not in tabu_list:
                fitness = evaluate_schedule(neighbor)
                if fitness > best_fitness:
                    best_neighbor = neighbor
                    best_fitness = fitness
        
        if best_neighbor is None:
            break
        
        current_schedule = best_neighbor
        if evaluate_schedule(current_schedule) > evaluate_schedule(best_schedule):
            best_schedule = current_schedule
        
        tabu_list.append(current_schedule)
        if len(tabu_list) > TABU_TENURE:
            tabu_list.pop(0)
    
    return best_schedule

# Ejemplo de uso
best_schedule = tabu_search()
print("Mejor asignación de turnos encontrada:")
for day in range(DAYS):
    for timeslot in range(TIMESLOTS):
        print(f"Día {day+1}, Turno {timeslot+1}: {best_schedule[day][timeslot]}")