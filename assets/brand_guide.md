# CGI-Style Brand Guide (Demo)

This document describes the branding assets and usage guidelines for the
Candidate Ranker demo application.

---

## Color Palette

| Color Name          | Hex Code  | Usage                                      |
|---------------------|-----------|-------------------------------------------|
| CGI Red (Primary)   | `#E31937` | Primary buttons, links, accent elements   |
| CGI Orange          | `#FF6B00` | Gradient endpoint, hover states           |
| Text Color          | `#333333` | Body text, headings                       |
| Background          | `#FFFFFF` | Main content background                   |
| Secondary Background| `#F3F6F9` | Sidebar, cards, secondary sections        |
| White               | `#FFFFFF` | Text on dark/gradient backgrounds         |

---

## Logo Files

### Primary Logo
- **File**: `assets/logo.png` or `assets/CGI_logo_color_rgb.png`
- **Recommended width**: 200–400 pixels for header
- **Alt text**: "CGI-style logo (anonymized demo)"

### Logo Variants
| Filename                     | Use Case                              |
|------------------------------|---------------------------------------|
| `CGI_logo_color_rgb.png`     | Standard use on light backgrounds     |
| `CGI_logo_color_rgb.svg`     | Scalable vector for any size          |
| `CGI_logo_rgb_white.png`     | Use on dark or gradient backgrounds   |
| `CGI_logo_rgb_white.svg`     | White logo vector version             |
| `logo.png`                   | Fallback/alias (symlink or copy)      |

### Favicon
- **File**: `assets/favicon.ico`
- **Size**: 64×64 pixels recommended (also works with 32×32, 16×16)
- **Format**: ICO or PNG

---

## Gradient Assets

### Header Gradient
- **File**: `assets/gradients/header-gradient.svg`
- **Colors**: Linear gradient from CGI Red (`#E31937`) to CGI Orange (`#FF6B00`)
- **Dimensions**: 1920×200 pixels (scales responsively)

### CSS Fallback
If the SVG gradient file is not available, use this CSS gradient:
```css
background: linear-gradient(90deg, #E31937 0%, #FF6B00 100%);
```

### Source Files (Adobe Illustrator)
Located in `assets/gradients/`:
- `CGI_UpdatedGradients_RGB.ai` — RGB color space
- `CGI_UpdatedGradients_CMYK.ai` — CMYK for print
- `CGI-colors-RGB-11-09-2023.ai` — Color palette source

---

## How to Replace Assets

### Replacing the Logo
1. Add your logo file to `assets/` as `logo.png` (or `logo.svg`)
2. Recommended dimensions: 200–400px wide, transparent background
3. Update `BRANDING["logo_path"]` in `streamlit_app.py` if using a different filename

### Replacing the Gradient
1. Create a new SVG or PNG gradient (1920×200 recommended)
2. Save as `assets/gradients/header-gradient.svg` (or `.png`)
3. Update `BRANDING["gradient_file"]` in `streamlit_app.py` if using a different path
4. Alternatively, modify `BRANDING["gradient_css_fallback"]` for a pure CSS gradient

### Changing Colors
1. Edit `BRANDING` dictionary at the top of `streamlit_app.py`
2. Update `.streamlit/config.toml` to match the new theme colors
3. Regenerate gradient assets if needed

---

## Contrast & Accessibility

### Minimum Contrast Ratios (WCAG 2.1 AA)
- **Normal text**: 4.5:1 minimum
- **Large text (18pt+)**: 3:1 minimum
- **UI components**: 3:1 minimum

### Banner Text on Gradient
The demo banner uses white text (`#FFFFFF`) on the gradient background.
To ensure readability:
- A semi-transparent overlay (`rgba(0,0,0,0.35)`) is applied behind banner text
- This maintains contrast ratio above 4.5:1

### Contrast Check Function
The app includes a `check_contrast_ratio()` function in `utils.py` that:
- Calculates relative luminance of foreground/background colors
- Logs a warning if contrast ratio falls below 4.5:1
- Can be called during app startup for accessibility validation

---

## Typography

### Recommended Fonts
- **Primary**: System sans-serif (Streamlit default)
- **Alternatives**: Inter, Roboto, Open Sans

### Text Sizes
- **Hero title**: 2rem (32px)
- **Section headers**: 1.5rem (24px)
- **Body text**: 1rem (16px)
- **Small/caption**: 0.875rem (14px)

---

## Demo Disclaimer

This branding is for demonstration purposes only and uses CGI-style colors
and patterns. For production use with actual CGI branding, obtain proper
authorization and use official brand assets from CGI's brand portal.

**Banner text must always be displayed:**
> "DEMO ONLY — Anonymized data — Not for real hiring decisions."
