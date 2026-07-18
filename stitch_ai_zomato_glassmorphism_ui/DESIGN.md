---
name: Culinary Velocity
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#ffdf9e'
  on-secondary: '#3f2e00'
  secondary-container: '#fabd00'
  on-secondary-container: '#6a4e00'
  tertiary: '#71dd7c'
  on-tertiary: '#003910'
  tertiary-container: '#37a54c'
  on-tertiary-container: '#00320d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdf9e'
  secondary-fixed-dim: '#fabd00'
  on-secondary-fixed: '#261a00'
  on-secondary-fixed-variant: '#5b4300'
  tertiary-fixed: '#8dfa96'
  tertiary-fixed-dim: '#71dd7c'
  on-tertiary-fixed: '#002106'
  on-tertiary-fixed-variant: '#00531b'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
  background-deep: '#020617'
  surface-card: '#0F172A'
  text-primary: '#FFFFFF'
  text-secondary: '#94A3B8'
  zomato-white: '#FFFFFF'
  zomato-black: '#1C1C1C'
  rating-gold: '#8C6115'
typography:
  display-lg:
    fontFamily: Lexend
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Lexend
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Lexend
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Lexend
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  margin-mobile: 16px
  margin-desktop: 24px
  gutter: 16px
  container-max: 1200px
---

## Brand & Style
The design system is engineered to evoke appetite, urgency, and reliability. It targets a diverse audience ranging from hungry commuters to fine-dining enthusiasts, requiring a UI that is both high-energy and impeccably organized. 

The aesthetic is **Modern & High-Contrast**, leaning into a sophisticated "Dark Mode" first approach for premium surfaces while maintaining a "Light Mode" for high-utility tasks. The style prioritizes crispness over soft blurs, using deep shadows to create a sense of physical layering. A specialized **"AI Frost"** treatment—a controlled application of glassmorphism—is reserved exclusively for intelligent discovery features, distinguishing them from the standard transactional UI.

## Colors
This design system utilizes a high-impact palette led by **Zomato Red**, used primarily for calls-to-action and critical brand moments. The core experience is built upon a deep "Midnight" foundation (`#020617`), which provides maximum contrast for high-fidelity food photography.

- **Primary Red:** High saturation for action and branding.
- **Surface Neutrals:** Tiered shades of slate and navy to define hierarchy.
- **Functional Accents:** Gold is strictly reserved for ratings and "Pro" status indicators. Success Green is used for sustainability messaging and order confirmations.
- **Contrast Strategy:** All text on dark backgrounds must meet WCAG AA standards, utilizing pure white for headings and muted slate for metadata.

## Typography
The typography strategy pairs the geometric clarity of **Lexend** for headlines with the utilitarian precision of **Inter** for body and UI labels.

- **Headlines:** Use Lexend with tighter letter-spacing to create a punchy, editorial feel. 
- **Readability:** Inter is used for all descriptive text and restaurant menus to ensure maximum legibility at small sizes on mobile devices.
- **Hierarchy:** High weight contrast (Bold vs. Regular) is preferred over color shifts to denote importance.

## Layout & Spacing
The layout follows a strict **8px grid system**, ensuring vertical rhythm across all components.

- **Grid:** A 12-column fluid grid for desktop and a 4-column grid for mobile. 
- **Safe Areas:** Generous 16px horizontal margins on mobile to prevent content from touching the screen edges.
- **Rhythm:** Spacing increments of 8px (8, 16, 24, 32, 48, 64) are used for all padding and margins. 
- **Content-First:** Imagery should occupy 40-60% of the viewport in discovery phases, with text density increasing during the checkout and menu-browsing phases.

## Elevation & Depth
Depth is created through a combination of **Tonal Layers** and **Refined Shadows**.

- **Level 0 (Background):** Deepest color (#020617).
- **Level 1 (Cards):** Surface color (#0F172A) with a 1px subtle border (#1E293B).
- **Level 2 (Active/Hover):** Raised with an ambient shadow (0px 8px 24px rgba(0,0,0,0.4)).
- **AI Sections:** Apply a backdrop filter (Blur: 12px) and a semi-transparent white stroke (10% opacity) to create a "floating glass" effect that sits above the primary UI.

## Shapes
The design system uses a consistent **Rounded (12px to 16px)** corner radius to soften the high-contrast aesthetic.

- **Standard Components:** Buttons and Input fields use a 12px radius.
- **Containers:** Restaurant cards and high-level surface containers use a 16px radius.
- **Micro-elements:** Rating badges and tags use a 6px radius or "Pill" shapes depending on the context.

## Components
- **Buttons:** Primary buttons are Zomato Red with white text. Secondary buttons use a transparent background with a 1px slate border.
- **Restaurant Cards:** Feature edge-to-edge photography at the top with a 16px padding for the info area below.
- **Rating Badges:** Solid Gold (#8C6115) background with white bold text, typically positioned in the top-right corner of restaurant cards.
- **Inputs:** Darker than the surface color with a focus state that glows slightly in Zomato Red.
- **Chips:** Low-profile slate backgrounds for filters; active filters toggle to Zomato Red.
- **AI Recommendation Module:** Uses the "AI Frost" glass effect with a subtle prismatic gradient border to distinguish it from manual search results.