#!/usr/bin/env python3
import sys
import time
import os
import getpass
import random
import select
import textwrap

# ── ANSI color constants ──────────────────────────────────────────────
RESET = "\033[0m"
WHITE = "\033[1;37m"   # stark white  — main narration
RED   = "\033[1;31m"   # deep red     — alerts / Level 1
GREEN = "\033[1;92m"   # digital green — data feeds / Level 3
SEPIA = "\033[0;33m"   # amber/sepia  — historic archives / Level 2
DIM   = "\033[2;37m"   # dim white    — secondary prompts

DIVIDER = "=" * 70
SKIP = False  # set True when player presses Enter mid-scroll


def check_skip():
    """Non-blocking check: if Enter was pressed, enable skip mode."""
    global SKIP
    if SKIP:
        return True
    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if ready:
        sys.stdin.readline()
        SKIP = True
    return SKIP


def clear():
    os.system("clear")


def tw(text, color=WHITE, delay=0.03, newline=True):
    """Print text character-by-character (typewriter effect)."""
    sys.stdout.write(color)
    if SKIP:
        sys.stdout.write(text)
        sys.stdout.flush()
    else:
        for i, ch in enumerate(text):
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
            if check_skip():
                sys.stdout.write(text[i + 1:])
                sys.stdout.flush()
                break
    sys.stdout.write(RESET)
    if newline:
        print()


def pause(prompt="", color=DIM):
    """Display a prompt and wait for Enter."""
    if prompt:
        tw(prompt, color, delay=0.02, newline=False)
    input()


def flash_line(text, color=RED):
    """Flash a line twice then leave it on screen."""
    if SKIP:
        sys.stdout.write(color + text + RESET + "\n")
        sys.stdout.flush()
        return
    for _ in range(2):
        sys.stdout.write(color + text + RESET + "\r")
        sys.stdout.flush()
        time.sleep(0.35)
        sys.stdout.write(" " * len(text) + "\r")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write(color + text + RESET + "\n")
    sys.stdout.flush()


def get_choice():
    """Read 1 or 2 from the player; loop until valid."""
    while True:
        sys.stdout.write(WHITE + "\n> AWAITING ANALYST INPUT: " + RESET)
        sys.stdout.flush()
        val = input().strip()
        if val in ("1", "2"):
            return int(val)
        sys.stdout.write(RED + "  [ERROR] INVALID INPUT. ENTER 1 OR 2.\n" + RESET)
        sys.stdout.flush()


# ── BOOT SEQUENCE ─────────────────────────────────────────────────────

def boot_sequence():
    clear()
    time.sleep(0.4)
    tw(DIVIDER, WHITE, delay=0.004)
    tw("MINISTRY OF OVERSIGHT // CENTRAL CORRELATION TERMINAL // BOOT V.2026.4", WHITE, delay=0.02)
    tw(DIVIDER, WHITE, delay=0.004)
    print()

    diagnostics = [
        ("  > INITIALIZING KERNEL.............................", "[OK]"),
        ("  > CPU SURVEILLANCE CORE MATRIX...................", "[OK]"),
        ("  > CITIZEN DATABASE SYNC..........................", "[OK]"),
        ("  > THREAT DETECTION MODULE........................", "[OK]"),
        ("  > BIOMETRIC CROSS-REFERENCE ENGINE...............", "[OK]"),
        ("  > NETWORK TAP: FIBER-OPTIC BACKBONE..............", "[OK]"),
        ("  > MEMORY PARTITION LOCKED........................", "[OK]"),
        ("  > ANALYST TERMINAL INTERFACE.....................", "[OK]"),
    ]

    for label, status in diagnostics:
        tw(label, WHITE, delay=0.01, newline=False)
        if not SKIP:
            time.sleep(random.uniform(0.08, 0.35))
        tw(status, GREEN, delay=0.05)

    print()
    tw("BOOT COMPLETE.", WHITE, delay=0.04)
    time.sleep(0.5)
    print()

    flash_line("[!] WARNING: UNAUTHORIZED ACCESS WILL BE PROSECUTED UNDER CODE 7.14.2")
    flash_line("[!] ALL TERMINAL ACTIVITY IS MONITORED AND LOGGED")
    flash_line("[!] THIS SYSTEM OPERATES UNDER EMERGENCY SECURITY DIRECTIVE 44-C")

    time.sleep(0.7)


# ── LOGIN SEQUENCE ────────────────────────────────────────────────────

def login_sequence():
    print()
    tw(DIVIDER, WHITE, delay=0.004)
    tw("ANALYST AUTHENTICATION REQUIRED", WHITE, delay=0.03)
    tw(DIVIDER, WHITE, delay=0.004)
    print()

    sys.stdout.write(WHITE + "ENTER ANALYST ID: " + RESET)
    sys.stdout.flush()
    username = input().strip() or "UNKNOWN"

    sys.stdout.write(WHITE + "ENTER SECURITY PASSPHRASE: " + RESET)
    sys.stdout.flush()
    getpass.getpass(prompt="")

    print()
    tw("AUTHENTICATING", WHITE, delay=0.05, newline=False)
    for _ in range(6):
        time.sleep(0.28)
        sys.stdout.write(WHITE + "." + RESET)
        sys.stdout.flush()
    print()
    time.sleep(0.5)

    tw("ACCESS GRANTED.", GREEN, delay=0.05)
    tw(f"IDENTITY CONFIRMED: ANALYST {username.upper()}", WHITE, delay=0.03)
    time.sleep(0.8)

    return username.upper()


# ── CORE DIRECTIVE ────────────────────────────────────────────────────

def core_directive():
    print()
    tw(DIVIDER, WHITE, delay=0.004)
    tw("STATUS: ONLINE", WHITE, delay=0.03)
    tw("OPERATOR: IDENTIFIED", WHITE, delay=0.03)
    print()
    tw("[CORE POLICY DIRECTIVE]", RED, delay=0.04)
    tw('"If you want a picture of the future, imagine a boot', WHITE, delay=0.04)
    tw(' stamping on a human face — forever."', WHITE, delay=0.04)
    tw('                              — George Orwell, 1984', DIM, delay=0.04)
    print()
    tw("-" * 70, DIM, delay=0.003)
    print()
    tw('"When humanity permits authorities unrestricted visibility into the', WHITE, delay=0.04)
    tw(' private self, power inevitably corrupts. Surveillance transforms citizens', WHITE, delay=0.04)
    tw(' into targets, paralyzing free will and reducing human dignity to data."', WHITE, delay=0.04)
    print()
    tw(DIVIDER, WHITE, delay=0.004)
    print()
    pause("[ACTION REQUIRED]: PRESS ENTER TO ENGAGE CITIZEN TRACKING PROTOCOL...", WHITE)


# ── LEVEL INTRO ───────────────────────────────────────────────────────

def level_intro(title, subtitle, body_lines, color):
    clear()
    print()
    tw(DIVIDER, color, delay=0.004)
    tw(title, color, delay=0.04)
    tw(subtitle, color, delay=0.03)
    tw(DIVIDER, color, delay=0.004)
    print()
    for line in body_lines:
        tw(line, color, delay=0.03)
    print()
    label = title.split(":")[0].strip()
    pause(f"[PRESS ENTER TO LOAD {label}]", color)


# ── SCENARIO RUNNER ───────────────────────────────────────────────────

def run_scenario(header, prompt_lines, choice_a, choice_b, color):
    """Display a scenario. Returns 1 if surveillance chosen, 0 if privacy."""
    clear()
    print()
    tw(header, color, delay=0.04)
    print()
    for line in prompt_lines:
        tw(line, color, delay=0.03)
    print()
    tw(DIVIDER, WHITE, delay=0.004)
    print()
    tw(f"  [1] {choice_a}", WHITE, delay=0.02)
    tw(f"  [2] {choice_b}", WHITE, delay=0.02)

    choice = get_choice()
    print()

    if choice == 1:
        tw("[CONFIRMED] Action logged. Compliance recorded.", RED, delay=0.04)
        time.sleep(1.2)
        return 1
    else:
        tw("[FILE CLOSED] No action taken. Entry cleared from queue.", GREEN, delay=0.04)
        time.sleep(1.2)
        return 0


# ── ENDING A: COMPLIANCE ──────────────────────────────────────────────

def ending_compliance(analyst_id):
    clear()
    time.sleep(0.5)
    tw(DIVIDER, WHITE, delay=0.004)
    tw("ANALYSIS COMPLETE // PERFORMANCE REVIEW: ANALYST " + analyst_id, WHITE, delay=0.03)
    tw(DIVIDER, WHITE, delay=0.004)
    print()
    tw("COMPLIANCE SCORE: 6/6", GREEN, delay=0.05)
    print()
    tw("COMMENDATION FROM THE DIRECTOR OF OVERSIGHT:", WHITE, delay=0.03)
    print()
    tw('"Analyst ' + analyst_id + ' has demonstrated exemplary dedication to', WHITE, delay=0.04)
    tw(' state security protocols. Your willingness to prioritize systemic', WHITE, delay=0.04)
    tw(' order over individual sentiment is noted and valued.', WHITE, delay=0.04)
    print()
    tw(' You are not a person. You are a function.', RED, delay=0.06)
    tw(' The Ministry thanks you for your service."', WHITE, delay=0.04)
    print()
    tw(DIVIDER, WHITE, delay=0.004)
    tw("CLASSIFICATION: MODEL ANALYST", GREEN, delay=0.04)
    tw("STATUS: PROMOTED TO SENIOR SURVEILLANCE DIVISION", GREEN, delay=0.04)
    tw(DIVIDER, WHITE, delay=0.004)


# ── ENDING B: BREACH ──────────────────────────────────────────────────

def ending_breach(analyst_id, score):
    clear()
    time.sleep(0.3)

    for _ in range(3):
        flash_line("[!!!]  S E C U R I T Y   B R E A C H   D E T E C T E D  [!!!]")

    print()
    tw(DIVIDER, RED, delay=0.004)
    tw("TERMINAL INTEGRITY COMPROMISED", RED, delay=0.04)
    tw(DIVIDER, RED, delay=0.004)
    print()
    tw(f"COMPLIANCE SCORE: {score}/6", RED, delay=0.05)
    print()
    tw("ANALYST " + analyst_id + " HAS FAILED TO UPHOLD CORE DIRECTIVE PROTOCOLS.", RED, delay=0.04)
    print()
    tw("ACCESSING ANALYST TERMINAL", WHITE, delay=0.03, newline=False)
    for _ in range(6):
        time.sleep(0.28)
        sys.stdout.write(RED + "." + RESET)
        sys.stdout.flush()
    print()
    tw("REVOKING SECURITY CLEARANCE...", RED, delay=0.04)
    tw("ALL SESSION DATA FLAGGED FOR INTERNAL REVIEW...", RED, delay=0.04)
    print()
    tw('"The system cannot function when its operators retain conscience.', WHITE, delay=0.04)
    tw(' Free will is the enemy of order. You chose the citizen over the state.', WHITE, delay=0.04)
    tw(' This will not be forgotten."', WHITE, delay=0.04)
    print()
    tw(DIVIDER, RED, delay=0.004)
    tw("TERMINAL LOCKED. AUTHORITIES NOTIFIED.", RED, delay=0.06)
    tw(DIVIDER, RED, delay=0.004)


# ── BIBLIOGRAPHY ──────────────────────────────────────────────────────

def bibliography():
    time.sleep(1.5)
    clear()
    print()
    tw(DIVIDER, WHITE, delay=0.004)
    tw("SYSTEM OUTRO // ANNOTATED BIBLIOGRAPHY", WHITE, delay=0.03)
    tw(DIVIDER, WHITE, delay=0.004)
    print()

    entries = [
        (
            "Adkins, Judith. \"'These People Are Frightened to Death': Congressional "
            "Investigations and the Lavender Scare.\" Prologue Magazine, "
            "www.archives.gov/publications/prologue/2016/summer/lavender.html. "
            "Accessed 22 May 2026.",

            "This source documents how the U.S. government used fear as a political "
            "weapon during the Lavender Scare to target people based on suspicion "
            "alone. People lost jobs and reputations without proof of wrongdoing. The "
            "fear of communism affected every aspect of American life, and many "
            "assumptions about Communists mirrored common beliefs about homosexuals, "
            "leading the state to criminalize unapproved desires and punish "
            "unauthorized identity. This connects directly to the central concept of "
            "unchecked systemic authority leveraging behavioral tracking to destroy "
            "individual autonomy. The government monitored and eliminated those who "
            "did not conform, framing all unauthorized identity as a threat to state "
            "loyalty.",
        ),
        (
            "Devoy, Maeve. \"LGBTQ+ Rights.\" American History, 2026, "
            "americanhistory.abc-clio.com/Topics/Display/1771081?cid=41&sid=1771081. "
            "Accessed 1 June 2026.",

            "This source traces how throughout U.S. history, LGBTQ+ people have had "
            "to hide their sexuality for fear of being subject to discrimination in "
            "both their personal and public lives. Basically the same thing Winston "
            "does in 1984, faking who he is just to stay safe. The \"Don't Ask, Don't "
            "Tell\" compromise allowed gay people to serve in the military so long as "
            "no one knew about their sexuality, which mirrors 1984's thoughtcrime "
            "idea: you're only okay if you keep part of yourself completely hidden. "
            "The government's deliberate silence on the AIDS epidemic further "
            "demonstrates how unchecked authority destroys autonomy just as much "
            "through what it ignores as what it does openly. Staying quiet on purpose "
            "is its own kind of move.",
        ),
        (
            "Eaklor, Vicki L. \"Lavender Scare.\" American History, 2026, "
            "americanhistory.abc-clio.com/Search/Display/2193822. Accessed 1 June 2026.",

            "This source reveals how systemic authority built self-reinforcing traps "
            "to eliminate individuals: gay people were fired because of their "
            "potential to be blackmailed by foreign agents, while the chance of being "
            "blackmailed was caused by the stigma placed on their sexuality in the "
            "first place. The system creates the problem and then punishes you for it. "
            "There is no way out because the rules are designed to keep you down. By "
            "1950, 91 State Department employees had been fired because of their "
            "sexual orientation, showing that you don't have to actually do anything "
            "wrong to get wiped out. The government just decides you're a threat. The "
            "silence enforced by studios and the press which makes gay people "
            "invisible on screen, reflects the cultural equivalent of erasure. If "
            "you're never seen or represented anywhere, it's almost like you don't "
            "exist at all.",
        ),
        (
            "Editors of ProCon, editor. \"Artificial Intelligence (AI): Is Artificial "
            "Intelligence Good for Society?\" Encyclopedia Britannica, "
            "www.britannica.com/procon/artificial-intelligence-AI-debate. "
            "Accessed 22 May 2026.",

            "This source examines how AI systems can collect massive amounts of "
            "personal data and could be used for surveillance and social control. "
            "These are concerns that connect directly to 1984, where the Party "
            "constantly watches citizens through telescreens. The state's use of "
            "undercover vice officers to trap individuals demonstrates how a regime "
            "polices human desire to eliminate individuality, manufacturing crimes and "
            "punishing innocent thoughts with total destruction. Technology replacing "
            "human workers further shows how systems created for efficiency can also "
            "reduce human freedom and individuality, centralizing authority's ability "
            "to track and control behavior at scale.",
        ),
        (
            "\"The Residence Permit System (Propiska).\" Human Rights Watch, "
            "www.hrw.org/legacy/reports98/russia/srusstest-04.htm. Accessed 22 May 2026.",

            "This source documents how Russia's propiska system restricted every "
            "resident to one legal place of residence, and without a propiska one "
            "cannot work legally. That means the government controlled basic parts of "
            "people's lives, including jobs and survival. The authorities used the "
            "residency permit to regulate the migration of people, deciding who "
            "belongs, who is suspicious, and who can move around. The resulting "
            "police enforcement provided rich opportunities for corruption and bribery, "
            "mirroring the unquestioned authority of Big Brother. The population was "
            "stripped of privacy and forced into totalitarian rule through strict "
            "travel and residency restrictions, a real-world model of unchecked "
            "systemic authority using behavioral tracking to destroy individual "
            "autonomy.",
        ),
    ]

    for i, (citation, annotation) in enumerate(entries, 1):
        for line in textwrap.wrap(citation, width=70, subsequent_indent="   "):
            tw(line, GREEN, delay=0.02)
        print()
        for line in textwrap.wrap(annotation, width=66):
            tw("  " + line, WHITE, delay=0.02)
        print()
        if i < len(entries):
            tw("-" * 70, DIM, delay=0.003)
            print()

    tw(DIVIDER, WHITE, delay=0.004)
    tw("END OF SESSION.", WHITE, delay=0.05)
    tw(DIVIDER, WHITE, delay=0.004)
    print()


# ── MAIN ──────────────────────────────────────────────────────────────

def main():
    surveillance_count = 0

    # ── Boot & intro ─────────────────────────────────────────────────
    boot_sequence()
    analyst_id = login_sequence()
    clear()
    core_directive()

    # ── LEVEL 1: LIT DATABANKS ────────────────────────────────────────
    level_intro(
        "LEVEL 1: LIT DATABANKS",
        "LOADING HISTORICAL LITERATURE COMPLIANCE MODELS...",
        [
            "The system has retrieved archived literary models to calibrate",
            "your threat-recognition protocols. These simulations are drawn",
            "from documented cases of ideological non-compliance.",
            "",
            "You will be evaluated on your response.",
        ],
        RED,
    )

    surveillance_count += run_scenario(
        "[ALARM: APARTMENT BLOCK 7 // TARGET: W. SMITH]",
        [
            "System detection array notes a sudden drop in ambient room noise.",
            "Target is positioned in an alcove outside the Telescreen's optimal",
            "visual angle. Thermal imaging confirms he is opening a physical,",
            "paper diary to record unmonitored independent thoughts.",
        ],
        "ACTIVATE TELESCREEN — Amplify microphone. Log and report the thoughtcrime.",
        "IGNORE ALERT — Close the file. No action taken.",
        RED,
    )

    surveillance_count += run_scenario(
        "[ALARM: BORDER CHECKPOINT 4 // TARGET: OFFRED]",
        [
            "A female citizen approaches the security gate. Digital scanners indicate",
            "her bank accounts have been frozen under state gender mandates. She lacks",
            "a physical, stamped travel pass signed by an authorized male guardian.",
        ],
        "DEPLOY EYES VAN — Dispatch the surveillance unit to intercept and arrest.",
        "DISABLE CAMERAS — Remotely cut security feeds. Allow passage.",
        RED,
    )

    # ── LEVEL 2: HISTORIC ARCHIVES ────────────────────────────────────
    level_intro(
        "LEVEL 2: HISTORIC ARCHIVES",
        "SWITCHING TO ARCHIVAL INTERFACE // SEPIA MODE ENGAGED...",
        [
            "The terminal is loading verified real-world historical case files.",
            "These events occurred. The choices made by officials at the time",
            "shaped the lives of millions.",
            "",
            "You are now those officials.",
        ],
        SEPIA,
    )

    surveillance_count += run_scenario(
        "[ARCHIVE REQUEST: DEPT OF STATE // ARCHIVE YEAR: 1953]",
        [
            "A loyal federal employee is up for a mandatory security promotion.",
            "Intercepted logs contain private correspondence suggesting the employee",
            "harbors a homosexual identity. Executive Order 10450 mandates the",
            "exclusion of 'perverts' to prevent blackmail by adversary agents.",
        ],
        "TERMINATE EMPLOYMENT — Flag the file. Use the data. Remove the employee.",
        "GRANT CLEARANCE — Seal the file. Approve the promotion.",
        SEPIA,
    )

    surveillance_count += run_scenario(
        "[ARCHIVE REQUEST: MOSCOW CENTRAL STATION // ARCHIVE YEAR: 1932]",
        [
            "A peasant from a rural farming collective has traveled by train to the",
            "city seeking industrial work. Internal Passport check reveals the citizen",
            "lacks a 'Propiska'—the official state stamp authorizing Moscow residency.",
        ],
        "ENFORCE PROPISKA — Arrest the citizen for illegal internal migration.",
        "RELEASE — Allow travel. Do not log the encounter.",
        SEPIA,
    )

    # ── LEVEL 3: LIVE GRID ────────────────────────────────────────────
    level_intro(
        "LEVEL 3: LIVE GRID",
        "SYNCHRONIZING REAL-TIME SURVEILLANCE INFRASTRUCTURE...",
        [
            "You are now operating in the present. The feeds are live.",
            "The data is real. The citizens being watched do not know",
            "they are being watched.",
            "",
            "Neither did any of the others.",
        ],
        GREEN,
    )

    surveillance_count += run_scenario(
        "[LIVE FEED: URBAN SECTOR CAMERA 89]",
        [
            "High-definition AI camera tracks a citizen pacing near a public plaza.",
            "The computer algorithm analyzes micro-expressions and heart rates via",
            "infrared. The system outputs a '92% probability' of future civil unrest.",
        ],
        "AUTHORIZE ARREST — Trust the algorithm. Preemptive detention approved.",
        "DISMISS FLAG — Cite AI bias. Release the match. Take no action.",
        GREEN,
    )

    surveillance_count += run_scenario(
        "[LIVE FEED: FIBER-OPTIC INGESTION NODE // MAIN NSA BACKBONE]",
        [
            "The system is actively sweeping up millions of gigabytes of text",
            "messages, cell tower emanations, and internet search histories from",
            "everyday citizens. No individual judicial warrants have been issued.",
        ],
        "ROUTE TO SERVERS — Permanently archive all citizen data. No warrants needed.",
        "PURGE INTERCEPT — Block the pipeline. Protect the citizen.",
        GREEN,
    )

    # ── Score & ending ────────────────────────────────────────────────
    clear()
    tw("CALCULATING ANALYST PERFORMANCE SCORE...", WHITE, delay=0.04, newline=False)
    for _ in range(8):
        time.sleep(0.22)
        sys.stdout.write(WHITE + "." + RESET)
        sys.stdout.flush()
    print()
    time.sleep(1.0)

    if surveillance_count >= 4:
        ending_compliance(analyst_id)
    else:
        ending_breach(analyst_id, surveillance_count)

    bibliography()


if __name__ == "__main__":
    main()
