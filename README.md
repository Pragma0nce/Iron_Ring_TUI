# Iron Ring Space Station Terminal

A retro DOS-style CLI application for your D&D campaign, simulating a computer terminal on the Iron Ring space station.

## Features

- **Retro DOS Styling**: Authentic ASCII art and terminal aesthetics
- **Loading Screen**: System boot sequence with progress bars
- **User Authentication**: Login system with username/password
- **Role-Based Access Control**: Different users have access to different features
- **Interactive Menu System**: Navigate through various station systems

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## User Accounts

The system comes with pre-configured user accounts:

| Username | Password | Role | Access Level |
|----------|----------|------|--------------|
| `admin` | `admin123` | ADMIN | Full access (all screens) |
| `captain` | `captain2024` | COMMAND | Full access (all screens) |
| `engineer` | `tech456` | ENGINEERING | Full access (all screens) |
| `security` | `secure789` | SECURITY | Full access (all screens) |
| `medical` | `med123` | MEDICAL | Full access (all screens) |
| `science` | `research321` | SCIENCE | Full access (all screens) |
| `cargo` | `cargo555` | CARGO | Full access (all screens) |
| `guest` | `visitor` | GUEST | News, Shuttle Status, Food Delivery |

## Available Screens

1. **Personal** - Personal belongings and character management with two sub-options:
   - Inventory: View character sheet and current inventory items
   - Manage Inventory: Add or delete items from personal inventory
2. **Station News** - Latest news articles and announcements from the station
3. **Shuttle Status** - Ominous "ALL SHUTTLES OFFLINE" display
4. **Food Delivery** - Order food items with credit deduction from user account
5. **Bank** - Credit management system with two options:
   - Check Balance: View current credit balance
   - Transfer Credits: Transfer credits between users
6. **Maintenance** - Maintenance systems with sub-options:
   - Open Maintenance Hatch: Input hatch number to access
   - View Maintenance Notes: Display maintenance notes from file
7. **Logout** - Return to login screen

## File Structure

- `main.py` - Main application file
- `users.txt` - User credentials and roles
- `permissions.txt` - Role-based access permissions
- `user_holos.txt` - User holo balances for food delivery and transfers
- `user_inventory.txt` - User inventory items (Item|Description|Rarity format)
- `news.txt` - News articles (Title|Body format)
- `food_menu.txt` - Food items and prices (Item|Price format)
- `maintenance_notes.txt` - Maintenance notes (Hatch|Note format)
- `requirements.txt` - Python dependencies

## Credit System

Each user starts with a credit balance:
- **Admin**: 1000 credits
- **Captain**: 1500 credits
- **Engineer**: 800 credits
- **Security**: 1200 credits
- **Medical**: 900 credits
- **Science**: 750 credits
- **Cargo**: 600 credits
- **Guest**: 100 credits

Credits are used for:
- Food delivery orders
- Transferring between users

## Customization

### Adding New Users

Edit `users.txt` and add a new line:
```
newuser:password:ROLE
```

### Modifying Permissions

Edit `permissions.txt` and modify the role's access list:
```
ROLE:1,2,3,4,5,6
```

Numbers represent menu options (1=News, 2=Shuttle Status, 3=Food Delivery, 4=Transfer Credits, 5=Maintenance, 6=Logout)

### Adding New Roles

1. Add the role to `users.txt` with a user
2. Add the role and permissions to `permissions.txt`
3. Add the user and starting credits to `user_credits.txt`

### Adding News Articles

Edit `news.txt` and add a new line:
```
Title|Article body text here
```

### Adding Food Items

Edit `food_menu.txt` and add a new line:
```
Food Item Name|Price in credits
```

### Adding Maintenance Notes

Edit `maintenance_notes.txt` and add a new line:
```
Hatch-XXX|Maintenance note description
```

## Security Features

- 3 login attempts before terminal lock
- Password masking during input
- Role-based menu restrictions
- Session management with logout functionality
- Credit balance validation for purchases

## D&D Campaign Integration

This terminal can be used to:
- Give players different access levels based on their character roles
- Create tension with the ominous shuttle status
- Allow players to manage resources through the credit system
- Provide atmospheric immersion in your space station setting
- Create plot hooks through news articles and maintenance notes

## Troubleshooting

- Ensure all text files exist in the same directory as `main.py`
- Check that all required Python packages are installed
- Verify file permissions allow reading and writing the text files
- Make sure credit balances are properly formatted in `user_credits.txt`

## License

This is a D&D campaign tool - feel free to modify and use as needed for your game!
