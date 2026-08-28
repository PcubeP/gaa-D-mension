"""Proportional side-view silhouette generator for cars."""
import numpy as np


def generate_side_profile_svg(make: str, model: str, 
                               length_mm: float, height_mm: float, 
                               wheelbase_mm: float, width_mm: float = None) -> dict:
    """
    Generate a proportional side-view silhouette SVG based on car dimensions.
    
    The profile is built from geometric primitives (trapezoids, curves) that
    approximate typical car shapes. Everything is scaled proportionally.
    
    Args:
        make: Car brand (e.g., "Maruti Suzuki")
        model: Car model (e.g., "Swift")
        length_mm: Overall length in mm
        height_mm: Height from ground to roof in mm
        wheelbase_mm: Wheelbase in mm
        width_mm: Overall width (used for front/rear fender protrusion)
    
    Returns:
        dict with svg_data, width_px, height_px, and generation_metadata
    """
    
    if width_mm is None:
        # Typical width-to-length ratio ~0.85
        width_mm = length_mm * 0.85
    
    # Scale factor to pixels (1mm -> 3px for high-res output)
    SCALE_PX_PER_MM = 3.0
    
    # Base silhouette height and length in pixels
    profile_height_px = int(height_mm * SCALE_PX_PER_MM)
    profile_length_px = int(length_mm * SCALE_PX_PER_MM)
    
    # Wheelbase ratio (affects visual "wheel position")
    wb_ratio = wheelbase_mm / length_mm  # Typical range: 0.45-0.52
    
    # Store length for use in draw_wheel_svg
    total_length = length_mm
    
    # Fender overhangs (front + rear)
    front_overhang = (length_mm - wheelbase_mm) * 0.6  # Front is shorter typically
    rear_overhang = (length_mm - wheelbase_mm) * 0.4
    
    # Build SVG coordinate system
    padding = 10  # Padding around the car
    svg_width = profile_length_px + 2 * padding
    svg_height = profile_height_px + 30  # Extra for wheels
    
    # Generate silhouette points (approximate side profile)
    def generate_profile_points(length: float, height: float, width_ratio: float, total_length: float):
        """Generate approximate car side profile as a list of (x,y) pixel coordinates."""
        
        # Normalized positions (0 to 1 along length)
        L = total_length
        H = height
        
        # Profile segments (normalized x from 0 to 1)
        points = []
        
        # Front overhang top
        front_top_x = front_overhang / L
        points.append((front_top_x, 0))
        
        # Windshield start (typical ~25% from front wheel)
        wind_start_x = front_overhang/L + (wb_ratio - front_overhang/L)*0.15/0.6
        wind_y = H * 0.75  # Windshield base height
        points.append((wind_start_x, wind_y))
        
        # A-pillar slope
        for i in range(4):
            x_norm = front_top_x + (1 - front_top_x) * (i+1)/5
            y = H * (0.75 - (0.98-0.75)*(i+1)/5)  # Slight inward slope
            points.append((x_norm, y))
        
        # Roofline (peaks around middle-rear overhang transition)
        roof_peak_x = front_overhang/L + wb_ratio * 0.6
        roof_peak_y = H * 0.95  # Slightly less than full height for aerodynamic shape
        
        points.append((roof_peak_x, roof_peak_y))
        
        # Roofline down to rear window
        for i in range(3):
            x_norm = roof_peak_x + (1-roof_peak_x) * (i+1)/4
            y = roof_peak_y - H * 0.85 * ((i+1)/4) ** 1.2  # Gradual slope down
            points.append((x_norm, y))
        
        # Rear window to tailgate
        tailgate_top_x = front_overhang/L + (1-roof_peak_x) * 0.35/0.65
        tailgate_y = H * 0.82
        points.append((tailgate_top_x, tailgate_y))
        
        # Tailgate slope down
        for i in range(4):
            x_norm = tailgate_top_x + (1-tailgate_top_x) * (i+1)/5
            y = H * 0.82 - H * 0.82 * ((i+1)/5) ** 1.3
            points.append((x_norm, y))
        
        # Rear overhang to rear bumper
        for i in range(4):
            x_norm = tailgate_top_x + (1-tailgate_top_x) * (i+1)/5
            y = H * 0.82 - (H*0.82)*(i+1)/5
            points.append((x_norm, y))
        
        # Rear bumper corner
        points.append((length, H * 0.72))  # Slightly lower at rear
        
        return points
    
    front_points = generate_profile_points(length_mm, height_mm, width_mm/length_mm, length_mm)
    rear_points = list(reversed(generate_profile_points(length_mm, height_mm, width_mm/length_mm, length_mm)))
    
    # Simplify for a clean outline (keep key points only)
    all_points = list(zip(
        [p[0] for p in front_points + rear_points],
        [p[1] for p in front_points + rear_points]
    ))
    
    # Remove duplicates (within tolerance)
    unique_points = []
    if all_points:
        last_point = all_points[0]
        for pt in all_points[1:]:
            dist = np.sqrt((pt[0]-last_point[0])**2 + (pt[1]-last_point[1])**2)
            if dist > 0.5:  # Minimum distance between kept points
                last_point = pt
                unique_points.append(pt)
        all_points = unique_points
    
    # Convert to SVG path data
    def point_to_svg(px, py):
        return f"{px},{py}"
    
    svg_path = ""
    if all_points:
        svg_path = f"  <path d=\"M {point_to_svg(*all_points[0])}\" "
        for pt in all_points[1:]:
            svg_path += f"L {point_to_svg(*pt)} "
        # Close the path
        svg_path += f"L {point_to_svg(all_points[-1][0], profile_height_px)} \" />"
    
    # Build wheel elements (2 wheels at front and rear)
    def draw_wheel_svg(wheel_center_x_px: float, is_front: bool):
        """Generate a simple wheel SVG element."""
        offset = wheel_center_x_px
        y_offset = profile_height_px - 2  # Wheels go to bottom
        
        r_str = int(profile_height_px * 0.25)  # Wheel radius ~1/4 height
        
        return f'  <circle cx="{offset}" cy="{y_offset + r_str}" r="{r_str}"/>' \
               f'  <rect x="{offset-r_str//3}" y="{y_offset+r_str*0.7}" width="{r_str*2//3}" height="{r_str*0.6}"/>'
    
    wheel_front = draw_wheel_svg(wheel_center_x_px=padding + front_overhang, is_front=True)
    wheel_rear = draw_wheel_svg(wheel_center_x_px=padding + profile_length_px - rear_overhang, is_front=False)
    
    # Generate SVG
    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" 
         width="{svg_width}px" height="{svg_height}px" role="img" aria-label="{make} {model} Side View">
  <title>{make} {model}</title>
  <desc>Side profile silhouette for "{make} {model}" scaled to actual dimensions.</desc>'''
    
    svg_footer = '''</svg>'''.strip()
    
    full_svg = svg_header + "\n" + "\n".join([wheel_front, wheel_rear]) + "\n" + svg_path + "\n" + svg_footer
    
    return {
        "svg_data": full_svg,
        "width_px": svg_width,
        "height_px": svg_height,
        "dimensions_mm": {
            "length": length_mm,
            "width": width_mm,
            "height": height_mm,
            "wheelbase": wheelbase_mm
        },
        "make": make,
        "model": model
    }
