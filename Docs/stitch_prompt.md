# Prompt for Google Stitch (Frontend UI Generation)

**Context:**
I am building an AI-powered restaurant recommendation web app inspired by Zomato. The backend API is already built and handles filtering and LLM-based ranking. I need you to generate a premium, production-ready frontend using **HTML5, Vanilla CSS (no Tailwind), and Vanilla JavaScript**.

**Design System & Aesthetics (CRITICAL):**
The UI must have a premium, modern **Glassmorphism Dark-Mode** aesthetic. It must WOW the user.
- **Background:** Deep dark `hsl(230, 25%, 8%)` with subtle glowing abstract gradient orbs in the background (e.g., a soft red/gold blur) to give depth.
- **Cards/Containers:** Glass effect using `background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;`.
- **Accents:** Zomato-inspired red `hsl(350, 85%, 55%)` for primary buttons/highlights, and warm gold `hsl(40, 95%, 60%)` for secondary accents (like stars/ratings).
- **Typography:** Modern sans-serif (e.g., 'Inter', 'Outfit', or system-ui). Text colors: Primary `hsl(0, 0%, 95%)`, Secondary `hsl(0, 0%, 60%)`.
- **Interactions:** Smooth CSS transitions (`0.3s ease`) on all interactive elements. Buttons and cards should have subtle hover lift and glow effects.

**Layout & Structure:**
Create a single-page application (SPA) layout with the following elements:
1. **Header:** Clean navbar with an AI/Zomato inspired logo/title and a short tagline ("Discover your next favorite meal").
2. **Hero Section / Preference Form (`#preferences-form`):**
   - A clean, grid-based form embedded in a glass card.
   - **Location:** Dropdown (`<select>`) containing placeholder neighborhoods like "Indiranagar", "Koramangala", "Bellandur".
   - **Cuisine:** Dropdown containing "North Indian", "Cafe", "Italian", etc.
   - **Budget:** Dropdown with options: "low", "medium", "high".
   - **Minimum Rating:** Range slider or number input (0.0 to 5.0).
   - **Additional Preferences:** A textarea or text input for free-form requests (e.g., "outdoor seating, pet friendly").
   - **Submit Button:** A prominent, glowing button labeled "Find Restaurants 🪄".
3. **Loading State:** A beautiful pulsing skeleton loader or spinner that appears while waiting for AI results.
4. **Results Container (`#results`):** A responsive CSS grid to hold recommendation cards.
5. **Recommendation Card (Mock up at least two cards in the results):**
   - Must show the Rank badge (e.g., #1).
   - **Name:** E.g., "Tipsy Bull".
   - **Rating Badge:** E.g., "★ 4.4" (styled distinctly).
   - **Cuisine Tags:** "North Indian, Chinese".
   - **Cost:** "Rs. 1400 for two".
   - **AI Explanation:** A stylized text block mimicking an AI's voice explaining why it was chosen based on the preferences.
6. **Toast Notification:** A hidden div styled as a modern floating toast for error/success messages.

**Javascript Requirements:**
- Include a mock `app.js` script block that handles the form submission `event.preventDefault()`.
- Add logic to show the loading state for 2 seconds, then hide the form, and smoothly fade in the mock recommendation cards to demonstrate the interaction flow.

**Output Rules:**
- Do NOT use Tailwind or Bootstrap. Write custom CSS.
- Ensure the layout is fully responsive (mobile-first).
- Deliver the final output as a cohesive, single `index.html` file containing the `<style>` and `<script>` blocks so I can run it immediately in the browser.
