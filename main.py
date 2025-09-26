import typer
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.rule import Rule
from rich.live import Live
from rich import box
import os

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

# Global variables for current user
current_user = None
current_role = None
user_permissions = []

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    """Display retro ASCII art banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║    ██╗██████╗  ██████╗ ███╗   ██╗    ██████╗ ██╗███╗  ██╗ ██████╗  ║
    ║    ██║██╔══██╗██╔═══██╗████╗  ██║    ██╔══██╗██║████╗ ██║██╔════╝  ║
    ║    ██║██████╔╝██║   ██║██╔██╗ ██║    ██████╔╝██║██╔██╗██║██║  ███╗ ║
    ║    ██║██╔══██╗██║   ██║██║╚██╗██║    ██╔══██╗██║██║╚████║██║   ██║ ║
    ║    ██║██║  ██║╚██████╔╝██║ ╚████║    ██║  ██║██║██║ ╚███║╚██████╔╝ ║
    ║    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝╚═╝  ╚══╝     ║
    ║                                                                    ║
    ║                    SPACE STATION TERMINAL                          ║
    ║                    [IRON RING DOS v1.0]                            ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bright_cyan")

def loading_screen():
    """Display loading screen with progress bar"""
    console.print("\n[bold green]INITIALIZING SYSTEM...[/bold green]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]>>[/bold green] {task.description}"),
        BarColumn(bar_width=40, complete_style="bright_green", finished_style="bright_green"),
        TextColumn("[bold green]{task.percentage:>3.0f}%[/bold green]"),
        console=console
    ) as progress:
        
        tasks = [
            ("BOOTING CORE SYSTEMS", 100),
            ("INITIALIZING NEURAL NETWORKS", 80),
            ("LOADING DATABASE CONNECTIONS", 60),
            ("ESTABLISHING SECURE CHANNELS", 40),
            ("SYNCING WITH STATION NETWORK", 20),
            ("READY FOR USER INPUT", 0)
        ]
        
        for task_desc, total in tasks:
            task = progress.add_task(task_desc, total=total)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(random.uniform(0.02, 0.08))
            progress.remove_task(task)
    
    console.print("\n[bold bright_green]SYSTEM READY![/bold bright_green]\n")
    time.sleep(1)

def load_users():
    """Load user credentials from users.txt"""
    users = {}
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    username, password, role = line.split(':')
                    users[username] = {'password': password, 'role': role}
    except FileNotFoundError:
        console.print("[red]ERROR: users.txt not found![/red]")
        return {}
    return users

def load_permissions():
    """Load role permissions from permissions.txt"""
    permissions = {}
    try:
        with open('permissions.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    role, perms = line.split(':')
                    permissions[role] = [int(x) for x in perms.split(',')]
    except FileNotFoundError:
        console.print("[red]ERROR: permissions.txt not found![/red]")
        return {}
    return permissions

def load_user_holos():
    """Load user credit balances from user_holos.txt"""
    holos = {}
    try:
        with open('user_holos.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    username, credit_amount = line.split(':')
                    holos[username] = int(credit_amount)
    except FileNotFoundError:
        console.print("[red]ERROR: user_holos.txt not found![/red]")
        return {}
    return holos

def save_user_holos(holos):
    """Save user credit balances to user_holos.txt"""
    try:
        with open('user_holos.txt', 'w') as f:
            for username, credit_amount in holos.items():
                f.write(f"{username}:{credit_amount}\n")
        return True
    except Exception as e:
        console.print(f"[red]ERROR: Could not save holos: {e}[/red]")
        return False

def login_screen():
    """Display login screen and authenticate user"""
    global current_user, current_role, user_permissions
    
    users = load_users()
    permissions = load_permissions()
    
    if not users or not permissions:
        console.print("[red]CRITICAL ERROR: Cannot load user database![/red]")
        return False
    
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        clear_screen()
        print_ascii_art()
        
        # Display login panel
        login_panel = Panel(
            Align.center(
                Text("USER AUTHENTICATION REQUIRED", style="bold bright_yellow")
            ),
            border_style="bright_yellow",
            box=box.DOUBLE
        )
        console.print(login_panel)
        
        console.print("\n[bold cyan]ENTER CREDENTIALS:[/bold cyan]")
        console.print("=" * 50, style="bright_yellow")
        
        username = Prompt.ask("\n[bold green]USERNAME[/bold green]")
        password = Prompt.ask("[bold green]PASSWORD[/bold green]", password=True)
        
        if username in users and users[username]['password'] == password:
            current_user = username
            current_role = users[username]['role']
            user_permissions = permissions.get(current_role, [])
            
            console.print(f"\n[bold bright_green]ACCESS GRANTED![/bold bright_green]")
            console.print(f"[green]Welcome, {username.upper()}[/green]")
            console.print(f"[green]Role: {current_role}[/green]")
            console.print(f"[green]Security Level: {len(user_permissions)}/7[/green]")
            
            time.sleep(2)
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            console.print(f"\n[bold red]ACCESS DENIED![/bold red]")
            console.print(f"[red]Invalid credentials. {remaining} attempts remaining.[/red]")
            time.sleep(2)
    
    console.print("\n[bold red]MAXIMUM LOGIN ATTEMPTS EXCEEDED![/bold red]")
    console.print("[red]Terminal locked for security reasons.[/red]")
    time.sleep(3)
    return False

def check_permission(menu_option):
    """Check if current user has permission to access a menu option"""
    return menu_option in user_permissions

def main_menu():
    """Display main menu with options based on user permissions"""
    global current_user, current_role, user_permissions
    
    while True:
        clear_screen()
        print_ascii_art()
        
        # Display user info panel
        user_panel = Panel(
            f"USER: {current_user.upper()} | ROLE: {current_role} | SECURITY: {len(user_permissions)}/7",
            border_style="bright_cyan",
            box=box.ASCII
        )
        console.print(user_panel)
        
        menu_panel = Panel(
            Align.center(
                Text("MAIN TERMINAL MENU", style="bold bright_cyan")
            ),
            border_style="bright_cyan",
            box=box.DOUBLE
        )
        console.print(menu_panel)
        
        # Create menu table with permission indicators
        table = Table(show_header=False, box=box.ASCII2, border_style="bright_cyan")
        table.add_column("Option", style="bright_green", width=10)
        table.add_column("Description", style="white", width=50)
        table.add_column("Access", style="yellow", width=15)
        
        menu_options = [
            (1, "PERSONAL", "Personal Belongings, and Information"),
            (2, "STATION NEWS", "Latest news and announcements"),
            (3, "SHUTTLE STATUS", "Shuttle fleet status"),
            (4, "FOOD DELIVERY", "Order food and supplies"),
            (5, "BANK", "Credit management and transfers"),
            (6, "MAINTENANCE", "Maintenance systems and notes"),
            (7, "LOGOUT", "Return to login")
        ]
        
        for option, description, access_desc in menu_options:
            if check_permission(option):
                status = "[green]ACCESSIBLE[/green]"
                option_style = f"[{option}]"
            else:
                status = "[red]RESTRICTED[/red]"
                option_style = f"[dim][{option}][/dim]"
            
            table.add_row(option_style, description, status)
        
        console.print(table)
        console.print("\n" + "="*60, style="bright_cyan")
        
        # Only allow selection of accessible options
        accessible_options = [str(opt) for opt in user_permissions]
        choice = Prompt.ask(
            "\n[bold bright_green]SELECT OPTION[/bold bright_green]",
            choices=accessible_options,
            default=accessible_options[0] if accessible_options else "6"
        )
        
        choice = int(choice)
        
        if choice == 1 and check_permission(1):
            personal_menu()
        elif choice == 2 and check_permission(2):
            station_news()
        elif choice == 3 and check_permission(3):
            shuttle_status()
        elif choice == 4 and check_permission(4):
            food_delivery()
        elif choice == 5 and check_permission(5):
            bank_menu()
        elif choice == 6 and check_permission(6):
            maintenance_menu()
        elif choice == 7:
            if Confirm.ask("[bold red]CONFIRM LOGOUT?[/bold red]"):
                logout_user()
                break

def station_news():
    """Display station news articles"""
    clear_screen()
    console.print(Panel("[bold cyan]STATION NEWS NETWORK[/bold cyan]", border_style="cyan"))
    
    try:
        with open('news.txt', 'r') as f:
            news_articles = []
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    title, body = line.split('|', 1)
                    news_articles.append((title, body))
        
        if not news_articles:
            console.print("[yellow]No news articles available.[/yellow]")
        else:
            for i, (title, body) in enumerate(news_articles, 1):
                console.print(f"\n[bold bright_green]{i}. {title}[/bold bright_green]")
                console.print(f"[white]{body}[/white]")
                console.print("─" * 80, style="dim")
        
    except FileNotFoundError:
        console.print("[red]ERROR: news.txt not found![/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to main menu[/bold green]")

def shuttle_status():
    """Display ominous shuttle status"""
    clear_screen()
    console.print(Panel("[bold red]SHUTTLE FLEET STATUS[/bold red]", border_style="red"))
    
    console.print("\n" * 5)
    console.print(Align.center("[bold red]ALL SHUTTLES OFFLINE[/bold red]"))
    console.print("\n" * 2)
    console.print(Align.center("[red]EMERGENCY PROTOCOLS ACTIVATED[/red]"))
    console.print("\n" * 2)
    console.print(Align.center("[dim]Contact engineering for assistance...[/dim]"))
    console.print("\n" * 5)
    
    Prompt.ask("\n[bold green]Press ENTER to return to main menu[/bold green]")

def food_delivery():
    """Food delivery system with credit deduction"""
    clear_screen()
    console.print(Panel("[bold cyan]FOOD DELIVERY SYSTEM[/bold cyan]", border_style="cyan"))
    
    # Load user holos
    holos = load_user_holos()
    user_balance = holos.get(current_user, 0)
    
    console.print(f"\n[green]Current Balance: {user_balance} holos[/green]")
    console.print("=" * 50)
    
    # Load food menu
    try:
        with open('food_menu.txt', 'r') as f:
            food_items = []
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    item, price = line.split('|')
                    food_items.append((item, int(price)))
        
        if not food_items:
            console.print("[yellow]No food items available.[/yellow]")
            Prompt.ask("\n[bold green]Press ENTER to return to main menu[/bold green]")
            return
        
        # Display food menu
        food_table = Table(title="Available Food Items", box=box.ASCII2, border_style="cyan")
        food_table.add_column("Item", style="bright_green")
        food_table.add_column("Price", style="yellow")
        food_table.add_column("Item #", style="white")
        
        for i, (item, price) in enumerate(food_items, 1):
            food_table.add_row(item, f"{price} holos", str(i))
        
        console.print(food_table)
        
        # Get user selection
        choice = IntPrompt.ask(
            "\n[bold green]Select item number to order[/bold green]"
        )

        quantity = IntPrompt.ask(
            "\n[bold green]How many would you like to order?[/bold green]"
        )
        
        if 1 <= choice <= len(food_items):
            selected_item, price = food_items[choice - 1]
            
            if user_balance >= price:
                # Process order
                holos[current_user] -= price * quantity
                if save_user_holos(holos):
                    console.print(f"\n[bold bright_green]ORDER CONFIRMED![/bold bright_green]")
                    console.print(f"[green]You ordered: {selected_item}[/green]")
                    console.print(f"[green]Cost: {price * quantity} holos[/green]")
                    console.print(f"[green]New Balance: {holos[current_user]} holos[/green]")
                    console.print(f"\n[yellow]Your order will be delivered to your quarters within 30 minutes.[/yellow]")

                    try:
                        with open('user_inventory.txt', 'a') as f:
                            f.write(f"{current_user}:{selected_item}|{selected_item}|{quantity}\n")
                    except Exception as e:
                        console.print(f"[red]ERROR: Could not add item to inventory: {e}[/red]")
                        Prompt.ask("\n[bold green]Press ENTER to return to food delivery menu[/bold green]")
                        return
                else:
                    console.print("[red]ERROR: Could not process payment![/red]")
            else:
                console.print(f"\n[bold red]INSUFFICIENT FUNDS![/bold red]")
                console.print(f"[red]Item costs {price} holos, but you only have {user_balance} holos.[/red]")
        
    except FileNotFoundError:
        console.print("[red]ERROR: food_menu.txt not found![/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to main menu[/bold green]")

def bank_menu():
    """Bank menu with credit management options"""
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]BANKING SYSTEM[/bold cyan]", border_style="cyan"))
        
        # Load user holos
        holos = load_user_holos()
        user_balance = holos.get(current_user, 0)
        
        console.print(f"\n[green]Current Balance: {user_balance} holos[/green]")
        console.print("=" * 50)
        
        console.print("\n[bold yellow]BANKING OPTIONS:[/bold yellow]")
        
        bank_table = Table(show_header=False, box=box.ASCII2, border_style="cyan")
        bank_table.add_column("Option", style="bright_green", width=10)
        bank_table.add_column("Description", style="white", width=50)
        
        bank_options = [
            ("1", "Check Balance"),
            ("2", "Transfer holos"),
            ("3", "Return to Main Menu")
        ]
        
        for option, description in bank_options:
            bank_table.add_row(f"[{option}]", description)
        
        console.print(bank_table)
        
        choice = Prompt.ask(
            "\n[bold bright_green]SELECT OPTION[/bold bright_green]",
            choices=["1", "2", "3"],
            default="3"
        )
        
        if choice == "1":
            check_balance()
        elif choice == "2":
            transfer_holos()
        elif choice == "3":
            break

def check_balance():
    """Display current user's credit balance"""
    clear_screen()
    console.print(Panel("[bold cyan]ACCOUNT BALANCE[/bold cyan]", border_style="cyan"))
    
    # Load user holos
    holos = load_user_holos()
    user_balance = holos.get(current_user, 0)
    
    console.print("\n" * 3)
    console.print(Align.center(f"[bold bright_green]CURRENT BALANCE[/bold bright_green]"))
    console.print(Align.center(f"[bold bright_green]{user_balance} holos[/bold bright_green]"))
    console.print("\n" * 3)
    
    # Show recent transactions (placeholder for future enhancement)
    console.print("[dim]Recent transactions will appear here in future updates.[/dim]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to bank menu[/bold green]")

def transfer_holos():
    """Transfer holos between users"""
    clear_screen()
    console.print(Panel("[bold cyan]CREDIT TRANSFER SYSTEM[/bold cyan]", border_style="cyan"))
    
    # Load user holos
    holos = load_user_holos()
    user_balance = holos.get(current_user, 0)
    
    console.print(f"\n[green]Your Balance: {user_balance} holos[/green]")
    console.print("=" * 50)
    
    # Get recipient
    recipient = Prompt.ask("\n[bold green]Enter recipient username[/bold green]")
    
    if recipient not in holos:
        console.print(f"[red]ERROR: User '{recipient}' not found![/red]")
        Prompt.ask("\n[bold green]Press ENTER to retry transfer[/bold green]")
        transfer_holos()
    
    
    # Get transfer amount
    try:
        amount = IntPrompt.ask(
            "[bold green]Enter amount to transfer[/bold green]"
        )
        if amount > user_balance and recipient != current_user:
            console.print(f"[red]ERROR: Insufficient funds! You only have {user_balance} holos.[/red]")
            Prompt.ask("\n[bold green]Press ENTER to retry transfer[/bold green]")
            transfer_holos()
        if amount < 0:
            console.print("[red]ERROR: Invalid amount![/red]")
            Prompt.ask("\n[bold green]Press ENTER to retry transfer[/bold green]")
            transfer_holos()
    except ValueError:
        console.print("[red]ERROR: Invalid amount![/red]")
        Prompt.ask("\n[bold green]Press ENTER to return to bank menu[/bold green]")
        return
    
    # Confirm transfer
    if Confirm.ask(f"[bold yellow]Confirm transfer of {amount} holos to {recipient}?[/bold yellow]"):
        # Process transfer
        if recipient == current_user:
            holos[current_user] += amount
        else:
            holos[current_user] -= amount
            holos[recipient] += amount
        
        if save_user_holos(holos):
            console.print(f"\n[bold bright_green]TRANSFER SUCCESSFUL![/bold bright_green]")
            console.print(f"[green]Transferred {amount} holos to {recipient}[/green]")
            console.print(f"[green]Your new balance: {holos[current_user]} holos[/green]")
            console.print(f"[green]{recipient}'s new balance: {holos[recipient]} holos[/green]")
        else:
            console.print("[red]ERROR: Transfer failed![/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to bank menu[/bold green]")
    return

def maintenance_menu():
    """Maintenance menu with sub-options"""
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]MAINTENANCE SYSTEMS[/bold cyan]", border_style="cyan"))
        
        console.print("\n[bold yellow]MAINTENANCE OPTIONS:[/bold yellow]")
        console.print("=" * 40)
        
        maintenance_table = Table(show_header=False, box=box.ASCII2, border_style="cyan")
        maintenance_table.add_column("Option", style="bright_green", width=10)
        maintenance_table.add_column("Description", style="white", width=50)
        
        maintenance_options = [
            ("1", "Open Maintenance Hatch"),
            ("2", "View Maintenance Notes"),
            ("3", "Return to Main Menu")
        ]
        
        for option, description in maintenance_options:
            maintenance_table.add_row(f"[{option}]", description)
        
        console.print(maintenance_table)
        
        choice = Prompt.ask(
            "\n[bold bright_green]SELECT OPTION[/bold bright_green]",
            choices=["1", "2", "3"],
            default="3"
        )
        
        if choice == "1":
            open_maintenance_hatch()
        elif choice == "2":
            view_maintenance_notes()
        elif choice == "3":
            break

def open_maintenance_hatch():
    """Open maintenance hatch with user input"""
    clear_screen()
    console.print(Panel("[bold cyan]MAINTENANCE HATCH ACCESS[/bold cyan]", border_style="cyan"))
    
    console.print("\n[yellow]Enter maintenance hatch number to access:[/yellow]")
    
    try:
        hatch_number = Prompt.ask("[bold green]Hatch Number[/bold green]")
        
        if hatch_number:
            console.print(f"\n[green]Accessing Hatch-{hatch_number}...[/green]")
            time.sleep(1)
            
            # Simulate hatch opening
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold green]>>[/bold green] {task.description}"),
                BarColumn(bar_width=30, complete_style="bright_green"),
                console=console
            ) as progress:
                task = progress.add_task("OPENING HATCH", total=100)
                while not progress.finished:
                    progress.update(task, advance=1)
                    time.sleep(0.02)
            
            console.print(f"\n[bold bright_green]HATCH-{hatch_number} OPENED SUCCESSFULLY[/bold bright_green]")
            console.print(f"[green]Maintenance access granted.[/green]")
        else:
            console.print("[red]ERROR: Invalid hatch number![/red]")
    
    except Exception as e:
        console.print(f"[red]ERROR: {e}[/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to maintenance menu[/bold green]")

def view_maintenance_notes():
    """Display maintenance notes from file"""
    clear_screen()
    console.print(Panel("[bold cyan]MAINTENANCE NOTES[/bold cyan]", border_style="cyan"))
    
    try:
        with open('maintenance_notes.txt', 'r') as f:
            notes = []
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    hatch, note = line.split('|', 1)
                    notes.append((hatch, note))
        
        if not notes:
            console.print("[yellow]No maintenance notes available.[/yellow]")
        else:
            for hatch, note in notes:
                console.print(f"\n[bold bright_green]{hatch}[/bold bright_green]")
                console.print(f"[white]{note}[/white]")
                console.print("─" * 80, style="dim")
        
    except FileNotFoundError:
        console.print("[red]ERROR: maintenance_notes.txt not found![/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to maintenance menu[/bold green]")

def logout_user():
    """Logout current user and return to login"""
    global current_user, current_role, user_permissions
    
    console.print(f"\n[bold yellow]Logging out {current_user}...[/bold yellow]")
    time.sleep(1)
    console.print("[green]User session terminated successfully.[/green]")
    time.sleep(1)
    
    current_user = None
    current_role = None
    user_permissions = []

def exit_terminal():
    """Exit terminal with shutdown sequence"""
    console.print("\n[bold red]INITIATING SHUTDOWN SEQUENCE...[/bold red]")
    time.sleep(1)
    console.print("[red]Logging out user...[/red]")
    time.sleep(1)
    console.print("[red]Closing all connections...[/red]")
    time.sleep(1)
    console.print("[bold bright_green]Goodbye, user. Iron Ring terminal signing off.[/bold bright_green]")
    time.sleep(2)

def personal_menu():
    """Personal menu with inventory management options"""
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]PERSONAL MENU[/bold cyan]", border_style="cyan"))
        
        # Load user holos for display
        holos = load_user_holos()
        user_balance = holos.get(current_user, 0)
        
        console.print(f"\n[green]Current Balance: {user_balance} holos[/green]")
        console.print("=" * 50)
        
        console.print("\n[bold yellow]PERSONAL OPTIONS:[/bold yellow]")
        
        personal_table = Table(show_header=False, box=box.ASCII2, border_style="cyan")
        personal_table.add_column("Option", style="bright_green", width=10)
        personal_table.add_column("Description", style="white", width=50)
        
        personal_options = [
            ("1", "Inventory - View Character Sheet & Items"),
            ("2", "Manage Inventory - Add/Delete Items"),
            ("3", "Return to Main Menu")
        ]
        
        for option, description in personal_options:
            personal_table.add_row(f"[{option}]", description)
        
        console.print(personal_table)
        
        choice = Prompt.ask(
            "\n[bold bright_green]SELECT OPTION[/bold bright_green]",
            choices=["1", "2", "3"],
            default="3"
        )
        
        if choice == "1":
            view_inventory()
        elif choice == "2":
            manage_inventory()
        elif choice == "3":
            break

def view_inventory():
    """Display user's character sheet and inventory"""
    clear_screen()
    console.print(Panel("[bold cyan]CHARACTER INVENTORY[/bold cyan]", border_style="cyan"))
    
    # Load user holos
    holos = load_user_holos()
    user_balance = holos.get(current_user, 0)
    
    # Display character info
    console.print(f"\n[bold bright_green]CHARACTER INFORMATION[/bold bright_green]")
    console.print("=" * 50)
    console.print(f"[white]Username: {current_user.upper()}[/white]")
    console.print(f"[white]Role: {current_role}[/white]")
    console.print(f"[white]Holo Balance: {user_balance} holos[/white]")
    console.print(f"[white]Security Level: {len(user_permissions)}/7[/white]")

    console.print("\n" + "=" * 50)
    
    # Load and display inventory
    try:
        with open('user_inventory.txt', 'r') as f:
            user_items = []
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    username, item_info = line.split(':', 1)
                    if username == current_user:
                        if '|' in item_info:
                            item_name, description, quantity = item_info.split('|')
                            user_items.append((item_name, description, quantity))
            
            if not user_items:
                console.print("\n[yellow]No items in inventory.[/yellow]")
            else:
                console.print(f"\n[bold bright_green]INVENTORY ITEMS ({len(user_items)} items)[/bold bright_green]")
                
                inventory_table = Table(title="Personal Inventory", box=box.ASCII2, border_style="cyan")
                inventory_table.add_column("Item", style="bright_green")
                inventory_table.add_column("Description", style="white")
                inventory_table.add_column("Quantity", style="yellow")
                
                for item_name, description, quantity in user_items:
                    inventory_table.add_row(item_name, description, quantity)
                
                console.print(inventory_table)
        
    except FileNotFoundError:
        console.print("[red]ERROR: user_inventory.txt not found![/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to personal menu[/bold green]")

def manage_inventory():
    """Manage inventory - add or delete items"""
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]INVENTORY MANAGEMENT[/bold cyan]", border_style="cyan"))
        
        console.print("\n[bold yellow]MANAGEMENT OPTIONS:[/bold yellow]")
        
        manage_table = Table(show_header=False, box=box.ASCII2, border_style="cyan")
        manage_table.add_column("Option", style="bright_green", width=10)
        manage_table.add_column("Description", style="white", width=50)
        
        manage_options = [
            ("1", "Add New Item"),
            ("2", "Delete Item"),
            ("3", "Return to Personal Menu")
        ]
        
        for option, description in manage_options:
            manage_table.add_row(f"[{option}]", description)
        
        console.print(manage_table)
        
        choice = Prompt.ask(
            "\n[bold bright_green]SELECT OPTION[/bold bright_green]",
            choices=["1", "2", "3"],
            default="3"
        )
        
        if choice == "1":
            add_inventory_item()
        elif choice == "2":
            delete_inventory_item()
        elif choice == "3":
            break

def add_inventory_item():
    """Add a new item to user's inventory"""
    clear_screen()
    console.print(Panel("[bold cyan]ADD INVENTORY ITEM[/bold cyan]", border_style="cyan"))
    
    console.print("\n[yellow]Enter item details:[/yellow]")
    
    item_name = Prompt.ask("[bold green]Item Name[/bold green]")
    if not item_name:
        console.print("[red]ERROR: Item name cannot be empty![/red]")
        Prompt.ask("\n[bold green]Press ENTER to return to inventory management[/bold green]")
        return
    
    description = Prompt.ask("[bold green]Item Description[/bold green]")
    if not description:
        console.print("[red]ERROR: Item description cannot be empty![/red]")
        Prompt.ask("\n[bold green]Press ENTER to return to inventory management[/bold green]")
        return
    
    quantity = Prompt.ask(
        "[bold green]Quantity[/bold green]",
        default="1"
    )
    
    # Add item to inventory file
    try:
        with open('user_inventory.txt', 'a') as f:
            f.write(f"{current_user}:{item_name}|{description}|{quantity}\n")
        
        console.print(f"\n[bold bright_green]ITEM ADDED SUCCESSFULLY![/bold bright_green]")
        console.print(f"[green]Added: {item_name}[/green]")
        console.print(f"[green]Quantity: {quantity}[/green]")
        
    except Exception as e:
        console.print(f"[red]ERROR: Could not add item: {e}[/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to inventory management[/bold green]")

def delete_inventory_item():
    """Delete an item from user's inventory"""
    clear_screen()
    console.print(Panel("[bold cyan]DELETE INVENTORY ITEM[/bold cyan]", border_style="cyan"))
    
    # Load current inventory
    try:
        with open('user_inventory.txt', 'r') as f:
            lines = f.readlines()
        
        user_items = []
        for line in lines:
            line = line.strip()
            if line and ':' in line:
                username, item_info = line.split(':', 1)
                if username == current_user:
                    if '|' in item_info:
                        item_name, description, quantity = item_info.split('|')
                        user_items.append((item_name, description, quantity))
        
        if not user_items:
            console.print("\n[yellow]No items in inventory to delete.[/yellow]")
            Prompt.ask("\n[bold green]Press ENTER to return to inventory management[/bold green]")
            return
        
        # Display items for selection
        console.print(f"\n[bold yellow]SELECT ITEM TO DELETE:[/bold yellow]")
        
        delete_table = Table(title="Your Inventory", box=box.ASCII2, border_style="cyan")
        delete_table.add_column("Item #", style="bright_green")
        delete_table.add_column("Item", style="white")
        delete_table.add_column("Description", style="cyan")
        delete_table.add_column("Quantity", style="yellow")
        
        for i, (item_name, description, quantity) in enumerate(user_items, 1):
            delete_table.add_row(str(i), item_name, description, quantity)
        
        console.print(delete_table)
        
        # Get user selection
        try:
            choice = IntPrompt.ask(
                "\n[bold green]Select item number to delete[/bold green]"
            )
            
            if 1 <= choice <= len(user_items):
                selected_item = user_items[choice - 1][0]
                
                if Confirm.ask(f"[bold red]Confirm deletion of '{selected_item}'?[/bold red]"):
                    # Remove the item from the file
                    new_lines = []
                    item_found = False
                    
                    for line in lines:
                        line = line.strip()
                        if line and ':' in line:
                            username, item_info = line.split(':', 1)
                            if username == current_user and item_info.startswith(selected_item + '|'):
                                item_found = True
                                continue  # Skip this line (delete the item)
                        new_lines.append(line)
                    
                    if item_found:
                        # Write back the file without the deleted item
                        with open('user_inventory.txt', 'w') as f:
                            for line in new_lines:
                                f.write(line + '\n')
                        
                        console.print(f"\n[bold bright_green]ITEM DELETED SUCCESSFULLY![/bold bright_green]")
                        console.print(f"[green]Deleted: {selected_item}[/green]")
                    else:
                        console.print("[red]ERROR: Item not found in inventory![/red]")
                
        except ValueError:
            console.print("[red]ERROR: Invalid selection![/red]")
        
    except FileNotFoundError:
        console.print("[red]ERROR: user_inventory.txt not found![/red]")
    except Exception as e:
        console.print(f"[red]ERROR: {e}[/red]")
    
    Prompt.ask("\n[bold green]Press ENTER to return to inventory management[/bold green]")

@app.command()
def main():
    """Iron Ring Space Station Terminal - Retro DOS Style CLI"""
    try:
        while True:
            clear_screen()
            print_ascii_art()
            loading_screen()
            
            if not login_screen():
                console.print("\n[bold red]TERMINAL LOCKED. EXITING.[/bold red]")
                break
            
            main_menu()
            
            # After logout, ask if user wants to exit completely
            if Confirm.ask("\n[bold yellow]Exit terminal completely?[/bold yellow]"):
                exit_terminal()
                break
                
    except KeyboardInterrupt:
        console.print("\n\n[bold red]TERMINAL INTERRUPTED BY USER[/bold red]")
        exit_terminal()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app()
