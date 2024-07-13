import google.generativeai as genai
import re
from dotenv import load_dotenv
# from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()

def get_color_analysis(skin_hex, eye_hex, hair_hex):
    """Generates a response from the Gemini LLM based on provided hex codes.

    Args:
        skin_hex: Hex code for skin color.
        eye_hex: Hex code for eye color.
        hair_hex: Hex code for hair color.

    Returns:
        The generated response from the LLM.
    """
    
    # Configure API key (replace with your actual API key)
    genai.configure(api_key="AIzaSyAU1RvIrI_U8IvZgKiymmwGNKsuxiVH9ms")

    # Replace with your desired model
    model = genai.GenerativeModel('gemini-pro')
    
    # prompt = (f"These are the hex codes for my colors: skin #{skin_hex}, eye #{eye_hex}, hair #{hair_hex}. "
    #           "Which skin tone color palette am I in terms of spring, winter, summer, fall? Do a color analysis. "
    #           "Tell me which colors would look good on me, including jewelry colors. Give all the colors you recommend first and then give an explanation.")
    
    try:
        response = model.generate_content(f"""These are the hex codes for my colors: skin #{skin_hex}, eye #{eye_hex}, hair #{hair_hex}.
                                        Do a detailed color palette analysis and give my color palette in terms of the seasons - Spring, Winter, Summer, Autumn. Choose only one season palette, pick the best one that fits my palette.
                                        Give all the colors you reccomend including clothing and jelwery colors. 
                                        Additionally give me some fashion tips. Do not mention any colors that will not suit my palette in your response. Do not tell me what colors to avoid. Limit your response to 200 words.""" )
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None



# Example usage
skin_color = "DA9762"
eye_color = "664236"
hair_color = "2D1D20"
response = get_color_analysis(skin_color, eye_color, hair_color)


myntra_color_list = [
    "white", "blue", "black", "pink", "green", "beige", "brown", "burgundy", 
    "charcoal", "coffee brown", "coral", "cream", "fluorescent green", "gold", 
    "grey melange", "grey", "khaki", "lavender", "lime green", "magenta", 
    "maroon", "mauve", "multi", "mustard", "navy blue", "nude", "off white", 
    "olive", "orange", "peach", "purple", "red", "rose", "rust", "sea green", 
    "silver", "tan", "taupe", "teal", "turquoise blue", "yellow"
]

color_hexcodes = {
    'red': '#FF0000', 'crimson': '#DC143C', 'scarlet': '#FF2400', 'ruby': '#E0115F',
    'cherry': '#DE3163', 'burgundy': '#800020', 'maroon': '#800000',
    'orange': '#FFA500', 'tangerine': '#F28500', 'coral': '#FF7F50', 'peach': '#FFDAB9',
    'apricot': '#FBCEB1', 'burnt orange': '#CC5500', 'yellow': '#FFFF00', 'lemon': '#FFF700',
    'gold': '#FFD700', 'canary': '#FFFF99', 'amber': '#FFBF00', 'mustard': '#FFDB58',
    'green': '#008000', 'emerald': '#50C878', 'jade': '#00A86B', 'olive': '#808000',
    'mint': '#3EB489', 'forest green': '#228B22', 'blue': '#0000FF', 'cobalt': '#0047AB',
    'azure': '#007FFF', 'cyan': '#00FFFF', 'sky blue': '#87CEEB', 'indigo': '#4B0082',
    'purple': '#800080', 'violet': '#8F00FF', 'lavender': '#E6E6FA', 'lilac': '#C8A2C8',
    'plum': '#8E4585', 'mauve': '#E0B0FF', 'pink': '#FFC0CB', 'rose': '#FF007F', 'blush': '#DE5D83',
    'salmon': '#FA8072', 'fuchsia': '#FF00FF', 'hot pink': '#FF69B4', 'brown': '#A52A2A',
    'chocolate': '#D2691E', 'tan': '#D2B48C', 'sienna': '#A0522D', 'chestnut': '#954535',
    'mahogany': '#C04000', 'white': '#FFFFFF', 'ivory': '#FFFFF0', 'cream': '#FFFDD0',
    'snow': '#FFFAFA', 'pearl': '#EAE0C8', 'black': '#000000', 'ebony': '#555D50',
    'charcoal': '#36454F', 'onyx': '#353839', 'gray': '#808080', 'slate': '#708090',
    'silver': '#C0C0C0', 'ash': '#B2BEB5', 'beige': '#F5F5DC', 'khaki': '#C3B091',
    'sand': '#C2B280', 'camel': '#C19A6B', 'turquoise': '#40E0D0', 'aquamarine': '#7FFFD4',
    'teal': '#008080', 'champagne': '#F7E7CE', 'brass': '#B5A642', 'platinum': '#E5E4E2',
    'steel gray': '#262626', 'wine': '#722F37', 'bordeaux': '#5C0120', 'army green': '#4B5320',
    'sage': '#9CB071', 'aqua': '#00FFFF', 'light blue': '#ADD8E6', 'magenta': '#FF00FF',
    'orchid': '#DA70D6', 'raspberry': '#E30B5C', 'coffee brown': '#4B3621',
    'fluorescent green': '#08FF00', 'grey melange': '#D1D0CE', 'metallic': '#85754D',
    'multi': '#FFFFFF', 'navy blue': '#000080', 'off white': '#FAF0E6',
    'turquoise blue': '#00FFEF', 'nude': '#F2D2B5', 'rust': '#B7410E',
    'sea green': '#2E8B57', 'taupe': '#483C32'
}


def extract_color(description):
    # Initialize a set to store unique colors
    found_colors = set()

    # Find colors in description
    for color in myntra_color_list:
        if re.search(r'\b' + re.escape(color) + r'\b', description, flags=re.IGNORECASE):
            found_colors.add(color)
    
    return list(found_colors)  # Convert set to list before returning


def get_hexcodes_for_colors(colors):
    hexcodes = []
    for color in colors:
        hexcodes.append(color_hexcodes[color.lower()])  # Add None if the color is not in the dictionary
    return hexcodes

def extract_palette(response):
    pattern = re.compile(r'\b(summer|winter|autumn|spring)\b', re.IGNORECASE)
    match = pattern.search(response)
    
    if match:
        return match.group(0)
    else:
        return None

print("Your Personal Color Analysis by GlamBot")

palette = extract_palette(response)
print("Your Most Suitable Season Palette:", palette)

print(response)

recommended_colors = extract_color(response)
print("Recommended Colors:", recommended_colors)

color_hexcodes_list = get_hexcodes_for_colors(recommended_colors)
print("Reccomended Color Hexcodes:", color_hexcodes_list)