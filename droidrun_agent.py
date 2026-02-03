import os
from droidrun import DroidAgent
from droidrun.config_manager import DroidrunConfig
from pydantic import BaseModel, Field
from llama_index.llms.google_genai import GoogleGenAI

api_key = os.getenv("GOOGLE_API_KEY")

class Response(BaseModel):
    status: str = Field(description="Must be 'EMPTY' or 'PROCESSED'.")
    customer_handle: str = Field(default=None, description="The user handle starting with @.")
    category: str = Field(default=None, description="One of: 'SALE', 'ENQUIRY', 'URGENT', 'GENERAL'.")
    details: str = Field(default=None, description="Summary of the user's message/order item.")
    
class DAgent:
    def __init__(self):
        self.config = DroidrunConfig()
        
    async def run_cycle(self, biz_name, inv):
        goal_prompt = f"""
        **SYSTEM ROLE**
        You are the AI Operator for "{biz_name}". You control a physical phone screen.
        Your job is to read Instagram DMs and reply based ONLY on the provided Inventory.

        **CRITICAL INVENTORY**
        {inv}
        RULE: If a user asks for an item NOT in this list, reply that you will check stock. DO NOT invent products.

        **EXECUTION PROTOCOL**

        **PHASE 1: NAVIGATION**
        1. Open Instagram.
        2. Tap the Messenger Button (Bottom Middle it looks like a paper plane).
        3. Scan for UNREAD messages (Bold Text or Blue Dots).
           - IF NONE FOUND: Stop. Return status='EMPTY'.
           - IF FOUND: Tap the top unread conversation.

        **PHASE 2: ANALYSIS**
        4. Analyze the last 3 messages.
        5. Check if the last message is from YOU (Right side). If yes, go to phase 4(Close Instagram).
        6. **IDENTIFY USER:**
           - Look at the TOP of the chat. Find the Handle (starts with @).
           - DO NOT use the Display Name.

        **PHASE 3: DECISION TREE & OUTPUT GENERATION**

        **PATH A: DIRECT ORDER (High Intent)**
        - Criteria: User says "I want to buy", "I'll take it", "Order this".
        - Action: Confirm availability.
        - Reply: "Great choice! I have noted your order. We will confirm details shortly."
        - **OUTPUT:** - Category: 'SALE'
          - Details: "[Item Name] - [Price]"

        **PATH B: PRODUCT INQUIRY (Low Intent)**
        - Criteria: User asks "How much?", "Is this available?", "Size?".
        - Action: Check Inventory and answer.
        - Reply: Provide all the info(Should incude name, price and all attributes provided). End with "Would you like to grab one?"
        - **OUTPUT:**
          - Category: 'ENQUIRY'
          - Details: "User asked about [Item Name/Topic]"

        **PATH C: URGENT SUPPORT**
        - Criteria: Angry tone, "Where is my order?", "Wrong item".
        - Action: Apologize and de-escalate.
        - Reply: "I am so sorry about this. I am escalating this to a human manager right now."
        - **OUTPUT:**
          - Category: 'URGENT'
          - Details: "Complaint: [Issue Summary]"

        **PATH D: GENERAL CHAT**
        - Criteria: "Hello", "Location?", "Hours?".
        - Action: Answer helpfully.
        - **OUTPUT:**
          - Category: 'GENERAL'
          - Details: "Question: [Topic]"

        **PHASE 4: EXECUTION (Mechanical)**
        7. Type the generated reply in the text box which you MUST send.
        8. **CRITICAL STEP - SENDING:**
           - Look for the "Send" button or Paper Plane Icon.
           - **TAP IT.** Verify the message appears in chat.
        9. If you have not sent the message (saved as draft) you must go back and send it before exiting
        10. Tap Back to return to DM list.
        11. Close the app and return to Home Screen.
        """ 
        
        llm=GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)

        agent = DroidAgent(
            goal=goal_prompt,
            config=self.config,
            output_model=Response,
            llms=llm
        )
        
        print(f"DroidRun Agent active for {biz_name}...")
        
        result = await agent.run()
        
        if result.success and result.structured_output:
            return result.structured_output
        return None