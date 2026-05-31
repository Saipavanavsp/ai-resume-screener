import os
import sys

# Try to import PIL, install if missing
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("PIL (Pillow) is not installed. Installing it now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(text_filepath, output_image_path, title="PowerShell"):
    if not os.path.exists(text_filepath):
        print(f"Error: {text_filepath} not found.")
        return
        
    try:
        with open(text_filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(text_filepath, "r", encoding="utf-16") as f:
            lines = f.readlines()
        
    # Remove empty lines at start/end
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
        
    # Configurations
    bg_color = (30, 30, 30)      # Dark grey terminal bg
    text_color = (240, 240, 240)  # Off-white text
    title_bar_color = (45, 45, 45) # Slightly lighter title bar
    
    font_size = 14
    line_spacing = 6
    char_width = 8.5
    line_height = font_size + line_spacing
    
    # Try to load Consolas font, fallback to default
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Calculate dimensions
    max_line_len = max(len(line.rstrip()) for line in lines) if lines else 80
    num_lines = len(lines)
    
    width = int(max_line_len * char_width) + 40
    width = max(width, 650)  # Min width
    
    title_bar_height = 30
    padding = 20
    height = title_bar_height + (num_lines * line_height) + (padding * 2)
    
    # Create Image
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw Title Bar
    draw.rectangle([(0, 0), (width, title_bar_height)], fill=title_bar_color)
    
    # Draw Window Control Dots (red, yellow, green)
    dot_radius = 6
    dot_y = title_bar_height // 2
    draw.ellipse([(15 - dot_radius, dot_y - dot_radius), (15 + dot_radius, dot_y + dot_radius)], fill=(255, 95, 87))
    draw.ellipse([(35 - dot_radius, dot_y - dot_radius), (35 + dot_radius, dot_y + dot_radius)], fill=(255, 189, 46))
    draw.ellipse([(55 - dot_radius, dot_y - dot_radius), (55 + dot_radius, dot_y + dot_radius)], fill=(40, 200, 64))
    
    # Draw Title Text
    try:
        title_font = ImageFont.truetype("arial.ttf", 12)
    except IOError:
        title_font = ImageFont.load_default()
    draw.text((width // 2, title_bar_height // 2), title, fill=(200, 200, 200), font=title_font, anchor="mm")
    
    # Draw Terminal Lines
    current_y = title_bar_height + padding
    for line in lines:
        draw.text((padding, current_y), line.rstrip(), fill=text_color, font=font)
        current_y += line_height
        
    img.save(output_image_path)
    print(f"Rendered terminal screenshot saved to {output_image_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_screenshots.py <input_log_path> <output_image_path> [window_title]")
        sys.exit(1)
        
    title = sys.argv[3] if len(sys.argv) > 3 else "PowerShell"
    render_terminal_screenshot(sys.argv[1], sys.argv[2], title)
