MM_TO_INCH = 1 / 25.4
DPI = 300

CARD_WIDTH = int(63 * MM_TO_INCH * DPI)   # ~744 px
CARD_HEIGHT = int(88 * MM_TO_INCH * DPI)  # ~1039 px

A4_WIDTH = int(210 * MM_TO_INCH * DPI)    # ~2480 px
A4_HEIGHT = int(297 * MM_TO_INCH * DPI)   # ~3508 px

from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_card(name, race, team, team_effect, value, rarity, suit, text):
    img = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    # Load fonts (use a .ttf file you have)
    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    race_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    font_suit = ImageFont.truetype("DejaVuSans.ttf", 72)
    font_value = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 40)
    font_text = ImageFont.truetype("DejaVuSans.ttf", 40)

    # Border
    draw.rectangle([0, 0, CARD_WIDTH-1, CARD_HEIGHT-1], outline="black", width=4)

    # Name (top)
    draw.text((CARD_WIDTH//2, 20), name, font=font_title, fill="black", anchor="ma")

    # Value and suit (top right)
    draw.text((CARD_WIDTH - 100, 20), suit, font=font_suit, fill="black")
    draw.text((CARD_WIDTH - 100 + (+5 if value < 10 else -5), 20 + 72), str(value), font=font_value, fill="black")

    # Text box for race and rarity
    race_text_box = (20, CARD_HEIGHT // 2 - 60, CARD_WIDTH - 20, CARD_HEIGHT // 2 - 5)
    draw.rectangle(race_text_box, outline="black")
    # Race
    draw.text((30, CARD_HEIGHT // 2 - 50), race, font=race_font, fill="green")
    # Rarity
    draw.text((CARD_WIDTH - 100, CARD_HEIGHT // 2 - (50 if len(rarity) < 4 else 100)), str(rarity), font=race_font, fill="blue")

    # Team text box    
    team_y = CARD_HEIGHT // 2 + 5
    effect_y = CARD_HEIGHT // 2 + 200
    team_text_box = (20, team_y, CARD_WIDTH - 20, effect_y-5)
    draw.rectangle(team_text_box, outline="black")
    # Team
    draw.text((CARD_WIDTH // 2, team_y), str(team), font=race_font, fill="gray", anchor="ma")
    team_lines = textwrap.wrap(team_effect, width=32)
    y = team_y + 40
    for line in team_lines:
        draw.text((30, y), line, font=font_text, fill="black")
        y += 40

    # Text box
    text_box = (20, effect_y, CARD_WIDTH - 20, CARD_HEIGHT - 50)
    draw.rectangle(text_box, outline="black")

    # Simple text wrapping
    lines = textwrap.wrap(text, width=32)

    y = effect_y + 20
    for line in lines:
        draw.text((30, y), line, font=font_text, fill="black")
        y += 40

    return img

def create_a4_sheet(cards):
    sheet = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    cols = 3
    rows = 3

    margin_x = (A4_WIDTH - cols * CARD_WIDTH) // (cols + 1)
    margin_y = (A4_HEIGHT - rows * CARD_HEIGHT) // (rows + 1)

    i = 0
    for r in range(rows):
        for c in range(cols):
            if i >= len(cards):
                break

            x = margin_x + c * (CARD_WIDTH + margin_x)
            y = margin_y + r * (CARD_HEIGHT + margin_y)

            sheet.paste(cards[i], (x, y))
            i += 1

    return sheet

cards = []

for i in range(8):
    card = create_card(
        name=f"Hvězdná Fregata ",
        race="Flora",
        team="Cacti",
        team_effect="Karta Cacti je bez efektu pokud je vedle jiné Cacti, Tým: +10 za každý kaktus",
        value=i+7,
        rarity="R:3",
        suit="♣",
        text="+2 za každý Stroj vedlé této karty; Bez efektu pokud není vedle karty Octopus."
    )
    cards.append(card)

sheet = create_a4_sheet(cards)
sheet.save("cards_a4.png", dpi=(300, 300))