import streamlit as st
from strands.models import BedrockModel
from support_engineer import support_engineer


BEDROCK_MODEL_ID    = "anthropic.claude-3-7-sonnet-20250219-v1:0"
REGION              = "eu-west-2"
TEMPERATURE         = 0.3

bedrock_model = BedrockModel(
    model_id    = BEDROCK_MODEL_ID,
    region_name = REGION,
    temperature = TEMPERATURE,
)

st.set_page_config(page_title="AWS Support Engineer!", layout="wide")
st.title("AWS Support Engineer")

view = st.sidebar.radio("Choose a view:", ["Support Engineer"])

if view == "Support Engineer":
    support_engineer(bedrock_model)
