import dearpygui.dearpygui as dpg
import dearpygui.demo
from threading import Timer

score = 0
increment = 1

ups = [10]

ver = "0.0.1"

achievements = ["Upgrades", "100!"]
achievement_states = [False for _ in range(len(achievements))]
achievement_descriptions = ["You have bought an upgrade", "You have 100 points"]

dpg.create_context()

def cheating(isScore = True) -> None:
    global score, increment
    if isScore:
        score += 1000000
    else:
        increment += 1000000

def _hide():
    dpg.hide_item("toast")

def save(showToast = True):
    global score, increment, ups, achievement_states
    with open("save.dat", "w") as f:
        f.write(str(score) + "\n")
        f.write(str(increment) + "\n")
        for i in ups:
            f.write(str(i) + "\n")
        for i in achievement_states:
            if i:
                f.write("1\n")
            else:
                f.write("0\n")
    #show the save message toast
    if not showToast: return
    dpg.show_item("toast")
    Timer(2, _hide).start()

def load():
    global score, increment, ups, achievement_states
    try:
        with open("save.dat", "r") as f:
            score = int(f.readline())
            increment = int(f.readline())
            for i in range(len(ups)):
                ups[i] = int(f.readline())
            for i in range(len(achievement_states)):
                achievement_states[i] = bool(int(f.readline()))
    except:
        #print an error message in red
        print("\u001b[31mError loading save file" + u"\u001b[0m")
        save(False)

def update():
    global score, increment, ups, achievement_states, achievement_descriptions, achievements
    dpg.set_value("score", f"You have {score} points")
    dpg.set_value("increment", f"You get {increment} points per click")
    for i in range(len(ups)):
        dpg.set_value("upgrade" + str(i + 1), f"Cost: {ups[i]} points")
    for i in range(len(achievement_states)):
        if achievement_states[i]:
            dpg.set_value("achievement" + str(i), f"{achievements[i]}: {achievement_descriptions[i]}")
    if increment == 2:
        achievement_states[0] = True
    if score >= 100 and not achievement_states[1]:
        achievement_states[1] = True


def increment_score()->None:
    global score, increment
    score += increment

def upgrade_increment(upgrade):
    global score, increment, ups
    if score >= ups[upgrade]:
        increment += 1
        score -= ups[upgrade]
        ups[upgrade] = round(ups[upgrade] * 1.35)

with dpg.window(tag="main_window", label="Main Window"):
    with dpg.menu_bar():
        with dpg.menu(label="Upgrades"):
            dpg.add_menu_item(label="Open", callback=lambda: dpg.show_item("upgrades"))
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Save", callback=save)
            dpg.add_menu_item(label="About", callback=lambda: dpg.show_item("about"))
        with dpg.menu(label="Achievements"):
            dpg.add_menu_item(label="Open", callback=lambda: dpg.show_item("achievements"))
    dpg.add_text(f"You have {score} points", tag="score")
    dpg.add_text(f"You get {increment} points per click", tag="increment")
    dpg.add_button(label="Add Point", callback=increment_score)

    dpg.add_text("Saved Game!", tag="toast", show=False)

with dpg.window(tag="upgrades", label="Upgrades", show=False, no_resize=True):
    dpg.add_button(label="Add 1 point per click", callback=lambda: upgrade_increment(0))
    dpg.add_text(f"Cost: {ups[0]} points", tag="upgrade1")

with dpg.window(tag="about", label="About", show=False, no_resize=True):
    dpg.add_text("Made by SuperjakeyLKR")
    dpg.add_text(f"Version {ver}")

with dpg.window(tag="achievements", label="Achievements", show=False, width=300, height=300, no_resize=True):
    for i in range(len(achievements)):
        dpg.add_text(f"{achievements[i]}: Locked", tag=f"achievement{i}")


with dpg.window(tag="debug", label="Debug", show=False):
    dpg.add_text("Debug window")
    dpg.add_button(label="Score + 1000000",callback=lambda:cheating())
    dpg.add_button(label="Increment + 1000000",callback=lambda:cheating(False))


dpg.create_viewport(title="Clicker Game", width=1280//2, height=720//2)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)

load()
dpg.set_item_pos("upgrades", [0, 100])
dpg.set_item_pos("about", [0, 100])
dpg.set_item_pos("achievements", [0, 100])
dpg.set_item_pos("debug", [0, 100])

while dpg.is_dearpygui_running():
    #if F12 is pressed, show the demo
    if dpg.is_key_pressed(dpg.mvKey_F12):
        dearpygui.demo.show_demo()
    #if the user inputs l, k and r, open the dev console
    if dpg.is_key_down(dpg.mvKey_L) and dpg.is_key_down(dpg.mvKey_K) and dpg.is_key_down(dpg.mvKey_R):
        dpg.show_item("debug")
    dpg.render_dearpygui_frame()
    update()

dpg.destroy_context()
