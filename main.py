import json
import webbrowser
from datetime import datetime
from pathlib import Path

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from phonenumbers import NumberParseException
from colorama import Fore, Style, init

init(autoreset=True)

APP_NAME = "NexTrace"
VERSION = "0.0.3 By NexForm"
REPORT_DIR = Path("reports")

CYAN = Fore.CYAN + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
GRAY = Fore.LIGHTBLACK_EX
RESET = Style.RESET_ALL


def clear_screen():
    print("\033[2J\033[H", end="")


def show_banner():
    print(CYAN + r"""
 _   _ _____  __  _______ ____      _    ____ _____
| \ | | ____| \ \/ /_   _|  _ \    / \  / ___| ____|
|  \| |  _|    \  /  | | | |_) |  / _ \| |   |  _|
| |\  | |___   /  \  | | |  _ <  / ___ \ |___| |___
|_| \_|_____| /_/\_\ |_| |_| \_\/_/   \_\____|_____|
""")
    print(CYAN + f"          PHONE INTELLIGENCE TOOLKIT")
    print(GRAY + f"           Version {VERSION}")
    print(GRAY + "=" * 55)


def show_menu():
    print(CYAN + "\n  MAIN MENU")
    print(GRAY + "  " + "-" * 35)
    print(f"  {CYAN}[1]{WHITE} Analyze phone number")
    print(f"  {CYAN}[2]{WHITE} Messaging tools")
    print(f"  {CYAN}[3]{WHITE} About NexTrace")
    print(f"  {RED}[0]{WHITE} Exit")
    print(GRAY + "  " + "-" * 35)


def normalize_phone(raw_number):
    return "".join(char for char in raw_number if char.isdigit())


def analyze_phone(raw_number):
    try:
        number = phonenumbers.parse(raw_number, None)
    except NumberParseException as error:
        return {"error": str(error)}

    international = phonenumbers.format_number(
        number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )
    e164 = phonenumbers.format_number(
        number, phonenumbers.PhoneNumberFormat.E164
    )

    number_type = phonenumbers.number_type(number)

    type_names = {
        0: "Fixed line",
        1: "Mobile",
        2: "Fixed line or mobile",
        3: "Toll-free",
        4: "Premium rate",
        5: "Shared cost",
        6: "VoIP",
        7: "Personal number",
        8: "Pager",
        9: "UAN",
        10: "Voicemail",
        99: "Unknown",
    }

    return {
        "input": raw_number,
        "international": international,
        "national": phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "e164": e164,
        "country_calling_code": f"+{number.country_code}",
        "region": phonenumbers.region_code_for_number(number),
        "number_type": type_names.get(number_type, "Unknown"),
        "possible": phonenumbers.is_possible_number(number),
        "valid_format": phonenumbers.is_valid_number(number),
        "description": geocoder.description_for_number(number, "en"),
        "carrier_data": carrier.name_for_number(number, "en"),
        "time_zones": list(timezone.time_zones_for_number(number)),
        "whatsapp_url": f"https://wa.me/{normalize_phone(e164)}",
        "telegram_url": f"https://t.me/{normalize_phone(e164)}",
        "limitations": [
            "Validity does not prove that the number is active.",
            "Carrier information may be outdated or unavailable.",
            "Geographic descriptions are not precise GPS locations.",
            "WhatsApp links do not confirm account existence.",
            "Telegram links do not guarantee profile lookup by number.",
            "No subscriber identity has been verified.",
        ],
    }


def display_report(report):
    if "error" in report:
        print(RED + f"\n  [!] Invalid number: {report['error']}")
        return False

    print(CYAN + "\n" + "=" * 55)
    print(CYAN + "  PHONE INTELLIGENCE REPORT")
    print(CYAN + "=" * 55)

    fields = [
        ("Input", "input"),
        ("International", "international"),
        ("National", "national"),
        ("E.164", "e164"),
        ("Calling code", "country_calling_code"),
        ("Region", "region"),
        ("Number type", "number_type"),
        ("Possible", "possible"),
        ("Valid format", "valid_format"),
        ("Description", "description"),
        ("Carrier", "carrier_data"),
        ("Time zones", "time_zones"),
    ]

    for label, key in fields:
        value = report.get(key)

        if isinstance(value, list):
            value = ", ".join(value) if value else "Unknown"

        if value is None or value == "":
            value = "Unknown"

        if key in ("possible", "valid_format"):
            color = GREEN if value is True else RED
        else:
            color = WHITE

        print(f"  {CYAN}{label:<18}{color}{value}")

    print(CYAN + "\n  MESSAGING LINKS")
    print(f"  {GREEN}WhatsApp: {WHITE}{report['whatsapp_url']}")
    print(f"  {GREEN}Telegram: {WHITE}{report['telegram_url']}")

    print(YELLOW + "\n  LIMITATIONS")
    for limitation in report["limitations"]:
        print(f"  {YELLOW}[*] {GRAY}{limitation}")

    print(CYAN + "=" * 55)
    return True


def export_report(report):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = REPORT_DIR / f"nextrace_{timestamp}.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(GREEN + f"\n  [+] Report exported: {file_path}")


def messaging_menu(report):
    while True:
        print(CYAN + "\n  MESSAGING TOOLS")
        print(GRAY + "  " + "-" * 35)
        print(f"  {CYAN}[1]{WHITE} Open WhatsApp link")
        print(f"  {CYAN}[2]{WHITE} Open Telegram link")
        print(f"  {CYAN}[3]{WHITE} Copy WhatsApp link to screen")
        print(f"  {CYAN}[4]{WHITE} Copy Telegram link to screen")
        print(f"  {CYAN}[0]{WHITE} Back")
        print(GRAY + "  " + "-" * 35)

        choice = input(CYAN + "\n  Select an option: " + WHITE).strip()

        if choice == "1":
            webbrowser.open(report["whatsapp_url"])
            print(GREEN + "  [+] WhatsApp link sent to your browser.")
        elif choice == "2":
            webbrowser.open(report["telegram_url"])
            print(GREEN + "  [+] Telegram link sent to your browser.")
        elif choice == "3":
            print(GREEN + f"\n  {report['whatsapp_url']}")
        elif choice == "4":
            print(GREEN + f"\n  {report['telegram_url']}")
        elif choice == "0":
            break
        else:
            print(RED + "  [!] Invalid option.")

        input(GRAY + "\n  Press Enter to continue...")


def analyze_workflow():
    raw_number = input(
        CYAN + "\n  Enter number in international format: " + WHITE
    ).strip()

    if not raw_number:
        print(RED + "  [!] No number entered.")
        input(GRAY + "\n  Press Enter to continue...")
        return

    report = analyze_phone(raw_number)

    if not display_report(report):
        input(GRAY + "\n  Press Enter to continue...")
        return

    while True:
        print(CYAN + "\n  REPORT ACTIONS")
        print(f"  {CYAN}[1]{WHITE} Messaging tools")
        print(f"  {CYAN}[2]{WHITE} Export JSON report")
        print(f"  {CYAN}[0]{WHITE} Back to main menu")

        choice = input(CYAN + "\n  Select an option: " + WHITE).strip()

        if choice == "1":
            messaging_menu(report)
        elif choice == "2":
            export_report(report)
        elif choice == "0":
            break
        else:
            print(RED + "  [!] Invalid option.")

        if choice in ("1", "2"):
            input(GRAY + "\n  Press Enter to continue...")


def show_about():
    print(CYAN + "\n  ABOUT NEXTRACE")
    print(GRAY + "  " + "-" * 35)
    print(f"  {WHITE}Name:        {APP_NAME}")
    print(f"  {WHITE}Version:     {VERSION}")
    print(f"  {WHITE}Purpose:     Phone number intelligence")
    print(f"  {WHITE}Metadata:    Local phonenumbers database")
    print(f"  {WHITE}Reports:     JSON")
    print(f"  {WHITE}API keys:    Not required")
    print(GRAY + "\n  NexTrace does not identify subscribers.")
    print("  Messaging links do not confirm account ownership.")


def main():
    while True:
        clear_screen()
        show_banner()
        print(GREEN + "  [+] System ready")
        show_menu()

        choice = input(CYAN + "\n  Select an option: " + WHITE).strip()

        if choice == "1":
            analyze_workflow()
        elif choice == "2":
            print(YELLOW + "\n  Analyze a number first to access messaging tools.")
            input(GRAY + "\n  Press Enter to continue...")
        elif choice == "3":
            show_about()
            input(GRAY + "\n  Press Enter to continue...")
        elif choice == "0":
            print(GREEN + "\n  [+] NexTrace terminated. Goodbye!")
            break
        else:
            print(RED + "\n  [!] Invalid option.")
            input(GRAY + "  Press Enter to retry...")




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(RED + "\n\n  [!] NexTrace interrupted by user.")
