from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.client import Users
from diagrams.gcp.compute import Run
from diagrams.aws.storage import S3
from diagrams.custom import Custom

# Set diagram formatting
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "splines": "ortho",
}

# Base path for images (Updated to your absolute path)
base_path = r"input_icons"

# Create the diagram
with Diagram("FitAura", show=False, graph_attr={"rankdir": "LR", "splines": "polyline", "nodesep": "0.5"}):
   
    # User/Client
    user = Users("End User")

    # Frontend Cluster
    with Cluster("Frontend (User Interface)"):
        streamlit = Custom("Streamlit UI", f"{base_path}/streamlit.png")
   

    with Cluster("Backend"):
        fastapi = Custom("FastAPI", f"{base_path}/FastAPI.png")

        with Cluster("LangChain LLM Integration"):
            gemini = Custom("Gemini \n (Google)", f"{base_path}/gemini.png")

    user >> streamlit >> fastapi >> gemini
    gemini >> fastapi >> streamlit >> user
    