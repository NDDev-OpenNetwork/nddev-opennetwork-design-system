# OpenNetwork visual language

Use the platform's OpenNetwork direction, not an independently themed NDS skin.
The bright yellow brand, gold controls, neutral surfaces, IBM Plex Sans and
authentic mark come from the recorded platform source. Dark and light palettes
have separate text, fill, heading, outline and status roles; a decorative brand
color must not replace a contrast-corrected text role.

Use the public tokens from `tokens/tokens.json`. Every status has text, icon and
color; color is never the only signal. Focus states, keyboard navigation,
contrast and reduced-motion behavior are required for all components.

The Flutter kit maps primary/secondary/quiet buttons, fields/selects, cards,
menus, navigation and chips onto native semantics. It retains the platform's
geometry and states without copying marketing pages or web layout machinery.
Controls use at least the native 48 px target; natural height grows with text
scale. Disabled buttons are hollow and non-interactive; errors retain text.
Product layouts own their content and composition, never independent tokens.

