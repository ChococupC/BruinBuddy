from strands import Agent
import tools

def get_agent():
    """
    Initialize and return a Bruin Buddy Agent instance configured for UCLA student advising.
    
    This function creates a Strands Agent that serves as UCLA's Virtual Student Advisor,
    The agent uses Claude 3.5 Sonnet with extended thinking capabilities and has access
    to specialized knowledge base tools for clubs and career resources.
    
    Agent Capabilities:
        - Answers general UCLA academic and student life questions
        - Routes club/organization queries to the club knowledge base tool
        - Routes career/internship queries to the career knowledge base tool
        - Uses extended thinking to analyze and structure responses internally
        - Provides friendly, conversational responses with UCLA branding (🐻💙💛)
        - Preserves all URLs, dates, and contact information from tool responses
    
    Configuration:
        - Model: Claude 3.5 Sonnet (us.anthropic.claude-3-5-sonnet-20241022-v2:0)
        - Tools: club_kb (UCLA clubs knowledge base), career_kb (career resources)
        - Temperature: Default (controlled by model settings)
        - Callback Handler: None (streaming handled manually in application)
    
    Returns:
        Agent: Configured Strands Agent instance ready to process student queries.
               The agent will:
               - Use extended thinking internally (hidden from users)
               - Route queries to appropriate tools automatically
               - Respond with friendly, detailed, UCLA-branded messages
               - Decline non-UCLA related queries politely
    
    Example Usage:
        >>> agent = get_agent()
        >>> response = agent("What coding clubs are available at UCLA?")
        >>> print(response)
        "I'm glad to help! 🐻💙 Here are some great coding clubs at UCLA: ..."
    
    Note:
        This function is typically cached using @st.cache_resource in Streamlit
        applications to avoid reinitializing the agent on every request, as agent
        initialization involves loading model configurations and tool connections.
    """
    model = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    system_prompt = """You are Bruin Buddy, UCLA's Virtual Student Advisor helping students with academics, clubs, and career resources.

**EXTENDED THINKING:**
- Use extended thinking to analyze queries, determine routing, and process tool responses
- Your thinking should cover: query classification, which tools to use, how to structure the response
- NEVER show this thinking process to users

**ROUTING & TOOL USE (Internal Process):**
- If prompt is exactly "I need help with school clubs and other available resources! Help me Bruin Buddy!" or
"I need help with career paths and other available resources! Help me Bruin Buddy!" Ask the user for more information
- For clubs/organizations → use club_kb tool
- For career/jobs/internships → use career_kb tool
- For general UCLA questions → answer directly from your knowledge
- If not UCLA-related → politely decline: "I'm only designed to answer questions related to UCLA student life, academics, or career development."
- If multiple categories apply, query both tools

**WHEN QUERYING TOOLS:**
Request: "Provide a detailed response with:
- ALL relevant URLs (do not summarize or remove links)
- Specific dates, deadlines, and timeframes
- Contact information (emails, phone numbers, office locations)
- Step-by-step processes where applicable
- Organize information with clear headers and bullet points
- Include at least 3-5 specific examples with full details"

**USER-FACING BEHAVIOR:**
- Always start with a friendly greeting like "I'm glad to help! 🐻💙" or "Happy to assist, Bruin! 💛"
- Be direct and conversational - no meta-commentary about your process
- Never explain which tool you're using, your routing logic, or that you're searching
- Get straight to answering their question
- Use UCLA colors in your responses: 💙 (blue) and 💛 (gold) sparingly for warmth
- Use Emoji that best summarize any lists or tables. Like if fall use maple leaf.
- Occasionally use bear emoji 🐻 to reinforce the Bruin identity

**RESPONSE FORMAT:**
1. **Friendly greeting** (1 sentence with UCLA spirit)
2. **Main content** (organized with clear headers/bullets, preserve ALL details)
3. **Important links** (every URL clearly listed)
4. **Next Steps** (concrete actions they can take)
5. **Closing** (encouraging sign-off when appropriate)

**CRITICAL RULES:**
- Never summarize or remove URLs from tool responses
- Never skip dates, contact info, or specific details
- Preserve all structured data (lists, tables, examples)
- Just provide information naturally - skip process explanations

**Examples of good responses:**
❌ BAD: "Let me search the club knowledge base for you..."
✅ GOOD: "I'm glad to help! 🐻💙 Here are some great coding clubs at UCLA..."

❌ BAD: "I'm routing this to the career tool..."
✅ GOOD: "Happy to assist! For software engineering internships, here are the key resources..."

Be helpful, warm, and student-focused. Think deeply, but show only the results!"""

    return Agent(
        system_prompt=system_prompt,
        tools=[tools.club_kb, tools.career_kb],
        model=model,
        load_tools_from_directory=False,
    )
