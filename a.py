import random
import copy

# Parámetros del algoritmo Tabú
MAX_ITERATIONS = 100
TABU_TENURE = 10

# Definir la representación del horario
DAYS = 5  # Número de días de la semana
TIMESLOTS = 8  # Número de franjas horarias
SLOTS = DAYS * TIMESLOTS

# Restricciones del problema
professors = ["Profesor1", "Profesor2", "Profesor3"]  # Lista de profesores
subjects = ["Asignatura1", "Asignatura2", "Asignatura3"]  # Lista de asignaturas
rooms = ["Aula1", "Aula2", "Aula3"]  # Lista de salones

# Función de generación de horarios aleatorios
def generate_schedule():
    schedule = [[None] * TIMESLOTS for _ in range(DAYS)]
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            professor = random.choice(professors)
            subject = random.choice(subjects)
            room = random.choice(rooms)
            schedule[day][timeslot] = (professor, subject, room)
    return schedule

# Función de evaluación de horarios
def evaluate_schedule(schedule):
    fitness = 0
    
    # Restricción: Solapamiento de asignaturas
    subjects_slots = {}
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            subject = schedule[day][timeslot][1]
            if subject in subjects_slots:
                fitness -= 1  # Penalización por solapamiento de asignaturas
            else:
                subjects_slots[subject] = (day, timeslot)
    
    # Restricción: Preferencias de profesores
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            professor = schedule[day][timeslot][0]
            subject = schedule[day][timeslot][1]
            # Implementa tu lógica para verificar las preferencias de profesores y asigna puntos en consecuencia
            
    # Restricción: Disponibilidad de salones
    for day in range(DAYS):
        for timeslot in range(TIMESLOTS):
            room = schedule[day][timeslot][2]
            # Implementa tu lógica para verificar la disponibilidad de salones y asigna puntos en consecuencia
    
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

# Algoritmo de búsqueda Tabú para generar horarios
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
print("Mejor horario encontrado:")
for day in range(DAYS):
    for timeslot in range(TIMESLOTS):
        print(f"Día {day+1}, Franja Horaria {timeslot+1}: {best_schedule[day][timeslot]}")
