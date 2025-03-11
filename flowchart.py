import google.generativeai as genai
import os
import graphviz
from PIL import Image

def generate_flowchart_structure(user_input, api_key):
    """Uses Google Gemini API to generate a structured Mermaid flowchart."""
    os.environ["AIzaSyAZc_D_kRPTLf8Jv3uvtUZqD5wqTcvIW_k"] = api_key  # Set API key in environment
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Generate a top-down Mermaid flowchart for: {user_input}. "
                                      "Ensure the flowchart has NO labels like A, B, C before each step. "
                                      "Make all connections directly between shapes."
                                      "input statement always in parallelogram shape."
                                      "Input first number,Sum = First Number + Second Number,Display Sum,End mention the flowchart content that inside {} bracket"
                                      )

    return response.text

def create_flowchart(flowchart_text, output_file="flowchart"):
    """Converts Mermaid-style structured text into a Graphviz flowchart image with vertical alignment."""
    
    dot = graphviz.Digraph(format="jpg")
    dot.attr(rankdir="TB")  # ✅ Ensures a vertical flow

    shape_map = {
        "Start": "oval",
        "End": "oval",
        "Input": "parallelogram",
        "Output": "parallelogram",
        "Sum": "rectangle",
        "Calculate": "rectangle",
        "Display": "parallelogram"
    }

    nodes = {}  # Store unique nodes

    # Ensure `graph TD` is used
    flowchart_text = flowchart_text.replace("graph LR", "graph TD")

    # Process lines and construct the flowchart
    for line in flowchart_text.strip().split("\n"):
        line = line.strip()
        if line.startswith("graph TD"):
            continue  # Skip header

        if "-->" in line:
            parts = line.split("-->")
            if len(parts) != 2:
                continue  # Avoid index errors

            start = parts[0].strip()
            end = parts[1].strip()

            # Determine correct shape for each node
            start_shape = shape_map.get(start.split()[0], "rectangle")
            end_shape = shape_map.get(end.split()[0], "rectangle")

            # Create nodes only if they don’t exist
            if start not in nodes:
                nodes[start] = start
                dot.node(start, start, shape=start_shape)

            if end not in nodes:
                nodes[end] = end
                dot.node(end, end, shape=end_shape)

            # Add edge between nodes
            dot.edge(start, end)

    # Save and render the flowchart
    dot.render(output_file, format="jpg", cleanup=True)
    print(f"✅ Flowchart saved as {output_file}.jpg")

    # Open and display the generated image
    image = Image.open(f"{output_file}.jpg")
    image.show()

def main():
    api_key = "AIzaSyAZc_D_kRPTLf8Jv3uvtUZqD5wqTcvIW_k"
    
    if not api_key:
        print("❌ Error: No API key provided. Please enter a valid Google Gemini API key.")
        return
    
    user_input = input("📝 Describe your program or algorithm: ")
    
    print("🔄 Generating flowchart...")
    try:
        flowchart_structure = generate_flowchart_structure(user_input, api_key)
        print("📌 Generated structure:\n", flowchart_structure)
        create_flowchart(flowchart_structure, "flowchart")
    except Exception as e:
        print(f"⚠️ Error generating flowchart: {e}")
    
if __name__ == "__main__":
    main()
