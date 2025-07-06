import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.config import Config

# Enable fullscreen
Config.set('graphics', 'fullscreen', 'auto')
Window.fullscreen = 'auto'

# 🔗 Data + Google API setup
DATA_URL = "https://aadi-playz23.github.io/my-hosting/data.json"
GOOGLE_API_KEY = "AIzaSyCKyUp4kMwS1hfab7JyKcOdUw0pYFx60Zw"
GOOGLE_CX = "10a12e92a5daa49c1"

# 📌 Fetch medicine usage snippet
def fetch_medicine_uses_google(medicine_name, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": f"What is {medicine_name} used for?",
        "num": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        if "items" in results and results["items"]:
            return results["items"][0].get("snippet", "No usage info found.")
        return "No information found online."
    except Exception as e:
        return f"Error fetching uses: {e}"

# 🖼️ Fetch medicine image
def fetch_medicine_image_google(medicine_name, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": f"{medicine_name} medicine packaging",
        "searchType": "image",
        "num": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        if "items" in results and results["items"]:
            return results["items"][0].get("link", "")
        return ""
    except Exception as e:
        return ""

class MedicineFinder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=0, **kwargs)
        self.data_loaded = False
        self.medicine_data = []

        # Header
        header = BoxLayout(size_hint_y=None, height=60, padding=15, spacing=10)
        header.add_widget(Label(text="💊 Medicine Finder", font_size=20, bold=True, color=(1, 1, 1, 1)))
        with header.canvas.before:
            Color(0.15, 0.3, 0.6, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header, pos=self._update_header)
        self.add_widget(header)

        # Input fields
        input_section = BoxLayout(orientation='vertical', padding=15, spacing=10, size_hint_y=None)
        input_section.bind(minimum_height=input_section.setter('height'))

        self.name_input = self.create_input("🔍 Medicine Name")
        self.type_input = self.create_input("📦 Type (Any, Allopath, etc.)")
        self.manufacturer_input = self.create_input("🏭 Manufacturer")

        self.search_button = Button(
            text="🔎 Search",
            size_hint_y=None,
            height=45,
            background_color=(0.2, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.search_button.bind(on_press=self.threaded_search)

        input_section.add_widget(self.name_input)
        input_section.add_widget(self.type_input)
        input_section.add_widget(self.manufacturer_input)
        input_section.add_widget(self.search_button)
        self.add_widget(input_section)

        # Image and Result Display
        self.image = AsyncImage(size_hint_y=None, height=180)

        self.result_label = Label(
            text="Enter details and tap Search",
            halign="left",
            valign="top",
            markup=True,
            color=(1, 1, 1, 1),
            font_size=17,
            size_hint_y=None,
            text_size=(Window.width - 40, None)
        )
        self.result_label.bind(texture_size=self._update_label_height)

        self.result_container = GridLayout(cols=1, size_hint_y=None, padding=15, spacing=10)
        self.result_container.bind(minimum_height=self.result_container.setter('height'))
        self.result_container.add_widget(self.image)
        self.result_container.add_widget(self.result_label)

        with self.result_container.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.bg_rect = Rectangle(size=self.result_container.size, pos=self.result_container.pos)
        self.result_container.bind(size=self._update_bg, pos=self._update_bg)

        scroll = ScrollView()
        scroll.add_widget(self.result_container)
        self.add_widget(scroll)

    def _update_header(self, instance, value):
        self.header_rect.size = instance.size
        self.header_rect.pos = instance.pos

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def create_input(self, hint):
        return TextInput(
            hint_text=hint,
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size=15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=(10, 10)
        )

    def _update_label_height(self, instance, value):
        self.result_label.height = value[1]

    def load_data(self):
        if not self.data_loaded:
            try:
                response = requests.get(DATA_URL)
                response.raise_for_status()
                raw_data = response.json()
                self.medicine_data = [
                    {
                        **med,
                        "_name": med.get("name", "").lower(),
                        "_type": med.get("type", "").lower(),
                        "_manufacturer": med.get("manufacturer_name", "").lower()
                    }
                    for med in raw_data
                ]
                self.data_loaded = True
            except Exception as e:
                self.result_label.text = f"[color=ff0000]❌ Failed to load data: {e}[/color]"

    def threaded_search(self, instance):
        threading.Thread(target=self.search_medicine, daemon=True).start()

    def search_medicine(self):
        self.result_label.text = "🔄 Searching..."
        self.image.source = ""

        self.load_data()
        if not self.data_loaded:
            return

        name = self.name_input.text.strip().lower()
        mtype = self.type_input.text.strip().lower()
        manufacturer = self.manufacturer_input.text.strip().lower()

        filtered = [
            med for med in self.medicine_data
            if (not name or med["_name"].startswith(name))
            and (mtype == "any" or med["_type"].startswith(mtype))
            and (not manufacturer or med["_manufacturer"].startswith(manufacturer))
        ]

        if not filtered:
            self.result_label.text = "[color=ff0000]❌ No medicine found.[/color]"
            return

        med = filtered[0]
        name_display = med.get("name") or "Not available"
        manufacturer = med.get("manufacturer_name") or "Not available"
        mtype = med.get("type") or "Not available"
        price = med.get("price") or "Not available"

        uses = fetch_medicine_uses_google(name_display, GOOGLE_API_KEY, GOOGLE_CX)
        image_url = fetch_medicine_image_google(name_display, GOOGLE_API_KEY, GOOGLE_CX)

        self.result_label.text = (
            f"[b]🩺 Name:[/b] {name_display}\n\n"
            f"[b]🏭 Manufacturer:[/b] {manufacturer}\n\n"
            f"[b]💊 Type:[/b] {mtype}\n\n"
            f"[b]💰 Price:[/b] ₹{price}\n\n"
            f"[b]📌 Uses:[/b] {uses}"
        )
        self.image.source = image_url

class MedicineApp(App):
    def build(self):
        self.title = "💊 Medicine Finder"
        return MedicineFinder()

if __name__ == "__main__":
    MedicineApp().run()
