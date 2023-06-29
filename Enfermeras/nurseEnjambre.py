import time
import csv
import copy
import random

# Parámetros del algoritmo de enjambre de partículas
PARTICLE_COUNT = 10
MAX_ITERATIONS = 100
COGNITIVE_WEIGHT = 1.0
SOCIAL_WEIGHT = 2.0
INERTIA_WEIGHT = 0.8
process = 0 
# Definir la representación del horario
DAYS = 14
TIMESLOTS = 4
SLOTS = DAYS * TIMESLOTS

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

# Mapeo de enfermeras a valores numéricos y viceversa
nurse_mapping = {i: nurse['name'] for i, nurse in enumerate(nurses)}
inverse_nurse_mapping = {nurse['name']: i for i, nurse in enumerate(nurses)}

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

# Función para evaluar la aptitud de una asignación de horarios
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

# Función para calcular la prioridad de una enfermera
def calculate_priority(nurse):
    atencion_pacientes = nurse['atencion_pacientes']
    conocimiento = nurse['conocimiento']
    disponibilidad_flexibilidad = nurse['disponibilidad_flexibilidad']
    return (atencion_pacientes + conocimiento + disponibilidad_flexibilidad) / 3

# Algoritmo de enjambre de partículas para asignar turnos a enfermeras
def particle_swarm_optimization():
    particles = []
    best_particle = None
    best_fitness = float('-inf')
    global process
    for _ in range(PARTICLE_COUNT):
        process = process + 1
        particle = {
            'position': generate_schedule(),
            'velocity': [[0] * TIMESLOTS for _ in range(DAYS)],
            'best_position': None,
            'best_fitness': None
        }
        particle['best_position'] = particle['position']
        particle['best_fitness'] = evaluate_schedule(particle['position'])
        
        particles.append(particle)
        
        if particle['best_fitness'] > best_fitness:
            best_particle = particle
            best_fitness = particle['best_fitness']
    
    for _ in range(MAX_ITERATIONS):
        for particle in particles:
            neighborhood = get_neighborhood(particle['position'])
            best_neighbor = None
            best_fitness = float('-inf')
            
            for neighbor in neighborhood:
                process = process + 1 
                fitness = evaluate_schedule(neighbor)
                if fitness > best_fitness:
                    best_neighbor = neighbor
                    best_fitness = fitness
            
            if best_neighbor is not None:
                particle['position'] = best_neighbor
            
            if evaluate_schedule(particle['position']) > evaluate_schedule(particle['best_position']):
                particle['best_position'] = particle['position']
            
            if evaluate_schedule(particle['position']) > evaluate_schedule(best_particle['position']):
                best_particle = particle
        
        for particle in particles:
            for day in range(DAYS):
                for timeslot in range(TIMESLOTS):
                    process = process + 1 
                    inertia_term = INERTIA_WEIGHT * particle['velocity'][day][timeslot]
                    cognitive_term = COGNITIVE_WEIGHT * random.random() * int(particle['best_position'][day][timeslot] != particle['position'][day][timeslot])
                    social_term = SOCIAL_WEIGHT * random.random() * int(best_particle['position'][day][timeslot] != particle['position'][day][timeslot])
                    particle['velocity'][day][timeslot] = inertia_term + cognitive_term + social_term
                    nurse_index = inverse_nurse_mapping[particle['position'][day][timeslot]]
                    particle['position'][day][timeslot] = nurse_mapping[(nurse_index + int(particle['velocity'][day][timeslot])) % len(nurses)]
        
    return best_particle['position']

# Ordenar las enfermeras por prioridad
nurses = sorted(nurses, key=calculate_priority, reverse=True)

tiempo_inicio = time.time()
best_schedule = particle_swarm_optimization()
print("Mejor asignación de turnos encontrada:")
for day in range(DAYS):
    for timeslot in range(TIMESLOTS):
        nurse_id = inverse_nurse_mapping[best_schedule[day][timeslot]]
        nurse_name = nurse_mapping[nurse_id]
        print(f"Día {day+1}, Turno {timeslot+1}: {nurse_name}")
tiempo_fin = time.time() 
time = tiempo_fin - tiempo_inicio

if time >= 60:
    minutos = time/60
    segundos = time - minutos * 60
    print("Tiempo de Ejecucion: ", minutos , ":",round(segundos,3))
    print("Procesamiento: ", process)
else: 
    print("Tiempo de Eejecucion: ", round(time,3))
    print("Procesamiento:", process)

