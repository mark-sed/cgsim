import csv
from sys import argv

MM_TO_INCH = 1 / 25.4
DPI = 300

CARD_WIDTH = int(63 * MM_TO_INCH * DPI)   # ~744 px
CARD_HEIGHT = int(88 * MM_TO_INCH * DPI)  # ~1039 px

A4_WIDTH = int(210 * MM_TO_INCH * DPI)    # ~2480 px
A4_HEIGHT = int(297 * MM_TO_INCH * DPI)   # ~3508 px

from PIL import Image, ImageDraw, ImageFont
import textwrap

def suit2symbol(suit):
    if suit == "Srdce":
        return ("♥", "red")
    elif suit == "Káry":
        return ("♦", "red")
    elif suit == "Piky":
        return ("♠", "black")
    elif suit == "Kříže":
        return ("♣", "black")
    assert False, "Missing suit " + suit

def get_race_color(race):
    if race == "Flora":
        return "green"
    elif race == "Fauna":
        return (255, 100, 100)
    elif race == "Stroje":
        return (80, 80, 80)
    elif race == "Lidé":
        return (245, 188, 66)
    elif race == "Jiné":
        return (66, 121, 143)

    return "black"

def create_card(name, race, team, team_effect, value, rarity, suit, text):
    img = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    suit, suit_color = suit2symbol(suit)

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
    draw.text((CARD_WIDTH - 100, 20), suit, font=font_suit, fill=suit_color)
    draw.text((CARD_WIDTH - 100 + (+5 if value < 10 else -5), 20 + 72), str(value), font=font_value, fill=suit_color)

    # Text box for race and rarity
    race_text_box = (20, CARD_HEIGHT // 2 - 60, CARD_WIDTH - 20, CARD_HEIGHT // 2 - 5)
    draw.rectangle(race_text_box, outline="black")
    # Race
    draw.text((30, CARD_HEIGHT // 2 - 50), race, font=race_font, fill=get_race_color(race))
    # Rarity
    draw.text((CARD_WIDTH - 100, CARD_HEIGHT // 2 - (50 if len(rarity) < 4 else 100)), str(rarity), font=race_font, fill="blue")

    # Team text box    
    team_y = CARD_HEIGHT // 2 + 5
    effect_y = CARD_HEIGHT // 2 + 200
    team_text_box = (20, team_y, CARD_WIDTH - 20, effect_y-5)
    draw.rectangle(team_text_box, outline="black")
    # Team
    draw.text((CARD_WIDTH // 2, team_y), str(team), font=race_font, fill="black", anchor="ma")
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

def create_item_card(name, item_type, effect):
    img = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    # Fonts
    font_type = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
    font_effect = ImageFont.truetype("DejaVuSans.ttf", 40)

    # Colors by type
    type_colors = {
        "artefakt": "#eba834",
        "item": "#1ad2db",
        "aréna": "#9e0b12"
    }

    item_type_lower = item_type.lower()
    type_color = type_colors.get(item_type_lower, "black")

    # Outer border
    draw.rectangle(
        [0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1],
        outline="black",
        width=6
    )

    # Type text at top
    draw.text(
        (CARD_WIDTH // 2, 30),
        item_type if item_type != "Item" else "Věc",
        font=font_type,
        fill=type_color,
        anchor="ma"
    )

    # Name in middle
    draw.text(
        (CARD_WIDTH // 2, CARD_HEIGHT // 2),
        name,
        font=font_title,
        fill="black",
        anchor="mm"
    )

    # Bottom effect box
    effect_box_margin = 30
    effect_box_height = 320

    effect_box = (
        effect_box_margin,
        CARD_HEIGHT - effect_box_height - effect_box_margin,
        CARD_WIDTH - effect_box_margin,
        CARD_HEIGHT - effect_box_margin
    )

    draw.rectangle(effect_box, outline=type_color, width=4)

    # Wrap effect text
    lines = textwrap.wrap(effect, width=30)

    # Center lines vertically inside box
    line_height = 45
    total_text_height = len(lines) * line_height

    y = effect_box[1] + (
        (effect_box_height - total_text_height) // 2
    )

    for line in lines:
        draw.text(
            (effect_box[0] + 20, y),
            line,
            font=font_effect,
            fill="black"
        )
        y += line_height

    return img

def create_a4_sheet(cards):
    sheet = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    cols = 3
    rows = 3

    margin_x = 2#(A4_WIDTH - cols * CARD_WIDTH) // (cols + 1)
    margin_y = 2#(A4_HEIGHT - rows * CARD_HEIGHT) // (rows + 1)

    i = 0
    for r in range(rows):
        for c in range(cols):
            if i >= len(cards):
                break

            x = 100 + margin_x + c * (CARD_WIDTH + margin_x)
            y = 100 + margin_y + r * (CARD_HEIGHT + margin_y)

            sheet.paste(cards[i], (x, y))
            i += 1

    return sheet

card_data = []
item_data = []
arena_data = []

with open(argv[1], "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        card_data.append(row)

with open(argv[2], "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        item_data.append(row)

with open(argv[3], "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        arena_data.append(row)

card_imgs = []

sheet_num = 1
for i, c in enumerate(card_data, 1):
    card = create_card(
        name=c["Jméno"],
        race=c["Rasa"],
        team=c["Tým"],
        team_effect=c["Efekt týmu"],
        value=int(c["Hodnota"]),
        rarity=c["Rarita"],
        suit=c["Barva"],
        text=c["Efekt"]
    )
    card_imgs.append(card)

    if i % 9 == 0 or i == len(card_data):
        sheet = create_a4_sheet(card_imgs)
        sheet.save(f"output/cards_a4_{sheet_num}.png", dpi=(300, 300))
        sheet_num += 1
        card_imgs.clear()

card_imgs.clear()

sheet_num = 1
for i, c in enumerate(item_data, 1):
    card = create_item_card(
        name=c["Jméno"],
        item_type=c["Typ"],
        effect=c["Efekt"]
    )
    card_imgs.append(card)

    if i % 9 == 0 or i == len(item_data):
        sheet = create_a4_sheet(card_imgs)
        sheet.save(f"output/items_a4_{sheet_num}.png", dpi=(300, 300))
        sheet_num += 1
        card_imgs.clear()

card_imgs.clear()

sheet_num = 1
for i, c in enumerate(arena_data, 1):
    card = create_item_card(
        name=c["Jméno"],
        item_type="Aréna",
        effect=c["Efekt"]
    )
    card_imgs.append(card)

    if i % 9 == 0 or i == len(arena_data):
        sheet = create_a4_sheet(card_imgs)
        sheet.save(f"output/arenas_a4_{sheet_num}.png", dpi=(300, 300))
        sheet_num += 1
        card_imgs.clear()