import streamlit as st
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

def support_engineer(bedrock_model):
    st.markdown("Support Engineer")
    user_description = st.text_area("Describe the issue you are having")

    if st.button("Go!"):
        if not user_description.strip():
            st.warning("Please provide a description.")
            st.stop()

        with st.spinner("Analyzing..."):
            aws_cloudwatch_tools = MCPClient(
                lambda: stdio_client(StdioServerParameters(
                    command="uvx", 
                    args=[
                        "awslabs.cloudwatch-mcp-server@latest",
                        ]
                    )
                )
            )

            aws_documentation_tools = MCPClient(
                lambda: stdio_client(StdioServerParameters(
                    command="uvx", 
                    args=[
                        "awslabs.documentation-mcp-server@latest",
                        ]
                    )
                )
            )

            aws_knowledge_tools = MCPClient(
                lambda: stdio_client(StdioServerParameters(
                    command="uvx", 
                    args=[
                        "awslabs.knowledge-mcp-server@latest",
                        ]
                    )
                )
            )

            aws_pricing_tools = MCPClient(
                lambda: stdio_client(StdioServerParameters(
                    command="uvx", 
                    args=[
                        "awslabs.pricing-mcp-server@latest",
                        ]
                    )
                )
            )

            agent = Agent(
                name="Support Engineer", 
                description="Assists diagnosing issues in client AWS accounts", 
                model=bedrock_model, 
                tools=[aws_cloudwatch_tools, aws_documentation_tools, aws_knowledge_tools, aws_pricing_tools])
            
            prompt = f"""
            You are an AWS support enginee and FinOps expert. You are going to be provided with ticket details raised on our Jira board.
            - You will assess the input and come up with potential fixes for the issue described.
            - You should aim to provide a summary of what is wrong, as well as potential paths forward.
            - Your output should include; tests to diagnose the issue, questions to ask the client to get a better idea of the conext, potential escaltion paths to either our Data, Devops, or Solution Architect teams.
            - If logs are provided you should analyse them with the cloudwatch mcp server.
            - you should use the knowledge base and documentation mcp servers to provide fixes and links to helpful documentation.
            - you should use the pricing mcp server to estimate costs of suggested fixes, and also estimate costs for any work that clients suggest they want to via the ticket.
            - I would also like you to make a best guess judgement of whether the client request is a support ticket or something that should be done via our Proffessional Services team (ie, a scoped out bit of work).
            --- INPUT START ---
            {user_description}
            --- INPUT END ---
            """
            
            response = agent(prompt)
            st.subheader("Support Engineer")
            st.markdown(str(response).strip())
