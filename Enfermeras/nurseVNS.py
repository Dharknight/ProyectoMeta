import random
import csv
import copy
import time

# Parámetros del algoritmo VNS
MAX_ITERATIONS = 2500
MAX_NEIGHBORHOODS = 5

# Definir la representación del horario
DAYS = 31  # Número de días de la semana
TIMESLOTS = 4  # Número de turnos (cada turno de 6 horas)
SLOTS = DAYS * TIMESLOTS
process = 0

# Restricciones del problema
nurses = []  # Lista de enfermeras y sus características

# Leer datos desde el archivo CSV
with open('datos.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        nurse = {
            'name': row['Nurses'],
            'atencion_pacientes': int(row['Atencion Pacientes']),
            'conocimiento': int(row['Conocimiento']),
            'disponibilidad_flexibilidad': int(row['Disponibilidad y Flexibilidad'])
        }
        nurses.append(nurse)

# Función de generación de horarios aleatorios
def generate_schedule():
    schedule = [[None] * TIMESLOTS for _ in range(DAYS)]
    assigned_nurses = set()
    nurse_index = 0
    
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            nurse = nurses[nurse_index % len(nurses)]
            schedule[day][timeslot] = nurse['name']
            assigned_nurses.add(nurse['name'])
            nurse_index += 1
    
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

# Función para obtener los movimientos vecinos de un vecindario específico
def get_neighborhood(schedule, neighborhood_size):
    neighborhood = []
    for _ in range(neighborhood_size):
        neighbor = copy.deepcopy(schedule)
        random_day1 = random.randint(0, DAYS - 1)
        random_timeslot1 = random.randint(0, TIMESLOTS - 1)
        random_day2 = random.randint(0, DAYS - 1)
        random_timeslot2 = random.randint(0, TIMESLOTS - 1)
        neighbor[random_day1][random_timeslot1], neighbor[random_day2][random_timeslot2] = \
            neighbor[random_day2][random_timeslot2], neighbor[random_day1][random_timeslot1]
        neighborhood.append(neighbor)
    return neighborhood

# Función para calcular la prioridad de una enfermera
def calculate_priority(nurse):
    atencion_pacientes = nurse['atencion_pacientes']
    conocimiento = nurse['conocimiento']
    disponibilidad_flexibilidad = nurse['disponibilidad_flexibilidad']
    return (atencion_pacientes + conocimiento + disponibilidad_flexibilidad) #/ 3

# Algoritmo de búsqueda Variable Neighborhood Search (VNS) para asignar turnos a enfermeras
def variable_neighborhood_search():
    current_schedule = generate_schedule()
    best_schedule = current_schedule
    current_fitness = evaluate_schedule(current_schedule)
    
    for _ in range(MAX_ITERATIONS):
        neighborhood_size = 1
        while neighborhood_size <= MAX_NEIGHBORHOODS:
            neighborhood = get_neighborhood(current_schedule, neighborhood_size)
            best_neighbor = None
            best_fitness = float('-inf')
            global process
            for neighbor in neighborhood:
                process = process + 1  # contamos 'nodos'
                fitness = evaluate_schedule(neighbor)
                if fitness > best_fitness:
                    best_neighbor = neighbor
                    best_fitness = fitness
            
            if best_neighbor is not None and best_fitness > current_fitness:
                current_schedule = best_neighbor
                current_fitness = best_fitness
                neighborhood_size = 1
            else:
                neighborhood_size += 1
        
        if evaluate_schedule(current_schedule) > evaluate_schedule(best_schedule):
            best_schedule = current_schedule
    
    return best_schedule

# Ordenar las enfermeras por prioridad
nurses = sorted(nurses, key=calculate_priority, reverse=True)

# Main
tiempo_inicio = time.time()
best_schedule = variable_neighborhood_search()
print("Mejor asignación de turnos encontrada:")
for day in range(DAYS):
    for timeslot in range(TIMESLOTS):
        print(f"Día {day+1}, Turno {timeslot+1}: {best_schedule[day][timeslot]}")
tiempo_fin = time.time()
elapsed_time = tiempo_fin - tiempo_inicio

if elapsed_time >= 60:
    minutos = int(elapsed_time / 60)
    segundos = elapsed_time - (minutos * 60)
    print("Tiempo de Ejecución: ", minutos, ":", round(segundos, 3))
    print("Procesamiento: ", process)
else:
    print("Tiempo de Ejecución: ", round(elapsed_time, 3))
    print("Procesamiento: ", process)
