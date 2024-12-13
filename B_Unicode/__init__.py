bl_info = {
    "name": "B Unicode",
    "author": "Dinesh",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "description": "Access Unicode characters in Text Editor, VSE, and 3D Viewport.",
    "category": "3D Viewport, VSE, Text Editor",
}

import bpy

# Shared function to draw Unicode panels
def draw_unicode_panel(layout, settings):
    # Dropdown for categories
    row = layout.row()
    row.prop(settings, "active_category", text="Category", icon='OUTLINER_COLLECTION')

    # Get unicode characters based on the selected category
    active_category = settings.active_category
    unicode_characters = get_unicode_characters(active_category)

    # Display characters in a grid
    grid = layout.grid_flow(row_major=True, columns=5, align=True)
    for char in unicode_characters[:100]:  # Limit to first 50 characters
        grid.operator("text.insert_unicode", text=char).unicode_char = char


# Panels
class UnicodeCollectionPanelTextEditor(bpy.types.Panel):
    bl_label = "Unicode Collection"
    bl_idname = "TEXT_PT_unicode_collection"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Unicode'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.unicode_settings
        draw_unicode_panel(layout, settings)


class UnicodeCollectionPanelVSE(bpy.types.Panel):
    bl_label = "Unicode Collection"
    bl_idname = "VSE_PT_unicode_collection"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Unicode'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.unicode_settings
        draw_unicode_panel(layout, settings)


class UnicodeCollectionPanelViewport(bpy.types.Panel):
    bl_label = "Unicode Collection"
    bl_idname = "VIEW3D_PT_unicode_collection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unicode'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.unicode_settings
        draw_unicode_panel(layout, settings)


# Operator
class InsertUnicodeOperator(bpy.types.Operator):
    bl_idname = "text.insert_unicode"
    bl_label = "Insert Unicode Character"

    unicode_char: bpy.props.StringProperty()

    def execute(self, context):
        # Handle different editor types
        space_type = context.space_data.type
        if space_type == 'TEXT_EDITOR':
            # Insert into the Text Editor
            text = context.space_data.text
            if text:
                text.write(self.unicode_char)
        elif space_type == 'SEQUENCE_EDITOR':
            # Insert as a text strip in the VSE
            scene = context.scene
            strip = scene.sequence_editor.active_strip
            if strip and strip.type == 'TEXT':
                strip.text += self.unicode_char
            else:
                self.report({'WARNING'}, "Please select a text strip to add the character.")
        elif space_type == 'VIEW_3D':
            # Insert into a 3D Viewport Text Object
            text_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'FONT']
            if text_objects:
                # Add the unicode character to the first text object found
                text_object = text_objects[0]
                text_object.data.body += self.unicode_char
                self.report({'INFO'}, "Unicode added to 3D Viewport text object.")
            else:
                self.report({'WARNING'}, "Please select a text object in the 3D Viewport.")
        return {'FINISHED'}


# Property Group
class UnicodeSettings(bpy.types.PropertyGroup):
    active_category: bpy.props.EnumProperty(
        name="Category",
        items = [
            ("Symbols", "Symbols", ""),
            ("Greek Letters", "Greek Letters", ""),
            ("Math Operators", "Math Operators", ""),
            ("Currency", "Currency", ""),
            ("Arrow & Bracket", "Arrow & Bracket", ""),
            ("Ballot & Marks", "Ballot & Marks", ""),
            ("Roman Numerals", "Roman Numerals", ""),
            ("Heart", "Heart Symbols", ""),
            ("Musical", "Musical Symbols", ""),
            ("Hand Emojis", "Hand Emojis", ""),
            ("Face Emojis", "Face Emojis", ""),
            ("Plants", "Plants", ""),
            ("Weather", "Weather", ""),
            ("Fruits", "Fruits", ""),
            ("Vegetables", "Vegetables", ""),
            ("Food & Drink", "Food & Drink", ""),
            ("Animal & Nature", "Animal & Nature", ""),
            ("Space & Celestial", "Space & Celestial", ""),
            ("Technology", "Technology", ""),
            ("Vehicles", "Vehicles", ""),
            ("Card & Chess", "Card & Chess", ""),
            ("Games", "Games", ""),
            ("Building", "Building", ""),
            ("House & Office", "House & Office", ""),
            ("Other", "Other", "")
        ],
        default="Symbols"
    )


# Function to get Unicode characters by category
def get_unicode_characters(category):
    unicode_categories = {
        "Symbols": ['©', '®', '™', '♱', '☽', '☭','卍', '☢', '⚑', '☮', '☯', '⚠', '⚒', '⚓', '⚔', '⚛', '☣', '⌚', '⌛', '👀', '💢', '☘', '∞', '🐾', '💋', '👣', '☠', '💀', '👻', '🎃', '👑'],
        "Hand Emojis": ['👋', '🤚', '✋', '🖐️', '👏', '🤲', '👌', '✌️', '🤞', '🤟', '🤘', '👈', '👉', '👆', '👇', '👍', '👎'],
        "Face Emojis": ['😀', '😁', '😂', '🤣', '😃', '😄', '😅', '😆', '😇', '😈', '😉', '😊', '😋', '😌', '😍', '😘', '😗', '😙', '😚', '😜', '😝', '😛', '😎', '😏', '😒', '😓', '😔', '😕', '😖', '😗', '😙', '😚', '😜', '😝', '😛', '😋', '😇', '😎', '🤓', '😏', '😺', '🙃', '🥺', '🤗', '🤭', '🤫', '🤔', '🤐', '😶', '😏', '😵', '🤯', '🤠', '😷', '🤒', '🤕', '🤢', '🤧', '😇', '😔'],
        "Plants": ['🌸', '🌺', '🌻', '🌼', '🌷', '🌹', '🥀', '💐', '🌾', '🌱', '🌿', '🍀', '🍁', '🍂', '🍃', '🌳', '🌲', '🎄', '🌴', '🌵'],
        "Weather": ['☀️', '🌤️', '⛅', '🌥️', '☁️', '🌦️', '🌧️', '⛈️', '🌩️', '🌨️', '🌪️', '🌫️', '🌬️', '❄️', '☃️', '⛄', '🌨️', '🧊', '💦', '💧', '🌈', '⚡', '🔥', '💥', '💨', '🌡️'],
        "Fruits": ['🍎', '🍏', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅'],
        "Vegetables": ['🥕', '🌽', '🥒', '🥬', '🥦', '🧄', '🧅', '🍆', '🍠', '🥔', '🌶️'],
        "Food & Drink": ['🍔', '🍟', '🍕', '🌭', '🌮', '🌯', '🥗', '🥙', '🍲', '🍜', '🍝', '🥘', '🥩', '🍖', '🍗', '🍤', '🍳', '🥞', '🧇', '🥓', '🧀', '🥐', '🥖', '🥨', '🥯', '🍞', '🧈', '🧂', '🍿', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬', '🍭', '🍮', '🍯', '🍼', '🥤', '☕', '🍵', '🍶', '🍹', '🍸', '🍺', '🍻', '🥂', '🍾'],
        "Animal & Nature": ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🪲', '🐢', '🐍', '🦎', '🐙', '🦑', '🦐', '🦀', '🐡', '🐠', '🐟', '🐳', '🐋', '🦈', '🐊', '🦧', '🦍', '🦓', '🦒', '🐆', '🐅', '🐘', '🦏', '🦛', '🐪', '🐫', '🦙', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦌', '🐕', '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🕊', '🐇', '🐁', '🐀', '🐿', '🦔', '🐉', '🐲'],
        "Space & Celestial": ['🌌', '🌠', '🌇', '🌅', '🌄', '🌉', '🌃', '🌆', '🌗', '🌖', '🌕', '🌔', '🌓', '🌒', '🌑', '🌘', '🌎', '🌍', '🌏', '🌙', '☀️', '⭐', '🌟', '✨', '🌞', '🌝', '🌚', '🌛', '🌜', '☄️', '🌠', '🪐'],
        "Technology": ['💻', '🖥️', '🖨️', '⌨️', '🖱️', '🖲️', '💽', '💾', '💿', '📀', '🎥', '📷', '📹', '📺', '📻', '📱', '📲', '☎️', '📞', '📟', '📠', '🔋', '🔌', '💡', '🔦', '🕹️', '🖼️', '🪟', '💰', '💵', '💴', '💶', '💷', '💳'],
        "Vehicles": ['🚗', '🚕', '🚙', '🚌', '🚎', '🏎️', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🚲', '🛴', '🛵', '🏍️', '🛺', '✈️', '🛫', '🛬', '🛩️', '🚁', '🛸', '🛶', '🚀', '🛰️', '🚢', '⛴️', '🛳️', '⛵', '🚤', '🛥️', '🛶', '⛽', '🚂', '🚃', '🚄', '🚅', '🚆', '🚇', '🚛', '🚜', '🛹', '🚡', '🚠', '🚟'],
        "Greek Letters": ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω'],
        "Math Operators": ['∞', 'π', '∑', '√', '≈', '≠', '≡', '±', '∓', '≡', '≪', '≫', '∏', '∂', '∇', '∫', '∮', '∝', '∩', '∪', '⊂', '⊃', '⊆', '⊇', '⊥', '∠', '∼', '≺', '≻', '⊕', '⊗', '⊥', '≻'],
        "Currency": ['$', '€', '£', '¥', '₹', '₣', '₤', '₣', '₽', '₳', '฿', '￠', '₡', '₢', '₫', '₦', '₱', '¤', '₴', '₸', '₰', '៛', '₪', '₪', '₠', '﷼', '円', '元', '圓', '㍐', '원', '৳', '৲', '₮'],
        "Arrow & Bracket": ['←', '↑', '→', '↓', '↔️', '↕️', '🔼', '🔽', '↗', '↖', '↘', '↙', '➔', '➞', '➝', '⇄', '⇅','〈', '〉', '❪', '❫', '❰', '❱', '❲', '❳', '⟦', '⟧', '⧼', '⧽', '⸨', '⸩', '❮', '❯', '⟪', '⟫', '⦑', '⦒', '︽', '︾'],
        "Ballot & Marks": ['⬛', '♦', '🔶', '🔸', '🔘', 'ℹ', '■', '□', '☑', '☒', '✓', '✔', '✅', '𝤿', '✗', '❌', '❎', '•', '∙', '⊙', '⊚', '⊛', '◉', '○', '◌', '◍', '◎', '●', '◘', '◦', '。', '⁌', '⁍', '◆', '◇', '◈', '★', '☆', '❖', '⋄', '☸', '✤', '✱', '✲', '✦', '✧'],
        "Roman Numerals": ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ', 'Ⅺ', 'Ⅻ', 'Ⅼ', 'Ⅽ', 'Ⅾ', 'Ⅿ'],
        "Heart": ['❦', '♡', '❤', '❤️', '💔', '💝', '💓', '💕', '💖', '💗', '💞', '💘', '💙', '🫀', '💟', '💑', '💏', '❧', '☙', '❥', '❣', '➳', 'ღ', '🎔', '💌'],
        "Musical": ['♩', '♪', '♬', '♭', '♮', '🎶', '🎵', '♫', '🎼', '🎤', '🎧', '🎷', '🎸', '🎹', '🎺', '🎻', '🥁', '🔔', '🔊', '📯', '🎛', '🎚', '🎙', '📻'],
        "Card & Chess": ['♠', '♣', '♥', '♦', '♔', '♕', '♖', '♗', '♘', '♙', '♚', '♛', '♜', '♝', '♞', '♟'],
        "Games": ['⚽', '🏀', '🏈', '⚾', '🎾', '🏐', '🎱', '🏓', '🥌', '🏏', '🎳', '🎲', '🧩', '🪀', '🎯', '🎮', '🧸'],
        "Building": ['🏠', '🏡', '🏢', '🏣', '🏥', '🏦', '🏨', '🏩', '🏪', '🏬', '🏛', '💒', '🎪'],
        "House & Office": ['🛋', '🛏', '🪑', '🚪', '🚽', '🧻', '🧴', '🧼', '🛁', '🚿', '🧹', '🧺', '🛒', '🖊', '🖋', '✒', '📚', '📖', '📎', '📌', '📏', '📐', '🗂', '📄', '📅', '📉', '📊', '📈'],
        "Other": ['🦠', '🚰', '💉', '💊', '🚦', '🚥', '🔮', '🎉', '🎊', '🎂', '🎁', '🎈', '💡', '🎇', '💫', '🎆', '🏳', '🏴', '🏳️‍🌈', '🏳️', '🏴‍☠️',]

    }
    return unicode_categories.get(category, [])


classes = (
    UnicodeCollectionPanelTextEditor,
    UnicodeCollectionPanelVSE,
    UnicodeCollectionPanelViewport,
    InsertUnicodeOperator,
    UnicodeSettings
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.unicode_settings = bpy.props.PointerProperty(type=UnicodeSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.unicode_settings


if __name__ == "__main__":
    register()
