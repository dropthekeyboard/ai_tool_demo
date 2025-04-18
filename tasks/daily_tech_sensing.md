# Daily Tech Sensing Task Guide

## Directory Setup

- Build directory for research under `./Daily/{date}` (note: capital D in `Daily`)
  - **IMPORTANT**: Directory creation requires careful attention to shell command syntax:
  - ✅ CORRECT: Use double quotes: `mkdir -p "./Daily/$(date +%Y-%m-%d)"`
  - ✅ CORRECT: Use no quotes: `mkdir -p ./Daily/$(date +%Y-%m-%d)`
  - ✅ RECOMMENDED: Save date to variable first: `today=$(date +%Y-%m-%d)` and then `mkdir -p "./Daily/$today"`
  - ❌ INCORRECT: Using single quotes: `mkdir -p './Daily/$(date +%Y-%m-%d)'` (this prevents shell expansion)
  - ❌ INCORRECT: Literal interpretation: The directory should NOT be named literally "$(date +%Y-%m-%d)"
  - 🔍 VERIFICATION: Always verify directory creation with `ls -la ./Daily/` to confirm proper date expansion

## Check for Overlap with Previous Research

- Before starting new research, examine previous dated directories:
  - List all directories: `ls -la ./Daily/`
  - Review the most recent 2-3 directories' content
  - Check `list.md` and `overview.md` in previous directories to identify already-researched startups
  - Ensure new research doesn't duplicate previous findings
  - Note any emerging patterns or continued trends from previous research

## Research Focus

- Search for early-stage AI startups meeting these criteria:
  - Valuation under $100M
  - Early stages (seed, pre-seed, Series A)
  - Recently received significant media attention or gone viral
  - Innovative AI technology or application
  - Founded within the past 1-3 years

## Information Sources (Ensure Diversity)

- **Primary Sources:**
  - **Accelerators and Incubators:**
    - Y Combinator (YC) recent batches
    - Techstars AI cohorts
    - Antler portfolio companies
    - SOSV/HAX hardware startups
    - 500 Startups AI investments
  
  - **Hacker News Trend Monitoring:**
    - Search "Show HN" posts with AI/ML tags
    - Monitor discussions about new AI tools and libraries
    - Track trending GitHub repositories mentioned on HN
    - Use search queries like "AI startup site:news.ycombinator.com" for recent discussions
    - Monitor "Ask HN" threads about AI tools people are using
  
  - **Investment Sources:**
    - Recent seed/Series A announcements from AI-focused VCs
    - AngelList trending AI startups
    - Crunchbase newly funded companies in AI/ML categories
    - CB Insights AI startup reports and funding announcements
  
  - **Industry News and Communities:**
    - TechCrunch, VentureBeat, and The Information startup coverage
    - ML/AI research paper repositories and discussions
    - Product Hunt launches in AI category
    - AI-focused Discord and Slack communities
    - Twitter/X conversations about emerging AI tools

  - **Global Coverage:**
    - Ensure geographic diversity (not just US-based startups)
    - Include startups from emerging tech hubs (Europe, Asia, Latin America)
    - Track international accelerator programs focused on AI

## Research Structure

1. Create `list.md` in the dated directory with:
   - Criteria checklist for startup investigation
   - Diverse list of startups to be researched (from varied sources)
   - Analysis points to cover for each startup
   - Reference links to diverse sources where startups were identified

2. For each identified startup:
   - Create `{company_name}.md` under `./Daily/{date}/`
   - Write comprehensive report following the checklist points
   - Include sections on: company overview, founding team, technology, funding details, market opportunity, competition, media attention, partnerships, challenges, and future outlook
   - **Include reference URLs** for all factual information with clear citations
   - Maintain a "References" section at the bottom of each report with numbered links

3. Create `overview.md` providing a holistic analysis:
   - Summary of key trends across the researched startups
   - Comparative analysis highlighting similarities and differences
   - Market implications and future predictions
   - Overall conclusions about the early-stage AI startup landscape
   - Include reference links to support trend analysis and predictions
   - Note any continuations of trends identified in previous research cycles

4. **Comparative Analysis (When Applicable):**
   - If researching multiple startups in the same domain or with overlapping technologies, create a dedicated comparative analysis section either within `overview.md` or as a separate `comparative.md` file
   - Compare and contrast startups across key dimensions:
     - Technical approaches and innovation styles
     - Business models and go-to-market strategies
     - Funding structures and investor backing
     - Team composition and expertise distribution
     - Market positioning and competitive advantages
     - Growth metrics and traction indicators (when available)
   - Create comparison tables for easy visualization of differences
   - Identify complementary technologies or potential future collaborations/acquisitions
   - Analyze which approaches might be most promising given current market conditions
   - Note when startups are taking fundamentally different approaches to solving similar problems
   - Include expert opinions or market analyst perspectives on competing approaches (if available)

5. **Daily Summary File:**
   - Create a consolidated `daily_startup_search_YYMMDD.md` file that includes:
     - The overview analysis section
     - Individual company profiles appended sequentially
     - Clear separation between sections using markdown dividers (---)
     - This file serves as a single document for easy sharing and archiving
     - Use this as the base document for translations when needed

## Internationalization Requirements

- Create translated versions of key findings for international distribution as needed:
  - Primary documents to translate: `overview.md` and potentially individual company profiles
  - Use consistent file naming convention: `{original_filename}_{language_code}.md` (e.g., `daily_startup_search_250313_ko.md`)
  - Maintain all formatting structures in translations (tables, bullet points, markdown styling)
  - Preserve technical terminology, company names, and numerical data accurately
  - When translating technical concepts, provide appropriate cultural context
  - Verify that tables render correctly after translation

## Communication Materials Preparation

- After completing research, format findings for appropriate communication channels:
  - Review message template formats in `message_template.md`
  - For Telegram messages:
    - Include URL to primary source at the beginning
    - Create a concise title in quotation marks highlighting key trend
    - Provide brief introduction summarizing the research
    - Use headers with # symbol for clear section organization
    - Include a "당사 시너지 가능성" (Company Synergy Potential) section if relevant
    - Format code blocks with triple backticks for Telegram compatibility
  - Keep messages concise but comprehensive for mobile viewing
  - Emphasize actionable insights rather than just descriptive information

## Output Quality

- Ensure all reports are well-structured with clear headings
- Include specific data and details where available
- Analyze not just facts but implications and patterns
- Maintain professional tone and language throughout
- **Fact-checking requirements:**
  - Every significant claim should have at least one reference URL
  - Prioritize primary sources (company websites, founder interviews, official announcements)
  - Include direct links to relevant online discussions where appropriate
  - For funding information, link to credible sources (Crunchbase, TechCrunch, etc.)
  - Note any conflicting information found during research
  - Indicate when information comes from analysis rather than direct sources
  - Cross-reference findings across multiple sources when possible
