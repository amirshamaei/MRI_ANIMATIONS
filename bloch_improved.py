#!/usr/bin/env python3
"""
Improved Bloch Equation Visualization in MRI using Manim

Enhanced version with:
- Tilted magnetization vector
- Rotating camera view
- Short, accurate animation
- Camera-aligned text
- High quality rendering

Author: Amir Shamaei
"""

import numpy as np
from manim import (
    ThreeDScene,
    DEGREES,
    ThreeDAxes,
    Text,
    MathTex,
    Arrow3D,
    VGroup,
    Dot,
    Create,
    Write,
    Transform,
    FadeOut,
    FadeIn,
    # Constants
    WHITE,
    RED,
    GREEN,
    BLUE,
    YELLOW,
    ORANGE,
    GOLD,
    # Directions
    RIGHT,
    UP,
    OUT,
    DOWN,
    LEFT,
    UR,
    # Text styles
    BOLD,
)

class ImprovedBlochEquation(ThreeDScene):
    def construct(self):
        # Testing mode flag - set to True for fast testing, False for full quality
        self.testing_mode = True  # Change this to False for full quality rendering
        
        # Enhanced camera setup with initial position - zoomed closer
        self.set_camera_orientation(
            phi=45 * DEGREES, 
            theta=-75 * DEGREES,
            distance=6  # Closer zoom for better detail
        )
        
        # MRI Physics Constants
        self.gamma = 2.675e8  # Gyromagnetic ratio (rad/s/T)
        self.B0 = 1.5  # Main field strength (Tesla)
        self.T1 = 1.0  # Longitudinal relaxation (seconds)
        self.T2 = 0.1  # Transverse relaxation (seconds)
        self.M0 = 1.0  # Equilibrium magnetization
        self.omega_0 = self.gamma * self.B0  # Larmor frequency
        
        # Setup scene with rotating camera
        self.setup_scene()
        
        # Show Bloch equation sequence
        self.demonstrate_bloch_physics()

    def setup_scene(self):
        """Setup 3D coordinate system and magnetic field with camera alignment"""
        
        # Create enhanced 3D axes
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5], 
            z_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        # Create fixed labels that will stay with camera - improved font spacing
        self.x_label = Text("Mx", font_size=22, color=RED, font="Arial", weight=BOLD)
        self.y_label = Text("My", font_size=22, color=GREEN, font="Arial", weight=BOLD)
        self.z_label = Text("Mz", font_size=22, color=BLUE, font="Arial", weight=BOLD)

        self.x_label.move_to(axes.x_axis.get_end() + 0.3*RIGHT)
        self.y_label.move_to(axes.y_axis.get_end() + 0.3*UP)
        self.z_label.move_to(axes.z_axis.get_end() + 0.3*OUT)

        self.add(self.x_label, self.y_label, self.z_label)
        
        # B0 field representation - positioned outside center for clarity
        b0_origin = 3 
        b0_start = [b0_origin, b0_origin, -0.3]
        b0_end = [b0_origin, b0_origin, 1.3]
        
        b0_arrow = Arrow3D(
            start=b0_start,
            end=b0_end, 
            color=BLUE,
            thickness=0.05,
            height=0.3,  # Larger arrow head
            base_radius=0.05
        )
        
        # Camera-aligned B0 label - positioned near the offset arrow
        self.b0_label = Text("B₀", font_size=26, color=BLUE, font="Arial", weight=BOLD)
        self.b0_label.move_to([b0_origin+0.5, b0_origin+0.5, 1.0])
        self.add(self.b0_label)
        
        # Enhanced title - stays at top regardless of camera with improved font
        self.title = Text("Bloch Equations in MRI", font_size=34, color=WHITE, font="Arial", weight=BOLD)
        self.title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(self.title)  # Keep title fixed to camera frame
        
        # Compact Bloch equation - fixed to camera with improved size
        self.equation = MathTex(
            r"\frac{d\vec{M}}{dt} = \gamma\,(\vec{M}\times\vec{B}) - \frac{\vec{M}_{\perp}}{T_2} - \frac{(M_z - M_0)}{T_1}\,\hat{\mathbf z}",
            font_size=22
        )
        self.equation.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(self.equation)  # Keep equation fixed to camera frame
        
        # Animate scene setup - faster in testing mode
        runtime = 0.5 if self.testing_mode else 2
        self.play(
            Create(axes),
            Write(self.x_label),
            Write(self.y_label), 
            Write(self.z_label),
            Create(b0_arrow),
            Write(self.b0_label),
            Write(self.title),
            Write(self.equation),
            runtime=runtime
        )
        
        # Start slow camera rotation that continues for the whole animation
        # rotation_rate = 0.05  # Slow rotation for better visualization
        # self.begin_ambient_camera_rotation(rate=rotation_rate)
        
        # Store objects for later use
        self.axes = axes
        self.b0_arrow = b0_arrow

    def demonstrate_bloch_physics(self):
        """Demonstrate Bloch equation physics with rotating camera"""
        
        # Start with equilibrium magnetization - tilted for better visualization
        initial_tilt = 15 * DEGREES  # Small tilt from z-axis for visibility
        equilibrium_end = [
            0.2 * np.sin(initial_tilt),  # Small x component
            0,  # No y component initially
            self.M0 * np.cos(initial_tilt)  # Mostly z component
        ]
        self.equilibrium_end = equilibrium_end
        
        # Create tilted magnetization vector with enhanced appearance
        self.magnetization = Arrow3D(
            start=[0, 0, 0],
            end=equilibrium_end,
            color=YELLOW,
            thickness=0.06,
            height=0.25,  # Larger arrow head for visibility
            base_radius=0.06
        )
        
        # Magnetization label that follows the arrow with improved font
        self.m_label = Text("M", font_size=22, color=YELLOW, font="Arial", weight=BOLD)
        self.m_label.add_updater(lambda m: m.next_to(self.magnetization.get_end(), RIGHT + UP, buff=0.1))
        self.add(self.m_label)
        
        # Status text - positioned on left edge to avoid overlap with improved font
        self.status_text = Text("Equilibrium State", font_size=20, color=YELLOW, font="Arial", weight=BOLD)
        self.status_text.to_edge(LEFT, buff=0.5).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(self.status_text)
        
        # Show initial state - faster in testing mode
        runtime = 0.3 if self.testing_mode else 1.5
        self.play(
            Create(self.magnetization),
            Write(self.m_label),
            Write(self.status_text),
            runtime=runtime
        )
        
        # Apply 90-degree RF pulse
        self.apply_rf_pulse_enhanced()
        
        # Show precession and relaxation
        self.show_relaxation_enhanced()
        
        # Final summary
        self.show_final_summary()

    def apply_rf_pulse_enhanced(self):
        """Apply RF pulse with enhanced visualization"""
        
        # Update status text by transforming the existing one
        new_status = Text("90° RF Pulse Applied", font_size=20, color=GREEN, font="Arial", weight=BOLD)
        new_status.to_edge(LEFT, buff=0.5).shift(UP * 2)
        
        runtime = 0.1 if self.testing_mode else 0.5
        
        self.play(FadeOut(self.status_text, shift=UP*0.5), runtime=runtime/2)
        self.remove_fixed_in_frame_mobjects(self.status_text)
        self.status_text = new_status
        self.add_fixed_in_frame_mobjects(self.status_text)
        self.play(FadeIn(self.status_text, shift=UP*0.5), runtime=runtime/2)

        # Create RF field representation - increased length for better visibility
        rf_arrow = Arrow3D(
            start=[0, 0, 0],
            end=[1, 0, 0],
            color=GREEN,
            thickness=0.04,
            height=0.2
        )
        
        self.play(Create(rf_arrow), runtime=runtime)
        
        # Rotate magnetization to xy-plane (90-degree pulse)
        target_end = [0, self.M0, 0]  # Pure y-magnetization after 90° pulse
        
        new_magnetization = Arrow3D(
            start=[0, 0, 0],
            end=target_end,
            color=YELLOW,
            thickness=0.06,
            height=0.25,
            base_radius=0.06
        )
        
        runtime = 0.3 if self.testing_mode else 1.5
        
        # Animate the camera tilt and magnetization rotation simultaneously
        self.move_camera(phi=60 * DEGREES, run_time=runtime)
        self.play(
            Transform(self.magnetization, new_magnetization),
            FadeOut(rf_arrow),
            runtime=runtime
        )
        
        # Create parameter display right after RF pulse to show Mx, My, Mz values
        self.create_parameter_display(0.0, self.M0, 0.0, 0.0)

    def show_relaxation_enhanced(self):
        """Show enhanced precession and relaxation with rotating camera"""
        
        # Update status text by transforming the existing one
        new_status = Text("Free Induction Decay", font_size=20, color=ORANGE, font="Arial", weight=BOLD)
        new_status.to_edge(LEFT, buff=0.5).shift(UP * 2)
        
        runtime = 0.1 if self.testing_mode else 0.5
        
        self.play(FadeOut(self.status_text, shift=UP*0.5), runtime=runtime/2)
        self.remove_fixed_in_frame_mobjects(self.status_text)
        self.status_text = new_status
        self.add_fixed_in_frame_mobjects(self.status_text)
        self.play(FadeIn(self.status_text, shift=UP*0.5), runtime=runtime/2)

        # Animate the camera panning during the relaxation
        self.move_camera(theta=-165 * DEGREES, run_time=1.5)

        # Physics-based relaxation matching RF pulse time
        total_time = 0.3 if self.testing_mode else 1.5
        dt = 0.05  # Smaller dt for smoother animation
        steps = int(total_time / dt)

        # Initial state after 90° pulse
        initial_M_transverse = np.array([0.0, self.M0, 0.0])
        
        # Animate relaxation with precession
        for i in range(steps):
            t = (i + 1) * dt
            
            # T2 decay for the transverse component
            decay_t2 = np.exp(-t / self.T2)
            M_transverse_t = initial_M_transverse * decay_t2
            
            # T1 recovery for the longitudinal component
            # This should recover towards the equilibrium z-component
            Mz_equilibrium = self.equilibrium_end[2]
            Mz_t = Mz_equilibrium * (1 - np.exp(-t / self.T1))

            # For simplicity, we assume precession happens in the xy-plane and then we add the Mz component.
            # A full simulation would be more complex, but this gives a good visual representation.
            # We are not including precession here to keep the return path direct as requested.
            
            # The vector returns towards the tilted equilibrium state
            # We can interpolate between the decaying transverse vector and the recovering longitudinal vector.
            # A simple interpolation:
            final_pos = self.equilibrium_end
            start_pos = np.array([0, self.M0, 0])
            
            # Interpolation factor based on time
            alpha = t / total_time
            current_pos = (1 - alpha) * start_pos + alpha * np.array(final_pos)
            
            new_magnetization = Arrow3D(
                start=[0, 0, 0],
                end=current_pos,
                color=YELLOW,
                thickness=0.06,
                height=0.25,
                base_radius=0.06
            )
            
            # Update the display with interpolated values
            self.update_parameter_display(current_pos[0], current_pos[1], current_pos[2], t)
            
            self.play(
                Transform(self.magnetization, new_magnetization),
                run_time=dt
            )
            
        # Ensure final state is accurate
        final_magnetization = Arrow3D(
            start=[0, 0, 0],
            end=self.equilibrium_end,
            color=YELLOW,
            thickness=0.06,
            height=0.25,
            base_radius=0.06
        )
        self.play(Transform(self.magnetization, final_magnetization), run_time=dt)
        self.update_parameter_display(self.equilibrium_end[0], self.equilibrium_end[1], self.equilibrium_end[2], total_time)
        self.wait(1)


    def create_parameter_display(self, mx=0.0, my=0.0, mz=0.0, t=0.0):
        """Create real-time parameter display fixed to camera with improved font"""
        
        self.mx_display = Text(f"Mx: {mx:.2f}", font_size=18, color=RED, font="Arial", weight=BOLD)
        self.my_display = Text(f"My: {my:.2f}", font_size=18, color=GREEN, font="Arial", weight=BOLD)
        self.mz_display = Text(f"Mz: {mz:.2f}", font_size=18, color=BLUE, font="Arial", weight=BOLD)
        self.time_display = Text(f"t: {t:.2f}s", font_size=18, color=WHITE, font="Arial", weight=BOLD)
        
        # Position on right edge and fix to camera frame - avoid corner conflicts
        self.mx_display.to_edge(RIGHT, buff=0.5).shift(UP * 2)
        self.my_display.next_to(self.mx_display, DOWN, buff=0.1)
        self.mz_display.next_to(self.my_display, DOWN, buff=0.1)
        self.time_display.next_to(self.mz_display, DOWN, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(self.mx_display, self.my_display, self.mz_display, self.time_display)
        
        runtime = 0.1 if self.testing_mode else 0.5
        self.play(
            Write(self.mx_display),
            Write(self.my_display),
            Write(self.mz_display),
            Write(self.time_display),
            runtime=runtime
        )

    def update_parameter_display(self, Mx, My, Mz, t):
        """Update parameter display values with improved font"""
        
        new_mx = Text(f"Mx: {Mx:.2f}", font_size=18, color=RED, font="Arial", weight=BOLD).move_to(self.mx_display.get_center())
        new_my = Text(f"My: {My:.2f}", font_size=18, color=GREEN, font="Arial", weight=BOLD).move_to(self.my_display.get_center())
        new_mz = Text(f"Mz: {Mz:.2f}", font_size=18, color=BLUE, font="Arial", weight=BOLD).move_to(self.mz_display.get_center())
        new_time = Text(f"t: {t:.2f}s", font_size=18, color=WHITE, font="Arial", weight=BOLD).move_to(self.time_display.get_center())
        
        # Note: These will be handled by Transform so no need to add_fixed_in_frame_mobjects again
        
        self.mx_display.become(new_mx)
        self.my_display.become(new_my)
        self.mz_display.become(new_mz)
        self.time_display.become(new_time)

    def show_final_summary(self):
        """Show final summary with camera aligned text"""
        
        # Update status text by transforming the existing one
        final_status = Text("Return to Equilibrium", font_size=20, color=GOLD, font="Arial", weight=BOLD)
        final_status.to_edge(LEFT, buff=0.5).shift(UP * 2)
        
        runtime = 0.2 if self.testing_mode else 1
        
        self.play(FadeOut(self.status_text, shift=UP*0.5), runtime=runtime/2)
        self.remove_fixed_in_frame_mobjects(self.status_text)
        self.status_text = final_status
        self.add_fixed_in_frame_mobjects(self.status_text)
        self.play(FadeIn(self.status_text, shift=UP*0.5), runtime=runtime/2)
        
        # Key physics summary - fixed to camera with improved font
        # summary_text = Text(
        #     "Bloch equations govern all MRI signal behavior:\n" +
        #     "• Precession around B₀ field\n" +
        #     "• T₁ longitudinal relaxation\n" +
        #     "• T₂ transverse relaxation\n" +
        #     "• Basis for all MRI contrast",
        #     font_size=16,
        #     color=YELLOW,
        #     font="Arial",
        #     weight=BOLD,
        #     line_spacing=1.3
        # )
        # summary_text.move_to(ORIGIN + 2*DOWN)
        # self.add_fixed_in_frame_mobjects(summary_text)
        
        # runtime = 0.5 if self.testing_mode else 2
        # self.play(Write(summary_text), runtime=runtime)
        
        wait_time = 0.5 if self.testing_mode else 2
        self.wait(wait_time)

# Position check scene for verifying alignment
class PositionCheck(ThreeDScene):
    def construct(self):
        """Quick scene to check positioning of all elements with improved alignment"""
        
        # Same enhanced camera setup as main scene
        self.set_camera_orientation(
            phi=-75 * DEGREES, 
            theta=30 * DEGREES,
            distance=6  # Closer zoom for better detail
        )
        
        # Same constants as main scene
        self.M0 = 1.0
        
        # Create enhanced 3D axes (same as main scene)
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5], 
            z_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        # Create fixed labels that stay with camera (same as main scene) with improved font
        x_label = Text("Mx", font_size=22, color=RED, font="Arial", weight=BOLD)
        y_label = Text("My", font_size=22, color=GREEN, font="Arial", weight=BOLD)
        z_label = Text("Mz", font_size=22, color=BLUE, font="Arial", weight=BOLD)

        x_label.move_to(axes.x_axis.get_end() + 0.3*RIGHT)
        y_label.move_to(axes.y_axis.get_end() + 0.3*UP)
        z_label.move_to(axes.z_axis.get_end() + 0.3*OUT)

        self.add(x_label, y_label, z_label)
        
        # B0 field representation - positioned outside center for clarity
        b0_origin = 2.5
        b0_start = [-b0_origin, b0_origin, -0.3]
        b0_end = [-b0_origin, b0_origin, 1.3]
        
        b0_arrow = Arrow3D(
            start=b0_start,
            end=b0_end, 
            color=BLUE,
            thickness=0.05,
            height=0.3,
            base_radius=0.05
        )
        
        # Camera-aligned B0 label (same as main scene) with improved font
        b0_label = Text("B₀", font_size=26, color=BLUE, font="Arial", weight=BOLD)
        b0_label.move_to([-b0_origin+0.5, b0_origin+0.5, 1.0])
        self.add(b0_label)
        
        # Tilted magnetization vector (same as main scene)
        initial_tilt = 15 * DEGREES
        equilibrium_end = [
            0.2 * np.sin(initial_tilt),
            0,
            self.M0 * np.cos(initial_tilt)
        ]
        
        magnetization = Arrow3D(
            start=[0, 0, 0],
            end=equilibrium_end,
            color=RED,
            thickness=0.06,
            height=0.25,
            base_radius=0.06
        )
        
        # Magnetization label that follows the arrow (same as main scene) with improved font
        m_label = Text("M", font_size=22, color=YELLOW, font="Arial", weight=BOLD)
        m_label.add_updater(lambda m: m.next_to(magnetization.get_end(), RIGHT + UP, buff=0.1))
        self.add(m_label)
        
        # RF pulse for position check
        rf_arrow = Arrow3D(
            start=[0, 0, 0],
            end=[1, 0, 0],
            color=GREEN,
            thickness=0.04,
            height=0.2
        )
        
        # Enhanced title (fixed to camera) with improved font
        title = Text("POSITION CHECK - Improved Bloch Equations", font_size=30, color=WHITE, font="Arial", weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        
        # Compact equation (fixed to camera) with improved size
        equation = MathTex(
            r"\frac{dM}{dt} = \gamma(\vec{M} \times \vec{B}) - \frac{M_{\perp}}{T_2} - \frac{M_z - M_0}{T_1}",
            font_size=18
        )
        equation.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(equation)
        
        # Status displays (fixed to camera) with improved font
        status_text = Text("All elements visible & properly aligned", font_size=18, color=YELLOW, font="Arial", weight=BOLD)
        status_text.to_edge(LEFT, buff=0.5).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(status_text)
        
        # Parameter displays (fixed to camera, same positioning as main scene) with improved font
        mx_display = Text("Mx: 0.20", font_size=16, color=RED, font="Arial", weight=BOLD)
        my_display = Text("My: 0.00", font_size=16, color=GREEN, font="Arial", weight=BOLD)
        mz_display = Text("Mz: 0.97", font_size=16, color=BLUE, font="Arial", weight=BOLD)
        
        mx_display.to_edge(RIGHT, buff=0.5).shift(UP * 2)
        my_display.next_to(mx_display, DOWN, buff=0.1)
        mz_display.next_to(my_display, DOWN, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(mx_display, my_display, mz_display)
        
        # Add all elements at once to check positioning
        self.add(
            axes, x_label, y_label, z_label,  # Coordinate system
            b0_arrow, b0_label,  # Magnetic field
            magnetization, m_label,  # Magnetization
            rf_arrow,  # RF pulse
            title, equation,  # Text elements
            status_text,  # Status
            mx_display, my_display, mz_display  # Parameter displays
        )
        
        # Brief wait to examine the scene
        self.wait(3)

if __name__ == "__main__":
    print("=== FAST TESTING OPTIONS ===")
    print("\nPosition check (3 seconds):")
    print("manim bloch_improved.py PositionCheck -pql")
    
    print("\n=== MAIN ANIMATION ===")
    print("Testing mode (faster, ~10 seconds):")
    print("manim bloch_improved.py ImprovedBlochEquation -pql")
    print("^ Set testing_mode = True in code (line 21)")
    
    print("\nFull quality (slower, ~25 seconds):")
    print("manim bloch_improved.py ImprovedBlochEquation -pqh")
    print("^ Set testing_mode = False in code (line 21)")
    
    print("\n=== INSTRUCTIONS ===")
    print("1. For development: Use FastTest or PositionCheck")
    print("2. For testing physics: Use ImprovedBlochEquation with testing_mode=True")  
    print("3. For final render: Set testing_mode=False and use -pqh flag")
