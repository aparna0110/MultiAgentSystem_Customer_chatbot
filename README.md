# MultiAgentSystem_Customer_chatbot

Agent Orchestration Flow
The system uses LangGraph to orchestrate multiple agents:

Tier-1 FAQ Agent (vector-based)
Tier-2 Escalation Agent (LLM reasoning)
Manager/Audit Agent (quality control)
Flow diagram is available in graph/agent_flow.png.

# Architecture

       +----------------+
       |   User Query   |
       +--------+-------+
                |
                v
       +--------+-------+
       | Tier-1 Agent   |
       | (FAQ + RAG)    |
       +--------+-------+
                |
        Confidence >= 0.6
         /                \
       Yes                 No
      /                     \
	Manager Agent		    +--------+----------+
       |              | Tier-2 Escalation |
    Return Ans        | Agent             |
                      +--------+----------+
                             |
                          Manager Agent
						                 |
                           Return Ans

# Tech Stack used

LangGraph
LangChain
Azure OpenAi
DeepEval

# IMPLEMENTATION in working---

Payload of RestApi- 

{
  "question": "How can I reset my password?"
}

Backend--

➡️ ENTERED: Tier-1 Agent Answer: You can reset your password using the Forgot Password option. Confidence: 0.5391336604952812 Tier-1 confidence: 0.5391336604952812 

➡️ ENTERED: Tier-2 Agent Tier-2 confidence: 0.9 

➡️ ENTERED: Manager/Audit Agent Manager status: {'final_answer': 'To reset your password, follow these steps:\n\n1. **Go to the login page** of the platform or service you are trying to access.\n2. Click on the **"Forgot Password"** or similar option (e.g., "Reset Password").\n3. Enter the email address or username associated with your account when prompted.\n4. Check your email inbox for a password reset link. If you don’t see it, check your spam or junk folder.\n5. Click on the link provided in the email. This will redirect you to a secure page where you can create a new password.\n6. Follow the instructions to set a new password. Make sure it meets any security requirements (e.g., minimum length, use of special characters, etc.).\n7. Once the password is successfully reset, return to the login page and sign in using your new password.\n\nIf you encounter any issues during this process, such as not receiving the reset email or being unable to access your account, please contact our support team for further assistance.', 'confidence': 0.9, 'status': 'approved', 'reason': 'Response approved by audit agent'} 

Final Output: {'question': 'How can I reset my password?', 'answer': 'To reset your password, follow these steps:\n\n1. **Go to the login page** of the platform or service you are trying to access.\n2. Click on the **"Forgot Password"** or similar option (e.g., "Reset Password").\n3. Enter the email address or username associated with your account when prompted.\n4. Check your email inbox for a password reset link. If you don’t see it, check your spam or junk folder.\n5. Click on the link provided in the email. This will redirect you to a secure page where you can create a new password.\n6. Follow the instructions to set a new password. Make sure it meets any security requirements (e.g., minimum length, use of special characters, etc.).\n7. Once the password is successfully reset, return to the login page and sign in using your new password.\n\nIf you encounter any issues during this process, such as not receiving the reset email or being unable to access your account, please contact our support team for further assistance.', 'confidence': 0.9}
