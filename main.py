import asyncio
from db import Database
from droidrun_agent import DAgent

async def main():
    db = Database()
    agent = DAgent()
    print("---ECHO BRAIN SERVER STARTED---")
    
    while True:
        biz_name, inventory = db.get_context()
        
        print(f"Starting Cycle for: {biz_name}")
        print(f"Context Loaded: {len(inventory)} chars")

        report = await agent.run_cycle(biz_name, inventory)
        
        if report:
            if report.status == "EMPTY":
                print("Inbox Empty. No actions taken.")
            
            elif report.status == "PROCESSED":
                handle = report.customer_handle
                category = report.category
                details = report.details
                
                print(f"Agent Reported: {category} | {handle}")
                
                if category == "SALE":
                    db.log_sale(handle, details)
                    print(f"ORDER SAVED: {handle} bought {details}")
                else:
                    db.log_query(handle, category, details)
                    print(f"TICKET SAVED: {handle} -> {details}")
        else:
            print("Agent finished but returned no report.")

        print("Waiting 5s...")
        await asyncio.sleep(5)
        
if __name__ == "__main__":
    asyncio.run(main())