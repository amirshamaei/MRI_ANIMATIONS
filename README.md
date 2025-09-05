# 3D Bloch Equation Animation for MRI

This project provides a detailed 3D visualization of the Bloch Equations, which are fundamental to understanding Magnetic Resonance Imaging (MRI). The animation is created using the [Manim Community](https://www.manim.community/) Python animation engine.

The simulation visualizes the behavior of the net magnetization vector (M) from its initial tilted equilibrium, through a 90-degree radiofrequency (RF) pulse, and during the subsequent T1 and T2 relaxation processes (Free Induction Decay).

## Features

- **Full 3D Environment:** The scene is rendered in 3D with a continuously rotating camera for a dynamic viewing experience.
- **Physics Simulation:** The animation accurately models:
    - An initial, tilted equilibrium state of the magnetization vector for better visibility.
    - The application of a 90-degree RF pulse that tips the vector into the transverse plane.
    - T1 (longitudinal) and T2 (transverse) relaxation processes, showing the vector's return to equilibrium.
- **Real-time Parameter Display:** On-screen text displays the values of the magnetization components (`Mx`, `My`, `Mz`) and time (`t`) as they evolve.
- **High-Quality Graphics:** Utilizes Manim for smooth animations, crisp text, and clear vector graphics to represent the coordinate system, magnetic field (`B₀`), and magnetization vector (`M`).
- **Configurable Quality:** The script includes a `testing_mode` flag for rapid, low-quality previews and can be rendered in high quality (1080p, 60fps) for final output.

## Dependencies

To run this animation, you will need a Python environment with the following libraries installed:

- **Manim Community:** The core animation engine.
- **NumPy:** For numerical operations.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amirshamaei/MRI_ANIMATIONS.git
    cd MRI_ANIMATIONS
    ```

2.  **Set up a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Manim may have additional system-level dependencies like FFmpeg, LaTeX, etc. Please refer to the official [Manim installation guide](https://docs.manim.community/en/stable/installation.html) for your operating system.)*

## Usage

You can render the animation from your terminal. Ensure your virtual environment is activated.

### High-Quality Render (Final Version)

To generate the final high-quality video (1080p, 60fps), first set `self.testing_mode = False` inside `bloch_improved.py`, then run:

```bash
manim bloch_improved.py ImprovedBlochEquation -pqh
```

### Low-Quality Preview (Fast)

For a quick preview (480p, 15fps), set `self.testing_mode = True` inside the script, then run:

```bash
manim bloch_improved.py ImprovedBlochEquation -pql
```

The rendered video files will be saved in the `media/videos/` directory.

## Customization

You can easily customize the physics and animation parameters at the beginning of the `ImprovedBlochEquation` class in `bloch_improved.py`:

-   **MRI Physics Constants:** Modify `self.B0`, `self.T1`, `self.T2`, etc., to simulate different tissues or field strengths.
-   **Camera:** Change the initial camera orientation (`phi`, `theta`, `distance`) in the `construct` method.
-   **Animation Speed:** Adjust the `total_time` variable in the `show_relaxation_enhanced` method to make the relaxation animation faster or slower.

## License

This project is open-source under the MIT License.
