# src/utils/visualize.py

from celluloid import Camera
import matplotlib.pyplot as plt

#visualize ever step of cellular automata
def visualize_automata(automata, steps, output_path):
    fig, ax = plt.subplots()  # Minimal matplotlib usage
    camera = Camera(fig)

    for i in range(steps):
        automata.update_grid()
        print(f"############   Step{i+1}    ###############\n")
        print(automata.current_grid)
        print("\n########################################\n\n\n\n")
        ax.imshow(automata.current_grid, cmap='viridis')
        ax.axis('off')  # Turn off axis
        camera.snap()

    animation = camera.animate()
    animation.save(output_path, writer='ffmpeg') 

# save final image of cellular automata
def save_final_state(automata, output_path):
    plt.imshow(automata.current_grid, cmap='viridis')
    plt.axis('off')  # Hide the axes
    plt.savefig(output_path)
    plt.close()
