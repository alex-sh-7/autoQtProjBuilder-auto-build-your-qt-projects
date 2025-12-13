import os
import toml
import subprocess
import sys
import glob

# ---------------- ПУТИ ---------------- #
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(PROJECT_ROOT, "build-script_config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.toml")
DEFAULT_BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

# ---------------- ЛОКАЛИЗАЦИЯ ---------------- #

LANG = {
    "en": {
        "language_name": "English",
        "main_menu_start": "Start",
        "main_menu_settings": "Settings",
        "main_menu_quit": "Quit",
        "start_menu_title": "Build Menu",
        "start_menu_build_release": "Build release version",
        "start_menu_build_beta": "Build beta version",
        "start_menu_build_debug": "Build debug version",
        "start_menu_back": "Back",
        "run_menu_title": "Run Output",
        "run_menu_run": "Run the output file",
        "run_menu_back": "Back",
        "settings_title": "Settings",
        "settings_change_qt": "Change Qt path",
        "settings_change_msvc": "Change MSVC path",
        "settings_restore": "Restore defaults (delete config)",
        "settings_back_save": "Back and Save",
        "settings_back_cancel": "Back and Cancel",
        "info_auto_qt": "[INFO] Performing auto-search for Qt...",
        "info_auto_msvc": "[INFO] Performing auto-search for MSVC / x64 Native Tools...",
        "warning_qt": "[WARNING] Auto-search could not find Qt. Set it manually in Settings.",
        "warning_msvc": "[WARNING] Auto-search could not find MSVC / x64 Native Tools. Set it manually in Settings.",
        "error_qt": "[ERROR] Qt path not found. Set it manually in Settings.",
        "error_msvc": "[ERROR] MSVC / x64 Native Tools path not found. Set it manually in Settings.",
        "info_building": "[INFO] Setting up MSVC environment and building ({type})...",
        "info_build_succeeded": "[INFO] Build succeeded!",
        "error_build_failed": "[ERROR] Build failed. Check CMake, Ninja, and Qt/MSVC paths.",
        "info_config_saved": "[INFO] Config saved",
        "info_config_deleted": "[INFO] Config deleted. Auto-search will run next time.",
        "language_select_title": "Select Language",
        "language_option_en": "English",
        "language_option_ru": "Русский",
        "language_option_uk": "Українська",
        "language_option_de": "Deutsch",
        "language_option_fr": "Français",
        "ninja_warning": "[!] Ninja must be installed and added to PATH"
    },
    "ru": {
        "language_name": "Русский",
        "main_menu_start": "Начать сборку",
        "main_menu_settings": "Настройки",
        "main_menu_quit": "Выход",
        "start_menu_title": "Меню сборки",
        "start_menu_build_release": "Собрать релизную версию",
        "start_menu_build_beta": "Собрать бета-версию",
        "start_menu_build_debug": "Собрать отладочную версию",
        "start_menu_back": "Назад",
        "run_menu_title": "Запуск приложения",
        "run_menu_run": "Запустить приложение",
        "run_menu_back": "Назад",
        "settings_title": "Настройки",
        "settings_change_qt": "Изменить путь Qt",
        "settings_change_msvc": "Изменить путь MSVC",
        "settings_restore": "Восстановить значения по умолчанию (удалить конфиг)",
        "settings_back_save": "Назад и сохранить",
        "settings_back_cancel": "Назад и отменить",
        "info_auto_qt": "[INFO] Выполняется авто-поиск Qt...",
        "info_auto_msvc": "[INFO] Выполняется авто-поиск MSVC / x64 Native Tools...",
        "warning_qt": "[WARNING] Авто-поиск не смог найти Qt. Укажите путь вручную в Настройках.",
        "warning_msvc": "[WARNING] Авто-поиск не смог найти MSVC / x64 Native Tools. Укажите путь вручную в Настройках.",
        "error_qt": "[ERROR] Путь к Qt не найден. Укажите его вручную в Настройках.",
        "error_msvc": "[ERROR] Путь к MSVC / x64 Native Tools не найден. Укажите его вручную в Настройках.",
        "info_building": "[INFO] Настройка MSVC и сборка ({type})...",
        "info_build_succeeded": "[INFO] Сборка успешно завершена!",
        "error_build_failed": "[ERROR] Сборка не удалась. Проверьте CMake, Ninja и пути к Qt/MSVC.",
        "info_config_saved": "[INFO] Конфигурация сохранена",
        "info_config_deleted": "[INFO] Конфиг удалён. Авто-поиск включится при следующем запуске.",
        "language_select_title": "Выберите язык",
        "language_option_en": "English",
        "language_option_ru": "Русский",
        "language_option_uk": "Українська",
        "language_option_de": "Deutsch",
        "language_option_fr": "Français",
        "ninja_warning": "[!] Для сборки обязательно установлен Ninja и добавлен в PATH"
    },
    "uk": {
        "language_name": "Українська",
        "main_menu_start": "Почати збірку",
        "main_menu_settings": "Налаштування",
        "main_menu_quit": "Вихід",
        "start_menu_title": "Меню збірки",
        "start_menu_build_release": "Зібрати релізну версію",
        "start_menu_build_beta": "Зібрати бета-версію",
        "start_menu_build_debug": "Зібрати відлагоджену версію",
        "start_menu_back": "Назад",
        "run_menu_title": "Запуск програми",
        "run_menu_run": "Запустити програму",
        "run_menu_back": "Назад",
        "settings_title": "Налаштування",
        "settings_change_qt": "Змінити шлях Qt",
        "settings_change_msvc": "Змінити шлях MSVC",
        "settings_restore": "Відновити значення за замовчуванням (видалити конфіг)",
        "settings_back_save": "Назад і зберегти",
        "settings_back_cancel": "Назад і відмінити",
        "info_auto_qt": "[INFO] Виконується авто-пошук Qt...",
        "info_auto_msvc": "[INFO] Виконується авто-пошук MSVC / x64 Native Tools...",
        "warning_qt": "[WARNING] Авто-пошук не знайшов Qt. Вкажіть шлях вручну в Налаштуваннях.",
        "warning_msvc": "[WARNING] Авто-пошук не знайшов MSVC / x64 Native Tools. Вкажіть шлях вручну в Налаштуваннях.",
        "error_qt": "[ERROR] Шлях до Qt не знайдено. Вкажіть його вручну в Налаштуваннях.",
        "error_msvc": "[ERROR] Шлях до MSVC / x64 Native Tools не знайдено. Вкажіть його вручну в Налаштуваннях.",
        "info_building": "[INFO] Налаштування MSVC і збірка ({type})...",
        "info_build_succeeded": "[INFO] Збірка успішно завершена!",
        "error_build_failed": "[ERROR] Збірка не вдалася. Перевірте CMake, Ninja та шляхи до Qt/MSVC.",
        "info_config_saved": "[INFO] Конфіг збережено",
        "info_config_deleted": "[INFO] Конфіг видалено. Авто-пошук включиться при наступному запуску.",
        "language_select_title": "Оберіть мову",
        "language_option_en": "English",
        "language_option_ru": "Русский",
        "language_option_uk": "Українська",
        "language_option_de": "Deutsch",
        "language_option_fr": "Français",
        "ninja_warning": "[!] Для збірки обов'язково встановлений Ninja і доданий у PATH"
    },
    "de": {
        "language_name": "Deutsch",
        "main_menu_start": "Starten",
        "main_menu_settings": "Einstellungen",
        "main_menu_quit": "Beenden",
        "start_menu_title": "Build-Menü",
        "start_menu_build_release": "Release-Version bauen",
        "start_menu_build_beta": "Beta-Version bauen",
        "start_menu_build_debug": "Debug-Version bauen",
        "start_menu_back": "Zurück",
        "run_menu_title": "Programm ausführen",
        "run_menu_run": "Programm ausführen",
        "run_menu_back": "Zurück",
        "settings_title": "Einstellungen",
        "settings_change_qt": "Qt-Pfad ändern",
        "settings_change_msvc": "MSVC-Pfad ändern",
        "settings_restore": "Standardwerte wiederherstellen (Konfig löschen)",
        "settings_back_save": "Zurück und speichern",
        "settings_back_cancel": "Zurück und abbrechen",
        "info_auto_qt": "[INFO] Automatische Suche nach Qt...",
        "info_auto_msvc": "[INFO] Automatische Suche nach MSVC / x64 Native Tools...",
        "warning_qt": "[WARNING] Qt nicht gefunden. Bitte in Einstellungen angeben.",
        "warning_msvc": "[WARNING] MSVC / x64 Native Tools nicht gefunden. Bitte in Einstellungen angeben.",
        "error_qt": "[ERROR] Qt-Pfad nicht gefunden. Bitte in Einstellungen angeben.",
        "error_msvc": "[ERROR] MSVC / x64 Native Tools-Pfad nicht gefunden. Bitte in Einstellungen angeben.",
        "info_building": "[INFO] MSVC einrichten und bauen ({type})...",
        "info_build_succeeded": "[INFO] Build erfolgreich abgeschlossen!",
        "error_build_failed": "[ERROR] Build fehlgeschlagen. Prüfen Sie CMake, Ninja und Qt/MSVC-Pfade.",
        "info_config_saved": "[INFO] Konfiguration gespeichert",
        "info_config_deleted": "[INFO] Konfiguration gelöscht. Auto-Suche wird beim nächsten Start aktiviert.",
        "language_select_title": "Sprache wählen",
        "language_option_en": "English",
        "language_option_ru": "Русский",
        "language_option_uk": "Українська",
        "language_option_de": "Deutsch",
        "language_option_fr": "Français",
        "ninja_warning": "[!] Ninja muss installiert und im PATH sein"
    },
    "fr": {
        "language_name": "Français",
        "main_menu_start": "Démarrer",
        "main_menu_settings": "Paramètres",
        "main_menu_quit": "Quitter",
        "start_menu_title": "Menu de compilation",
        "start_menu_build_release": "Compiler la version release",
        "start_menu_build_beta": "Compiler la version beta",
        "start_menu_build_debug": "Compiler la version debug",
        "start_menu_back": "Retour",
        "run_menu_title": "Exécuter le programme",
        "run_menu_run": "Exécuter le fichier",
        "run_menu_back": "Retour",
        "settings_title": "Paramètres",
        "settings_change_qt": "Changer le chemin Qt",
        "settings_change_msvc": "Changer le chemin MSVC",
        "settings_restore": "Restaurer les valeurs par défaut (supprimer le config)",
        "settings_back_save": "Retour et enregistrer",
        "settings_back_cancel": "Retour et annuler",
        "info_auto_qt": "[INFO] Recherche automatique de Qt...",
        "info_auto_msvc": "[INFO] Recherche automatique de MSVC / x64 Native Tools...",
        "warning_qt": "[WARNING] Qt non trouvé. Veuillez le définir dans Paramètres.",
        "warning_msvc": "[WARNING] MSVC / x64 Native Tools non trouvé. Veuillez le définir dans Paramètres.",
        "error_qt": "[ERROR] Chemin Qt non trouvé. Veuillez le définir dans Paramètres.",
        "error_msvc": "[ERROR] Chemin MSVC / x64 Native Tools non trouvé. Veuillez le définir dans Paramètres.",
        "info_building": "[INFO] Configuration MSVC et compilation ({type})...",
        "info_build_succeeded": "[INFO] Compilation réussie !",
        "error_build_failed": "[ERROR] Échec de la compilation. Vérifiez CMake, Ninja et les chemins Qt/MSVC.",
        "info_config_saved": "[INFO] Configuration enregistrée",
        "info_config_deleted": "[INFO] Configuration supprimée. La recherche automatique sera activée au prochain démarrage.",
        "language_select_title": "Choisir la langue",
        "language_option_en": "English",
        "language_option_ru": "Русский",
        "language_option_uk": "Українська",
        "language_option_de": "Deutsch",
        "language_option_fr": "Français",
        "ninja_warning": "[!] Ninja doit être installé et ajouté au PATH"
    }
}

# ---------------- ФУНКЦИИ ---------------- #

def load_config():
    if os.path.exists(CONFIG_PATH):
        return toml.load(CONFIG_PATH)
    return {"qt_path": "", "msvc_path": "", "build_dir": DEFAULT_BUILD_DIR, "language": "en"}

def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        toml.dump(config, f)

def delete_config():
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)

def input_path(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def detect_qt_path():
    qt_candidates = []
    for base in ["C:/Qt", "C:/Program Files/Qt", "C:/Qt/*", "C:/Program Files/Qt/*"]:
        for path in glob.glob(base):
            if os.path.exists(os.path.join(path, "lib", "cmake")):
                qt_candidates.append(path)
    for var in ["QT_DIR", "QTDIR"]:
        val = os.environ.get(var)
        if val and os.path.exists(os.path.join(val, "lib", "cmake")):
            qt_candidates.append(val)
    return sorted(qt_candidates)[-1] if qt_candidates else ""

def detect_msvc_path():
    msvc_path = ""
    try:
        vswhere_cmd = r'"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath'
        output = subprocess.check_output(vswhere_cmd, shell=True, text=True).strip()
        if output and os.path.exists(output):
            candidate = os.path.join(output, "VC", "Auxiliary", "Build", "vcvars64.bat")
            if os.path.exists(candidate):
                msvc_path = candidate
    except Exception:
        pass
    if not msvc_path:
        default_path = r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
        if os.path.exists(default_path):
            msvc_path = default_path
    return msvc_path

# ---------------- МЕНЮ ---------------- #

def main_menu():
    config = load_config()
    while True:
        language = config.get("language", "en")
        lang = LANG.get(language, LANG["en"])
        # Формируем кнопку Language с локализацией
        if language == "en":
            language_btn = "Language"
        elif language == "ru":
            language_btn = "Language | Язык"
        elif language == "uk":
            language_btn = "Language | Мова"
        elif language == "de":
            language_btn = "Language | Sprache"
        elif language == "fr":
            language_btn = "Language | Langue"
        else:
            language_btn = "Language"
        
        print("\n=== Build Script ===")
        print(lang["ninja_warning"])
        print(f"[1] {lang['main_menu_start']}")
        print(f"[2] {lang['main_menu_settings']}")
        print(f"[3] {lang['main_menu_quit']}")
        print(f"[4] {language_btn}")  # здесь кнопка с корректным текстом
        choice = input("> ").strip()
        if choice == "1":
            start_menu(config)
        elif choice == "2":
            settings_menu(config)
        elif choice == "3":
            sys.exit(0)
        elif choice == "4":
            language_menu(config)


def start_menu(config):
    language = config.get("language", "en")
    lang = LANG.get(language, LANG["en"])
    qt_path = config.get("qt_path", "")
    msvc_path = config.get("msvc_path", "")
    build_dir = config.get("build_dir", DEFAULT_BUILD_DIR)

    # авто-поиск если пусто
    if not qt_path:
        print(lang["info_auto_qt"])
        qt_path = detect_qt_path()
        if not qt_path:
            print(lang["warning_qt"])
    if not msvc_path:
        print(lang["info_auto_msvc"])
        msvc_path = detect_msvc_path()
        if not msvc_path:
            print(lang["warning_msvc"])

    while True:
        print(f"\n=== {lang['start_menu_title']} ===")
        print(f"[1] {lang['start_menu_build_release']}")
        print(f"[2] {lang['start_menu_build_beta']}")
        print(f"[3] {lang['start_menu_build_debug']}")
        print(f"[4] {lang['start_menu_back']}")
        choice = input("> ").strip()
        if choice in ["1", "2", "3"]:
            build_type = {"1": "Release", "2": "Beta", "3": "Debug"}[choice]
            build(config, qt_path, msvc_path, build_dir, build_type)
            run_output_menu(build_dir, config)
        elif choice == "4":
            break

def settings_menu(config):
    language = config.get("language", "en")
    lang = LANG.get(language, LANG["en"])
    while True:
        print(f"\n=== {lang['settings_title']} ===")
        print(f"[!] Qt path: {config.get('qt_path', '') or '(NOT FOUND)'}")
        print(f"[!] MSVC path: {config.get('msvc_path', '') or '(NOT FOUND)'}")
        print(f"[1] {lang['settings_change_qt']}")
        print(f"[2] {lang['settings_change_msvc']}")
        print(f"[3] {lang['settings_restore']}")
        print(f"[4] {lang['settings_back_save']}")
        print(f"[5] {lang['settings_back_cancel']}")
        choice = input("> ").strip()
        if choice == "1":
            config['qt_path'] = input_path("Enter Qt path", config.get('qt_path', ''))
        elif choice == "2":
            config['msvc_path'] = input_path("Enter MSVC path", config.get('msvc_path', ''))
        elif choice == "3":
            delete_config()
            print(lang["info_config_deleted"])
            config.update({"qt_path": "", "msvc_path": "", "build_dir": DEFAULT_BUILD_DIR, "language": config.get("language","en")})
        elif choice == "4":
            save_config(config)
            print(lang["info_config_saved"])
            break
        elif choice == "5":
            break

def language_menu(config):
    print("\n=== Language Menu ===")
    print("[1] English\n[2] Русский\n[3] Українська\n[4] Deutsch\n[5] Français")
    choice = input("> ").strip()
    mapping = {"1":"en","2":"ru","3":"uk","4":"de","5":"fr"}
    lang_code = mapping.get(choice, "en")
    config["language"] = lang_code
    save_config(config)
    print(f"Language set to {LANG[lang_code]['language_name']}")

def build(config, qt_path, msvc_path, build_dir, build_type):
    language = config.get("language", "en")
    lang = LANG.get(language, LANG["en"])
    os.makedirs(build_dir, exist_ok=True)
    print(lang["info_building"].format(type=build_type))
    try:
        # Создаём батник для выполнения всех команд в одной среде MSVC
        batch_file = os.path.join(build_dir, "build_temp.bat")
        with open(batch_file, "w") as f:
            f.write(f'@echo off\n')
            f.write(f'call "{msvc_path}"\n')
            f.write(f'cd /d "{build_dir}"\n')
            f.write(f'cmake -G Ninja -DQt6_DIR="{qt_path}/lib/cmake/Qt6" -DCMAKE_BUILD_TYPE={build_type} "{PROJECT_ROOT}"\n')
            f.write(f'ninja\n')
        
        # Запускаем батник
        subprocess.check_call(batch_file, shell=True)
        
        # Удаляем временный батник
        os.remove(batch_file)
        print(lang["info_build_succeeded"])
    except subprocess.CalledProcessError:
        print(lang["error_build_failed"])
    except Exception as e:
        print(f"{lang['error_build_failed']} ({str(e)})")

def run_output_menu(build_dir, config):
    language = config.get("language", "en")
    lang = LANG.get(language, LANG["en"])
    # ищем exe
    exes = glob.glob(os.path.join(build_dir, "*.exe"))
    exe_path = exes[0] if exes else None
    if not exe_path:
        print("[ERROR] No output file found.")
        return
    while True:
        print(f"\n=== {lang['run_menu_title']} ===")
        print(f"[1] {lang['run_menu_run']}")
        print(f"[2] {lang['run_menu_back']}")
        choice = input("> ").strip()
        if choice == "1":
            subprocess.Popen(exe_path, shell=True)
        elif choice == "2":
            break

# ---------------- ЗАПУСК ---------------- #
if __name__ == "__main__":
    main_menu()
