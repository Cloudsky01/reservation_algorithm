import random
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_random_reservations_without_wanted_room(start_time, end_time):
    """
    Generate a list of random reservations without the 'wantedRoom' attribute.
    
    num_reservations: Number of reservations to generate.
    start_time: Start time range for reservations.
    end_time: End time range for reservations.
    """
    start = random.randint(start_time, end_time - 4)
    end = random.randint(start + 1, start + 4)
    reservation = {"start": start, "end": end}
    return reservation

def visualize_solution_plot(reservations: list[Reservation], assignments, num_rooms):
    """
    Visualize the reservation assignments.
    
    reservations: List of reservation dicts with "start" and "end" keys.
    assignments: Result of the optimizer (2D list) where assignments[i][j] == 1 indicates
                 that reservation i is assigned to room j.
    num_rooms: Number of rooms.
    """
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(num_rooms, 10))  # Adjust figsize to match the desired orientation
    ax.set_ylim(max(r.endTime for r in reservations), min(r.startTime for r in reservations))  # Invert y-axis limits for time
    ax.set_xlim(0, num_rooms)  # Set x-axis limits for rooms
    
    ax.set_xlabel('Room')
    ax.set_ylabel('Time')
    ax.set_xticks([i + 0.5 for i in range(num_rooms)])
    ax.set_xticklabels([f'Room {i}' for i in range(num_rooms)], rotation='vertical')
    
    # Loop through each reservation and room, checking assignments
    for i, reservation in enumerate(reservations):
        for j in range(num_rooms):
            if assignments[i][j] == 1:  # If reservation i is assigned to room j
                rect = patches.Rectangle((j, reservation.endTime), 1, reservation.startTime - reservation.endTime, facecolor='blue', edgecolor='black')  # Adjust coordinates
                ax.add_patch(rect)
                ax.text(j + 0.5, (reservation.startTime + reservation.endTime) / 2, reservation.id[0:4], ha='center', va='center', color='white')
                
    plt.tight_layout()
    plt.savefig('schedule_inverted_time.png')  # Save the graph with inverted time axis